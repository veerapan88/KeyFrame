# KeyFrame v0 — Screen List & Information Architecture
**Derived from:** PRD v3.1 (corrected)
**v2 changes from v1:** Renamed PropOps → KeyFrame throughout. Fixed A5 to remove the "default to Option A by inviting one at a time" language (no partial-compliance pathway exists in this product — see §3, A5 notes). Split the duplicate "A5.2" numbering: fee disclosure stays A5.2, unselected-candidate pooling/decline-timing folded into A5.4's refund trigger. Restored the Y/N/Maybe structured field to A4.3/A4-S6 alongside free text. Added A5-S1a (refund-obligation framing at batch-invite time). Combined decline notice + refund confirmation into a single applicant-facing message. Added §10: wireframe direction synthesis, with compliance notes per direction.
**Purpose:** Canonical screen/state reference for wireframe exploration (Gemini) and final design (Claude Design). This is the source of truth both tools should build from — don't re-derive screens from the PRD independently.

---

## 0. How to read this document

Each screen entry follows the same shape:

- **Surface** — which channel it lives on (Landlord Dashboard, SMS, Hosted Web Link)
- **Entry trigger** — what causes this screen/message to appear
- **State shown** — what data/fields are visible, including which entity statuses drive it
- **Actions available** — what the user can do here
- **Triggers next** — what this screen's actions cause downstream
- **PRD ref** — feature number, for traceability

Screens are grouped by PRD feature area, not by literal page — several "screens" on SMS are really message templates with a small state machine behind them, not a page a person navigates to.

---

## 1. Surfaces & Actors

| Actor | Surface | Notes |
|---|---|---|
| **Landlord** | In-app web dashboard + conversational chat (PWA) | Single source of truth interface. No SMS for landlord actions. |
| **Lead / Applicant / Tenant** | SMS (conversational) + Hosted Web Links | No account, no login. Each link is single-purpose and pre-authenticated (magic-link style). |
| **Trusted Individual** | SMS only | Zero friction, no links unless absolutely necessary (e.g. availability picker). |
| **Vendor** | None (receives landlord's own SMS/text, outside KeyFrame) | Vendor directory is landlord-dashboard-only; vendor never sees KeyFrame UI. |

---

## 2. Landlord Dashboard — Top-Level Navigation

Five primary nav sections, mapping directly to PRD structure:

1. **Properties** — property list → property detail (A2, A3 criteria, A5.5 jurisdiction)
2. **Pipeline** — the funnel view across all active turnovers (A3.5), this is the primary proof-of-value screen
3. **Tickets** — maintenance + make-ready (B1–B3)
4. **Chat** — the conversational AI surface itself (cross-cutting; where most landlord *input* happens)
5. **Settings** — billing, Stripe connection, vendor directory (B2.1), notification prefs

**Design note:** Chat is not a 6th tab bolted on — per §2a of the PRD, chat is the primary input mechanism. Most of the screens below are *rendered inline in chat* (the AI asking a question, showing a card) rather than separate pages. Treat "screen" loosely — many of these are chat-embedded cards, not full navigations.

---

## 3. Screen Inventory — Feature Set A (Leasing)

### A1 — Renewal & Turnover Trigger

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A1-S1: Renewal prompt card** | Landlord chat | Lease end date − 5 months (system cron) | Tenant name, unit, lease end date | "Start renewal conversation" / "Not yet" / "Skip" | Sends SMS to tenant (A1-S2) | A1.1 |
| **A1-S2: Renewal question (SMS)** | Tenant SMS | Landlord approves A1-S1 | — | Reply: renewing / leaving / undecided | Renewing → close loop; Leaving → opens Turnover (A1-S4); Undecided → auto-follow-up scheduled | A1.2 |
| **A1-S3: Undecided follow-up (SMS)** | Tenant SMS | Timer from A1-S2 | Prior answer context | Same reply options | Same branching as A1-S2 | A1.2 |
| **A1-S4: Turnover opened notice** | Landlord chat | "Leaving" reply received | Move-out date if known, links to new Make-Ready ticket (B3) and Deposit clock (A5.5) | Acknowledge, optionally jump to Trusted Individual ask | Opens B3.1, starts deposit-return countdown | A1.2 |
| **A1-S5: Trusted Individual ask card** | Landlord chat | A1-S4 fires | Outgoing tenant's info, optional "early release" leverage note | "Invite as Trusted Individual" / "I'll host" / "Someone else" | Sends SMS intro to Trusted Individual (A4-S1) | A1.3 |

---

### A2 — Listing Prep & Unit Knowledge

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A2-S1: Listing draft workspace** | Landlord chat + panel | Property onboarding or new turnover | AI-drafted description, suggested photo order, pricing guidance | Edit text, reorder photos, accept pricing or override | Produces copy-paste block (A2-S2) | A2.1 |
| **A2-S2: Copy-paste-ready export** | Landlord dashboard | A2-S1 accepted | Final listing text block + deep link to Zillow's post flow | Copy button | None (landlord posts externally — KeyFrame never posts on their behalf) | A2.1 |
| **A2-S3: Unit knowledge Q&A builder** | Landlord chat | Onboarding, or gap-flag trigger from A3-S4 | Running list of Q&A pairs (parking, laundry, pets, etc.) | Add/edit answer | Feeds A3.4 auto-responder | A2.2 |
| **A2-S4: Lead intake fallback** | Landlord dashboard | Email parse failure (template drift) | Raw email text, "couldn't parse" flag | Manual entry form → creates Lead record | Creates Lead entity | A2.3 |

---

### A3 — Lead Qualification

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A3-S1: Criteria builder** | Landlord dashboard, per property | Onboarding or edit | Income ratio, credit floor, eviction rules, move-in window, occupancy, pet/smoking policy | Edit fields, save | **Dual-write**: feeds pre-qual (A3.2) AND is the object published pre-charge in A5.2 — same stored object, two consumers | A3.1 |
| **A3-S2: Pre-qual SMS sequence** | Lead SMS | New Lead created | One question at a time | Text replies | Pass → A4 scheduling offer; Fail → A3-S3 | A3.2 |
| **A3-S3: Automated decline (SMS)** | Lead SMS | Pre-qual fails a criterion | Named failed criterion, optional co-signer path | Reply if co-signer path offered | Logged to Message Log, no refund implication (pre-fee) | A3.3 |
| **A3-S4: Auto Q&A (SMS)** | Lead SMS | Lead asks a question | Answer sourced from A2.2 knowledge base | Free text | If unanswered twice → gap-flags into A2-S3 | A3.4 |
| **A3-S5: Pipeline funnel view** | Landlord dashboard | Always available | Counts: inquiries → auto-declined → qualified → showed → interviewed, drill-down per stage | Click to drill into any Lead | None — this is the primary proof-of-value screen | A3.5 |

---

### A4 — Showings

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A4-S1: Host designation** | Landlord chat | New property / new turnover | Options: self or name a Trusted Individual | Select host, enter TI name+phone if applicable | Sends TI intro SMS if delegated | A4.1 |
| **A4-S2: TI intro + availability ask (SMS)** | Trusted Individual SMS | A4-S1 delegates | Intro message from AI | Reply with available time blocks | Availability stored on Trusted Individual entity | A1.3, A4.2 |
| **A4-S3: Landlord availability capture** | Landlord chat | A4-S1 self-hosts | Time block picker | Enter blocks | Same downstream as A4-S2 | A4.2 |
| **A4-S4: Showing offer (SMS)** | Lead SMS | Lead passes pre-qual (A3-S2) | Available slots | Pick a time or request alternative | Creates Showing record, confirms both sides | A4.2 |
| **A4-S5: Day-of reminder (SMS)** | Lead + Host SMS | Timer before showing time | Time, address, other party's name | — (informational) | — | A4.2 |
| **A4-S6: Post-showing read (SMS → landlord card)** [CORRECTED v2] | Host SMS, result surfaced in Landlord chat | Showing time passes | **Structured fields, not free text alone:** did they show (Y/N), would you rent to them (Y/N/Maybe), plus supplementary free text | Host replies via SMS; landlord views via card | Attached to Lead record, feeds decision alongside screening | A4.3 |
| **A4-S7: No-show flag** | Landlord dashboard | Repeated no-show pattern detected | Flag on Lead | Landlord can deprioritize | Downranks in A3-S5 pipeline view | A4.4 |

**Compliance note for design:** A4-S6 is flagged in the PRD as *the highest-risk Fair Housing surface in the product*. **v2 correction:** an earlier PRD draft dropped the Y/N/Maybe structured field in favor of free text alone — this was a regression and has been reverted here. Unconstrained free text is more likely to invite a stray protected-class comment than a bounded structured answer; free text should supplement the structured field, never replace it. Any free-text field here also needs visible guardrail copy (e.g. "Notes are reviewed for compliance") and should route through the guard before the landlord sees it — this may require a brief "processing" state rather than instant display.

---

### A5 — Application, Decision, and Lease

**v2 correction — no partial-compliance pathway exists.** An intermediate PRD draft suggested landlords could "default to Option A by selecting only one candidate at a time" to avoid refund obligations. This has been removed. Inviting one applicant at a time with discretion about whether to invite a second is not a compliant Option A queue (which requires strict, non-discretionary order-received processing) — it has none of Option A's legal protections and none of Option B's refund structure. **No screen in this document should present "invite one at a time" as a way to avoid the refund engine.** If a landlord genuinely invites only one applicant, that's a degenerate case of the same Option B flow (zero unselected co-applicants, so no refund event fires) — not a separate mode.

#### A5(i) — Batch invitation & fee disclosure

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A5-S1: Batch invite selector** | Landlord dashboard | Landlord reviewing showed/interviewed leads | Multi-select list of candidates | Select N candidates, "Invite to Apply" | Opens A5-S1a before sending | A5.1 |
| **A5-S1a: Refund-obligation framing (NEW v2)** | Landlord dashboard, interstitial before confirming invite | A5-S1 selection made | Plain statement: "You'll refund the application fee in full to anyone you don't select, automatically." Paired with brief framing on why a wider pool is worth the refund cost (better selection, minimal net cost with parallel screening) | Confirm & send, or go back and adjust selection | Sends application link SMS to each selected candidate | A5.1 (new, sits ahead of the point where a landlord might otherwise look for a workaround) |
| **A5-S2: Application invite (SMS)** | Applicant SMS | A5-S1a confirmed | Link to hosted application | Tap link | Opens A5-S3 | A5.1 |
| **A5-S3: Pre-charge disclosure (hosted web)** | Applicant hosted link | Link opened | Published criteria (from A3-S1), fee amount, screening-fee-rights statement, listing-availability confirmation, "I have a portable report" option | Proceed to pay, or declare portable report | **Hard block**: cannot proceed to payment if criteria/fee not set on property. Portable report → A5-S4b (no charge). Otherwise → A5-S4a | A5.2 |
| **A5-S4a: Fee payment (Stripe-hosted checkout)** | Applicant hosted link (Stripe) | A5-S3 proceed | Fee amount, itemized breakdown (service cost + time-value component) | Pay | Creates Screening Fee record, status=charged; triggers receipt (A5-S5) | A5.2 |
| **A5-S4b: Portable report intake** | Applicant hosted link | A5-S3 declares report | Upload/link portable report | Submit | No fee record created; `portable_report_used=true` on Application | A5.2 |
| **A5-S5: Receipt (auto-sent)** | Applicant SMS/email | Payment success | Itemized receipt | — | — | A5.2 |

#### A5(ii) — Screening execution & results

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A5-S6: Side-by-side screening dashboard** | Landlord dashboard | Screening partner returns results for any invited applicant | All batch applicants in parallel, each showing pass/fail vs. published criteria (A3-S1/A5.3), status per applicant (pending/complete). **No composite score, grade, or rank anywhere on this screen.** | View, compare | Feeds decision (A5-S7) | A5.3 |
| **A5-S7: Selection action** | Landlord dashboard | Landlord ready to decide | Same comparison view, "Select" button per applicant | Select one applicant | **Fires refund engine** for all others (A5-S8+); fires combined decline+refund notice (A5-S10); triggers adverse-action notice generation; unlocks A5-S11 (lease) | A5.3, A5.4 |
| **A5-S8: Credit report auto-delivery (SMS/email)** | Applicant | Screening partner returns result for that applicant | Copy of consumer credit report | — (automatic, unconditional if fee was paid) | — | A5.3 |

**v2 note on unselected candidates:** an intermediate PRD draft specified that unselected candidates "stay in the pool" and only receive a decline notice once the landlord signs someone — rather than being declined the moment another applicant is picked. This is folded into A5-S7's trigger description above and into A5-S10 below: the decline notice and the refund confirmation now fire together, as one combined message, at the moment of signing rather than at the moment of selection. This also means the refund clock (A5.4: 7 days from selection) starts at *signing*, not at the earlier "selected a favorite" moment if those are different events in the workflow — confirm this timing against A5.4's literal deadline language before build, since "selected a different applicant" and "signed a tenant" may not always be simultaneous in practice (e.g. lease negotiation could delay signing after a verbal pick).

#### A5(iii) — Refund engine — *the state machine that most needs to be visually unambiguous*

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A5-S9: Refund status card** | Landlord dashboard, per unselected applicant | Any of 3 triggers: tenant signed / applicant withdraws / listing pulled | Status (charged → refund_initiated → refunded/refund_failed), **countdown to effective_refund_deadline** (min of submission+30d, selection+7d) | None required — this is designed to be automatic. Manual "confirm" only appears on refund_failed (insufficient balance) | Auto-executes Stripe refund via standing authorization | A5.4 |
| **A5-S10: Combined decline + refund confirmation (Applicant SMS)** [CORRECTED v2] | Applicant SMS | Landlord signs selected tenant | **Single combined message**: polite decline notice + refund amount + which payment method it's returning to | — | Logs to Message Log | A5.1/A5.4 |
| **A5-S11: Refund failure alert (Landlord)** | Landlord dashboard + push/SMS alert | Insufficient Stripe balance detected | Amount owed, applicant, deadline remaining | "Use backup payment method" / resolve manually | Must not silently fail — this needs to be an interruptive alert, not a passive dashboard row | A5.4 |

**Design note — critical, unchanged from v1:** There is **no UI control anywhere** that lets a landlord mark an unselected applicant "no refund owed," and no "invite one at a time to avoid refunds" mode either (see A5 correction above). If any wireframe direction includes either pattern, that's a compliance bug in the design, not a feature to consider.

#### A5(iv) — Deposit, lease, move-in

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **A5-S12: Move-in date coordination (Landlord)** | Landlord chat | Screening in progress | Prompt for top 3 preferred dates | Enter dates | Stored, NOT surfaced to tenant yet | A5.5 |
| **A5-S13: Lease review & e-sign (hosted, both parties)** | Landlord dashboard + Applicant hosted link | Applicant selected | Generated lease doc via e-sign partner | Review, sign | Triggers deposit checkout | A5.5 |
| **A5-S14: Deposit + first month checkout** | Applicant hosted link (Stripe) | Lease signed | Amount due, jurisdiction-specific disclosures (21-day CA return, AB 2801 photo prompt, etc.) — **blocked entirely in Chicago/Cook per §7** | Pay | Releases move-in packet (A5-S15) | A5.5, §7 |
| **A5-S15: Move-in packet delivery** | Applicant SMS/hosted link | Funds clear | Utility transfer info, HOA rules, key handoff logistics, dated move-in photos prompt, **delivered as a PDF** | — | — | A5.6 |

---

## 4. Screen Inventory — Feature Set B (Maintenance & Make-Ready)

### B1 — Intake & Triage

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **B1-S1: Tenant issue report (SMS)** | Tenant SMS | Tenant texts the dedicated line | AI-guided structured intake: what, where, since when, photos | Reply/upload | Creates Ticket, status=triaging | B1.1 |
| **B1-S2: Guided troubleshooting (SMS)** | Tenant SMS | Common resolvable issue detected | Step-by-step (breaker, disposal reset, filter, shutoff) | Follow steps, confirm resolved or not | Resolved → close ticket; Not resolved → B1-S4 | B1.2 |
| **B1-S3: Hazard escalation (bypass)** | Landlord — call + SMS simultaneously | Gas/sparking/flooding/no-heat/CO keyword or photo detected | Full ticket immediately, marked emergency | Immediate response | **No triage delay — hard requirement** | B1.3 |
| **B1-S4: Triaged ticket card** | Landlord dashboard | Non-emergency issue confirmed unresolved | Photos, suspected cause, urgency, recommended action | Review, proceed to vendor match | Opens B2-S1 | B1.4 |

### B2 — Vendor Coordination

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **B2-S1: Vendor directory** | Landlord dashboard (Settings) | Always available | Landlord's own contacts, tagged by trade | Add/edit vendor | Feeds B2-S2 matching | B2.1 |
| **B2-S2: Match & draft message** | Landlord dashboard | Ticket ready (B1-S4) | Suggested vendor, drafted copy-pasteable message w/ photos | Edit, copy, send themselves (outside KeyFrame) | Ticket status=dispatched | B2.2 |
| **B2-S3: Follow-up prompt (Landlord)** | Landlord SMS/chat | Timer after B2-S2 | "Closed? Cost? Who?" | Reply | Parsed into ticket + expense log | B2.3 |
| **B2-S4: Expense log view** | Landlord dashboard | Ticket closed | Dated, categorized expense line, invoice attachment | Export | Feeds tax-time export | B2.4 |

### B3 — Make-Ready

| Screen | Surface | Entry trigger | State shown | Actions | Triggers next | PRD |
|---|---|---|---|---|---|---|
| **B3-S1: Move-out condition capture (SMS)** | Outgoing Tenant SMS | Weeks before move-out (from A1-S4) | Room-by-room checklist prompt, photo requests | Reply/upload | Generates scope list | B3.1 |
| **B3-S2: Make-ready scope list** | Landlord dashboard | B3-S1 complete | Clean/paint/repair/replace items | Route each to B2 | Each item becomes a Ticket | B3.2 |
| **B3-S3: Multi-item project tracker** | Landlord dashboard | Multiple make-ready tickets open | Quote vs. final invoice per line item, dropped-item flags | Review | Flags discrepancies | B3.3 |
| **B3-S4: Re-list readiness gate** | Landlord dashboard | Target listing date approaching | Open make-ready items vs. target date | Acknowledge or address | Blocks/unblocks re-listing (soft warning, not hard block) | B3.4 |

---

## 5. Applicant / Tenant-Facing Screen Summary (all SMS + hosted links, no account)

Full list, cross-referenced above, gathered here for a design-system pass since these need the most careful, trust-building visual treatment (a stranger is being asked to pay a fee here):

- A5-S2 (invite) → A5-S3 (disclosure — **highest design priority, this is the money screen**) → A5-S4a/b (payment or portable-report intake) → A5-S5 (receipt) → A5-S8 (report delivery) → A5-S10 (combined decline + refund, if applicable) → A5-S13 (lease sign) → A5-S14 (deposit checkout) → A5-S15 (move-in packet)

---

## 6. Trusted Individual Screen Summary (SMS only)

- A1-S5 → A4-S2 (intro + availability) → A4-S4/A4-S5 (per-showing coordination) → A4-S6 (post-showing read, structured + free text) → (if outgoing tenant) B3-S1 (move-out condition capture)

---

## 7. Cross-Cutting Systems

| System | What it does | Where it touches the UI |
|---|---|---|
| **Fair Housing + Refund-Compliance Guard** | Filters AI-generated messages for protected-class content; blocks refund-skip code paths **and blocks any "invite one at a time" workaround pattern (v2)** | Every AI-authored SMS/message; A4-S6's structured field requirement; A5-S9's absence of a "deny refund" control; A5-S1's absence of a sequential-invite mode |
| **Message Log** | Append-only log of every AI↔party message + every refund event | Not user-facing as a primary screen, but should exist as an admin/audit view for landlord or founder review |
| **Jurisdiction Gating (§7)** | Blocks/modifies A5.5 (deposit) in Chicago/Cook; governs which fee-cap logic applies in A5-S3/S4a (CA numeric cap vs. IL cost-justification vs. Chicago $20 cap) | Property setup screen must capture jurisdiction; A5-S3/S14 render differently per jurisdiction |
| **10DLC/TCPA consent (§6)** | Consent capture, STOP handling | First SMS to any new Lead/Tenant/TI must include opt-out language |

---

## 8. State Machine Reference (entity statuses)

| Entity | Status values |
|---|---|
| **Lead** | new → pre-qualifying → qualified / declined → showing_scheduled → showed → invited_to_apply |
| **Showing** | scheduled → confirmed → completed → (no_show flag) |
| **Application** | invited → submitted → (fee_pending / portable_report) |
| **Screening Fee** | charged → report_delivered → selected / unselected → refund_initiated → refunded / refund_failed |
| **Screening** | pending → complete → pass/fail vs. criteria |
| **Lease** | drafted → sent → signed |
| **Payment** (deposit/rent) | pending → cleared → failed |
| **Ticket** | reported → triaging → (emergency flag) → dispatched → in_progress → closed |
| **Expense** | auto-created on Ticket close |

---

## 9. Notes for handoff

**To Gemini (competitor teardown / wireframe exploration):** the four screen types worth generating multiple directions for, in priority order:
1. **A5-S6/A5-S7** — the parallel-applicant comparison dashboard (this is the product's core differentiator, get this right)
2. **A5-S3** — the applicant-facing fee/rights disclosure screen (money + trust, first impression for a stranger)
3. **A5-S9** — the refund status/countdown screen
4. **A4-S4/A4-S6** — showing scheduling + post-showing read

**To Claude Design (final build):** build from whichever direction is selected for the four screens above first — they're the highest-risk and highest-differentiation surfaces. Everything else in this document (A1–A3, B1–B3) is closer to standard SaaS pattern and lower risk to get slightly wrong on the first pass. §10 below contains the actual direction recommendations from the completed synthesis.

**What NOT to wireframe yet:** anything under A5(iii) refund engine's *logic* (deadline math, trigger conditions) — only the *display* of a status and countdown fed by static example data. Same constraint given to Gemini.

---

## 10. Wireframe Direction Synthesis (completed — supersedes any partial synthesis from Gemini's teardown)

Each screen type below has three candidate directions, a recommendation, and a compliance check specific to that screen. Directions were evaluated against 8 competitors (TurboTenant, Hemlane, Avail, RentRedi, Showdigs, Propilot, Zillow Rental Manager, Mynd) — **zero of which show an applicant a refund status, refund rights, or queue position**, confirming this as genuinely unbuilt territory rather than underbuilt.

### 10.1 — Parallel applicant comparison dashboard (A5-S6/S7)

- **Direction A — Criteria matrix.** Applicants as columns, landlord's published criteria (A3.1) as rows, pass/fail per cell. No aggregate score anywhere.
- **Direction B — Stacked cards with sticky criteria legend.** Mobile-first; each applicant is a card, criteria pinned at top for reference while scrolling.
- **Direction C — Normalized single-column profiles, viewed in sequence but pre-normalized** (RentRedi's data-normalization pattern) — same data shape as A, but browsed one at a time instead of side-by-side.

**Recommended: Direction A.** It's the only one that actually visualizes "parallel," which is the whole product thesis. Direction C quietly reintroduces sequential viewing even if the charging is parallel — a UX regression hiding inside a compliant backend.

**Compliance check:** no direction may include a composite grade, score, or ranked order — this rules out Propilot's A/B/C/D grading pattern outright. The PRD is explicit that KeyFrame "does not score, rank, or recommend applicants." A status strip ("invited: 5 · results in: 3 · pending: 2") is fine — that's pipeline state, not a judgment about people. Kanban-style pipeline boards (Hemlane, Showdigs) are a different screen (A3-S5's funnel view) and should not be conflated with this one.

### 10.2 — Applicant fee disclosure (A5-S3)

- **Direction A — Single scrolling page.** Criteria rendered as a checklist the applicant reads before the pay button activates; refund promise given equal visual weight to the fee amount; portable-report option at the same weight as the pay button.
- **Direction B — Conversational/stepped gate** (TurboTenant Pre-Screener pattern): question-by-question, ending in a pay screen.
- **Direction C — Modal summary over the application form**, fee terms as an expandable disclosure rather than a full page.

**Recommended: Direction A.** Direction B is good UX for pre-qualification (already used at A3.2) but this is a paid legal disclosure, not a filter — burying it in a conversational flow risks the applicant not registering it as a binding term. Direction C risks the refund promise reading as boilerplate rather than the differentiator it is.

**Compliance check:** the pre-charge hard-block (no criteria set = no pay button, full stop) must be a real disabled state in the design, not a validation error shown after the fact. Zillow's 30-day reusable fee is worth mirroring in tone for the portable-report messaging, since applicants may already recognize the concept.

### 10.3 — Refund status and countdown (A5-S9/S11)

- **Direction A — Embedded row within the same comparison dashboard** used for selection (A5-S6/S7), so "I picked someone" and "four refunds are now processing" are visually adjacent.
- **Direction B — Separate "Refunds" tab/section** in the nav.
- **Direction C — Timeline/activity feed style**, refunds appear as chronological log entries.

**Recommended: Direction A.** Direction B risks a landlord never visiting the tab and missing an active countdown; the point of this screen is that the causal link to the landlord's own selection action must be unmissable. Direction C is fine as a *secondary* audit view (could double as the Message Log surface from §7) but shouldn't be the primary place a landlord learns about an active deadline.

**Compliance check:** no variant includes a control to skip, deny, or delay a refund, and none includes an "invite one at a time" alternative path (see §3, A5 correction). Countdown displays days remaining, not a raw date. A5-S10's combined decline+refund message (v2 correction) should be reflected here too — the dashboard row and the applicant-facing message fire from the same event, so their copy/timing should visibly match in any prototype.

### 10.4 — Showing scheduling + post-showing read (A4-S4/A4-S6)

- **Direction A — List/Board/Timeline toggle** (Showdigs pattern, with all self-tour/smart-lock elements stripped — out of scope for this product).
- **Direction B — Calendar-week view** as default.
- **Direction C — Single unified "today's activity" feed**, showings and reads mixed chronologically.

**Recommended: Direction A**, defaulting to Timeline view. It's the strongest pattern found in the competitor set, is genuinely borrowable once the self-tour piece is removed, and scales better than a calendar view once a landlord has multiple concurrent showings across properties. Hemlane's adverse-action modal (a compliance action surfaced as a clean one-click UI element) is the right pattern to borrow separately for A5-S7's decline flow.

**Compliance check:** the post-showing read card (A4-S6) must show **Y/N (showed up) + Y/N/Maybe (would you rent to them) + free text** — not free text alone. This is the corrected version from §3 above; any wireframe direction that drops the structured field back to free-text-only should be treated as reintroducing a fixed bug, not as a stylistic choice.
