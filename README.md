# Frost Law Group — Search Audit & Topical-Authority Plan

Deliverables for Frost Law Group, LLC (Summerville, SC), covering both websites:

- `frostlawgroupsc.com` — estate planning, probate, criminal defense
- `summervilleaccidentattorney.com` — personal injury

## Deliverables

| File | What it is |
|---|---|
| `report/frost-law-group-search-audit.html` | The audit as a single self-contained web page (fonts and charts embedded; open in any browser) |
| `report/frost-law-group-search-audit.pdf` | The same audit rendered to Letter-size PDF |

Every number in the audit comes from the two Google Search Console properties. The report
contains: an executive summary, a plain-English explainer of how search works, a deep dive on
each site, the cross-site cannibalization evidence and the two-site decision, the topical-authority
plan (hub-and-spoke maps), high-intent and long-tail keyword targets, the fan-out playbook, the
channel playbook (YouTube, LinkedIn, Instagram, Google Business Profile, Yelp), a 90-day plan, a
measurement plan, and appendices (data tables, redirect map, proposed title tags, glossary).

## Data

`data/` holds the Search Console exports the report is built from:

- `frost_daily.csv`, `frost_nonbrand_daily.csv`, `sva_daily.csv` — daily clicks/impressions/position
- `frost_pages.csv`, `sva_pages.csv` — page-level performance
- `frost_queries_*.json`, `frost_query_page_*.json`, `sva_query_page_*.json` — query and query×page rows
- `devices.json`, `aggregates.json` — device splits and the topic/city/position groupings used in the charts

Windows: main site Jun 22 – Sep 8, 2026; injury site Jul 20 – Sep 8, 2026.

## Rebuilding

```bash
python3 build/build_report.py          # writes report/frost-law-group-search-audit.html
node build/render.js                   # writes report/frost-law-group-search-audit.pdf (needs Playwright + Chromium)
```

`build/charts.py` and `build/diagrams.py` draw the inline SVG charts and diagrams; `build/fonts/`
holds the embedded Newsreader and Public Sans subsets.
