"""Service-area pages: one page per community, built from verified county/court/route data plus
hand-written local copy. Each page explains which courts handle the reader's matter and how to
reach the office on local roads—the two things that genuinely differ from town to town."""
from .base import page, A, ext, checks, steps, callout, band, esc, table
from . import firm
from .local import PLACES, ROUTES, directions_cards, link

TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
DEST = firm.MAP_QUERY.replace(" ", "+")

# County-level facts used on every city page in that county.
COUNTY = {
    "Dorchester County": dict(
        probate="dorchester_probate", probate_extra="dorchester_detention", courthouse="dorchester_courthouse",
        magistrate="dorchester_magistrate_summerville", detention="Dorchester County Detention Center on Hodge Road in Summerville", seat="St. George",
        circuit="First Judicial Circuit", sheriff="Dorchester County Sheriff's Office",
        blurb="Dorchester County's courthouse complex—the probate court, the clerk of court and General Sessions (felony) court—is in St. George, about 28 miles up Highway 78 from Summerville. The county magistrates sit in St. George and at the Troy Knight Judicial Complex on Deming Way in Summerville, and bond hearings are held at the county detention center on Hodge Road in Summerville.",
    ),
    "Berkeley County": dict(
        probate="berkeley_probate", probate_extra="hill_finklea", courthouse="berkeley_courthouse",
        magistrate=None, detention="Hill-Finklea Detention Center in Moncks Corner", seat="Moncks Corner",
        circuit="First Judicial Circuit", sheriff="Berkeley County Sheriff's Office",
        blurb="Berkeley County's courthouse, probate court and detention center are all in Moncks Corner. Estates, guardianships and felony cases from Goose Creek, Hanahan, Nexton, Cane Bay and the rest of the county are heard there; misdemeanors and tickets go to the county magistrates or, inside city limits, the municipal courts.",
    ),
    "Charleston County": dict(
        probate="charleston_probate", probate_extra="al_cannon", courthouse="charleston_judicial",
        magistrate=None, detention="Sheriff Al Cannon Detention Center in North Charleston", seat="Charleston",
        circuit="Ninth Judicial Circuit", sheriff="Charleston County Sheriff's Office",
        blurb="Charleston County's probate court and judicial center are on Broad Street in downtown Charleston; bond hearings are held at the detention center in North Charleston. The county is its own judicial circuit, so a Charleston County charge is prosecuted by a different solicitor's office than a Dorchester or Berkeley charge.",
    ),
    "Colleton County": dict(
        probate="colleton_probate", probate_extra=None, courthouse="colleton_courthouse",
        magistrate=None, detention="Colleton County Detention Center in Walterboro", seat="Walterboro",
        circuit="Fourteenth Judicial Circuit", sheriff="Colleton County Sheriff's Office",
        blurb="Colleton County's courthouse and probate court are in Walterboro. Estates and guardianships for Walterboro, Cottageville and the rest of the county are filed there.",
    ),
}

# Per-community copy. county, route key, municipal court key (if the town has its own court), intro, and a
# practice-area angle written for that community. Population/ZIP/landmark facts render from PLACES when verified.
CITIES = [
    dict(slug="summerville", name="Summerville", county="Dorchester County", route="i26-199", court="summerville_municipal", label="Home base · Flowertown",
         intro="Summerville is home. Our office is on Linwood Lane, a few minutes from Hutchinson Square and Azalea Park, and Jack and Tara both graduated from Summerville High School. Most of our clients live within the town limits or just outside them in Dorchester County—though a growing share live in the Berkeley County part of town.",
         angle=("Probate for Summerville families", "Estates for Summerville addresses in Dorchester County are opened with the Dorchester County Probate Court in St. George; addresses in the Berkeley County part of Summerville (Nexton, Cane Bay, Sangaree) file in Moncks Corner. Tara served as a Dorchester County Associate Probate Judge and knows both dockets."),
         note="Inside the town limits, tickets written by Summerville police and town ordinance cases are heard in Summerville Municipal Court on the second floor of Town Hall, 200 S. Main Street, regardless of which county the stop happened in."),
    dict(slug="goose-creek", name="Goose Creek", county="Berkeley County", route="goose-creek", court="goose_creek_municipal", label="Berkeley County's largest city",
         intro="Goose Creek is fifteen minutes from our office by Highway 17-A or Highway 176, and a large share of our probate and estate-planning clients live in Crowfield, Brickhope and the neighborhoods around the Naval Weapons Station. Military and civilian families at Joint Base Charleston have planning needs—deployments, survivor benefits, out-of-state property—that we handle every week.",
         angle=("Planning for military families", "Service members and their spouses need powers of attorney that work during a deployment, wills that account for SGLI and survivor benefit designations, and guardianship nominations that name someone actually available. We coordinate with the base legal office's documents rather than duplicating them."),
         note="Goose Creek Police tickets and ordinance cases are heard in Goose Creek Municipal Court; sheriff and Highway Patrol cases go to the Berkeley County magistrate."),
    dict(slug="ladson", name="Ladson", county="Dorchester County", route="ladson", court="berkeley_probate", label="Three counties, one community",
         intro="Ladson sits where Dorchester, Berkeley and Charleston counties meet, which makes it the community where “which court?” is asked most often. College Park Road, Ladson Road and the Exchange Park fairgrounds are ten minutes from our office, and we sort out the county question on the first call.",
         angle=("Which county is your Ladson address in?", "A Ladson estate is probated in the county where the person lived—Dorchester for addresses off Ladson Road toward Summerville, Berkeley for the College Park Road corridor, Charleston for the southern edge. The county on the property tax bill controls. We check it before filing so the family does not lose weeks to a refiling."),
         note="Ladson is unincorporated, so there is no municipal court; charges go to the magistrate of the county where the stop or arrest happened."),
    dict(slug="north-charleston", name="North Charleston", county="Charleston County", route="north-charleston", court="north_charleston_municipal", label="South Carolina's third-largest city",
         intro="North Charleston is twenty minutes down I-26 and the source of a steady stream of criminal defense and probate work. Park Circle, the Tanger Outlets corridor and the neighborhoods off Dorchester Road and Ashley Phosphate are all in our regular rounds, and Jack knows the North Charleston Municipal Court and the Charleston County courts well from his years with the Sheriff's Office.",
         angle=("Criminal charges in North Charleston", "North Charleston Police tickets and misdemeanors are heard in North Charleston Municipal Court; felony charges go to Charleston County General Sessions and bond hearings to the Al Cannon Detention Center. The city extends into Dorchester and Berkeley counties near Ladson and Dorchester Road, which changes the court for sheriff's cases."),
         note="Estates for North Charleston addresses in Charleston County are opened at the Charleston County Probate Court on Broad Street downtown; the Dorchester County portion files in St. George."),
    dict(slug="moncks-corner", name="Moncks Corner", county="Berkeley County", route="moncks-corner", court=None, label="Berkeley County seat",
         intro="Moncks Corner is the Berkeley County seat and the town we drive to for every Berkeley County probate, guardianship and General Sessions matter. The courthouse, the probate court and the Hill-Finklea Detention Center are within a few blocks of each other on California Avenue and Highway 52. For residents of Moncks Corner, Pinopolis and the Lake Moultrie communities, we are thirty minutes down Highway 17-A.",
         angle=("Probate and guardianship in Berkeley County", "Tara handles estates and guardianships in the Berkeley County Probate Court regularly; the forms and procedure match Dorchester's, but the docket and local practices differ. Bond hearings for Berkeley County arrests are held at Hill-Finklea, and Jack appears there."),
         note="Moncks Corner Police cases go to the town's municipal court; county cases to the Berkeley County magistrate in Moncks Corner."),
    dict(slug="hanahan", name="Hanahan", county="Berkeley County", route="hanahan", court="hanahan_municipal", label="Berkeley County city on the Cooper River",
         intro="Hanahan's neighborhoods—Tanner Plantation, Otranto, the streets around Hanahan High—are twenty-five minutes from our office by I-26 and Rivers Avenue. It is a Berkeley County city surrounded by Charleston County, which regularly confuses families about where an estate or a charge belongs.",
         angle=("Hanahan estates go to Moncks Corner", "Because Hanahan is in Berkeley County, a Hanahan resident's estate is probated in Moncks Corner, not downtown Charleston, and a Hanahan Police charge is heard in Hanahan Municipal Court. We handle both and explain the geography on the first call."),
         note="Sheriff and Highway Patrol cases from Hanahan go to the Berkeley County magistrate."),
    dict(slug="charleston", name="Charleston", county="Charleston County", route="charleston", court="charleston_municipal", label="County seat · Ninth Circuit",
         intro="Downtown Charleston is thirty to forty minutes from Summerville depending on I-26, and it is where every Charleston County probate, guardianship and General Sessions matter is heard—the probate court at 84 Broad Street and the judicial center at 100 Broad. We represent Charleston families in estates and guardianships and defend charges in the Charleston Municipal Court and General Sessions.",
         angle=("Estates in the Charleston County Probate Court", "The Charleston County court is the busiest in the region, and its scheduling and filing practices differ from Dorchester and Berkeley. Tara's judicial background in the neighboring county translates directly: complete filings, supported valuations, and an accounting the court can approve the first time."),
         note="Charleston Police tickets and ordinance cases are heard in Charleston Municipal Court; county cases go to the Charleston County magistrates."),
    dict(slug="mount-pleasant", name="Mount Pleasant", county="Charleston County", route="mount-pleasant", court=None, label="East of the Cooper",
         intro="Mount Pleasant families come to us for estate plans that have to manage more than a house—rental property on the islands, a business, a second home, a blended family. The drive from Coleman Boulevard is about forty-five minutes on I-526 and I-26, and we schedule Mount Pleasant clients for a single longer meeting rather than several short ones.",
         angle=("Larger estates and trust-based plans", "Trust-based plans, asset protection for rental portfolios, and coordination with your advisors are the core of our Mount Pleasant work; see estate planning for larger estates. Probate and guardianship matters for Mount Pleasant addresses are heard at the Charleston County Probate Court downtown."),
         note="Mount Pleasant Police tickets are heard in the town's municipal court; sheriff cases go to the Charleston County magistrates."),
    dict(slug="ridgeville", name="Ridgeville", county="Dorchester County", route="ridgeville", court=None, label="Upper Dorchester County",
         intro="Ridgeville is twenty minutes up Highway 78 and Highway 27 from Summerville, and its families—longtime residents along Givhans Ferry and the newer households drawn by the Volvo campus at Camp Hall—are Dorchester County for probate, guardianship and General Sessions purposes. The courthouse in St. George is closer to Ridgeville than to us.",
         angle=("Heirs' property and family land", "Upper Dorchester County has more family land passed down without a will than anywhere else we work. Clearing title on heirs' property, probating estates that were never opened, and writing wills that keep land in the family without splitting it into unusable shares are a regular part of our Ridgeville practice."),
         note="Ridgeville is a town, but tickets and misdemeanors are heard by the Dorchester County magistrate; the town does not maintain a separate court docket for most cases."),
    dict(slug="st-george", name="St. George", county="Dorchester County", route="st-george", court=None, label="Dorchester County seat",
         intro="St. George is the Dorchester County seat, and we are in its courthouse complex on Jim Bilton Boulevard constantly—for probate hearings, guardianship hearings, General Sessions and bond hearings at the detention center. For St. George, Reevesville and Harleyville families, the courthouse is close; our office is thirty minutes down Highway 78.",
         angle=("Court-town practice", "Because the Dorchester County Probate Court and General Sessions sit in St. George, we can often combine a client meeting with a court appearance and meet St. George clients at the courthouse. Tara sat as an Associate Probate Judge in this building."),
         note="St. George has a municipal court for town-police cases; county cases go to the Dorchester County magistrate in St. George."),
    dict(slug="harleyville", name="Harleyville", county="Dorchester County", route="harleyville", court=None, label="Western Dorchester County",
         intro="Harleyville sits at the western edge of Dorchester County on Highway 178, closer to the courthouse in St. George than to Summerville. Its families are Dorchester County for every court purpose, and many hold land that has passed through generations without formal probate.",
         angle=("Estates that were never opened", "We regularly open estates for parents or grandparents who died years ago, clear title on family land, and prepare wills that keep the property together. If a Harleyville family is selling land and discovers a title problem, that is usually the moment to call."),
         note="Tickets and misdemeanors in the Harleyville area are heard by the Dorchester County magistrate in St. George."),
    dict(slug="walterboro", name="Walterboro", county="Colleton County", route="walterboro", court=None, label="Colleton County seat",
         intro="Walterboro is forty minutes southwest on I-95 or Highway 17-A, and the Colleton County Courthouse and Probate Court on Hampton Street handle every Walterboro and Cottageville estate, guardianship and felony case. We take Colleton County probate and estate-planning matters and, selectively, criminal cases in the Fourteenth Circuit.",
         angle=("Colleton County probate", "The Colleton County Probate Court uses the same statewide forms and statutes as Dorchester and Berkeley; Tara's experience transfers directly. For Walterboro families with property in more than one county, we coordinate the estate so ancillary filings are handled once."),
         note="Walterboro Police cases are heard in the city's municipal court; county cases go to the Colleton County magistrate."),
    dict(slug="knightsville", name="Knightsville", county="Dorchester County", route="knightsville", court=None, label="Just west of town",
         intro="Knightsville is five minutes from our office along Central Avenue and Orangeburg Road, and it is Summerville in every practical sense except that much of it lies outside the town limits. That one difference decides which court hears a ticket and which police agency responds.",
         angle=("Outside the town limits", "Knightsville addresses are unincorporated Dorchester County: sheriff's cases and Highway Patrol tickets go to the county magistrate on Deming Way in Summerville rather than to Summerville Municipal Court, and estates are opened with the Dorchester County Probate Court."),
         note="Knightsville has no municipal court; the Dorchester County Sheriff's Office is the responding agency."),
    dict(slug="sangaree", name="Sangaree", county="Berkeley County", route="sangaree", court=None, label="Berkeley County side of Summerville",
         intro="Sangaree is a Summerville-address community across the county line in Berkeley County, ten minutes from our office by Highway 78 and Royle Road. Its residents' estates, guardianships and county-level charges belong in Moncks Corner, which surprises many families who assume Dorchester County.",
         angle=("Berkeley County paperwork", "A Sangaree resident's estate is probated in the Berkeley County Probate Court and a durable power of attorney is recorded with the Berkeley County Register of Deeds. We prepare documents for the correct county and file where they belong."),
         note="Sangaree is unincorporated; tickets and misdemeanors go to the Berkeley County magistrate."),
    dict(slug="nexton", name="Nexton", county="Berkeley County", route="nexton", court=None, label="Summerville 29486 · Berkeley County",
         intro="Nexton is the fastest-growing part of “Summerville,” and it is in Berkeley County. The exit 197 interchange puts our office about ten minutes away, and Nexton families—many newly arrived from other states—make up a large share of our estate-plan reviews and new plans.",
         angle=("New residents, new documents", "Most Nexton households arrived with wills and powers of attorney from somewhere else. We review them, re-sign South Carolina documents where needed, record powers of attorney with Berkeley County, and make sure the new home is titled to the trust if there is one. Probate for a Nexton address is in Moncks Corner."),
         note="Nexton has been annexed into the Town of Summerville while remaining in Berkeley County: Summerville police cases go to Summerville Municipal Court, sheriff and Highway Patrol cases to the Berkeley County magistrate, and county filings to Moncks Corner."),
    dict(slug="cane-bay", name="Cane Bay", county="Berkeley County", route="cane-bay", court=None, label="Summerville 29486 · Berkeley County",
         intro="Cane Bay Plantation, off Highway 176 north of Summerville, is home to thousands of retirees and young families with a Summerville mailing address in Berkeley County. We are about twenty minutes away by Highway 176 and Highway 17-A, and we meet many Cane Bay clients for estate plans, trust reviews and, increasingly, probate.",
         angle=("Retirement planning and probate in Berkeley County", "Cane Bay's 55-plus neighborhoods generate the questions retirees ask everywhere: trust or will, how to protect a home from long-term-care costs, how to leave an inheritance to children in other states. When a Cane Bay resident dies, the estate is opened in Moncks Corner, not St. George."),
         note="Cane Bay is unincorporated Berkeley County; the sheriff's office responds and the county magistrate hears tickets."),
    dict(slug="lincolnville", name="Lincolnville", county="Charleston County", route="lincolnville", court=None, label="Historic town on the Dorchester line",
         intro="Lincolnville, founded in 1867, sits on the Charleston County side of the line just south of Summerville—five minutes from our office. Its families are Charleston County for probate and General Sessions purposes even though the town is surrounded by Dorchester County communities.",
         angle=("Charleston County court, Summerville neighbor", "A Lincolnville estate is opened at the Charleston County Probate Court downtown, and heirs' property questions—common in a town with a century and a half of family land—are a regular part of our work here. Tickets from the town's police are heard in Lincolnville's municipal court."),
         note="County cases from Lincolnville go to the Charleston County magistrates; bond hearings are at the Al Cannon Detention Center."),
    dict(slug="daniel-island", name="Daniel Island", county="Berkeley County", route="daniel-island", court=None, label="City of Charleston · Berkeley County",
         intro="Daniel Island is inside the City of Charleston but in Berkeley County—which means an estate is probated in Moncks Corner, not on Broad Street, and a Charleston Police ticket goes to Charleston Municipal Court while a sheriff's case goes to Berkeley County. We are about thirty-five minutes away by I-526 and I-26.",
         angle=("Trust-based plans for Daniel Island families", "Daniel Island households tend to need trust-based plans: privacy, a second property, a business, or an estate large enough that tax planning matters. Probate avoidance also matters more when the alternative is a Berkeley County estate for a Charleston-city resident."),
         note="The Charleston Police Department patrols Daniel Island; county-level matters are Berkeley County."),
    dict(slug="west-ashley", name="West Ashley", county="Charleston County", route="west-ashley", court="charleston_municipal", label="City of Charleston, west of the Ashley",
         intro="West Ashley—the neighborhoods off Savannah Highway, Glenn McConnell Parkway and Bees Ferry Road—is thirty minutes from our office by Highway 61 or I-526. It is part of the City of Charleston, so municipal charges are heard downtown and estates at the Charleston County Probate Court.",
         angle=("Charleston County estates and plans", "We handle West Ashley estates, guardianships and estate plans at the Charleston County court and, for clients who prefer it, by phone and video with a single signing meeting in Summerville."),
         note="Charleston Police cases from West Ashley go to Charleston Municipal Court; sheriff cases to the Charleston County magistrates."),
    dict(slug="james-island", name="James Island", county="Charleston County", route="james-island", court=None, label="Town and city, one island",
         intro="James Island is split between the Town of James Island and the City of Charleston, with Charleston County handling probate, guardianship and felony cases for the whole island. We are about forty minutes away and represent island families in estates, plans and criminal matters in the Charleston County courts.",
         angle=("Two governments, one county", "Whether a James Island ticket is heard in the town's municipal court or Charleston's depends on which police agency wrote it; the county court question is simpler—everything is Charleston County. We sort the jurisdiction out on the first call."),
         note="Bond hearings for James Island arrests are at the Al Cannon Detention Center in North Charleston."),
    dict(slug="johns-island", name="Johns Island", county="Charleston County", route="johns-island", court=None, label="Rural island, fast growth",
         intro="Johns Island's mix of generational family land and new subdivisions makes it, like upper Dorchester County, a place where heirs' property and never-opened estates are common. It is about forty-five minutes from Summerville by Highway 17 and Main Road, and we handle Johns Island estates and plans at the Charleston County Probate Court.",
         angle=("Family land on Johns Island", "Clearing title, probating a parent's or grandparent's estate decades late, and drafting wills and trusts that keep land intact are the core of our Johns Island work. Development pressure on the island means these questions now come with real money attached."),
         note="Johns Island is largely unincorporated Charleston County, with City of Charleston portions; the county magistrates hear sheriff cases."),
    dict(slug="ravenel", name="Ravenel", county="Charleston County", route="ravenel", court=None, label="Highway 17 South",
         intro="Ravenel, on Highway 17 south of Charleston, is about forty minutes from our office by Highway 165 and Highway 61. Its families are Charleston County for probate and General Sessions purposes, and its rural land brings the same heirs' property and estate questions we see on Johns Island and in upper Dorchester County.",
         angle=("Estates and land in southern Charleston County", "We open estates, clear title and prepare plans for Ravenel and Hollywood families at the Charleston County Probate Court, and handle Highway 17 traffic and criminal cases in the county magistrate's court."),
         note="Ravenel's town police cases go to the town's municipal court; county cases to the Charleston County magistrates."),
    dict(slug="hollywood", name="Hollywood", county="Charleston County", route="hollywood", court=None, label="Southern Charleston County",
         intro="Hollywood, near the Stono River and Highway 162, is Charleston County for every court purpose and about forty-five minutes from Summerville. Estates, guardianships and plans for Hollywood families are handled at the Charleston County Probate Court, and we meet clients by phone and video to save the drive.",
         angle=("Probate and planning for Hollywood families", "Generational land, mobile homes titled separately from the land beneath them, and estates that were never opened are the recurring issues. We untangle them one deed at a time."),
         note="The Town of Hollywood has a municipal court for town-police cases; county cases go to the Charleston County magistrates."),
    dict(slug="reevesville", name="Reevesville", county="Dorchester County", route="reevesville", court=None, label="Near the county seat",
         intro="Reevesville is a small Dorchester County town a few minutes from the courthouse in St. George. Its families are Dorchester County for probate, guardianship and General Sessions purposes, and we combine Reevesville meetings with our regular court days in St. George.",
         angle=("Family land and late estates", "As in Harleyville and Ridgeville, much of Reevesville's land has passed informally through families. We probate old estates, clear title and write wills that keep land together."),
         note="Tickets and misdemeanors go to the Dorchester County magistrate in St. George."),
    dict(slug="carnes-crossroads", name="Carnes Crossroads", county="Berkeley County", route="carnes-crossroads", court=None, label="Highway 17-A at Highway 176",
         intro="Carnes Crossroads, at the junction of Highway 17-A and Highway 176, is a planned community in Berkeley County with Summerville and Goose Creek addresses. It is fifteen minutes from our office up 17-A, and its residents' estates and guardianships are filed in Moncks Corner.",
         angle=("New homes, Berkeley County filings", "Most Carnes Crossroads households are new to South Carolina or new to the area. We review out-of-state documents, prepare South Carolina wills, trusts and powers of attorney, and record them with Berkeley County. When a resident dies, the estate is opened at the Berkeley County Probate Court."),
         note="Carnes Crossroads is unincorporated Berkeley County; the sheriff responds and the county magistrate hears tickets."),
    dict(slug="jedburg", name="Jedburg", county="Berkeley County", route="jedburg", court=None, label="I-26 exit 194",
         intro="Jedburg, around I-26 exit 194 and Jedburg Road, is a Berkeley County community with Summerville addresses, ten minutes from our office. Industrial growth along the interstate has brought new residents and new traffic—and Berkeley County paperwork for all of them.",
         angle=("Berkeley County estates and traffic cases", "A Jedburg estate is probated in Moncks Corner; a Highway Patrol stop on I-26 near exit 194 goes to the Berkeley County magistrate. We handle both, and we explain the county line to every new Jedburg client."),
         note="Jedburg is unincorporated; the Berkeley County Sheriff's Office responds."),
]


def facts_block(c):
    pl = PLACES.get(c["slug"])
    if not pl:
        return ""
    rows = []
    if pl.get("county_note"):
        rows.append(["County", esc(pl["county_note"])])
    else:
        rows.append(["County", esc(c["county"])])
    if pl.get("status"):
        rows.append(["Status", esc(pl["status"])])
    if pl.get("zips"):
        rows.append(["ZIP codes", esc(", ".join(pl["zips"]))])
    if pl.get("population"):
        rows.append(["Population (2020 census)", esc(pl["population"])])
    if pl.get("landmarks"):
        rows.append(["Landmarks", esc("; ".join(pl["landmarks"]))])
    trs = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows)
    return f'<h2>About {esc(c["name"])}</h2><div class="table-wrap"><table><tbody>{trs}</tbody></table></div>'


for c in CITIES:
    co = COUNTY[c["county"]]
    court_keys = [k for k in (co["probate"], co["probate_extra"], co["courthouse"], co["magistrate"], c["court"]) if k]
    r = ROUTES.get(c["route"], {})
    dist = f' The drive is about {esc(r["miles"])} miles and {esc(r["minutes"])} minutes in normal traffic.' if r.get("miles") else ""
    origin = esc(c["name"] + ", SC").replace(" ", "+")
    dir_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={DEST}"
    body = (
        f'<p>{c["intro"]}</p>'
        f'<h2>Where a {esc(c["name"])} case is heard</h2>'
        f'<p>{co["blurb"]}</p>'
        f'<p>{c["note"]}</p>'
        f'[[courts:{",".join(court_keys)}]]'
        f'<h2>{esc(c["angle"][0])}</h2><p>{c["angle"][1]}</p>'
        f'<h2>How we help {esc(c["name"])} families</h2>'
        + checks([
            f'<b>{A("estate-planning-attorney", "Estate planning")}</b> — wills, revocable trusts, powers of attorney and living wills drafted for South Carolina law and recorded in {esc(c["county"])} where required.',
            f'<b>{A("probate", "Probate and estate administration")}</b> — opening, administering and closing estates in the {esc(c["county"])} Probate Court, small-estate affidavits, and {A("executor-disputes", "disputes")} when they arise.',
            f'<b>{A("guardianship-and-conservatorship", "Guardianship and conservatorship")}</b> — for an aging parent or a minor, contested or not.',
            f'<b>{A("criminal-defense", "Criminal defense")}</b> — bond hearings at the {co["detention"]}, misdemeanors in magistrate and municipal court, and felonies in {esc(c["county"])} General Sessions, defended by a former officer.',
            f'<b>Personal injury</b> — car, truck and motorcycle crashes and dog bites, through {ext(firm.PI_SITE, "our dedicated injury site")}.',
        ]) +
        f'<h2>Getting to our office from {esc(c["name"])}</h2>'
        + (f'<p>{r["text"]}{dist}</p>' if r.get("text") else f'<p>We are at 128 Linwood Lane in Summerville, off the south side of town.{dist}</p>')
        + f'<p><a class="btn ghost sm" href="{dir_url}" rel="noopener" target="_blank">Directions from {esc(c["name"])} in Google Maps</a></p>'
        + facts_block(c)
        + band(f"Live in {c['name']}? Call Frost first.", "Consultations at our Summerville office, or by phone and video when the drive is not worth it.")
    )
    faqs = [
        (f"Which probate court handles an estate for a {c['name']} address?", f"The {c['county']} Probate Court in {co['seat']}. Estates are opened in the county where the person lived at death."),
        (f"Where is the bond hearing after an arrest in {c['name']}?", f"County arrests are heard at the {co['detention']}, usually within 24 hours. Municipal charges are heard by the municipal judge for that town." if c["court"] else f"At the {co['detention']}, usually within 24 hours of a warrant arrest."),
        (f"Do you meet clients in {c['name']}?", "Consultations are at our Summerville office or by phone and video. For estate-plan signings we can sometimes arrange a meeting closer to you; ask when you call."),
    ]
    title = f"{c['name']}, SC Estate Planning, Probate & Criminal Defense Attorneys"
    if len(title) > 70:
        title = f"{c['name']} Estate Planning, Probate & Criminal Defense Lawyers"
    desc = f"Estate planning, probate and criminal defense for {c['name']} families from Frost Law Group in Summerville: which {c['county']} courts hear your case and how to reach us."
    if len(desc) > 160:
        desc = f"Estate planning, probate and criminal defense for {c['name']} families from Frost Law Group: which courts hear your case and how to reach us."
    county_img = {"Dorchester County": "county-dorchester.jpg", "Berkeley County": "county-berkeley.jpg", "Charleston County": "county-charleston.jpg", "Colleton County": "county-colleton.jpg"}[c["county"]]
    page("service-areas/" + c["slug"], kind="city", county=c["county"], section_label=c["label"], hero_image=county_img, hero_caption=c["county"],
         title=title, description=desc,
         h1=f"Attorneys Serving {c['name']}, SC", eyebrow=f"Service area · {c['county']}", nav_label=c["name"],
         lead=f"Estate planning, probate, guardianship and criminal defense for {c['name']} families, from a husband-and-wife firm in Summerville.",
         body=body, faqs=faqs, related=["estate-planning-attorney", "probate", "criminal-defense"], priority=0.5)
