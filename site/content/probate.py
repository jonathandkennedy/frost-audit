"""Probate hub and spokes."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
from . import firm
from .local import cite, link

HUB = "probate"
TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'


def sp(slug, **kw):
    kw.setdefault("kind", "spoke")
    kw.setdefault("hub", HUB)
    kw.setdefault("eyebrow", "Probate · Summerville, SC")
    return page(slug, **kw)


hub_body = (
    answer("Frost Law Group handles probate and estate administration in the Dorchester, Berkeley and Charleston County probate courts—opening the estate, guiding the personal representative, dealing with creditors, and distributing and closing. Tara L. Frost served as a Dorchester County Associate Probate Judge from 2025 to 2026.", "Who helps with probate and estate administration in Summerville, SC?")
    + '<h2>What probate is</h2>'
    '<p>Probate is the court-supervised process of settling a person\'s affairs after death: proving the will (if there is one), appointing a personal representative, paying valid debts and taxes, and distributing what remains to the heirs or beneficiaries. In South Carolina it happens in the probate court of the county where the person lived—Dorchester County for Summerville, Berkeley County for Goose Creek and Moncks Corner, Charleston County for North Charleston, Charleston and Mount Pleasant.</p>'
    '<p>Not every estate needs full probate. The size of the estate, how assets are titled, and whether a valid will exists all change the path. We evaluate each family\'s situation and recommend the simplest route that works.</p>'
    '<h2>How we help</h2>'
    '[[cards:probate-process,executor-duties,small-estate-affidavit,probate-courts]]'
    '<h2>When there is a dispute</h2>'
    '<p>Probate is not always smooth. When heirs disagree, a personal representative will not account, or a will looks wrong, the probate court decides—and the family needs an attorney who knows how those hearings run.</p>'
    '[[cards:executor-disputes,will-contests,guardianship-and-conservatorship,trust-administration]]'
    '<h2>The South Carolina probate timeline, briefly</h2>'
    + steps([
        ("Deliver the will and open the estate.", f" Whoever holds the original will must deliver it to the probate court promptly after death ({cite('will_delivery', 'S.C. Code § 62-2-901')}). The court appoints the personal representative and issues letters (certificates of appointment)."),
        ("Notice to creditors.", f" A notice is published; creditors have eight months from first publication to file claims ({cite('creditor_period', 'S.C. Code § 62-3-801')}). This is why no South Carolina estate closes in less than eight months."),
        ("Inventory and appraisement.", " The personal representative files an inventory of the estate's assets and values within the time the court sets."),
        ("Pay debts, taxes and expenses.", " Valid claims are paid in the statutory order; final income tax returns are filed."),
        ("Distribute and close.", " Assets go to beneficiaries, receipts are collected, and a final accounting or application for settlement closes the estate."),
    ]) +
    '<h2>Assets that go through probate—and those that do not</h2>'
    + table(["Goes through probate", "Passes outside probate"], [
        ["Property titled solely in the decedent's name", "Assets in a properly funded revocable living trust"],
        ["Real estate owned individually, with no survivorship or transfer-on-death deed", "Jointly owned property with right of survivorship"],
        ["Bank and investment accounts with no beneficiary designation", "Life insurance and retirement accounts with a named living beneficiary"],
        ["Vehicles, jewelry and household goods with no surviving joint owner", "Accounts with payable-on-death or transfer-on-death designations"],
    ]) +
    f'<p>Planning ahead can keep most of an estate out of court. {A("revocable-trust", "Revocable trusts")}, beneficiary designations and transfer-on-death provisions let assets pass directly to your family. Ask us how to build a plan that works.</p>'
    '<h2>Why families in Summerville choose us for probate</h2>'
    + checks(["Tara Frost sat as an Associate Probate Judge in Dorchester County and as a Magistrate Judge before that; she knows what the court needs to see and what slows a file down.",
              "We tell you when you do not need us—small estates and simple affidavits included.",
              "Flat fees for uncontested estates where the facts allow it, quoted in writing.",
              "One office for probate, guardianship and estate planning, so the estate we close can end with a plan for the survivors."]) +
    band("We are here to help your family.", "Probate can feel overwhelming after a loss. Call and we will tell you what the court will need and what you can do yourself.")
)
page(HUB, kind="hub", section_label="Probate services",
     title="Probate Attorney in Summerville, SC | Dorchester, Berkeley & Charleston County Estates",
     description="Summerville, SC probate attorney Tara Frost, a former Dorchester County Associate Probate Judge, guides families through estate administration, executor duties, small estates, will contests and guardianship.",
     h1="Probate Attorney in Summerville, SC", eyebrow="Guiding families through the probate process", nav_label="Probate", hero_image="hero-probate.jpg", hero_caption="Probate court",
     lead="Losing a loved one is hard enough. Let Frost Law Group handle the legal process so your family can focus on what matters most.",
     summary="Estate administration, executor guidance, small estates, disputes and guardianship.",
     body=hub_body, priority=0.9,
     faqs=[
         ("How long does probate take in South Carolina?", "Eight months to a year for a typical uncontested estate, because creditors have eight months to file claims. Contested estates, real estate sales and tax issues take longer."),
         ("Do I need a lawyer to probate an estate?", f"Not always. Small estates and simple ones with cooperative heirs can often be handled by the personal representative with the court's forms. We will tell you which yours is. See {A('small-estate-affidavit', 'small estate affidavits')}."),
         ("What does a probate attorney cost?", "For uncontested estates we usually quote a flat fee once we see the assets and the will; contested matters are billed hourly with a written estimate. Fees are paid from the estate, not by the personal representative personally."),
     ])

sp("probate-process",
   title="The South Carolina Probate Process, Step by Step | Summerville Probate Attorneys",
   description="What happens from the day of death to the day the estate closes in a South Carolina probate court: delivering the will, appointment, creditor notice, inventory, taxes, distribution and closing. Summerville attorneys explain.",
   h1="The South Carolina Probate Process, Step by Step", nav_label="The probate process",
   lead="What actually happens, in order, from the first week after a death to the day the court closes the estate.",
   summary="Every step from delivering the will to closing the estate, with the deadlines that matter.",
   body=(
       '<h2>The first two weeks</h2>'
       f'<p>Locate the original will and deliver it to the probate court of the county where the person lived; South Carolina requires whoever holds it to do so ({cite("will_delivery", "S.C. Code § 62-2-901")}). Order several certified death certificates. Secure the home and vehicles, forward mail, and do not distribute anything—not even personal items—until the personal representative is appointed. Nothing else is urgent.</p>'
       '<h2>Step by step</h2>'
       + steps([
           ("Application or petition.", " The person named in the will (or, with no will, the person with statutory priority—usually the spouse or an heir) applies to the probate court to be appointed. Most estates open informally, without a hearing; a formal petition is used when a will is questioned or heirs disagree."),
           ("Appointment and letters.", " The court issues letters testamentary or letters of administration—the document banks, the DMV and title companies will ask for. A bond may be required unless the will waives it or the heirs consent."),
           ("Notice to creditors.", f" The court publishes notice; creditors have eight months from first publication to present claims ({cite('creditor_period', 'S.C. Code § 62-3-801')}). Known creditors should be notified directly."),
           ("Inventory and appraisement.", " A sworn list of the estate's assets and their date-of-death values, filed with the court on its form. Real estate, vehicles, accounts, business interests and personal property are all included; appraisals are used where values are not obvious."),
           ("Managing the estate.", " Open an estate bank account under a new tax ID, collect assets, keep insurance in force, and keep every receipt. The personal representative acts as a fiduciary and can be held personally responsible for losses."),
           ("Claims, debts and taxes.", " Allow or deny each claim in writing. Pay valid debts in the statutory order of priority. File the decedent's final income tax return and, if the estate earns income, a fiduciary return."),
           ("Distribution.", " After the creditor period closes and debts are paid, distribute according to the will or intestacy statute and collect signed receipts from each beneficiary. Real estate passes by deed of distribution."),
           ("Closing.", " File the final accounting (or an application for settlement with waivers from the beneficiaries). The court approves it and discharges the personal representative."),
       ]) +
       '<h2>How long it takes</h2>'
       '<p>Because of the creditor period, the fastest an ordinary South Carolina estate closes is a little over eight months. Ten to fourteen months is common. Real estate that must be sold, a business, an out-of-state asset, a tax audit or a family disagreement can stretch it to two years or more.</p>'
       '<h2>What can go wrong</h2>'
       + checks(["Distributing early and running out of money for a late creditor claim—the personal representative pays it personally",
                 "Missing the inventory deadline or filing values that cannot be supported",
                 "Commingling estate money with personal accounts",
                 "Selling real estate without the authority the will or court gives",
                 "Letting a beneficiary take the truck and the tools before the accounting"]) +
       f'<p>Most of these are avoidable with a checklist and a phone call. Our {A("executor-duties", "guide for personal representatives")} goes deeper.</p>'
       + band("Need a hand with an estate?", "Bring the will and a list of assets. We will map the process and tell you which steps you can do yourself.")
   ),
   faqs=[
       ("What is the difference between informal and formal probate?", "Informal probate is handled by the court's staff without a hearing and works when the will is clear and nobody objects. Formal probate is a court proceeding with notice and a judge's order, used when there is a dispute or a defect to resolve."),
       ("Can the personal representative be paid?", "Yes. South Carolina allows a reasonable commission, generally up to five percent of the personal property received, and reimbursement of expenses."),
   ],
   related=["executor-duties", "small-estate-affidavit", "probate-courts"])

sp("executor-duties",
   title="Executor (Personal Representative) Duties in South Carolina | Summerville Probate Attorney",
   description="What a South Carolina personal representative must do, in what order, with which deadlines—and the mistakes that create personal liability. Guidance from a former Dorchester County probate judge.",
   h1="Executor and Personal Representative Duties in South Carolina", nav_label="Executor duties",
   lead="You were named in the will, or the family chose you. Here is what the job actually involves, and where people get into trouble.",
   summary="The personal representative's checklist, deadlines and liabilities.",
   body=(
       answer("A South Carolina personal representative (executor) must deliver the will, get appointed, notify creditors, inventory and safeguard the assets, pay valid debts and taxes in the right order, distribute to the right people, account to the court, and act loyally and prudently throughout. Frost Law Group advises personal representatives in the Dorchester, Berkeley and Charleston County probate courts on every step.", "What does an executor of a will do in Summerville, SC?")
       + '<h2>The job, in order</h2>'
       + steps([
           ("Get appointed before you act.", " Until the court issues letters, you have no authority. Do not close accounts, sell anything or promise distributions."),
           ("Protect the assets.", " Change locks if needed, keep homeowner's and auto insurance in force, secure valuables, and collect mail. Photograph the contents of the home before family members remove anything."),
           ("Open an estate account.", " Get an EIN for the estate, open a checking account in the estate's name, and run every dollar through it. Never mix estate money with your own."),
           ("Notify and communicate.", " Creditors, the Social Security Administration, pension plans, insurers, and the beneficiaries. Beneficiaries are entitled to information; silence causes disputes."),
           ("Inventory.", " List every asset with a date-of-death value and file it on the court's form. Get appraisals for real estate, vehicles and collections."),
           ("Handle claims.", f" Review each claim, allow or disallow it in writing, and pay allowed claims in statutory priority after the creditor period ({cite('creditor_period', 'S.C. Code § 62-3-801')}). Funeral expenses, administration costs and taxes come before general creditors."),
           ("Taxes.", " File the decedent's final Form 1040 and SC1040, a fiduciary return if the estate earns income, and property taxes on real estate the estate holds."),
           ("Distribute and account.", " Distribute per the will or statute, get signed receipts, and file the accounting the court requires to close."),
       ]) +
       '<h2>Standards you are held to</h2>'
       '<p>A personal representative is a fiduciary: you must act in the beneficiaries\' interest, not your own, with the care a prudent person uses with their own affairs. You cannot buy estate property for yourself without court approval or beneficiary consent, favor one beneficiary, or use estate funds for personal expenses. Breaches lead to surcharge—paying the loss from your own pocket—and removal.</p>'
       '<h2>Compensation</h2>'
       '<p>South Carolina allows a reasonable commission, generally up to five percent of the personal property the estate receives (real estate is treated differently), plus reimbursement of legitimate expenses. Many family members waive it; the choice is yours, and it should be documented.</p>'
       '<h2>When you should call a lawyer</h2>'
       + checks(["The estate includes real estate to sell, a business, or out-of-state property", "A creditor claim looks wrong or large", "A beneficiary is unhappy, unreachable, a minor, or receiving benefits", "The will is unclear, was changed late in life, or is being questioned", "You are unsure whether an asset is a probate asset at all"]) +
       f'<p>If a dispute has already started, see {A("executor-disputes", "executor and beneficiary disputes")}.</p>'
       + band("Named as executor?", "We will walk you through the appointment and give you the checklist, whether or not you hire us for the rest.")
   ),
   faqs=[
       ("Can I be removed as personal representative?", "Yes, by the court, for mismanagement, conflict of interest, failure to account or failure to act. Beneficiaries petition; a hearing follows."),
       ("Do I have to serve if I was named?", "No. You can decline, and the alternate named in the will (or the next person with priority) is appointed instead."),
       ("Am I personally liable for the decedent's debts?", "Not for the debts themselves—only for losses you cause by mishandling the estate, such as distributing before paying a valid claim."),
   ],
   related=["probate-process", "executor-disputes", "probate-courts"])

sp("executor-disputes", card_new=True,
   title="Executor Disputes in Summerville, SC Probate Court | Frost Law Group",
   description="Who handles executor disputes in Summerville, SC probate court: removal petitions, demands for an accounting, self-dealing claims and contested distributions in Dorchester, Berkeley and Charleston counties. Former probate judge.",
   h1="Executor and Beneficiary Disputes in Summerville, SC Probate Court", nav_label="Executor disputes",
   lead="When the person running the estate is not doing the job—or is accused of it—the probate court decides. We represent both sides.",
   summary="Removal petitions, accountings, self-dealing and contested distributions.",
   body=(
       answer("Frost Law Group represents beneficiaries who believe an estate is being mishandled and personal representatives who are accused of it, in the Dorchester, Berkeley and Charleston County probate courts. Tara L. Frost served as a Dorchester County Associate Probate Judge and knows how these hearings are decided.", "Who handles executor disputes in Summerville, SC probate court?")
       + '<h2>Disputes we see most often</h2>'
       + checks(["<b>No information.</b> The personal representative will not share the inventory, the accounting or the will. Beneficiaries have a right to reasonable information and can petition the court to compel it.",
                 "<b>Delay.</b> The estate has been open for years with no accounting and no distribution.",
                 "<b>Self-dealing.</b> The personal representative bought the house cheaply, sold the truck to a cousin, or paid themselves fees nobody agreed to.",
                 "<b>Missing assets.</b> Accounts emptied before or after death, often under a power of attorney that should have ended at death.",
                 "<b>Unequal treatment.</b> One sibling's loan forgiven, another's counted; the house given to the child who lived in it.",
                 "<b>A questionable will.</b> If the dispute is really about whether the will is valid, see " + A("will-contests", "will contests") + "."]) +
       '<h2>What the probate court can do</h2>'
       '<p>Order an accounting; surcharge the personal representative for losses; remove and replace them; void improper sales; require a bond; award attorney\'s fees against a fiduciary who acted in bad faith; and, where property is being dissipated, act quickly on a motion. Most disputes settle once a judge orders the numbers onto the table.</p>'
       '<h2>If you are the personal representative</h2>'
       '<p>Being accused is not the same as being wrong. Beneficiaries frequently misunderstand why an estate stays open for eight months, why real estate cannot be given away before debts are paid, or why a commission is allowed. Good records and a prompt, complete accounting end most complaints. We help personal representatives prepare the accounting and respond to a petition without escalating the family fight.</p>'
       '<h2>Timing</h2>'
       '<p>Objections to an accounting or a proposed distribution must be raised before the court approves them; once an estate is closed, reopening it is harder and sometimes impossible. If you have received a notice of a proposed settlement, call before the date on it.</p>'
       + band("Estate not being handled right?", "Bring what you have—notices, the will, bank statements. We will tell you whether the court can help and what it will cost to find out.")
   ),
   faqs=[
       ("Can a beneficiary demand an accounting in South Carolina?", "Yes. Beneficiaries can request information informally and petition the probate court to compel a formal accounting if it is refused."),
       ("How do I remove an executor in South Carolina?", "File a petition for removal in the probate court stating the grounds—mismanagement, conflict of interest, failure to account or failure to act—and the court holds a hearing."),
       ("Does the estate pay my attorney's fees?", "Sometimes. The court can award fees from the estate when the action benefited the estate, and against a fiduciary who acted in bad faith. Ask us to assess your case."),
   ],
   related=["executor-duties", "will-contests", "trust-administration"])

sp("small-estate-affidavit",
   title="Small Estate Affidavit in South Carolina | Summary Administration | Summerville Attorneys",
   description="When a South Carolina estate can skip full probate: the $25,000 small-estate affidavit for personal property, summary administration, what counts toward the limit, and how to file in Dorchester, Berkeley or Charleston County.",
   h1="Small Estate Affidavits and Summary Administration in South Carolina", nav_label="Small estates",
   lead="Not every estate needs eight months of probate. Here is when a South Carolina family can use a simple affidavit instead—and when it cannot. The limit rose to $45,000 in 2025.",
   summary="The $45,000 affidavit and the summary procedure for small estates.",
   body=(
       answer(f"If the entire probate estate—everything passing under the will or by intestacy, less liens—is worth $45,000 or less and at least thirty days have passed since death, a successor can collect the decedent's personal property with a small estate affidavit under {cite('small_estate', 'S.C. Code § 62-3-1201')}, approved by the probate judge, instead of opening a full estate. The ceiling rose from $25,000 to $45,000 in May 2025. Frost Law Group prepares the affidavit and tells you first whether you qualify.", "The short answer")
       + '<h2>Who qualifies</h2>'
       + checks(["A total probate estate—bank accounts, vehicles, final paychecks, refunds, household goods, anything passing under the will or by intestacy—of $45,000 or less after subtracting liens",
                 "The affidavit transfers personal property; real estate titled solely in the decedent's name still needs a deed of distribution through the court, so a house usually means a regular estate",
                 "At least thirty days since the death",
                 "No personal representative already appointed or application pending",
                 "The person signing is entitled to the property—an heir under the will or intestacy statute"]) +
       '<h2>How it works</h2>'
       + steps([("Gather the numbers.", " Statements, titles and the death certificate. Value vehicles at fair market value."),
                ("Complete the affidavit.", " The probate court provides the form; it is sworn, approved and countersigned by the probate judge of the county where the decedent lived, and filed there with a small fee."),
                ("Present it.", " The certified affidavit is presented to the bank, the DMV or the employer, who must release the property to the affiant."),
                ("Distribute honestly.", " The affiant holds the property for the heirs and is accountable to them and to creditors.")]) +
       '<h2>What does not count toward the limit</h2>'
       '<p>Assets that pass outside probate are not part of the calculation: life insurance and retirement accounts with named beneficiaries, jointly owned accounts with survivorship, payable-on-death accounts, and anything in a trust. A family with a $300,000 house held jointly, a $200,000 IRA with a named beneficiary and a $30,000 checking account in Dad\'s name alone can often use the affidavit for the checking account.</p>'
       '<h2>When an affidavit is the wrong tool</h2>'
       '<p>Real estate in the decedent\'s name alone, a vehicle with a loan larger than its value, a lawsuit or injury claim to pursue, or heirs who disagree all call for a regular estate—informal probate is still fairly simple in those cases, and a summary administration may be available when the estate does not exceed exempt property, family allowances and administration expenses.</p>'
       + callout(f"<b>Frost first:</b> the bank will not tell you whether an affidavit is correct; it will simply accept or reject it. Filing one for an estate that needed probate creates personal liability to creditors and heirs. A ten-minute call sorts it out: {TEL}.")
       + band("Is your family's estate small enough?", "Tell us what was owned and how it was titled. If an affidavit will do, we will say so.")
   ),
   faqs=[
       ("Can I use a small estate affidavit for a house?", "No. Real estate in the decedent's name passes through a regular probate estate, even when the rest of the estate is small."),
       ("What is the fee?", "The probate court charges a modest filing fee for the affidavit, far less than the graduated fee for a full estate."),
   ],
   related=["probate-process", "executor-duties", "probate-courts"])

sp("will-contests", card_new=True,
   title="Will Contests & Probate Litigation in Summerville, SC | Frost Law Group",
   description="Grounds to contest a will in South Carolina—lack of capacity, undue influence, fraud and improper execution—who can bring one, the deadlines, and how the probate court decides. Summerville probate litigation attorneys.",
   h1="Will Contests and Probate Litigation in Summerville, SC", nav_label="Will contests",
   lead="When a will does not look like what your parent would have signed, South Carolina gives you a way to ask the court. It also gives you a deadline.",
   summary="Capacity, undue influence, fraud and execution challenges, and the deadlines to raise them.",
   body=(
       '<h2>Grounds to contest a will in South Carolina</h2>'
       + checks(["<b>Lack of testamentary capacity.</b> The person did not understand what they owned, who their family was, or what the will did—common with late-life dementia.",
                 "<b>Undue influence.</b> Someone in a position of trust—a caregiver, a new spouse, one child—substituted their wishes for the testator's. Isolation, a sudden change in the plan, and involvement in getting the will drafted are the classic signs.",
                 "<b>Fraud or forgery.</b> The signature is not genuine, or the person was deceived about what they were signing.",
                 "<b>Improper execution.</b> Missing or interested witnesses, unsigned pages, or a document that does not meet " + cite("will_execution", "S.C. Code § 62-2-502") + ".",
                 "<b>Revocation or a later will.</b> A newer valid will, or a physical act of revocation, replaced the one offered."]) +
       '<h2>Who can contest</h2>'
       '<p>An “interested person”—someone who would inherit more if the will failed: heirs under intestacy law, beneficiaries under an earlier will, and sometimes creditors. Being unhappy with a will is not enough; being harmed by it is.</p>'
       '<h2>Deadlines</h2>'
       '<p>A will admitted informally can be challenged in a formal proceeding, but generally only within the later of eight months after informal probate or one year after death; a will admitted formally after notice must be challenged by appeal. Once those windows close, the will stands. If you have received a notice from a probate court, the clock is already running—call before it stops.</p>'
       '<h2>How a contest proceeds</h2>'
       + steps([("Petition.", " A formal petition is filed in the probate court stating the grounds; the personal representative and beneficiaries are served."),
                ("Discovery.", " Medical records, the drafting attorney's file, bank records, witness statements. This is where most contests are won or lost."),
                ("Mediation.", " Probate courts routinely order it, and most contests settle here—often by adjusting shares rather than throwing out the will."),
                ("Trial.", " Before the probate judge or, on request, removed to circuit court for a jury. The contestant carries the burden on capacity and undue influence.")]) +
       '<h2>Defending a will</h2>'
       '<p>We also represent personal representatives and beneficiaries defending a will that reflects exactly what the person wanted—often a parent who chose to leave more to the child who cared for them. A well-drafted, properly witnessed, self-proved will with a lawyer\'s file behind it is hard to overturn.</p>'
       + band("Think a will is wrong?", "Bring the will, the notice and what you know about how it was signed. We will give you a candid read on the case and the deadline.")
   ),
   faqs=[
       ("What does a will contest cost?", "Contested matters are billed hourly with a written estimate. Some cases warrant a contingency arrangement; ask."),
       ("Can a no-contest clause stop me?", "South Carolina enforces them only against contests brought without probable cause. A contest with a genuine basis does not trigger the penalty."),
   ],
   related=["executor-disputes", "probate-process", "trust-administration"])

sp("guardianship-and-conservatorship", card_new=True,
   title="Guardianship & Conservatorship Attorney in Summerville, SC | Adults & Minors",
   description="Guardianship (person) and conservatorship (finances) for an incapacitated adult or a minor in Dorchester, Berkeley and Charleston County probate courts—including contested cases. Former probate judge Tara Frost.",
   h1="Guardianship and Conservatorship in Summerville, SC", nav_label="Guardianship & conservatorship",
   lead="When a parent can no longer manage safely, or a child needs a legal decision-maker, the probate court can appoint one. Here is how it works and how to avoid it when you can.",
   summary="Court-appointed decision-makers for adults who cannot manage and for minors—contested or not.",
   body=(
       answer("Frost Law Group handles guardianship and conservatorship petitions in the Dorchester, Berkeley and Charleston County probate courts, including contested cases where family members disagree about who should serve or whether the person is incapacitated. Tara L. Frost served as a Dorchester County Associate Probate Judge, where these cases are heard.", "Which attorneys in Summerville, SC handle contested guardianship cases?")
       + answer("Yes. We handle guardianship of minors—when parents have died, are absent, or cannot care for a child—and conservatorships to manage money a minor inherits or receives from a settlement.", "Which Summerville, SC attorneys help with guardianship of minors?")
       + '<h2>Guardianship vs. conservatorship</h2>'
       + table(["", "Guardian", "Conservator"], [
           ["Decides about", "The person: housing, medical care, daily life", "The money: accounts, bills, property, benefits"],
           ["Appointed when", "An adult cannot make or communicate responsible personal decisions, or a minor needs a decision-maker", "An adult cannot manage finances, or a minor receives funds"],
           ["Court", "Probate court of the county where the person lives", "Same"],
           ["Ongoing duties", "Annual report on the person's condition", "Inventory, bond, and annual accountings"],
       ]) +
       '<h2>Adult guardianship and conservatorship</h2>'
       f'<p>Under South Carolina\'s adult guardianship and protective proceedings statutes ({cite("guardianship", "S.C. Code Title 62, Article 5")}), a petition is filed in probate court with medical evidence of incapacity. The court appoints a guardian ad litem and examiners to evaluate the person, notifies family members, and holds a hearing. The alleged incapacitated person has the right to counsel and to object. If incapacity is proven, the court appoints the guardian or conservator with the powers the person actually needs—no more—and may order a limited guardianship.</p>'
       '<h2>When families disagree</h2>'
       '<p>Contested cases arise when siblings each want to serve, when a parent objects to any guardian, or when one relative believes another is exploiting the parent. The court decides based on the person\'s best interest and statutory priorities, with evidence about each candidate\'s suitability. We prepare these cases the way the court evaluates them: medical proof, financial records, and a concrete plan for the person\'s care.</p>'
       '<h2>Guardianship of minors</h2>'
       '<p>A guardian for a minor may be nominated in a parent\'s will and confirmed by the probate court, or appointed after a petition when parents are unable to act. A conservatorship is required when a minor receives significant funds—an inheritance, life insurance or a settlement—and the money is held under court supervision until the child turns eighteen. Structured settlements and trusts can reduce or avoid the need.</p>'
       '<h2>Avoiding a guardianship</h2>'
       f'<p>Most adult guardianships happen because no one signed a {A("power-of-attorney", "durable power of attorney and health care power of attorney")} while they could. If a parent still has capacity—even limited, fluctuating capacity—those documents may still be signed, and they are faster, cheaper and private. We will tell you honestly which path is available.</p>'
       '<h2>Serving as guardian or conservator</h2>'
       '<p>The role comes with reports, accountings, and personal responsibility for the person\'s welfare or money. We help guardians and conservators file what the court requires, obtain permission for major decisions, and close the case when it ends.</p>'
       + band("Worried about a parent or a child?", "Call. We will tell you whether a guardianship is needed, whether a power of attorney can still be signed, and what the court will require.")
   ),
   faqs=[
       ("How long does a guardianship take in South Carolina?", "Uncontested adult cases commonly take two to four months from filing to hearing, depending on the county's docket and how quickly examiners report. Emergency appointments are available when the person is in immediate danger."),
       ("Can a guardian move a parent to a facility?", "Generally yes, but South Carolina restricts certain placements and treatment decisions without additional court approval. The order sets the limits."),
       ("Does a guardian get paid?", "Family guardians often serve without pay; the court can approve reasonable compensation from the protected person's funds."),
   ],
   related=["power-of-attorney", "special-needs-planning", "probate-courts"])

sp("trust-administration", card_new=True,
   title="Trust Administration & Inherited Assets in Summerville, SC | Trustee Duties",
   description="Help for trustees and beneficiaries after a death: trustee duties under the South Carolina Trust Code, notices and accountings, managing and distributing inherited assets, and resolving trust disputes. Summerville attorneys.",
   h1="Trust Administration and Inherited Assets in Summerville, SC", nav_label="Trust administration",
   lead="A trust avoids probate, but it does not administer itself. What a successor trustee must do, and how beneficiaries make sure it is done.",
   summary="Trustee duties, notices and accountings, and managing an inheritance.",
   body=(
       answer("Frost Law Group advises successor trustees on administering a trust after a death—notices, inventories, taxes, distributions and accountings under the South Carolina Trust Code—and helps beneficiaries manage or protect what they inherit, including inherited retirement accounts and real estate.", "Who can assist with managing inherited assets in Summerville, SC?")
       + '<h2>The successor trustee\'s job</h2>'
       + steps([("Accept the role and get the paperwork.", " A certification of trust, the death certificate and a tax ID for the now-irrevocable trust let you deal with banks and brokerages."),
                ("Notify beneficiaries.", f" South Carolina's Trust Code ({cite('trust_code', 'S.C. Code § 62-7-813')}) requires the trustee to keep qualified beneficiaries reasonably informed—including notice of the trust's existence, the trustee's contact information and the right to a copy of the trust."),
                ("Inventory and value.", " Everything the trust owns, at date-of-death value, which also sets the new income-tax basis for most assets."),
                ("Pay and file.", " Final expenses, valid debts, and the decedent's and trust's tax returns."),
                ("Distribute per the document.", " Outright shares, continuing trusts for young or vulnerable beneficiaries, or a marital trust—exactly as written, with receipts."),
                ("Account.", " Beneficiaries are entitled to a report of the trust's assets, liabilities, receipts and disbursements at least annually and at termination.")]) +
       '<h2>Managing what you inherit</h2>'
       + checks(["<b>Inherited retirement accounts</b> follow strict federal timing rules; most non-spouse beneficiaries must empty the account within ten years. The election you make in the first year matters.",
                 "<b>Inherited real estate</b> usually receives a stepped-up basis; keep the appraisal. Decide early whether to keep, rent or sell, and who pays carrying costs meanwhile.",
                 "<b>A continuing trust for you</b> means a trustee decides distributions; you have rights to information and to ask the court if the trustee is unreasonable.",
                 "<b>Inheritance and your own plan.</b> A large inheritance is the moment to review your own will, beneficiary designations and asset-protection planning."]) +
       '<h2>When trusts go wrong</h2>'
       '<p>A trustee who will not communicate, mixes trust money with their own, favors one beneficiary, or simply does nothing can be compelled to act or removed by the probate court. We represent beneficiaries in those petitions and trustees who need to respond to them.</p>'
       + band("Just became a trustee—or a beneficiary?", "Bring the trust and the account statements. We will give you the checklist and the deadlines.")
   ),
   faqs=[
       ("Does a trust go through probate?", "No, if it was funded. Assets left outside the trust in the decedent's name may still require probate or a small estate affidavit."),
       ("Can a trustee be paid?", "Yes, reasonable compensation as the trust provides or the Trust Code allows, and reimbursement of expenses."),
   ],
   related=["revocable-trust", "executor-disputes", "high-net-worth-estate-planning"])

sp("probate-courts", card_new=True,
   title="Dorchester, Berkeley & Charleston County Probate Courts | Guide for Summerville Families",
   description="Where to file, what to bring and what to expect at the Dorchester County (St. George and Summerville), Berkeley County (Moncks Corner) and Charleston County probate courts. Addresses, phones and websites.",
   h1="Probate Courts Serving Summerville: Dorchester, Berkeley and Charleston Counties", nav_label="Probate courts guide",
   lead="Which court handles your family's estate, guardianship or trust matter depends on where the person lived. Here is where each court is and how it works.",
   summary="Addresses, phones and practical notes for the three probate courts we appear in.",
   body=(
       '<h2>Which court has your case</h2>'
       '<p>Estates are opened in the probate court of the county where the decedent was domiciled at death. Guardianships and conservatorships are filed where the person lives (or, for a minor, where the minor resides or has property). A Summerville address can fall in Dorchester <em>or</em> Berkeley County—Nexton, Cane Bay and Carnes Crossroads are Berkeley—so check the county on the property tax bill or voter registration before filing.</p>'
       '<h2>Dorchester County Probate Court</h2>'
       '<p>The Dorchester County Probate Court sits in the county courthouse complex in St. George, about half an hour up Highway 78 from Summerville. Tara Frost served here as an Associate Probate Judge; the court is busy, and files move faster when forms are complete and valuations are supported.</p>'
       '[[courts:dorchester_probate]]'
       '<h2>Berkeley County Probate Court</h2>'
       '<p>Berkeley County\'s probate court is in Moncks Corner. Goose Creek, Hanahan, Moncks Corner, Ladson addresses on the Berkeley side, and the Nexton and Cane Bay communities file here.</p>'
       '[[courts:berkeley_probate]]'
       '<h2>Charleston County Probate Court</h2>'
       '<p>Charleston County\'s probate court is in downtown Charleston. North Charleston, Charleston, Mount Pleasant, West Ashley, James Island, Johns Island and Daniel Island estates file here. Parking is metered; allow time.</p>'
       '[[courts:charleston_probate]]'
       '<h2>What to bring to open an estate</h2>'
       + checks(["The original will, if any, and any codicils", "A certified death certificate", "Names and addresses of heirs and beneficiaries", "A preliminary list of assets and approximate values, and known debts", "Photo identification and the filing fee, which is set by statute on a sliding scale"]) +
       '<h2>Practical notes</h2>'
       + checks(["Most filings use the court's own forms; the South Carolina Judicial Branch publishes them statewide, and each court has local practices about scheduling and notice.",
                 "Hearings in contested matters are before the probate judge; jury trials are available by removal to circuit court in limited cases.",
                 "Clerks cannot give legal advice; they can tell you which form applies and whether a filing is complete."]) +
       f'<p>Court addresses and hours change; the details above were checked against the counties\' websites in September {firm.BUILD_DATE[:4]}. Call the court, or us, before you drive.</p>'
       + band("Not sure which court?", "Tell us the address and what needs to be filed. We will point you to the right courthouse and tell you what to bring.")
   ),
   faqs=[
       ("Can I file in Dorchester County if my father lived in Goose Creek?", "No. The estate is opened where he was domiciled—Berkeley County for most Goose Creek addresses."),
       ("Do I need to appear in person?", "For an uncontested informal estate, usually not; filings can be handled by mail or through counsel. Contested matters and guardianships involve hearings."),
   ],
   related=["probate-process", "small-estate-affidavit", "guardianship-and-conservatorship"])
