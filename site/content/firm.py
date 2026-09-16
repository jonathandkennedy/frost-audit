"""Firm facts used everywhere: name, address, phone, hours, links, people, navigation, redirects.

Everything here is either taken verbatim from the current frostlawgroupsc.com pages or from the
firm's public Google Business Profile / Yelp listings. Items marked TODO need the firm's confirmation.
"""
import json
import os

BUILD_DATE = "2026-09-16"
ORIGIN = "https://frostlawgroupsc.com"
PI_SITE = "https://www.summervilleaccidentattorney.com/"

NAME = "Frost Law Group, LLC"
TAGLINE = "Frost First."
TAGLINE_LINE = "Before you sign, settle, or answer questions — call us."
STREET = "128 Linwood Lane"
CITY = "Summerville"
STATE = "SC"
ZIP = "29483"
PHONE = "(843) 419-6653"
PHONE_E164 = "+18434196653"
GEO = None  # (lat, lon) filled from local_data when verified

MAP_QUERY = "128 Linwood Lane, Summerville, SC 29483"
MAP_EMBED_URL = "https://www.google.com/maps?q=" + MAP_QUERY.replace(" ", "+") + "&output=embed"
DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=" + MAP_QUERY.replace(" ", "+")

# Public listings. The GBP and Yelp short links are the ones the firm shared; the review link is the
# Business Profile "write a review" address and is updated once the place id is confirmed.
GBP_URL = "https://maps.google.com/maps?cid=6320073536186250254"  # resolved from the firm's share.google link (CID 6320073536186250254)
GBP_SHARE_URL = "https://share.google/CBpXoFvmaAoVP0HuZ"
REVIEW_URL = "https://maps.google.com/maps?cid=6320073536186250254"  # TODO: replace with the "Ask for reviews" link from the Business Profile dashboard
YELP_URL = "https://www.yelp.com/biz/frost-law-group-summerville"  # canonical form of https://yelp.to/t18_URraS3
PREFERRED_SOURCE_URL = "https://www.google.com/preferences/source?q=https://www.frostlawgroupsc.com"
FACEBOOK = "https://www.facebook.com/frostlawgroupsc/"
INSTAGRAM = "https://www.instagram.com/frostlawgroupllc/"
TWITTER = "https://twitter.com/FrostLawGroup"
LINKEDIN = "https://www.linkedin.com/company/frost-law-groupsc"
SOCIAL = [("Facebook", FACEBOOK, "fb"), ("Instagram", INSTAGRAM, "ig"), ("LinkedIn", LINKEDIN, "in"), ("X (Twitter)", TWITTER, "x")]
SAME_AS = [FACEBOOK, INSTAGRAM, LINKEDIN, TWITTER, GBP_URL, YELP_URL, PI_SITE]
KGMID = "/g/11b5pl8mj4"  # Google Knowledge Graph id for the firm
RATING = (4.8, 30)  # Google Business Profile, September 2026

HOURS_DISPLAY = [("Monday – Thursday", "9:00 AM – 5:00 PM"), ("Friday", "9:00 AM – 12:00 PM"), ("Saturday – Sunday", "Closed")]
HOURS_SHORT = "Mon–Thu 9–5 · Fri 9–12 · Friday afternoons by appointment"
HOURS_LD = [("Monday", "09:00", "17:00"), ("Tuesday", "09:00", "17:00"), ("Wednesday", "09:00", "17:00"), ("Thursday", "09:00", "17:00"), ("Friday", "09:00", "12:00")]

DISCLAIMER = ("This website is for informational purposes only and does not create an attorney-client relationship. "
              "Nothing here is legal advice for your situation; talk to a licensed South Carolina attorney about your facts.")
ASIDE_BLURB = "Jack and Tara answer their own phones. Tell us what happened and we'll tell you the next step."
LLMS_SUMMARY = ("Frost Law Group, LLC is a husband-and-wife law firm in Summerville, South Carolina handling estate planning, "
                "probate and criminal defense for families in Dorchester, Berkeley and Charleston counties. Personal injury cases are handled at summervilleaccidentattorney.com.")

LOGO = "logo.svg"  # placeholder wordmark until the firm's PNG logo is dropped into site/assets/img/logo.png
OG_SOURCE = "couple.jpg"
FORM_ENDPOINT = "https://formspree.io/f/REPLACE_WITH_FORM_ID"  # TODO: swap for the firm's form handler before launch

ATTORNEYS = {
    "jack": dict(
        key="jack", slug="attorneys/jack-frost", name="Jack C. Frost", short="Jack Frost", first="Jack", headshot="headshot-jack.jpg", bio_photo="jack-bio.jpg",
        byline="Attorney at Law · 14 years in Lowcountry law enforcement before law school",
        aside="Jack spent fourteen years as a Summerville police officer and a Charleston County Sheriff's Office detective and SWAT operator before earning his law degree. He knows how cases are built because he built them.",
        alumni=["Charleston School of Law", "Strayer University", "Trident Technical College", "College of Charleston"],
        knows=["Criminal defense", "Drug charges", "Bond hearings", "Expungements", "Traffic offenses", "Arrest warrants", "Estate planning"],
        same_as=[],  # TODO: LinkedIn and SC Bar profile URLs
        ld_description="Summerville, SC criminal defense and estate planning attorney; former Summerville Police Department officer and Charleston County Sheriff's Office detective and SWAT team member.",
    ),
    "tara": dict(
        key="tara", slug="attorneys/tara-frost", name="Tara L. Frost", short="Tara Frost", first="Tara", headshot="headshot-tara.jpg", bio_photo="tara-bio.jpg",
        byline="Attorney at Law · former Dorchester County Magistrate and Associate Probate Judge",
        aside="Tara served as a Dorchester County Magistrate Judge (2022–2025) and Associate Probate Judge (2025–2026). She has sat on the other side of the probate bench and knows what the court needs to see.",
        alumni=["Charleston School of Law"],
        knows=["Probate and estate administration", "Estate planning", "Guardianship and conservatorship", "Wills and trusts", "Personal injury"],
        same_as=[],  # TODO: LinkedIn and SC Bar profile URLs
        ld_description="Summerville, SC probate, estate planning and personal injury attorney; former Dorchester County Magistrate Judge and Associate Probate Judge.",
    ),
}

TEAM = {
    "jack": dict(name="Jack C. Frost", role="Attorney at Law", photo="headshot-jack.jpg", alt="Jack C. Frost, attorney", slug="attorneys/jack-frost"),
    "tara": dict(name="Tara L. Frost", role="Attorney at Law", photo="headshot-tara.jpg", alt="Tara L. Frost, attorney", slug="attorneys/tara-frost"),
    "cassie": dict(name="Cassandra “Cassie” Snyder", role="Paralegal", photo="headshot-cassie.jpg", alt="Cassie Snyder, paralegal", slug=None),
    "dogs": dict(name="The Frost Pups", role="Comfort specialists · Mistoc and Palmer", photo="dogs.jpg", alt="The firm's Golden Retrievers, Mistoc and Palmer", slug=None),
}

# Client words quoted on the current site (kept verbatim). Source labels stay generic until the firm confirms where each came from.
REVIEWS = [
    dict(name="Beth Z.", stars=5, source="Client review · estate planning", text="Frost Law Group made our Estate Planning a relatively simple process. All our concerns were answered with clarity. They go out of their way to make you feel comfortable. Everything was handled promptly—just a great experience. We HIGHLY recommend. Thank you!!! The best!!"),
    dict(name="Maya J.", stars=5, source="Client review", text="The Frost Law Group went above and beyond for my family. They are passionate about their clients and their client's families. I will always recommend this group and will use them in the future."),
    dict(name="Leonard J.", stars=5, source="Google review · injury claim", text="My family settled our claim with this company following a car accident last year. The staff was professional, courteous and polite throughout the entire process. I would highly recommend their services."),
    dict(name="Mary J.", stars=5, source="Google review", text="Jack and his staff are so easy to work with."),
    dict(name="Stacy R.", stars=5, source="Google review", text="The energy and vibe when you walk into the building is amazing!"),
]

# Hubs and their spokes (order = order in menus and sidebars). DUI is a spoke but is kept out of the
# global navigation and footer so the home page never mentions it; it is linked from the criminal-defense hub.
HUB_SPOKES = {
    "estate-planning-attorney": ["last-will-and-testament", "revocable-trust", "power-of-attorney", "living-will", "asset-protection-trusts",
                                 "estate-planning-for-blended-families", "estate-plan-review", "estate-planning-for-business-owners",
                                 "special-needs-planning", "dying-without-a-will-in-south-carolina", "estate-planning-costs", "high-net-worth-estate-planning"],
    "probate": ["probate-process", "executor-duties", "executor-disputes", "small-estate-affidavit", "will-contests",
                "guardianship-and-conservatorship", "trust-administration", "probate-courts"],
    "criminal-defense": ["dui-lawyer-summerville-sc", "drug-charges", "domestic-violence-defense", "bond-hearings", "expungements", "traffic-tickets", "arrest-warrants"],
}
HUB_ATTORNEY = {"estate-planning-attorney": "tara", "probate": "tara", "criminal-defense": "jack"}

NAV = [
    ("Estate Planning", "estate-planning-attorney", HUB_SPOKES["estate-planning-attorney"][:8], "All estate planning services"),
    ("Probate", "probate", HUB_SPOKES["probate"], "All probate services"),
    ("Criminal Defense", "criminal-defense", [s for s in HUB_SPOKES["criminal-defense"] if s != "dui-lawyer-summerville-sc"], "All criminal defense services"),
    ("Personal Injury", "personal-injury", [], ""),
    ("About", "about-us", ["attorneys/jack-frost", "attorneys/tara-frost", "reviews", "service-areas", "faq"], "Our team"),
    ("In the Know", "blog", [], ""),
]

FOOTER_PRACTICE = [("Estate planning", "estate-planning-attorney"), ("Wills", "last-will-and-testament"), ("Revocable living trusts", "revocable-trust"),
                   ("Powers of attorney", "power-of-attorney"), ("Probate", "probate"), ("Guardianship & conservatorship", "guardianship-and-conservatorship"),
                   ("Criminal defense", "criminal-defense"), ("Expungements", "expungements")]
FOOTER_EXPLORE = [("Our team", "about-us"), ("Jack C. Frost", "attorneys/jack-frost"), ("Tara L. Frost", "attorneys/tara-frost"), ("Client reviews", "reviews"),
                  ("In the Know (blog)", "blog"), ("Frequently asked questions", "faq"), ("Contact & directions", "contact-us")]
FOOTER_AREAS = ["service-areas/summerville", "service-areas/goose-creek", "service-areas/ladson", "service-areas/north-charleston", "service-areas/moncks-corner",
                "service-areas/hanahan", "service-areas/charleston", "service-areas/mount-pleasant", "service-areas/ridgeville", "service-areas/st-george"]

COUNTY_ORDER = ["Dorchester County", "Berkeley County", "Charleston County", "Colleton County"]
AREA_SERVED = ["Summerville", "Goose Creek", "Ladson", "North Charleston", "Moncks Corner", "Hanahan", "Charleston", "Mount Pleasant", "Ridgeville", "St. George",
               "Harleyville", "Knightsville", "Sangaree", "Nexton", "Cane Bay", "Lincolnville", "Daniel Island", "West Ashley", "James Island", "Johns Island", "Walterboro"]

# Old address (regex, no leading slash) -> new address. Applied in .htaccess as 301s.
REDIRECTS = [
    ("probate-2/?", "/probate/"),
    ("motor-vehicle-personal-injury/?", "/personal-injury/"),
    ("author/.*", "/about-us/"),
    ("durable-power-of-attorney/?", "/power-of-attorney/"),
    ("healthcare-power-of-attorney/?", "/power-of-attorney/"),
]

# Courts and places come from the verified local data file (built from official sources).
COURTS = {}
_ld = os.path.join(os.path.dirname(__file__), "local_data.json")
if os.path.exists(_ld):
    _d = json.load(open(_ld, encoding="utf-8"))
    COURTS = _d.get("courts", {})
    if _d.get("office_geo"):
        GEO = tuple(_d["office_geo"])
