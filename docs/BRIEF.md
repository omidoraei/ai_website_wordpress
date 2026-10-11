# Aurora AI kit — signed brief (P-BRIEF)

**Status: PARTIALLY SIGNED.** 10 of the 15 interview questions were answered by the human on
2026-10-12; the third batch (5 questions) was **skipped** (the human's message: "keep going").
Skipped questions are recorded below as **ASSUMPTION** rows with a risk rating and a reversal
trigger, in line with the phase rules. No design artifact has been approved in this conversation:
approval stops at the answers quoted here.

**Proof-of-approval rule.** Every **ANSWERED** line quotes the human's literal reply — the option
label they selected in the interview UI, with the option id and the date. If a line does not carry
such a quote, it is not approved and is marked ASSUMPTION.

Question batches: batch 1 = B1–B5 (blocking), batch 2 = C1–C5, batch 3 = B4 list / C2 references /
C3 logo + channel / C6 definition of done / C7 gates — **skipped**.

---

## 1. Product identity

**ANSWERED — B1.** Human selected: *"A Template Kit to sell / distribute"* (option `sell_kit`,
2026-10-12).

This is a **commercial product for third parties**, not a live business site. Consequences:
sample data must be visibly labelled, copy stays generic, assets must be licence-clean, and no
fabricated claim may be presented as the kit author's own fact.

**ASSUMPTION (risk MED) — A1.** "Aurora AI" is the kit's **demo brand**; buyers rebrand.
*Reversal trigger:* the human states the kit must also run as their own live site (then the palette,
logo and copy become real-brand deliverables and fabrication becomes a legal rather than a
labelling problem). Surfaced at gate 1.

## 2. Audience and job to be done

**ANSWERED — B3.** Human selected: *"Book a demo"* (option `book_demo`, 2026-10-12).
Primary CTA = **book a demo**. KPI = **qualified demo requests**.

**ASSUMPTION (risk LOW) — A2.** The visitor is a technical evaluator of an AI/SaaS product
(the accepted option's description said "technical buyer evaluating the product"); the human did
not independently restate it. *Reversal trigger:* the human names a different buyer at gate 1.

**ASSUMPTION (risk MED) — A3.** What the visitor "already believes about this category" was never
collected (batch 3 skipped). Working position: the category is saturated with unverifiable AI
claims, so the kit's demo must **show evidence, not adjectives**. *Reversal trigger:* the human
supplies their own read of the audience at gate 1.

## 3. Language and RTL weight

**ANSWERED — B2.** Human selected: *"Genuinely bilingual, equal parity"* (option `equal_parity`,
2026-10-12).

EN and FA are both first-class. The FA set is a **re-layout, not a mirror**: logical properties
only, Vazirmatn typography (see §6), and Persian copy reviewed at JSON level with
`tools/bidi_check.py`, never from a rendered diff.

Coverage note (measurement, not a claim of parity): the current tree carries 9 pages, of which
1 is FA (`templates/pages/aurora-home-fa.json`), plus 5 FA blocks and an FA header/footer — 8 FA
documents in total against 39 templates. "Equal parity" is therefore a **target for content
coverage**, and P1-R/P2 must say what parity means per page.

## 4. Scope

**ANSWERED — C1.** Human selected: *"Keep all nine + popup"* (option `full_nine`, 2026-10-12).

Nine pages ship: Home · About · Services · Portfolio · Pricing · Blog (Journal) · Single Post ·
Contact · 404 — plus Header/Footer theme-builder parts and one **exit-intent popup** (Pro).
The block library's breadth is the product (22 blocks today), so block count is a feature, not
bloat. Evidence: `ls templates/pages` → 9 files; `templates/popups/aurora-lead-magnet.json`.

## 5. Data policy

**ANSWERED (partial) — B4.** Human selected: *"Mixed — I will list what is real"* (option `mixed`,
2026-10-12). The list was never supplied (batch 3 skipped).

**ASSUMPTION (risk HIGH) — A4.** Until the human's list arrives, **every dataset ships with a
visible SAMPLE / DEMO label** — metrics, prices, client logos, testimonials, team, case studies,
blog posts. No fabricated metric ships unlabelled. *Reversal trigger:* the human's list arrives →
real items get named sources; the rest keep the label or are removed (removal preferred for
anything a buyer could mistake for a promise). Surfaced at gate 1.

Consequence for the existing build: the 8 fabricated metrics, placeholder prices and unlabelled
testimonials are a **labelling defect** under this brief, and they outrank every aesthetic fix in
P2 (see `docs/p1/delta-table.md` and `docs/P1-DISPOSITION.md`).

## 6. Brand, type and assets

**ANSWERED — B5.** Human selected: *"Switch the FA type system to Vazirmatn now"* (option
`switch_vazirmatn`, 2026-10-12). Vazirmatn is SIL OFL-1.1, self-hosted through Elementor Custom
Fonts, no custom CSS. **Arad leaves the build.** It may return only as an optional documented swap
if the human produces licence proof.

**ANSWERED (partial) — C3.** Human selected: *"I have a logo, no photography"* (option `logo_only`,
2026-10-12). The file was never supplied.

**ASSUMPTION (risk LOW) — A5.** Until the logo file arrives, the kit ships an **editable demo
wordmark** (a native Image/icon element, not custom code) with a documented swap-in path.
*Reversal trigger:* logo file arrives → replace the placeholder and record the licence of the file.

**ASSUMPTION (risk MED) — A6.** Distribution channel and post-handover maintainer were never
collected (batch 3 skipped). Working position: the kit is distributed through a store-style channel
and the **buyer is the maintainer**, so documentation must be buyer-facing. *Reversal trigger:*
the human names a channel (e.g. Envato) and a maintainer; channel review rules may also constrain
page count and sample-data labelling.

**Palette: UNRATIFIED → VOID.** The human has no brand book (B5 question on brand assets was
skipped; C3 = logo only). The current charcoal + amber + coral palette is **not approved**, and as
built it does not implement itself: `amber-600` has 294 references against `primary` 299 and
`secondary` 272, while the coral `accent` has 15 of 2 136 colour references
(`docs/p1/delta-table.md:60-61`). A two-accent system exists on paper only. Re-derived in P1-R
with an accent budget expressed as a rule.

## 7. Compliance posture

**ANSWERED — C5.** Human selected: *"Assume EU buyers → WCAG 2.2 AA baseline + no-tracking posture
documented"* (option `eu_strict`, 2026-10-12).

Accessibility (contrast, focus visibility, motion reduction) is a **build gate**, not a polish
item. The kit ships **no tracking** and documents the consent hole the buyer must fill themselves.

**ASSUMPTION (risk LOW) — A7.** No AI-crawler policy was stated. Working position: documentation
mentions `llms.txt` as an option; the kit bakes in no Content Signals or pay-per-crawl defaults.
*Reversal trigger:* the human states a policy.

## 8. Constraints and budget

**ANSWERED — C4.** Human selected: *"I can install Elementor Pro on a staging site"* (option
`pro_available`, 2026-10-12). Pro-control verification becomes an **acceptance criterion of P2**
and closes P0's UNVERIFIED Pro debt — once the staging URL and licence are supplied.

**ASSUMPTION (risk MED) — A8.** Deadline and monetary budget were never collected (batch 3
skipped). Working position: phase turn caps as stated in each phase prompt (this phase: 12), and no
paid-API spend without explicit approval. *Reversal trigger:* the human states a deadline or a cap.

## 9. Taste references

**ANSWERED (partial) — C2.** Human selected: *"I'll paste 3–6 references + 2–3 anti-references"*
(option `will_paste`, 2026-10-12). No references were received (batch 3 skipped).

**ASSUMPTION (risk HIGH) — A9.** P1's DNA stays VOID. P1-R re-derives DNA from this brief plus the
brief's own constraints and reports, at gate 1, the difference between default-derived and
reference-derived choices — flagging every decision a human reference could overturn.
*Reversal trigger:* references arrive (they outrank everything derived here).

## 10. Definition of done (draft — NOT approved)

**ASSUMPTION (risk MED) — A10.** C6 was skipped; these five falsifiable criteria are proposed for
approval or editing at gate 1:

1. **Sourcing.** Every statistic, price and testimonial is either sourced (source named in the kit
   docs) or visibly labelled SAMPLE. Check: no fabricated-metric finding without a label.
2. **Traceability.** Every colour, font size and spacing value resolves to a global or a Kit
   style; no one-off hex/px outside the token set. Check: token census + no raw values in widgets.
3. **Editability.** Every text/image/button/spacing/background control is native; Custom HTML
   widgets = 0; every Pro-only control carries a documented Free fallback.
4. **Rhythm.** No two adjacent sections share the same skeleton, and the BANLIST FAIL bands are
   empty at the final gate. Check: `tools/banlist_check.py` FAIL count = 0.
5. **RTL.** The FA set passes the bidi scan and reads correctly to a Persian speaker; EN/FA parity
   is measured per page, not asserted.

## 11. Human gates

**ASSUMPTION (risk LOW) — A11.** C7 was skipped; the five booked slots stand:
gate 1 DNA (2026-10-14) · gate 2 IA + scope (10-16) · gate 3 block specs (10-19) ·
gate 4 FA/RTL read-through (10-21) · gate 5 final QA (10-23) — all 16:00 UTC, 45 minutes,
created on the human's primary calendar. *Reversal trigger:* the human replaces the schedule
or reduces the gate count.

## 12. Open assumptions, re-surfaced at gate 1

| id | assumption | risk | reversal trigger |
| --- | --- | --- | --- |
| A1 | Aurora is a demo brand, not the owner's identity | MED | kit doubles as the human's live site |
| A2 | visitor = technical evaluator | LOW | human names another buyer |
| A3 | category baseline: evidence over adjectives | MED | human's read of the audience |
| A4 | every unevidenced dataset carries a SAMPLE label | HIGH | B4 list arrives |
| A5 | placeholder editable wordmark until the logo file arrives | LOW | logo file arrives |
| A6 | store distribution; buyer maintains | MED | channel + maintainer named |
| A7 | no crawler policy baked in | LOW | policy stated |
| A8 | no deadline/cash budget recorded | MED | budget stated |
| A9 | DNA re-derived from brief; references pending | HIGH | references arrive |
| A10 | definition of done = the five criteria above | MED | human edits the list |
| A11 | five gates as booked | LOW | human replaces the schedule |
