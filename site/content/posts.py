"""Blog posts: local news and community questions, answered by the attorney who owns the topic.

Authorship rule: Tara writes probate and estate planning; Jack writes criminal defense. Each post
names the other attorney as reviewer. Outbound links go to the original reporting or official
sources (news outlets, county and state sites) and to the community threads where the question is
being asked (Nextdoor, Reddit — nofollow). Verified URLs come from local_data.json via local.link().
"""
from .base import page, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
from . import firm
from .local import cite, link, LINKS

TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
DATE = "2026-09-16"


def src(*keys):
    """Build a sources list from verified link keys (skips unknown keys)."""
    out = []
    for k in keys:
        l = LINKS.get(k)
        if l:
            out.append((l["label"], l["url"], l.get("nofollow", False)))
    return out


def post(slug, **kw):
    kw.setdefault("kind", "post")
    kw.setdefault("hub", "blog")
    kw.setdefault("date", DATE)
    kw.setdefault("cta", False)
    kw.setdefault("changefreq", "yearly")
    kw.setdefault("priority", 0.5)
    return page("blog/" + slug, **kw)


# ----------------------------------------------------------------------------- 1. New residents
post("new-summerville-residents-estate-plan", author="tara", reviewer="jack", category="Estate planning",
     title="Moved to Summerville? Five Documents South Carolina Wants Redone",
     description="Dorchester and Berkeley counties keep adding new residents. If your will and powers of attorney were signed in another state, here is what still works in South Carolina and what does not.",
     h1="Moved to Summerville? Five documents South Carolina wants you to redo",
     summary="Thousands of families arrive in Nexton, Cane Bay and Carnes Crossroads every year with estate documents from somewhere else. Most of the wills still work. Most of the powers of attorney do not.",
     lead="Every week the local papers report another subdivision approved in Dorchester or Berkeley County. If you are one of the families moving in, your estate plan probably moved with you—and part of it stopped working at the state line.",
     body=(
         '<h2>What the growth stories leave out</h2>'
         f'<p>Read {link("pc_summerville", "the Post and Courier’s Summerville coverage")} or the {link("berkeley_independent", "Berkeley Independent")} for a month and you will see the pattern: new neighborhoods off Nexton Parkway, Cane Bay Boulevard and Highway 17-A, new schools, new traffic counts. What the stories never mention is that the newcomers\' legal paperwork was written for Ohio, New York or Georgia. That matters more than most people expect.</p>'
         '<h2>The five documents, in order of urgency</h2>'
         + steps([
             ("Your durable power of attorney.", f" South Carolina adopted the Uniform Power of Attorney Act in 2017 ({cite('poa_act', 'S.C. Code Title 62, Article 8')}). A power of attorney signed elsewhere is generally recognized, but South Carolina requires a durable POA to be recorded with the county register of deeds before an agent can act during incapacity, and local banks are quick to reject unfamiliar forms. A new South Carolina POA in recordable form solves both problems."),
             ("Your health care power of attorney and living will.", f" Hospitals here look for South Carolina's own statutory forms ({cite('hcpoa', '§§ 62-5-503 and 62-5-504')} and the {cite('living_will_act', 'Death with Dignity Act')}). An out-of-state directive may be honored, but in an emergency room nobody wants to be the test case. These are quick to redo."),
             ("Your will.", f" A will valid where you signed it is valid here. The problems are practical: your named personal representative may now live 800 miles away, your guardian nomination may be stale, and the will may not be self-proved in a way the Dorchester or Berkeley County probate court accepts without a witness affidavit ({cite('self_proved', '§ 62-2-503')}). We usually re-sign a South Carolina will rather than patch the old one."),
             ("Your trust, if you have one.", " The trust itself travels fine. The funding does not: your new Lowcountry home was deeded to you personally at closing, not to the trust, unless someone caught it. Retitling the house is a one-page deed—but only if someone does it."),
             ("Your beneficiary designations.", " New job, new 401(k), new life insurance through the new employer. Each one has a beneficiary form that overrides your will. Check them the same week you change your driver's license."),
         ]) +
         '<h2>The county question</h2>'
         f'<p>Summerville sits in Dorchester County—except when it doesn\'t. Nexton, Cane Bay, Carnes Crossroads and much of the growth north of I-26 carry a Summerville address in <em>Berkeley</em> County. Your county decides where your estate will be probated, where a guardianship is filed and which sheriff serves a warrant. Our {A("probate-courts", "guide to the three probate courts")} and the {A("service-areas/nexton", "Nexton")} and {A("service-areas/cane-bay", "Cane Bay")} pages explain which is which.</p>'
         '<h2>What people are asking their neighbors</h2>'
         f'<p>The question shows up on {link("nextdoor_summerville", "Nextdoor for Summerville")} and in {link("reddit_charleston", "r/Charleston")} threads every few weeks: “Do I need a new will now that I\'m in South Carolina?” The honest answer is <em>probably not the will, definitely the powers of attorney, and check the deed.</em> A plan review is a flat fee and takes one meeting; see {A("estate-plan-review", "estate plan reviews")}.</p>'
         + callout("<b>Frost first:</b> before you sign the “South Carolina update” a moving-related service emails you, let us read it. We see plans every month that were “updated” without the recording language, the witnesses, or the deed.")
     ),
     sources=src("pc_summerville", "berkeley_independent", "nextdoor_summerville", "reddit_charleston") + [("S.C. Code Title 62, Article 8 (Uniform Power of Attorney Act)", "https://www.scstatehouse.gov/code/t62c008.php", False)],
     related=["estate-plan-review", "power-of-attorney", "probate-courts"],
     faqs=[("Is my out-of-state will valid in South Carolina?", "Yes, if it was valid where it was signed. We still recommend re-signing a South Carolina will so it is self-proved here and names people who can actually serve."),
           ("Do I have to record my power of attorney in South Carolina?", "A durable power of attorney must be recorded with the register of deeds in your county before your agent can act once you are incapacitated. We prepare it in recordable form and record it when needed.")])

# ----------------------------------------------------------------------------- 2. Hurricane season
post("hurricane-season-documents-dorchester-county", author="tara", reviewer="jack", category="Estate planning",
     title="Hurricane Season: Four Documents for the Go-Bag | Dorchester County",
     description="Every evacuation order raises the same question in Dorchester and Berkeley County homes: where is the will? Four documents to secure now, and what South Carolina law does if an original will is lost.",
     h1="Before the next evacuation order: four documents Dorchester County families should have in the go-bag",
     summary="When the county issues an evacuation order, the will is the last thing anyone thinks about—and the one document South Carolina law treats harshly if it goes missing.",
     lead="Hurricane season runs through November, and the Lowcountry's news outlets spend it tracking cones and evacuation zones. Here is the legal checklist that never makes the broadcast.",
     body=(
         '<h2>Why a lost will is worse than a lost roof</h2>'
         '<p>If an original will cannot be found after death, South Carolina presumes the person destroyed it on purpose. A copy can sometimes be admitted, but only after a court proceeding with evidence that the will was not revoked—expensive, slow, and easy for an unhappy relative to contest. A storm-soaked filing cabinet in a flooded garage produces exactly that situation.</p>'
         '<h2>The four documents</h2>'
         + steps([
             ("The original will (and trust).", " Keep it in a sealed, waterproof pouch with the go-bag, or leave the original with your attorney and keep a copy at home with a note saying where the original is. Our office holds originals for clients who ask."),
             ("Powers of attorney.", " If you are evacuated and a spouse or parent is hospitalized somewhere else, the health care power of attorney is what lets you speak for them by phone. Keep signed copies in the bag and photos on your phone."),
             ("Insurance policies and a home inventory.", " Not estate documents, but the same pouch: policy numbers, agent contacts, and a phone video walking through every room. Claims move faster with proof."),
             ("Deeds, titles and account list.", " A one-page list of accounts, policies and where the deeds are recorded. If the worst happens during a storm, this is what your personal representative will need first."),
         ]) +
         '<h2>Where to get the official information</h2>'
         f'<p>Evacuation zones and orders come from {link("scemd", "the South Carolina Emergency Management Division")} and {link("dorchester_emd", "Dorchester County Emergency Management")}; the local outlets—{link("live5", "Live 5 News")}, {link("abcnews4", "ABC News 4")} and {link("wcbd", "WCBD News 2")}—carry the county announcements and the traffic reversals on I-26. Bookmark them now, before the cone appears.</p>'
         '<h2>A note for families with older parents</h2>'
         f'<p>Evacuations are when families discover that nobody has authority to move a parent, talk to the facility, or pay the bill from the hotel in Columbia. If your parent does not have a durable power of attorney and a health care power of attorney, and still has the capacity to sign them, do it before the season peaks. If they no longer can, read our page on {A("guardianship-and-conservatorship", "guardianship and conservatorship")}.</p>'
         + callout("<b>Frost first:</b> the week after a storm, contractors and “document services” go door to door. A deed transfer signed under stress is the kind of thing we spend the next year undoing. Call before you sign.")
     ),
     sources=src("scemd", "dorchester_emd", "live5", "abcnews4", "wcbd", "nextdoor_summerville"),
     related=["last-will-and-testament", "power-of-attorney", "probate-process"],
     faqs=[("Can a copy of a will be probated in South Carolina?", "Sometimes, through a formal proceeding with evidence that the original was not revoked. It is far easier to keep the original safe—or leave it with your attorney."),
           ("Should I keep my will in a bank safe-deposit box?", "It is safe from water, but the box may be sealed at death until the personal representative is appointed—and the appointment needs the will. If you use a box, make sure a co-owner can open it.")])

# ----------------------------------------------------------------------------- 3. Guardianship for an aging parent
post("guardianship-aging-parent-summerville", author="tara", reviewer="jack", category="Probate",
     title="Guardianship for an Aging Parent in Summerville | Nextdoor Question Answered",
     description="“Who handles guardianship for my mom in Summerville?” A former Dorchester County Associate Probate Judge explains the process, the alternatives, and when a power of attorney can still avoid it.",
     h1="“Who handles guardianship for my aging parent in Summerville?” The Nextdoor question, answered",
     summary="It is one of the most common legal questions on Summerville's neighborhood forums, and the answers usually miss the first step: whether a guardianship is needed at all.",
     lead="A neighbor posts that Mom has stopped paying bills and will not see a doctor, and asks who to call. Thirty replies later, nobody has mentioned the probate court. Here is what actually happens.",
     body=(
         answer("Guardianship and conservatorship for an adult in Summerville are filed in the probate court of the county where the person lives—Dorchester County for most Summerville addresses, Berkeley County for Nexton, Cane Bay and Carnes Crossroads. Frost Law Group handles these cases; Tara Frost served as an Associate Probate Judge in Dorchester County, where they are heard. Before filing, we check whether a power of attorney can still be signed, because it is faster, cheaper and private.", "The short answer")
         + '<h2>First question: can Mom still sign?</h2>'
         '<p>Capacity to sign a power of attorney is a lower bar than people assume. A parent with early dementia who understands, on a good morning, that she is naming her daughter to handle her money and her medical decisions can usually sign valid documents. If that is your situation, the whole guardianship question may disappear with two signatures and a notary. We meet clients at home or at a facility for exactly this reason.</p>'
         '<h2>If she cannot: what a guardianship involves</h2>'
         + steps([
             ("A petition in probate court.", f" Filed under South Carolina's adult protective proceedings statutes ({cite('guardianship', 'S.C. Code Title 62, Article 5')}) with a physician's report on the person's condition."),
             ("Examiners and a guardian ad litem.", " The court appoints professionals to evaluate the person and report; the guardian ad litem represents the person's interests."),
             ("Notice to the family.", " Spouse, children and other close relatives receive notice and can object or ask to serve."),
             ("A hearing.", " The judge decides whether the person is incapacitated and, if so, who should serve and with what powers—often a limited guardianship tailored to the actual need."),
             ("Ongoing reporting.", " Guardians file annual reports; conservators file inventories and accountings and usually post a bond."),
         ]) +
         '<h2>What it costs and how long it takes</h2>'
         '<p>Filing fees, examiner fees and attorney\'s fees together commonly run into the low thousands of dollars for an uncontested case, and two to four months from filing to hearing depending on the court\'s docket. Contested cases—two siblings who each want to serve, or a parent who objects—take longer and cost more. Emergency appointments are available when someone is in immediate danger.</p>'
         '<h2>Where the neighbors\' advice goes wrong</h2>'
         + checks(["“Just get power of attorney” — a POA cannot be signed <em>for</em> someone who lacks capacity; that is what guardianship is for.",
                   "“Add yourself to her bank account” — that makes you a joint owner, exposes the money to your creditors, and changes who inherits it.",
                   "“The doctor can declare her incompetent” — a doctor's opinion is evidence; only the probate court can appoint a guardian.",
                   "“Adult Protective Services will handle it” — APS investigates abuse and neglect; it does not manage a parent's finances for the family."]) +
         f'<p>You will find versions of all four on {link("nextdoor_summerville", "Nextdoor")} and in {link("reddit_charleston", "r/Charleston")} threads. For non-legal help—home care, respite, Medicaid waiver programs—{link("trident_aging", "the Trident Area Agency on Aging")} is the right first call.</p>'
         + band("Worried about a parent?", "Call and describe what is happening. We will tell you whether documents can still be signed or a petition is needed, and what each path costs.")
     ),
     sources=src("nextdoor_summerville", "reddit_charleston", "trident_aging", "dorchester_probate_site") + [("S.C. Code Title 62, Article 5 (protection of persons under disability)", "https://www.scstatehouse.gov/code/t62c005.php", False)],
     related=["guardianship-and-conservatorship", "power-of-attorney", "probate-courts"],
     faqs=[("Can I get guardianship of my mother without a lawyer?", "The probate court accepts pro se petitions, but the medical evidence, notice requirements and hearing are unforgiving of mistakes. Most families use an attorney for at least the petition and hearing."),
           ("Which court handles guardianship for a Summerville address?", "Dorchester County Probate Court for most of Summerville; Berkeley County Probate Court for Nexton, Cane Bay, Carnes Crossroads and other Summerville addresses north of the county line.")])

# ----------------------------------------------------------------------------- 4. Expungement clinics
post("expungement-clinics-who-qualifies-dorchester-berkeley", author="jack", reviewer="tara", category="Criminal defense",
     title="Expungement Clinics in the News: Who Qualifies in Dorchester & Berkeley",
     description="Solicitors and legal aid groups hold expungement clinics around the Lowcountry. Before you stand in line, a former officer explains who qualifies under South Carolina's 2018 reforms and what the clinic can and cannot do.",
     h1="Saw the expungement clinic in the news? Here is who qualifies in Dorchester and Berkeley County",
     summary="Every few months a Lowcountry outlet covers a free expungement clinic. The lines are long and about half the people in them do not qualify—yet. Here is how to know before you go.",
     lead="Expungement clinics are a genuinely good thing. They are also confusing, because eligibility depends on the exact charge, the exact disposition and the calendar. Check these five things first.",
     body=(
         '<h2>What a clinic can do</h2>'
         '<p>A clinic helps you pull your record, confirm eligibility and complete the application that goes to the solicitor\'s office—the First Circuit for Dorchester and Berkeley counties, the Ninth Circuit for Charleston. The volunteers are usually law students and legal-aid attorneys. What they cannot do is change the law: if your charge is not eligible, or the waiting period has not run, the answer is the same at the clinic as anywhere else.</p>'
         '<h2>The five questions that decide eligibility</h2>'
         + steps([
             ("Was the charge dismissed, nol prossed or found not guilty?", " Then it is eligible now, at no cost. Many people do not realize a dismissed charge still shows on a background check until it is expunged."),
             ("Was it a first-offense misdemeanor with a maximum penalty of 30 days or $1,000?", f" Eligible three years after the conviction if you have had no other convictions ({cite('expungement_misdemeanor', 'S.C. Code § 22-5-910')}). Third-degree domestic violence, first offense, waits five years."),
             ("Was it first-offense simple possession or paraphernalia?", f" Eligible if handled through a conditional discharge ({cite('conditional_discharge', '§ 44-53-450')}) and three years have passed since completion—one of the 2018 changes."),
             ("Were you sentenced under the Youthful Offender Act?", f" Many nonviolent YOA sentences are eligible five years after completion with no later convictions ({cite('yoa', '§ 22-5-920')})."),
             ("Is it a DUI, a traffic offense, or a violent crime?", " Not eligible. No clinic and no attorney can change that."),
         ]) +
         '<h2>What changed in 2018</h2>'
         f'<p>{cite("expungement", "Act 254 of 2018")} expanded expungement in three ways people still do not know about: multiple charges resolved on the same sentencing sheet can be treated as one offense; first-offense drug possession became eligible; and expungement now applies to convictions even if the person later moved on to a clean record in a different way. If you were told “no” before 2018, ask again.</p>'
         '<h2>Before you go</h2>'
         + checks(["Pull your own record: the clinic will, but knowing your exact charges and dispositions beforehand saves an hour in line.",
                   "Bring photo identification and the case numbers if you have them.",
                   "Count the years from the date of conviction (or completion of the program), not the date of arrest.",
                   "If any charge is pending anywhere, resolve it first; a pending charge blocks expungement."]) +
         f'<p>Clinic announcements run in {link("pc_summerville", "the Post and Courier")}, on {link("live5", "Live 5 News")} and on the counties\' own pages. If you would rather not wait for the next one, we file expungements year-round for a flat fee; see {A("expungements", "expungements")}.</p>'
         + callout("<b>Frost first:</b> if the charge you want cleared was one of several from the same night, ask about the same-sentencing-sheet rule before assuming only one can be expunged.")
     ),
     sources=src("pc_summerville", "live5", "sccourts_expungement") + [("S.C. Code Title 22, Chapter 5 (expungement of criminal records)", "https://www.scstatehouse.gov/code/t22c005.php", False), ("S.C. Code Title 17, Chapter 22 (expungement procedure)", "https://www.scstatehouse.gov/code/t17c022.php", False)],
     related=["expungements", "drug-charges", "domestic-violence-defense"],
     faqs=[("Are expungement clinics free?", "Usually the clinic's help is free; the statutory fees for conviction expungements still apply unless the sponsor covers them. Expunging a dismissed charge is free."),
           ("Can I expunge a charge from another county at a Dorchester County clinic?", "The application goes to the solicitor for the circuit where the charge was heard, so a Charleston County charge goes to the Ninth Circuit regardless of where you live now.")])

# ----------------------------------------------------------------------------- 5. School zones
post("school-zone-traffic-enforcement-summerville", author="jack", reviewer="tara", category="Criminal defense",
     title="School-Zone Enforcement in Summerville: What a Ticket Really Costs",
     description="Each August, Summerville police and the Dorchester County Sheriff's Office announce school-zone enforcement. A former officer explains points, insurance, the school-bus charge that is not a ticket, and when to fight.",
     h1="Back-to-school traffic enforcement in Summerville: what a ticket really costs",
     summary="The August press releases promise extra patrols around Dorchester District Two schools. The tickets that follow cost more than the fine on the front.",
     lead="Every year the same announcement runs the week school starts: extra patrols on Central Avenue, Old Trolley Road and Highway 78 around the schools. Here is what the tickets do after you pay them.",
     body=(
         '<h2>The fine is the small part</h2>'
         f'<p>South Carolina puts points on your license for moving violations ({cite("points", "S.C. Code § 56-1-720")}): two for speeding ten over or less, four for eleven to twenty-four over, six for twenty-five or more over. Points post when you pay the ticket, because paying is a guilty plea. Insurance carriers read the same record. A four-point ticket can cost several times its fine in premiums over three years, and twelve points brings a suspension.</p>'
         '<h2>The charge that is not a ticket</h2>'
         '<p>Passing a stopped school bus with its stop arm out is a criminal misdemeanor in South Carolina, not a simple traffic infraction—six points, a fine that can run into the thousands on a first offense, and a court date you should not handle alone. Bus cameras in Dorchester District Two mean these charges arrive by mail weeks after the fact. Call before you respond.</p>'
         '<h2>Who is writing the tickets</h2>'
         f'<p>Inside town limits it is the {link("summerville_pd", "Summerville Police Department")}, and the ticket goes to Summerville Municipal Court. Outside the limits it is the Dorchester County Sheriff\'s Office or the Highway Patrol, and the case goes to the county magistrate. The court on the ticket tells you which. {link("dd2", "Dorchester District Two")} publishes the school calendar, which is also the enforcement calendar.</p>'
         '<h2>When fighting it makes sense</h2>'
         + checks(["Any ticket of four points or more, if your record is otherwise clean—reductions to non-moving violations are common.",
                   "Anything involving a commercial driver's license, where a personal-vehicle ticket can cost the job.",
                   "Reckless driving, driving under suspension or a school-bus charge—criminal charges with jail exposure.",
                   "A ticket you believe is wrong: the speed measurement, the school-zone timing, the signage."]) +
         '<p>For a two-point ticket with no CDL and a clean record, paying it is often the rational choice. We will tell you that on the phone.</p>'
         + callout("<b>Frost first:</b> photograph the ticket and text it to us before the court date printed on it. Missing that date turns a fine into a bench warrant and a license suspension.")
     ),
     sources=src("summerville_pd", "dd2", "live5", "pc_summerville") + [("S.C. Code Title 56, Chapter 1 (driver's license points)", "https://www.scstatehouse.gov/code/t56c001.php", False)],
     related=["traffic-tickets", "arrest-warrants", "expungements"],
     faqs=[("Do school-zone speeding fines double in South Carolina?", "South Carolina does not automatically double fines in school zones the way some states do, but the points, the insurance impact and the officer's discretion on how the ticket is written are all worse. Treat it as a four- or six-point ticket, not a parking fine."),
           ("Can a traffic ticket be expunged?", "No. Traffic convictions are not eligible for expungement in South Carolina, which is why the decision to pay or fight matters.")])

# ----------------------------------------------------------------------------- 6. Reddit: do I need a probate lawyer
post("do-i-need-a-probate-lawyer-south-carolina-reddit", author="tara", reviewer="jack", category="Probate",
     title="Reddit Asks: Do I Need a Probate Lawyer in SC? A Former Judge Answers",
     description="The question comes up constantly in r/Charleston and r/southcarolina. An honest answer from a former Dorchester County Associate Probate Judge: when you can do it yourself, when you should not, and how to tell.",
     h1="Reddit asks: “Do I really need a probate lawyer in South Carolina?” An honest answer from a former probate judge",
     summary="Half the replies say “just use the court forms,” the other half say “always hire a lawyer.” Both are right, for different estates. Here is how to tell which one you have.",
     lead="It is one of the most-asked legal questions in the Lowcountry's online forums, and the replies are usually somebody's one experience. Here is the view from the bench.",
     body=(
         answer("You can probate a simple South Carolina estate yourself: the probate court's forms are public, the clerks are helpful, and an estate with a clear will, cooperative heirs, no real estate to sell and no creditor problems is manageable. You should hire a lawyer when the estate owns real estate that must be sold or divided, when heirs disagree, when there is a business or out-of-state property, when a creditor claim is large, or when you are the personal representative and the beneficiaries are already unhappy. Call and we will tell you which yours is—for free, on the phone.", "The short answer")
         + '<h2>Estates you can usually handle alone</h2>'
         + checks([f"A small estate that qualifies for the affidavit—a probate estate of $45,000 or less after liens, collected by affidavit ({A('small-estate-affidavit', 'details')}).",
                   "A surviving spouse inheriting everything under a clear will, with all the accounts already joint or beneficiary-designated.",
                   "An informal estate where the only real asset is a house passing to one heir who is keeping it, and every heir signs waivers.",
                   f"Any of the above where the personal representative is organized and follows the eight-month creditor rule ({cite('creditor_period', '§ 62-3-801')}) instead of distributing early."]) +
         '<h2>Estates that go wrong without help</h2>'
         + checks(["Real estate that must be sold, especially heirs' property with several owners or an old family parcel with title problems.",
                   "A will that treats children unequally, was signed late in life, or was prepared by one child.",
                   "A business, rental property, or anything in another state.",
                   "Creditor claims larger than a few thousand dollars, or a Medicaid estate-recovery claim.",
                   "A beneficiary who is a minor, has a disability, or cannot be found.",
                   "Any estate where a beneficiary has already hired a lawyer."]) +
         '<h2>What the forum answers miss</h2>'
         f'<p>Two things. First, hiring a probate attorney is not all-or-nothing: we regularly handle just the opening and the inventory, or just the closing, for a flat fee, while the family does the rest. Second, attorney\'s fees for the estate are paid from the estate, not from the personal representative\'s pocket. That changes the math for a lot of the people asking in {link("reddit_charleston", "r/Charleston")} and {link("reddit_southcarolina", "r/southcarolina")}.</p>'
         '<h2>Where to start if you are doing it yourself</h2>'
         f'<p>The {link("sccourts_probate_forms", "South Carolina Judicial Branch publishes the probate forms")} used statewide, and each county court has a self-help page. Read our {A("probate-process", "step-by-step guide")} first, then the {A("executor-duties", "personal representative checklist")}. If you get stuck, a one-hour consultation is cheaper than unwinding a mistake.</p>'
         + band("Not sure which kind of estate you have?", "Tell us what was owned and who the heirs are. We will say honestly whether you need us.")
     ),
     sources=src("reddit_charleston", "reddit_southcarolina", "sccourts_probate_forms", "dorchester_probate_site"),
     related=["probate-process", "small-estate-affidavit", "executor-duties"],
     faqs=[("How much does a probate lawyer cost in South Carolina?", "There is no statutory percentage. Most firms, including ours, quote flat fees for uncontested estates and hourly rates with an estimate for contested matters. Fees are paid from the estate."),
           ("Can the personal representative hire a lawyer for the estate without the heirs' permission?", "Yes. Reasonable attorney's fees are an administration expense, though beneficiaries can object to unreasonable ones at the accounting.")])

# ----------------------------------------------------------------------------- 7. DV arrests in the news
post("domestic-violence-arrest-first-72-hours-dorchester-county", author="jack", reviewer="tara", category="Criminal defense",
     title="After a Domestic Violence Arrest in Dorchester County: The First 72 Hours",
     description="Local police blotters report domestic violence arrests every week. What happens in the first three days—bond, no-contact orders, going home—and the mistakes that turn one charge into two. By a former officer.",
     h1="After a domestic violence arrest in Dorchester County: the first 72 hours",
     summary="The arrest makes the blotter; what happens next does not. A former officer walks through bond, the no-contact order, and the three mistakes that create a second charge.",
     lead="Scan the weekly arrest reports in the local papers and you will see “domestic violence, 3rd degree” more than almost any other charge. The first three days after that arrest decide more than most people realize.",
     body=(
         '<h2>Hour 0–24: the bond hearing</h2>'
         f'<p>Most domestic violence arrests in Dorchester County are heard by a magistrate at the Dorchester County Detention Center on Hodge Road in Summerville within 24 hours ({cite("bond", "S.C. Code § 22-5-510")}); Berkeley County hearings are at Hill-Finklea in Moncks Corner. The judge sets a bond and, almost always, a no-contact condition covering the other person and often the shared home. The alleged victim may be present and may speak. What you say at this hearing about the facts is evidence; what you say about your job, your residence and your record is what the judge needs.</p>'
         '<h2>Hour 24–48: going home—or not</h2>'
         '<p>If the bond order bars you from the residence, you cannot go back for clothes, medication or a vehicle without a police escort, arranged through the agency that made the arrest. Showing up anyway violates the bond, even if the other person invited you. That is mistake number one, and it is the most common one we see.</p>'
         '<h2>Hour 48–72: the phone</h2>'
         '<p>Mistake number two is the text message. “I\'m sorry,” “can we talk,” “please drop this”—each one is a bond violation and, depending on content, a possible witness-tampering charge. Mistake number three is the phone call from the jail, which is recorded. The other person\'s wishes matter to the prosecutor, but only the prosecutor can dismiss the case, and pressure on a witness makes dismissal less likely, not more.</p>'
         '<h2>What the charge actually is</h2>'
         f'<p>South Carolina grades domestic violence by injury, history and circumstances ({cite("cdv", "S.C. Code § 16-25-20")}), from third degree in magistrate or municipal court to first degree and high-and-aggravated in General Sessions. Any conviction carries a lifetime federal firearms prohibition. Our {A("domestic-violence-defense", "domestic violence defense page")} covers the degrees and the defenses.</p>'
         '<h2>If you are the person who was hurt</h2>'
         f'<p>This article is written for people who were arrested, but the same 72 hours are frightening from the other side. {link("my_sisters_house", "My Sister’s House")} serves Dorchester, Berkeley and Charleston counties with a 24-hour line, shelter and court advocacy, and the {link("dorchester_sheriff", "Dorchester County Sheriff’s Office")} victim advocates can explain the bond process and orders of protection.</p>'
         + callout("<b>Frost first:</b> if a family member calls you from the detention center, the most useful thing you can do is call a lawyer before the bond hearing—not post on Facebook, not call the other person, not “go get his things.”")
     ),
     sources=src("dorchester_sheriff", "my_sisters_house", "pc_summerville", "live5") + [("S.C. Code Title 16, Chapter 25 (domestic violence)", "https://www.scstatehouse.gov/code/t16c025.php", False)],
     related=["domestic-violence-defense", "bond-hearings", "arrest-warrants"],
     faqs=[("Can the victim drop domestic violence charges in South Carolina?", "No. Only the solicitor can dismiss a charge. The alleged victim's wishes are considered but do not control."),
           ("Can I get the no-contact order lifted?", "The court that set bond can modify it on motion, often after a cooling-off period and with the other person's input. Do not test it in the meantime.")])

# ----------------------------------------------------------------------------- 8. Berkeley County side of Summerville
post("summerville-address-berkeley-county-what-it-means", author="tara", reviewer="jack", category="Probate",
     title="Summerville Address, Berkeley County: What It Means for Your Estate",
     description="Nexton, Cane Bay and Carnes Crossroads have Summerville addresses but sit in Berkeley County. That decides where your estate is probated, where a guardianship is filed and which court hears a ticket.",
     h1="Nexton, Cane Bay and Carnes Crossroads are in Berkeley County. Here is why that matters for your estate—and your speeding ticket",
     summary="The fastest-growing parts of “Summerville” are not in Dorchester County at all. The county line quietly decides which courthouse your family will deal with.",
     lead="Ask a Nexton resident what county they live in and you will get a pause. The mailing address says Summerville. The tax bill, the probate court and the sheriff say Berkeley.",
     body=(
         '<h2>The line</h2>'
         '<p>The Dorchester–Berkeley county line runs roughly along the old town\'s eastern and northern edges. The communities built since I-26\'s exit 197 opened—Nexton, Cane Bay, Carnes Crossroads, Sangaree, much of the 29486 ZIP code—are in Berkeley County. So is Jedburg. Historic downtown Summerville, Knightsville, Ashborough, Old Trolley Road and most of 29483 and 29485 are Dorchester County. Your property tax bill, your voter registration card and the county GIS map all say which side you are on.</p>'
         '<h2>What the county decides</h2>'
         + table(["Matter", "Dorchester side", "Berkeley side"], [
             ["Probate of an estate", "Dorchester County Probate Court, St. George", "Berkeley County Probate Court, Moncks Corner"],
             ["Guardianship or conservatorship", "Dorchester County Probate Court", "Berkeley County Probate Court"],
             ["Recording a deed or power of attorney", "Dorchester County Register of Deeds", "Berkeley County Register of Deeds"],
             ["A traffic stop by the sheriff or Highway Patrol", "Dorchester County magistrate", "Berkeley County magistrate"],
             ["A felony charge", "Dorchester County General Sessions, St. George", "Berkeley County General Sessions, Moncks Corner"],
             ["Bond hearing after arrest", "Dorchester County Detention Center, Hodge Road, Summerville", "Hill-Finklea Detention Center, Moncks Corner"],
         ]) +
         '<p>Inside the Summerville town limits—which also cross the county line—Summerville Municipal Court hears town-police tickets and ordinance cases regardless of county.</p>'
         '<h2>Why it matters for planning</h2>'
         f'<p>Estates are probated where the person was domiciled at death, so a Cane Bay retiree\'s estate goes to Moncks Corner even though every relative assumes Dorchester. A durable power of attorney is recorded in the county of residence. And when families file in the wrong court, the case is dismissed and refiled—weeks lost during a hard time. Our {A("probate-courts", "guide to the three probate courts")} has addresses and phones for each.</p>'
         '<h2>Why it matters for a charge</h2>'
         f'<p>Which sheriff\'s office made the arrest and which solicitor\'s office prosecutes are county questions too, although Dorchester and Berkeley share the First Judicial Circuit solicitor. Jack appears in both counties\' courts; see {A("service-areas/nexton", "Nexton")}, {A("service-areas/cane-bay", "Cane Bay")} and {A("service-areas/carnes-crossroads", "Carnes Crossroads")} for the specifics.</p>'
         + callout("<b>Frost first:</b> if you are opening an estate for someone who lived in a 29486 address, check the county before you file anything. It is the single most common wrong-court filing we see.")
     ),
     sources=src("berkeley_county", "dorchester_county", "berkeley_probate_site", "dorchester_probate_site"),
     related=["probate-courts", "service-areas/nexton", "service-areas/cane-bay"],
     faqs=[("Is Nexton in Dorchester or Berkeley County?", "Berkeley County, with a Summerville mailing address (ZIP 29486)."),
           ("Which probate court handles a Cane Bay estate?", "Berkeley County Probate Court in Moncks Corner.")])
