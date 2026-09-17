# frostlawgroupsc.com rebuild — build notes and recommendations

`website/` is a complete, deployable rebuild of frostlawgroupsc.com: 77 static pages, one stylesheet, self-hosted fonts, a sitemap, robots.txt, an `.htaccess` with the redirect map from the search audit (for Apache hosts), and `llms.txt`; `vercel.json` at the repository root carries the same rules for Vercel. The folder is generated from `site/` (`python3 site/build_site.py`), so copy changes go in the content files, not in the output. These notes stay in `site/` and are not published with the site.

## What changed versus the current site

| Audit finding | What the rebuild does |
|---|---|
| One title tag on every page | Every page has its own title (≤ 70 characters) and meta description (≤ 160) — see `site/content/meta.py` |
| Pages at two or three addresses (www / non-www / trailing slash / `?swcfpc=`) | One address per page: `https://frostlawgroupsc.com/<page>/`. `.htaccess` 301-redirects the rest |
| No DUI page, no city pages, no answer pages for the fan-out questions | 12 estate-planning, 8 probate and 7 criminal-defense spokes; 26 service-area pages; the 19 fan-out questions answered on the page that owns each topic |
| Blog with no posts | 8 articles keyed to local news and neighborhood questions, with bylines and outbound links |
| JavaScript-only navigation, no crawlable practice links, generic 404 | Plain HTML navigation with dropdowns, breadcrumbs, a real 404 page, hub-and-spoke internal linking |
| No structured data | LegalService + Attorney, Person (both attorneys), Service, FAQPage, BlogPosting, BreadcrumbList and WebPage JSON-LD on every page |
| Slow WordPress theme | No framework, no jQuery, ~25 KB of CSS, two variable fonts (~110 KB), lazy images, click-to-load map |

## The client's specific asks

**No DUI on the home page.** The home page, header, footer and every menu never say DUI (the build fails if it does: `DUI_RE` in `build_site.py`). The DUI page still exists at `/dui-lawyer-summerville-sc/` because "summerville dui lawyer" is one of the firm's strongest searches; it is linked from the criminal-defense hub, its sibling pages and the sitemap, so Google can find and rank it without it appearing on the front door.

**"Frost First."** Used as the brand line: top bar on every page, the hero kicker on the home page, the dark "Frost First." section that explains it (before you sign / settle / answer questions), the footer, and the closing call-to-action on every page ("Call Frost first."). The H1s stay keyword-led ("Estate Planning, Probate & Criminal Defense Attorneys in Summerville, SC") because the tagline carries no search demand of its own. It works because it is an instruction, not a slogan — see the recommendation below.

**Google Business Profile.** The share link resolves to CID 6320073536186250254 (Knowledge Graph id /g/11b5pl8mj4). The site links to the profile from the home page, contact page, reviews page and footer, and the JSON-LD `sameAs`/`hasMap` point at it. `REVIEW_URL` in `site/content/firm.py` is the "Ask for reviews" link from the Business Profile dashboard (place id ChIJ4Vm83lNj_ogRDnS6XmVptVc), so the "Leave a Google review" buttons open the review box directly.

**"Add us as a preferred source on Google."** The button uses `https://www.google.com/preferences/source?q=https://frostlawgroupsc.com` — non-www, matching the site's canonical address. Session-specific parameters from a copied browser link (`pli=1`, `authuser=1`, `#no_universal_links=`) are left off because they point at the visitor's own Google account slots, not the firm's. Honest caveat: Google's Preferred Sources feature affects Top Stories, which mostly surfaces news publishers; a law-firm blog will only benefit if it publishes timely, news-shaped articles regularly. The blog is built for exactly that, and the button costs nothing, so it stays — on the home page "Find us" block, the blog index and the footer.

**Yelp.** `https://yelp.to/t18_URraS3` resolves to `https://www.yelp.com/biz/frost-law-group-summerville`; linked from the home page, contact page, reviews page and footer, and included in `sameAs` so entity-matching systems (including the ones AI assistants use) connect the listings.

**Embedded map and directions on local roads.** The contact page and the home page carry a click-to-load Google Maps embed (no API key needed; loading on click keeps the page fast) and a "turn-by-turn in Google Maps" link. The contact page also has written directions from 12 origins (I-26 exit 199A, Goose Creek, Ladson, Moncks Corner, North Charleston, Charleston, St. George, Ridgeville, Knightsville, Nexton, Cane Bay, Mount Pleasant) using real road names in order (North Main Street / US-17A → West 2nd South Street → Central Avenue → South Laurel Street → West Carolina Avenue → Linwood Lane, etc.), with miles and minutes computed from OpenStreetMap routing. Each service-area page has its own directions paragraph and a Google Maps link pre-filled with that town as the origin.

**City pages.** 26 of them under `/service-areas/`. Each is built from verified facts that genuinely differ by town — which county, which probate court, which magistrate or municipal court, where the bond hearing is held, distance and route to the office, ZIP codes, population, landmarks — plus a hand-written local angle. That is what keeps them from being doorway pages.

**Local-news blog.** Eight articles, each tied to a recurring news theme (growth, hurricane season, expungement clinics, back-to-school enforcement, domestic-violence arrest reports, the county line) and each linking out to the original reporting (Post and Courier / Journal Scene / Berkeley Independent, Live 5, ABC News 4, WCBD, county and town news pages) and to the community threads where people ask the question (Nextdoor city pages, r/Charleston, r/SummervilleSC, r/southcarolina — those links carry `rel="nofollow"`). Every legal statement links to the statute on scstatehouse.gov.

## Blog authorship: split them, by expertise, with a "reviewed by" line

What moves the needle is not "two authors" but *credible* authors writing consistently on the topics they can prove they know. The recommendation, implemented in the build:

- **Tara writes probate, guardianship and estate planning.** She sat as a Dorchester County Magistrate Judge (2022–2025) and Associate Probate Judge (2025–2026). A former probate judge explaining how the probate court works is the single strongest expertise signal this firm has, and it is exactly what the fan-out questions ("who handles executor disputes in Summerville probate court?") are asking for.
- **Jack writes criminal defense.** Fourteen years as a Summerville officer and a Charleston County Sheriff's Office narcotics detective and SWAT operator. "By a former officer" is a credible, repeatable byline for drug, DUI, bond and warrant content.
- **Every article names the other attorney as reviewer** ("Reviewed by Jack C. Frost"). That gives both attorneys a footprint on every post and reads as editorial process, which Google's quality guidelines reward for legal content.
- **Do not co-author or alternate.** Co-authoring dilutes the byline; alternating puts the wrong expert on the topic half the time.
- Each attorney page is a real author page (`/attorneys/jack-frost/`, `/attorneys/tara-frost/`) with Person JSON-LD; link them from LinkedIn and YouTube channel descriptions and add the LinkedIn URLs to `same_as` in `firm.py` when available.
- Cadence beats volume: one article every two weeks per attorney, each answering one question people are actually asking on Nextdoor or Reddit, will outperform a monthly burst.

## Before launch — items only the firm can supply

1. **Photos and logo.** The firm's own photos and logo were pulled from the live site (logo, Jack and Tara with the dogs, the formal portrait, all three headshots, the dogs, the client-meeting photo, the estate-plan photo, WealthCounsel badge) and the office exterior from the firm's Facebook page. Fourteen scene images (probate courthouse hallway, downtown Summerville, one per county for the service-area pages, and a cover for each article) were generated with OpenAI's image model to prompts that exclude text, logos and identifiable faces; they are illustrations, not photographs of real places, and can be swapped for real photos at any time by replacing the files in `site/assets/img/` and rebuilding. The logo is the 124-pixel PNG from the live site; a larger or vector version would sharpen the header on high-resolution screens.
2. **Contact form.** Wired to Formspree form `xdekonez`: submissions are emailed to the recipients set in the Formspree dashboard, the subject line carries the topic the visitor chose, Formspree's `_gotcha` honeypot filters bots, and successful submissions land on `/thank-you/` (not indexed). If the Formspree plan ignores the custom redirect, visitors see Formspree's default confirmation instead. Add Jack, Tara and Cassie as recipients in the dashboard.
3. **Google review link** is in place (see above). LinkedIn profiles, bar numbers, admission dates and emails for both attorneys are in from the SC Judicial Branch directory and are shown on the attorney pages, the contact page and in the Person schema.
4. **Confirm three statements written from the audit's assumptions:** flat fees for estate plans and uncontested estates; free injury consultations (stated on the injury site) but not free consultations generally; "we meet clients at home or at a facility" for capacity-limited signings (guardianship article). Edit `site/content/*.py` if any is wrong.
5. **Jack's law-enforcement timeline.** The current main site says he retired from the Charleston County Sheriff's Office in 2013, the injury site says 2015, and the Town of Summerville's November 2023 announcement of his appointment as DUI prosecutor describes him as joining "from the Charleston County Sheriff's Office, where he was a narcotics detective." The rebuild keeps 2013; Jack should confirm the dates.
5a. **Jack's role as Summerville DUI prosecutor.** The attorney page states the November 2023 appointment (linked to the Town's announcement), and the DUI page says the firm does not defend DUI charges brought by the Town in Summerville Municipal Court because of it. If Jack no longer holds the role, or the conflict is handled differently, edit `attorneys/jack-frost` in `core.py` and the DUI page in `criminal.py`. This is also why DUI stays off the home page.
6. **Analytics.** No tracking is included, which is also why there is no cookie banner: the site sets no cookies and loads no third-party scripts on page load. If GA4, a chat widget, call tracking or a pixel is added in `head_html()` in `build_site.py`, add a consent tool at the same time and update the privacy policy.
7. **Legal pages.** The privacy policy, the terms of use and legal disclaimer, and the accessibility statement were drafted to match what the site does and the South Carolina advertising rules as we understand them. The attorneys should review all three before launch.
8. **The Dorchester County Probate Court's Summerville office**: the county's official page lists only St. George, so the site does not claim a Summerville office. If one exists, add it to `courts` in `site/build_local_data.py`.

## Deploying on Vercel

1. In Vercel, import the GitHub repository and set the production branch to `main`. Leave the framework as "Other"; `vercel.json` at the repository root tells Vercel to serve the prebuilt `website/` folder with no build step, to keep trailing slashes, to apply the redirect map, and to cache assets.
2. Add both `frostlawgroupsc.com` and `www.frostlawgroupsc.com` under the project's Domains and make the apex the primary domain. Vercel then 301-redirects www to the apex and issues the HTTPS certificate; the `.htaccess` file in `website/` is ignored on Vercel and only matters on an Apache host.
3. Point DNS at Vercel when you are ready to cut over (an A record for the apex and a CNAME for www, per the values Vercel shows). Until then the deployment is reachable at its `*.vercel.app` address for review.
4. `404.html` in `website/` is served automatically for unknown addresses.
5. To change content: edit `site/content/*.py`, run `python3 site/build_site.py`, commit `website/` and `vercel.json`, and push to `main`. Vercel deploys on push.

## Deploying on SiteGround (or any Apache host)

1. Upload the contents of `website/` to the document root (`public_html`). Include the hidden `.htaccess`.
2. Make sure WordPress is no longer serving the root, or its rewrite rules will override these (either move the WordPress install or delete its `.htaccess` first).
3. In Search Console, submit `https://frostlawgroupsc.com/sitemap.xml` and request indexing for the home page, the three hubs and the DUI page.
4. Update the Business Profile website field to `https://frostlawgroupsc.com/` (no www).
5. After launch, check that `https://www.frostlawgroupsc.com/probate` redirects to `https://frostlawgroupsc.com/probate/` — that single test exercises the host, https and trailing-slash rules.

## Facts and sources

Court addresses, phones and websites, office coordinates and routes, community populations and ZIP codes, and every statute cited were verified against official sources in September 2026 and are recorded with their source URLs in `site/content/facts.json`; `site/build_local_data.py` turns that into `local_data.json`, which the pages read. Notable corrections made while verifying: the small-estate affidavit ceiling is $45,000 (raised from $25,000 in May 2025); the Dorchester County Detention Center is on Hodge Road in Summerville, not in St. George; Summerville Municipal Court is on the second floor of Town Hall at 200 S. Main Street.
