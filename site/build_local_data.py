#!/usr/bin/env python3
"""Turn the verified research file (site/content/facts.json, assembled from official county, court,
state-code and OpenStreetMap sources) into the compact local_data.json the site generator reads.

    python3 site/build_local_data.py            # writes site/content/local_data.json

Routes for communities the research file lacks are computed with OSRM (public demo server); if the
network is unavailable those pages simply omit the distance line.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "content", "facts.json")
OUT = os.path.join(HERE, "content", "local_data.json")
UA = "frost-law-site-build/1.0 (contact: site build script)"

facts = json.load(open(SRC, encoding="utf-8"))
office = facts["office"]
LAT, LON = office["geocode"]["lat"], office["geocode"]["lon"]

# ----------------------------------------------------------------------------- courts
PHONE_RE = re.compile(r"\(?(\d{3})\)?[ -]?(\d{3})-(\d{4})")


def phone(s):
    m = PHONE_RE.search(s or "")
    return f"({m.group(1)}) {m.group(2)}-{m.group(3)}" if m else ""


C = facts["courts"]
mag = C["dorchester_county_magistrate_courts"]
courts = {
    "dorchester_courthouse": dict(name="Dorchester County Courthouse (Clerk of Court; General Sessions and Common Pleas)", street="5200 E. Jim Bilton Blvd.", city="St. George", zip="29477", phone=phone(C["dorchester_county_courthouse_clerk_of_court"]["phone"]), url=C["dorchester_county_courthouse_clerk_of_court"]["url"], note="Family Court sits at the Troy Knight Judicial Complex, 212 Deming Way, Summerville."),
    "dorchester_probate": dict(name="Dorchester County Probate Court", street="5200 E. Jim Bilton Blvd.", city="St. George", zip="29477", phone=phone(C["dorchester_county_probate_court"]["phone"]), url=C["dorchester_county_probate_court"]["url"], note="Estates, guardianships and conservatorships for Dorchester County residents. Call before visiting; hearings are by appointment."),
    "dorchester_magistrate_summerville": dict(name="Dorchester County Magistrate Court – Summerville (Troy Knight Judicial Complex)", street="212 Deming Way", city="Summerville", zip="29483", phone=phone(mag[1]["phone"]), url=mag[1]["url"], note="Bond hearings, misdemeanors and tickets written by the Sheriff's Office or Highway Patrol in the Summerville area."),
    "dorchester_magistrate_stgeorge": dict(name="Dorchester County Magistrate Court – St. George", street="5200 E. Jim Bilton Blvd.", city="St. George", zip="29477", phone=phone(mag[0]["phone"]), url=mag[0]["url"], note=""),
    "summerville_municipal": dict(name="Summerville Municipal Court", street="200 S. Main Street, 2nd Floor (Town Hall)", city="Summerville", zip="29483", phone=phone(C["summerville_municipal_court"]["phone"]), url=C["summerville_municipal_court"]["url"], note="Tickets and ordinance cases from the Summerville Police Department."),
    "berkeley_courthouse": dict(name="Berkeley County Courthouse (Clerk of Court; General Sessions and Common Pleas)", street="300-B California Avenue", city="Moncks Corner", zip="29461", phone=phone(C["berkeley_county_courthouse_clerk_of_court"]["phone"]), url=C["berkeley_county_courthouse_clerk_of_court"]["url"], note=""),
    "berkeley_probate": dict(name="Berkeley County Probate Court", street="300-B California Avenue", city="Moncks Corner", zip="29461", phone=phone(C["berkeley_county_probate_court"]["phone"]), url=C["berkeley_county_probate_court"]["url"], note="Estates, guardianships and conservatorships for Berkeley County residents, including Goose Creek, Hanahan, Nexton, Cane Bay and Daniel Island."),
    "goose_creek_municipal": dict(name="Goose Creek Municipal Court (Marguerite H. Brown Municipal Center)", street="519 N. Goose Creek Blvd.", city="Goose Creek", zip="29445", phone=phone(C["goose_creek_municipal_court"]["phone"]), url=C["goose_creek_municipal_court"]["url"], note=""),
    "hanahan_municipal": dict(name="Hanahan Municipal Court (City Hall)", street="1255 Yeamans Hall Road", city="Hanahan", zip="29410", phone=phone(C["hanahan_municipal_court"]["phone"]), url=C["hanahan_municipal_court"]["url"], note=""),
    "charleston_judicial": dict(name="Charleston County Judicial Center (Clerk of Court; General Sessions and Common Pleas)", street="100 Broad Street, Suite 106", city="Charleston", zip="29401", phone=phone(C["charleston_county_judicial_center"]["phone"]), url=C["charleston_county_judicial_center"]["url"], note=""),
    "charleston_probate": dict(name="Charleston County Probate Court", street="100 Broad Street, Suite 469 (Historic Courthouse, 84 Broad Street)", city="Charleston", zip="29401", phone=phone(C["charleston_county_probate_court"]["phone"]), url=C["charleston_county_probate_court"]["url"], note="Estates, guardianships and conservatorships for Charleston County residents, including North Charleston, Mount Pleasant, West Ashley, James Island and Johns Island."),
    "north_charleston_municipal": dict(name="North Charleston Municipal Court", street="2500 City Hall Lane", city="North Charleston", zip="29406", phone=phone(C["north_charleston_municipal_court"]["phone"]), url=C["north_charleston_municipal_court"]["url"], note=""),
    "charleston_municipal": dict(name="City of Charleston Municipal Court", street="180 Lockwood Boulevard, Suite B", city="Charleston", zip="29403", phone=phone(C["charleston_municipal_court"]["phone"]), url=C["charleston_municipal_court"]["url"], note="Charleston Police cases from downtown, West Ashley, James Island, Johns Island and Daniel Island."),
    "colleton_courthouse": dict(name="Colleton County Courthouse (Clerk of Court)", street="101 Hampton Street", city="Walterboro", zip="29488", phone=phone(C["colleton_county_courthouse_clerk_of_court"]["phone"]), url=C["colleton_county_courthouse_clerk_of_court"]["url"], note=""),
    "colleton_probate": dict(name="Colleton County Probate Court", street="239 N. Jefferies Blvd.", city="Walterboro", zip="29488", phone=phone(C["colleton_county_probate_court"]["phone"]), url=C["colleton_county_probate_court"]["url"], note=""),
    "dorchester_sheriff": dict(name="Dorchester County Sheriff's Office", street="212 Deming Way", city="Summerville", zip="29483", phone=phone(C["dorchester_county_sheriffs_office"]["phone"]), url=C["dorchester_county_sheriffs_office"]["url"], note="St. George office: 101 Ridge Street, Suite 1."),
    "summerville_pd": dict(name="Summerville Police Department", street="300 W. 2nd North Street", city="Summerville", zip="29483", phone=phone(C["summerville_police_department"]["phone"]), url=C["summerville_police_department"]["url"], note=""),
    "dorchester_detention": dict(name="Dorchester County Detention Center", street="220 Hodge Road (off US-78)", city="Summerville", zip="29483", phone=phone(C["dorchester_county_detention_center"]["phone"]), url=C["dorchester_county_detention_center"]["url"], note="Bond hearings for Dorchester County arrests are held here, in Summerville—not in St. George."),
    "hill_finklea": dict(name="Hill-Finklea Detention Center (Berkeley County)", street="300 California Avenue", city="Moncks Corner", zip="29461", phone=phone(C["hill_finklea_detention_center"]["phone"]), url=C["hill_finklea_detention_center"]["url"], note="Bond hearings for Berkeley County arrests."),
    "al_cannon": dict(name="Sheriff Al Cannon Detention Center (Charleston County)", street="3841 Leeds Avenue", city="North Charleston", zip="29405", phone=phone(C["al_cannon_detention_center"]["phone"]), url=C["al_cannon_detention_center"]["url"], note="Bond hearings for Charleston County arrests."),
}

# ----------------------------------------------------------------------------- routes
ROUTE_MAP = {
    "i26-199": ("1a_I26_exit199A_node_A", "I-26 exit 199A (N. Main Street / US-17A)"),
    "goose-creek": ("2_goose_creek_city_hall", "Goose Creek (City Hall)"),
    "ladson": ("3_ladson_college_park_us78", "Ladson (College Park Road at US-78)"),
    "moncks-corner": ("4_berkeley_county_courthouse", "Moncks Corner (Berkeley County Courthouse)"),
    "north-charleston": ("5_tanger_outlets_i26_exit213", "North Charleston (Tanger Outlets, I-26 exit 213)"),
    "charleston": ("6_downtown_charleston_100_broad", "downtown Charleston (100 Broad Street)"),
    "ridgeville": ("7_ridgeville_sc27_us78", "Ridgeville (SC-27 at US-78)"),
    "st-george": ("8_dorchester_courthouse_stgeorge", "St. George (Dorchester County Courthouse)"),
    "knightsville": ("9_knightsville_central_orangeburg", "Knightsville (Central Avenue at Orangeburg Road)"),
    "nexton": ("10_nexton_pkwy_i26_exit197", "Nexton (I-26 exit 197)"),
    "cane-bay": ("11_cane_bay_blvd_sc176", "Cane Bay (Cane Bay Boulevard at US-176)"),
    "walterboro": ("12_walterboro_colleton_courthouse", "Walterboro (Colleton County Courthouse)"),
    "mount-pleasant": ("13_mt_pleasant_coleman_blvd", "Mount Pleasant (Coleman Boulevard)"),
    "hanahan": ("14_hanahan_city_hall", "Hanahan (City Hall)"),
    "harleyville": ("15_harleyville", "Harleyville"),
    "lincolnville": ("16_lincolnville", "Lincolnville"),
    "sangaree": ("17_sangaree", "Sangaree"),
}
EXTRA_ORIGINS = {  # geocoded on the fly; falls back gracefully
    "daniel-island": "Daniel Island, Charleston, SC",
    "west-ashley": "West Ashley, Charleston, SC",
    "james-island": "James Island, SC",
    "johns-island": "Johns Island, SC",
    "ravenel": "Ravenel, SC",
    "hollywood": "Hollywood, SC",
    "reevesville": "Reevesville, SC",
    "carnes-crossroads": "Carnes Crossroads, Summerville, SC",
    "jedburg": "Jedburg, SC",
}
NAME_FIX = [("US 17 Alternate", "US-17A"), ("US 17 Alt", "US-17A"), ("(US 78)", "(US-78)"), ("(US 176)", "(US-176)"), ("(US 52)", "(US-52)"), ("(US 178)", "(US-178)"),
            ("(SC 642)", "(SC-642)"), ("(SC 703)", "(SC-703)"), ("(SC 63)", "(SC-63)"), ("(SC 64)", "(SC-64)"), ("(SC 6)", "(SC-6)"), ("(SC 453)", "(SC-453)"), ("(S-107)", ""), ("(SR S-8-21)", ""), ("I 26", "I-26")]


def clean_names(seq):
    out = []
    for raw in [x.strip() for x in seq.split("->")]:
        if not raw or raw.startswith("depart") or raw in ("on ramp", "off ramp", "fork"):
            continue
        m = re.match(r"off ramp \[exit (\w+)\]", raw)
        name = f"I-26 to exit {m.group(1)}" if m else raw
        for a, b in NAME_FIX:
            name = name.replace(a, b)
        name = re.sub(r"\((US|SC|I) (\d+[A-Z]?)(?:; (US|SC) (\d+))?\)", lambda m: "(" + m.group(1) + "-" + m.group(2) + ("/" + m.group(3) + "-" + m.group(4) if m.group(3) else "") + ")", name)
        name = re.sub(r"^(US|SC|I) (\d+[A-Z]?)$", r"\1-\2", name)
        name = re.sub(r"^State Highway (\d+) \(SC-\1\)$", r"SC-\1", name)
        name = re.sub(r"\s+", " ", name).strip()
        key = re.sub(r"[^a-z0-9]", "", name.lower().replace("street north", "north street"))
        refm = re.search(r"\((US|SC|I)-(\d+[A-Z]?)\)$", name) or re.match(r"^(US|SC|I)-(\d+[A-Z]?)$", name)
        ref = (refm.group(1) + "-" + refm.group(2)) if refm else None
        if out and out[-1][0] == key:
            continue
        if ref and out and out[-1][2] == ref and out[-1][1] != "I-26":
            continue
        if name == "I-26" and out and out[-1][1].startswith("I-26"):
            continue
        if out and out[-1][1] == "I-26" and name.startswith("I-26 to exit"):
            out.pop()
        out.append((key, name, ref))
    return [n for _, n, _ in out]


def sentence(names):
    names = [n for n in names if n]
    if not names:
        return ""
    if names[-1] != "Linwood Lane":
        names.append("Linwood Lane")
    if len(names) == 2:
        return f"Take {names[0]} and turn onto {names[1]}."
    mid = names[1:-1]
    return f"Follow {names[0]} to {mid[0]}" + (", then " + ", ".join(mid[1:]) if mid[1:] else "") + f", and turn onto {names[-1]}."


routes = {}
by_id = {r["id"]: r for r in office["routes_to_office"]}
for key, (rid, label) in ROUTE_MAP.items():
    r = by_id[rid]
    routes[key] = dict(**{"from": label}, text=sentence(clean_names(r["roads_in_order"])), miles=f"{r['driving_distance_mi']:.0f}" if r["driving_distance_mi"] >= 10 else f"{r['driving_distance_mi']:.1f}", minutes=str(r["driving_time_min"]))


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as f:
        return json.load(f)


def osrm_route(name, query):
    try:
        g = fetch_json("https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": query, "format": "json", "limit": 1}))
        if not g:
            return None
        lat, lon = float(g[0]["lat"]), float(g[0]["lon"])
        r = fetch_json(f"https://router.project-osrm.org/route/v1/driving/{lon},{lat};{LON},{LAT}?steps=true&overview=false")
        route = r["routes"][0]
        names = []
        for step in route["legs"][0]["steps"]:
            n = step.get("name") or ""
            ref = step.get("ref") or ""
            if step["maneuver"]["type"] == "arrive":
                continue
            if not n and ref:
                n = ref
            if n:
                label = n + (f" ({ref})" if ref and ref not in n else "")
                names.append(label)
        seq = " -> ".join(names)
        miles = route["distance"] / 1609.34
        mins = round(route["duration"] / 60)
        return dict(**{"from": name}, text=sentence(clean_names(seq)), miles=f"{miles:.0f}" if miles >= 10 else f"{miles:.1f}", minutes=str(mins))
    except Exception as e:  # network optional
        print("route skipped", name, e, file=sys.stderr)
        return None


for key, q in EXTRA_ORIGINS.items():
    label = q.split(",")[0]
    r = osrm_route(label, q)
    if r:
        routes[key] = r

# ----------------------------------------------------------------------------- places
STATUS = {
    "Summerville": "Incorporated town", "Goose Creek": "Incorporated city", "Ladson": "Census-designated place (unincorporated), spanning three counties",
    "North Charleston": "Incorporated city", "Moncks Corner": "Incorporated town; Berkeley County seat", "Hanahan": "Incorporated city",
    "Charleston": "Incorporated city; Charleston County seat", "Mount Pleasant": "Incorporated town", "Ridgeville": "Incorporated town",
    "St. George": "Incorporated town; Dorchester County seat", "Harleyville": "Incorporated town", "Walterboro": "Incorporated city; Colleton County seat",
    "Knightsville": "Unincorporated community straddling the Summerville town line", "Sangaree": "Census-designated place (unincorporated)",
    "Nexton": "Master-planned community inside the Summerville town limits", "Cane Bay": "Master-planned community, unincorporated Berkeley County",
    "Lincolnville": "Incorporated town", "Daniel Island": "Neighborhood of the City of Charleston", "West Ashley": "Area of the City of Charleston",
    "James Island": "Town of James Island and City of Charleston", "Johns Island": "Largely unincorporated, with City of Charleston portions",
    "Ravenel": "Incorporated town", "Hollywood": "Incorporated town", "Reevesville": "Incorporated town",
    "Carnes Crossroads": "Master-planned community, unincorporated Berkeley County", "Jedburg": "Unincorporated community",
}
SLUG = {n: re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-") for n in STATUS}
SLUG["St. George"] = "st-george"
places = {}
for name, pl in facts["places"].items():
    if name not in SLUG:
        continue
    zips = sorted(set(re.findall(r"\b29\d{3}\b", " ".join(pl.get("zips") or []))))
    counties = [c.split(" (")[0] + " County" for c in pl.get("counties") or []]
    lm = []
    for l in pl.get("landmarks") or []:
        l = re.sub(r"\s*\((?:[^()]*(?:OSM|Wikipedia|per |census|ZCTA|node)[^()]*)\)", "", l)
        l = re.sub(r"\s+", " ", l).strip(" ;,-")
        if l:
            lm.append(l)
    pop = pl.get("population_2020")
    places[SLUG[name]] = dict(county_note=", ".join(counties), status=STATUS[name], zips=zips, population=f"{pop:,}" if pop else None, landmarks=lm[:3])

# ----------------------------------------------------------------------------- statutes and links
SH = "https://www.scstatehouse.gov/code/"
statutes = {
    "will_execution": ("S.C. Code § 62-2-502", SH + "t62c002.php"), "self_proved": ("S.C. Code § 62-2-503", SH + "t62c002.php"),
    "intestacy": ("S.C. Code §§ 62-2-102 and 62-2-103", SH + "t62c002.php"), "elective_share": ("S.C. Code § 62-2-201", SH + "t62c002.php"),
    "will_delivery": ("S.C. Code § 62-2-901", SH + "t62c002.php"), "creditor_period": ("S.C. Code § 62-3-801", SH + "t62c003.php"),
    "small_estate": ("S.C. Code § 62-3-1201", SH + "t62c003.php"), "estate_time_limit": ("S.C. Code § 62-3-108", SH + "t62c003.php"),
    "guardianship": ("S.C. Code Title 62, Article 5", SH + "t62c005.php"), "hcpoa": ("S.C. Code §§ 62-5-503 and 62-5-504", SH + "t62c005.php"),
    "trust_code": ("S.C. Code § 62-7-813", SH + "t62c007.php"), "poa_act": ("S.C. Code Title 62, Article 8 (Uniform Power of Attorney Act)", SH + "t62c008.php"),
    "living_will_act": ("S.C. Code § 44-77-10 et seq. (Death with Dignity Act)", SH + "t44c077.php"), "probate_fees": ("S.C. Code § 8-21-770", SH + "t08c021.php"),
    "pti": ("S.C. Code § 17-22-10 et seq.", SH + "t17c022.php"), "expungement": ("Act 254 of 2018; S.C. Code § 17-22-910 et seq.", facts["law"]["act_254_of_2018_expungement_reform"]["url"]),
    "expungement_misdemeanor": ("S.C. Code § 22-5-910", SH + "t22c005.php"), "yoa": ("S.C. Code § 22-5-920", SH + "t22c005.php"),
    "conditional_discharge": ("S.C. Code § 44-53-450", SH + "t44c053.php"), "drugs": ("S.C. Code § 44-53-370", SH + "t44c053.php"),
    "cdv": ("S.C. Code § 16-25-20", SH + "t16c025.php"), "bond": ("S.C. Code § 22-5-510", SH + "t22c005.php"), "warrants": ("S.C. Code § 22-5-110", SH + "t22c005.php"),
    "points": ("S.C. Code § 56-1-720", SH + "t56c001.php"), "dui": ("S.C. Code § 56-5-2930", SH + "t56c005.php"), "duac": ("S.C. Code § 56-5-2933", SH + "t56c005.php"),
    "implied_consent": ("S.C. Code §§ 56-5-2950 and 56-5-2951", SH + "t56c005.php"), "dui_video": ("S.C. Code § 56-5-2953", SH + "t56c005.php"),
}
statutes = {k: dict(label=v[0], url=v[1]) for k, v in statutes.items()}

links = {
    "pc_summerville": ("The Post and Courier – Summerville", "https://www.postandcourier.com/summerville/", False),
    "pc_journal_scene": ("Summerville Journal Scene (Post and Courier)", "https://www.postandcourier.com/journal-scene/", False),
    "berkeley_independent": ("The Berkeley Independent (Post and Courier)", "https://www.postandcourier.com/berkeley-independent/", False),
    "moultrie_news": ("Moultrie News (Post and Courier)", "https://www.postandcourier.com/moultrie-news/", False),
    "live5": ("Live 5 News (WCSC)", "https://www.live5news.com/news/", False),
    "abcnews4": ("ABC News 4 (WCIV) – local news", "https://abcnews4.com/news/local", False),
    "wcbd": ("WCBD News 2 – local news", "https://www.counton2.com/news/local-news/", False),
    "city_paper": ("Charleston City Paper – news", "https://charlestoncitypaper.com/category/news/", False),
    "nextdoor_summerville": ("Nextdoor – Summerville, SC", "https://nextdoor.com/city/summerville--sc/", True),
    "nextdoor_goose_creek": ("Nextdoor – Goose Creek, SC", "https://nextdoor.com/city/goose-creek--sc/", True),
    "nextdoor_ladson": ("Nextdoor – Ladson, SC", "https://nextdoor.com/city/ladson--sc/", True),
    "nextdoor_moncks_corner": ("Nextdoor – Moncks Corner, SC", "https://nextdoor.com/city/moncks-corner--sc/", True),
    "nextdoor_north_charleston": ("Nextdoor – North Charleston, SC", "https://nextdoor.com/city/north-charleston--sc/", True),
    "reddit_charleston": ("r/Charleston on Reddit", "https://www.reddit.com/r/Charleston/", True),
    "reddit_summerville": ("r/SummervilleSC on Reddit", "https://www.reddit.com/r/SummervilleSC/", True),
    "reddit_southcarolina": ("r/southcarolina on Reddit", "https://www.reddit.com/r/southcarolina/", True),
    "dorchester_news": ("Dorchester County – news and notices", "https://www.dorchestercountysc.gov/services/advanced-components/news-list", False),
    "berkeley_newsroom": ("Berkeley County – newsroom", "https://berkeleycountysc.gov/newsroom/", False),
    "summerville_news": ("Town of Summerville – news flash", "https://www.summervillesc.gov/CivicAlerts.aspx", False),
    "sccourts_roster": ("SC Judicial Branch – court roster search", "https://www.sccourts.org/court-roster-search/", False),
    "sccourts_probate_forms": ("SC Judicial Branch – court forms", "https://www.sccourts.org/forms/", False),
    "scemd": ("South Carolina Emergency Management Division", "https://www.scemd.org/", False),
    "dorchester_emd": ("Dorchester County Emergency Management", "https://www.dorchestercountysc.gov/government/public-safety/emergency-management", False),
    "trident_aging": ("Trident Area Agency on Aging", "https://www.tridentaaa.org/", False),
    "dd2": ("Dorchester School District Two", "https://www.ddtwo.org/", False),
    "my_sisters_house": ("My Sister's House (24-hour line and shelter)", "https://mysistershouse.org/", False),
    "summerville_pd": ("Summerville Police Department", "https://www.summervillepolice.com/", False),
    "dorchester_sheriff": ("Dorchester County Sheriff's Office", courts["dorchester_sheriff"]["url"], False),
    "dorchester_probate_site": ("Dorchester County Probate Court", courts["dorchester_probate"]["url"], False),
    "berkeley_probate_site": ("Berkeley County Probate Court", courts["berkeley_probate"]["url"], False),
    "charleston_probate_site": ("Charleston County Probate Court", courts["charleston_probate"]["url"], False),
    "dorchester_county": ("Dorchester County government", "https://www.dorchestercountysc.gov/", False),
    "berkeley_county": ("Berkeley County government", "https://berkeleycountysc.gov/", False),
}
links = {k: dict(label=v[0], url=v[1], nofollow=v[2]) for k, v in links.items()}

office_out = dict(
    lat=LAT, lon=LON,
    roads_sentence=("Our office is in the southwest corner of Summerville's historic core, just off West Carolina Avenue near the Pine Forest Inn historical marker: "
                    "about a mile southwest of Town Hall and Hutchinson Square, a third of a mile northwest of South Main Street (US-17A), half a mile from Berlin G. Myers Parkway, "
                    "under a mile north of the Bacons Bridge Road and Old Trolley Road junction, and three miles southwest of I-26 exits 199A and 199B. "
                    "Linwood Lane runs between West Carolina Avenue and Salisbury Drive."),
)

out = dict(generated=facts["meta"].get("generated"), office=office_out, office_geo=[LAT, LON], courts=courts, routes=routes, places=places, statutes=statutes, links=links)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {OUT}: {len(courts)} courts, {len(routes)} routes, {len(places)} places, {len(statutes)} statutes, {len(links)} links")
