#!/usr/bin/env python3
"""Build the Frost Law Group search audit (single-file HTML) from the
Search Console exports and market-data exports in ../data.
Run: python3 build/build_report.py   (set ART_OUT=<path> to also write an artifact fragment)"""
import csv
import collections
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charts as C  # noqa: E402
import diagrams as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
MKT = os.path.join(DATA, "market")
OUT = os.path.join(ROOT, "report", "frost-law-group-search-audit.html")
FONTS = os.path.join(ROOT, "build", "fonts", "fonts-embedded.css")

esc = C.esc
fmt = C.fmt


# ----------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------
def load_csv(name):
    with open(os.path.join(DATA, name)) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("clicks", "impressions"):
            if k in r:
                r[k] = int(r[k])
        if "position" in r:
            r["position"] = float(r["position"])
        if "date" in r:
            r["date"] = date.fromisoformat(r["date"])
    return rows


def load_json(path):
    with open(path) as f:
        return json.load(f)


frost_daily = load_csv("frost_daily.csv")
frost_nb_daily = load_csv("frost_nonbrand_daily.csv")
sva_daily = load_csv("sva_daily.csv")
frost_pages = load_csv("frost_pages.csv")
sva_pages = load_csv("sva_pages.csv")
devices = load_json(os.path.join(DATA, "devices.json"))
frost_q = load_json(os.path.join(DATA, "frost_queries_2026-06-08_to_2026-09-08.json"))["rows"]
frost_qp = load_json(os.path.join(DATA, "frost_query_page_2026-06-08_to_2026-09-08.json"))["rows"]
sva_qp = load_json(os.path.join(DATA, "sva_query_page_2026-06-08_to_2026-09-08.json"))["rows"]
agg = load_json(os.path.join(DATA, "aggregates.json"))

# market data (volumes, CPC, map packs, competitor benchmarks) — never attributed by vendor in the report
KM = {r["keyword"]: r for r in load_json(os.path.join(MKT, "keyword_metrics.json"))}
MAP = load_json(os.path.join(MKT, "map_pack.json"))
VIS = load_json(os.path.join(MKT, "serp_competitors.json"))
NOTES = load_json(os.path.join(MKT, "serp_notes.json"))
BENCH = load_json(os.path.join(MKT, "domain_benchmarks.json"))
GAP = load_json(os.path.join(MKT, "keyword_gap.json"))
FROST_RANKED = load_json(os.path.join(MKT, "frost_ranked_summary.json"))

BRAND = re.compile(r"frost", re.I)
QRE = re.compile(r"^(who|which|what|where|how|when|why|is it|can |does |do |should )", re.I)
INJ = re.compile(r"accident|injury|crash|wreck|slip|dog bite|wrongful death|lyft|uber|truck|motorcycle", re.I)


def totals(rows):
    c = sum(r["clicks"] for r in rows)
    i = sum(r["impressions"] for r in rows)
    p = (sum(r["position"] * r["impressions"] for r in rows) / i) if i else 0
    return dict(clicks=c, impressions=i, ctr=(c / i if i else 0), position=p)


F = totals(frost_daily)
FNB = totals(frost_nb_daily)
S = totals(sva_daily)
F_DAYS, S_DAYS = len(frost_daily), len(sva_daily)
F_FIRST, F_LAST = frost_daily[0]["date"], frost_daily[-1]["date"]
S_FIRST, S_LAST = sva_daily[0]["date"], sva_daily[-1]["date"]

brand_rows = [r for r in frost_q if BRAND.search(r["keys"][0])]
nb_rows = [r for r in frost_q if not BRAND.search(r["keys"][0])]
B = totals([dict(clicks=r["clicks"], impressions=r["impressions"], position=r["position"]) for r in brand_rows])
NB = totals([dict(clicks=r["clicks"], impressions=r["impressions"], position=r["position"]) for r in nb_rows])
HID = dict(clicks=F["clicks"] - B["clicks"] - NB["clicks"], impressions=F["impressions"] - B["impressions"] - NB["impressions"])


def collapse(rows):
    out = collections.OrderedDict()
    for r in rows:
        q, p = r["keys"]
        a = out.setdefault(q, dict(clicks=0, impressions=0, wp=0.0, pages={}))
        a["clicks"] += r["clicks"]
        a["impressions"] += r["impressions"]
        a["wp"] += r["position"] * r["impressions"]
        a["pages"][p] = a["pages"].get(p, 0) + r["impressions"]
    for q, a in out.items():
        a["position"] = a["wp"] / a["impressions"] if a["impressions"] else 0
    return out


sq = collapse(sva_qp)
fq_all = collapse(frost_qp)

fan = [(q, a) for q, a in fq_all.items() if QRE.match(q)]
fan.sort(key=lambda x: -x[1]["impressions"])
FAN_N = len(fan)
FAN_I = sum(a["impressions"] for _, a in fan)

qw = {}
for r in frost_qp:
    q, p = r["keys"]
    if BRAND.search(q) or not p.startswith("https://frostlawgroupsc.com/"):
        continue
    if 4 <= r["position"] <= 20 and r["impressions"] >= 5:
        if q not in qw or r["impressions"] > qw[q]["impressions"]:
            qw[q] = dict(query=q, page=p, impressions=r["impressions"], position=r["position"])
quick_frost = sorted(qw.values(), key=lambda x: -x["impressions"])

ACTIONS = [
    (r"executor|probate", "Add an “Executor duties & disputes” section and FAQ to /probate; publish a dedicated answer page."),
    (r"asset protection", "New page: Asset Protection Trusts in South Carolina (link from Estate Planning)."),
    (r"\bwills?\b", "Retitle /last-will-and-testament for “wills lawyer Summerville SC”; add cost & process FAQ."),
    (r"trust amend|restate", "New answer page: Amending or restating a revocable trust in SC."),
    (r"trust", "Retitle /revocable-trust; add “trust vs. will” FAQ and video."),
    (r"power of attorney|living will", "Retitle /power-of-attorney and /living-will; cross-link the two."),
    (r"blended", "New answer page: Estate planning for blended families in SC."),
    (r"guardian|conservator", "New page: Guardianship & Conservatorship (contested cases) in Dorchester/Berkeley County."),
    (r"dui|drunk", "New page: Summerville DUI Lawyer (first offense, DUAC, implied consent)."),
    (r"drug", "New page: Drug charge defense in Summerville."),
    (r"criminal", "Retitle and expand /criminal-defense; add DUI, drug and CDV child pages."),
    (r"inherit", "New answer page: Managing inherited assets in SC."),
]


def action_for(q):
    for pat, txt in ACTIONS:
        if re.search(pat, q, re.I):
            return txt
    return "Publish a short answer page for this exact question; link it from the closest practice page."


quick_sva = sorted([(q, a) for q, a in sq.items() if a["position"] <= 35 and a["impressions"] >= 3 and not BRAND.search(q)],
                   key=lambda x: (x[1]["position"]))

DEAD = collections.OrderedDict([
    ("/goose-creek/", "new Goose Creek car-accident page (/areas/goose-creek)"),
    ("/attorneys/", "/about"),
    ("/truck-accident-3/", "/practice-areas/truck-accidents"),
    ("/blog/", "rebuilt /blog"),
    ("/summerville/", "home page (or /areas/summerville)"),
    ("/mt-pleasant/", "new /areas/mount-pleasant"),
    ("/motorcycle-accident/", "/practice-areas/motorcycle-accidents"),
    ("/wrongful-death-2/", "/practice-areas/wrongful-death"),
    ("/north-charleston/", "new /areas/north-charleston"),
    ("/car-accident/", "/practice-areas/car-accidents"),
    ("/walterboro/", "new /areas/walterboro"),
    ("/moncks-corner/", "new /areas/moncks-corner"),
    ("/results/", "/about (or a new case-results page)"),
    ("/serving/", "new /areas index"),
    ("/charleston/", "new /areas/charleston"),
    ("/other-areas/", "new /areas index"),
    ("/west-ashley/", "new /areas/west-ashley"),
])
dead_rows = []
for r in sva_pages:
    path = re.sub(r"^https?://(www\.)?summervilleaccidentattorney\.com", "", r["url"])
    if path in DEAD:
        dead_rows.append(dict(path=path, impressions=r["impressions"], position=r["position"], to=DEAD[path]))
dead_rows.sort(key=lambda x: -x["impressions"])
DEAD_I = sum(r["impressions"] for r in dead_rows)
SVA_PAGE_I = sum(r["impressions"] for r in sva_pages)

groups = collections.OrderedDict()
for r in frost_pages:
    path = re.sub(r"^https?://(www\.)?frostlawgroupsc\.com", "", r["url"]).rstrip("/") or "/"
    g = groups.setdefault(path, dict(path=path, clicks=0, impressions=0, wp=0.0, variants=[]))
    g["clicks"] += r["clicks"]
    g["impressions"] += r["impressions"]
    g["wp"] += r["position"] * r["impressions"]
    g["variants"].append(r["url"])
page_groups = sorted(groups.values(), key=lambda g: -g["impressions"])
for g in page_groups:
    g["position"] = g["wp"] / g["impressions"] if g["impressions"] else 0
MULTI = [g for g in page_groups if len(g["variants"]) > 1]

home_www = next(r for r in frost_pages if r["url"] == "http://www.frostlawgroupsc.com/")
home_https = next(r for r in frost_pages if r["url"] == "https://frostlawgroupsc.com/")

topics = agg["frost_topic_buckets"]
fh = agg["frost_pos_hist_nonbrand"]
sh = agg["sva_pos_hist"]
sva_city = agg["sva_city_buckets"]
sva_pr = agg["sva_practice_buckets"]
overlap = [o for o in agg["cross_site_overlap"] if o["sva_impr"] + o["frost_impr"] >= 6][:12]

top_frost_nb = sorted(nb_rows, key=lambda r: -r["impressions"])[:60]
top_frost_brand = sorted(brand_rows, key=lambda r: -r["clicks"])[:12]
top_sva = sorted(sq.items(), key=lambda x: -x[1]["impressions"])[:60]
spanish = [(q, a) for q, a in sq.items() if "abogad" in q]
SPAN_I = sum(a["impressions"] for _, a in spanish)
wrong = [(q, a) for q, a in sq.items() if re.search(r"sevierville|schererville|somerville|collierville|placerville|waterville|feasterville", q)]
WRONG_I = sum(a["impressions"] for _, a in wrong)
SVA_Q_I = sum(a["impressions"] for a in sq.values())

# --- market helpers ---------------------------------------------------------
def vol(k):
    r = KM.get(k)
    return r["volume"] if r and r.get("volume") else None


def cpc(k):
    r = KM.get(k)
    return r["cpc"] if r and r.get("cpc") else None


def money(x):
    return "–" if x is None else f"${x:,.0f}" if x >= 10 else f"${x:,.2f}"


def volfmt(k):
    v = vol(k)
    return "–" if v is None else fmt(v)


BENCH_BY = {b["domain"]: b for b in BENCH}
DIRS = {"justia.com", "attorneys.superlawyers.com", "lawyers.law.cornell.edu", "yelp.com", "avvo.com", "lawyers.findlaw.com", "youtube.com"}

# keyword gap: keep the firm's four subjects, drop competitors' unrelated practice areas
KEEP = re.compile(r"probate|estate|\bwill|trust|\bpoa\b|power of attorney|guardian|conservator|executor|inherit|heir|devisee|special needs|elder|medicaid|\bdui\b|duac|criminal|drug|possession|expung|assault|domestic|\bcdv\b|bond|arrest|injury|accident|crash|dog bite|wrongful death|slip|summerville|goose creek|dorchester", re.I)
DROP = re.compile(r"defamation|libel|slander|mediat|common law|life estate|civil law|civil matter|contract|concealed|constitutional carry|divorce|family|custody|real estate|deed|closing|gal attorney|providence|ponce|gail law|illegitimate|barbara|liability insurance|malpractice", re.I)
gap_rows = [g for g in GAP if KEEP.search(g["keyword"]) and not DROP.search(g["keyword"])]
gap_rows.sort(key=lambda g: -(g["volume"] or 0))
GAP_TOP = gap_rows[:32]
PMC_NAME = {"pmclawfirm": "PMC Law Firm", "gilgatchlaw": "Gil Gatch Law", "shelbournelaw": "Shelbourne Law"}


def gap_page(k):
    k = k.lower()
    if re.search(r"poa|power of attorney", k):
        return "/power-of-attorney (deepen: SC requirements, where to get one, healthcare vs. durable)"
    if re.search(r"will and trust|attorney for will|trust lawyer", k):
        return "/last-will-and-testament + /revocable-trust (retitle; add “near me” signals: address, map, county)"
    if re.search(r"special needs", k):
        return "new: Special needs planning"
    if re.search(r"guardian", k):
        return "new: Guardianship & conservatorship"
    if re.search(r"probate judge|probate lawyer|probate lawyers|probate court|probate", k):
        return "/probate (deepen) + county probate court guides"
    if re.search(r"devisee|heir|certified copy|will storing|will amend|inherit", k):
        return "new: Probate & estate glossary / answer pages"
    if re.search(r"injury|accident|crash|dog bite|wrongful death|slip", k):
        return "injury site: hub pages (+ address, map, county on every page)"
    if re.search(r"dui|duac|criminal|drug|possession|expung|assault|domestic|cdv|bond|arrest", k):
        return "/criminal-defense + new DUI / drug / CDV / expungement pages"
    if re.search(r"summerville", k):
        return "home page + attorney bios (retitle; LegalService schema)"
    return "answer page in the matching cluster"


# map-pack derived
mp_rows = []
firms = {}
for q, v in MAP["queries"].items():
    rk = v["frost_rank"]
    mp_rows.append(dict(label=q, value=(rk if rk else 21), note="pack: " + " · ".join(t["name"] for t in v["top"][:3])))
    for t in v["top"][:3]:
        firms[t["name"]] = t
firm_rows = sorted(firms.values(), key=lambda t: -t["reviews"])
review_rows = [dict(label=t["name"], value=t["reviews"], note=f"{t['photos']} photos · {t['rating']}★") for t in firm_rows] + \
              [dict(label="Frost Law Group (you)", value=MAP["frost"]["reviews"], note=f"{MAP['frost']['photos']} photos · {MAP['frost']['rating']}★", color=C.ORANGE)]
review_rows.sort(key=lambda r: -r["value"])
photo_rows = sorted([dict(label=t["name"], value=t["photos"]) for t in firm_rows] + [dict(label="Frost Law Group (you)", value=MAP["frost"]["photos"], color=C.ORANGE)], key=lambda r: -r["value"])
PACK_MEDIAN_REVIEWS = sorted(t["reviews"] for t in firm_rows)[len(firm_rows) // 2]

# value table (head terms)
VALUE_TERMS = [
    ("personal injury lawyer summerville sc", "Injury site"), ("attorney summerville sc", "Main site (home)"), ("lawyer summerville sc", "Main site (home)"),
    ("criminal defense attorney summerville sc", "Main site"), ("estate planning attorney summerville sc", "Main site"), ("probate attorney summerville sc", "Main site"),
    ("dui lawyer summerville sc", "Main site (new DUI page)"), ("elder law attorney summerville sc", "Main site"), ("personal injury lawyer north charleston sc", "Injury site (city page)"),
    ("car accident lawyer charleston sc", "Injury site (Charleston page)"), ("probate lawyer charleston sc", "Main site (Charleston-area probate)"), ("south carolina dui laws", "Main site (answer page)"),
    ("first offense dui south carolina", "Main site (answer page)"), ("how much does estate planning cost", "Main site (answer page)"), ("south carolina power of attorney requirements", "Main site (answer page)"),
    ("living will south carolina", "Main site (living will page)"), ("expungement south carolina", "Main site (new expungement page)"), ("south carolina dog bite law", "Injury site (dog-bite page)"),
]


# ----------------------------------------------------------------------------
# html helpers
# ----------------------------------------------------------------------------
def pct(x, d=1):
    return f"{x * 100:.{d}f}%"


def pos(x):
    return f"{x:.1f}"


def fig(svg, title, sub=None, caption=None):
    return (f'<figure><div class="ft">{title}</div>' + (f'<div class="fs">{sub}</div>' if sub else "") + svg +
            (f"<figcaption>{caption}</figcaption>" if caption else "") + "</figure>")


def plain(text, title="In plain English"):
    return f'<div class="plain"><div class="t">{title}</div><p>{text}</p></div>'


def callout(text, title=None):
    return f'<div class="callout">' + (f"<strong>{title}</strong> " if title else "") + f"{text}</div>"


def table(cols, rows, cls=""):
    th = "".join(f'<th class="{a}">{h}</th>' for h, _, a in cols)
    body = []
    for r in rows:
        tds = []
        for h, k, a in cols:
            v = k(r) if callable(k) else r.get(k, "")
            tds.append(f'<td class="{a}">{v}</td>')
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<div class="tblwrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def todo(items):
    return '<ul class="todo">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def kpis(items):
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="l">{l}</div><div class="v">{v}</div><div class="d">{d}</div></div>' for l, v, d in items) + "</div>"


def sec(id_, eyebrow, title, lead=None):
    return (f'<section class="sec" id="{id_}"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>' +
            (f'<p class="lead">{lead}</p>' if lead else ""))


def pill(kind, text):
    return f'<span class="pill {kind}">{text}</span>'


# ----------------------------------------------------------------------------
# charts
# ----------------------------------------------------------------------------
f_dates = [r["date"] for r in frost_daily]
s_dates = [r["date"] for r in sva_daily]
i_all = [r["impressions"] for r in frost_daily]
i_nb = [r["impressions"] for r in frost_nb_daily]
c_all = [r["clicks"] for r in frost_daily]


def idx(dates, d):
    return dates.index(date.fromisoformat(d))


chart_f_impr = C.line_chart(
    f_dates,
    [dict(name="All impressions", values=i_all, color=C.BLUE),
     dict(name="Non-brand impressions (searches that don't contain “frost”)", values=i_nb, color=C.ORANGE)],
    annotations=[dict(index=idx(f_dates, "2026-09-01"), text="Sep 1: 562 — Business Profile shown for “business law attorney” etc."),
                 dict(index=idx(f_dates, "2026-08-14"), text="Aug 14: 328 — landlord-tenant searches, profile link at #1, 0 clicks"),
                 dict(index=idx(f_dates, "2026-07-16"), text="Jul 16: 263")],
    aria="Daily impressions for frostlawgroupsc.com, all queries vs non-brand queries")
chart_f_clicks = C.columns(f_dates, c_all, color=C.BLUE, aria="Daily clicks for frostlawgroupsc.com")
chart_brand_clicks = C.stacked_bar([("Brand searches (contain “frost”)", B["clicks"], C.BLUE), ("Non-brand searches", NB["clicks"], C.ORANGE), ("Searches Google hides for privacy", HID["clicks"], C.GRAY)], aria="Clicks by search type")
chart_brand_impr = C.stacked_bar([("Brand searches (contain “frost”)", B["impressions"], C.BLUE), ("Non-brand searches", NB["impressions"], C.ORANGE), ("Searches Google hides for privacy", HID["impressions"], C.GRAY)], aria="Impressions by search type")
chart_home = C.hbar([
    dict(label="http://www.frostlawgroupsc.com/ — Business Profile link", value=home_www["impressions"], note=f"{home_www['clicks']} clicks · avg. position {pos(home_www['position'])}", color=C.ORANGE),
    dict(label="https://frostlawgroupsc.com/ — the real home page", value=home_https["impressions"], note=f"{home_https['clicks']} clicks · avg. position {pos(home_https['position'])}", color=C.BLUE),
], label_w=400, note_w=190, aria="Impressions for the two home-page addresses")
chart_topics = C.hbar([dict(label=k, value=v["impressions"], note=f"avg. pos {v['avg_position']} · {v['queries']} queries · {v['clicks']} clicks")
                       for k, v in sorted(topics.items(), key=lambda kv: -kv[1]["impressions"]) if v["impressions"] > 0],
                      label_w=250, note_w=230, highlight={"Estate planning / wills / trusts", "Probate / executor", "DUI", "Criminal defense"},
                      aria="Non-brand impressions by practice-area topic, main site")
chart_f_hist_q = C.bucket_bar([(f"Positions {k}", v["queries"]) for k, v in fh.items()], aria="Non-brand queries by position bucket, main site")
chart_f_hist_i = C.bucket_bar([(f"Positions {k}", v["impressions"]) for k, v in fh.items()], aria="Non-brand impressions by position bucket, main site")
chart_dev_f = C.stacked_bar([("Mobile", devices["frost"]["MOBILE"]["clicks"], C.BLUE), ("Desktop", devices["frost"]["DESKTOP"]["clicks"], C.ORANGE), ("Tablet", devices["frost"]["TABLET"]["clicks"], C.AQUA)], aria="Main site clicks by device")
chart_dev_fi = C.stacked_bar([("Mobile", devices["frost"]["MOBILE"]["impressions"], C.BLUE), ("Desktop", devices["frost"]["DESKTOP"]["impressions"], C.ORANGE), ("Tablet", devices["frost"]["TABLET"]["impressions"], C.AQUA)], aria="Main site impressions by device")
chart_s_impr = C.line_chart(s_dates, [dict(name="Impressions", values=[r["impressions"] for r in sva_daily], color=C.ORANGE)],
                            annotations=[dict(index=idx(s_dates, "2026-07-27"), text="Jul 27: 190"), dict(index=idx(s_dates, "2026-09-04"), text="Sep 4: the one click")],
                            legend=False, area=True, aria="Daily impressions for summervilleaccidentattorney.com")
chart_s_pos = C.line_chart(s_dates, [dict(name="Average position", values=[r["position"] for r in sva_daily], color=C.ORANGE)], legend=False, aria="Daily average position for summervilleaccidentattorney.com")
chart_s_hist_q = C.bucket_bar([(f"Positions {k}", v["queries"]) for k, v in sh.items()], aria="Queries by position bucket, injury site")
chart_s_hist_i = C.bucket_bar([(f"Positions {k}", v["impressions"]) for k, v in sh.items()], aria="Impressions by position bucket, injury site")
chart_s_pr = C.hbar([dict(label=k, value=v["impressions"], note=f"avg. pos {v['avg_position']} · {v['queries']} queries") for k, v in sva_pr.items() if v["impressions"] > 0 and k != "Other"],
                    label_w=250, note_w=170, highlight={"Dog bite", "Motorcycle accident"}, aria="Injury-site impressions by case type")
chart_s_city = C.hbar([dict(label=k, value=v["impressions"], note=f"avg. pos {v['avg_position']} · {v['queries']} queries") for k, v in sva_city.items() if v["impressions"] > 0],
                      label_w=290, note_w=170, highlight={"Goose Creek", "Mt Pleasant", "Moncks Corner", "Walterboro", "North Charleston"}, aria="Injury-site impressions by city named in the search")
chart_dead = C.hbar([dict(label=r["path"], value=r["impressions"], note=f"avg. pos {pos(r['position'])}") for r in dead_rows[:12]], label_w=200, note_w=110, color=C.ORANGE, aria="Impressions still landing on removed pages")
chart_overlap = C.dumbbell([(o["query"], o["frost_pos"], o["sva_pos"]) for o in overlap], "frostlawgroupsc.com", "summervilleaccidentattorney.com", label_w=310, aria="The same injury searches show both sites, both far from page 1")
chart_fan = C.hbar([dict(label=q, value=a["impressions"], note=f"avg. pos {pos(a['position'])}") for q, a in fan[:14]], label_w=540, note_w=90, aria="Question-style (fan-out) searches showing the main site")

# market charts
chart_map = C.hbar([dict(label=r["label"], value=r["value"], note=r["note"], color=(C.ORANGE if r["value"] > 3 else C.AQUA)) for r in mp_rows],
                   label_w=290, note_w=340, max_value=25, value_fmt=lambda v: ("not in top 20" if v >= 21 else f"#{int(v)}"), aria="Frost Law Group's position in the map results for six money searches")
chart_reviews = C.hbar(review_rows, label_w=230, note_w=140, color=C.BLUE, aria="Google reviews: Frost vs. the firms in the map packs")
chart_photos = C.hbar(photo_rows, label_w=230, note_w=0, color=C.BLUE, aria="Business Profile photos: Frost vs. the firms in the map packs")
chart_traffic = C.hbar([dict(label=b["domain"], value=b["est_traffic"], note=f"{fmt(b['keywords'])} ranking keywords", color=(C.ORANGE if "frost" in b["domain"] or "summerville" in b["domain"] else C.BLUE)) for b in sorted(BENCH, key=lambda b: -b["est_traffic"])],
                       label_w=260, note_w=170, aria="Estimated monthly organic visits, Frost sites vs. three Summerville competitors")
chart_links = C.hbar([dict(label=b["domain"], value=b["referring_domains"], note=f"link-quality score {b['rank']} · spam share {b['spam_score']}%", color=(C.ORANGE if "frost" in b["domain"] or "summerville" in b["domain"] else C.BLUE)) for b in sorted([b for b in BENCH if b["referring_domains"]], key=lambda b: -b["referring_domains"])],
                      label_w=260, note_w=230, aria="Referring domains (sites linking in), Frost sites vs. two Summerville competitors")
chart_value = C.hbar([dict(label=k, value=vol(k), note=f"{money(cpc(k))} per click · {site}") for k, site in VALUE_TERMS if vol(k)],
                     label_w=330, note_w=250, aria="Monthly searches and what advertisers pay per click for the head terms")

# diagrams
dia_search = D.flow([("Someone in Summerville searches", "“probate attorney summerville sc”", D.SURF), ("Google shows a results page", "AI answer · map pack · 10 links", D.SURF), ("Your page is on it", "= 1 impression", C.BLUE), ("They click it", "= 1 click", C.NAVY), ("They call or book", "= a lead", D.AZALEA)])
dia_zones = D.serp_zones()
dia_two = D.two_sites()
dia_fan = D.fanout("“Who should I hire to handle my dad’s estate in Summerville?”", [
    ("who handles executor disputes in Summerville probate court?", "Executor duties & disputes page", "gap"),
    ("how long does probate take in South Carolina?", "SC probate timeline page", "gap"),
    ("what does a probate attorney cost in SC?", "Probate fees & costs page", "gap"),
    ("which assets avoid probate in SC?", "/probate (section exists)", "have"),
    ("best-reviewed probate attorney near Summerville", "Business Profile + reviews", "have")])
dia_estate = D.hub_spoke("Estate Planning hub (/estate-planning-attorney)", ["Last will & testament", "Revocable living trust", "Powers of attorney", "Living will", ("Asset protection trusts", "new"), ("Estate planning for blended families", "new"), ("Estate plan reviews & trust amendments", "new"), ("Estate planning for business owners", "new"), ("Special needs planning", "new"), ("What happens without a will in SC", "new"), ("What estate planning costs in SC", "new"), ("Guardianship & conservatorship", "new")])
dia_probate = D.hub_spoke("Probate hub (/probate)", ["SC probate process (existing section)", ("How long probate takes in SC", "new"), ("Executor duties & disputes", "new"), ("Contesting a will in SC", "new"), ("Small-estate / summary administration", "new"), ("Assets that avoid probate", "existing"), ("Probate litigation", "existing"), ("Managing inherited assets", "new"), ("Dorchester County Probate Court guide", "new"), ("Berkeley County Probate Court guide", "new"), ("Charleston County Probate Court guide", "new"), ("Probate costs & fees in SC", "new")], hub_fill=C.NAVY)
dia_crim = D.hub_spoke("Criminal Defense hub (/criminal-defense)", [("Summerville DUI lawyer", "new"), ("First-offense DUI penalties in SC", "new"), ("DUAC & implied consent", "new"), ("Drug charges", "new"), ("CDV / domestic violence", "new"), ("Bond hearings in Dorchester County", "new"), ("Expungement in SC", "new"), ("Traffic tickets & CDL", "new"), ("Juvenile defense", "new"), ("What happens after an arrest in Dorchester County", "new"), ("Summerville Municipal Court guide", "new"), ("Boating under the influence (BUI)", "new")], hub_fill=C.NAVY)
dia_pi = D.hub_spoke("Car Accident hub (/practice-areas/car-accidents)", [("Rear-end collisions", "new"), ("Hit-and-run crashes", "new"), ("Uninsured / underinsured motorist", "new"), ("Drunk-driving crash victims", "new"), ("Uber & Lyft accidents", "new"), ("Delivery-driver injuries", "new"), ("Distracted-driving crashes", "new"), ("I-26 · Hwy 17A · Dorchester Rd crash guide", "new"), ("What to do after a crash in SC", "new"), ("Is SC an at-fault state? (comparative negligence)", "new"), ("SC car-accident statute of limitations", "new"), ("How settlements work in SC", "new")], hub_fill=C.ORANGE, accent=C.ORANGE)
dia_pi2 = D.hub_spoke("Injury site: other hubs", ["Truck accidents", "Motorcycle accidents", "Dog bites (SC strict liability)", "Wrongful death", "Slip & fall", "Workers’ comp", ("Goose Creek", "new"), ("Ladson · Knightsville", "new"), ("Moncks Corner", "new"), ("North Charleston · West Ashley", "new"), ("Mount Pleasant · Charleston", "new"), ("Abogado de accidentes (Spanish)", "new")], hub_fill=C.ORANGE, accent=C.ORANGE)
dia_cycle = D.cycle([("1 answer page", "on the right site", C.NAVY), ("1 YouTube video", "the question is the title", D.SURF), ("3 vertical clips", "YouTube Shorts + Reels", D.SURF), ("1 LinkedIn post", "Tara or Jack, in their voice", D.SURF), ("1 Instagram reel + carousel", "the pups can co-star", D.SURF), ("1 Business Profile post", "with the link", D.SURF), ("FAQ + video schema", "so Google can read it", D.SURF)])
dia_gantt = D.gantt([
    ("## Weeks 1–2 · plumbing", 0, 0, "", ""), ("One address per page (redirects, canonicals)", 1, 2, C.NAVY, ""), ("Unique title tags on every page (both sites)", 1, 2, C.NAVY, ""), ("Injury site: 17 redirects for removed pages", 1, 2, C.NAVY, ""), ("Business Profile: URL, categories, photos", 1, 2, C.NAVY, ""), ("Request re-indexing of home + money pages", 2, 2, C.NAVY, ""),
    ("## Weeks 3–6 · money pages", 0, 0, "", ""), ("DUI · drug · CDV · guardianship · asset protection", 3, 6, C.BLUE, ""), ("Injury: Goose Creek + 4 city pages + Spanish", 3, 6, C.ORANGE, ""), ("Retitle & expand existing practice pages", 3, 5, C.BLUE, ""), ("Yelp: claim, categories, photos, specialties", 3, 4, C.AQUA, ""),
    ("## Weeks 5–12 · answer pages & channels", 0, 0, "", ""), ("2 answer pages / week (main site)", 5, 12, C.BLUE, ""), ("1 answer page / week (injury site)", 5, 12, C.ORANGE, ""), ("YouTube launch: 1 video / week", 5, 12, C.AQUA, ""), ("LinkedIn + Instagram cadence", 5, 12, C.AQUA, ""), ("Weekly Business Profile post + review asks", 3, 12, C.AQUA, ""), ("Monthly Search Console scorecard", 4, 12, C.GRAY, ""),
], label_w=330)

# ----------------------------------------------------------------------------
# page
# ----------------------------------------------------------------------------
CSS = open(FONTS).read() + r"""
:root{--paper:#eef1ee;--sheet:#ffffff;--ink:#101c2b;--ink2:#4a5566;--muted:#7c8694;--hair:#dfe4e2;--navy:#1f4e8c;--blue:#2a78d6;--orange:#eb6834;--aqua:#1baf7a;--azalea:#b8386f;--azalea-bg:#fbeef3;--tint:#eef4fb;--serif:'Newsreader',Georgia,'Times New Roman',serif;--sans:'Public Sans',system-ui,-apple-system,'Segoe UI',sans-serif}
html{color-scheme:light}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.55;padding-inline:16px;padding-block:24px}
.sheet{max-width:980px;margin:0 auto;background:var(--sheet);border:1px solid var(--hair);border-radius:14px;padding:clamp(20px,4vw,56px)}
h1,h2,h3{font-family:var(--serif);font-weight:600;line-height:1.15;text-wrap:balance;margin:0}
h1{font-size:clamp(34px,5vw,52px);font-weight:700}
h2{font-size:clamp(26px,3.4vw,34px);margin-top:6px}
h3{font-size:22px;margin-top:36px;margin-bottom:8px}
h4{font-size:15.5px;font-weight:700;margin:22px 0 6px}
p{margin:10px 0;max-width:74ch}
ul,ol{max-width:76ch}
li{margin:4px 0}
.lead{font-size:17px;color:var(--ink2);max-width:70ch}
.eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:8px}
section.sec{margin-top:60px;padding-top:28px;border-top:1px solid var(--hair)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:18px 0}
.kpi{border:1px solid var(--hair);border-radius:10px;padding:14px 16px}
.kpi .l{font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.kpi .v{font-size:30px;font-weight:600;margin-top:4px;line-height:1.1}
.kpi .d{font-size:12.5px;color:var(--ink2);margin-top:4px}
figure{margin:22px 0;padding:16px 16px 12px;border:1px solid var(--hair);border-radius:10px;background:#fff}
figure .ft{font-weight:700;font-size:15px;margin-bottom:2px}
figure .fs{font-size:13px;color:var(--muted);margin-bottom:10px}
figcaption{font-size:13px;color:var(--ink2);margin-top:10px;max-width:84ch}
.plain{border-left:4px solid var(--azalea);background:var(--azalea-bg);padding:12px 16px;border-radius:0 10px 10px 0;margin:18px 0;max-width:84ch}
.plain .t{font-weight:700;color:var(--azalea);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.plain p{margin:6px 0 0;max-width:none}
.callout{border:1px solid var(--hair);border-left:4px solid var(--navy);padding:12px 16px;border-radius:0 10px 10px 0;margin:16px 0;background:#fafbfa;max-width:84ch}
table{border-collapse:collapse;width:100%;font-size:13.5px;margin:12px 0}
th,td{padding:7px 10px;border-bottom:1px solid var(--hair);text-align:left;vertical-align:top}
th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tblwrap{overflow-x:auto}
.todo{list-style:none;padding:0;margin:12px 0;max-width:84ch}
.todo li{padding:8px 0 8px 30px;position:relative;border-bottom:1px dashed var(--hair)}
.todo li::before{content:"";position:absolute;left:2px;top:12px;width:13px;height:13px;border:2px solid var(--navy);border-radius:4px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin:14px 0}
.card{border:1px solid var(--hair);border-radius:10px;padding:16px}
.card h4{margin-top:0}
.pro{border-top:4px solid var(--aqua)} .con{border-top:4px solid var(--orange)}
.pill{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;letter-spacing:.04em;white-space:nowrap}
.pill.crit{background:#fbe9e9;color:#8f2323} .pill.warn{background:#fff3d6;color:#7a5200} .pill.good{background:#e6f6e6;color:#0a5a0a} .pill.info{background:var(--tint);color:var(--navy)}
.finding{display:grid;grid-template-columns:48px 1fr;gap:12px;padding:14px 0;border-bottom:1px solid var(--hair);max-width:90ch}
.finding .num{font-family:var(--serif);font-size:32px;color:var(--navy);line-height:1;font-weight:600}
.finding p{margin:4px 0 0}
.toc ol{columns:2;column-gap:32px;padding-left:20px;max-width:none} .toc li{margin:4px 0;break-inside:avoid}
a{color:var(--navy)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;background:#f3f5f3;padding:1px 5px;border-radius:4px}
.cover{padding:30px 0 10px}
.cover .meta{display:flex;flex-wrap:wrap;gap:28px;margin-top:28px;font-size:13px;color:var(--ink2)}
.cover .meta b{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}
.small{font-size:13px;color:var(--muted)}
.channel{display:grid;grid-template-columns:150px 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--hair)}
.channel h4{margin:0;font-family:var(--serif);font-size:20px;font-weight:600}
.channel .why{color:var(--ink2);font-size:13.5px}
.tag{font-size:12px;color:var(--muted)}
.two{columns:2;column-gap:32px;max-width:none}
@media (max-width:640px){.channel{grid-template-columns:1fr}.toc ol,.two{columns:1}}
@media print{body{background:#fff;padding:0} .sheet{border:0;border-radius:0;padding:0;max-width:none} section.sec{break-before:page;border-top:0;margin-top:0;padding-top:0} figure,table,.kpis,.plain,.card,.finding,.callout,.channel{break-inside:avoid} h2,h3,h4{break-after:avoid} .toc{break-before:page} a{text-decoration:none;color:inherit} .noprint{display:none} .cover{min-height:70vh}}
@page{size:Letter;margin:14mm 12mm}
"""

parts = []
add = parts.append

add(f"""<title>Frost Law Group Search Audit</title>
<meta name="description" content="Search Console audit, market analysis and topical-authority plan for frostlawgroupsc.com and summervilleaccidentattorney.com">
<style>{CSS}</style>
<div class="sheet">
<header class="cover">
<div class="eyebrow">Search audit &amp; topical-authority plan · September 2026</div>
<h1>Frost Law Group Search Audit</h1>
<p class="lead" style="margin-top:14px">Two websites, one plan. What Google Search Console says about <strong>frostlawgroupsc.com</strong> and <strong>summervilleaccidentattorney.com</strong>, what the Summerville market looks like, what it all means in plain English, and exactly what to build next — on the sites, on YouTube, on LinkedIn, on Instagram, on your Google Business Profile and on Yelp.</p>
<div class="meta">
<div><b>Prepared for</b>Tara &amp; Jack Frost · Frost Law Group, LLC · Summerville, SC</div>
<div><b>Your own data</b>Google Search Console, both properties</div>
<div><b>Market data</b>Search volumes, ad prices, competitor visibility, map-pack rankings</div>
<div><b>Main site window</b>{F_FIRST.strftime('%b %-d')} – {F_LAST.strftime('%b %-d, %Y')} ({F_DAYS} days)</div>
<div><b>Injury site window</b>{S_FIRST.strftime('%b %-d')} – {S_LAST.strftime('%b %-d, %Y')} ({S_DAYS} days)</div>
<div><b>Report date</b>September 11, 2026</div>
</div>
<p class="small" style="margin-top:22px">Clicks, impressions and positions are the firm's own Search Console figures (exact; the last two or three days are provisional). Monthly search volumes, cost-per-click, competitor traffic and link counts are industry estimates, rounded. Map-pack rankings were checked from central Summerville on September 11, 2026. Where we describe the live pages or the Business Profile, we say so.</p>
</header>

<nav class="toc"><div class="eyebrow">Contents</div><ol>
<li><a href="#summary">The 60-second version</a></li>
<li><a href="#how">How Google works, explained simply</a></li>
<li><a href="#site1">Site 1: frostlawgroupsc.com</a></li>
<li><a href="#site2">Site 2: summervilleaccidentattorney.com</a></li>
<li><a href="#mappack">The map pack: you vs. the top three</a></li>
<li><a href="#market">Who owns the Summerville search results</a></li>
<li><a href="#twosites">Two websites: the honest pros and cons</a></li>
<li><a href="#authority">The topical-authority plan</a></li>
<li><a href="#keywords">Keywords: high intent, long tail, and where to win first</a></li>
<li><a href="#fanout">Using Google's fan-out queries to our advantage</a></li>
<li><a href="#channels">YouTube, LinkedIn, Instagram, Business Profile, Yelp</a></li>
<li><a href="#plan">The 90-day plan and the year after</a></li>
<li><a href="#measure">How we'll know it's working</a></li>
<li><a href="#appendix">Appendix: data tables, redirects, title tags, glossary</a></li>
</ol></nav>
""")

# ---------------------------------------------------------------- summary
add(sec("summary", "1 · Read this first", "The 60-second version",
        "Both websites are being <em>shown</em> by Google far more than they are being <em>clicked</em>. The main site is found by people who already know your name; the injury site is on page 5–6 for everything; the Business Profile is outside the map pack for every money search. The good news: Google already treats the firm as relevant for estate, probate, criminal and DUI searches in Summerville, the market is winnable (small local firms hold page one today), and the searches are valuable — the pages just aren't built to win the click yet."))
add("<h3>frostlawgroupsc.com</h3>")
add(kpis([("Clicks", fmt(F["clicks"]), f"{F_DAYS} days"), ("Impressions", fmt(F["impressions"]), "times a page was shown"), ("Click-through rate", pct(F["ctr"]), "clicks ÷ impressions"), ("Average position", pos(F["position"]), "1 = top of page 1"), ("Non-brand clicks", fmt(NB["clicks"]), f"from {fmt(NB['impressions'])} non-brand impressions")]))
add("<h3>summervilleaccidentattorney.com</h3>")
add(kpis([("Clicks", fmt(S["clicks"]), f"{S_DAYS} days"), ("Impressions", fmt(S["impressions"]), "times a page was shown"), ("Click-through rate", pct(S["ctr"], 2), "clicks ÷ impressions"), ("Average position", pos(S["position"]), "page 6 of results"), ("Queries on page 1", fmt(sh["1-3"]["queries"] + sh["4-10"]["queries"]), f"of {fmt(sum(v['queries'] for v in sh.values()))} queries seen")]))
add("<h3>The market</h3>")
add(kpis([("Map-pack position", "#13–19", "for the six money searches; DUI: not in top 20"), ("Your reviews", fmt(MAP["frost"]["reviews"]), f"map-pack firms: median {fmt(PACK_MEDIAN_REVIEWS)}"), ("Est. monthly organic visits", fmt(BENCH_BY['frostlawgroupsc.com']['est_traffic']), f"vs. {fmt(BENCH_BY['pmclawfirm.com']['est_traffic'])} for PMC Law Firm"), ("Cost of one injury click in ads", money(cpc("personal injury lawyer summerville sc")), "“personal injury lawyer summerville sc”"), ("Searches for a Summerville lawyer", fmt(vol("attorney summerville sc") + vol("lawyer summerville sc")), "per month, two head terms")]))

findings = [
    ("Almost every click on the main site comes from people who already know your name.",
     f"Of the {fmt(B['clicks'] + NB['clicks'])} clicks Google attributes to identifiable searches, {fmt(B['clicks'])} contained “frost”. Only {fmt(NB['clicks'])} clicks came from the {fmt(len(nb_rows))} non-brand searches — even though those searches produced {fmt(NB['impressions'])} impressions. Google is showing you; people aren't choosing you yet."),
    ("Google already shows the firm for money searches — through the Business Profile link, not the website.",
     f"The address stored in your Business Profile (<code>http://www.frostlawgroupsc.com/</code>) collected {fmt(home_www['impressions'])} impressions at an average position of {pos(home_www['position'])}, for searches like “summerville dui lawyer”, “estate planning attorney” and “landlord tenant attorney in summerville sc”. Your actual practice pages sit at positions 16–35 for the same topics."),
    ("You are outside the map pack for every money search, and the gap is reviews and photos.",
     f"Checked from central Summerville: estate planning #{MAP['queries']['estate planning attorney summerville sc']['frost_rank']}, probate #{MAP['queries']['probate attorney summerville sc']['frost_rank']}, criminal defense #{MAP['queries']['criminal defense attorney summerville sc']['frost_rank']}, car accident #{MAP['queries']['car accident lawyer summerville sc']['frost_rank']}, dog bite #{MAP['queries']['dog bite lawyer summerville sc']['frost_rank']}, DUI not in the top 20. The firms in the packs have {fmt(min(t['reviews'] for t in firm_rows))}–{fmt(max(t['reviews'] for t in firm_rows))} reviews and up to {fmt(max(t['photos'] for t in firm_rows))} photos; you have {MAP['frost']['reviews']} and {MAP['frost']['photos']}."),
    ("The two sites compete with each other for injury searches.",
     f"{len(agg['cross_site_overlap'])} injury searches showed <em>both</em> domains. The injury site averages position {pos(S['position'])} and has {fmt(S['clicks'])} click in {S_DAYS} days; the main site's injury page averages position {agg['frost_topic_buckets']['Personal injury / accidents']['avg_position']}. Neither wins because each is holding the other back — on a search advertisers pay {money(cpc('personal injury lawyer summerville sc'))} a click for."),
    ("The injury site's rebuild dropped the pages that were getting seen.",
     f"{len(dead_rows)} old URLs (Goose Creek, Mount Pleasant, the attorneys page, the blog, truck and wrongful-death pages) now say “This page could not be found”, yet they still collected {fmt(DEAD_I)} impressions — {pct(DEAD_I / SVA_PAGE_I, 0)} of everything the site was shown for. They need redirects and, for the city pages, rebuilding."),
    ("Basic plumbing is splitting your signals.",
     f"Every inner page of the main site shares one title tag; every page of the injury site shares another. {len(MULTI)} main-site pages exist at two or three addresses (with and without <code>www</code>, with and without a trailing slash) and Google is counting them separately. Google's index still shows the main home page as “Remodeling – Coming Soon” from the redesign."),
    ("Google's AI is already using the main site to answer estate and probate questions.",
     f"{FAN_N} question-style searches — “who handles executor disputes in summerville, sc probate court?”, “which attorneys in summerville, sc handle contested guardianship cases?” — showed the site {fmt(FAN_I)} times at average positions between 4 and 13. These are the sub-questions Google's AI asks itself (its “fan-out”). No page on the site is written to answer any of them yet."),
]
add("<h3>Seven findings that explain the numbers</h3>")
for i, (t, d) in enumerate(findings, 1):
    add(f'<div class="finding"><div class="num">{i}</div><div><strong>{t}</strong><p>{d}</p></div></div>')
add("<h3>If we only do five things this month</h3>")
add(todo([
    "<strong>Fix the plumbing.</strong> One address per page, redirects for the other versions, a unique title on every page, and the Business Profile pointed at <code>https://frostlawgroupsc.com/</code>. (Weeks 1–2.)",
    "<strong>Build the missing money pages.</strong> Main site: DUI, drug charges, CDV/domestic violence, guardianship &amp; conservatorship, asset protection. Injury site: Goose Creek and four more city pages, plus a Spanish car-accident page. (Weeks 3–6.)",
    f"<strong>Start the review engine and fix the Business Profile.</strong> Categories, photos (you have {MAP['frost']['photos']}; the pack has dozens), services, a weekly post, and a review ask at every closed matter — the map pack is decided by reviews, categories and distance, and it already produces more impressions than any page you own.",
    f"<strong>Publish the first answer pages.</strong> Start with the {min(FAN_N, 8)} fan-out questions Google is already asking you. Short, direct, local, with a video.",
    "<strong>Start the flywheel.</strong> One video a week from Jack or Tara becomes a YouTube video, three clips, a LinkedIn post, an Instagram reel and a Business Profile post. Same work, seven places.",
]))
add(plain("Google is a librarian. Right now she pulls your book off the shelf a lot, but the cover is blank (same title on every page), the book is filed under two call numbers (two addresses), and it isn't the book people asked for (they asked about DUI; you handed them “Criminal Defense”). Down the street, the firms with the most library cards (reviews) get shelved at eye level on the map. We're going to give every page its own cover, one call number, write the exact books people are asking for — and collect library cards every week."))
add("</section>")

# ---------------------------------------------------------------- how it works
add(sec("how", "2 · The basics", "How Google works, explained simply", "Everything in this report uses five words. Here is what they mean, with the picture that goes with them."))
add(fig(dia_search, "What happens when someone searches", "The five steps between a search and a phone call",
        "An <strong>impression</strong> is Google showing your page. A <strong>click</strong> is the person choosing it. <strong>Position</strong> is where on the page you were (1–10 is page one). <strong>CTR</strong> is clicks divided by impressions. A <strong>query</strong> is the exact words the person typed."))
add(fig(dia_zones, "The three places you can appear on a results page", "Each zone is won differently",
        "The <strong>AI answer</strong> is assembled from many pages and rewards pages that answer one small question cleanly. The <strong>map pack</strong> is your Business Profile: reviews, photos, categories, distance. The <strong>blue links</strong> are your website pages: titles, content, authority."))
add("<h3>What “topical authority” means</h3>")
add("<p>Imagine two law firms. Firm A has one page called “Estate Planning”. Firm B has that page, plus a page for wills, one for trusts, one for powers of attorney, one explaining what happens if you die without a will in South Carolina, one about blended families, one about what it costs, one about reviewing an old plan — all linked to each other, all written for Summerville and Dorchester County. The librarian trusts Firm B as the expert. She sends Firm B the hard questions <em>and</em> the easy ones. That trust is topical authority, and it is earned one connected page at a time.</p>")
add(plain("Firm A wrote a pamphlet. Firm B wrote the whole shelf. Google hands the shelf to people first. Our plan is to write the shelf — for estate planning, probate and criminal defense on the main site, and for injuries on the injury site."))
add("<h3>What Google's AI “fan-out” means (and why it's in your data)</h3>")
add("<p>When someone asks Google's AI a big question — “who should handle my dad's estate in Summerville?” — the AI doesn't search that sentence. It quietly splits it into five or ten smaller questions, searches each one, and stitches the answers together. Those smaller questions are called fan-out queries. They show up in Search Console as oddly precise, complete sentences. You already have " + f"{FAN_N} of them. Section 10 shows how to use them.</p>")
add(fig(dia_fan, "Fan-out: one big question becomes five small ones", "Google's AI picks one clean page per small question",
        "Two of the five small questions already have a home. Three don't — those are pages to write. When every small question has a page, you get quoted in the big answer."))
add("<h3>Why the Business Profile and Yelp matter</h3>")
add(f"<p>Your <strong>Google Business Profile</strong> is the sign on the map. It decides whether you are in the three-business map pack, and it already produces more impressions than any page on your website (Section 3). <strong>Yelp</strong> is a second sign that other assistants read: ChatGPT, Bing and Apple Maps lean on Yelp's listings and reviews when someone asks them for “a good probate attorney near Summerville”. Yelp's own Summerville estate-planning list also ranks #{NOTES['yelp_positions']['estate planning attorney summerville sc']} on Google for “estate planning attorney summerville sc” — being on it is a second seat on page one.</p>")
add("</section>")

# ---------------------------------------------------------------- site 1
add(sec("site1", "3 · Site 1", "frostlawgroupsc.com: seen a lot, clicked by people who already know you",
        f"Search Console has data for this property from {F_FIRST.strftime('%B %-d, %Y')} — the redesign. In {F_DAYS} days Google showed the site {fmt(F['impressions'])} times and people clicked {fmt(F['clicks'])} times."))
add("<h3>3.1 The trend</h3>")
add(fig(chart_f_impr, "Daily impressions, all searches vs. non-brand searches", f"{F_FIRST.strftime('%b %-d')} – {F_LAST.strftime('%b %-d, %Y')}",
        "The spikes are not website wins. They are days when your Business Profile link was shown at position 1 for local searches (landlord-tenant, business law, DUI) — hundreds of impressions, almost no clicks. Steady non-brand impressions run 30–80 a day."))
add(fig(chart_f_clicks, "Daily clicks", "Never more than nine in a day; most days one to three", "Clicks are flat because nearly all of them are people searching your name. The non-brand line above is what has to grow."))
add("<h3>3.2 Brand vs. non-brand</h3>")
add(fig(chart_brand_clicks, "Clicks by type of search", f"{fmt(F['clicks'])} clicks in {F_DAYS} days"))
add(fig(chart_brand_impr, "Impressions by type of search", f"{fmt(F['impressions'])} impressions in {F_DAYS} days",
        f"Search Console hides very rare searches for privacy (the gray segment). Among the searches it does show, brand searches produced {fmt(B['clicks'])} clicks from {fmt(B['impressions'])} impressions (a {pct(B['ctr'], 0)} click-through rate); non-brand searches produced {fmt(NB['clicks'])} clicks from {fmt(NB['impressions'])} impressions ({pct(NB['ctr'])})."))
add(plain(f"Out of every 100 times Google showed you for a search that did <em>not</em> include the word “frost”, people clicked about {round(NB['ctr'] * 1000) / 10:g} times. The people who did click mostly typed “frost law group” — they were coming to see you anyway. The whole opportunity is in the orange segment."))
add("<h3>3.3 Where the impressions actually land</h3>")
add(fig(chart_home, "Two “home pages” in the data", "Impressions, with clicks and average position at right",
        f"<code>http://www.frostlawgroupsc.com/</code> is the exact address saved in your Google Business Profile. Google credits that address whenever the profile appears with its website link. That is why it shows a great average position ({pos(home_www['position'])}) with a {pct(home_www['clicks'] / home_www['impressions'])} click-through rate: people click Call or Directions, not the website button. The real home page averages position {pos(home_https['position'])}."))
add(callout("Google already knows the firm is relevant for DUI, estate planning, business law, divorce and landlord-tenant searches in Summerville — it shows the Business Profile for them at position 1. The website doesn't get those clicks because the pages behind the profile aren't the pages people want (there is no DUI page, no landlord-tenant page, no divorce page).", "Why this matters:"))
add("<h4>Pages, grouped by address</h4>")
add(table([("Page", lambda g: f"<code>{esc(g['path'])}</code>" + (f' <span class="pill warn">{len(g["variants"])} addresses</span>' if len(g["variants"]) > 1 else ""), ""), ("Clicks", lambda g: fmt(g["clicks"]), "n"), ("Impressions", lambda g: fmt(g["impressions"]), "n"), ("Avg. position", lambda g: pos(g["position"]), "n"), ("Addresses Google is counting separately", lambda g: "<br>".join(f"<code>{esc(v)}</code>" for v in g["variants"]), "")], page_groups))
add(f"<p class=\"small\">{len(MULTI)} of {len(page_groups)} pages exist at more than one address. Google has picked the no-trailing-slash <code>https://frostlawgroupsc.com/…</code> versions as the official ones (we checked with the URL Inspection tool), but the site itself still links to the slash versions, so both keep collecting impressions.</p>")
add("<h4>Devices</h4>")
add(fig(chart_dev_f, "Clicks by device", f"{fmt(F['clicks'])} clicks"))
add(fig(chart_dev_fi, "Impressions by device", f"{fmt(F['impressions'])} impressions",
        f"Desktop impressions are inflated by the Business Profile link (desktop shows the profile panel far more). On mobile — where real local searches happen — the site's click-through rate is {pct(devices['frost']['MOBILE']['clicks'] / devices['frost']['MOBILE']['impressions'])} at an average position of {devices['frost']['MOBILE']['position']}. That is the number we'll move."))
add("<h3>3.4 What people search for (and how far away you are)</h3>")
add(fig(chart_topics, "Non-brand impressions by topic", "Highlighted: the four subjects the main site should own",
        "Landlord-tenant and eviction searches are the biggest single bucket, and there is no page for them — those impressions are the Business Profile being shown at position 1, and the home page at position 50–60. Estate planning is the biggest bucket the site actually competes in, and it already averages page 2. DUI averages position 8 — but almost entirely through the profile link, because the criminal-defense page sits at ~30 for DUI searches."))
add(table([("Topic", "k", ""), ("Queries", lambda r: fmt(r["v"]["queries"]), "n"), ("Impressions", lambda r: fmt(r["v"]["impressions"]), "n"), ("Clicks", lambda r: fmt(r["v"]["clicks"]), "n"), ("Avg. position", lambda r: r["v"]["avg_position"], "n"),
           ("Page that exists today", lambda r: {"Estate planning / wills / trusts": "/estate-planning-attorney + will, trust, POA, living-will pages", "Probate / executor": "/probate", "DUI": "none (folded into /criminal-defense)", "Criminal defense": "/criminal-defense", "Landlord / tenant / eviction": "none", "Divorce / family": "none (not a practice area)", "Real estate / business": "none", "Personal injury / accidents": "/motor-vehicle-personal-injury (competes with the injury site)", "Generic \"attorney near me\"": "home page"}.get(r["k"], "—"), "")],
          [dict(k=k, v=v) for k, v in sorted(topics.items(), key=lambda kv: -kv[1]["impressions"]) if v["impressions"] > 0]))
add(callout(f"Keyword tools measure exact phrases, so hyper-local phrases look small: “estate planning attorney summerville sc” ≈ {volfmt('estate planning attorney summerville sc')} searches a month, “criminal defense attorney summerville sc” ≈ {volfmt('criminal defense attorney summerville sc')}, “probate attorney summerville sc” ≈ {volfmt('probate attorney summerville sc')}, “dui lawyer summerville sc” ≈ {volfmt('dui lawyer summerville sc')}. Your Search Console shows the real picture: {fmt(topics['Estate planning / wills / trusts']['impressions'])} impressions for estate-planning searches alone in {F_DAYS} days, spread across {fmt(topics['Estate planning / wills / trusts']['queries'])} different phrasings. The big pools are the state-level questions — “south carolina dui laws” ≈ {volfmt('south carolina dui laws')}/month, “first offense dui south carolina” ≈ {volfmt('first offense dui south carolina')}, “how much does estate planning cost” ≈ {volfmt('how much does estate planning cost')}, “south carolina power of attorney requirements” ≈ {volfmt('south carolina power of attorney requirements')}, “living will south carolina” ≈ {volfmt('living will south carolina')}, “expungement south carolina” ≈ {volfmt('expungement south carolina')} — and those are exactly the answer pages in the plan.", "Market check:"))
add("<h3>3.5 Where you rank, in buckets</h3>")
add(fig(chart_f_hist_q, "Non-brand queries by position bucket", f"{fmt(sum(v['queries'] for v in fh.values()))} queries"))
add(fig(chart_f_hist_i, "Non-brand impressions by position bucket", f"{fmt(sum(v['impressions'] for v in fh.values()))} impressions",
        f"The {fmt(fh['1-3']['queries'])} queries in positions 1–3 produced {fmt(fh['1-3']['clicks'])} click — they are the Business Profile link, not pages. The realistic “about to break through” group is positions 4–20: {fmt(fh['4-10']['queries'] + fh['11-20']['queries'])} queries and {fmt(fh['4-10']['impressions'] + fh['11-20']['impressions'])} impressions, almost all of them estate, probate and criminal."))
add(plain("Position 4–20 means you're on page one near the bottom or on page two. Those are the books already on the cart — a better cover (title), a better first page (opening paragraph), and a few more chapters (FAQs) is usually what moves them to eye level."))
add("<h3>3.6 Quick wins: searches already close to page one on your own pages</h3>")
add("<p>These are non-brand searches where one of the site's real pages (not the profile link) sits between positions 4 and 20 with at least five impressions. Each row is a small, specific piece of work.</p>")
add(table([("Search", lambda r: esc(r["query"]), ""), ("Impr.", lambda r: fmt(r["impressions"]), "n"), ("Pos.", lambda r: pos(r["position"]), "n"), ("Page today", lambda r: f"<code>{esc(re.sub(r'^https://frostlawgroupsc.com', '', r['page']))}</code>", ""), ("What to do", lambda r: action_for(r["query"]), "")], quick_frost[:24]))
add("<h3>3.7 The questions Google's AI is already asking you</h3>")
add(fig(chart_fan, "Question-style searches (fan-out) that showed the main site", f"{FAN_N} questions · {fmt(FAN_I)} impressions · positions mostly 4–13",
        "Notice the shape: complete, specific, local sentences. Nobody types these. Google's AI generates them when a person asks a bigger question, and it is pulling your estate-planning, probate and trust pages into the answer. Every one of these deserves its own short page (Section 10)."))
add("<h3>3.8 Technical findings on the main site</h3>")
tech1 = [
    ("crit", "Google's index still shows the home page title as “Remodeling – Coming Soon – Summerville Estate Planning &amp; Criminal Defense Attorneys”.", "The live page title is fine (“Frost Law Group, LLC | Summerville, SC Estate Planning &amp; Injury Attorneys”); Google hasn't refreshed it since the redesign. Fix: request indexing for the home page in Search Console after the plumbing fixes below, and keep the home page linked from every page."),
    ("crit", "Every inner page shares one title tag: “Frost Law Group, LLC — Summerville, SC Law Firm”.", "The title is the book cover and the single strongest on-page signal. Probate, criminal defense, wills, trusts and powers of attorney all wear the same one. Appendix C lists a proposed title for every page."),
    ("crit", f"{len(MULTI)} pages live at two or three addresses.", "Google chose the no-slash <code>https://frostlawgroupsc.com/page</code> versions. The site's own navigation links to the slash versions and the Business Profile links to <code>http://www</code>. Fix: 301-redirect <code>http://</code>, <code>www.</code> and trailing-slash versions to the official address; update every internal link; set the Business Profile website to <code>https://frostlawgroupsc.com/</code>. Also remove or redirect leftovers Google found: <code>/probate-2/</code>, <code>/about-us/?swcfpc=1</code>, <code>/author/adminfrost-lawgroup-com/</code>."),
    ("warn", "The personal-injury page competes with the injury site.", f"<code>/motor-vehicle-personal-injury</code> (two addresses, {fmt(sum(r['impressions'] for r in frost_pages if 'motor-vehicle' in r['url']))} impressions, average position 14–32) targets the same searches as summervilleaccidentattorney.com. Section 7 gives the rule; the short version is: one site per subject."),
    ("warn", "“In The Know” has no articles.", "The blog page shows four cards, but each “Read more” goes to a practice page or to the injury site. There is no informational content on the site at all — which is exactly what topical authority and fan-out answers require."),
    ("warn", "Practice pages are short.", "Criminal defense is ~480 words with no sub-pages for DUI, drug charges or CDV even though the Business Profile lists all three as services and Search Console shows demand for each. Estate planning is ~580 words. Probate (~970) and powers of attorney (~1,000) are the best-built pages — and, not by coincidence, the ones Google's AI already quotes."),
    ("info", "No YouTube or LinkedIn links on the site; Facebook, X and Instagram only.", "Add the LinkedIn company page and the YouTube channel (once created) to the header/footer and to the firm's structured data (<code>sameAs</code>), so Google connects the profiles to the firm."),
    ("info", "No FAQ, attorney or LegalService structured data detected by Search Console on the inspected pages.", "Adding LegalService (with address, phone, hours, sameAs), Attorney bios and FAQPage markup gives Google and the AI systems a clean, machine-readable version of who you are and what you answer."),
]
for k, t, d in tech1:
    add(f'<div class="finding"><div>{pill(k, {"crit": "Fix first", "warn": "Fix soon", "info": "Improve"}[k])}</div><div><strong>{t}</strong><p>{d}</p></div></div>')
add("</section>")

# ---------------------------------------------------------------- site 2
add(sec("site2", "4 · Site 2", "summervilleaccidentattorney.com: on page six for everything",
        f"Search Console has data from {S_FIRST.strftime('%B %-d, %Y')}. In {S_DAYS} days the site was shown {fmt(S['impressions'])} times, at an average position of {pos(S['position'])}, and was clicked {fmt(S['clicks'])} time."))
add("<h3>4.1 The trend</h3>")
add(fig(chart_s_impr, "Daily impressions", f"{S_FIRST.strftime('%b %-d')} – {S_LAST.strftime('%b %-d, %Y')}", "Impressions fell through August as the removed old-site pages started dropping out of Google's index, then recovered slightly in September as the new practice-area pages were picked up."))
add(fig(chart_s_pos, "Daily average position", "Lower is better; page one is 1–10", "The site has never averaged better than position 30 on any day. Page-six positions are effectively invisible: fewer than one searcher in a hundred looks there."))
add("<h3>4.2 Where you rank, in buckets</h3>")
add(fig(chart_s_hist_q, "Queries by position bucket", f"{fmt(sum(v['queries'] for v in sh.values()))} queries"))
add(fig(chart_s_hist_i, "Impressions by position bucket", f"{fmt(sum(v['impressions'] for v in sh.values()))} impressions",
        f"{fmt(sh['51+']['queries'])} of {fmt(sum(v['queries'] for v in sh.values()))} queries — and {pct(sh['51+']['impressions'] / sum(v['impressions'] for v in sh.values()), 0)} of impressions — are at position 51 or worse. Nothing is on page one. The closest group is dog bites."))
add(plain("Google knows this site exists and files it under the right subject. It just doesn't trust it yet: the site is new, has almost no reputation, and lost its most-seen pages in the rebuild. Trust is built with the plan in Sections 8–12; the redirects in 4.4 stop the bleeding first."))
add("<h3>4.3 What people search for</h3>")
add(fig(chart_s_pr, "Impressions by case type", "Highlighted: the two case types closest to page one",
        f"Car accidents are the volume (avg. position {sva_pr['Car / auto accident']['avg_position']}); dog bites and motorcycle accidents are the openings (avg. positions {sva_pr['Dog bite']['avg_position']} and {sva_pr['Motorcycle accident']['avg_position']}). Rideshare, drunk-driving-victim and delivery-driver searches are real demand with no dedicated pages."))
add(callout(f"“personal injury lawyer summerville sc” is searched about {volfmt('personal injury lawyer summerville sc')} times a month and advertisers pay about {money(cpc('personal injury lawyer summerville sc'))} for a single click on it — the most valuable search in this report. Today the injury site is not in the top 50 for it; three Summerville firms (Shelbourne, Gil Gatch, PMC) hold positions 3, 4 and 15 with ordinary pages. The city variants — North Charleston ({volfmt('personal injury lawyer north charleston sc')}/month, {money(cpc('personal injury lawyer north charleston sc'))} a click) and Charleston ({volfmt('car accident lawyer charleston sc')}/month, {money(cpc('car accident lawyer charleston sc'))}) — are the second and third targets.", "The prize:"))
add(fig(chart_s_city, "Impressions by the city named in the search", "Highlighted: cities whose pages were removed in the rebuild",
        f"Goose Creek alone produced {fmt(sva_city['Goose Creek']['impressions'])} impressions — and its page now returns “not found”. The “wrong town” row ({fmt(WRONG_I)} impressions: Sevierville TN, Schererville IN, Somerville MA…) means Google isn't yet sure where <em>this</em> Summerville is: the site needs the firm's address, map and structured data on every page."))
add(f"<p>Spanish-language searches (“abogado de accidentes carro summerville”) produced {fmt(SPAN_I)} impressions with no Spanish page — a cheap page to add and a market the big Charleston firms mostly ignore in Summerville and Goose Creek.</p>")
add("<h3>4.4 Removed pages that are still being shown</h3>")
add(fig(chart_dead, "Impressions landing on pages that now say “This page could not be found”", f"{len(dead_rows)} old-site URLs · {fmt(DEAD_I)} impressions",
        "These pages were indexed before the rebuild (Search Console still shows them as “Submitted and indexed”, last crawled July 20–23) and are still shown to searchers — who land on a not-found page. Each one needs a permanent redirect to the closest new page, and the city pages deserve rebuilding."))
add(table([("Old address", lambda r: f"<code>{esc(r['path'])}</code>", ""), ("Impressions", lambda r: fmt(r["impressions"]), "n"), ("Avg. pos.", lambda r: pos(r["position"]), "n"), ("Redirect to", lambda r: esc(r["to"]), "")], dead_rows))
add("<h3>4.5 Duplicate addresses and identical titles</h3>")
add("<p>Search Console reports the non-www home page as “Duplicate, Google chose different canonical than user”: the site answers at both <code>www.</code> and non-<code>www</code> addresses, each claiming to be the original. Google chose <code>https://www.summervilleaccidentattorney.com/</code>. The non-www copies of the practice pages also collect impressions (motorcycle accidents at position 20.5, dog bites at 25). Fix: pick <code>www</code>, 301-redirect everything else to it, and make every internal link and canonical tag agree.</p>")
add("<p>Every page on the site carries the same title: “Summerville Accident Attorney | Personal Injury Lawyers | Frost Law Group”. The headings are good (“Summerville Dog Bite Lawyers”), but the title is the cover Google reads first. Appendix C has a proposed title per page.</p>")
add("<h3>4.6 Quick wins: closest to page one</h3>")
add(table([("Search", lambda r: esc(r[0]), ""), ("Impr.", lambda r: fmt(r[1]["impressions"]), "n"), ("Avg. pos.", lambda r: pos(r[1]["position"]), "n"),
           ("What to do", lambda r: ("Expand the dog-bite page: SC strict-liability statute, children, homeowner's insurance, scarring; add a dog-bite video and FAQ schema." if "dog bite" in r[0] else
                                     "Retitle the motorcycle page; add helmet-law, lane-splitting and bias FAQs; redirect the old /motorcycle-accident/ address to it." if "motorcycle" in r[0] else
                                     "Retitle the truck page; redirect /truck-accident-3/ to it; add I-26 corridor and trucking-regulation FAQs." if "truck" in r[0] else
                                     "Rebuild the city page with local roads, courts and directions." if re.search(r"walterboro|moncks|goose|pleasant|charleston|knightsville|ladson", r[0]) else
                                     "Add a premises-liability section to the slip-and-fall page." if "premises" in r[0] else "Answer page + FAQ on the closest practice page."), "")], quick_sva[:16]))
add("<h3>4.7 Technical findings on the injury site</h3>")
tech2 = [
    ("crit", f"{len(dead_rows)} removed pages need permanent redirects (table above).", "Until they are redirected, Google keeps showing not-found pages and the reputation those addresses had earned is lost."),
    ("crit", "www and non-www both live; Google and the site disagree on the original.", "One address per page. Redirect non-www to www and fix the canonical tags."),
    ("crit", "One title tag across the whole site.", "See Appendix C for the proposed titles."),
    ("warn", "No city pages, no blog, no Spanish page on the new site.", "The old site had city pages that earned most of the impressions; the new one has an “Areas We Serve” heading with nothing under it. Rebuild Goose Creek first."),
    ("warn", "Weak “where are we” signals.", f"{pct(WRONG_I / SVA_Q_I, 0)} of impressions come from searches about other towns called Summerville/Sevierville/Schererville. Put the full address, an embedded map, county names and LegalService structured data on every page; link the Business Profile and the main site prominently."),
    ("warn", f"Almost no reputation: {fmt(BENCH_BY['summervilleaccidentattorney.com']['referring_domains'])} sites link to it, and most of those links are low-quality directories.", "Section 6 shows the gap to the local firms. Links come from the plan in Section 12: local organizations, directories the firm already qualifies for, and the main site itself."),
    ("info", "Stock hero images are hot-linked from Unsplash.", "Replace with real photos of Jack, Tara, the office and Summerville — the same photos that go on the Business Profile. Real photos also feed the E-E-A-T signals Google uses for legal content."),
    ("good", "Review snippets and breadcrumbs are already detected as rich results.", "Keep them; add Attorney, LegalService and FAQPage markup alongside."),
]
for k, t, d in tech2:
    add(f'<div class="finding"><div>{pill(k, {"crit": "Fix first", "warn": "Fix soon", "info": "Improve", "good": "Keep"}[k])}</div><div><strong>{t}</strong><p>{d}</p></div></div>')
add("</section>")

# ---------------------------------------------------------------- map pack
add(sec("mappack", "5 · The map", "The map pack: you vs. the top three",
        "For every money search, the three businesses in the map pack get the calls. We checked the map results from central Summerville for six searches. You are in none of the packs — and the reason is measurable."))
add(fig(chart_map, "Where Frost Law Group sits in the map results", "Six money searches, checked from central Summerville · 1–3 is the pack",
        "Green would mean “in the pack”. For DUI the profile isn't in the top 20 at all, even though Search Console shows the profile link at position 1 for DUI searches on some days — those are searches made very close to the office. From the rest of Summerville, other firms win."))
add("<h4>Who is in each pack</h4>")
add(table([("Search", lambda r: esc(r[0]), ""), ("Frost", lambda r: (f"#{r[1]['frost_rank']}" if r[1]["frost_rank"] else "not in top 20"), "n"),
           ("The three in the pack (reviews · photos)", lambda r: " · ".join(f"<strong>{esc(t['name'])}</strong> ({fmt(t['reviews'])} · {t['photos']})" for t in r[1]["top"][:3]), "")],
          list(MAP["queries"].items())))
add(fig(chart_reviews, "Google reviews: you vs. the firms in the packs", "Review count, with photo count and rating at right",
        f"Every firm in a pack has more reviews than you; the median is {fmt(PACK_MEDIAN_REVIEWS)}. Susan E. Williams — #1 for DUI and criminal defense — has {fmt(firms['Susan E. Williams']['reviews'])} reviews and {fmt(firms['Susan E. Williams']['photos'])} photos as a solo practitioner. Reviews are the one lever here that a two-attorney firm controls completely."))
add(fig(chart_photos, "Business Profile photos: you vs. the firms in the packs", "Photos uploaded to the profile",
        "Photos are a weak ranking signal but a strong choosing signal: the profile with real faces, the office and the dogs gets the tap. Four photos reads as “not sure this firm is active”."))
add("<h3>What decides the map pack, in plain terms</h3>")
add("<ol>"
    "<li><strong>Relevance</strong> — your categories and services. Every firm in the DUI and criminal packs has “Criminal justice attorney” as its <em>primary</em> category; yours is the generic “Attorney”. The estate packs are led by firms whose primary category is “Estate planning attorney”.</li>"
    "<li><strong>Distance</strong> — how close the searcher is. Your office on Linwood Lane sits south of the downtown cluster where most competitors are; you can't move, so you win on the other two.</li>"
    f"<li><strong>Prominence</strong> — reviews, photos, posts, mentions and links. This is where the gap is: {MAP['frost']['reviews']} reviews vs. {fmt(PACK_MEDIAN_REVIEWS)}+ for the pack; {MAP['frost']['photos']} photos vs. dozens.</li>"
    "</ol>")
add(plain("The map is a popularity contest with a distance rule. You're a little far from downtown, so you have to be clearly more popular to make the top three: more happy clients writing reviews, more photos, more updates. Ask every single client, and you'll pass most of these firms within a year."))
add("<h4>The category fix</h4>")
add("<p>Primary category should be <strong>Estate planning attorney</strong> (your largest demand and the practice the packs reward most), with <strong>Criminal justice attorney</strong>, <strong>Personal injury attorney</strong>, <strong>Probate attorney</strong>, <strong>Elder law attorney</strong>, <strong>Trial attorney</strong> and <strong>Law firm</strong> as additional categories. If the injury practice becomes the priority, the primary can be switched later; Google re-evaluates within days.</p>")
add("</section>")

# ---------------------------------------------------------------- market
add(sec("market", "6 · The competition", "Who owns the Summerville search results",
        "Before deciding how hard this is, look at who is winning. It is not the billboard firms. For the Summerville searches that matter to you, page one is held by a solo DUI lawyer, three small local firms, and the lawyer directories."))
add(table([("Site", lambda r: (f"<strong>{esc(r['domain'])}</strong>" if r["domain"] not in DIRS else esc(r["domain"]) + " " + pill("info", "directory")), ""),
           ("Visibility", lambda r: f"{r['visibility']:.1f}", "n"), ("Avg. position", lambda r: f"{r['avg_position']:.1f}", "n"), ("Money searches ranked", lambda r: fmt(r["keywords"]), "n"), ("Est. visits / month from them", lambda r: fmt(r["est_traffic"]), "n")],
          VIS[:16]))
add("<p class=\"small\">Visibility is a share-of-page-one score across the money searches in this report (estate, probate, criminal, DUI, injury, plus “lawyer/attorney summerville sc”). Neither Frost site appears on page one for any of them today.</p>")
add(fig(chart_traffic, "Estimated monthly organic visits", "Frost sites vs. three Summerville firms with the same practice mix",
        f"PMC Law Firm (estate, probate, criminal) ranks for {fmt(BENCH_BY['pmclawfirm.com']['keywords'])} keywords and draws an estimated {fmt(BENCH_BY['pmclawfirm.com']['est_traffic'])} visits a month; Shelbourne Law (injury + estate + criminal) {fmt(BENCH_BY['shelbournelaw.com']['est_traffic'])}; Gil Gatch Law (all four of your practice areas) {fmt(BENCH_BY['gilgatchlaw.com']['est_traffic'])}. The main site draws about {fmt(BENCH_BY['frostlawgroupsc.com']['est_traffic'])} — nearly all of it from the firm's name — and the injury site effectively none."))
add(fig(chart_links, "Referring domains (other websites that link in)", "Quantity, with a link-quality score and the share that is spam",
        f"Gil Gatch grew from 34 to 92 referring domains in twelve months (local press releases, directories, sponsorships). Your main site's links are older and heavier on low-quality directories; the injury site's {fmt(BENCH_BY['summervilleaccidentattorney.com']['referring_domains'])} are mostly spam-grade. Links are the slowest lever, which is why the plan starts with pages and reviews and adds links from month four."))
add("<h3>Three things the winners have in common</h3>")
add("<ul>"
    f"<li><strong>A page for every service, with the city in the title.</strong> Shelbourne ranks #1 for “attorneys in summerville sc” ({volfmt('attorney summerville sc')} searches a month) with a plain home page that says Summerville in the title, headline and address block; its estate page (“Summerville Estate Planning Lawyer”) is #2 for that search. PMC ranks #3 for “poa lawyers near me” ({fmt(next((g['volume'] for g in GAP if g['keyword'] == 'poa lawyers near me'), 6600))} searches a month nationally, served locally) with a dedicated power-of-attorney page under its probate hub — you have a POA page too; theirs is deeper and better linked.</li>"
    "<li><strong>Reviews in volume.</strong> Every firm in a map pack has more reviews than you; the DUI winner has 161 with 217 photos.</li>"
    "<li><strong>Presence on the directories that hold page one.</strong> Justia, Super Lawyers, Cornell LII and Yelp each rank on page one for several money searches. A complete profile on each is a second and third seat on page one — and the sources AI assistants read.</li>"
    "</ul>")
add(plain("The firms beating you are your size. They didn't buy their way in; they wrote a page for each thing they do, put “Summerville” on it, collected reviews for years, and made sure they were listed everywhere people look. Same recipe, and you have a head start on the AI answers."))
add("</section>")

# ---------------------------------------------------------------- two sites
add(sec("twosites", "7 · The decision", "Two websites: the honest pros and cons", "You asked for a straight answer on whether to keep both sites. Here is the evidence, the trade-offs in plain language, and the rules that make two sites work if that's the choice."))
add(fig(chart_overlap, "The same injury searches show both sites", "Average position per site for the searches both domains appeared for",
        "Both dots are far from page one for every shared search. Two weak pages on two domains don't add up to one strong page; Google picks one to show and the other dilutes it. Whatever we decide, only one domain should target injury searches."))
add('<div class="grid2">')
add('<div class="card pro"><h4>Why two sites can work</h4><ul>'
    '<li><strong>Two clear subjects.</strong> Google rewards focus. A site that is only about injuries, and a site that is only about estate, probate and criminal, are each easier to make “the shelf” than one site that is about everything.</li>'
    '<li><strong>The domain says what it is.</strong> “summervilleaccidentattorney.com” matches what injury clients type, and it lets the injury practice look and sound different (urgent, free consultation, 24/7) from the calm, family estate-planning brand.</li>'
    '<li><strong>Two chances on the page.</strong> When both are strong, a brand search and some local searches can show both domains — two of ten results instead of one.</li>'
    '<li><strong>Different audiences, different partners.</strong> Estate planning is referred by financial advisors and CPAs; injury work by chiropractors, body shops and past clients. Separate sites make each referral story clean.</li>'
    '<li><strong>The main site keeps its head start.</strong> Google\'s AI is already quoting the main site for estate and probate questions; keeping injuries off it protects that focus.</li>'
    '</ul></div>')
add('<div class="card con"><h4>What it costs you</h4><ul>'
    f'<li><strong>Reputation splits.</strong> Every link, mention and review builds one domain. The injury site starts from almost nothing ({fmt(BENCH_BY["summervilleaccidentattorney.com"]["referring_domains"])} mostly low-quality linking sites, no estimated organic visits) and currently averages position {pos(S["position"])}.</li>'
    '<li><strong>One Business Profile, one Yelp.</strong> A business gets one profile and it links to one website. The injury site is not connected to the map listing that already produces most of your impressions.</li>'
    '<li><strong>Double the work.</strong> Two sets of pages, titles, redirects, content, videos and monthly checks. The plan below assumes you have the capacity (or a partner) for both.</li>'
    '<li><strong>Same firm, same address, same phone on two sites.</strong> Google needs to be told clearly that these are one firm with two practice sites, or it may treat one as a copy.</li>'
    '<li><strong>Cannibalization is already happening</strong> (chart above) and has to be engineered away.</li>'
    '<li><strong>Brand confusion.</strong> Someone who searched “Frost Law Group” after a crash should land on the injury site, not the estate site — that routing has to be designed.</li>'
    '</ul></div></div>')
add("<h3>Our recommendation</h3>")
add(f"<p><strong>Keep both — but only under the seven rules below, and with a checkpoint.</strong> The data supports the split: the main site's strength is estate, probate and criminal (that is where Google already trusts it), and the injury market in Summerville is worth the effort — “personal injury lawyer summerville sc” alone is ~{volfmt('personal injury lawyer summerville sc')} searches a month at {money(cpc('personal injury lawyer summerville sc'))} a click, and the firms holding it today (Shelbourne, Gil Gatch) are your size. A focused, family-run injury site can position against the billboard firms better than a general practice page can. The risks are all manageable if the sites are wired correctly from day one.</p>")
add("<p><strong>The checkpoint:</strong> at the end of month six, the injury site should have at least a handful of searches on page one (dog bite, motorcycle, Goose Creek) and its first non-brand clicks every week. If it doesn't, we fold it into the main site as <code>/personal-injury/</code> with permanent redirects — nothing built is wasted, because every page moves with it.</p>")
add(fig(dia_two, "How the two sites are wired", "One subject per site, cross-linked, one Business Profile pointing at the main site"))
add("<h3>The seven rules for running two sites</h3>")
add(todo([
    "<strong>One subject per site.</strong> The main site's <code>/motor-vehicle-personal-injury</code> page is redirected (301) to the injury site's car-accident page; the “Personal Injury” menu item links across. No injury pages on the main site; no estate, probate or criminal pages on the injury site. Where subjects touch — a DUI <em>charge</em> is criminal (main site), a crash caused by a drunk driver is injury (injury site) — the boundary is written down.",
    "<strong>Say it's one firm.</strong> Identical name, address and phone on both; LegalService structured data on both that lists the other site and the Business Profile in <code>sameAs</code>; attorney bios on both that link to each other.",
    "<strong>Cross-link in the header and footer</strong> with descriptive words (“Our injury practice: Summerville Accident Attorney”), not just a logo.",
    "<strong>The Business Profile links to the main site</strong> (https, no www). The injury site gets its own signals: Avvo, Justia, FindLaw and Super Lawyers profiles for Jack updated to list it; the LinkedIn company page and YouTube channel link both; the Instagram bio uses a link page with both.",
    "<strong>Separate content calendars, no crossover.</strong> Two answer pages a week on the main site, one on the injury site. The injury site also gets the Spanish page and the city pages.",
    "<strong>Route the brand.</strong> The main site's home page gets a visible “Injured in an accident?” panel linking to the injury site; the injury site's header says “A Frost Law Group practice” linking back.",
    "<strong>Measure them separately, monthly</strong> (two Search Console properties, already in place) and hold the month-six checkpoint.",
]))
add(plain("Two stores, one owner. Each store sells one thing and says so on the sign. Both stores have the same name on the door and point customers to the other store when they walk into the wrong one. And we agree now: if the second store isn't earning its keep in six months, we merge it into the first — without throwing away anything on its shelves."))
add("</section>")

# ---------------------------------------------------------------- authority plan
add(sec("authority", "8 · The plan", "The topical-authority plan: write the shelf", "Four hubs on the main site, two on the injury site. Each hub is an existing practice page rebuilt as the center of a cluster; each spoke is a page that answers one question people ask. Blue outlines are pages to build."))
add("<h3>8.1 Main site clusters</h3>")
add(fig(dia_estate, "Estate Planning cluster", "Hub: the existing estate-planning page · 12 spokes, 8 new", "The existing will, trust, POA and living-will pages become spokes with proper titles. New spokes come straight from Search Console: asset protection (six different searches), blended families, trust amendments and restatements, guardianship, costs, and “what happens without a will”."))
add(fig(dia_probate, "Probate cluster", "Hub: the existing probate page · 12 spokes, 9 new", "Probate is where Google's AI already quotes you. The county court guides (Dorchester, Berkeley, Charleston) are the kind of useful, local page nobody else in Summerville has written — and they attract links from local organizations."))
add(fig(dia_crim, "Criminal Defense cluster", "Hub: the existing criminal-defense page · 12 spokes, all new", f"DUI is the biggest gap: 24 DUI searches, 410 impressions, no DUI page — and the state-level questions (“south carolina dui laws” ≈ {volfmt('south carolina dui laws')}/month, “first offense dui south carolina” ≈ {volfmt('first offense dui south carolina')}) are large and easy. Jack's fourteen years in law enforcement is the story every page in this cluster should tell — “a former deputy, now on your side” is a real, defensible difference."))
add("<h3>8.2 Injury site clusters</h3>")
add(fig(dia_pi, "Car Accident cluster", "Hub: the existing car-accident page · 12 spokes, all new", "Search Console already shows demand for hit-and-run, drunk-driving-victim, uninsured-motorist, distracted-driving, rideshare and delivery-driver searches — almost all of them with “Goose Creek” or “Summerville” attached."))
add(fig(dia_pi2, "The other injury hubs and the city pages", "Existing practice pages plus six city pages and a Spanish page", "City pages are only worth building if they are genuinely local: the roads and intersections, the hospital people get taken to, the police department that writes the report, the courthouse, directions from that town to the office."))
add("<h3>8.3 How every page is built</h3>")
add('<div class="grid2">')
add('<div class="card"><h4>Hub page (a practice area)</h4><ul><li>Title: “[Practice] Attorney in Summerville, SC | Frost Law Group”</li><li>Opens with a 40–60 word answer to “what do you do and for whom”</li><li>Sections for each service, each linking to its spoke page</li><li>“How it works here” — Dorchester/Berkeley/Charleston specifics</li><li>Attorney box: who handles it, credentials, photo</li><li>Reviews about this practice area</li><li>6–8 FAQs (taken from the fan-out questions) with FAQ markup</li><li>Embedded video (2–5 minutes) and its transcript</li></ul></div>')
add('<div class="card"><h4>Answer page (a spoke)</h4><ul><li>Title is the question, in the words people use</li><li>First paragraph answers it directly — the sentence Google can quote</li><li>Then the detail: steps, timelines, costs, statute names, local court</li><li>Three to five follow-up questions (the next fan-out) answered briefly</li><li>Links up to the hub and sideways to two related spokes</li><li>Author and “reviewed on” date; Attorney markup</li><li>60–90 second vertical video from Jack or Tara, embedded</li><li>800–1,500 words; no filler</li></ul></div>')
add("</div>")
add("<h4>Site-wide rules</h4>")
add(todo(["Every page links to its hub; every hub links to every spoke; no page is more than two clicks from the home page.", "One page per question. If two pages could rank for the same search, merge them.", "Structured data on every page: LegalService (organization), Attorney (bios), FAQPage (answer blocks), VideoObject (embedded videos), BreadcrumbList.", "Real photos, real names, real courts. Google's quality guidelines for legal content weight who wrote it and whether they are who they say they are.", "Publish, then request indexing in Search Console; check impressions on the new page at 14 and 45 days."]))
add("</section>")

# ---------------------------------------------------------------- keywords
add(sec("keywords", "9 · Keywords", "High intent, long tail, and where to win first",
        "“High intent” means the person is ready to hire (“dui lawyer summerville sc”). “Long tail” means specific, longer questions with fewer searches each but far less competition — and they add up. We rank both by how close you already are (your Search Console positions), then check each against monthly search volume and what advertisers pay per click — the market's own estimate of what a lead is worth."))
add(fig(chart_value, "What the head terms are worth", "Monthly searches, with the average price advertisers pay for one click",
        f"A single click on “personal injury lawyer summerville sc” costs advertisers about {money(cpc('personal injury lawyer summerville sc'))}; “attorney summerville sc” about {money(cpc('attorney summerville sc'))}; “elder law attorney summerville sc” about {money(cpc('elder law attorney summerville sc'))}. Ranking organically for these is the same traffic without the invoice. Hyper-local injury and city phrases (dog bite, Goose Creek, motorcycle) show no measurable volume in keyword tools — but Search Console proves the demand exists, which is why they are cheap to win."))
add("<h3>9.1 Main site: high-intent targets</h3>")
hi_main = [
    ("Summerville DUI lawyer", "summerville dui lawyer · dui lawyer summerville sc · dui attorney summerville (sc) · summerville dui attorney · drinking and driving attorney summerville sc", "new /dui-lawyer-summerville-sc", "Profile shown at #1; criminal page at ~30", "dui lawyer summerville sc", "1"),
    ("Criminal defense attorney Summerville SC", "criminal defense attorney summerville sc · summerville criminal defense attorney/lawyer · criminal defense lawyer summerville sc · criminal attorney summerville sc", "/criminal-defense (retitle + expand)", "25–35", "criminal defense attorney summerville sc", "1"),
    ("Estate planning attorney Summerville SC", "estate planning attorney summerville sc · summerville estate planning attorney · estate lawyer summerville sc · summerville estate attorney · estate planning attorney in ladson sc", "/estate-planning-attorney (retitle + expand)", "8–17", "estate planning attorney summerville sc", "1"),
    ("Probate lawyer Summerville SC", "probate lawyer summerville sc · probate attorney summerville · summerville probate · summerville probate litigation lawyer · avoiding probate summerville", "/probate (retitle + executor section)", "5–17", "probate attorney summerville sc", "1"),
    ("Wills lawyer Summerville SC", "wills lawyer summerville sc · summerville wills · wills and estate planning lawyer summerville sc · summerville wills and trusts", "/last-will-and-testament (retitle)", "4–11", "estate attorney summerville sc", "1"),
    ("Living trust attorney Summerville", "living trust lawyers summerville · summerville revocable living trusts · trusts summerville · creating a trust summerville · summerville trust attorneys", "/revocable-trust (retitle)", "8–12", "revocable living trust south carolina", "2"),
    ("Guardianship & conservatorship lawyer Summerville", "summerville conservatorship lawyer · which attorneys in summerville, sc handle contested guardianship cases? · guardianship of minors", "new /guardianship-conservatorship", "5–12 (no page!)", "guardianship in south carolina", "1"),
    ("Asset protection attorney Summerville", "asset protection attorneys/lawyers summerville · asset protection planning summerville · who helps create asset protection trusts in summerville, sc?", "new /asset-protection", "9–17", None, "2"),
    ("Drug charge lawyer Summerville SC", "drug defense attorney summerville sc · drug lawyer summerville sc · drug defense lawyer summerville sc", "new /drug-charges", "5–29", "simple possession south carolina", "2"),
    ("CDV / domestic violence attorney Summerville", "cdv attorney summerville sc · domestic violence lawyer", "new /domestic-violence-cdv", "24", "cdv south carolina", "2"),
    ("Power of attorney lawyer Summerville", "summerville durable power of attorneys · durable power of attorneys summerville · power of attorney lawyer south carolina", "/power-of-attorney (retitle)", "6–18", "south carolina power of attorney requirements", "2"),
    ("Elder law / Medicaid planning Summerville", "summerville medicaid attorneys · elder law attorney summerville sc", "new /elder-law-medicaid-planning", "5 (1 query)", "elder law attorney summerville sc", "3"),
    ("Living will attorney Summerville", "living will sc · sc living will form · living will south carolina", "/living-will (retitle + SC form explainer)", "40–56", "living will south carolina", "3"),
]
add(table([("Target", lambda r: f"<strong>{r[0]}</strong>", ""), ("Searches already seen in Search Console", lambda r: r[1], ""), ("Page", lambda r: f"<code>{r[2]}</code>", ""), ("Position today", lambda r: r[3], "n"),
           ("Market check", lambda r: (f"“{r[4]}”: {volfmt(r[4])}/mo · {money(cpc(r[4]))}/click" if r[4] else "no measurable volume; real demand in Search Console"), ""), ("Priority", lambda r: pill("info", "P" + r[5]), "")], hi_main))
add("<h3>9.2 Main site: long-tail and question targets</h3>")
add("<p>The first group is verbatim from Search Console (with impressions and position). The second group is the logical next layer of the same clusters — questions Google's AI will fan out to once the hubs exist, with monthly search volume where the market can measure it.</p>")
add(table([("Question already showing the site", lambda r: esc(r[0]), ""), ("Impr.", lambda r: fmt(r[1]["impressions"]), "n"), ("Pos.", lambda r: pos(r[1]["position"]), "n"), ("Page to write", lambda r: action_for(r[0]).replace("New answer page: ", "").replace("New page: ", ""), "")], fan[:18]))
add("<h4>Next-layer questions (build after the hubs)</h4>")
NEXT = [("How long does probate take in South Carolina?", "how long does probate take in south carolina"), ("How much does probate cost in SC, and who pays?", None), ("Does a will have to be probated in South Carolina?", None),
        ("What happens if you die without a will in South Carolina?", "south carolina intestate succession"), ("How much does an estate plan cost?", "how much does estate planning cost"), ("Will vs. revocable trust in South Carolina — which do we need?", "revocable living trust south carolina"),
        ("South Carolina power of attorney requirements (witnesses, notary, recording)", "south carolina power of attorney requirements"), ("Where do I get the South Carolina durable power of attorney form?", "south carolina durable power of attorney form"), ("How do I remove an executor in South Carolina?", None),
        ("Can I contest a will in Dorchester County?", None), ("Small-estate affidavit in South Carolina: who qualifies?", "small estate affidavit south carolina"), ("How to avoid probate in South Carolina", "how to avoid probate in south carolina"),
        ("Living wills in South Carolina: what they cover", "living will south carolina"), ("Guardianship of an adult in South Carolina", "guardianship in south carolina"), ("Conservatorship in South Carolina", "conservatorship south carolina"),
        ("First-offense DUI penalties in South Carolina", "first offense dui south carolina"), ("South Carolina DUI laws, explained", "south carolina dui laws"), ("What is DUAC and how is it different from DUI?", "duac south carolina"),
        ("Do I have to take the breathalyzer in SC (implied consent)?", "implied consent south carolina"), ("How does a bond hearing work in Dorchester County?", "bond hearing south carolina"), ("Can a CDV charge be expunged in South Carolina?", "cdv south carolina"),
        ("How to get a criminal record expunged in SC", "expungement south carolina"), ("Simple possession in South Carolina: penalties and options", "simple possession south carolina"), ("What happens after an arrest in Summerville (first 72 hours)?", None)]
add('<ul class="two">' + "".join(f"<li>{q}" + (f" <span class='tag'>({volfmt(k)}/mo)</span>" if k and vol(k) else "") + "</li>" for q, k in NEXT) + "</ul>")
add("<h3>9.3 Injury site: high-intent targets</h3>")
hi_pi = [
    ("Summerville personal injury lawyer", "summerville personal injury lawyer/attorney(s) · personal injury law firm summerville · summerville sc personal injury lawyer", "/ (home) + /practice-areas (retitle, rebuild)", "50–71", "personal injury lawyer summerville sc", "1"),
    ("Summerville dog bite lawyer", "dog bite lawyer summerville sc · summerville dog bite lawyer/attorney(s) · dog bite law firm summerville · dog bite lawyer knightsville", "/practice-areas/dog-bites (expand)", "20–27", "south carolina dog bite law", "1"),
    ("Summerville motorcycle accident lawyer", "motorcycle accident lawyer summerville (sc) · summerville motorcycle accident attorney/lawyer · summerville motorcycle crash lawyer", "/practice-areas/motorcycle-accidents (+ redirect)", "17–36", "south carolina motorcycle helmet law", "1"),
    ("Summerville truck accident lawyer", "summerville truck accident lawyer/attorney(s) · truck accident lawyer summerville · summerville fatal truck accident lawyer", "/practice-areas/truck-accidents (+ redirect)", "30–66", "truck accident lawyer charleston sc", "1"),
    ("Goose Creek car accident lawyer", "goose creek car accident lawyer/attorney · goose creek hit and run/drunk driving/distracted driving/uninsured motorist accident attorney (40 searches)", "new /areas/goose-creek", "49–75 (page removed)", None, "1"),
    ("Summerville car accident lawyer", "summerville car accident lawyer/attorney(s) · car accident lawyer summerville sc · summerville auto accident attorney/lawyer · summerville car accident law firm", "/practice-areas/car-accidents (retitle + rebuild)", "44–89", "car accident attorney summerville sc", "1"),
    ("North Charleston / Charleston injury", "car accident lawyer north charleston (sc) · north charleston car accident attorney · north charleston auto accident attorney", "new /areas/north-charleston + /areas/charleston", "40–66 (pages removed)", "personal injury lawyer north charleston sc", "2"),
    ("Abogado de accidentes en Summerville", "abogado(s) de accidentes carro summerville · abogado de accidentes coche summerville · abogado de accidentes carro goose creek", "new /es/abogado-de-accidentes", f"29–71 ({fmt(SPAN_I)} impr.)", None, "2"),
    ("Summerville Uber / Lyft accident lawyer", "summerville uber accident attorney/lawyer(s) · summerville lyft accident attorney/lawyer(s) · goose creek uber accident attorney", "new /practice-areas/rideshare-accidents", "48–82", None, "2"),
    ("Drunk-driving crash victims", "summerville drunk driving accident attorney/lawyer(s) · summerville dui accident attorney · goose creek drunk driving accident attorney", "new /practice-areas/drunk-driving-accidents", "59–84", None, "2"),
    ("Mount Pleasant / Moncks Corner / Walterboro", "mount pleasant car accident lawyer(s) · mt pleasant car accident attorney · moncks corner car accident attorneys · walterboro car accident lawyer", "new /areas/… pages", "13–66 (pages removed)", None, "2"),
    ("Summerville wrongful death lawyer", "summerville wrongful death attorney/lawyer · summerville fatal car accident attorney/lawyer(s) · wrongful death law firm summerville", "/practice-areas/wrongful-death (+ redirect)", "49–80", "south carolina wrongful death statute", "3"),
    ("Delivery-driver & work injuries", "summerville delivery driver injury attorney/lawyer(s) · summerville mechanic injury lawyer · summerville work injury lawyer", "new spoke under car accidents + workers' comp", "67–90", None, "3"),
]
add(table([("Target", lambda r: f"<strong>{r[0]}</strong>", ""), ("Searches already seen in Search Console", lambda r: r[1], ""), ("Page", lambda r: f"<code>{r[2]}</code>", ""), ("Position today", lambda r: r[3], "n"),
           ("Market check", lambda r: (f"“{r[4]}”: {volfmt(r[4])}/mo · {money(cpc(r[4]))}/click" if r[4] else "no measurable volume; real demand in Search Console"), ""), ("Priority", lambda r: pill("info", "P" + r[5]), "")], hi_pi))
add("<h4>Injury site: long-tail and question targets</h4>")
NEXT_PI = [("What to do after a car accident in South Carolina (the first 48 hours)", None), ("Is South Carolina an at-fault state?", "is south carolina an at fault state"), ("How does comparative negligence work in SC (the 51% rule)?", "south carolina comparative negligence"),
           ("How long do I have to file a car-accident claim in SC (statute of limitations)?", "personal injury statute of limitations south carolina"), ("South Carolina car accident laws, explained", "south carolina car accident laws"), ("Should I talk to the other driver's insurance company?", None),
           ("What is South Carolina's dog-bite law (strict liability)?", "south carolina dog bite law"), ("What if my child was bitten by a neighbor's dog?", None), ("Does homeowner's insurance pay for a dog bite in SC?", None),
           ("Who pays after an Uber or Lyft accident in South Carolina?", None), ("What if the driver who hit me was drunk — can I get punitive damages?", None), ("What if the driver who hit me has no insurance (UM/UIM in SC)?", "uninsured motorist coverage south carolina"),
           ("South Carolina motorcycle helmet law and your claim", "south carolina motorcycle helmet law"), ("South Carolina's wrongful death statute, explained", "south carolina wrongful death statute"), ("Where do crashes happen on I-26, Hwy 17A and Dorchester Road?", None),
           ("Getting your injuries evaluated after a crash in Summerville (the “auto injury assessment” search)", None), ("Accident on the Highway 17 bypass — who is responsible?", None)]
add('<ul class="two">' + "".join(f"<li>{q}" + (f" <span class='tag'>({volfmt(k)}/mo)</span>" if k and vol(k) else "") + "</li>" for q, k in NEXT_PI) + "</ul>")
add("<h3>9.4 The keyword gap: what the local winners rank for that you don't</h3>")
add(f"<p>We took every search that PMC Law Firm, Gil Gatch Law or Shelbourne Law ranks for, kept the ones in your four subjects, and removed the ones you already rank for. {len(gap_rows)} remain; the {len(GAP_TOP)} largest are below. “Near me” searches are national totals — Google serves them locally, which is how a Summerville firm ends up #3 for “poa lawyers near me”.</p>")
add(table([("Search", lambda g: esc(g["keyword"]), ""), ("Searches / mo", lambda g: fmt(g["volume"]), "n"), ("Ad price / click", lambda g: money(g["cpc"]), "n"), ("Who ranks (position)", lambda g: "; ".join(f"{PMC_NAME[w[0]]} #{w[1]}" for w in g["who"]), ""), ("Your page", lambda g: gap_page(g["keyword"]), "")], GAP_TOP))
add("<h3>9.5 The “win fast” order</h3>")
add("<p>Fast wins are searches where you already sit at positions 4–20 and the fix is a better page, not a new reputation. In order:</p>")
add("<ol>"
    "<li><strong>Main site, week 1–2:</strong> retitle every page (Appendix C) and fix the addresses. This alone touches every search in the 4–20 band.</li>"
    "<li><strong>Main site, week 3–4:</strong> the DUI page and the guardianship page — both have demand with no page, and the profile already ranks #1 for DUI close to the office.</li>"
    "<li><strong>Main site, week 3–6:</strong> executor-disputes, trust-amendment, asset-protection and blended-family answer pages — the fan-out questions already at positions 4–10 — then the large state-level questions (DUI laws, first-offense DUI, POA requirements, estate-planning cost).</li>"
    "<li><strong>Injury site, week 1–2:</strong> the 17 redirects and the www fix.</li>"
    "<li><strong>Injury site, week 3–6:</strong> expand dog bites (closest to page one), rebuild Goose Creek, retitle motorcycle and truck, add the Spanish page; then go after “personal injury lawyer summerville sc” with the rebuilt home page and hub.</li>"
    "</ol>")
add("</section>")

# ---------------------------------------------------------------- fan-out
add(sec("fanout", "10 · AI search", "Using Google's fan-out queries to our advantage", "Fan-out is the biggest change in how Google works in years, and your Search Console already shows it happening. Here is the playbook."))
add("<h3>10.1 Harvest the questions every month</h3>")
add("<p>In Search Console → Performance → Queries, filter with a regular expression for question words: <code>^(who|which|what|how|where|when|can|does|is it|should)</code>. Sort by impressions. Every row is a question Google's AI asked on someone's behalf and considered your site for. Copy them into the content calendar.</p>")
add("<h3>10.2 Answer each one on its own page, answer-first</h3>")
add("<p>The AI is looking for the cleanest 40–60 word answer to <em>that</em> question, from a page that is clearly about <em>that</em> question, on a site that is clearly an authority on the subject. So: the question is the title and the H1; the first paragraph is the answer; the rest of the page earns the trust (statutes, steps, local court, who you are). Add the three to five follow-up questions the AI will ask next as short H2 sections.</p>")
add("<h3>10.3 Be the same firm everywhere</h3>")
add("<p>AI answers are built from many sources at once: your pages, your Business Profile, Yelp, Avvo, Justia, the SC Bar directory, LinkedIn, YouTube. They check that the facts agree — name, address, phone, attorneys, practice areas. Keep every listing identical and complete, and link them all in your structured data. This is also why Yelp matters for ChatGPT-style answers.</p>")
add("<h3>10.4 Put the answer in more than one format</h3>")
add(f"<p>The same answer as a page, as a short video with a transcript, as an FAQ block with markup, and as a Business Profile post gives the AI four consistent places to find it. Google already shows YouTube results for these searches (positions {min(NOTES['youtube_positions'].values())}–{max(NOTES['youtube_positions'].values())} for “estate planning attorney summerville sc”, “dui lawyer summerville sc” and others) and no Summerville firm has made the videos — a Frost video titled with the exact question is often the only video answer for a Summerville-specific question.</p>")
add("<h3>10.5 Worked example: guardianship</h3>")
add(f"<p>Search Console shows “which attorneys in summerville, sc handle contested guardianship cases?” — {fmt(next((a['impressions'] for q, a in fan if 'guardianship cases' in q), 39))} impressions at an average position of {pos(next((a['position'] for q, a in fan if 'guardianship cases' in q), 5.4))} — with no guardianship page on the site; “guardianship in south carolina” is searched about {volfmt('guardianship in south carolina')} times a month statewide. The plan: a hub page “Guardianship &amp; Conservatorship Attorney in Summerville, SC”, three spokes (“What is a contested guardianship in SC?”, “How to become a legal guardian in Dorchester County”, “Conservatorship vs. power of attorney”), a four-minute video from Tara, FAQ markup, and a Business Profile post. Then we watch that question move from position 5 to position 1–2, and watch the AI answer start naming the firm.</p>")
add(plain("Google's AI is a student writing a report. It doesn't read one book; it asks ten small questions and grabs the clearest paragraph for each. We're going to write the clearest paragraph in Summerville for each of the questions it's already asking — and put your name on every one."))
add("</section>")

# ---------------------------------------------------------------- channels
add(sec("channels", "11 · Channels", "YouTube, LinkedIn, Instagram, the Business Profile and Yelp", "The websites are where authority lives; the channels are how it spreads and how Google learns the firm is real, active and trusted. One piece of work feeds all of them."))
add(fig(dia_cycle, "The content flywheel", "One answer page a week becomes seven assets"))
channels = [
    ("YouTube", f"Google owns it, indexes every transcript, and already shows YouTube results for your money searches (positions {min(NOTES['youtube_positions'].values())}–{max(NOTES['youtube_positions'].values())}) — with no Summerville firm supplying the videos. There is no Frost Law Group channel today.",
     ["Create the channel as the firm; link it from both sites, the Business Profile and LinkedIn.", "Series 1 — <em>Ask a Summerville Lawyer</em>: 60–90 second answers to the fan-out questions (vertical, Shorts).", "Series 2 — <em>Probate in Plain English</em> (Tara, 4–8 minutes): the probate process, executor duties, timelines, costs — one video per spoke page.", "Series 3 — <em>Know Your Rights in SC</em> (Jack, 3–6 minutes): DUI stops, bond hearings, what to say and not say — the former-deputy angle.", "Series 4 — <em>After the Crash</em> (injury site): what to do, insurance calls, dog bites, motorcycle bias.", "Title = the question. Description = the 60-word answer + link to the page. Chapters, captions and a pinned comment with the phone number.", "Embed every video on its page and mark it up as VideoObject."],
     "1 long video + 3 shorts per week, filmed in one 90-minute session every other week."),
    ("LinkedIn", "Where estate-planning referrals come from: financial advisors, CPAs, realtors, HR managers. Tara's and Jack's personal profiles reach more people than the company page.",
     ["Tara posts weekly on estate and probate for professionals: “What a financial advisor should check before a client funds a trust”, “Three probate mistakes we see in Dorchester County”.", "Jack posts weekly on criminal and injury topics for the community: bond hearings, what a police report means, the drunk-driving-victim path.", "Company page shares every new answer page and video; website field → main site; injury posts link to the injury site.", "Ask five referral partners a month to follow and comment; comment on theirs. Send a quarterly “what changed in SC estate law” post to the same list.", "Add both attorneys' LinkedIn URLs to the Attorney structured data on both sites."],
     "2 personal posts + 1 company post per week."),
    ("Instagram", "Your existing account (@frostlawgroupllc) is the human side: the husband-and-wife firm, the Golden Retrievers, Summerville. It builds brand recall and sends Google engagement and entity signals.",
     ["Reels: the same vertical clips as YouTube Shorts (the question as on-screen text in the first second).", "Carousels: “5 things to do after a dog bite in SC”, “What a will does and doesn't do”, “DUI stop: your 4 rights”.", "The Frost Pups as a recurring feature — office life, Flowertown Festival, local events; geo-tag Summerville on everything.", "Bio: a link page with both websites, the Business Profile review link and the phone number.", "Highlights: Estate · Probate · Criminal · Injury · The Pups."],
     "3 posts per week: one reel, one carousel, one photo."),
    ("Google Business Profile", f"It already produces more impressions than any page ({fmt(home_www['impressions'])} in {F_DAYS} days), and it is #13–19 in the map results for the money searches (Section 5). Right now it is a plain listing: the “Attorney” category plus “Estate planning attorney”, {MAP['frost']['photos']} photos, {MAP['frost']['reviews']} reviews, no posts.",
     ["Website: change to <code>https://frostlawgroupsc.com/</code> (it currently stores <code>http://www.</code>).", "Categories: primary <strong>Estate planning attorney</strong>; add Criminal justice attorney, Personal injury attorney, Probate attorney, Elder law attorney, Trial attorney, Law firm.", "Photos: 20+ real photos (exterior with the sign, reception, conference room, Jack, Tara, Cassie, the dogs) — then two new photos a month.", "Services: keep the list, add a two-sentence description with the local phrase for each (“Summerville DUI defense…”).", "Posts: one a week, reusing the answer page and video; every post has a call to action.", "Q&amp;A: seed eight questions (the fan-out questions) with the firm's answers.", f"Reviews: ask at every closed matter with a direct link; goal four to six new reviews a month, which passes the pack median of {fmt(PACK_MEDIAN_REVIEWS)} within a year; reply to every review, including the one-star.", "Verify ownership: the public listing shows an “Own this business?” prompt, which Google typically displays when a profile isn't verified — confirm in the Business Profile dashboard.", "Hours: consider a 24/7 intake line for injury calls (an answering service) so the injury practice can honestly show extended availability — every injury firm in the pack shows “Open 24 hours”."],
     "Weekly post, monthly photos, review ask at every matter."),
    ("Yelp", f"ChatGPT, Bing and Apple Maps use Yelp listings and reviews when someone asks them for a lawyer nearby, and Yelp's own Summerville list ranks #{NOTES['yelp_positions']['estate planning attorney summerville sc']} on Google for “estate planning attorney summerville sc” and #{NOTES['yelp_positions']['probate attorney summerville sc']} for probate. The listing exists (category: Criminal Defense Law) and is thin.",
     ["Claim/verify and complete: categories Estate Planning Law, Wills Trusts &amp; Probates, Criminal Defense Law, DUI Law, Personal Injury Law.", "“From the business” and specialties written as short answers to the fan-out questions.", "Ten real photos; hours; website → main site; phone.", "Respond to every review. Don't mass-solicit (Yelp filters that); do mention the Yelp page in the review email as a second option for clients who use Yelp.", "Update it quarterly so it stays “Updated [month]” in Google's results."],
     "Complete once (week 3–4), then quarterly."),
]
for name, why, items, cadence in channels:
    add(f'<div class="channel"><div><h4>{name}</h4><div class="tag">{cadence}</div></div><div><p class="why">{why}</p><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div></div>")
add("<h3>A 12-week starter calendar</h3>")
cal = [
    ("1", "Plumbing week: redirects, titles, Business Profile URL & categories", "—", "Announce the new site", "Office & pups intro", "Welcome post"),
    ("2", "Plumbing week 2; request indexing", "—", "Tara: “why every family needs an estate plan” (link)", "Carousel: what a will does", "Estate planning post"),
    ("3", "DUI page (main) · Goose Creek page (injury)", "Jack: DUI stop rights", "Jack: what a DUI stop looks like", "Reel: 4 rights in a DUI stop", "DUI post"),
    ("4", "Guardianship page · dog-bite expansion", "Tara: contested guardianship", "Tara: guardianship vs. POA", "Reel: dog-bite first steps", "Dog-bite post (injury)"),
    ("5", "Executor duties & disputes · Spanish injury page", "Tara: executor duties", "Tara: 3 executor mistakes", "Carousel: executor checklist", "Probate post"),
    ("6", "Asset protection · motorcycle retitle", "Tara: asset-protection trusts", "Tara: asset protection for business owners", "Reel: trust vs. will", "Trust post"),
    ("7", "Drug charges · rideshare accidents", "Jack: first-offense drug charge", "Jack: bond hearings in Dorchester County", "Reel: after an Uber crash", "Criminal post"),
    ("8", "Trust amendments · truck retitle", "Tara: amending a trust", "Tara: when to review an old plan", "Carousel: 5 reasons to update a plan", "Estate post"),
    ("9", "CDV/domestic violence · Mt Pleasant page", "Jack: CDV charges", "Jack: what CDV means in SC", "Reel: the first 72 hours after arrest", "Criminal post"),
    ("10", "Blended families · drunk-driving victims", "Tara: second-marriage planning", "Tara: blended-family plans", "Reel: the pups at Flowertown", "Injury post"),
    ("11", "Dorchester County Probate Court guide · Moncks Corner page", "Tara: probate court walkthrough", "Tara: how long probate takes", "Carousel: probate timeline", "Probate post"),
    ("12", "What happens without a will · North Charleston page", "Tara: dying without a will in SC", "Jack + Tara: 90-day recap", "Reel: recap", "Review-thank-you post"),
]
add(table([("Wk", lambda r: r[0], "n"), ("Pages", lambda r: r[1], ""), ("YouTube", lambda r: r[2], ""), ("LinkedIn", lambda r: r[3], ""), ("Instagram", lambda r: r[4], ""), ("Business Profile", lambda r: r[5], "")], cal))
add("</section>")

# ---------------------------------------------------------------- plan
add(sec("plan", "12 · Timeline", "The 90-day plan, and the year after", "Plumbing first, money pages second, then the weekly rhythm of answer pages and video. Nothing here depends on buying anything; it depends on Jack's and Tara's time in front of a camera and a partner who builds the pages."))
add(fig(dia_gantt, "The first 13 weeks", "Navy: technical · blue: main-site pages · orange: injury-site pages · green: channels"))
add("<h3>Months 4–6: authority</h3>")
add(todo(["County court guides (Dorchester, Berkeley, Charleston probate courts; Summerville Municipal Court) — the pages local organizations link to.",
          "Local links: Summerville Chamber (already lists the firm), Dorchester County Bar, WealthCounsel directory, sponsorships (youth sports, Flowertown Festival), local news quotes. Update Avvo, Justia, FindLaw and Super Lawyers profiles to list both sites — the directories that hold page one.",
          "Second layer of answer pages for each cluster (the “next-layer questions” in Section 9).",
          f"Review milestone: pass the map-pack median ({fmt(PACK_MEDIAN_REVIEWS)}) with practice-area keywords appearing naturally in the reviews.",
          "Month-six checkpoint on the injury site (Section 7)."]))
add("<h3>Months 7–12: expansion</h3>")
add(todo(["Injury site: catastrophic-injury and workers'-comp clusters; case-results page; more city pages only where searches appear; the Charleston and North Charleston pages aimed at the larger city searches.",
          "Main site: special-needs planning, Medicaid/elder-law planning, business-owner estate planning; expungement and traffic clusters.",
          "Long-form YouTube (10–15 minutes) on the top three questions of the year; a quarterly LinkedIn newsletter for referral partners.",
          "Annual refresh: every hub page reviewed, dated and re-requested for indexing."]))
add(plain("First we fix the plumbing so nothing leaks. Then we build the rooms people are asking for. Then, every week, we add one more book to the shelf, ask one more client for a review, and tell people about it in five places. Twelve months of that is how a two-person firm becomes the name Google says first."))
add("</section>")

# ---------------------------------------------------------------- measurement
add(sec("measure", "13 · Measurement", "How we'll know it's working", "Six numbers checked monthly, plus the only number that really matters: calls and consultations."))
add(table([("Signal", "s", ""), ("Today", "t", "n"), ("What good looks like", "g", ""), ("Where to see it", "w", "")], [
    dict(s="Non-brand clicks per month (main site)", t=f"≈{fmt(round(NB['clicks'] / F_DAYS * 30))}", g="Growing every month; the first goal is double digits every month, then dozens", w="Search Console → Performance → Queries, filter “does not contain frost”"),
    dict(s="Non-brand queries in positions 1–10 on real pages (main site)", t=f"{fmt(fh['4-10']['queries'])} in 4–10 (profile-inflated)", g="A growing count of estate/probate/criminal searches on page one from the pages themselves", w="Performance → Pages → pick a page → Queries"),
    dict(s="Question-style (fan-out) searches showing the site", t=f"{FAN_N} questions · {fmt(FAN_I)} impressions", g="More questions each month, average position moving toward 1–3", w="Queries filtered by the regular expression in Section 10"),
    dict(s="Map-pack position for the six money searches", t="#13–19; DUI not in top 20", g="In the pack (top 3) for two searches by month six, four by month twelve", w="Monthly map check from the same Summerville location"),
    dict(s="Google reviews", t=fmt(MAP["frost"]["reviews"]), g=f"+4–6 per month; past the pack median ({fmt(PACK_MEDIAN_REVIEWS)}) within a year", w="Business Profile dashboard"),
    dict(s="Injury site: queries on page one · non-brand clicks", t=f"0 · {fmt(S['clicks'])} click in {S_DAYS} days", g="Dog bite, motorcycle and Goose Creek on page one by month six; weekly clicks by month three", w="Injury property → Performance"),
    dict(s="Calls, forms and consultations by source", t="not tracked", g="Every lead tagged: Google (site), Google (profile), Yelp, LinkedIn, referral", w="Call tracking + form field “how did you hear about us”"),
]))
add("<p class=\"small\">These are targets, not guarantees. Technical fixes usually show in Search Console within two to six weeks; new pages within six to twelve weeks; authority builds over six to twelve months. We report the actual numbers monthly, against this baseline.</p>")
add("</section>")

# ---------------------------------------------------------------- appendix
add(sec("appendix", "14 · Appendix", "Data tables, redirects, title tags, glossary"))
add("<h3>A. Main site: top non-brand searches</h3>")
add(table([("Search", lambda r: esc(r["keys"][0]), ""), ("Clicks", lambda r: fmt(r["clicks"]), "n"), ("Impressions", lambda r: fmt(r["impressions"]), "n"), ("Avg. position", lambda r: pos(r["position"]), "n")], top_frost_nb))
add("<h3>A2. Main site: brand searches</h3>")
add(table([("Search", lambda r: esc(r["keys"][0]), ""), ("Clicks", lambda r: fmt(r["clicks"]), "n"), ("Impressions", lambda r: fmt(r["impressions"]), "n"), ("Avg. position", lambda r: pos(r["position"]), "n")], top_frost_brand))
add("<h3>B. Injury site: top searches</h3>")
add(table([("Search", lambda r: esc(r[0]), ""), ("Impressions", lambda r: fmt(r[1]["impressions"]), "n"), ("Avg. position", lambda r: pos(r[1]["position"]), "n"), ("Pages shown", lambda r: ", ".join(f"<code>{esc(re.sub(r'^https?://(www.)?summervilleaccidentattorney.com', '', p) or '/')}</code>" for p in list(r[1]["pages"])[:2]), "")], top_sva))
add("<h3>B2. Injury site: every page Search Console reported</h3>")
add(table([("Page", lambda r: f"<code>{esc(r['url'])}</code>", ""), ("Clicks", lambda r: fmt(r["clicks"]), "n"), ("Impressions", lambda r: fmt(r["impressions"]), "n"), ("Avg. position", lambda r: pos(r["position"]), "n"),
           ("Status", lambda r: (pill("crit", "removed · redirect") if re.sub(r"^https?://(www\.)?summervilleaccidentattorney\.com", "", r["url"]) in DEAD else (pill("warn", "non-www duplicate") if r["url"].startswith("https://summervilleaccidentattorney.com/") else pill("good", "live"))), "")], sorted(sva_pages, key=lambda r: -r["impressions"])))
add("<h3>C. Proposed title tags</h3>")
titles_main = [("/", "Summerville, SC Estate Planning, Probate & Criminal Defense Attorneys | Frost Law Group"), ("/estate-planning-attorney", "Estate Planning Attorney in Summerville, SC | Wills, Trusts & POAs | Frost Law Group"), ("/probate", "Probate Attorney in Summerville, SC | Dorchester & Berkeley County Estates | Frost Law Group"), ("/criminal-defense", "Criminal Defense Attorney in Summerville, SC | Former Deputy Jack Frost | Frost Law Group"), ("/dui-lawyer-summerville-sc (new)", "Summerville DUI Lawyer | First-Offense DUI & DUAC Defense | Frost Law Group"), ("/drug-charges (new)", "Drug Charge Defense Lawyer in Summerville, SC | Frost Law Group"), ("/domestic-violence-cdv (new)", "CDV / Domestic Violence Defense Attorney in Summerville, SC | Frost Law Group"), ("/guardianship-conservatorship (new)", "Guardianship & Conservatorship Attorney in Summerville, SC | Frost Law Group"), ("/asset-protection (new)", "Asset Protection Trust Attorney in Summerville, SC | Frost Law Group"), ("/elder-law-medicaid-planning (new)", "Elder Law & Medicaid Planning Attorney in Summerville, SC | Frost Law Group"), ("/last-will-and-testament", "Wills Lawyer in Summerville, SC | Last Will & Testament | Frost Law Group"), ("/revocable-trust", "Revocable Living Trust Attorney in Summerville, SC | Frost Law Group"), ("/power-of-attorney", "Power of Attorney Lawyer in Summerville, SC | Durable & Healthcare POA | Frost Law Group"), ("/living-will", "Living Will Attorney in Summerville, SC | Frost Law Group"), ("/about-us", "About Jack & Tara Frost | Summerville, SC Husband-and-Wife Law Firm | Frost Law Group"), ("/contact-us", "Contact Frost Law Group | Summerville, SC Attorneys | (843) 419-6653"), ("/blog", "In The Know: Estate, Probate & Criminal Law Guides for the Lowcountry | Frost Law Group")]
titles_pi = [("/", "Summerville Car Accident & Personal Injury Lawyers | Frost Law Group"), ("/practice-areas", "Personal Injury Practice Areas | Summerville, SC | Frost Law Group"), ("/practice-areas/car-accidents", "Summerville Car Accident Lawyer | Free Consultation | Frost Law Group"), ("/practice-areas/truck-accidents", "Summerville Truck Accident Lawyer | 18-Wheeler Crash Attorneys | Frost Law Group"), ("/practice-areas/motorcycle-accidents", "Summerville Motorcycle Accident Lawyer | Frost Law Group"), ("/practice-areas/dog-bites", "Summerville Dog Bite Lawyer | SC Strict-Liability Claims | Frost Law Group"), ("/practice-areas/wrongful-death", "Summerville Wrongful Death Lawyer | Frost Law Group"), ("/practice-areas/slip-and-fall", "Summerville Slip & Fall Lawyer | Premises Liability | Frost Law Group"), ("/practice-areas/workers-compensation", "Summerville Workers' Compensation Lawyer | Frost Law Group"), ("/practice-areas/catastrophic-injuries", "Catastrophic Injury Lawyer in Summerville, SC | Frost Law Group"), ("/practice-areas/rideshare-accidents (new)", "Summerville Uber & Lyft Accident Lawyer | Frost Law Group"), ("/practice-areas/drunk-driving-accidents (new)", "Hit by a Drunk Driver in Summerville, SC? | Frost Law Group"), ("/areas/goose-creek (new)", "Goose Creek Car Accident Lawyer | Frost Law Group"), ("/areas/north-charleston · /charleston · /mount-pleasant · /moncks-corner · /walterboro (new)", "[City] Car Accident & Personal Injury Lawyer | Frost Law Group"), ("/es/abogado-de-accidentes (new)", "Abogado de Accidentes de Carro en Summerville, SC | Frost Law Group"), ("/about", "Our Attorneys | Jack & Tara Frost | Summerville Accident Attorneys"), ("/contact", "Free Consultation | Summerville Accident Attorneys | 843-419-6653")]
add("<h4>frostlawgroupsc.com</h4>")
add(table([("Page", lambda r: f"<code>{esc(r[0])}</code>", ""), ("Proposed title", lambda r: esc(r[1]), "")], titles_main))
add("<h4>summervilleaccidentattorney.com</h4>")
add(table([("Page", lambda r: f"<code>{esc(r[0])}</code>", ""), ("Proposed title", lambda r: esc(r[1]), "")], titles_pi))
add("<h3>D. Redirect map</h3>")
add("<h4>frostlawgroupsc.com — one address per page</h4>")
add(table([("From", lambda r: f"<code>{esc(r[0])}</code>", ""), ("To (301)", lambda r: f"<code>{esc(r[1])}</code>", "")], [
    ("http://www.frostlawgroupsc.com/… and https://www.frostlawgroupsc.com/…", "https://frostlawgroupsc.com/…"), ("https://frostlawgroupsc.com/page/ (trailing slash)", "https://frostlawgroupsc.com/page"), ("/probate-2/", "/probate"),
    ("/about-us/?swcfpc=1 (and any ?swcfpc= address)", "/about-us (strip the parameter)"), ("/author/adminfrost-lawgroup-com/", "/about-us (or noindex the author archive)"), ("/motor-vehicle-personal-injury", "https://www.summervilleaccidentattorney.com/practice-areas/car-accidents (after the two-site decision)")]))
add("<h4>summervilleaccidentattorney.com — removed pages</h4>")
add(table([("From", lambda r: f"<code>{esc(r['path'])}</code>", ""), ("To (301)", lambda r: esc(r["to"]), ""), ("Impressions lost so far", lambda r: fmt(r["impressions"]), "n")], dead_rows +
          [dict(path="https://summervilleaccidentattorney.com/… (non-www, all pages)", to="https://www.summervilleaccidentattorney.com/… (same path)", impressions=sum(r["impressions"] for r in sva_pages if r["url"].startswith("https://summervilleaccidentattorney.com/practice-areas")) + 20),
           dict(path="/pedestrian-accident/ (old page Google still references)", to="new /practice-areas/pedestrian-accidents", impressions=0)]))
add("<h3>E. Market reference tables</h3>")
add("<h4>Monthly searches and ad prices for the terms in this report</h4>")
add(table([("Search", lambda r: esc(r["keyword"]), ""), ("Searches / mo", lambda r: fmt(r["volume"]) if r["volume"] else "–", "n"), ("Ad price / click", lambda r: money(r["cpc"]), "n"), ("Difficulty (0–100)", lambda r: (fmt(r["kd"]) if r["kd"] is not None else "–"), "n"), ("Intent", lambda r: r["intent"] or "–", "")],
          sorted(KM.values(), key=lambda r: -(r["volume"] or 0))))
add("<p class=\"small\">Difficulty is a 0–100 estimate of how strong the current page-one sites are; below 20 is winnable for a local firm with a good page. Hyper-local phrases with no row (dog bite, Goose Creek, motorcycle, Spanish) have no measurable volume in keyword databases; Search Console is the evidence for those.</p>")
add("<h4>What the main site ranks for today (market estimate)</h4>")
add(table([("Search", lambda r: esc(r["keyword"]), ""), ("Searches / mo", lambda r: fmt(r["volume"]) if r["volume"] else "–", "n"), ("Position", lambda r: fmt(r["rank"]) if r["rank"] else "–", "n"), ("Page", lambda r: f"<code>{esc(r['url'] or '/')}</code>", "")],
          FROST_RANKED[:20]))
add(f"<p class=\"small\">The main site ranks for {fmt(len(FROST_RANKED))} measurable searches; all of its page-one rankings are the firm's own name (and “all &amp; frost llc”, a different firm). Everything else sits on pages 3–7.</p>")
add("<h3>F. Glossary</h3>")
add("<dl>" + "".join(f"<dt><strong>{t}</strong></dt><dd>{d}</dd>" for t, d in [
    ("Impression", "One time Google showed a page of yours on a results page (including in the map pack via your Business Profile link and in AI answers)."), ("Click", "One time a person chose that result."), ("Position", "Where the result sat on the page, averaged over all the times it was shown. 1–10 is page one."), ("CTR", "Click-through rate: clicks ÷ impressions."),
    ("Query", "The exact words typed or spoken. Search Console hides very rare queries for privacy, which is why query totals are lower than site totals."), ("Brand / non-brand", "Brand searches contain the firm's name (“frost”). Non-brand searches are people who don't know you yet — the only ones that grow a practice."),
    ("Search volume", "The estimated number of times a phrase is searched per month in the United States (rounded). Local phrases are undercounted; Search Console impressions are the better local measure."), ("Cost per click", "What advertisers currently pay Google, on average, for one click on an ad shown for that search — a market price for one lead-shaped visit."),
    ("Map pack", "The three Business Profiles Google shows with a map at the top of a local search. Decided by relevance (categories), distance and prominence (reviews, photos, links)."), ("Referring domains", "The number of different websites that link to yours. A rough measure of reputation; quality matters more than count."),
    ("Canonical", "The one official address for a page. When a page has several addresses, Google picks one and treats the rest as copies."), ("301 redirect", "A permanent forward from an old address to a new one. It sends people and Google's trust to the new page."),
    ("Topical authority", "Being the site Google trusts most on one subject, earned by covering the subject completely and coherently."), ("Fan-out", "How Google's AI answers a big question: it splits it into smaller questions, searches each, and stitches the best paragraphs together."),
    ("Structured data (schema)", "Machine-readable labels in the page code that tell Google exactly who you are (LegalService, Attorney), what a block is (FAQPage), and what a video is (VideoObject)."), ("E-E-A-T", "Experience, Expertise, Authoritativeness, Trust — the qualities Google looks for on legal and financial pages; shown with real authors, credentials, reviews and consistent facts."),
]) + "</dl>")
add("<h3>G. Method notes</h3>")
add(f"<p class=\"small\">Both properties are domain properties in Google Search Console. The main site has data from {F_FIRST.isoformat()}; the injury site from {S_FIRST.isoformat()}. Query, page and date tables use the property's own reported values; where we group pages by address or queries by topic, the grouping is ours and the underlying numbers are unchanged. Page-level impressions can exceed site-level impressions because one search can show two of your pages. Positions are impression-weighted averages. Search volumes, ad prices, difficulty scores, competitor traffic estimates and link counts are third-party market estimates for the United States, gathered September 11, 2026, and rounded. Map-pack rankings were checked once from central Summerville (mobile) on September 11, 2026; results vary with the searcher's exact location. Observations about the live pages (titles, headings, word counts, not-found pages) were made the same day; Business Profile details are as shown publicly on Google.</p>")
add("</section>")
add('<footer class="small" style="margin-top:48px;padding-top:16px;border-top:1px solid var(--hair)">Frost Law Group Search Audit · prepared September 11, 2026 · your data: Google Search Console · market data: industry estimates, September 2026</footer></div>')

html = "\n".join(parts)
head, body = html.split('<div class="sheet">', 1)
body = '<div class="sheet">' + body
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n' + head + '</head><body>\n' + body + '\n</body></html>')
print("wrote", OUT, os.path.getsize(OUT), "bytes")
ART = os.environ.get("ART_OUT")
if ART:
    with open(ART, "w") as f:
        f.write(head + body)
    print("wrote", ART)
print("fan-out:", FAN_N, FAN_I, "| quick wins main:", len(quick_frost), "| injury:", len(quick_sva), "| dead:", len(dead_rows), DEAD_I, "| multi-address:", len(MULTI), "| gap rows:", len(gap_rows), "| pack firms:", len(firm_rows), "median reviews", PACK_MEDIAN_REVIEWS)
