"""Estate planning hub and spokes. Statute links come from the verified local data (local.cite)."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
from . import firm
from .local import cite, link

HUB = "estate-planning-attorney"
TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'


def sp(slug, **kw):
    kw.setdefault("kind", "spoke")
    kw.setdefault("hub", HUB)
    kw.setdefault("eyebrow", "Estate planning · Summerville, SC")
    return page(slug, **kw)


# ----------------------------------------------------------------------------- HUB
hub_body = (
    '<h2>Why estate planning matters in South Carolina</h2>'
    f'<p>Without a plan, South Carolina law—not you—decides who inherits your estate, who raises your children and who manages your money if you cannot. The intestacy statute ({cite("intestacy", "S.C. Code § 62-2-102")}) gives a surviving spouse only half of an estate when there are children, and a court, not your family, appoints the person in charge. A complete plan replaces those defaults with your decisions, in documents the probate court and your bank will accept without argument.</p>'
    '<p>Frost Law Group prepares plans for families across Dorchester, Berkeley and Charleston counties. Tara Frost served as a Dorchester County Associate Probate Judge; she has read hundreds of wills and trusts from the bench and knows which ones cause trouble later.</p>'
    '<h2>What a complete estate plan includes</h2>'
    '<p>A thorough plan is more than a will. Each document below has its own page explaining what it does, why it matters here, and whether it belongs in your plan.</p>'
    '[[cards:last-will-and-testament,revocable-trust,power-of-attorney,living-will]]'
    '<h2>Planning for your situation</h2>'
    '<p>Most families need the four documents above. Many need one of these as well.</p>'
    '[[cards:asset-protection-trusts,estate-planning-for-blended-families,estate-planning-for-business-owners,special-needs-planning,high-net-worth-estate-planning,estate-plan-review]]'
    '<h2>How it works here</h2>'
    + steps([
        ("A conversation, not a questionnaire.", " We meet at the office (or by phone if you prefer) and talk through your family, your assets, and what worries you. You leave with a recommendation and a flat-fee quote."),
        ("Design.", " We draft the documents and send you a plain-English summary of what each one does. Changes are part of the price."),
        ("Signing.", " You sign at our office with the witnesses and notary South Carolina requires, so the will is self-proved and the powers of attorney are ready to record."),
        ("Funding and follow-through.", " Trusts only work if assets are titled to them. We give you a funding checklist, letters for your financial institutions, and deeds for Lowcountry real estate."),
        ("Reviews.", " Life changes—marriages, births, a move, a business sale. We review plans on request and recommend a look every three to five years."),
    ]) +
    '<h2>Questions and answers</h2>'
    f'<p>Short answers to the questions people in Summerville ask us and Google most often are on the pages linked above and on our {A("faq", "FAQ page")}. Two we hear every week:</p>'
    + answer("<b>Will or trust?</b> A will plus powers of attorney serves most families. A revocable living trust adds incapacity planning and keeps your estate out of probate, which matters most if you own real estate in more than one state, want privacy, or want to spare your family the eight-month probate timeline.", "Will or trust")
    + answer("<b>What happens without a will?</b> The estate is divided by statute among spouse and children (or parents, siblings and further relatives), a court chooses the personal representative, and a judge chooses the guardian for minor children.", "Without a will")
    + f'<p>{img("nest-egg.jpg", "Protecting your nest egg with a thoughtful estate plan in Summerville, SC")}</p>'
    + band("Plan today, rest easy.", "A single consultation with our Summerville estate planning attorneys can give you, and your family, real peace of mind.")
)
page(HUB, kind="hub", section_label="Estate planning services",
     title="Estate Planning Attorney in Summerville, SC | Wills, Trusts & POAs | Frost Law Group",
     description="Summerville, SC estate planning attorneys Jack and Tara Frost prepare wills, revocable living trusts, powers of attorney and living wills for Dorchester, Berkeley and Charleston County families. Flat fees.",
     h1="Estate Planning Attorney in Summerville, SC", eyebrow="Secure your legacy for generations", nav_label="Estate planning",
     lead="Protect your family's future with a complete estate plan tailored to your life, your values and South Carolina law. Our Summerville attorneys guide you every step of the way.",
     quote="“A good man leaves an inheritance to his children's children.” — Proverbs 13:22",
     summary="Wills, trusts, powers of attorney and living wills for South Carolina families.",
     body=hub_body, priority=0.9,
     faqs=[
         ("Do you offer flat fees for estate plans?", "Yes. Once we know what you need, we quote one price that covers drafting, changes and the signing meeting."),
         ("Do both spouses need their own will?", "Yes. Each spouse signs their own will and powers of attorney; a couple can share one revocable trust."),
         ("Can you update a plan from another state?", f"Yes. We review out-of-state and online documents and amend or restate them so they work under South Carolina law. See {A('estate-plan-review', 'plan reviews')}."),
     ])

# ----------------------------------------------------------------------------- SPOKES
sp("last-will-and-testament", card_new=False,
   title="Last Will and Testament Attorney in Summerville, SC | Frost Law Group",
   description="A South Carolina will names who inherits, who serves as personal representative and who raises your children. Summerville attorneys explain what a valid SC will requires and what happens without one.",
   h1="Last Will and Testament in Summerville, SC", nav_label="Last will and testament",
   lead="A legally valid will ensures your assets reach the people you choose, names a guardian for your minor children, and keeps the state out of your family's decisions.",
   summary="Who inherits, who is in charge, and who raises the kids—decided by you, not the statute.",
   body=(
       '<h2>What a last will and testament does</h2>'
       '<p>A will is the document the probate court uses to carry out your wishes after death. It names beneficiaries for property that passes through probate, appoints a personal representative (South Carolina\'s term for executor) to settle the estate, and—for parents of minor children—nominates a guardian. It can also create trusts for young or vulnerable beneficiaries, forgive debts, and direct how taxes and expenses are paid.</p>'
       '<h2>What your will can cover</h2>'
       + checks(["Who receives your home, accounts, vehicles and personal property, and in what shares",
                 "Specific gifts—a ring to a granddaughter, a truck to a son, a sum to your church",
                 "A guardian and an alternate for minor children",
                 "A personal representative and an alternate, and whether they must post a bond",
                 "A trust for a child's inheritance until an age you choose",
                 "What happens if a beneficiary dies before you"]) +
       '<h2>What South Carolina requires for a valid will</h2>'
       f'<p>Under {cite("will_execution", "S.C. Code § 62-2-502")}, a will must be in writing, signed by you, and signed by two witnesses who saw you sign or acknowledge it. South Carolina does not accept an unwitnessed handwritten will. Adding a self-proving affidavit before a notary ({cite("self_proved", "§ 62-2-503")}) lets the court admit the will without tracking down witnesses years later—we do this at every signing.</p>'
       '<h2>What happens without a will in South Carolina</h2>'
       f'<p>Your estate passes by the intestacy statute: a surviving spouse takes everything if you have no children, or half if you do, with the children sharing the rest. Step-children and unmarried partners receive nothing. A judge chooses the guardian for your children. Details are on {A("dying-without-a-will-in-south-carolina", "our page on dying without a will")}.</p>'
       '<h2>Is your will up to date?</h2>'
       '<p>A will written before a marriage, divorce, birth, death, or move to South Carolina should be reviewed. A will from another state is usually valid here, but the powers of attorney and health care documents that came with it often are not.</p>'
       + callout("<b>Frost first:</b> if a relative hands you a printed form will to sign, or a website offers a $49 will, let us read it before you rely on it. The most expensive wills we see are the ones that were free.")
       + band("Ready to protect your family?", "Call for a flat-fee quote on a will-based plan.")
   ),
   faqs=[
       ("Does a will avoid probate?", "No. A will directs probate; it does not avoid it. Assets with beneficiary designations, joint ownership and funded trusts pass outside probate."),
       ("Can I write my own will in South Carolina?", "You can, if it is signed by you and two witnesses. Most problems we see come from unclear wording, missing alternates and unsigned pages rather than the form itself."),
       ("Where should I keep my will?", "Somewhere your personal representative can find it—our office keeps a signed original for clients who ask. Whoever holds the original must deliver it to the probate court after your death."),
   ],
   related=["revocable-trust", "power-of-attorney", "dying-without-a-will-in-south-carolina"])

sp("revocable-trust",
   title="Revocable Living Trust Attorney in Summerville, SC | Frost Law Group",
   description="A revocable living trust lets your family skip probate, handles incapacity, and keeps your estate private. Summerville attorneys explain when a trust beats a will under South Carolina law.",
   h1="Revocable Living Trust in Summerville, SC", nav_label="Revocable living trust",
   lead="A flexible, private trust that helps your family avoid probate, transfer assets quickly, and protect your estate during incapacity—all while you remain in full control.",
   summary="Avoid probate, plan for incapacity, keep it private. When a trust is worth it.",
   body=(
       '<h2>What a revocable living trust is</h2>'
       '<p>A revocable living trust is a legal container you create during life and control completely. You are the trustee; you buy, sell and spend exactly as before. The difference is what happens when you cannot act or when you die: the successor trustee you named steps in immediately, without a court appointment, and distributes or manages the assets under the instructions you wrote. Because trust assets are not owned in your individual name, they do not go through probate.</p>'
       '<h2>Why Lowcountry families choose a revocable trust</h2>'
       + checks(["<b>No probate.</b> South Carolina estates stay open at least eight months for creditor claims; a funded trust distributes on your timeline.",
                 "<b>Incapacity.</b> If a stroke or dementia takes you out of the picture, your successor trustee manages the trust without a conservatorship hearing.",
                 "<b>Privacy.</b> A probated will is a public record at the county courthouse; a trust is not.",
                 "<b>Out-of-state property.</b> A beach house in North Carolina or a family farm in Georgia would otherwise require a second probate in that state.",
                 "<b>Control after death.</b> Hold an inheritance for a child until 25 or 30, protect a beneficiary who struggles with money, or provide for a spouse while preserving the remainder for your children."]) +
       '<h2>Revocable trust vs. a will—which do you need?</h2>'
       + table(["", "Will-based plan", "Trust-based plan"], [
           ["Probate", "Yes, in the county probate court", "No, if the trust is funded"],
           ["Incapacity", "Relies on a durable power of attorney", "Successor trustee steps in; POA still used for assets outside the trust"],
           ["Privacy", "Public record", "Private"],
           ["Upfront cost", "Lower", "Higher"],
           ["Ongoing work", "None", "Keep assets titled to the trust"],
           ["Best for", "Simpler estates, younger families", "Real estate in two states, blended families, privacy, larger estates"],
       ]) +
       '<h2>Who should consider a revocable trust</h2>'
       '<p>Owners of real estate in more than one state; blended families; anyone with a beneficiary who is a minor, has special needs, or is not ready for a lump sum; people who have watched a relative\'s probate drag on; and anyone who values privacy. Everyone with a trust still needs a short “pour-over” will and powers of attorney—the trust replaces probate, not the rest of the plan.</p>'
       '<h2>The step most people miss: funding</h2>'
       '<p>A trust controls only what it owns. Deeds for Lowcountry real estate must be recorded to the trustee, accounts retitled, and beneficiary designations coordinated. We prepare the deeds and letters and check the work at the end. An unfunded trust is the most common reason a family ends up in probate anyway.</p>'
       + band("Protect what you've built.", "Ask whether a trust-based plan is worth it for your family. We will tell you honestly if a will is enough.")
   ),
   faqs=[
       ("Does a revocable trust protect my assets from creditors or nursing homes?", f"No. Because you control it, a revocable trust is treated as yours. Protection requires an irrevocable trust; see {A('asset-protection-trusts', 'asset protection trusts')}."),
       ("Do I lose control of my property?", "No. You are the trustee and can change or revoke the trust at any time while you have capacity."),
       ("Can a married couple share one trust?", "Yes. Most married couples in South Carolina use one joint revocable trust."),
   ],
   related=["last-will-and-testament", "asset-protection-trusts", "trust-administration"])

sp("power-of-attorney",
   title="Power of Attorney Lawyer in Summerville, SC | Durable & Health Care POA",
   description="South Carolina durable and health care powers of attorney explained: what each agent can do, the Uniform Power of Attorney Act's recording rule, and how to choose agents. Summerville attorneys.",
   h1="Powers of Attorney in Summerville, SC", nav_label="Powers of attorney",
   lead="A durable power of attorney covers your finances and legal matters; a health care power of attorney names someone to make medical decisions. Both are essential when you cannot act for yourself.",
   summary="Financial and medical decision-makers, named by you and ready before a crisis.",
   body=(
       answer("Yes—Frost Law Group prepares durable (financial) powers of attorney, health care powers of attorney and living wills for Summerville families, usually as a set with a will or trust, and records the durable POA when the time comes.", "Which Summerville law firms help with living wills and powers of attorney?")
       + '<h2>Planning for the unexpected</h2>'
       '<p>If an accident or illness leaves you unable to manage your affairs, someone has to pay the mortgage, deal with the insurance company and talk to your doctors. Without powers of attorney, that someone must first ask the probate court to appoint a conservator and guardian—a public, expensive process that takes months. Two signatures now avoid it.</p>'
       '<h2>Durable power of attorney</h2>'
       f'<p>South Carolina\'s {cite("poa_act", "Uniform Power of Attorney Act (S.C. Code Title 62, Article 8)")} governs financial powers of attorney. “Durable” means it keeps working after you lose capacity. Your agent can:</p>'
       + checks(["Pay bills, manage accounts and file tax returns", "Handle real estate, including selling a home to pay for care", "Deal with insurance, retirement plans and government benefits", "Run or wind down a business", "Make gifts and continue your estate plan—only if you specifically grant those powers"]) +
       f'<p>Two South Carolina wrinkles matter. First, a durable POA must be recorded with the register of deeds in your county before your agent can act once you are incapacitated, so we prepare it in recordable form. Second, banks may refuse old or generic forms; a document drafted under the current Act with the powers spelled out is honored far more readily.</p>'
       '<h2>Health care power of attorney</h2>'
       f'<p>A health care power of attorney under {cite("hcpoa", "S.C. Code §§ 62-5-503 and 62-5-504")} names an agent to make medical decisions when you cannot, including consent to treatment, choice of providers and facilities, access to your records, and end-of-life decisions consistent with your {A("living-will", "living will")}. It can also state your wishes about organ donation and funeral arrangements.</p>'
       '<h2>Choosing your agents</h2>'
       '<p>Pick people, not titles. The financial agent should be organized and honest; the health care agent should be able to sit in a hospital hallway and say the hard thing you told them to say. They need not be the same person, and each should have an alternate. Adult children who live nearby are common choices; so is a trusted friend when children live far away or do not get along.</p>'
       + callout("<b>Frost first:</b> if a hospital or nursing facility hands you a power of attorney form to sign for a parent, call before signing. Some forms limit the agent to that facility; others grant powers the family never discussed.")
       + band("Put the right people in place.", "Powers of attorney are included in every plan we prepare and can be done on their own.")
   ),
   faqs=[
       ("When does a power of attorney take effect?", "You choose: immediately, or only when a physician certifies incapacity (a “springing” POA). Immediate powers are simpler for banks; springing powers appeal to people who want control until they truly need help."),
       ("Does a power of attorney end at death?", f"Yes. At death the personal representative named in the will, or the successor trustee, takes over. See {A('probate', 'probate')}."),
       ("Can my agent change my will?", "No. An agent can never make or change a will. Gifts and beneficiary changes are allowed only if the document expressly permits them."),
   ],
   related=["living-will", "guardianship-and-conservatorship", "last-will-and-testament"])

sp("living-will",
   title="Living Will Attorney in Summerville, SC | Declaration of a Desire for a Natural Death",
   description="A South Carolina living will (Declaration of a Desire for a Natural Death) records your end-of-life wishes so family and physicians know them. Summerville attorneys explain when it applies and how it works with a health care POA.",
   h1="Living Will in Summerville, SC", nav_label="Living will",
   lead="Document your end-of-life care preferences—from life support to artificial nutrition—so your family and physicians know exactly what you want before a crisis arises.",
   summary="Your end-of-life wishes, in the form South Carolina hospitals recognize.",
   body=(
       '<h2>What a living will is</h2>'
       f'<p>In South Carolina, a living will is formally a Declaration of a Desire for a Natural Death under the {cite("living_will_act", "Death with Dignity Act (S.C. Code § 44-77-10 et seq.)")}. It tells physicians whether you want life-sustaining procedures withheld or withdrawn if you have a terminal condition or are permanently unconscious, and whether artificial nutrition and hydration should be provided. It speaks only when you cannot.</p>'
       '<h2>What a living will can address</h2>'
       + checks(["Mechanical ventilation and other life-sustaining procedures", "Artificial nutrition and hydration (feeding tubes)", "Comfort care and pain relief, which continue regardless of your other choices", "Organ and tissue donation wishes, which we usually also place in the health care POA"]) +
       '<h2>When it takes effect</h2>'
       '<p>The declaration applies only after your attending physician and a second physician determine that you have a terminal condition or are permanently unconscious, and only if you cannot make decisions yourself. Until then, you decide—and you can revoke it at any time, in any way that shows your intent.</p>'
       '<h2>Living will + health care power of attorney</h2>'
       f'<p>The two documents work together. The living will states your wishes for the narrow end-of-life situation the statute covers; the {A("power-of-attorney", "health care power of attorney")} names a person to make every other medical decision and to enforce the living will if a facility hesitates. Families with both rarely end up in the emergency-room disputes families without them do.</p>'
       '<h2>Signing it correctly</h2>'
       '<p>South Carolina\'s statutory form requires witnesses who are not related to you, not your heirs, and not your health care providers, and the declaration must be acknowledged before a notary. We handle the signing at our office so the document will be honored at Summerville Medical Center, Trident, MUSC, Roper St. Francis or wherever you are treated.</p>'
       + band("Speak for yourself before you can't.", "A living will and health care power of attorney take one short meeting.")
   ),
   faqs=[
       ("Is a living will the same as a DNR?", "No. A do-not-resuscitate order is a physician's order about CPR in an emergency; a living will is your own statement about life-sustaining treatment in a terminal condition. Many people have both."),
       ("Will paramedics follow my living will?", "Emergency responders follow physician orders (such as a DNR or POST form), not a living will. The living will guides hospital decisions once your condition is assessed."),
   ],
   related=["power-of-attorney", "last-will-and-testament", "estate-plan-review"])

sp("asset-protection-trusts", card_new=True,
   title="Asset Protection Trusts & Planning in Summerville, SC | Frost Law Group",
   description="What asset protection actually means in South Carolina: irrevocable trusts, Medicaid's five-year look-back, retirement account protections and the limits. Summerville estate planning attorneys.",
   h1="Asset Protection Trusts in Summerville, SC", nav_label="Asset protection trusts",
   lead="Keeping a lifetime of work from being lost to a lawsuit, a nursing home bill or a beneficiary's divorce—within what South Carolina law actually allows.",
   summary="Irrevocable trusts, Medicaid look-back, and honest limits on what can be protected.",
   body=(
       answer("Frost Law Group designs asset protection plans for Summerville families—irrevocable trusts, Medicaid-compliant planning and trusts that protect an inheritance from a child's creditors or divorce. We also tell you plainly what South Carolina law does not allow.", "Who helps create asset protection trusts in Summerville, SC?")
       + '<h2>What “asset protection” means here</h2>'
       '<p>South Carolina does not have a domestic asset protection trust statute, so you cannot simply move your own assets into a trust you benefit from and put them beyond your creditors. Protection comes from four real tools: giving assets away irrevocably on a timeline, using exemptions the law already provides, structuring ownership properly, and—most often—protecting what your children and grandchildren inherit.</p>'
       '<h2>The tools</h2>'
       + steps([
           ("Irrevocable trusts.", " Assets you transfer to a properly drafted irrevocable trust, managed by someone else for your family, are generally outside your estate for creditor and long-term-care purposes once the applicable look-back period passes. You give up control; that is the price of protection."),
           ("Medicaid planning.", " Medicaid looks back five years at transfers. Planning early—a Medicaid asset protection trust, spousal protections, or a strategy for the family home—can preserve a house or savings for a spouse or children. Planning in the crisis is still possible, but the options narrow."),
           ("Exempt assets.", " Qualified retirement accounts, life insurance and annuities have statutory protection in South Carolina, and a homestead exemption applies in bankruptcy. Sometimes the best plan is making sure exempt assets stay exempt."),
           ("Inheritance protection.", " A trust for your children's inheritance—instead of an outright gift—can keep it out of a child's divorce, lawsuit or bankruptcy and away from a spendthrift problem. This is the protection most families actually need, and it fits inside a revocable trust plan."),
       ]) +
       '<h2>What we will not do</h2>'
       '<p>Transfer assets to hide them from an existing creditor or a pending lawsuit. South Carolina\'s fraudulent-transfer law unwinds those transfers and the attempt itself becomes evidence. Asset protection is planning done early, in the open, with a clear purpose.</p>'
       + callout("<b>Frost first:</b> if you have been told to “just put the house in the kids' names,” call before signing a deed. That move can cost a step-up in basis, expose the house to the child's creditors, and still count as a transfer for Medicaid.")
       + band("Plan before you need it.", "Bring your list of assets and your worries. We will map what can be protected and what cannot.")
   ),
   faqs=[
       ("Does a revocable trust protect assets?", "No. Because you keep control, a revocable trust is treated as yours by creditors and Medicaid. Protection requires an irrevocable structure."),
       ("How long is Medicaid's look-back in South Carolina?", "Five years for nursing-home Medicaid, under federal rules applied by South Carolina Healthy Connections."),
       ("Can an LLC protect my rental property?", "An LLC separates the rental's liabilities from your other assets and is often part of a plan, but it does not protect the rental from your personal creditors by itself."),
   ],
   related=["revocable-trust", "high-net-worth-estate-planning", "special-needs-planning"])

sp("estate-planning-for-blended-families", card_new=True,
   title="Estate Planning for Blended Families in Summerville, SC | Frost Law Group",
   description="Second marriages, stepchildren and children from a prior relationship: how South Carolina's default rules disinherit them and how a trust-based plan provides for a spouse and your own children. Summerville attorneys.",
   h1="Estate Planning for Blended Families in Summerville, SC", nav_label="Blended families",
   lead="A plan that provides for your spouse without accidentally disinheriting your own children—or the reverse.",
   summary="Second marriages and stepchildren: fixing the defaults that leave someone out.",
   body=(
       answer("Frost Law Group prepares plans for blended families in Summerville: trusts that provide for a surviving spouse while preserving assets for children of a prior relationship, and wills that treat stepchildren as you intend. Tara Frost has seen what happens in probate court when families skip this step.", "Who offers estate planning for blended families in Summerville, SC?")
       + '<h2>Why the defaults fail blended families</h2>'
       f'<p>South Carolina\'s intestacy statute leaves everything to a surviving spouse when there are no children, and half when there are—but stepchildren are not “children” under the statute and inherit nothing. A simple “I leave everything to my spouse” will has a second problem: once the assets belong to your spouse, your children have no claim to what is left when the spouse dies or remarries. The elective-share statute ({cite("elective_share", "S.C. Code § 62-2-201")}) also lets a surviving spouse claim one-third of a probate estate regardless of what the will says, which surprises couples who assumed a will alone kept things separate.</p>'
       '<h2>Tools that work</h2>'
       + checks(["<b>A marital trust.</b> The surviving spouse receives income (and principal for health and support) for life; the remainder passes to your children. Neither side can change the outcome.",
                 "<b>Separate and joint shares.</b> A joint revocable trust with separate sub-trusts for “his,” “hers” and “ours” assets, each with its own beneficiaries.",
                 "<b>Prenuptial or postnuptial agreements.</b> The reliable way to waive the elective share and define what is separate.",
                 "<b>Beneficiary designations.</b> Retirement accounts and life insurance pass by designation, not by will; they must be coordinated or they undo the plan.",
                 "<b>Specific provisions for stepchildren.</b> Named as beneficiaries if you intend it, or expressly omitted if you do not, so nobody has to guess.",
                 "<b>The house.</b> A right for the spouse to live there for life with the remainder to your children, and clarity about who pays taxes, insurance and repairs."]) +
       '<h2>A common Summerville scenario</h2>'
       '<p>A retired couple, each with adult children from a first marriage, buys a home together in Nexton. Each assumes “my half goes to my kids.” Without a plan, the survivor owns the entire house by survivorship and their will—or intestacy—decides where all of it goes. A joint trust with a life interest for the survivor and a split remainder fixes it in one document.</p>'
       + band("Protect both families.", "Bring your spouse, or come alone first. Either way we will map the plan before drafting anything.")
   ),
   faqs=[
       ("Can I leave my stepchildren an inheritance?", "Yes, by naming them in your will or trust. They do not inherit automatically."),
       ("Can my spouse and I have different wills?", "Yes, and in blended families you usually should, alongside a joint trust or an agreement that neither will be changed after the first death."),
   ],
   related=["revocable-trust", "last-will-and-testament", "estate-plan-review"])

sp("estate-plan-review", card_new=True,
   title="Estate Plan Review, Trust Amendments & Restatements | Summerville, SC",
   description="Get an existing will or trust reviewed in Summerville, SC—including online, out-of-state and older documents. Frost Law Group amends or restates trusts and updates plans after life changes.",
   h1="Estate Plan Review, Trust Amendments &amp; Restatements", nav_label="Plan reviews & trust amendments",
   lead="Already have a will or trust? We read it, tell you whether it still works under South Carolina law and your current life, and fix what does not.",
   summary="Second opinions on existing plans; amendments and restatements of trusts.",
   body=(
       answer("Frost Law Group reviews existing wills and trusts—drafted by another firm, in another state, or online—and prepares trust amendments or full restatements in Summerville. Bring the documents; the review comes with a written list of what to change and why.", "Who helps with trust amendments or restatements in Summerville, SC?")
       + answer("At our Summerville office. Tara Frost, who served as an Associate Probate Judge in Dorchester County, reviews the trust, the funding, and the beneficiary designations that work alongside it.", "Where can I get a trust reviewed in Summerville, SC?")
       + '<h2>When a plan needs review</h2>'
       + checks(["You moved to South Carolina with documents from another state", "A marriage, divorce, birth, adoption or death in the family", "You bought or sold real estate, a business, or a large asset", "A named agent, trustee or guardian has died, moved away or fallen out of favor", "The plan is more than five years old, or was drafted before the 2017 Uniform Power of Attorney Act", "You used an online service and were never told about funding, recording or witnesses"]) +
       '<h2>Amendment or restatement?</h2>'
       '<p>A trust <b>amendment</b> changes specific provisions and is right for one or two edits—a new successor trustee, a changed share. A <b>restatement</b> rewrites the whole trust while keeping its original name and date, so assets already titled to the trust do not have to be retitled. Restatements make sense when a trust has been amended more than once, was drafted elsewhere, or is old enough that the tax and trustee provisions are out of date. Wills are simply re-signed; a “codicil” is rarely worth the confusion.</p>'
       '<h2>What our review covers</h2>'
       + steps([("Validity.", " Signatures, witnesses, self-proving affidavit, and whether the document meets South Carolina's execution rules."),
                ("Fit.", " Does it still say what you want, with the right people in the right roles?"),
                ("Funding.", " Are deeds, accounts and designations actually pointed at the trust? This is where most plans fail."),
                ("Coordination.", " Retirement accounts, life insurance, transfer-on-death registrations and joint accounts either support the plan or quietly override it."),
                ("Ancillary documents.", " Powers of attorney and health care directives from other states are the most frequently rejected documents we see; we replace them with South Carolina forms.")]) +
       band("Bring what you have.", "Reviews are a flat fee, credited toward any work you decide to do.")
   ),
   faqs=[
       ("Is my out-of-state will valid in South Carolina?", "Usually, if it was valid where signed. The powers of attorney and health care documents are the problem; those should be redone under South Carolina law."),
       ("Can you fix a trust from an online service?", "Yes. Most need funding, a South Carolina-compliant signing, and clean-up of provisions that do not apply here."),
   ],
   related=["revocable-trust", "power-of-attorney", "trust-administration"])

sp("estate-planning-for-business-owners", card_new=True,
   title="Estate Planning for Business Owners in Summerville, SC | Succession & Operating Agreements",
   description="Succession plans, buy-sell and operating agreements, powers of attorney that cover the business, and trusts that keep a Lowcountry company running after death or disability. Summerville attorneys.",
   h1="Estate Planning for Business Owners in Summerville, SC", nav_label="Business owners",
   lead="What happens to the company, the employees and the family income if you die or become disabled tomorrow. Answer it now, in writing.",
   summary="Succession, buy-sell and operating agreements, and trusts that keep a company running.",
   body=(
       '<h2>The problem most owners have not solved</h2>'
       '<p>If you own an LLC or corporation and die without a plan, your interest becomes a probate asset. For months nobody can sign checks, renew licenses or sell the business, and your spouse inherits a company they may not want to run alongside partners they did not choose. A disability is worse: nobody has authority at all unless a power of attorney names them.</p>'
       '<h2>What a business owner\'s plan includes</h2>'
       + checks(["<b>An operating agreement (or shareholder agreement) that addresses death and disability.</b> Who can inherit an interest, who must be bought out, at what price, and how it is paid.",
                 "<b>A buy-sell agreement funded with life insurance</b> so partners can buy a deceased owner's share and the family receives cash instead of a minority interest.",
                 "<b>A durable power of attorney that expressly covers the business,</b> naming someone who can sign, hire and borrow if you cannot.",
                 "<b>A revocable trust that holds the business interest,</b> so a successor trustee can act immediately and the business stays out of probate.",
                 "<b>A written succession plan</b>—who runs the company for the first ninety days, where the passwords and bank contacts are, and who calls the customers.",
                 "<b>Tax planning</b> for larger companies, where estate tax exposure or a step-up in basis changes the structure."]) +
       '<h2>Operating agreements for Summerville LLCs</h2>'
       '<p>Many Lowcountry LLCs were formed online with no operating agreement or a template that never mentions death. Under South Carolina\'s LLC Act, the default rules then decide whether a deceased member\'s heirs become members or merely receive distributions. We draft or amend operating agreements so the answer is the one you choose, and we coordinate them with your will or trust so the documents do not contradict each other.</p>'
       '<h2>Who this is for</h2>'
       '<p>Contractors, medical and dental practices, restaurants, rental-property owners, farms and family businesses across Dorchester and Berkeley counties—any owner whose family income depends on the company continuing for at least a season after something happens to them.</p>'
       + band("Keep the doors open.", "Bring your formation documents and your current operating agreement, if you have one.")
   ),
   faqs=[
       ("Can my LLC interest be held in a trust?", "Yes, if the operating agreement allows it or is amended to allow it. We do both at the same time."),
       ("What if my partner dies and there is no agreement?", "The default statutory rules apply and the partner's estate—often a spouse with no involvement in the business—holds an economic interest. A buy-sell agreement prevents that."),
   ],
   related=["revocable-trust", "power-of-attorney", "high-net-worth-estate-planning"])

sp("special-needs-planning", card_new=True,
   title="Special Needs Trusts in Summerville, SC | Planning for a Child or Adult With a Disability",
   description="Third-party special needs trusts, ABLE accounts and guardianship for a loved one with a disability—how to leave an inheritance without losing SSI or Medicaid. Summerville estate planning attorneys.",
   h1="Special Needs Planning in Summerville, SC", nav_label="Special needs planning",
   lead="Provide for a child or adult with a disability without costing them the SSI, Medicaid and services they depend on.",
   summary="Special needs trusts and ABLE accounts that protect benefits and provide extras.",
   body=(
       '<h2>Why an ordinary inheritance can hurt</h2>'
       '<p>Supplemental Security Income and Medicaid are needs-based. A person receiving them generally cannot hold more than $2,000 in countable assets. An inheritance left outright—even a modest one from a grandparent—can suspend benefits until it is spent down, and the money is often gone within a year with nothing lasting to show for it.</p>'
       '<h2>Third-party special needs trust</h2>'
       '<p>A third-party special needs trust holds assets you leave for your loved one, managed by a trustee you choose, for “supplemental” needs—therapies not covered, a vehicle, travel, technology, a better apartment, a caregiver. Because the beneficiary never owns the assets, benefits continue, and because the funds were never the beneficiary\'s, Medicaid has no payback claim when the trust ends. It can be created inside your revocable trust and funded by your estate, life insurance and gifts from other relatives.</p>'
       '<h2>First-party trusts and ABLE accounts</h2>'
       '<p>When the person with a disability already has assets—a settlement, an inheritance received outright—a first-party (d)(4)(A) trust or a pooled trust can preserve eligibility, with a Medicaid payback at death. An ABLE account (South Carolina participates through Palmetto ABLE) lets a person whose disability began before the qualifying age save for disability expenses without affecting SSI up to the program limits. We usually combine the tools.</p>'
       '<h2>Guardianship and the alternatives</h2>'
       f'<p>When a child with a disability turns eighteen, parents lose legal authority. Options range from powers of attorney and supported decision-making, when the young adult can sign them, to {A("guardianship-and-conservatorship", "guardianship or conservatorship")} through the probate court when they cannot. We help families choose the least restrictive option that actually works.</p>'
       '<h2>Letter of intent</h2>'
       '<p>Alongside the legal documents, we ask parents to write a letter of intent: routines, medications, providers, what calms and what upsets, hopes for the future. Trustees and guardians tell us it is the most useful document in the file.</p>'
       + band("Plan for a lifetime.", "Bring the benefits letters and any existing trust documents. We will build the plan around what your loved one receives.")
   ),
   faqs=[
       ("Can grandparents leave money to a special needs trust?", "Yes. Once the trust exists, any relative can name it in a will, trust or beneficiary designation."),
       ("Who should be trustee?", "Often a sibling or trusted relative, sometimes with a professional co-trustee for larger trusts. The trustee must understand benefit rules; we provide written guidance."),
   ],
   related=["guardianship-and-conservatorship", "revocable-trust", "asset-protection-trusts"])

sp("dying-without-a-will-in-south-carolina", card_new=True,
   title="What Happens If You Die Without a Will in South Carolina? | Frost Law Group",
   description="South Carolina's intestacy rules explained: what a spouse and children receive, who is left out, who the court appoints, and what a family in Summerville should do next. Probate attorneys.",
   h1="What Happens Without a Will in South Carolina", nav_label="Dying without a will",
   lead="The state has a will for you. It was written by the legislature, and most people would not choose it.",
   summary="Who inherits under SC intestacy law, who is left out, and what to do next.",
   body=(
       answer(f"If you die without a will in South Carolina, your probate estate passes under the intestacy statute: everything to your spouse if you have no descendants; half to your spouse and half to your children if you do; and if you have no spouse, to your children, then parents, then siblings and more distant relatives. The probate court appoints the personal representative, and a judge chooses the guardian for minor children.", "The short answer")
       + '<h2>Who inherits under South Carolina intestacy law</h2>'
       + table(["If you leave…", "Your probate estate goes to…"], [
           ["A spouse and no descendants", "Spouse—everything"],
           ["A spouse and descendants", "Spouse one-half; descendants share one-half"],
           ["Descendants and no spouse", "Descendants, by representation (a deceased child's share goes to that child's children)"],
           ["No spouse, no descendants", "Parents; then siblings and their descendants; then grandparents and their descendants; then more distant relatives"],
           ["No relatives at all", "The State of South Carolina"],
       ]) +
       f'<p>The rules are in {cite("intestacy", "S.C. Code §§ 62-2-102 and 62-2-103")}. Adopted children inherit exactly as biological children; stepchildren, foster children, unmarried partners and friends inherit nothing.</p>'
       '<h2>What “probate estate” leaves out</h2>'
       '<p>Intestacy only controls assets that go through probate. Jointly owned property with survivorship, life insurance and retirement accounts with named beneficiaries, and accounts with payable-on-death designations pass by their own terms. That is why two families with identical wills (or none) can have very different outcomes.</p>'
       '<h2>Who is in charge</h2>'
       '<p>The court appoints a personal representative in a statutory order of priority—surviving spouse first, then heirs—and may require a bond. Disagreements among adult children about who serves are one of the most common reasons an intestate estate ends up in a hearing.</p>'
       '<h2>Minor children</h2>'
       '<p>A judge chooses their guardian based on the evidence presented, without knowing your wishes. A child\'s inheritance is held in a conservatorship and paid out at eighteen, regardless of maturity. A will fixes both problems with two paragraphs.</p>'
       '<h2>If someone in your family has already died without a will</h2>'
       f'<p>The estate still goes through probate, in the county where the person lived. We help families open the estate, determine heirs, deal with creditors and distribute correctly. Start with our {A("probate", "probate overview")} or call {TEL}.</p>'
       + band("Write your own rules.", "A will-based plan takes one meeting and a signing. Call for a flat-fee quote.")
   ),
   faqs=[
       ("Does my spouse get the house if I die without a will?", "If the house is titled jointly with survivorship, yes, automatically. If it is in your name alone and you have children, your spouse receives a half interest and the children the other half."),
       ("Do I have to go through probate if there is no will?", f"Usually, unless the estate is small enough for an affidavit or everything passes outside probate. See {A('small-estate-affidavit', 'small estate affidavits')}."),
   ],
   related=["last-will-and-testament", "probate", "probate-process"])

sp("estate-planning-costs", card_new=True,
   title="What Estate Planning Costs in Summerville, SC | Flat Fees Explained",
   description="What a will, a trust-based plan and powers of attorney typically cost in the Charleston area, what drives the price, and why Frost Law Group quotes flat fees before starting. Summerville estate planning attorneys.",
   h1="What Estate Planning Costs in Summerville, SC", nav_label="What it costs",
   lead="An honest look at what you are paying for, what drives the number up or down, and how our flat fees work.",
   summary="Flat fees, what drives the price, and what you get for it.",
   body=(
       '<h2>How we charge</h2>'
       '<p>Every estate plan at Frost Law Group is a flat fee quoted at the end of the first meeting, once we know your family, your assets and what you want. The fee covers design, drafting, a plain-English summary, changes, the signing meeting with witnesses and notary, and—for trusts—the deeds and funding letters. There is no hourly clock during the planning process.</p>'
       '<h2>What drives the price</h2>'
       + checks(["<b>Will-based or trust-based.</b> A trust-based plan is more work: the trust itself, a pour-over will, deeds, and funding.",
                 "<b>Single or married.</b> Couples receive two sets of documents and, often, one joint trust.",
                 "<b>Complexity.</b> A blended family, a business, a child with special needs, out-of-state property or asset-protection goals add drafting and design time.",
                 "<b>Real estate.</b> Each parcel titled to a trust needs a deed, recorded with the county.",
                 "<b>Tax planning.</b> Estates approaching the federal exemption need structures most families do not."]) +
       '<h2>Typical market ranges</h2>'
       '<p>Across the Charleston area, a standalone will or set of powers of attorney is generally priced in the hundreds of dollars; a complete will-based plan for a couple in the low thousands; and a trust-based plan more than that, rising with complexity. These are ranges for the market, not a quote—we will give you an exact number for your plan before you commit. Ask us; the consultation itself is where the quote comes from.</p>'
       '<h2>What it costs to skip it</h2>'
       f'<p>Probate court fees in South Carolina rise with the size of the estate ({cite("probate_fees", "S.C. Code § 8-21-770")}), estates stay open at least eight months, and an attorney is usually needed anyway. A conservatorship for an incapacitated adult with no power of attorney involves petitions, examiner reports, a hearing and annual accountings. Measured against that, planning is inexpensive.</p>'
       + band("Get a number.", "Tell us what you own and who you love. You will leave the first meeting with a flat-fee quote.")
   ),
   faqs=[
       ("Do you charge for the first meeting?", "Call us and we will tell you. For estate planning, the first meeting is where the plan is designed, and any consultation fee is credited toward the plan."),
       ("Are updates included?", "Changes during drafting are included. Later amendments are quoted separately and are usually modest."),
   ],
   related=["estate-planning-attorney", "revocable-trust", "last-will-and-testament"])

sp("high-net-worth-estate-planning", card_new=True,
   title="Estate Planning for Larger Estates in Summerville, SC | Trusts, Tax & Complex Portfolios",
   description="Planning for families with complex portfolios, multiple properties, businesses and estate-tax exposure: irrevocable trusts, gifting, trustee selection and coordination with your advisors. Summerville attorneys.",
   h1="Estate Planning for Larger and More Complex Estates", nav_label="Larger estates & complex portfolios",
   lead="When the plan has to manage a portfolio, a business, several properties and a tax return, not just pass a house to the kids.",
   summary="Complex portfolios, multiple properties, tax exposure and professional trustees.",
   body=(
       answer("Frost Law Group designs plans for Summerville families with complex portfolios—investment accounts, rental and commercial property, closely held businesses and retirement assets—coordinating with your CPA and financial advisor so the documents, titles and designations work as one system.", "Which Summerville, SC attorneys manage complex estate portfolios?")
       + '<h2>What changes when the estate is larger</h2>'
       + checks(["<b>Tax.</b> Estates near the federal estate-tax exemption need lifetime gifting, irrevocable trusts or charitable planning; South Carolina has no separate estate or inheritance tax.",
                 "<b>Income tax on inherited assets.</b> Retirement accounts inherited by children must generally be emptied within ten years; the plan can name trusts as beneficiaries to control the timing.",
                 "<b>Trustee choice.</b> A sibling may be fine for a house and a checking account; a portfolio and a business may call for a professional or corporate co-trustee.",
                 "<b>Liquidity.</b> Real estate-heavy estates need cash for taxes, expenses and equalizing gifts; life insurance in an irrevocable trust is the classic answer.",
                 "<b>Multiple states.</b> Property outside South Carolina goes into the trust to avoid ancillary probate.",
                 "<b>Privacy.</b> A trust keeps the inventory of a large estate out of the public probate file."]) +
       '<h2>Tools we use</h2>'
       '<p>Joint and separate revocable trusts; irrevocable life insurance trusts; spousal lifetime access trusts; grantor trusts for gifting; charitable remainder trusts and donor-advised funds; family LLCs for rental portfolios; and beneficiary designations drafted, not defaulted. We are a WealthCounsel member firm and draft on that platform, with tax provisions kept current.</p>'
       '<h2>Working with your other advisors</h2>'
       '<p>Larger plans succeed when the attorney, CPA and financial advisor share one picture. We will, with your permission, meet with them, coordinate account titling and beneficiary forms, and give everyone a one-page map of the plan.</p>'
       + band("Bring the balance sheet.", "We will tell you which structures earn their cost and which do not.")
   ),
   faqs=[
       ("Does South Carolina have an estate tax?", "No. Only the federal estate tax applies, and only above the federal exemption amount in effect at death."),
       ("Do I need a corporate trustee?", "Not always. Many families name a relative with a professional co-trustee or an advisor as “trust protector.” We match the trustee to the assets."),
   ],
   related=["asset-protection-trusts", "estate-planning-for-business-owners", "trust-administration"])
