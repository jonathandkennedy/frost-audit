# Frost Law Group — Search Audit & Topical-Authority Plan

Deliverables for Frost Law Group, LLC (Summerville, SC), covering both websites:

- `frostlawgroupsc.com` — estate planning, probate, criminal defense
- `summervilleaccidentattorney.com` — personal injury

## Deliverables

| File | What it is |
|---|---|
| `report/frost-law-group-search-audit.html` | The audit as a single self-contained web page (fonts and charts embedded; open in any browser) |
| `report/frost-law-group-search-audit.pdf` | The same audit rendered to Letter-size PDF with Legal Leads Group branding (full-bleed cover, logo header, page numbers, closing page) |

Search Console figures are the firm's own data; market figures (volumes, cost-per-click, competitor traffic, links, map-pack ranks) are third-party estimates and are presented without vendor attribution. The report
contains: an executive summary, a plain-English explainer of how search works, a deep dive on
each site, the cross-site cannibalization evidence and the two-site decision, the topical-authority
plan (hub-and-spoke maps), high-intent and long-tail keyword targets, the fan-out playbook, the
channel playbook (YouTube, LinkedIn, Instagram, Google Business Profile, Yelp), a 90-day plan, a
measurement plan, and appendices (data tables, redirect map, proposed title tags, glossary).

## Website rebuild

`website/` is a deployable static rebuild of frostlawgroupsc.com (78 pages) generated from `site/`:

```bash
python3 site/build_local_data.py       # optional: regenerate site/content/local_data.json from facts.json (uses OSRM for routes)
python3 site/build_site.py             # writes website/ (production build with sitemap, robots.txt, .htaccess, llms.txt)
python3 site/build_site.py --preview out.html   # single-file clickable preview (used for the shared artifact)
```

Content lives in `site/content/` (`core.py`, `estate.py`, `probate.py`, `criminal.py`, `cities.py`, `posts.py`, `firm.py` for name/address/links, `meta.py` for titles and descriptions). `website/BUILD-NOTES.md` explains the design decisions, the recommendations (blog authorship, the "Frost First" tagline, the no-DUI home page) and the pre-launch checklist.

## Data

`data/` holds the Search Console exports the report is built from, and `data/market/` holds the market-data exports (keyword volumes and ad prices, map-pack snapshots, competitor visibility and domain/link benchmarks, competitor ranked keywords):

- `frost_daily.csv`, `frost_nonbrand_daily.csv`, `sva_daily.csv` — daily clicks/impressions/position
- `frost_pages.csv`, `sva_pages.csv` — page-level performance
- `frost_queries_*.json`, `frost_query_page_*.json`, `sva_query_page_*.json` — query and query×page rows
- `devices.json`, `aggregates.json` — device splits and the topic/city/position groupings used in the charts

Windows: main site Jun 22 – Sep 8, 2026; injury site Jul 20 – Sep 8, 2026.

## Rebuilding

```bash
python3 build/build_report.py          # writes report/frost-law-group-search-audit.html
node build/render.js                   # writes report/frost-law-group-search-audit.pdf (needs Playwright + Chromium, and pymupdf for the merge)
```

`build/render.js` renders the PDF in two passes (a full-bleed cover, then the body with the branded
header and footer) and `build/merge_pdf.py` joins them. `build/charts.py` and `build/diagrams.py`
draw the inline SVG charts and diagrams; `build/fonts/` holds the embedded Public Sans subset.

## Branding

`build/brand/` holds the Legal Leads Group assets used on the cover, page header and closing page
(logo, logo tile, planet, rocket and moon artwork), taken from the LLG brand deck. The report's
purple palette (`--brand`, `--brand-bright`, `--brand-lav`, `--space` in `build/build_report.py`)
follows the same deck; chart colors stay on the accessible blue/orange/aqua set so the data reads clearly.
