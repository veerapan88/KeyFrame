# **KeyFrame — Product Requirements Document v3.1**

**Research inputs:** Dipesh, Sergio, John, Faridun, Cherry, Simon (advisory), and one async Reddit respondent (referred to below as the Reddit landlord), Sathwik, Anthony, Steve, additional Reddit landlord.

---

## **1\. Vision**

Self-managing owners of small rental properties are stuck between two bad options: do everything themselves, or hand 8–10% of rent plus a placement fee to a property manager they don't trust. 10/11 landlords interviewed rejected property managers. 

KeyFrame is an AI coordinator for landlords who intend to stay in charge. It runs the communication, scheduling, chasing, and record-keeping around two recurring events — **re-renting a unit** and **fixing something that broke** — while the landlord keeps every decision that carries money, judgment, or liability.

**Product posture:** minimize human touchpoints; deliberately preserve them where trust matters. A trusted human hosts every showing. The landlord picks every tenant and every contractor. The AI never spends money, never selects a vendor unilaterally, and never takes custody of funds.

---

## **2\. Personas**

**Primary — the self-managing owner.** Owns one to several properties of 1–4 units each; typically 1–6 doors total. Financially literate, price-sensitive, uses Zillow Rental Manager, has a handyman or two on text. Explicitly rejects property managers. Wants organization and automation, not decisions made for them.

**Variant — the realtor-assisted owner.** Same profile, but pays a realtor one month's rent to list, show, and pre-screen, then handles interviewing, verification, and selection personally. Values the realtor for reputational self-interest — a realtor who places a bad tenant damages their own standing. KeyFrame competes here against a known human with skin in the game, sometimes at zero cost to the landlord where the tenant pays commission. Two implications: the Trusted Individual pitch is competing with an alternative that already works, and the landlord's retained work (interview, verification, decision) is exactly the part they will not delegate to software.

**Secondary — the Trusted Individual.** The current tenant, a neighbor, or a local contact who opens the door for showings. Validated as existing behavior: Dipesh already asks current tenants to host, and reports they almost always agree. Incentives align sharply when the outgoing tenant wants to leave early. Interacts by SMS only. Zero friction, no accounts, nothing to sign or collect.

**Secondary — the tenant.** Books showings, applies, pays a screening fee, signs, pays, and later reports maintenance issues. SMS plus hosted web links. **Note (v3.1):** the applicant is now a paying party at the application step, which makes applicant-side experience a commercial concern and not only a courtesy one. A confusing fee, a missing receipt, or a late refund is now a liability surface, not a UX complaint.

**Secondary — the vendor.** The landlord's existing handyman, cleaner, or appliance contact. Receives work by the landlord's own text, not through a KeyFrame account. KeyFrame prepares the message; the landlord sends it.

---

## **3\. Scope**

**Feature Set A — Leasing.** Ships first. Renewal check-in through move-in.

**Feature Set B — Maintenance & Make-Ready.** Ships second, on the same ticket engine. Tenant-reported issues and turnover prep.

The two connect at move-out: the outgoing tenant's condition report becomes the make-ready ticket list, which must close before re-listing.

---

## **4\. Feature Set A — Leasing**

### **A1. Renewal check-in and turnover trigger**

* **A1.1 Renewal window monitor.** KeyFrame tracks lease end dates and prompts the landlord 5 months out to start the renewal conversation. Landlord approves; AI texts the tenant.  
* **A1.2 Renewal outcome capture.** Tenant replies renewing, leaving, or undecided. Undecided schedules an automatic follow-up. A "leaving" answer opens a turnover and starts the make-ready checklist (B3) and the deposit clock (A5.5).  
* **A1.3 Trusted Individual ask.** When the outgoing tenant indicates they're leaving, the AI asks the landlord whether to invite them to host showings, and if the tenant wants an early release, surfaces that as leverage the landlord may choose to offer.

*Rationale: Potential capture funnel for customers. No competitor addresses this and no landlord interviewed has a real system for it.*

### **A2. Listing prep and unit knowledge**

* **A2.1 Listing preparation.** AI drafts the listing description, suggests photo order, and gives pricing guidance. Landlord copy-pastes into Zillow themselves. KeyFrame never posts on the landlord's behalf.  
* **A2.2 Unit knowledge base.** A structured record of unit facts — laundry, parking, pets, utilities, sublets, smoking — built conversationally and gap-flagged when leads ask something unanswered twice.  
* **A2.3 Lead intake.** Zillow and Apartments.com notification emails parsed into Lead records, with manual entry as fallback. Treat template drift as a production alarm.

### **A3. Lead qualification**

* **A3.1 Criteria capture.** Landlord defines income-to-rent ratio, credit floor, eviction rules, move-in window, occupancy, and pet/smoking policy. Stored per property, editable, applied identically to every lead. **These criteria are now dual-purpose:** they drive pre-qualification *and* must be published to applicants in writing before any fee is charged (A5.2). One stored object, two consumers.  
* **A3.2 Automated pre-qualification.** Every inquiry receives the same questions in the same order over SMS before any showing is offered.  
* **A3.3 Automated decline.** Failing leads are declined immediately and courteously, with the specific failed criterion named and a co-signer path offered where the landlord permits one. Declines are logged. Pre-qualification declines happen before any money changes hands and therefore carry no refund obligation. Pre-qual is the free filter Background/credit check fees happen after.  
* **A3.4 Automated Q\&A.** Leads asking about the unit get answered from A2.2 without landlord involvement, then are moved toward scheduling.  
* **A3.5 Funnel view.** Landlord sees inquiries, auto-declined, qualified, showed, and interviewed as counts with drill-down. This is the primary proof-of-value \+ transparency screen.

### **A4. Showings**

* **A4.1 Host designation.** Landlord names themselves or a Trusted Individual per property.  
* **A4.2 Host coordination.** AI texts the host, collects availability, offers slots to qualified leads, confirms both sides, sends day-of reminders with the lead's name, and handles cancellations and rebooking.  
* **A4.3 Post-showing read.** Immediately after each showing the host receives a three-question text: did they show (Yes/No), would you rent to them (Y/N)), and tenant feedback (free text response). Returned to the landlord attached to that lead.  
* **A4.4 No-show tracking.** Repeat no-shows are flagged and downranked.

*Constraint: every showing is hosted by a human the landlord named.* 

### **A5. Application, decision, and lease**

* **A5.1 Batch invitation.** Landlord selects everyone worth considering; those candidates apply in parallel. Nothing is pulled, consented to, or charged before this point. Applicants never invited are never charged, which independently satisfies the "no fee without consideration" rule. Landlord receives an alert that they are required to refund application fees to candidates who are not selected with marketing copy about the benefit of widening the pool at a minimal cost. Landlords who do not want to refund background checks can simply select only one candidate and move to the next screen. Unselected candidates then hold until the landlord makes a decision on the selected candidate.   
* **A5.2 Fee disclosure and pre-charge gate.**

  * No applicant can be charged until the property's written screening criteria (A3.1) and the fee amount are published to the application flow. The system hard-blocks collection if criteria are unset. Published criteria are what make "not selected" defensible rather than discretionary.  
  * Before paying, the applicant sees: the fee amount, a screening-fee rights statement (right to a copy of their credit report, right to a receipt, right to a full refund if unselected), and confirmation that a unit is actually available. Collection is blocked if the property is not in an available state.  
  * The fee is landlord-configurable per property, capped to the current statutory ceiling. **Store the cap as configuration, never as a constant.** It is CPI-adjusted annually from a 1998 base and the state publishes no official adjusted figure; some cities publish their own, higher, local number. This requires an annual review task and, at minimum, a per-jurisdiction override field. Confirm the operative figure with counsel before launch and each January.  
  * **Reusable/portable report path.** California has a separate portable-screening-report law. An applicant who submits a valid reusable report cannot be charged a fee — not for the report, not for access to it. This needs its own intake option offered *before* payment, and if a fee is collected in error it must be returned immediately. Treat a charged fee co-existing with a valid portable report as a data-integrity alarm.  
* **A5.3 Screening execution.** Credit, criminal, and eviction via an FCRA-compliant partner. Results shown side by side against the landlord's stated criteria. Adverse action notices generated automatically on decline. Every applicant who paid a fee automatically receives a copy of their consumer credit report within 7 days of results returning — system-triggered, not a landlord task, and not dependent on the applicant asking.

* **A5.4 Refund engine.** The requirement that makes this survivable for a landlord who is not tracking deadlines.

  * **Triggers.** An applicant becomes refund-eligible when a different applicant is selected, when the applicant withdraws, or when the listing is pulled from the market. Unselected candidates stay in the pool and are only sent a polite decline notice after the landlord signs a tenant. All three workflows (applicant selected, withdraws, or listing is pulled) fire the same workflow.   
  * **Deadline.** Refund within 7 days of tenant selection or 30 days of that applicant's submission, whichever is earlier. Compute and store both at charge time; recompute when selection occurs; act on the earlier. Surface a countdown to the landlord, not a stored date.  
  * **Execution.** Fees land in the landlord's connected Stripe account, so refunds pull from that balance via Stripe Connect. Request standing refund authorization at onboarding so refunds fire automatically.   
  * **Insufficient balance.** If the landlord has already withdrawn the fees, fall back to a backup payment method on file, or block further fee collection on that property until resolved.   
  * **No skip path.** There is no "denied for cause, no refund owed" state in this product. That exception belongs to Option A, which KeyFrame does not implement. The code path should not exist — not as a landlord control, not as an admin override. See §6.  
  * **Audit trail.** Every refund event writes to the Message Log with its computed deadline and outcome, and notifies the applicant automatically.  
* **A5.5 Deposit and lease.** Lease generated and e-signed via a third-party API. Deposit and first month collected via hosted checkout, routed directly to the landlord — KeyFrame never holds funds. Jurisdiction rules enforced per §7.

* **A5.6 Move-in packet.** Utilities, HOA rules, key handoff, and dated move-in condition photos assembled during screening and released as a PDF to the tenant once funds clear.

**Deferred — reference checks (A5.7).** The mockups show KeyFrame calling prior landlords and employers with a fixed question set and an attempt log. Nothing comparable exists in market; it addresses Faridun's complaint that realtors filter what the owner sees; and the Reddit landlord performs exactly this work by hand on every applicant, alongside credit and background. That makes it the most-validated item in the deferred pile and the strongest candidate for promotion after Phase 0\. However, this is a complex and potentially large build. **Fee note:** if reference-check labor is ever recovered from the applicant, it must fit inside the same statutory cap as everything else and be itemized on the receipt as time reasonably spent. It cannot be priced at what it's worth.

**Retained by the landlord — the interview.** Every sophisticated landlord interviewed keeps a live conversation with the applicant, from fifteen to thirty minutes, and treats it as the real decision. The Reddit landlord was blunt about why: software would need "a fine grained bullshit detector" he doesn't believe exists. KeyFrame must never appear to be exercising judgment about a person. It prepares the landlord for that conversation (stated facts, host's read, suggested questions) and does the verification legwork around it. It does not score, rank, or recommend applicants.

**Deferred — unlawful detainer search (A5.8).** Sergio notes eviction records appear in public court records only where the landlord prevailed, so standard reports understate risk. A county-records check is cheap and manual. Concierge-phase task first.

---

## **5\. Feature Set B — Maintenance & Make-Ready**

One ticket engine serves both. A make-ready item and a broken dishwasher differ in trigger and volume, not in shape.

### **B1. Intake and triage**

* **B1.1 Tenant line.** A number the landlord gives tenants. Issues arrive by text with photos.  
* **B1.2 AI triage.** Structured intake — what, where, since when, photos — then guided troubleshooting for issues commonly resolved without a visit (breaker, garbage disposal reset, filter, water shutoff).  
* **B1.3 Hazard escalation.** Gas smell, sparking, active flooding, no heat, and CO alarms bypass triage entirely and alert the landlord immediately by call and text. **Hard requirement.** Habitability obligations carry statutory deadlines; a mis-triaged emergency is the highest-severity failure in this product.  
* **B1.4 Ticket delivery.** Landlord receives a triaged ticket with photos, suspected cause, urgency, and a recommended next action. No 3am calls.

### **B2. Vendor coordination and logging**

* **B2.1 Vendor directory.** Landlord's own contacts, pre-tagged by trade. This is the default and the priority path — landlords trust their existing people.  
* **B2.2 Match and draft.** AI matches the ticket to a vendor from the directory and drafts a copy-pasteable message including the description and photos. The landlord sends it themselves.  
* **B2.3 Follow-up capture.** Days later the AI texts the landlord: is this closed, what did it cost, who did it. Replies are parsed and written to the ticket. This is the mechanism — landlords will answer a prompt they won't proactively fill a spreadsheet with.  
* **B2.4 Expense log and export.** Every closed ticket becomes a dated, categorized, per-property expense line with any attached invoice, exportable at tax time.  
* **B2.5 Vendor overflow (deferred).** When the landlord's own list can't cover a job, surface vetted alternatives. Requires a supply-side network that does not yet exist. Sequence after B2.1–B2.4 prove out.

### **B3. Make-ready**

* **B3.1 Move-out condition capture.** Weeks before move-out, the AI asks the outgoing tenant for a room-by-room checklist and photos, plus wear-and-tear items they wouldn't otherwise report.  
* **B3.2 Scope list.** Findings become a make-ready ticket list — clean, paint, repair, replace — each item routed through B2.  
* **B3.3 Multi-item project tracking.** Make-ready jobs span days and multiple line items. Each quoted item is tracked against its quote and final invoice, with dropped items flagged. *Dipesh's worst vendor experience was an unitemized invoice with silently removed line items.*  
* **B3.4 Re-list gate.** Open make-ready items are surfaced against the target listing date so re-listing isn't blocked by a forgotten task.

---

## **6\. Shared foundations**

**Channels.** Landlord uses in-app conversational chat. Tenants, hosts, and vendors use SMS and hosted links, no accounts. One leasing number per property.

**Data model.** Landlord · Property · Lease · Tenant · Trusted Individual · Lead · Showing · Application · Screening · **Screening Fee** · Payment · Vendor · Ticket · Expense · Message Log. Every stateful entity carries an explicit status field. Airtable or Supabase.

**Screening Fee (new in v3.1).** One record per charge, because parallel charging requires parallel deadline tracking. Fields: application reference · Stripe charge id · amount · submitted\_at · deadline\_by\_submission (submitted\_at \+ 30d) · competitor\_selected\_at (nullable) · deadline\_by\_selection (that date \+ 7d) · effective\_deadline (the earlier of the two) · status (charged → report\_delivered → selected / unselected → refund\_initiated → refunded / refund\_failed) · refund\_trigger (selected\_other / withdrew / listing\_removed) · portable\_report\_used (boolean; if true no fee record should exist, so a true value here is an integrity alarm).

**Compliance:**

* *Fair Housing:* no question, answer, decline reason, or feedback prompt may touch a protected class. Every AI-to-party message logged. Applies with particular force to A4.3, which is the highest-risk surface in the product.  
* *FCRA:* consent before any pull; adverse action on every decline; landlord never receives raw consumer-report data outside the partner's compliant surface. Credit report delivery to the applicant is automatic and unconditional where a fee was paid.  
* *Screening fees (new):* the fee may never exceed actual out-of-pocket cost plus reasonable time value, capped at the statutory ceiling; a receipt with itemization is required; every unselected applicant is refunded in full on the A5.4 clock. **The same "log everything, no silent override" posture that governs Fair Housing messaging governs refunds.** A refund that is skipped, delayed past deadline, or manually suppressed must be impossible by design and visible in the Message Log by default. The reason to state this alongside Fair Housing rather than under payments: both are per-instance liabilities that look like paperwork right up until they are a lawsuit.  
* *TCPA:* consent recorded, STOP honored, 10DLC registered.  
* *Habitability:* B1.3 escalation is non-negotiable.

**Legal review is a prerequisite to the pilot, not a follow-on.** Exposure is per-message and per-charge, not proportional to user count.

---

## **7\. Jurisdiction handling**

The v2 Chicago/Cook block was a deposit-custody problem, not a market judgment. It applies to one feature. **v3.1 adds a second jurisdiction-gated feature: screening fees.**

* **Feature A5.5 (deposit routing)** is disabled where local law requires segregated, interest-bearing, disclosed accounts — Chicago and Cook County most notably, where penalties run to double the deposit plus fees. In those jurisdictions KeyFrame surfaces the requirement and the landlord collects the deposit outside the platform.  
* **Features A5.2 and A5.4 (screening fee collection and refunds)** run the California ruleset only where the property is in California. AB 2493 and §1950.6 are California statutes. Whether Illinois imposes analogous ordering, cap, receipt, or refund requirements has not been researched, and the CA logic must not be silently applied there as a proxy. Until confirmed, either (a) run Illinois properties on the same full-refund flow as a conservative posture, which is defensible because refunding more than required is not a violation, or (b) hold applicant-paid screening to California only and use landlord-paid in Illinois. Option (a) is simpler to build and is the recommendation, but the research still needs doing.  
* **Everything else** — renewal monitoring, listing prep, pre-qualification, showing coordination, screening execution, lease e-signature, maintenance, make-ready, expense logging — operates in Cook County unchanged.  
* California rules per v2: AB 12 deposit cap, 21-day return with itemization, AB 2801 photo documentation, AB 414 electronic refund, local interest ordinances.  
* Illinois outside Chicago/Cook: 30-day itemization, 45-day return, no escrow requirement under 25 units.  
* Some California cities (Berkeley is the clearest example) publish their own screening-fee maximum and their own disclosure requirements on top of state law. City-level overrides need a field, not a code branch.

---

## **8\. Pricing hypothesis**

Triangulation across interviews:

| Source | Signal |
| ----- | ----- |
| Dipesh | $200–300/mo for a portfolio with both feature sets; $100/mo at two properties; wants volume discounting; explicitly price-sensitive |
| Faridun | $120–130 one-time for leasing alone, after a guided walkthrough; near zero from a cold ad |
| Sergio | Under one month's rent for placement; "no more than a couple thousand" |
| Teuben | \~5% of rent is fair; a full month's rent is not |
| Reddit landlord | Pays a realtor one month's rent; would not price software in the abstract and declined to try |
| Market | Hemlane $86/mo \+ $695/placement |

**Reading.** Leasing alone doesn't support a subscription at 1–4 units — turnover is too infrequent, and Faridun's number lands near $130. Both feature sets together do, because maintenance recurs. Dipesh's ceiling is roughly $2,400/year for a portfolio; discounted to a one-time equivalent that's near $1,000–1,500 — which brackets Sergio's "couple thousand" and sits under Hemlane.

**Working hypothesis:** per-door monthly subscription with portfolio tiering once Feature Set B ships; a per-placement fee for leasing-only customers before that. Both are hypotheses. The test is a card on file, not a stated number.

**Structural pricing constraint.** The realtor charges one month's rent and delivers listing, showings, pre-screening, and a reputational guarantee. Any KeyFrame price must be justified against that bundle, not against free DIY software.

---

## **9\. Out of scope**

* **Escrow and funds release.** Requested by Dipesh — platform holds contractor payment until both sides sign off. Requires money transmission licensing and contradicts the custody-free principle. Solid demand but not at this stage. To revisit only as a chartered partner integration.  
* **Listing syndication and posting on the landlord's behalf.** Zillow's terms prohibit automated posting, and credential-based posting transfers liability to the landlord. KeyFrame prepares listings only.  
* **Dispatch and contractor marketplace.** Requires supply density that doesn't exist yet.  
* **Rent collection and accounting.** Landlords report this as easy. Expense logging (B2.4) is the deliberate exception.  
* **Unattended showings.**  
* **Short-term and month-to-month rentals.** Different criteria and timing; noted by Dipesh, deferred.  
* **HOA-level vendor sourcing.** Interesting, unclear buyer.  
* **Rent-setting calculator.** Faridun's suggestion, aimed at less sophisticated landlords — a different segment than the one this document targets.

---

## **10\. Build sequence**

**Phase 0 — Concierge (now).** Five landlords. Airtable as source of truth. A human performs the AI's role manually: renewal texts, lead pre-qualification, host coordination, post-showing prompts, maintenance triage, vendor drafts, follow-up capture. Real Stripe, screening, and e-signature — the compliance-sensitive parts are never simulated. Outreach describes a tool in development and never claims automation that isn't running.

**Phase 0 exception — refund deadlines are not a manual step (new).** Everything else in Phase 0 can be a human with a checklist. Refunds can't be, because they are the one manual task in this document with a statutory deadline and a per-instance penalty attached. Even in the concierge phase, build the minimum: a dated Screening Fee record per charge, a computed effective deadline, and an alarm that fires before it. The refund execution itself can be a human clicking refund in Stripe; the *knowing when* cannot be a human remembering. This is a few hours of Airtable work and it is the cheapest liability reduction available in Phase 0\.

**Transition trigger.** Automate a step only after it has been performed manually enough times to be demonstrably repeated, high-volume, and low-judgment. Concierge runs produce the build backlog; the backlog is not written in advance.

**Phase 1 — Leasing build.** A1–A5, prioritized by hours saved in Phase 0\.

**Phase 2 — Maintenance build.** B1–B3 on the same engine.

---

## **11\. Open questions**

1. \~\~Who pays for screening?\~\~ **Resolved in v3.1:** applicant-paid on the full-refund path (A5.2–A5.4). What remains open is downstream: does an applicant-paid fee suppress application volume in the batch-invitation model, where the landlord has already narrowed the field before anyone is asked to pay? Measure application-completion rate after invitation in Phase 0\.  
2. Subscription or per-placement? Resolvable only with a real price ask.  
3. Does the renewal check-in (A1) convert as an acquisition hook, or only retain existing users?  
4. Can KeyFrame be positioned against a realtor rather than against software? The realtor is the incumbent this persona actually pays, and the comparison is unflattering on trust and flattering on price.  
5. Does Illinois impose its own screening-fee rules?