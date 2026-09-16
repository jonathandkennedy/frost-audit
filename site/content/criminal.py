"""Criminal defense hub and spokes. The DUI page exists but is linked only from this hub and its siblings,
never from the global navigation, footer or home page (client instruction)."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
from . import firm
from .local import cite, link

HUB = "criminal-defense"
TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'


def sp(slug, **kw):
    kw.setdefault("kind", "spoke")
    kw.setdefault("hub", HUB)
    kw.setdefault("eyebrow", "Criminal defense · Summerville, SC")
    return page(slug, **kw)


hub_body = (
    '<h2>Defense from someone who built cases for fourteen years</h2>'
    '<p>Jack Frost was a Summerville police officer and a Charleston County Sheriff\'s Office detective, narcotics investigator and SWAT operator before he became a lawyer. He has written the warrants, run the surveillance, handled the informants and testified in the courtrooms where he now defends clients. That background is not a slogan; it is how he finds the weak point in a case.</p>'
    '<p>We handle charges in the magistrate and municipal courts of Summerville, Dorchester, Berkeley and Charleston counties and in General Sessions (circuit) court, for adults and, in appropriate cases, juveniles and young adults facing their first charge.</p>'
    '<h2>Charges we defend</h2>'
    '[[cards:drug-charges,domestic-violence-defense,dui-lawyer-summerville-sc,traffic-tickets]]'
    '<h2>Getting out, getting ahead, and cleaning up</h2>'
    '[[cards:bond-hearings,arrest-warrants,expungements]]'
    '<p>We also defend assault and battery, shoplifting and other theft charges, disorderly conduct and open container cases, weapons charges, and probation violations. If your charge is not listed, call—if we cannot take it, we will tell you who should.</p>'
    '<h2>What to do right now</h2>'
    + steps([
        ("Stop talking about the case.", " Not to the officer, not to the “victim,” not on social media, not on a recorded jail phone. Everything you say is evidence, and a friendly conversation is the most common way a case gets finished."),
        ("Write down what happened.", " Times, places, names, what was said and by whom—while it is fresh. Keep it for your lawyer only."),
        ("Keep every piece of paper.", " The ticket, the bond paperwork, the incident report number, the court date. Photograph them."),
        ("Call before the first court date.", " Bond conditions, a no-contact order, or a missed date can create new problems before the original charge is even addressed."),
    ]) +
    '<h2>How a South Carolina criminal case moves</h2>'
    + steps([
        ("Arrest or citation.", " A uniform traffic ticket or a warrant. Some charges start with a courtesy summons rather than an arrest."),
        ("Bond hearing.", f" Usually within 24 hours of a warrant arrest, before a magistrate or municipal judge. {A('bond-hearings', 'What happens at a bond hearing')}."),
        ("Which court.", " Magistrate and municipal courts handle most misdemeanors with penalties up to 30 days in jail (and specific offenses the legislature assigned to them, such as third-degree domestic violence). Everything heavier goes to General Sessions."),
        ("Discovery and investigation.", " We obtain the incident report, body-camera and dash-camera video, lab results and witness statements—and we investigate on our own."),
        ("Resolution.", " Dismissal, diversion (pretrial intervention, conditional discharge, traffic education), a negotiated plea to a lesser charge, or trial. Most cases resolve before trial; the ones that do not are prepared as if they will."),
    ]) +
    '<h2>Why clients choose Jack</h2>'
    + checks(["He reads reports and video the way the officer wrote and recorded them, and sees what is missing.",
              "He knows the prosecutors, officers and judges in Dorchester, Berkeley and Charleston counties, which makes negotiation faster and calmer.",
              "He is direct about the likely outcomes and the cost, and he returns calls.",
              "A conviction follows you for employment, housing, licensing and immigration; his goal from day one is the resolution that leaves the smallest mark."]) +
    band("Facing charges? Let's talk today.", "A prompt consultation can make all the difference. Call before you answer anyone else's questions.")
)
page(HUB, kind="hub", section_label="Criminal defense services",
     title="Criminal Defense Attorney in Summerville, SC | Former Detective Jack Frost",
     description="Summerville, SC criminal defense attorney Jack Frost spent 14 years in law enforcement before law school. Drug charges, domestic violence, bond hearings, warrants, traffic offenses and expungements in Dorchester, Berkeley and Charleston counties.",
     h1="Criminal Defense Attorney in Summerville, SC", eyebrow="Protecting your future", nav_label="Criminal defense",
     lead="Experienced, discreet defense from an attorney who understands both sides of the justice system. The sooner you call, the more options you have.",
     summary="Drug charges, domestic violence, bond, warrants, traffic and expungements.",
     body=hub_body, priority=0.9,
     faqs=[
         ("Should I talk to the police to clear things up?", "Not without a lawyer. You have the right to remain silent and to counsel; using both is the single best decision most people can make in the first 48 hours."),
         ("What will my case cost?", "Most misdemeanors are quoted as a flat fee after we hear the facts; felonies and trials are quoted in stages. We tell you the number before you hire us."),
         ("Do you handle cases in Berkeley and Charleston counties?", "Yes—magistrate, municipal and General Sessions courts in all three counties."),
     ])

# ----------------------------------------------------------------------------- DUI (linked from hub and siblings only)
sp("dui-lawyer-summerville-sc", card_new=True,
   title="Summerville DUI Lawyer | First-Offense DUI & DUAC Defense | Frost Law Group",
   description="Charged with DUI or DUAC in Summerville, Dorchester or Berkeley County? Former detective Jack Frost explains SC's video requirement, the 30-day license hearing deadline, first-offense penalties and how these cases are defended.",
   h1="Summerville DUI Lawyer", nav_label="DUI &amp; DUAC defense",
   lead="Two clocks start the night you are charged: the criminal case and your driver's license. A former officer who has made these arrests explains both.",
   summary="Video rules, the 30-day license deadline, first-offense penalties and the defenses that work.",
   body=(
       '<h2>The first 30 days: your license</h2>'
       f'<p>If you refused the breath test or registered 0.15 or higher, your license was suspended on the spot under South Carolina\'s implied-consent law ({cite("implied_consent", "S.C. Code § 56-5-2950 and § 56-5-2951")}). You have <b>30 days</b> to request an administrative hearing and can obtain a temporary alcohol license in the meantime. Missing the deadline forfeits the hearing—and the hearing is often the first chance to question the officer under oath.</p>'
       '<h2>What South Carolina requires of the officer</h2>'
       f'<p>South Carolina\'s DUI video statute ({cite("dui_video", "S.C. Code § 56-5-2953")}) requires the incident to be recorded from the activation of blue lights through the arrest, including the field sobriety tests and the reading of your rights, and requires video of the breath-test room. Missing or incomplete video, when there is no valid excuse, can result in dismissal. Jack knows exactly what the recording is supposed to show because he made these stops.</p>'
       '<h2>Penalties for a first offense</h2>'
       f'<p>Under {cite("dui", "S.C. Code § 56-5-2930")}, a first-offense DUI carries a fine or jail time that rises with the blood-alcohol level—from a $400 fine or 48 hours to 30 days at 0.08–0.09, up to $1,000 or 30 to 90 days at 0.16 and above—plus a license suspension, the Alcohol and Drug Safety Action Program, higher insurance (SR-22), and, for higher readings, ignition interlock. Second and subsequent offenses escalate sharply. DUAC (driving with an unlawful alcohol concentration, {cite("duac", "§ 56-5-2933")}) carries the same penalties on proof of the number alone.</p>'
       '<h2>How these cases are defended</h2>'
       + checks(["<b>The stop.</b> Was there a lawful reason to pull you over? A stop without reasonable suspicion suppresses everything after it.",
                 "<b>The field sobriety tests.</b> Were they administered and scored as the officer was trained, on video, on a suitable surface?",
                 "<b>The breath test.</b> Observation period, machine records, operator certification, and the required video of the test room.",
                 "<b>Blood draws.</b> Warrant, chain of custody and lab procedures.",
                 "<b>The video.</b> What it shows, what it does not, and whether the statute's requirements were met.",
                 "<b>The paperwork.</b> Implied-consent advisements, the ticket itself and the officer's report, compared line by line to the video."]) +
       '<h2>Court</h2>'
       '<p>First-offense DUI is tried in magistrate or municipal court—Summerville Municipal Court, the Dorchester County magistrate, or the court for the town where you were stopped—with a right to a jury trial. Higher offenses go to General Sessions. Jack appears in all of them.</p>'
       + callout("<b>Frost first:</b> if you have not yet requested the administrative hearing, that is the first call. The criminal case can wait a day; the license deadline cannot.")
       + band("Charged with DUI in Dorchester or Berkeley County?", "Call today. The 30-day license clock is already running.")
   ),
   faqs=[
       ("Will I lose my license after a first DUI in South Carolina?", "A conviction brings a six-month suspension for a first offense, with driving privileges available through ADSAP enrollment and, for higher readings, ignition interlock. A refusal or high breath result triggers a separate administrative suspension you can contest within 30 days."),
       ("Can a DUI be expunged in South Carolina?", "No. DUI convictions are not eligible for expungement, which is one reason the defense matters so much."),
       ("Do I have to take the breath test?", "You can refuse, but refusal triggers an administrative suspension and can be used at trial. Whether it helped or hurt depends on facts we will review with you."),
   ],
   related=["traffic-tickets", "bond-hearings", "expungements"])

sp("drug-charges",
   title="Drug Charge Lawyer in Summerville, SC | Possession, PWID & Trafficking Defense",
   description="Simple possession, possession with intent to distribute and trafficking charges in Dorchester, Berkeley and Charleston counties, defended by former narcotics detective Jack Frost. Conditional discharge, PTI and suppression explained.",
   h1="Drug Charges in Summerville, SC", nav_label="Drug charges",
   lead="Jack Frost investigated narcotics cases for years before he defended them. Here is how South Carolina drug charges work and where they fall apart.",
   summary="Possession, PWID and trafficking, from a former narcotics detective.",
   body=(
       '<h2>The three levels</h2>'
       + table(["Charge", "What it means", "Where it is tried"], [
           ["Simple possession", "A personal-use amount—for marijuana, one ounce or less on a first offense", "Magistrate or municipal court (first offense)"],
           ["Possession with intent to distribute (PWID)", "A larger amount, or possession with packaging, scales, cash or messages suggesting sale; an amount over the statutory threshold is prima facie evidence of intent", "General Sessions"],
           ["Trafficking", "Possession of a quantity at or above the trafficking threshold, regardless of intent to sell—with mandatory minimum sentences", "General Sessions"],
       ]) +
       f'<p>The controlling statute is {cite("drugs", "S.C. Code § 44-53-370")}; penalties depend on the drug schedule, the weight, and prior convictions. Proximity to a school or park adds a separate charge.</p>'
       '<h2>First offense? There may be a way out</h2>'
       f'<p>For a first simple-possession charge, South Carolina\'s conditional discharge statute ({cite("conditional_discharge", "S.C. Code § 44-53-450")}) allows the court to defer proceedings and dismiss the charge after a period of probation-style conditions—leaving no conviction and, after the waiting period, an expungeable record. Pretrial intervention ({cite("pti", "S.C. Code § 17-22-10 et seq.")}) is available for many first-time offenders facing more serious charges, with dismissal on completion. Jack knows which prosecutors offer which programs and when to ask.</p>'
       '<h2>Where drug cases fall apart</h2>'
       + checks(["<b>The search.</b> A traffic stop stretched into a search without consent, probable cause or a warrant; a “knock and talk” that became an entry; a K-9 sniff that extended the stop unlawfully.",
                 "<b>Possession itself.</b> Drugs in a shared car or house belong to nobody until the State proves knowledge and control. Constructive-possession cases are among the weakest prosecutors bring.",
                 "<b>The weight.</b> Trafficking thresholds are exact; packaging, moisture and lab method matter.",
                 "<b>Informants and controlled buys.</b> Reliability, corroboration and whether the warrant affidavit told the whole truth—Jack has written these affidavits and knows how they are supposed to read.",
                 "<b>Chain of custody and the lab.</b> Every hand the evidence passed through, documented."]) +
       '<h2>Collateral consequences</h2>'
       '<p>A drug conviction can cost federal student aid, a professional license, public housing, immigration status and a security clearance. Diversion and reduced charges are usually worth more than the sentence itself, and we plan the defense around what you stand to lose.</p>'
       + band("Drug charge in Dorchester, Berkeley or Charleston County?", "Say nothing to investigators. Call Jack, and bring every piece of paper you were given.")
   ),
   faqs=[
       ("Is marijuana legal in South Carolina?", "No. Possession of any amount remains a crime, though first-offense simple possession is a magistrate-level misdemeanor with diversion options."),
       ("They found drugs in my car but they weren't mine.", "That is a constructive-possession case, and the State must prove you knew about the drugs and had control over them. These cases are very defensible."),
       ("Can a drug charge be expunged?", f"Many first-offense simple-possession dispositions can, after the waiting period, and dismissed charges are expunged automatically or on request. See {A('expungements', 'expungements')}."),
   ],
   related=["bond-hearings", "expungements", "arrest-warrants"])

sp("domestic-violence-defense",
   title="Domestic Violence (CDV) Defense Lawyer in Summerville, SC | Frost Law Group",
   description="Charged with domestic violence in Dorchester, Berkeley or Charleston County? The three degrees under SC law, no-contact bond conditions, the firearm consequences, and how these cases are defended. Former officer Jack Frost.",
   h1="Domestic Violence Defense in Summerville, SC", nav_label="Domestic violence (CDV)",
   lead="A domestic violence arrest happens fast—often on one person's word, the same night. What follows is slower, and it can be defended.",
   summary="Degrees, bond conditions, firearm consequences and defense of CDV charges.",
   body=(
       '<h2>The charge</h2>'
       f'<p>South Carolina\'s domestic violence statute ({cite("cdv", "S.C. Code § 16-25-20")}) applies to household members—spouses and former spouses, people with a child in common, and people who live or have lived together. Degrees run from third degree (a misdemeanor tried in magistrate or municipal court, up to 90 days) through second and first degree (felonies in General Sessions with up to three and ten years) to domestic violence of a high and aggravated nature (up to twenty years). The degree depends on injury, prior convictions, whether a protective order was in place, and other factors—not on how the argument felt.</p>'
       '<h2>What happens the first week</h2>'
       + steps([("Arrest.", " Officers responding to a domestic call are trained to identify a primary aggressor and make an arrest. It is not unusual for the person who called 911 to be the one arrested."),
                ("Bond hearing.", " Usually within 24 hours. The judge will almost always impose a no-contact condition covering the other person and often the shared home. Violating it—even by a text the other person invites—is a new charge and a revoked bond."),
                ("Living arrangements.", " You may need to retrieve belongings with a police escort. We handle the requests to modify bond conditions when the family wants contact restored."),
                ("The case.", " The State, not the alleged victim, decides whether to prosecute; a request to “drop the charges” does not end the case. Evidence is gathered from the 911 call, body-camera video, photographs and statements.")]) +
       '<h2>Consequences beyond the sentence</h2>'
       '<p>Any domestic violence conviction triggers a federal lifetime prohibition on possessing firearms and ammunition, and South Carolina adds its own prohibition. For a hunter, a police officer, a service member or anyone with a concealed-weapons permit, that alone changes the calculus. Convictions also affect custody cases, security clearances, immigration status and employment.</p>'
       '<h2>How these cases are defended</h2>'
       + checks(["<b>Self-defense and defense of others</b>—South Carolina law protects the person who was actually attacked.",
                 "<b>The body-camera video</b> often tells a different story than the incident report; Jack reviews every minute.",
                 "<b>Inconsistent statements</b> between the 911 call, the scene interview and later accounts.",
                 "<b>Injuries</b> that do not match the description, or none at all.",
                 "<b>Pretrial intervention</b> and, for some third-degree cases, a resolution that avoids a conviction and preserves expungement eligibility after the waiting period."])
       + callout("<b>Frost first:</b> do not contact the other person to “work it out,” even if they reach out first. Call us; we will address the no-contact order through the court.")
       + band("Arrested for domestic violence?", "Call before the bond hearing if you can, and before you talk to anyone if you cannot.")
   ),
   faqs=[
       ("Can the victim drop domestic violence charges in South Carolina?", "No. Only the prosecutor can dismiss a charge. The alleged victim's wishes matter, but the State decides."),
       ("Can I go home after a CDV arrest?", "Not if the bond order says no contact with the other person or the residence. We can ask the court to modify the conditions once things have settled."),
       ("Can third-degree domestic violence be expunged?", "A first-offense third-degree conviction can be expunged after five years without a subsequent conviction; dismissed charges are expunged sooner."),
   ],
   related=["bond-hearings", "expungements", "arrest-warrants"])

sp("bond-hearings",
   title="Bond Hearings in Dorchester, Berkeley & Charleston County | Summerville Defense Attorney",
   description="What happens at a South Carolina bond hearing, how bond amounts and conditions are set, how to get a bond reduced or modified, and why having a lawyer at the first hearing matters. Former officer Jack Frost.",
   h1="Bond Hearings in Summerville, Dorchester and Berkeley County", nav_label="Bond hearings",
   lead="The bond hearing is the first decision in a case, and it is made within a day of arrest. Here is what happens and how to make it go better.",
   summary="How bond is set, getting out, and changing conditions later.",
   body=(
       '<h2>When and where</h2>'
       f'<p>After a warrant arrest, South Carolina requires a bond hearing within 24 hours ({cite("bond", "S.C. Code § 22-5-510")}). In Dorchester County the hearing is held by a magistrate at the Dorchester County Detention Center on Hodge Road in Summerville; in Berkeley County at the Hill-Finklea Detention Center in Moncks Corner; in Charleston County at the Sheriff Al Cannon Detention Center in North Charleston. Municipal charges are heard by the municipal judge. For the most serious offenses—those punishable by life or death—only a circuit judge can set bond, which takes longer.</p>'
       '<h2>What the judge decides</h2>'
       + checks(["Whether to release on a personal recognizance (PR) bond—a promise to appear, with no money",
                 "The amount of a surety or cash bond, based on the charge, the person's ties to the community, criminal history and risk of flight or danger",
                 "Conditions: no contact with the alleged victim, no return to a residence, electronic monitoring, no alcohol, surrender of firearms"]) +
       '<p>The judge hears from the officer, the alleged victim if one appears, and the defendant or counsel. Most people say too much. A lawyer speaks to the factors that matter—job, family, residence, no history—and says nothing about the facts of the case.</p>'
       '<h2>After the hearing</h2>'
       + steps([("Posting bond.", " Cash to the clerk, or a bondsman for a percentage fee. Property bonds are possible but slow."),
                ("Reduction or modification.", " If bond is set too high or the conditions are unworkable—a no-contact order that keeps a parent from a child, a curfew that conflicts with work—a motion to reconsider goes to the court that set it, or to circuit court for General Sessions charges."),
                ("Stay compliant.", " A violated condition or a missed court date leads to revocation and a bench warrant. We calendar every date for you.")]) +
       '<h2>If someone you love was arrested</h2>'
       f'<p>Call {TEL}. Tell us the name, the charge and where they are being held. We can often appear at the hearing, and in every case we can prepare you for what the judge will ask and arrange the release once bond is set.</p>'
       + band("Someone in custody?", "Bond hearings happen fast. Call now and we will tell you what to expect in the next 24 hours.")
   ),
   faqs=[
       ("How much is bond in South Carolina?", "There is no schedule; the judge sets it case by case. Many misdemeanors get a PR bond; felonies vary widely."),
       ("Do I get bond money back?", "A cash bond is returned at the end of the case (less any fines) if every court date was kept. A bondsman's fee is not refundable."),
       ("Can bond conditions be changed?", "Yes, by motion to the court that set them. No-contact orders in domestic cases are the most common request."),
   ],
   related=["arrest-warrants", "domestic-violence-defense", "drug-charges"])

sp("expungements",
   title="Expungement Lawyer in Summerville, SC | Clear Your South Carolina Record",
   description="Who qualifies for expungement in South Carolina after the 2018 reforms, how long you must wait, what it costs, and how the process works in Dorchester, Berkeley and Charleston counties. Frost Law Group, Summerville.",
   h1="Expungements in Summerville, SC", nav_label="Expungements",
   lead="A charge that was dismissed, a first offense from years ago, a mistake at nineteen. South Carolina lets many of them be erased. Here is who qualifies.",
   summary="Who qualifies, waiting periods, cost and the process.",
   body=(
       answer(f"Dismissed and not-guilty charges can be expunged at no cost. Many first-offense convictions can be expunged after a waiting period—three years for most low-level misdemeanors, five years for first-offense third-degree domestic violence and Youthful Offender Act sentences, and three years for first-offense simple drug possession handled through conditional discharge—if there have been no other convictions. Some offenses, including DUI and traffic offenses, cannot be expunged.", "The short answer")
       + '<h2>What can be expunged in South Carolina</h2>'
       + table(["Situation", "Eligibility", "Waiting period"], [
           ["Charge dismissed, nol prossed or not guilty", "Eligible; no fee", "None—apply once the case is closed"],
           ["First-offense misdemeanor with a maximum penalty of 30 days or $1,000 (S.C. Code § 22-5-910)", "Eligible if no other convictions", "3 years"],
           ["First-offense third-degree domestic violence", "Eligible if no other convictions", "5 years"],
           ["First-offense simple possession or possession of paraphernalia via conditional discharge (§ 44-53-450)", "Eligible", "3 years after completion"],
           ["Youthful Offender Act sentence (§ 22-5-920)", "Eligible for many nonviolent offenses", "5 years after completion, no other convictions"],
           ["Pretrial intervention completed", "Eligible", "On completion"],
           ["DUI, DUAC, traffic offenses, violent crimes, most felonies", "Not eligible", "—"],
       ]) +
       f'<p>The 2018 expungement reforms ({cite("expungement", "Act 254 of 2018; S.C. Code § 17-22-910 et seq.")}) expanded eligibility, including allowing multiple charges resolved on the same sentencing sheet to be treated as one, and made first-offense drug possession expungeable. Eligibility rules are detailed and change; we check the current statute for every applicant.</p>'
       '<h2>The process</h2>'
       + steps([("Pull the record.", " We obtain your SLED record and the court dispositions to confirm what is on it and what qualifies."),
                ("Application.", " Filed with the solicitor's office of the circuit where the charge was heard (Dorchester and Berkeley are the First Circuit; Charleston is the Ninth). Fees for conviction expungements are set by statute; dismissed charges are free."),
                ("Review and order.", " The solicitor verifies eligibility, SLED verifies the record, and a circuit judge signs the order."),
                ("Destruction.", " The order directs the court, the arresting agency and SLED to destroy the records. Background checks run afterward come back clean for that charge.")]) +
       '<p>Most applications take a few months from filing to order. The process is paper-driven and unforgiving of mistakes; an incomplete application goes to the bottom of the pile.</p>'
       '<h2>Why it matters</h2>'
       '<p>Employers, landlords, licensing boards and schools all run background checks. A dismissed charge from years ago still shows as an arrest until it is expunged. The application is a small effort for a permanent result.</p>'
       + band("Want to know if you qualify?", "Tell us the charge, the county and the year. We will check the statute and tell you honestly.")
   ),
   faqs=[
       ("How much does an expungement cost in South Carolina?", "Expungement of a dismissed charge is free. For conviction expungements the solicitor's office, SLED and the clerk each charge a statutory fee, and attorney's fees are a flat amount we quote up front."),
       ("Do I have to go to court?", "Usually not. The application is processed on paper and signed by a judge."),
       ("Will an expunged charge show on a background check?", "No. The records are destroyed and you may lawfully answer that you were not arrested or convicted, with narrow exceptions for certain law-enforcement and licensing applications."),
   ],
   related=["drug-charges", "domestic-violence-defense", "traffic-tickets"])

sp("traffic-tickets",
   title="Traffic Ticket Lawyer in Summerville, SC | Points, Suspensions & Court Dates",
   description="Speeding, reckless driving, driving under suspension and other South Carolina traffic charges: how points work, when a ticket becomes a suspension, and why paying it is a guilty plea. Summerville traffic attorney.",
   h1="Traffic Tickets in Summerville, SC", nav_label="Traffic tickets",
   lead="Paying a ticket is pleading guilty. Before you do, know what it does to your license, your insurance and, for some charges, your record.",
   summary="Points, suspensions, CDL holders and why not to just pay it.",
   body=(
       '<h2>Points and suspensions</h2>'
       f'<p>South Carolina assigns points to moving violations ({cite("points", "S.C. Code § 56-1-720")}): two for speeding 10 mph or less over, four for 11–24 over, six for 25 or more over or for reckless driving, and so on. Twelve or more points brings a suspension, and points are halved after a year. Insurance companies read the same record and price it.</p>'
       '<h2>Tickets that are more than tickets</h2>'
       + checks(["<b>Reckless driving</b>—a criminal misdemeanor with six points, and a second offense within five years brings a suspension.",
                 "<b>Driving under suspension</b>—a criminal charge with jail exposure that grows with each offense.",
                 "<b>Leaving the scene, racing, and habitual-offender status</b>—each with consequences far beyond a fine.",
                 "<b>Commercial drivers</b>—a personal-vehicle ticket can still put a CDL at risk; never pay one without checking.",
                 "<b>Out-of-state drivers</b>—South Carolina reports to your home state under the interstate compact."]) +
       '<h2>What we can often do</h2>'
       '<p>Negotiate a reduction to a non-moving or lower-point violation, arrange a defensive-driving resolution where the court allows it, challenge speed measurement and stop legality when the facts support it, and appear for you so you do not lose a workday in Summerville Municipal Court or a magistrate\'s court. For serious charges, we prepare for trial.</p>'
       '<h2>Court</h2>'
       '<p>Tickets are heard in the municipal court of the town where you were stopped (Summerville, Goose Creek, North Charleston and so on) or the county magistrate\'s court for stops by the sheriff or Highway Patrol. Your ticket shows the court and the date; if you miss the date, the court can convict you in your absence and suspend your license for failure to pay.</p>'
       + band("Got a ticket?", "Send us a photo of it. We will tell you the points, the risk, and whether it is worth fighting.")
   ),
   faqs=[
       ("Can I just pay a speeding ticket in South Carolina?", "Yes, but paying is a guilty plea and the points post to your record. For anything above a minor speed, ask first."),
       ("Do I have to appear in court?", "For most tickets an attorney can appear for you. Some charges require your presence."),
       ("Will a ticket in South Carolina affect my Georgia or North Carolina license?", "Usually yes; states share convictions through the Driver License Compact."),
   ],
   related=["dui-lawyer-summerville-sc", "expungements", "arrest-warrants"])

sp("arrest-warrants",
   title="Arrest Warrant Lawyer in Summerville, SC | Turn Yourself In the Right Way",
   description="Heard there is a warrant for your arrest in Dorchester, Berkeley or Charleston County? How to confirm it, why to surrender with a lawyer, how a bond hearing is arranged, and what to do about a bench warrant. Former officer Jack Frost.",
   h1="Arrest Warrants in Summerville, SC", nav_label="Arrest warrants",
   lead="A warrant does not go away, and being picked up at work or at a traffic stop is the worst way to deal with it. There is a better one.",
   summary="Confirming a warrant, surrendering with counsel, and bench warrants.",
   body=(
       '<h2>Two kinds of warrants</h2>'
       + checks([f"<b>Arrest warrants</b> are issued by a magistrate or municipal judge on an officer's sworn affidavit that there is probable cause you committed a crime ({cite('warrants', 'S.C. Code § 22-5-110')}). Jack has written hundreds; he knows what a sufficient affidavit looks like and what a deficient one looks like.",
                 "<b>Bench warrants</b> are issued by a judge when you miss a court date or violate a court order. They usually come with a bond revocation and a license suspension for failure to appear on a traffic charge."]) +
       '<h2>If you think there is a warrant</h2>'
       + steps([("Do not wait for the knock.", " Warrants are served at traffic stops, at work and at 6 a.m. at home. None of those lets you prepare."),
                ("Call us first.", " We confirm whether a warrant exists and what it charges through the issuing court or agency, without exposing you."),
                ("Arrange the surrender.", " We schedule a time to turn yourself in at the detention center, often with the bond hearing arranged so you are processed and released the same day. For some charges we can ask that a courtesy summons be used instead of an arrest."),
                ("Prepare for bond.", " Employment letter, residence proof, family present—what the judge weighs. See " + A("bond-hearings", "bond hearings") + "."),
                ("Start the defense.", " A warrant is the beginning of a case, not a verdict. The affidavit is the first thing we attack.")]) +
       '<h2>Bench warrants</h2>'
       '<p>If you missed a court date, the fix is a motion to recall the bench warrant and reset the case—faster and cheaper than being arrested on it. Many people miss dates because a notice went to an old address; the court is usually willing to reset once, with counsel.</p>'
       '<h2>Warrants from other counties or states</h2>'
       '<p>Charleston County warrants are served in Dorchester County and vice versa, and out-of-state warrants lead to extradition holds. We coordinate with the issuing jurisdiction so a surrender happens once, in the right place.</p>'
       + callout("<b>Frost first:</b> if an officer or investigator calls and asks you to “come in and talk,” there is a reasonable chance a warrant already exists. Call us before you go.")
       + band("Think there is a warrant with your name on it?", "Call. We will find out quietly and arrange the surrender on your terms.")
   ),
   faqs=[
       ("How do I check for a warrant in Dorchester County?", "The sheriff's office and the magistrate's court can confirm active warrants, but calling them yourself can prompt an arrest. Let us check on your behalf."),
       ("Will I have to spend the night in jail?", "Usually not when a surrender is arranged with a bond hearing scheduled; processing and release often happen the same day."),
   ],
   related=["bond-hearings", "drug-charges", "domestic-violence-defense"])
