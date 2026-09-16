"""Core pages: home, team, attorney bios, contact, reviews, personal-injury hand-off, FAQ, privacy, indexes."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, section, band, esc, twocol
from . import firm
from . import local

PH = firm.PHONE
TEL = f'<a href="tel:{firm.PHONE_E164}">{PH}</a>'

# ----------------------------------------------------------------------------- HOME
# Rule from the client: the home page never mentions DUI. Criminal defense is described without it.

home_practice = (
    '<ul class="cards">'
    '<li class="card"><div class="icon"><svg viewBox="0 0 24 24"><path d="M4 4h12l4 4v12H4z"/><path d="M8 12h8M8 16h5"/></svg></div><h3><a href="[[estate-planning-attorney]]">Estate planning</a></h3>'
    '<p>Wills, revocable living trusts, powers of attorney and living wills, written for South Carolina law and your family—blended families, business owners and special-needs planning included.</p><a class="more" href="[[estate-planning-attorney]]">Estate planning services</a></li>'
    '<li class="card"><div class="icon"><svg viewBox="0 0 24 24"><path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/></svg></div><h3><a href="[[probate]]">Probate &amp; estate administration</a></h3>'
    '<p>Opening and settling an estate in Dorchester, Berkeley or Charleston County, executor guidance, small-estate affidavits, will contests, guardianship and conservatorship—from an attorney who sat as an associate probate judge.</p><a class="more" href="[[probate]]">Probate services</a></li>'
    '<li class="card"><div class="icon"><svg viewBox="0 0 24 24"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg></div><h3><a href="[[criminal-defense]]">Criminal defense</a></h3>'
    '<p>Drug charges, domestic violence, bond hearings, arrest warrants, traffic offenses and expungements in magistrate, municipal and General Sessions court—defended by a former detective who knows how cases are built.</p><a class="more" href="[[criminal-defense]]">Criminal defense services</a></li>'
    f'<li class="card"><div class="icon"><svg viewBox="0 0 24 24"><path d="M3 13l2-5h14l2 5v6H3z"/><circle cx="7.5" cy="16.5" r="1.5"/><circle cx="16.5" cy="16.5" r="1.5"/></svg></div><h3><a href="{firm.PI_SITE}" rel="noopener">Personal injury</a></h3>'
    f'<p>Car, truck and motorcycle crashes, dog bites and wrongful death claims are handled on our dedicated injury site, where Tara explains what to do before you talk to an insurance company.</p><a class="more" href="[[personal-injury]]">How injury cases work with us</a></li>'
    '</ul>')

home_ff = (
    '<div class="ff"><div><div class="word">Frost <span>First.</span></div></div><div>'
    '<p class="lead" style="color:#e6eef7">Two words that tell you exactly what to do. Before you sign the document, accept the offer, or answer the question—call Frost first.</p>'
    '<ul>'
    '<li><b>Before you sign.</b> A will printed off the internet, a deed change a relative suggested, a trust a seminar sold you. Let us read it first.</li>'
    '<li><b>Before you settle.</b> An estate that “seems simple,” a sibling who wants to divide things informally, an insurance adjuster with a number. Ask us first.</li>'
    '<li><b>Before you answer questions.</b> An investigator who “just wants your side,” a bench warrant you heard about, a citation with a court date. Talk to Jack first.</li>'
    '</ul>'
    f'<p style="margin:1.2rem 0 0;color:#cfdcea">One call. We tell you plainly whether you need a lawyer, what it would cost, and what to do in the meantime. {TEL}</p>'
    '</div></div>')

home_why = (
    '<ul class="cards three">'
    '<li class="card"><h3>Both sides of the system</h3><p>Jack spent fourteen years in law enforcement, from the Summerville Police Department to the Charleston County Sheriff\'s Office detective and SWAT ranks. Tara served as a Dorchester County Magistrate and then Associate Probate Judge. When we tell you how a case will be handled, it is because we have handled it from the other chair.</p></li>'
    '<li class="card"><h3>You talk to an attorney</h3><p>When you call, you reach Jack, Tara, or Cassie, our paralegal—people who know your file. Questions get answered the same day, in plain English.</p></li>'
    '<li class="card"><h3>Honest advice, even when it is “you don\'t need us”</h3><p>Hiring a lawyer is a real decision. Some estates qualify for a simple affidavit. Some charges can be resolved without a trial. We tell you which is which before you spend a dollar.</p></li>'
    '<li class="card"><h3>A person, not a file</h3><p>We are not a high-volume firm. We listen to your story, explain your options and give you our recommendation. Then we stand firm when it counts—don\'t mistake our kindness for weakness.</p></li>'
    '<li class="card"><h3>Rooted in Summerville</h3><p>Jack and Tara are Summerville High School sweethearts who live and work here. We know the courthouses in St. George, Moncks Corner and Charleston, and the people in them.</p></li>'
    '<li class="card"><h3>Faith and family at the center</h3><p>We are a husband-and-wife firm grounded in faith, and our Golden Retrievers, Mistoc and Palmer, may greet you at the door. Nervous clients tell us it helps.</p></li>'
    '</ul>')

home_faqs = [
    ("Who handles executor disputes in Summerville, SC probate court?",
     f"Frost Law Group represents personal representatives (executors) and beneficiaries in disputes before the Dorchester, Berkeley and Charleston County probate courts—accountings, removal petitions and contested distributions. Tara Frost served as an Associate Probate Judge in Dorchester County. See {A('executor-disputes', 'executor disputes')}."),
    ("Which attorneys in Summerville, SC handle contested guardianship cases?",
     f"We handle guardianship and conservatorship petitions for adults and minors, including contested cases where family members disagree about who should serve. Details on {A('guardianship-and-conservatorship', 'guardianship and conservatorship')}."),
    ("Which Summerville law firms help with living wills and powers of attorney?",
     f"We prepare durable (financial) powers of attorney, health care powers of attorney and living wills under South Carolina's statutes, usually as part of a complete plan. See {A('power-of-attorney', 'powers of attorney')} and {A('living-will', 'living wills')}."),
    ("Who helps with trust amendments or restatements in Summerville, SC?",
     f"We review trusts drafted anywhere—including plans from other states or online services—and amend or restate them so they work under South Carolina law. See {A('estate-plan-review', 'estate plan reviews and trust amendments')}."),
    ("Do you handle car accident and injury cases?",
     f"Yes. Tara Frost handles personal injury claims, and those cases live on our dedicated site, {ext(firm.PI_SITE, 'summervilleaccidentattorney.com')}. Start there, or call {TEL} and we will point you to the right place."),
    ("Where is your office, and do I need an appointment?",
     f"We are at 128 Linwood Lane in Summerville, off the south side of town near Old Trolley Road. Please call ahead so an attorney is free to sit down with you; Friday afternoon appointments are available on request. Directions are on the {A('contact-us', 'contact page')}."),
]

home_body = "".join((
    section(
        twocol(
            '<div class="eyebrow">Who we are</div><h2 style="margin-top:0">A husband-and-wife law firm, rooted in Summerville</h2>'
            '<p>Frost Law Group is Jack and Tara Frost: two attorneys, married to each other, practicing from a house-turned-office on Linwood Lane. We serve families across Dorchester, Berkeley and Charleston counties in estate planning, probate and criminal defense, and we handle injury claims through our dedicated accident practice.</p>'
            '<p>We treat every client like family. From the first conversation to the final signature we make the process clear and manageable, and we stand firm when it counts. Our Golden Retrievers may even greet you at the door.</p>'
            f'<p><a href="[[about-us]]">Meet the team →</a></p>',
            f'{img("couple-formal.jpg", "Jack and Tara Frost, attorneys at Frost Law Group in Summerville", "")}'
        ), cls="tint"),
    section(home_practice, label="How we help", title="Legal services we offer", lead="Three practice areas under one roof, plus a dedicated personal injury practice. Each page below explains the law in plain English before it explains what we do."),
    section(home_ff, cls="navy"),
    section(home_why, label="The Frost Law difference", title="Why families choose Frost Law Group"),
    section(
        f'<p class="lead">Rated {firm.RATING[0]} out of 5 on Google from {firm.RATING[1]} reviews. Here is some of what clients have said.</p>{"[[reviews:3]]"}'
        f'<div class="links"><a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Read our Google reviews</a><a href="{esc(firm.REVIEW_URL)}" rel="noopener" target="_blank">Leave a review</a><a href="{esc(firm.YELP_URL)}" rel="noopener" target="_blank">Find us on Yelp</a><a href="[[reviews]]">All client reviews</a></div>',
        cls="tint", label="Kind words", title="What our clients say"),
    section('[[team]]' + f'<p><a href="[[about-us]]">More about the team and how we work →</a></p>', label="The people behind the practice", title="Meet the team"),
    section('<div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in home_faqs) + f'</div><p><a href="[[faq]]">More questions and answers →</a></p>',
            cls="tint", label="Questions people ask", title="Straight answers to the questions Summerville families search for"),
    section(
        '<p>Our office is in Summerville, and we appear in the probate, magistrate, municipal and General Sessions courts of Dorchester, Berkeley and Charleston counties. Each community page explains which courthouse handles your matter and how to reach us from there.</p>'
        '<ul class="areas">' + "".join(f'<li><a href="[[{s}]]">{esc(n)}</a></li>' for s, n in [("service-areas/summerville", "Summerville"), ("service-areas/goose-creek", "Goose Creek"), ("service-areas/ladson", "Ladson"), ("service-areas/north-charleston", "North Charleston"), ("service-areas/moncks-corner", "Moncks Corner"), ("service-areas/hanahan", "Hanahan"), ("service-areas/charleston", "Charleston"), ("service-areas/mount-pleasant", "Mount Pleasant"), ("service-areas/ridgeville", "Ridgeville"), ("service-areas/st-george", "St. George"), ("service-areas/nexton", "Nexton"), ("service-areas/cane-bay", "Cane Bay")]) + '</ul>'
        '<p><a href="[[service-areas]]">All communities and courts we serve →</a></p>',
        label="Where we work", title="Serving Summerville and the tri-county Lowcountry"),
    section('[[postcards:blog/new-summerville-residents-estate-plan,blog/hurricane-season-documents-dorchester-county,blog/guardianship-aging-parent-summerville]]' + '<p><a href="[[blog]]">All articles →</a></p>',
            cls="tint", label="In the Know", title="Local news, explained by your lawyers"),
    section(
        '[[nap]]' + '[[map]]' + f'<p style="margin-top:1rem">{local.office_roads_sentence()}</p>' + '[[findus]]',
        label="Find us", title="128 Linwood Lane, Summerville", lead="Park in front, come to the door, and expect a wagging tail or two. If you are coming from out of town, the contact page has turn-by-turn directions from every community we serve."),
    section(band("Call Frost first.", "Tell us what happened. We will tell you the next step, what it costs, and whether you need us at all."), wrap=True),
))

page("home", kind="home", layout="raw",
     title="Summerville, SC Estate Planning, Probate & Criminal Defense Attorneys | Frost Law Group",
     description="Frost Law Group is a husband-and-wife law firm in Summerville, SC handling estate planning, probate and criminal defense for Dorchester, Berkeley and Charleston County families. Call (843) 419-6653.",
     h1="Estate Planning, Probate &amp; Criminal Defense Attorneys in Summerville, SC",
     kicker='<b>Frost First.</b> Before you sign, settle, or answer questions.',
     lead="A husband-and-wife firm at 128 Linwood Lane. Jack and Tara Frost help Lowcountry families protect what they have built, settle a loved one's estate, and face a charge with someone in their corner who knows the system from the inside.",
     quote="“Do justice, love kindness, and walk humbly with your God.” — Micah 6:8",
     hero_image="couple.jpg", hero_caption="Jack and Tara Frost with the Frost pups",
     body=home_body, priority=1.0, changefreq="weekly", nav_label="Home")

# ----------------------------------------------------------------------------- ABOUT / TEAM
about_body = (
    '<h2>Built on faith, family and fourteen years of knowing how the system works</h2>'
    '<p>Frost Law Group opened in 2019 as a two-attorney firm with a simple idea: people in a legal crisis should be able to talk to the lawyer, not a call center. Jack and Tara Frost are married, live in Summerville, and share an office on Linwood Lane with a paralegal, Cassie, and two Golden Retrievers who take their greeting duties seriously.</p>'
    '<p>Between them, they have seen the Lowcountry\'s legal system from almost every seat. Jack spent fourteen years as a Summerville police officer and then a Charleston County Sheriff\'s Office deputy, detective and SWAT team member before earning his law degree. Tara served as a Dorchester County Magistrate Judge from 2022 to 2025 and as a Dorchester County Associate Probate Judge from 2025 to 2026. That is why our advice tends to be specific: we know what the officer wrote down, what the judge will ask, and what the probate clerk will send back.</p>'
    '[[team]]'
    '<h2>How we divide the work</h2>'
    f'<p><b>Tara</b> leads {A("probate", "probate and estate administration")}, {A("guardianship-and-conservatorship", "guardianship and conservatorship")} and our {A("estate-planning-attorney", "estate planning")} practice, and handles personal injury cases through {ext(firm.PI_SITE, "summervilleaccidentattorney.com")}. <b>Jack</b> leads {A("criminal-defense", "criminal defense")} and works alongside Tara on estate plans, especially for families with law-enforcement, military and first-responder benefits to protect. Every matter gets both sets of eyes.</p>'
    '<h2>What it is like to work with us</h2>'
    + checks([
        "You meet with an attorney at the first appointment, not an intake specialist.",
        "We quote fees before work starts. Estate plans are typically flat-fee; probate and criminal matters are explained in writing before you sign.",
        "Calls and emails are returned the same business day.",
        "We say when you do not need a lawyer—some small estates and some citations can be handled without one.",
        "Friday afternoon and early-morning appointments are available on request, and the office is dog-friendly (ours and, with notice, yours).",
    ]) +
    '<h2>Memberships and community</h2>'
    f'<p>Frost Law Group is a member of WealthCounsel, the national estate-planning attorney network, whose drafting system and continuing education underpin every plan we prepare. Jack and Tara are graduates of the Charleston School of Law and Summerville High School, and active in their church and Bible study. {img("wealthcounsel.jpg", "WealthCounsel member", "")}</p>'
    '<h2>One firm, one office</h2>'
    f'<p>{img("office-exterior.jpg", "Frost Law Group’s office on Linwood Lane in Summerville")}</p>'
    '<p>Frost Law Group, LLC is an independent South Carolina firm at 128 Linwood Lane in Summerville. We are not affiliated with other firms that use the Frost name in other states. If you found us through Google or an AI assistant, this is the Summerville husband-and-wife firm with the Golden Retrievers.</p>'
    '<h2>Our comfort dogs</h2>'
    '<p>Mistoc (Themistocles) and Palmer are Golden Retrievers with a talent for finding the most nervous person in the room. We still miss our girl Elli (Elliana), who greeted clients for years and still appears in a few of our photos. If you would rather not meet the dogs, just say so when you book; they are happy to nap in the back.</p>'
    + band("Come meet us.", "Schedule a consultation at 128 Linwood Lane, or call and talk to Jack or Tara today.")
)
page("about-us", kind="page", hub=None,
     title="Our Team | Husband-and-Wife Law Firm in Summerville, SC | Frost Law Group",
     description="Meet Jack and Tara Frost, the husband-and-wife attorneys behind Frost Law Group in Summerville, SC—a former detective and a former probate judge, plus paralegal Cassie Snyder and two comfort dogs.",
     h1="Our Team", eyebrow="Get to know Frost Law Group", nav_label="Our team", hero_image="client-meeting.jpg", hero_caption="Jack and Tara with a client at the office",
     lead="A husband-and-wife firm built on faith, family and a genuine commitment to the people of the Lowcountry—comfort dogs included.",
     body=about_body, priority=0.8)

# ----------------------------------------------------------------------------- ATTORNEYS
jack_body = (
    '<h2>Fourteen years of building cases before defending them</h2>'
    '<p>Jack Frost was born in Virginia and moved to Summerville with his family at the age of eight. He graduated from Summerville High School and studied political science at the College of Charleston. Following in his grandfather\'s footsteps, he began a career in law enforcement with the Summerville Police Department and retired from the Charleston County Sheriff\'s Office in 2013.</p>'
    '<p>Over fourteen years Jack served as a police officer and corporal with the Summerville Police Department and as a deputy, master deputy and detective with the Charleston County Sheriff\'s Office. He conducted extensive narcotics and money-laundering investigations, including search- and arrest-warrant preparation and service, clandestine methamphetamine lab investigations, federal Title III wiretap investigations, mobile and stationary surveillance, and undercover operations. He was also an entry-team member of the Sheriff\'s Office SWAT team, with duties including dynamic entries, high-risk warrant service, fugitive apprehension, dignitary protection and firearms proficiency.</p>'
    '<h2>What that means for your case</h2>'
    + checks([
        "He reads an incident report the way the officer who wrote it intended—and sees what is missing.",
        "He knows how a traffic stop becomes a search, how a confidential informant is handled, and where warrants go wrong.",
        "He has testified in the same courtrooms where he now defends clients, before many of the same judges.",
        "He speaks the language of prosecutors and officers, which makes negotiating a better outcome faster and calmer.",
    ]) +
    '<h2>Education and credentials</h2>'
    + ul([
        "Juris Doctor, Charleston School of Law (2016)",
        "Admitted to the South Carolina Bar November 27, 2018; South Carolina Bar No. 103633, regular member in good standing (" + ext(firm.BAR_DIRECTORY_URL, "SC Judicial Branch attorney directory") + ")",
        "Town of Summerville DUI prosecutor, appointed November 2023 (" + ext("https://www.summervillepolice.com/m/newsflash/Home/Detail/106", "Town announcement") + ")",
        "Bachelor of Science in Criminal Justice and Police Administration, Strayer University",
        "Associate of Science in Criminal Justice, Trident Technical College",
        "Political science studies, College of Charleston",
        "Type 1 SWAT Operator designation, U.S. Department of Homeland Security",
        "DEA Basic Narcotics Investigations certification",
    ]) +
    '<h2>Prosecutor and defender</h2>'
    '<p>In November 2023 the Town of Summerville appointed Jack its DUI prosecutor, citing his years as a Charleston County narcotics detective and a Summerville police officer. Prosecuting impaired-driving cases for the Town means he sees the evidence, the video and the procedure from the State\'s side every week. Because of that role, the firm does not defend DUI charges brought by the Town of Summerville in Summerville Municipal Court; Jack defends those charges in the other courts of Dorchester, Berkeley and Charleston counties, and every other kind of criminal charge everywhere.</p>' +
    '<h2>Practice focus</h2>'
    f'<p>Jack leads the firm\'s {A("criminal-defense", "criminal defense practice")}: {A("drug-charges", "drug charges")}, {A("domestic-violence-defense", "domestic violence")}, {A("bond-hearings", "bond hearings")}, {A("arrest-warrants", "arrest warrants")}, {A("traffic-tickets", "traffic offenses")} and {A("expungements", "expungements")}, along with the alcohol-related driving charges described on the criminal defense page. He also works with Tara on {A("estate-planning-attorney", "estate plans")}, particularly for law-enforcement, military and first-responder families.</p>'
    '<h2>Off the clock</h2>'
    '<p>An avid golfer, Jack credits his attention to client service to his years as a caddy at the Ocean Course on Kiawah Island, where he also served as personal security for Tiger Woods and Vijay Singh during the 2012 PGA Championship. He and Tara, his Summerville High School sweetheart, live in Summerville with their Golden Retrievers.</p>'
    '<h2>Articles by Jack</h2><p>Jack writes the criminal-defense articles in [[blog]]—what a charge actually means, what happens at the first court date, and what to do before you talk to anyone.</p>'
    '<h2>Reach Jack</h2>'
    f'<p>Email <a href="mailto:{firm.ATTORNEYS["jack"]["email"]}">{firm.ATTORNEYS["jack"]["email"]}</a>, call {TEL}, or connect on {ext(firm.ATTORNEYS["jack"]["linkedin"], "LinkedIn")}. Please do not send details of a pending criminal case by email until we have spoken.</p>'
    + band("Facing a charge? Talk to Jack first.", "If your case requires experience, a steadfast resolve, or involves a complex investigation, call before you answer any questions.")
)
page("attorneys/jack-frost", kind="attorney", author="jack", hub="about-us",
     title="Jack C. Frost, Criminal Defense Attorney | Former Detective | Summerville, SC",
     description="Jack C. Frost is a Summerville, SC criminal defense and estate planning attorney who spent 14 years as a Summerville police officer and Charleston County Sheriff's Office detective and SWAT operator.",
     h1="Jack C. Frost", eyebrow="Attorney at Law", nav_label="Jack C. Frost",
     lead="Former Summerville police officer, Charleston County Sheriff's Office detective and SWAT operator, now defending the people he used to arrest—with an insider's understanding of how a case gets built.",
     hero_image="jack-bio.jpg", hero_caption="Jack C. Frost, Attorney at Law", body=jack_body, priority=0.8)

tara_body = (
    '<h2>From the bench to your side of the table</h2>'
    '<p>Tara L. Frost is a Summerville attorney whose practice centers on probate and estate administration, estate planning, guardianship and conservatorship, and personal injury. A lifelong resident of the tri-county area, she was born and raised locally, is married to her Summerville High School sweetheart Jack, and together they live and work in Summerville.</p>'
    '<p>Tara\'s background includes meaningful judicial service in Dorchester County. She served as a Dorchester County Magistrate Judge from July 2022 through August 2025, and then as a Dorchester County Associate Probate Judge from August 2025 through June 2026. That courtroom and judicial experience gives her a rare perspective on how estates, guardianships and contested matters are actually evaluated—what the court needs to see, which mistakes slow a file down, and how preparation and credibility decide close cases.</p>'
    '<p>Before becoming an attorney, Tara spent roughly sixteen years in the hospitality industry and later owned a window-covering company with her father. Those years taught her customer service, communication, and how to understand what people need during stressful times. Her personal motto—“Don\'t mistake my kindness for weakness”—describes how she approaches every case: with compassion and honesty, and with a firm hand when an opposing party or insurance company refuses to do what is right.</p>'
    '<h2>Education and credentials</h2>'
    + ul([
        "Juris Doctor, Charleston School of Law (2012)—Vice President of the Student Trial Lawyers Association; helped institute the law school's Trial Advocacy Board",
        "Admitted to the South Carolina Bar November 13, 2012; South Carolina Bar No. 100610, regular member in good standing (" + ext(firm.BAR_DIRECTORY_URL, "SC Judicial Branch attorney directory") + ")",
        "Dorchester County Associate Probate Judge, August 2025 – June 2026",
        "Dorchester County Magistrate Judge, July 2022 – August 2025",
        "WealthCounsel member firm (estate planning)",
    ]) +
    '<h2>Practice focus</h2>'
    f'<p>Tara leads {A("probate", "probate and estate administration")}, including {A("executor-duties", "guidance for personal representatives")}, {A("executor-disputes", "executor and beneficiary disputes")}, {A("will-contests", "will contests")} and {A("guardianship-and-conservatorship", "guardianship and conservatorship")}, and the firm\'s {A("estate-planning-attorney", "estate planning")} practice. Her personal injury work—car, truck and motorcycle crashes, dog bites and wrongful death—is on {ext(firm.PI_SITE, "summervilleaccidentattorney.com")}.</p>'
    '<h2>A note on her judicial service</h2>'
    '<p>Tara no longer serves on the bench and does not appear in matters she handled as a judge. What she brings to your case is an understanding of how probate and magistrate courts work in practice: the forms, the timelines, the hearings and the questions a judge is likely to ask.</p>'
    '<h2>Off the clock</h2>'
    '<p>Tara enjoys church and Bible study, reading, movies, swimming and fair-weather golf, and time with Jack, family and their Golden Retrievers, Mistoc and Palmer, who occasionally come to the office to greet clients with wagging tails.</p>'
    '<h2>Articles by Tara</h2><p>Tara writes the probate and estate-planning articles in [[blog]]—what to do in the first weeks after a death, how guardianship works for an aging parent, and what new Summerville residents should update.</p>'
    '<h2>Reach Tara</h2>'
    f'<p>Email <a href="mailto:{firm.ATTORNEYS["tara"]["email"]}">{firm.ATTORNEYS["tara"]["email"]}</a>, call {TEL}, or connect on {ext(firm.ATTORNEYS["tara"]["linkedin"], "LinkedIn")}.</p>'
    + band("Settling an estate or planning one?", "Tara will tell you what the probate court will need and what you can do yourself.")
)
page("attorneys/tara-frost", kind="attorney", author="tara", hub="about-us",
     title="Tara L. Frost, Probate & Estate Planning Attorney | Former Probate Judge | Summerville, SC",
     description="Tara L. Frost is a Summerville, SC probate, estate planning and personal injury attorney who served as a Dorchester County Magistrate Judge (2022–2025) and Associate Probate Judge (2025–2026).",
     h1="Tara L. Frost", eyebrow="Attorney at Law", nav_label="Tara L. Frost",
     lead="Former Dorchester County Magistrate and Associate Probate Judge, now guiding families through probate, guardianship and estate planning with a judge's eye for what the court needs.",
     hero_image="tara-bio.jpg", hero_caption="Tara L. Frost, Attorney at Law", body=tara_body, priority=0.8)

# ----------------------------------------------------------------------------- CONTACT
contact_form = (
    f'<form class="form" method="POST" action="{esc(firm.FORM_ENDPOINT)}" accept-charset="UTF-8" data-contact>'
    f'<input type="hidden" name="_subject" id="f-subject" value="Website inquiry">'
    f'<input type="hidden" name="_next" value="{firm.ORIGIN}/thank-you/">'
    '<div class="row"><label>Your name<input type="text" name="name" id="f-name" autocomplete="name" required></label>'
    '<label>Phone<input type="tel" name="phone" id="f-phone" autocomplete="tel" required></label></div>'
    '<label>Email<input type="email" name="email" id="f-email" autocomplete="email"></label>'
    '<label>What do you need help with?<select name="topic" id="f-topic"><option>Estate planning</option><option>Probate or estate administration</option><option>Guardianship or conservatorship</option><option>Criminal charge or warrant</option><option>Traffic ticket</option><option>Injury claim</option><option>Something else</option></select></label>'
    '<label>Tell us briefly what happened<textarea name="message" id="f-message" required></textarea></label>'
    '<label class="hp" aria-hidden="true">Leave this field empty<input type="text" name="_gotcha" id="f-gotcha" tabindex="-1" autocomplete="off"></label>'
    '<p class="fine">Please do not include confidential details about a criminal case in this form; call instead. Sending a message does not create an attorney-client relationship until we agree in writing to represent you.</p>'
    '<div><button class="btn" type="submit">Send message</button></div></form>')

contact_body = (
    section('[[nap]]' + f'<div class="nap"><div><h3>Email</h3><p><a href="mailto:{firm.ATTORNEYS["jack"]["email"]}">{firm.ATTORNEYS["jack"]["email"]}</a><br><a href="mailto:{firm.ATTORNEYS["tara"]["email"]}">{firm.ATTORNEYS["tara"]["email"]}</a></p><p class="small">For a new matter, a call gets a faster answer.</p></div><div><h3>Mail</h3><p>{firm.NAME}<br>{firm.PO_BOX}</p><p class="small">Please send documents to the P.O. Box, and come to Linwood Lane in person.</p></div><div><h3>Attorneys</h3><p><a href="[[attorneys/jack-frost]]">Jack C. Frost</a>, SC Bar No. 103633<br><a href="[[attorneys/tara-frost]]">Tara L. Frost</a>, SC Bar No. 100610</p></div></div>' + '[[map]]', wrap=True),
    section(
        f'<p class="lead">{local.office_roads_sentence() or "Linwood Lane is a short residential street in Summerville; the office is the house with our sign out front."}</p>'
        + local.directions_cards(["i26-199", "goose-creek", "ladson", "moncks-corner", "north-charleston", "charleston", "st-george", "ridgeville", "knightsville", "nexton", "cane-bay", "mount-pleasant"])
        + f'<p><a class="btn ghost sm" href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Open turn-by-turn directions in Google Maps</a></p>',
        cls="tint", label="Directions", title="Getting here on local roads", lead="Written for people who know the area by road names, not GPS pins."),
    section(
        twocol(
            '<h3 style="margin-top:0">What to expect at your first visit</h3>' + checks([
                "Free parking in front of the office; the entrance is at ground level.",
                "You will meet with Jack or Tara, not an intake assistant.",
                "Bring what you have: the will or trust, the death certificate, the citation, the bond paperwork or the letter that prompted the call. Photos on your phone are fine.",
                "Consultations are scheduled so an attorney has uninterrupted time; please call ahead rather than dropping in.",
                "Our Golden Retrievers may say hello. Tell us when you book if you would prefer they stay in the back.",
            ]) + f'<p>{img("office-exterior.jpg", "The Frost Law Group office at 128 Linwood Lane, Summerville", "")}</p>',
            '<h3 style="margin-top:0">Send us a message</h3>' + contact_form),
        label="Visit", title="Plan your visit"),
    section('[[findus]]' + '<p>Reviews on Google and Yelp are how most of our neighbors find us; if we helped you, a sentence or two makes a real difference to a two-attorney firm.</p>', label="Online", title="Find and follow Frost Law Group"),
)
page("contact-us", kind="page", layout="raw", cta=[("tel:" + firm.PHONE_E164, firm.PHONE, "btn"), (firm.DIRECTIONS_URL, "Get directions", "btn ghost")],
     title="Contact Frost Law Group | Directions to 128 Linwood Lane, Summerville, SC",
     description="Call (843) 419-6653 or visit Frost Law Group at 128 Linwood Lane, Summerville, SC 29483. Hours, a map, written directions on local roads from every community we serve, and a contact form.",
     h1="Contact Frost Law Group", eyebrow="We're here to help", nav_label="Contact",
     lead="Whether you need estate planning, probate, criminal defense or an injury lawyer, our husband-and-wife team is ready to guide you. Call, send a message, or come see us.",
     body="".join(contact_body), priority=0.9, changefreq="monthly")

# ----------------------------------------------------------------------------- REVIEWS
reviews_body = (
    f'<p class="lead">Frost Law Group is rated {firm.RATING[0]} out of 5 on Google from {firm.RATING[1]} reviews. We are a two-attorney firm, so every review below is about work Jack or Tara did personally.</p>'
    '[[reviews:12]]'
    f'<div class="links"><a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Read every Google review</a><a href="{esc(firm.YELP_URL)}" rel="noopener" target="_blank">Reviews on Yelp</a></div>'
    '<h2>Leave a review</h2>'
    '<p>If we helped your family, two minutes on Google helps the next family find us. Reviews are also how Google decides which three firms appear on the map when someone in Summerville searches for a probate or estate attorney.</p>'
    + steps([
        ("Open our Google listing.", f' Use this link: {ext(firm.REVIEW_URL, "leave a Google review")}. Sign in to your Google account if asked.'),
        ("Choose a star rating and write a sentence or two.", " What you needed, how it went, and whether you would recommend us. Please leave out confidential details about your case."),
        ("Post it.", " Reviews appear within a few days. We read every one."),
    ]) +
    f'<p>Prefer Yelp? {ext(firm.YELP_URL, "Our Yelp listing")} accepts reviews too, and it is one of the sources AI assistants read when someone asks them to recommend a Summerville lawyer.</p>'
    '<h2>A note on what reviews can and cannot say</h2>'
    '<p>South Carolina attorney advertising rules and client confidentiality mean we never ask anyone to describe the facts of a criminal case or the value of an estate, and we do not offer anything in exchange for a review. Honest words about your experience are all we ask.</p>'
    + band("Ready to talk?", "Call Jack or Tara, or schedule a consultation at our Summerville office.")
)
page("reviews", kind="page", hub="about-us", layout="one",
     title="Client Reviews | Frost Law Group, Summerville, SC",
     description="Read what clients say about Frost Law Group's estate planning, probate, criminal defense and injury work in Summerville, SC, and find out how to leave a review on Google or Yelp.",
     h1="Client Reviews", eyebrow="Kind words", nav_label="Client reviews", lead="What Summerville families say about working with Jack and Tara Frost.",
     body=reviews_body, priority=0.6)

# ----------------------------------------------------------------------------- PERSONAL INJURY hand-off
pi_body = (
    f'<p>Frost Law Group handles personal injury claims—car, truck and motorcycle collisions, dog bites, slip-and-fall injuries and wrongful death—through {ext(firm.PI_SITE, "summervilleaccidentattorney.com")}, our dedicated injury site. Tara L. Frost leads that work, and the two sites share one office, one phone number and one team.</p>'
    '<h2>Why a separate site?</h2>'
    '<p>Injury clients need different information than an executor or a family planning an estate: what to say to an insurance adjuster, how medical bills get paid while a claim is open, what a case is worth and how long it takes. Keeping that material on its own site keeps both sites clear.</p>'
    '<h2>Start here</h2>'
    + checks([
        f'{ext(firm.PI_SITE, "Summerville accident and injury attorneys")} — the main injury site, with pages on each type of case.',
        f'Call {TEL}. If you have just been in a crash, do it before you give a recorded statement to any insurance company.',
        'Bring the police report number, photos, the other driver\'s insurance information and your medical paperwork to the first meeting.',
    ]) +
    '<h2>What Tara brings to an injury claim</h2>'
    '<p>Tara served as a Dorchester County Magistrate Judge, where civil claims are tried and evidence is weighed every week. Insurance companies know which firms prepare cases for trial; that reputation is what moves a settlement number.</p>'
    + band("Hurt in a crash?", "Call before you talk to the insurance company. The first conversation shapes everything after it.", primary=("contact-us", "Contact us"))
)
page("personal-injury", kind="page", layout="one", cta=[(firm.PI_SITE, "Go to our injury site", "btn"), ("tel:" + firm.PHONE_E164, firm.PHONE, "btn ghost")],
     title="Personal Injury | Frost Law Group's Dedicated Injury Practice | Summerville, SC",
     description="Frost Law Group handles car, truck and motorcycle crash, dog bite and wrongful death claims through its dedicated injury site, summervilleaccidentattorney.com. Here is how the two sites work together.",
     h1="Personal Injury Cases", eyebrow="Handled on our dedicated injury site", nav_label="Personal injury",
     lead="Tara Frost's injury practice lives at summervilleaccidentattorney.com. Same office, same phone number, same team.",
     body=pi_body, priority=0.5)

# ----------------------------------------------------------------------------- FAQ
faq_groups = [
    ("Estate planning", [
        ("Do I need a will if I don't have much?", f"Yes. A will names who receives what, who serves as personal representative, and—most importantly for parents—who raises minor children. Without one, South Carolina's intestacy statute decides. See {A('dying-without-a-will-in-south-carolina', 'what happens without a will')}."),
        ("Will or trust—which do I need?", f"Most Summerville families are well served by a will plus powers of attorney; a revocable living trust adds privacy, incapacity planning and probate avoidance, and makes the most sense when you own real estate in more than one state or want to avoid the probate process altogether. {A('revocable-trust', 'Revocable trusts explained')}."),
        ("Can you review a trust I already have?", f"Yes, including plans drafted in another state or by an online service. We check that it works under South Carolina law, that it is funded, and that it still matches your family. {A('estate-plan-review', 'Plan reviews, amendments and restatements')}."),
        ("What does an estate plan cost?", f"We quote a flat fee at the first meeting once we know what you need. {A('estate-planning-costs', 'What drives the price')}."),
    ]),
    ("Probate", [
        ("Does every estate go through probate in South Carolina?", f"No. Assets with beneficiary designations, joint ownership with survivorship, and assets held in a funded trust pass outside probate, and small estates can use an affidavit. {A('small-estate-affidavit', 'Small estate affidavits')}."),
        ("How long does probate take?", f"An uncontested South Carolina estate usually takes eight months to a year, because creditors have eight months from the first published notice to file claims. Disputes, real estate sales and tax issues add time. {A('probate-process', 'The probate process step by step')}."),
        ("Which probate court handles my parent's estate?", f"The probate court of the county where your parent lived at death—Dorchester County for Summerville addresses, Berkeley County for Goose Creek and Moncks Corner, Charleston County for North Charleston, Charleston and Mount Pleasant. {A('probate-courts', 'Our guide to the three courts')}."),
        ("Who handles executor disputes in Summerville, SC probate court?", f"We represent both personal representatives and beneficiaries in accountings, removal petitions and contested distributions in the Dorchester, Berkeley and Charleston County probate courts. {A('executor-disputes', 'Executor disputes')}."),
        ("Which attorneys in Summerville, SC handle contested guardianship cases?", f"Frost Law Group handles guardianship and conservatorship for adults and minors, including contested cases. Tara Frost served as an Associate Probate Judge in Dorchester County, where these cases are heard. {A('guardianship-and-conservatorship', 'Guardianship and conservatorship')}."),
    ]),
    ("Criminal defense", [
        ("I was arrested—what happens first?", f"A bond hearing, normally within 24 hours, before a magistrate or municipal judge. Having a lawyer there changes what you say and often the bond amount. {A('bond-hearings', 'Bond hearings')}."),
        ("Should I talk to the investigator who called me?", "Not before you talk to a lawyer. Officers can and do use a friendly conversation to complete a case. Call Jack first; the call is confidential."),
        ("Can I get my record cleared?", f"Many first-offense convictions and all dismissed or not-guilty charges can be expunged in South Carolina. {A('expungements', 'Who qualifies for expungement')}."),
        ("Do you handle federal cases?", "Jack handles state charges in magistrate, municipal and General Sessions court. For federal matters we will refer you to a federal practitioner we trust."),
    ]),
    ("Working with us", [
        ("Do you offer free consultations?", "Injury consultations are free. For estate planning, probate and criminal matters, call us—we will tell you on the phone whether a paid consultation makes sense for your situation and what it costs."),
        ("Where are you and what are your hours?", f"128 Linwood Lane, Summerville, SC 29483. Monday–Thursday 9–5, Friday 9–12, with Friday afternoon appointments on request. {A('contact-us', 'Directions and a map')}."),
        ("Which areas do you serve?", f"Summerville and all of Dorchester, Berkeley and Charleston counties, with clients from Colleton County as well. {A('service-areas', 'Communities we serve')}."),
    ]),
]
faq_body = "".join(f'<h2>{esc(g)}</h2><div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in items) + "</div>" for g, items in faq_groups)
faq_body += band("Didn't find your question?", "Call us. Most questions take five minutes to answer.")
all_faqs = [qa for _, items in faq_groups for qa in items]
page("faq", kind="page", hub="about-us", layout="two",
     title="Frequently Asked Questions | Frost Law Group, Summerville, SC",
     description="Plain-English answers to the questions Summerville families ask about wills, trusts, probate, guardianship, criminal charges and working with Frost Law Group.",
     h1="Frequently Asked Questions", eyebrow="Straight answers", nav_label="Frequently asked questions",
     lead="Short answers first, with a link to the page that goes deeper.", body=faq_body, faqs=[], priority=0.5)
# Use the grouped questions as FAQ schema on this page without repeating the accordion.
from .base import BY_SLUG as _BS  # noqa: E402
_BS["faq"]["faqs"] = []
_BS["faq"]["_faq_schema"] = all_faqs

# ----------------------------------------------------------------------------- SERVICE AREAS index
sa_body = (
    '<p class="lead">Frost Law Group is in Summerville, and we appear in the probate, magistrate, municipal and General Sessions courts of Dorchester, Berkeley and Charleston counties. Which courthouse handles your matter depends on where you live and, for a criminal charge, where it happened. Each community page below explains that and gives directions to our office on local roads.</p>'
    '[[citylist]]'
    '<h2>The courts we appear in</h2>'
    '[[courts:dorchester_probate,dorchester_courthouse,dorchester_magistrate_summerville,summerville_municipal,dorchester_detention,berkeley_probate,berkeley_courthouse,hill_finklea,charleston_probate,charleston_judicial,al_cannon,north_charleston_municipal,goose_creek_municipal,colleton_probate]]'
    + band("Not on the list?", "We take cases throughout the Lowcountry. Call and ask.")
)
page("service-areas", kind="page", layout="one",
     title="Areas We Serve | Dorchester, Berkeley & Charleston County, SC | Frost Law Group",
     description="Frost Law Group serves Summerville, Goose Creek, Ladson, North Charleston, Moncks Corner, Charleston and the rest of Dorchester, Berkeley and Charleston counties. Find your community and its courts.",
     h1="Communities and Courts We Serve", eyebrow="Where we work", nav_label="Service areas", hero_image="summerville-downtown.jpg", hero_caption="Downtown Summerville",
     lead="One office in Summerville; clients from every corner of the tri-county area.", body=sa_body, priority=0.6)

# ----------------------------------------------------------------------------- BLOG index
blog_body = (
    '<p class="lead">Local news raises legal questions—a new subdivision, a hurricane forecast, a change in state law, a story about an estate dispute. Jack writes about criminal defense; Tara writes about probate and estate planning. Each article answers the question people are actually asking on Nextdoor, Reddit and Google, and links to the news source so you can read the original.</p>'
    f'<div class="links"><a href="{esc(firm.PREFERRED_SOURCE_URL)}" rel="noopener" target="_blank">Add Frost Law Group as a preferred source on Google</a><a href="{esc(firm.FACEBOOK)}" rel="noopener" target="_blank">Follow on Facebook</a><a href="{esc(firm.INSTAGRAM)}" rel="noopener" target="_blank">Follow on Instagram</a></div>'
    '[[latestposts:40]]'
    + band("Have a question the news raised?", "Send it to us. If it is one other families are asking, we will write the answer.")
)
page("blog", kind="page", layout="one", changefreq="weekly",
     title="In the Know | Local News Explained by Summerville Attorneys | Frost Law Group",
     description="Frost Law Group's blog explains what Lowcountry news means for your estate plan, a probate case, or a criminal charge—written by attorneys Jack and Tara Frost with links to the original reporting.",
     h1="In the Know", eyebrow="Insights and articles", nav_label="In the Know",
     lead="Guidance from Jack and Tara Frost on estate planning, probate and criminal defense, prompted by what is in the local news.", body=blog_body, priority=0.7)

# ----------------------------------------------------------------------------- PRIVACY
privacy_body = (
    '<p>Frost Law Group, LLC (“we”) respects your privacy. This policy explains what information this website collects and how it is used. It applies to frostlawgroupsc.com; our injury site has its own policy.</p>'
    '<h2>What we collect</h2>'
    + ul([
        "<b>Information you send us.</b> When you use the contact form or call, you give us your name, contact details and a description of your matter. We use it only to respond to you and, if you hire us, to represent you. Contact-form submissions are delivered to us through Formspree, a form-processing service that stores them on our behalf under its own privacy policy.",
        "<b>Website analytics.</b> We may use privacy-respecting analytics to understand which pages are read. Analytics data is aggregated and is not used to identify you.",
        "<b>Embedded maps.</b> The map on our contact page loads from Google only after you click to load it. Google's privacy policy applies to that map.",
    ]) +
    '<h2>What we do not do</h2>'
    '<p>We do not sell or rent personal information, and we do not share what you tell us with anyone outside the firm except as needed to provide legal services or as required by law. Communications through this website are not privileged until we agree to represent you, so please do not send confidential details about a criminal matter through the form.</p>'
    '<h2>Cookies and links</h2>'
    '<p>This site sets no advertising cookies. Links to Google, Yelp, Facebook, Instagram, news outlets and government sites take you to those organizations\' own sites and policies.</p>'
    '<h2>Questions</h2>'
    f'<p>Write to Frost Law Group, LLC, {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}, or call {TEL}. Policy updated {firm.BUILD_DATE[:4]}.</p>'
)
page("privacy-policy", kind="page", layout="one", cta=False, priority=0.1,
     title="Privacy Policy | Frost Law Group, Summerville, SC",
     description="How Frost Law Group's website handles the information you share through its contact form, analytics and embedded maps, and what we do not do with it.",
     h1="Privacy Policy", eyebrow="Your information", nav_label="Privacy policy", lead="", body=privacy_body)

# ----------------------------------------------------------------------------- TERMS OF USE & LEGAL DISCLAIMER
terms_body = (
    '<p>These terms govern your use of frostlawgroupsc.com (the “site”), which is operated by Frost Law Group, LLC, a South Carolina law firm at 128 Linwood Lane, Summerville, SC 29483. By using the site you agree to them. If you do not, please do not use the site.</p>'
    '<h2>Information, not legal advice</h2>'
    '<p>Everything on this site—practice-area pages, service-area pages, articles, answers to common questions—is general information about South Carolina law as we understand it on the date it was written. It is not legal advice, it may not reflect the most recent changes in the law, and it does not address the facts of your situation. Do not act or refrain from acting because of something you read here without talking to a licensed South Carolina attorney about your own circumstances.</p>'
    '<h2>No attorney-client relationship</h2>'
    '<p>Reading this site, calling our office, sending a message through the contact form, or emailing an attorney does not make you a client of Frost Law Group. An attorney-client relationship is created only when we have checked for conflicts of interest and both you and the firm have signed a written engagement agreement. Until then, we may be unable to represent you, and we may represent someone whose interests differ from yours.</p>'
    '<h2>Please do not send confidential information yet</h2>'
    '<p>Because no attorney-client relationship exists until an engagement agreement is signed, information you send through the site or by email before then may not be treated as confidential or privileged. Please keep initial messages to your name, contact details and a general description of the matter, and do not include details of a pending criminal case. We will tell you when it is safe to share more.</p>'
    '<h2>No guarantee of results</h2>'
    '<p>Descriptions of our practice areas and experience, and any client reviews quoted on the site, describe past matters. Any result we achieved for another client does not indicate that a similar result can be obtained for you. Every case depends on its own facts and on the law in force at the time.</p>'
    '<h2>Client reviews and testimonials</h2>'
    '<p>Reviews quoted on the site are the words of clients as they wrote them on Google, Yelp or directly to the firm, edited only for length. They reflect those clients\' experiences and are not a promise of a particular outcome or level of service in your matter. We do not pay for reviews.</p>'
    '<h2>Attorney advertising</h2>'
    '<p>This site is attorney advertising under the South Carolina Rules of Professional Conduct. The attorneys responsible for its content are Jack C. Frost and Tara L. Frost, Frost Law Group, LLC, 128 Linwood Lane, Summerville, South Carolina 29483, (843) 419-6653. Both are licensed to practice law in South Carolina only. Jack and Tara Frost do not claim certification as specialists in any field; South Carolina does not recognize specialties in the practice areas described on this site.</p>'
    '<h2>Links to other sites</h2>'
    '<p>We link to court, county and state websites, news outlets, community forums and our own injury-practice site, summervilleaccidentattorney.com, because we think they are useful. We do not control those sites, we are not responsible for their content or their privacy practices, and a link is not an endorsement. Community forums such as Nextdoor and Reddit contain opinions of their users, not of the firm.</p>'
    '<h2>Accuracy and changes</h2>'
    '<p>We work to keep the site accurate, and we cite the statute or official source for the legal statements we make. Laws, court addresses, fees and procedures change, and we may not update every page immediately. We may change or remove any content, and these terms, at any time without notice.</p>'
    '<h2>Intellectual property</h2>'
    '<p>The text, design and images on this site belong to Frost Law Group, LLC or are used with permission. You may print or share pages for personal, non-commercial use with attribution. You may not copy the site\'s content for another website or commercial purpose without written permission.</p>'
    '<h2>Limitation of liability</h2>'
    '<p>The site is provided “as is.” To the fullest extent the law allows, Frost Law Group, LLC and its attorneys and staff are not liable for any loss arising from your use of, or reliance on, the site or any site linked from it, including interruptions, errors or omissions.</p>'
    '<h2>Governing law</h2>'
    '<p>These terms are governed by the laws of the State of South Carolina, without regard to conflict-of-law rules. Any dispute about the site will be heard in the state courts of Dorchester County, South Carolina.</p>'
    '<h2>Questions</h2>'
    f'<p>Write to Frost Law Group, LLC, {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}, or call {TEL}. Our {A("privacy-policy", "privacy policy")} explains how we handle information you share through the site. Terms last updated September {firm.BUILD_DATE[:4]}.</p>'
)
page("terms-of-use", kind="page", layout="one", cta=False, priority=0.1,
     title="Terms of Use & Legal Disclaimer | Frost Law Group, Summerville SC",
     description="The terms that govern use of frostlawgroupsc.com: no legal advice, no attorney-client relationship until an engagement agreement, attorney advertising notice, results and review disclaimers, governing law.",
     h1="Terms of Use &amp; Legal Disclaimer", eyebrow="Please read", nav_label="Terms of use", lead="What this site is, what it is not, and the rules for using it.", body=terms_body)

# ----------------------------------------------------------------------------- ACCESSIBILITY STATEMENT
access_body = (
    '<p>Frost Law Group wants every visitor—including people who use screen readers, keyboard navigation, magnification or voice control—to be able to read this site and reach us. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at level AA.</p>'
    '<h2>What we have done</h2>'
    + checks([
        "Every page is built with semantic HTML: one heading per page, ordered headings, real lists, tables with header cells, and landmarks for the header, navigation, main content and footer.",
        "The whole site works with a keyboard. A “Skip to content” link appears on the first Tab press, focus is always visible, and the menus open on focus as well as hover.",
        "Text and background colors meet WCAG contrast ratios, text resizes with your browser or device settings, and nothing depends on color alone.",
        "Images carry descriptive alternative text; decorative graphics are hidden from assistive technology.",
        "Forms have visible labels tied to their fields, and errors are described in text.",
        "There is no autoplaying media or flashing content, and animations are disabled for visitors who have asked their device to reduce motion.",
        "Pages are light and work on slow connections and small screens; the site does not require JavaScript to read.",
    ]) +
    '<h2>Known limitations</h2>'
    + checks([
        "The interactive map on the contact page is provided by Google and loads only when you choose it; its accessibility is Google's. The written directions and address on the same page carry the same information as text.",
        "Some links lead to court, county and state websites and to documents (often PDFs) we do not control.",
    ]) +
    '<h2>Our office</h2>'
    '<p>Our office at 128 Linwood Lane has free parking directly in front and a ground-level entrance. If you have a mobility, hearing, vision or other need, tell us when you book and we will make arrangements—including meeting by phone or video, providing documents in large print, or allowing extra time. Our comfort dogs stay in the back on request.</p>'
    '<h2>Tell us if something does not work</h2>'
    f'<p>If any part of this site is hard to use, or you need information in another format, call {TEL} or use the {A("contact-us", "contact form")}. Tell us the page and what happened; we will fix what we can and send you the information another way in the meantime. This statement was last reviewed in September {firm.BUILD_DATE[:4]}.</p>'
)
page("accessibility", kind="page", layout="one", cta=False, priority=0.1,
     title="Accessibility Statement | Frost Law Group, Summerville SC",
     description="Frost Law Group's commitment to an accessible website and office: WCAG 2.1 AA measures, known limitations, accommodations at our Summerville office, and how to report a problem.",
     h1="Accessibility Statement", eyebrow="For every visitor", nav_label="Accessibility", lead="How this site is built to be usable by everyone, and how to reach us if it is not.", body=access_body)


# ----------------------------------------------------------------------------- THANK YOU (form landing page, not indexed)
thanks_body = (
    '<p class="lead">Your message is on its way to Jack, Tara and Cassie. We read every one and reply by phone or email as soon as we can, usually the next business day.</p>'
    '<h2>If it cannot wait</h2>'
    f'<p>Call {TEL}. If someone has been arrested, a bond hearing is usually held within 24 hours, so please call rather than wait for a reply.</p>'
    '<h2>While you wait</h2>'
    + checks([
        f'{A("probate-process", "How probate works in South Carolina")}, step by step.',
        f'{A("estate-planning-attorney", "What a complete estate plan includes")} and what it costs.',
        f'{A("criminal-defense", "What to do right now")} if you or a family member has been charged.',
        f'{A("contact-us", "Directions to the office")} on local roads, and what to bring.',
    ])
    + '<p class="small">Sending a message does not create an attorney-client relationship, and please do not email details of a pending criminal case until we have spoken.</p>'
)
page("thank-you", kind="page", layout="one", cta=False, noindex=True, priority=0.1,
     title="Thank You | Frost Law Group, Summerville SC",
     description="We received your message and will reply as soon as we can, usually the next business day. For urgent matters, call (843) 419-6653.",
     h1="Thank you. We have your message.", eyebrow="Message received", nav_label="Thank you", lead="", body=thanks_body)
