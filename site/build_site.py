#!/usr/bin/env python3
"""Static-site generator for the frostlawgroupsc.com rebuild.

    python3 site/build_site.py                 -> website/  (production: one folder per URL, sitemap, .htaccess)
    python3 site/build_site.py --preview OUT   -> single-file preview with a hash router (for the artifact)

Content lives in site/content/*.py; assets in site/assets/.
"""
import argparse
import base64
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
IMG_DIR = os.path.join(ASSETS, "img")
OUT = os.path.join(ROOT, "website")
sys.path.insert(0, SITE)

from content.base import PAGES, BY_SLUG, esc  # noqa: E402
from content import firm  # noqa: E402
import content.core  # noqa: E402,F401  (registers pages)
import content.estate  # noqa: E402,F401
import content.probate  # noqa: E402,F401
import content.criminal  # noqa: E402,F401
import content.cities  # noqa: E402,F401
import content.posts  # noqa: E402,F401

BUILD_DATE = firm.BUILD_DATE
ORIGIN = firm.ORIGIN
MODE = "prod"
WARNINGS = []
CSS_HREF = "/assets/site.css"


def file_hash(path, n=8):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()[:n]


def warn(msg):
    WARNINGS.append(msg)


# ---------------------------------------------------------------- URLs & images

def url(slug):
    if slug == "home":
        return "/" if MODE == "prod" else "#/"
    return f"/{slug}/" if MODE == "prod" else f"#/{slug}/"


def abs_url(slug):
    return ORIGIN + ("/" if slug == "home" else f"/{slug}/")


_IMG_CACHE = {}
_PLACEHOLDERS = {}


def image_info(name):
    """Return (src, width, height) for an image name; falls back to a generated SVG placeholder."""
    if name in _IMG_CACHE:
        return _IMG_CACHE[name]
    path = os.path.join(IMG_DIR, name)
    if os.path.exists(path):
        if name.lower().endswith(".svg"):
            w, h = 1200, 800
            m = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(path, encoding="utf-8").read())
            if m:
                w, h = int(m.group(1)), int(m.group(2))
            if MODE == "prod":
                src = f"/assets/img/{name}?v={file_hash(path)}"
            else:
                src = "data:image/svg+xml;base64," + base64.b64encode(open(path, "rb").read()).decode()
        else:
            im = Image.open(path)
            w, h = im.size
            if MODE == "prod":
                src = f"/assets/img/{name}?v={file_hash(path)}"
            else:
                buf = io.BytesIO()
                im2 = im.convert("RGB") if im.mode not in ("RGB", "RGBA") else im
                mx = 900
                if im2.width > mx:
                    im2 = im2.resize((mx, round(im2.height * mx / im2.width)), Image.LANCZOS)
                if name.lower().endswith(".png") and im2.mode == "RGBA":
                    im2.save(buf, "PNG", optimize=True)
                    src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
                else:
                    im2.convert("RGB").save(buf, "JPEG", quality=78, optimize=True, progressive=True)
                    src = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    else:
        warn(f"missing image {name}; placeholder used")
        w, h = (1200, 900) if not name.startswith("head") else (800, 1000)
        label = os.path.splitext(name)[0].replace("-", " ").title()
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
               f'<stop offset="0" stop-color="#173b66"/><stop offset="1" stop-color="#3f86bd"/></linearGradient></defs>'
               f'<rect width="{w}" height="{h}" fill="url(#g)"/><text x="50%" y="52%" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w/22)}" fill="#ffffff" opacity=".9">{esc(label)}</text>'
               f'<text x="50%" y="60%" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w/40)}" fill="#dbe7f3">photo to be supplied</text></svg>')
        _PLACEHOLDERS[name] = svg
        pname = "placeholder-" + os.path.splitext(name)[0] + ".svg"
        src = f"/assets/img/{pname}" if MODE == "prod" else "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    _IMG_CACHE[name] = (src, w, h)
    return _IMG_CACHE[name]


def fix_images(html):
    def rep(m):
        tag = m.group(0)
        name = m.group(1)
        src, w, h = image_info(name)
        tag = tag.replace(f"[[img:{name}]]", src)
        if " width=" not in tag:
            tag = tag[:-1] + f' width="{w}" height="{h}">'
        return tag
    return re.sub(r'<img[^>]*src="\[\[img:([^\]]+)\]\]"[^>]*>', rep, html)


def img_tag(name, alt, extra='loading="lazy" decoding="async"'):
    return fix_images('<img src="[[img:%s]]" alt="%s" %s>' % (name, esc(alt), extra))

# ---------------------------------------------------------------- token expansion

def card(pg, new=None):
    isnew = (pg["card_new"] if new is None else new) and MODE == "preview"
    return (f'<li class="card{" new" if isnew else ""}"><h3><a href="{url(pg["slug"])}">{esc(pg["nav_label"])}</a></h3>'
            f'<p>{pg["summary"]}</p><a class="more" href="{url(pg["slug"])}">Learn more</a></li>')


def cards(slugs):
    return '<ul class="cards">' + "".join(card(BY_SLUG[s]) for s in slugs) + "</ul>"


def post_card(pg):
    a = firm.ATTORNEYS[pg["author"]]
    return (f'<li class="post-card"><div class="cat">{esc(pg["category"])}</div><h3><a href="{url(pg["slug"])}">{esc(pg["h1"])}</a></h3>'
            f'<p>{pg["summary"]}</p><div class="meta">{fmt_date(pg["date"])} · {esc(a["short"])}</div></li>')


def posts_sorted():
    return sorted([p for p in PAGES if p["kind"] == "post"], key=lambda p: p["date"], reverse=True)


def fmt_date(d):
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")


def reviews_html(n):
    out = []
    for r in firm.REVIEWS[:n]:
        out.append(f'<blockquote class="review"><div class="stars" aria-label="{r["stars"]} out of 5 stars">{"★" * r["stars"]}</div><p>“{esc(r["text"])}”</p><footer><b>{esc(r["name"])}</b> · {esc(r["source"])}</footer></blockquote>')
    return '<div class="cards three" style="list-style:none">' + "".join(out) + "</div>"


def team_html():
    figs = []
    for key in ("jack", "tara", "cassie", "dogs"):
        m = firm.TEAM[key]
        inner = f'{img_tag(m["photo"], m["alt"])}<figcaption><b>{esc(m["name"])}</b><span>{esc(m["role"])}</span></figcaption>'
        if m.get("slug"):
            inner = f'<a href="{url(m["slug"])}" style="text-decoration:none">{inner}</a>'
        figs.append(f"<figure>{inner}</figure>")
    return '<div class="team">' + "".join(figs) + "</div>"


def hours_html():
    return '<ul class="hours">' + "".join(f"<li><span>{d}</span><span>{h}</span></li>" for d, h in firm.HOURS_DISPLAY) + "</ul>"


def nap_html():
    return ('<div class="nap">'
            f'<div><h3>Office</h3><p><b>{esc(firm.NAME)}</b><br>{firm.STREET}<br>{firm.CITY}, {firm.STATE} {firm.ZIP}</p>'
            f'<p><a href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Get directions</a> · <a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Google Business Profile</a></p></div>'
            f'<div><h3>Call or text</h3><p><a href="tel:{firm.PHONE_E164}" style="font-family:var(--display);font-size:1.4rem;font-weight:600;text-decoration:none">{firm.PHONE}</a></p><p class="small">Friday afternoon appointments available on request.</p></div>'
            f'<div><h3>Hours</h3>{hours_html()}</div></div>')


def map_html():
    q = esc(firm.MAP_QUERY)
    embed = esc(firm.MAP_EMBED_URL)
    return (f'<div class="map" data-embed="{embed}"><div class="inner"><div class="pin"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg></div>'
            f'<p><b>{esc(firm.NAME)}</b><br>{firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}</p>'
            f'<button class="btn sm" type="button" data-loadmap>Load the interactive map</button>'
            f'<p><a href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Open turn-by-turn directions in Google Maps</a></p></div></div>')


def findus_html():
    items = [
        (firm.GBP_URL, "Google Business Profile", "g"),
        (firm.REVIEW_URL, "Leave a Google review", "star"),
        (firm.PREFERRED_SOURCE_URL, "Add us as a preferred source on Google", "g"),
        (firm.YELP_URL, "Find us on Yelp", "yelp"),
        (firm.FACEBOOK, "Facebook", "fb"),
        (firm.INSTAGRAM, "Instagram", "ig"),
    ]
    out = []
    for href, label, ic in items:
        if not href:
            continue
        out.append(f'<a href="{esc(href)}" rel="noopener" target="_blank">{ICONS.get(ic, "")}{esc(label)}</a>')
    return '<div class="links">' + "".join(out) + "</div>"


def citylist_html():
    cities = [p for p in PAGES if p["kind"] == "city"]
    by_county = {}
    for c in cities:
        by_county.setdefault(c["county"], []).append(c)
    out = []
    for county in firm.COUNTY_ORDER:
        if county not in by_county:
            continue
        lis = "".join(f'<li><a href="{url(c["slug"])}">{esc(c["nav_label"])}</a><small>{esc(c["section_label"] or "")}</small></li>' for c in sorted(by_county[county], key=lambda x: x["nav_label"]))
        out.append(f'<h3>{esc(county)}</h3><ul class="areas">{lis}</ul>')
    return "".join(out)


def courts_html(keys):
    out = []
    for k in keys:
        c = firm.COURTS.get(k)
        if not c:
            warn(f"court {k} missing from local_data.json")
            continue
        addr = f'{esc(c["street"])}, {esc(c["city"])}, SC {esc(c["zip"])}'
        extra = f'<p>{esc(c["note"])}</p>' if c.get("note") else ""
        link = f' · <a href="{esc(c["url"])}" rel="noopener" target="_blank">Website</a>' if c.get("url") else ""
        phone = f' · {esc(c["phone"])}' if c.get("phone") else ""
        out.append(f'<div class="court"><h3>{esc(c["name"])}</h3><p>{addr}{phone}{link}</p>{extra}</div>')
    return '<div class="county-grid">' + "".join(out) + "</div>"


def author_box(key, reviewer=None):
    a = firm.ATTORNEYS[key]
    rev = ""
    if reviewer:
        r = firm.ATTORNEYS[reviewer]
        rev = f' Reviewed by <a href="{url(r["slug"])}">{esc(r["name"])}</a>.'
    return (f'<div class="byline">{img_tag(a["headshot"], a["name"])}'
            f'<p><b>Written by <a href="{url(a["slug"])}">{esc(a["name"])}</a></b>, {esc(a["byline"])}.{rev}</p></div>')


ICONS = {
    "g": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 12.2c0-.7-.1-1.3-.2-1.9H12v3.7h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"/><path d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1a6 6 0 0 1-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z"/><path d="M6.4 14a6 6 0 0 1 0-3.9V7.5H3.1a10 10 0 0 0 0 9.1L6.4 14z"/><path d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.5L6.4 10A6 6 0 0 1 12 6z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.6 7 .8-5.2 4.8 1.4 7L12 17.7 5.8 21.2l1.4-7L2 9.4l7-.8z"/></svg>',
    "yelp": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.6 2.4c.5-.7 1.6-.5 1.8.4l.3 8.6c0 .9-1 1.4-1.7.9L4.6 8.2c-.7-.5-.5-1.6.3-1.8l5.7-4zm2.7 11.2 6.7-2.3c.9-.3 1.7.7 1.2 1.5l-2.4 3.4c-.5.7-1.6.6-1.9-.2l-3.7-1.4c-.4-.3-.3-.9.1-1zm-1 2.5 5 5.1c.6.7 0 1.8-.9 1.6l-4.1-1c-.8-.2-1.1-1.2-.6-1.8l.5-3.7c0-.5.7-.6 1-.2h-.9zm-2.1-1 .9 7c.1.9-1 1.5-1.7 1L6 21.1c-.7-.5-.5-1.6.3-1.9l3.6-3.6c.3-.4.9-.2.9.3l-.6-.8zm-.5-2.2L3.4 14c-.9.3-1.7-.7-1.2-1.5l2.4-3.4c.5-.7 1.6-.6 1.9.2l3.7 1.3c.4.2.3.9-.1 1l-.4 1.3z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.4H7.4v3.2h2.8V22h3.3z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.2A4.8 4.8 0 1 0 12 16.8 4.8 4.8 0 1 0 12 7.2zm0 7.9a3.1 3.1 0 1 1 0-6.2 3.1 3.1 0 0 1 0 6.2zM17 5.9a1.1 1.1 0 1 0 0 2.2 1.1 1.1 0 0 0 0-2.2zM21.9 8c-.1-1.5-.4-2.9-1.5-4S18 2.4 16.5 2.3C15 2.2 9 2.2 7.5 2.3 6 2.4 4.6 2.7 3.6 3.8S2.2 6.3 2.1 7.8C2 9.3 2 15 2.1 16.5c.1 1.5.4 2.9 1.5 4s2.5 1.4 4 1.5c1.5.1 7.5.1 9 0 1.5-.1 2.9-.4 4-1.5s1.4-2.5 1.5-4c.1-1.5.1-7.5-.2-8.5zm-2.2 10.7c-.3.8-.9 1.4-1.7 1.7-1.2.5-4 .4-5.9.4s-4.8.1-6-.4c-.8-.3-1.4-.9-1.7-1.7-.5-1.2-.4-4-.4-5.9s-.1-4.8.4-6c.3-.8.9-1.4 1.7-1.7C7.3 4.6 10.1 4.7 12 4.7s4.8-.1 6 .4c.8.3 1.4.9 1.7 1.7.5 1.2.4 4 .4 5.9s.1 4.8-.4 6z"/></svg>',
    "in": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.2 8h4.6v14H.2V8zm7.6 0h4.4v1.9h.1c.6-1.1 2.1-2.3 4.3-2.3 4.6 0 5.4 3 5.4 6.9V22h-4.6v-6.6c0-1.6 0-3.6-2.2-3.6s-2.5 1.7-2.5 3.5V22H7.8V8z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 3h3.1l-6.8 7.8L21.8 21h-6.3l-4.9-6.4L5 21H1.9l7.3-8.3L1.5 3H8l4.4 5.9L17.5 3zm-1.1 16.2h1.7L7 4.7H5.2l11.2 14.5z"/></svg>',
}


def expand_tokens(html):
    html = re.sub(r"\[\[cards:([a-z0-9,/-]+)\]\]", lambda m: cards(m.group(1).split(",")), html)
    html = re.sub(r"\[\[postcards:([a-z0-9,/-]+)\]\]", lambda m: '<ul class="posts">' + "".join(post_card(BY_SLUG[s]) for s in m.group(1).split(",")) + "</ul>", html)
    html = re.sub(r"\[\[latestposts:(\d+)\]\]", lambda m: '<ul class="posts">' + "".join(post_card(p) for p in posts_sorted()[: int(m.group(1))]) + "</ul>", html)
    html = re.sub(r"\[\[reviews:(\d+)\]\]", lambda m: reviews_html(int(m.group(1))), html)
    html = re.sub(r"\[\[courts:([a-z0-9,_-]+)\]\]", lambda m: courts_html(m.group(1).split(",")), html)
    html = re.sub(r"\[\[author:([a-z]+)(?::([a-z]+))?\]\]", lambda m: author_box(m.group(1), m.group(2)), html)
    html = html.replace("[[team]]", team_html()).replace("[[nap]]", nap_html()).replace("[[map]]", map_html())
    html = html.replace("[[findus]]", findus_html()).replace("[[hours]]", hours_html()).replace("[[citylist]]", citylist_html())
    html = fix_images(html)
    # remaining [[slug]] tokens are internal links
    def link(m):
        slug = m.group(1)
        if slug not in BY_SLUG:
            warn(f"unknown link target [[{slug}]]")
            return "#"
        return url(slug)
    html = re.sub(r"\[\[([a-z0-9/-]+)\]\]", link, html)
    return html


# ---------------------------------------------------------------- layout pieces

def nav_html():
    def sub(hub_slug, spokes, all_label):
        lis = f'<a class="all" href="{url(hub_slug)}">{all_label}</a>' + "".join(f'<a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a>' for s in spokes)
        return f'<div class="sub">{lis}</div>'
    items = []
    for label, hub_slug, spokes, all_label in firm.NAV:
        if spokes:
            items.append(f'<li class="has-sub"><a href="{url(hub_slug)}" aria-haspopup="true">{label}</a>{sub(hub_slug, spokes, all_label)}</li>')
        else:
            href = url(hub_slug) if hub_slug in BY_SLUG else hub_slug
            items.append(f'<li><a href="{esc(href)}">{label}</a></li>')
    items.append(f'<li class="cta"><a class="btn sm" href="{url("contact-us")}">Contact us</a></li>')
    return f'<nav class="nav" id="nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>'


def header_html():
    logo_src, lw, lh = image_info(firm.LOGO)
    return (
        f'<a class="skip" href="#main">Skip to content</a>'
        f'<div class="topbar"><div class="wrap"><span class="tag"><b class="ff-tag">{esc(firm.TAGLINE)}</b><span class="line"> <span style="color:#7f95b0">·</span> {esc(firm.TAGLINE_LINE)}</span></span>'
        f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a></div></div>'
        f'<header class="hdr"><div class="wrap">'
        f'<a class="brand" href="{url("home")}" aria-label="{esc(firm.NAME)} home"><img src="{logo_src}" alt="" width="{lw}" height="{lh}"><span class="word">Frost Law Group<small>Summerville, SC</small></span></a>'
        f'<a class="phone-hdr" href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
        f'<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" data-navtoggle>Menu</button>'
        f'{nav_html()}</div></header>')


def footer_html():
    logo_src, lw, lh = image_info(firm.LOGO)
    pa = "".join(f'<li><a href="{url(s)}">{esc(l)}</a></li>' for l, s in firm.FOOTER_PRACTICE) + f'<li><a href="{esc(firm.PI_SITE)}" rel="noopener">Personal Injury (summervilleaccidentattorney.com)</a></li>'
    explore = "".join(f'<li><a href="{url(s)}">{esc(l)}</a></li>' for l, s in firm.FOOTER_EXPLORE)
    areas = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in firm.FOOTER_AREAS if s in BY_SLUG)
    soc = "".join(f'<a href="{esc(h)}" rel="noopener" target="_blank" aria-label="{esc(l)}">{ICONS[i]}</a>' for l, h, i in firm.SOCIAL if h)
    find = (f'<li><a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Google Business Profile</a></li>'
            f'<li><a href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Directions</a></li>'
            f'<li><a href="{esc(firm.REVIEW_URL)}" rel="noopener" target="_blank">Leave a Google review</a></li>'
            f'<li><a href="{esc(firm.PREFERRED_SOURCE_URL)}" rel="noopener" target="_blank">Add us as a preferred source on Google</a></li>'
            f'<li><a href="{esc(firm.YELP_URL)}" rel="noopener" target="_blank">Find us on Yelp</a></li>')
    return (
        f'<footer class="foot"><div class="wrap"><div class="grid">'
        f'<div><a class="brand" href="{url("home")}"><img src="{logo_src}" alt="" width="{lw}" height="{lh}"><span class="word">Frost Law Group<small>Summerville, South Carolina</small></span></a>'
        f'<p class="tagline">{esc(firm.TAGLINE)}</p>'
        f'<address><b>{esc(firm.NAME)}</b><br>{firm.STREET}<br>{firm.CITY}, {firm.STATE} {firm.ZIP}<br><a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a></address>'
        f'<p class="small" style="color:#93a4ba;margin:.6rem 0 0">{firm.HOURS_SHORT}</p><div class="soc">{soc}</div></div>'
        f'<div><h3>Practice areas</h3><ul>{pa}</ul><h3 style="margin-top:1.4rem">Find us</h3><ul>{find}</ul></div>'
        f'<div><h3>Explore</h3><ul>{explore}</ul></div>'
        f'<div><h3>Communities we serve</h3><ul>{areas}<li><a href="{url("service-areas")}">All service areas →</a></li></ul></div>'
        f'</div><div class="legal"><p>© 2019–{BUILD_DATE[:4]} {esc(firm.NAME)}. {firm.DISCLAIMER}</p>'
        f'<p><a href="{url("privacy-policy")}">Privacy policy</a> · <a href="{url("terms-of-use")}">Terms of use &amp; legal disclaimer</a> · <a href="{url("accessibility")}">Accessibility</a> · <a href="{url("faq")}">Frequently asked questions</a> · <a href="{url("service-areas")}">Service areas</a></p></div></div></footer>')


def breadcrumb_trail(p):
    trail = [("home", "Home")]
    if p["kind"] == "spoke" and p["hub"]:
        trail.append((p["hub"], BY_SLUG[p["hub"]]["nav_label"]))
    elif p["kind"] == "city":
        trail.append(("service-areas", "Service areas"))
    elif p["kind"] == "post":
        trail.append(("blog", "In the Know"))
    elif p["kind"] == "attorney":
        trail.append(("about-us", "Our team"))
    elif p["hub"]:
        trail.append((p["hub"], BY_SLUG[p["hub"]]["nav_label"]))
    trail.append((p["slug"], p["nav_label"]))
    return trail


def crumbs_html(p):
    if p["kind"] == "home":
        return ""
    trail = breadcrumb_trail(p)
    lis = "".join(f'<li><a href="{url(s)}">{esc(l)}</a></li>' for s, l in trail[:-1]) + f'<li aria-current="page">{esc(trail[-1][1])}</li>'
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'


def hero_html(p):
    cta = p["cta"]
    if cta is None:
        cta = [("contact-us", "Schedule a consultation", "btn"), (f"tel:{firm.PHONE_E164}", firm.PHONE, "btn ghost")]
    actions = ""
    if cta:
        btns = []
        for target, label, cls in cta:
            href = target if target.startswith(("tel:", "http", "mailto:")) else url(target)
            btns.append(f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>')
        actions = f'<div class="actions">{"".join(btns)}</div>'
    kicker = f'<p class="kicker">{p["kicker"]}</p>' if p["kicker"] else ""
    eyebrow = f'<div class="eyebrow">{esc(p["eyebrow"])}</div>' if p["eyebrow"] else ""
    lead = f'<p class="lead">{p["lead"]}</p>' if p["lead"] else ""
    quote = f'<p class="quote">{p["quote"]}</p>' if p["quote"] else ""
    meta = ""
    if p["kind"] == "post":
        a = firm.ATTORNEYS[p["author"]]
        meta = (f'<div class="post-meta"><span class="cat">{esc(p["category"])}</span><span>By <a href="{url(a["slug"])}">{esc(a["name"])}</a></span>'
                f'<span>Published {fmt_date(p["date"])}</span>' + (f'<span>Updated {fmt_date(p["modified"])}</span>' if p["modified"] != p["date"] else "") + "</div>")
    if p.get("hero_style") == "photo" and p["hero_image"]:
        src, w, h = image_info(p["hero_image"])
        if " · " in p["eyebrow"]:  # keep only the first part (the tagline) on small screens
            first, rest = esc(p["eyebrow"]).split(" · ", 1)
            eyebrow = f'<div class="eyebrow">{first}<span class="eb2"> · {rest}</span></div>'
        text = f'<div>{kicker}{eyebrow}<h1>{p["h1"]}</h1>{lead}{actions}</div>'
        band_ = f'<div class="quote-band"><div class="wrap">{p["quote"]}</div></div>' if p["quote"] else ""
        img_html = f'<img class="bg" src="{src}" alt="{esc(p["hero_caption"] or "")}" width="{w}" height="{h}" fetchpriority="high">'
        if p.get("hero_image_wide"):  # wide crop with room for the text beside the subjects on large screens
            wsrc, _, _ = image_info(p["hero_image_wide"])
            img_html = f'<picture><source media="(min-width:1101px)" srcset="{wsrc}">{img_html}</picture>'
        return (f'<section class="hero photo"><div class="media">{img_html}<div class="shade"></div></div>'
                f'<div class="wrap">{text}</div></section>{band_}')
    text = f'<div>{crumbs_html(p)}{kicker}{eyebrow}<h1>{p["h1"]}</h1>{meta}{lead}{actions}{quote}</div>'
    if p["hero_image"]:
        src, w, h = image_info(p["hero_image"])
        cap = f'<figcaption>{esc(p["hero_caption"])}</figcaption>' if p["hero_caption"] else ""
        fcls = ' class="portrait"' if h > w * 1.3 else ""  # tall headshots get a 4:5 frame instead of the 4:3 crop
        fig = f'<figure{fcls}><img src="{src}" alt="{esc(p["hero_caption"] or p["h1"])}" width="{w}" height="{h}" fetchpriority="high">{cap}</figure>'
        return f'<section class="hero"><div class="wrap">{text}{fig}</div></section>'
    return f'<section class="hero plain"><div class="wrap">{text}</div></section>'


def faq_html(faqs):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs)
    return f'<h2 id="faq">Questions people ask</h2><div class="faq">{items}</div>'


def related_html(p):
    rel = [s for s in p["related"] if s in BY_SLUG]
    if not rel:
        return ""
    return '<h2>Related pages</h2><ul class="cards">' + "".join(card(BY_SLUG[s], new=False) for s in rel) + "</ul>"


def aside_html(p):
    cards_ = []
    cards_.append(f'<div class="acard navy"><h3>Talk to an attorney</h3><a class="big" href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
                  f'<p style="margin:0 0 .8rem;font-size:.95rem">{firm.ASIDE_BLURB}</p><a class="btn light sm" href="{url("contact-us")}">Send a message</a>'
                  f'<p class="hours">{firm.HOURS_SHORT}</p></div>')
    if p["kind"] in ("hub", "spoke"):
        hub = p["slug"] if p["kind"] == "hub" else p["hub"]
        spokes = [s for s in firm.HUB_SPOKES.get(hub, []) if s in BY_SLUG]
        lis = f'<li class="{"here" if p["slug"] == hub else ""}"><a href="{url(hub)}">{esc(BY_SLUG[hub]["nav_label"])} overview</a></li>'
        lis += "".join(f'<li class="{"here" if s == p["slug"] else ""}"><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in spokes)
        cards_.append(f'<div class="acard"><h3>{esc(BY_SLUG[hub]["section_label"] or BY_SLUG[hub]["nav_label"])}</h3><ul>{lis}</ul></div>')
        key = firm.HUB_ATTORNEY.get(hub)
        if key:
            a = firm.ATTORNEYS[key]
            cards_.append(f'<div class="acard"><div class="person">{img_tag(a["headshot"], a["name"])}<div><b>{esc(a["name"])}</b><small>{esc(a["byline"])}</small></div></div>'
                          f'<p style="font-size:.93rem;margin:.8rem 0 0">{a["aside"]}</p><p style="margin:.6rem 0 0;font-size:.93rem"><a href="{url(a["slug"])}">Read {esc(a["first"])}\'s background →</a></p></div>')
    elif p["kind"] == "city":
        same = [c for c in PAGES if c["kind"] == "city" and c["county"] == p["county"] and c["slug"] != p["slug"]]
        lis = "".join(f'<li><a href="{url(c["slug"])}">{esc(c["nav_label"])}</a></li>' for c in sorted(same, key=lambda x: x["nav_label"])[:9])
        cards_.append(f'<div class="acard"><h3>Also serving {esc(p["county"])}</h3><ul>{lis}<li><a href="{url("service-areas")}">All service areas →</a></li></ul></div>')
        lis2 = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in ("estate-planning-attorney", "probate", "criminal-defense"))
        cards_.append(f'<div class="acard"><h3>What we handle</h3><ul>{lis2}<li><a href="{esc(firm.PI_SITE)}" rel="noopener">Personal injury (separate site)</a></li></ul></div>')
    elif p["kind"] == "post":
        a = firm.ATTORNEYS[p["author"]]
        cards_.append(f'<div class="acard"><div class="person">{img_tag(a["headshot"], a["name"])}<div><b>{esc(a["name"])}</b><small>{esc(a["byline"])}</small></div></div><p style="font-size:.93rem;margin:.8rem 0 0">{a["aside"]}</p></div>')
        others = [q for q in posts_sorted() if q["slug"] != p["slug"]][:4]
        lis = "".join(f'<li><a href="{url(q["slug"])}">{esc(q["h1"])}</a></li>' for q in others)
        cards_.append(f'<div class="acard"><h3>More from In the Know</h3><ul>{lis}<li><a href="{url("blog")}">All articles →</a></li></ul></div>')
    elif p["kind"] == "attorney":
        other = "tara" if p["author"] == "jack" else "jack"
        o = firm.ATTORNEYS[other]
        c = firm.TEAM["cassie"]
        cards_.append(f'<div class="acard"><h3>Also on the team</h3><div class="person">{img_tag(o["headshot"], o["name"])}<div><b><a href="{url(o["slug"])}" style="text-decoration:none">{esc(o["name"])}</a></b><small>{esc(o["byline"])}</small></div></div>'
                      f'<div class="person" style="margin-top:.9rem">{img_tag(c["photo"], c["alt"])}<div><b><a href="{url(c["slug"])}" style="text-decoration:none">{esc(c["name"])}</a></b><small>{esc(c["role"])}</small></div></div></div>')
    else:
        lis = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in ("estate-planning-attorney", "probate", "criminal-defense", "about-us", "reviews", "service-areas"))
        cards_.append(f'<div class="acard"><h3>Explore</h3><ul>{lis}</ul></div>')
    return '<aside class="aside">' + "".join(cards_) + "</aside>"


def body_html(p):
    inner = p["body"]
    if p["kind"] == "post":
        inner += f"[[author:{p['author']}{':' + p['reviewer'] if p['reviewer'] else ''}]]"
    if p["faqs"]:
        inner += faq_html(p["faqs"])
    if p["sources"]:
        from content.base import sources as _sources
        inner += _sources(p["sources"])
    inner += related_html(p)
    if p["layout"] == "raw":
        return f'<main id="main">{inner}</main>'
    if p["layout"] == "one":
        return f'<main id="main"><div class="wrap layout single"><div class="main prose" style="max-width:none">{inner}</div></div></main>'
    return f'<main id="main"><div class="wrap layout"><div class="main prose">{inner}</div>{aside_html(p)}</div></main>'


# ---------------------------------------------------------------- structured data

def firm_ld():
    hours = [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in firm.HOURS_LD]
    d = {
        "@type": ["LegalService", "Attorney"], "@id": ORIGIN + "/#firm", "name": firm.NAME, "alternateName": "Frost Law Group",
        "slogan": firm.TAGLINE, "url": ORIGIN + "/", "telephone": firm.PHONE_E164, "image": ORIGIN + "/assets/img/og.jpg",
        "logo": ORIGIN + "/assets/img/" + firm.LOGO, "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": firm.STREET, "addressLocality": firm.CITY, "addressRegion": firm.STATE, "postalCode": firm.ZIP, "addressCountry": "US"},
        "openingHoursSpecification": hours, "sameAs": [s for s in firm.SAME_AS if s],
        "areaServed": [{"@type": "City", "name": n} for n in firm.AREA_SERVED],
        "founder": [{"@id": abs_url(firm.ATTORNEYS[k]["slug"]) + "#person"} for k in ("jack", "tara")],
        "knowsAbout": ["Estate planning", "Wills and trusts", "Probate and estate administration", "Guardianship and conservatorship", "Criminal defense", "Personal injury"],
        "hasMap": firm.GBP_URL,
        "employee": [{"@id": abs_url(firm.TEAM["cassie"]["slug"]) + "#person"}],
    }
    if firm.GEO:
        d["geo"] = {"@type": "GeoCoordinates", "latitude": firm.GEO[0], "longitude": firm.GEO[1]}
    if firm.RATING:
        d["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": firm.RATING[0], "reviewCount": firm.RATING[1]}
    return d


def person_ld(key):
    a = firm.ATTORNEYS[key]
    return {"@type": "Person", "@id": abs_url(a["slug"]) + "#person", "name": a["name"], "givenName": a["first"], "familyName": "Frost",
            "jobTitle": "Attorney at Law", "url": abs_url(a["slug"]), "image": ORIGIN + "/assets/img/" + a["headshot"],
            "worksFor": {"@id": ORIGIN + "/#firm"}, "alumniOf": [{"@type": "CollegeOrUniversity", "name": s} for s in a["alumni"]],
            "knowsAbout": a["knows"], "sameAs": [s for s in a["same_as"] if s], "description": a["ld_description"],
            "email": a.get("email"), "telephone": firm.PHONE_E164,
            "identifier": {"@type": "PropertyValue", "propertyID": "South Carolina Bar Number", "value": a.get("bar_number")},
            "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Admitted to the South Carolina Bar", "dateCreated": a.get("admitted_iso"),
                              "recognizedBy": {"@type": "Organization", "name": "Supreme Court of South Carolina"}}}


def page_ld(p):
    graph = []
    trail = breadcrumb_trail(p) if p["kind"] != "home" else [("home", "Home")]
    graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": l, "item": abs_url(s)} for i, (s, l) in enumerate(trail)]})
    wp = {"@type": "WebPage", "@id": abs_url(p["slug"]), "url": abs_url(p["slug"]), "name": p["title"], "description": p["description"],
          "isPartOf": {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": firm.NAME, "publisher": {"@id": ORIGIN + "/#firm"}},
          "about": {"@id": ORIGIN + "/#firm"}, "inLanguage": "en-US", "dateModified": p["modified"] or BUILD_DATE}
    graph.append(wp)
    if p["kind"] == "home" or p["slug"] == "contact-us":
        graph.append(firm_ld())
        graph.append(person_ld("jack"))
        graph.append(person_ld("tara"))
    if p["kind"] in ("hub", "spoke"):
        graph.append({"@type": "Service", "name": p["h1"], "serviceType": p["nav_label"], "provider": {"@id": ORIGIN + "/#firm"},
                      "areaServed": [{"@type": "City", "name": n} for n in firm.AREA_SERVED[:8]], "url": abs_url(p["slug"]), "description": p["description"]})
    if p["kind"] == "city":
        graph.append({"@type": "Service", "name": p["h1"], "provider": {"@id": ORIGIN + "/#firm"}, "areaServed": {"@type": "City", "name": p["nav_label"], "containedInPlace": {"@type": "AdministrativeArea", "name": p["county"]}}, "url": abs_url(p["slug"])})
    faqs = p["faqs"] or p.get("_faq_schema") or []
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]})
    if p.get("_person"):  # staff bio pages
        sp = p["_person"]
        graph.append({"@type": "Person", "@id": abs_url(p["slug"]) + "#person", "name": sp["name"], "alternateName": sp["alternateName"],
                      "givenName": sp["givenName"], "familyName": sp["familyName"], "jobTitle": sp["jobTitle"], "url": abs_url(p["slug"]),
                      "image": ORIGIN + "/assets/img/" + sp["photo"], "worksFor": {"@id": ORIGIN + "/#firm"}, "description": sp["description"],
                      "telephone": firm.PHONE_E164})
    if p["kind"] == "post":
        a = firm.ATTORNEYS[p["author"]]
        graph.append({"@type": "BlogPosting", "headline": p["h1"], "description": p["description"], "url": abs_url(p["slug"]), "mainEntityOfPage": abs_url(p["slug"]),
                      "datePublished": p["date"], "dateModified": p["modified"], "author": {"@id": abs_url(a["slug"]) + "#person"},
                      "publisher": {"@id": ORIGIN + "/#firm"}, "articleSection": p["category"], "inLanguage": "en-US", "image": ORIGIN + "/assets/img/og.jpg"})
    if p["kind"] == "attorney":
        graph.append(person_ld(p["author"]))
    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------- documents

INLINE_JS = r"""
(function(){
  var t=document.querySelector('[data-navtoggle]'),n=document.getElementById('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');t.textContent=o?'Close':'Menu';});}
  document.addEventListener('click',function(e){var b=e.target.closest('[data-loadmap]');if(!b)return;var m=b.closest('.map');
    if(window.__PREVIEW__){b.replaceWith(Object.assign(document.createElement('p'),{textContent:'The interactive Google Map loads here on the live site.'}));return;}
    var f=document.createElement('iframe');f.src=m.getAttribute('data-embed');f.title='Map to Frost Law Group, 128 Linwood Lane, Summerville';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.allowFullscreen=true;m.appendChild(f);});
  var f=document.querySelector('form[data-contact]');
  if(f){f.addEventListener('submit',function(e){var hp=f.querySelector('[name=_gotcha]');if(hp&&hp.value){e.preventDefault();return;}var t=f.querySelector('[name=topic]'),s=f.querySelector('[name=_subject]');if(t&&s){s.value='Website inquiry: '+t.value;}
    if(window.__PREVIEW__){e.preventDefault();alert('On the live site this sends your message to the firm and lands on the thank-you page.');return;}
    if(!window.fetch||!window.FormData){return;}
    e.preventDefault();var btn=f.querySelector('button[type=submit]'),msg=f.querySelector('[data-formmsg]');if(btn){btn.disabled=true;btn.textContent='Sending…';}
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}}).then(function(r){return r.ok?r.json().catch(function(){return {ok:true};}):Promise.reject(r);}).then(function(){window.location.href=f.getAttribute('data-thanks')||'/thank-you/';}).catch(function(){
      if(btn){btn.disabled=false;btn.textContent='Send message';}if(msg){msg.hidden=false;}});});}
})();
"""


def head_html(p):
    og_type = "article" if p["kind"] == "post" else "website"
    robots = '<meta name="robots" content="noindex,follow">' if p["noindex"] else '<meta name="robots" content="index,follow,max-image-preview:large">'
    ld = json.dumps(page_ld(p), ensure_ascii=False, separators=(",", ":"))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(p["title"])}</title><meta name="description" content="{esc(p["description"])}">{robots}'
        f'<link rel="canonical" href="{abs_url(p["slug"])}">'
        f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(firm.NAME)}"><meta property="og:title" content="{esc(p["title"])}">'
        f'<meta property="og:description" content="{esc(p["description"])}"><meta property="og:url" content="{abs_url(p["slug"])}"><meta property="og:image" content="{ORIGIN}/assets/img/og.jpg">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="geo.region" content="US-SC"><meta name="geo.placename" content="{firm.CITY}">'
        '<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">'
        '<link rel="preload" href="/assets/fonts/cormorant-garamond-300-700.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="preload" href="/assets/fonts/inter-300-700.woff2" as="font" type="font/woff2" crossorigin>'
        f'<link rel="stylesheet" href="{CSS_HREF}">'
        f'<script type="application/ld+json">{ld}</script>'
        '</head><body>')


def render_prod(p):
    doc = head_html(p) + header_html() + hero_html(p) + body_html(p) + footer_html() + f"<script>{INLINE_JS}</script></body></html>"
    return expand_tokens(doc)


def write_prod():
    global CSS_HREF
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets", "img"))
    css_src = os.path.join(ASSETS, "site.css")
    css_name = f"site.{file_hash(css_src)}.css"
    CSS_HREF = f"/assets/{css_name}"
    shutil.copy(css_src, os.path.join(OUT, "assets", css_name))
    shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(OUT, "assets", "fonts"))
    # pages
    for p in PAGES:
        html = render_prod(p)
        check_page(p, html)
        d = OUT if p["slug"] == "home" else os.path.join(OUT, p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
    # images (optimized copies) + placeholders
    if os.path.isdir(IMG_DIR):
        for name in os.listdir(IMG_DIR):
            src = os.path.join(IMG_DIR, name)
            dst = os.path.join(OUT, "assets", "img", name)
            if name.lower().endswith((".jpg", ".jpeg", ".png")):
                im = Image.open(src)
                mx = 1600
                if im.width > mx:
                    im = im.resize((mx, round(im.height * mx / im.width)), Image.LANCZOS)
                if name.lower().endswith(".png"):
                    im.save(dst, "PNG", optimize=True)
                else:
                    im.convert("RGB").save(dst, "JPEG", quality=82, optimize=True, progressive=True)
            else:
                shutil.copy(src, dst)
    for name, svg in _PLACEHOLDERS.items():
        open(os.path.join(OUT, "assets", "img", "placeholder-" + os.path.splitext(name)[0] + ".svg"), "w", encoding="utf-8").write(svg)
    write_favicons()
    write_og()
    # sitemap, robots, htaccess, llms, 404
    urls = []
    for p in PAGES:
        if p["noindex"]:
            continue
        urls.append(f"<url><loc>{abs_url(p['slug'])}</loc><lastmod>{p['modified'] or BUILD_DATE}</lastmod><changefreq>{p['changefreq']}</changefreq><priority>{p['priority']:.1f}</priority></url>")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(urls) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8").write(htaccess())
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(llms_txt())
    write_vercel_json()
    p404 = dict(BY_SLUG["home"], slug="404", title="Page not found | Frost Law Group", description="That page has moved.", h1="We couldn't find that page", kind="page", layout="one", noindex=True,
                eyebrow="Page not found", lead="The address may have changed when we rebuilt the site. The links below will get you where you were headed.", kicker="", quote="", hero_image=None, cta=None, faqs=[], related=[], sources=[],
                body='<p>Try one of these: <a href="[[estate-planning-attorney]]">Estate planning</a>, <a href="[[probate]]">Probate</a>, <a href="[[criminal-defense]]">Criminal defense</a>, <a href="[[contact-us]]">Contact us</a>, or call <a href="tel:' + firm.PHONE_E164 + '">' + firm.PHONE + "</a>.</p>")
    html = expand_tokens(head_html(p404).replace(f'<link rel="canonical" href="{abs_url("404")}">', "") + header_html() + hero_html(p404) + body_html(p404) + footer_html() + f"<script>{INLINE_JS}</script></body></html>")
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(html)


def htaccess():
    lines = ["# Frost Law Group — canonical host, HTTPS, trailing slashes, and the redirect map from the search audit",
             "Options -Indexes", "ErrorDocument 404 /404.html", "", "<IfModule mod_rewrite.c>", "RewriteEngine On",
             "# https + non-www (one address for every page)",
             "RewriteCond %{HTTPS} off [OR]", "RewriteCond %{HTTP_HOST} ^www\\. [NC]",
             "RewriteCond %{HTTP_HOST} ^(?:www\\.)?(.+)$ [NC]", "RewriteRule ^ https://%1%{REQUEST_URI} [R=301,L,NE]",
             "# strip the cache-plugin parameter Google indexed", "RewriteCond %{QUERY_STRING} (^|&)swcfpc= [NC]", "RewriteRule ^(.*)$ /$1? [R=301,L]",
             "# old addresses -> new pages"]
    for old, new in firm.REDIRECTS:
        lines.append(f"RewriteRule ^{old}$ {new} [R=301,L]")
    lines += ["# add a trailing slash to directory-style URLs", "RewriteCond %{REQUEST_FILENAME} !-f", "RewriteCond %{REQUEST_URI} !/$", "RewriteCond %{REQUEST_URI} !\\.[a-zA-Z0-9]{2,5}$",
              "RewriteRule ^(.*)$ /$1/ [R=301,L]", "</IfModule>", "",
              "<IfModule mod_headers.c>", 'Header set X-Content-Type-Options "nosniff"', 'Header set Referrer-Policy "strict-origin-when-cross-origin"',
              '<FilesMatch "\\.(woff2|css|svg|jpg|png)$">', 'Header set Cache-Control "public, max-age=31536000, immutable"', "</FilesMatch>", "</IfModule>", "",
              "<IfModule mod_deflate.c>", "AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml", "</IfModule>", ""]
    return "\n".join(lines)


def write_vercel_json():
    """Vercel equivalent of the .htaccess rules: serve website/, keep trailing slashes, redirect old addresses, cache assets."""
    redirects = []
    for old, new in firm.REDIRECTS:
        base = old.rstrip("/?").rstrip("?")
        if base.endswith(".*"):
            src = "/" + base[:-2].rstrip("/") + "/:path*"
            redirects.append({"source": src, "destination": new, "permanent": True})
        else:
            redirects.append({"source": "/" + base, "destination": new, "permanent": True})
            redirects.append({"source": "/" + base + "/", "destination": new, "permanent": True})
    cfg = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "buildCommand": None,
        "installCommand": None,
        "outputDirectory": "website",
        "trailingSlash": True,
        "redirects": redirects,
        "headers": [
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                                             {"key": "X-Frame-Options", "value": "SAMEORIGIN"}, {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}]},
        ],
    }
    open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8").write(json.dumps(cfg, indent=2) + "\n")


def llms_txt():
    lines = [f"# {firm.NAME}", "", f"> {firm.LLMS_SUMMARY}", "", f"- Address: {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}", f"- Phone: {firm.PHONE}", f"- Hours: {firm.HOURS_SHORT}",
             f"- Attorneys: {firm.ATTORNEYS['jack']['name']} (criminal defense; former Summerville police officer and Charleston County Sheriff's Office detective) and {firm.ATTORNEYS['tara']['name']} (probate and estate planning; former Dorchester County magistrate and associate probate judge)",
             f"- Personal injury matters: {firm.PI_SITE}", f"- Google Business Profile: {firm.GBP_URL}", f"- Yelp: {firm.YELP_URL}", "", "## Pages", ""]
    for p in PAGES:
        if not p["noindex"]:
            lines.append(f"- [{p['h1']}]({abs_url(p['slug'])}): {p['description']}")
    return "\n".join(lines) + "\n"


def write_favicons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f2a4a"/>'
           '<text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="40" fill="#fff">F</text></svg>')
    open(os.path.join(OUT, "assets", "img", "favicon.svg"), "w", encoding="utf-8").write(svg)
    im = Image.new("RGB", (180, 180), "#0f2a4a")
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 120)
    except Exception:
        f = ImageFont.load_default()
    d.text((90, 92), "F", fill="#ffffff", font=f, anchor="mm")
    im.save(os.path.join(OUT, "assets", "img", "apple-touch-icon.png"))


def write_og():
    """1200x630 share image: the couple photo if present, otherwise a navy card with the wordmark."""
    path = os.path.join(OUT, "assets", "img", "og.jpg")
    src = os.path.join(IMG_DIR, firm.OG_SOURCE)
    W, H = 1200, 630
    if os.path.exists(src):
        im = Image.open(src).convert("RGB")
        scale = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        left, top = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((left, top, left + W, top + H))
    else:
        im = Image.new("RGB", (W, H), "#0f2a4a")
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, H - 170, W, H], fill=(15, 42, 74, 235))
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 54)
        f2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 28)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    d.text((48, H - 140), "Frost Law Group, LLC", fill="#ffffff", font=f1)
    d.text((48, H - 70), f"{firm.TAGLINE}  Estate planning · Probate · Criminal defense · Summerville, SC", fill="#cfdcea", font=f2)
    im.save(path, "JPEG", quality=85, optimize=True)


# ---------------------------------------------------------------- preview (single file)

def write_preview(out_path):
    css = open(os.path.join(ASSETS, "site.css"), encoding="utf-8").read()
    css = re.sub(r"@font-face\{[^}]*\}", "", css)
    tpl = []
    for p in PAGES:
        inner = expand_tokens(hero_html(p) + body_html(p))
        tpl.append(f'<template data-slug="{p["slug"]}" data-title="{esc(p["title"])}">{inner}</template>')
    groups = [("Core pages", [p for p in PAGES if p["kind"] in ("home", "page", "attorney")]),
              ("Estate planning", [p for p in PAGES if p["slug"] == "estate-planning-attorney" or p.get("hub") == "estate-planning-attorney"]),
              ("Probate", [p for p in PAGES if p["slug"] == "probate" or p.get("hub") == "probate"]),
              ("Criminal defense", [p for p in PAGES if p["slug"] == "criminal-defense" or p.get("hub") == "criminal-defense"]),
              ("Service areas", [p for p in PAGES if p["kind"] == "city"]),
              ("Blog", [p for p in PAGES if p["kind"] == "post"])]
    drawer = ""
    for label, items in groups:
        drawer += f"<h3>{label} ({len(items)})</h3><ul>" + "".join(f'<li><a href="{url(p["slug"])}">{esc(p["h1"])}</a></li>' for p in items) + "</ul>"
    header = expand_tokens(header_html())
    footer = expand_tokens(footer_html())
    js = r"""
window.__PREVIEW__=true;
(function(){
  var T={};document.querySelectorAll('template[data-slug]').forEach(function(t){T[t.dataset.slug]=t;});
  var app=document.getElementById('app'),drawer=document.getElementById('pv-drawer');
  function go(){var s=location.hash.replace(/^#\/?/,'').replace(/\/$/,'')||'home';var t=T[s]||T['home'];app.innerHTML='';app.appendChild(t.content.cloneNode(true));
    document.title=t.dataset.title;window.scrollTo(0,0);var n=document.getElementById('nav');if(n){n.classList.remove('open');}var b=document.querySelector('[data-navtoggle]');if(b){b.textContent='Menu';b.setAttribute('aria-expanded','false');}drawer.classList.remove('open');}
  window.addEventListener('hashchange',go);go();
  document.getElementById('pv-open').addEventListener('click',function(){drawer.classList.add('open');});
  document.getElementById('pv-close').addEventListener('click',function(){drawer.classList.remove('open');});
})();
"""
    doc = (f'<title>Frost Law Group Site Preview</title><style>{css}</style>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&family=Inter:ital,wght@0,300..700;1,400&family=Proza+Libre:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">'
           f'<div class="pv-note">Preview of the rebuilt frostlawgroupsc.com — {len(PAGES)} pages. Use the menu, footer links or the “All pages” button to move around. Maps and the contact form activate on the live site.</div>'
           f'{header}<div id="app"></div>{footer}'
           f'<div class="pv-bar"><button type="button" id="pv-open">All {len(PAGES)} pages</button></div>'
           f'<div class="pv-drawer" id="pv-drawer"><button class="close" type="button" id="pv-close">Close</button><h2>Every page in the rebuild</h2><p class="small">Grouped the way the site is wired: hubs and their spokes, one page per service area, and the blog.</p>{drawer}</div>'
           + "".join(tpl) + f"<script>{INLINE_JS}</script><script>{js}</script>")
    open(out_path, "w", encoding="utf-8").write(doc)
    return len(doc)


# ---------------------------------------------------------------- checks

DUI_RE = re.compile(r"\bDUI\b|\bDUAC\b|driving under the influence|drunk driving", re.I)


def check_page(p, html):
    if len(p["title"]) > (90 if p["kind"] == "home" else 70):
        warn(f"{p['slug']}: title {len(p['title'])} chars")
    if not (60 <= len(p["description"]) <= 160):
        warn(f"{p['slug']}: description {len(p['description'])} chars")
    if html.count("<h1") != 1:
        warn(f"{p['slug']}: {html.count('<h1')} h1 tags")
    if "[[" in html:
        warn(f"{p['slug']}: unresolved token near {html[html.find('[['):html.find('[[') + 40]!r}")
    if p["kind"] == "home" and DUI_RE.search(html):
        m = DUI_RE.search(html)
        warn(f"HOME PAGE MENTIONS DUI: ...{html[max(0, m.start() - 60):m.end() + 60]!r}")
    words = len(re.sub(r"<[^>]+>", " ", html.split('<main', 1)[1].split("</main>", 1)[0]).split()) if "<main" in html else 0
    p["_words"] = words


def check_global():
    titles, descs = {}, {}
    for p in PAGES:
        titles.setdefault(p["title"], []).append(p["slug"])
        descs.setdefault(p["description"], []).append(p["slug"])
    for t, s in titles.items():
        if len(s) > 1:
            warn(f"duplicate title {t!r}: {s}")
    for t, s in descs.items():
        if len(s) > 1:
            warn(f"duplicate description: {s}")
    for p in PAGES:
        for s in p["related"]:
            if s not in BY_SLUG:
                warn(f"{p['slug']}: related target {s} missing")
        if p["hub"] and p["hub"] not in BY_SLUG:
            warn(f"{p['slug']}: hub {p['hub']} missing")


def main():
    global MODE
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="write a single-file preview to this path instead of website/")
    args = ap.parse_args()
    check_global()
    if args.preview:
        MODE = "preview"
        for p in PAGES:  # run per-page checks against a rendered document too
            check_page(p, hero_html(p) + expand_tokens(body_html(p)))
        n = write_preview(args.preview)
        print(f"preview: {args.preview} ({n/1e6:.2f} MB, {len(PAGES)} pages)")
    else:
        MODE = "prod"
        write_prod()
        total = sum(len(open(os.path.join(dp, f), encoding="utf-8").read()) for dp, _, fs in os.walk(OUT) for f in fs if f.endswith(".html"))
        print(f"website/: {len(PAGES)} pages, {total/1e6:.2f} MB of HTML")
    kinds = {}
    for p in PAGES:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    print("pages by kind:", kinds)
    short = sorted(((p.get("_words", 0), p["slug"]) for p in PAGES))[:6]
    print("shortest pages (words in main):", short)
    for w in WARNINGS:
        print("WARN:", w)
    if any("HOME PAGE MENTIONS DUI" in w for w in WARNINGS):
        sys.exit(1)


if __name__ == "__main__":
    main()
