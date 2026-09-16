"""Verified local data (courts, routes, places, statutes) loaded from local_data.json.

local_data.json is assembled from official sources (county and court websites, scstatehouse.gov,
OpenStreetMap routing). Helpers here render it; every helper degrades gracefully if a key is missing.
"""
import json
import os

from .base import esc, ext

_PATH = os.path.join(os.path.dirname(__file__), "local_data.json")
DATA = json.load(open(_PATH, encoding="utf-8")) if os.path.exists(_PATH) else {}
ROUTES = DATA.get("routes", {})
PLACES = DATA.get("places", {})
STATUTES = DATA.get("statutes", {})
LINKS = DATA.get("links", {})
OFFICE = DATA.get("office", {})


def cite(key, text=None):
    """Link to a verified statute/official source by key; plain text if unknown."""
    s = STATUTES.get(key)
    if not s:
        return esc(text or key)
    return ext(s["url"], esc(text or s["label"]))


def link(key, text=None, nofollow=False):
    l = LINKS.get(key)
    if not l:
        return esc(text or key)
    return ext(l["url"], esc(text or l["label"]), nofollow)


def route(key):
    return ROUTES.get(key)


def directions_cards(keys):
    """Direction cards for the contact page and city pages."""
    out = []
    for k in keys:
        r = ROUTES.get(k)
        if not r:
            continue
        dist = f'<span class="dist">{esc(r["miles"])} mi · about {esc(r["minutes"])} min</span>' if r.get("miles") else ""
        out.append(f'<article><h3>From {esc(r["from"])}</h3><p>{r["text"]}</p>{dist}</article>')
    if not out:
        return ""
    return '<div class="directions">' + "".join(out) + "</div>"


def office_roads_sentence():
    return OFFICE.get("roads_sentence", "")
