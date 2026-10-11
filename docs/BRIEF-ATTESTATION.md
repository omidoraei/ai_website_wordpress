# Brief attestation — human paste (class-A bootstrap)

**ATTESTATION_INPUT_MISSING** (P1.8, 2026-10-12). The P1.8 phase searched the phase prompt and the
session for attestation text and found **none**. Nothing was written, no row was upgraded, and no
answer was inferred: the ten rows below stay **CLASS-B-PENDING**. To close this item the human must
paste the B1-B5 / C1-C5 answers below, in their own words (one line per row is enough). The agent
then commits this file, records the commit hash and the file sha256 in `docs/CLAIMS.md`, and
upgrades only the rows whose text is present to **CLASS-A**. Blank rows stay pending.

**Status: EMPTY — awaiting the human. Highest-priority input to gate 2.**

This file is the one step that converts the ten chat-channel answers into **class A**
(machine-addressable) evidence. Until it is filled, those answers are **class B (human-attested)**
— see the evidence-classes table in `AGENTS.md` and `docs/PBRIEF-TRANSCRIPT.md`.

How it works:

1. The human pastes their answers below, in their own words (short is fine — one line per row).
2. The agent commits this file and records the **commit hash** in `docs/CLAIMS.md`.
3. From that commit on, those rows are class A: durable, reviewable without this conversation, and
   citable by id + hash.

Rules: paste what you actually decided. If a decision has changed since 2026-10-12, say so and the
agent records it as a reversal rather than silently rewriting the option. Leave any row you do not
want to attest blank — a blank row stays class B.

---

## B1 — product type
recorded option: `sell_kit` — "A Template Kit to sell / distribute"
human attestation (paste here):

## B2 — language and RTL weight
recorded option: `equal_parity` — "Genuinely bilingual, equal parity"
human attestation (paste here):

## B3 — job to be done / primary CTA and KPI
recorded option: `book_demo` — "Book a demo" (KPI: qualified demo requests)
human attestation (paste here):

## B4 — real data policy
recorded option: `mixed` — "Mixed — I will list what is real" (the list never arrived)
human attestation (paste here):

## B5 — brand, font licence, FA type system
recorded option: `switch_vazirmatn` — "Switch the FA type system to Vazirmatn now"
human attestation (paste here):

## C1 — page scope
recorded option: `full_nine` — "Keep all nine + popup"
human attestation (paste here):

## C2 — taste references
recorded option: `will_paste` — "I'll paste 3–6 references + 2–3 anti-references" (links never arrived)
human attestation (paste here):

## C3 — brand assets
recorded option: `logo_only` — "I have a logo, no photography" (file never arrived)
human attestation (paste here):

## C4 — Pro availability
recorded option: `pro_available` — "I can install Elementor Pro on a staging site"
human attestation (paste here):

## C5 — compliance posture
recorded option: `eu_strict` — "Assume EU buyers → WCAG 2.2 AA baseline + no-tracking posture documented"
human attestation (paste here):

---

## Batch-3 skip (optional, same mechanism)
recorded: batch 3 (5 questions) was skipped with the message "keep going"
human attestation (paste here):
