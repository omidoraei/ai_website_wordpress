# Decision ledger

Append-only. A decision is never deleted; it is superseded by a later row that names it.
Columns: `id | decision | rationale | owner | status | reversal trigger | phase`.

The live copy of this ledger is the Notion page **"Aurora AI — Decision Ledger (P-BRIEF)"**
(`app.notion.com/p/Aurora-AI-Decision-Ledger-P-BRIEF-3f68dd8c323d81198787fe3ad7064d66`).
The Notion page was created with rows 000–005 on 2026-10-12; subsequent appends failed twice with
connector errors and are therefore recorded **here** as the authoritative copy, with the failure
recorded in `HANDOFF-PBRIEF.md` (no silent divergence).

## P0 / P0.5 / P1 decisions already made (recorded retroactively)

| id | decision | rationale | owner | status | reversal trigger | phase |
| --- | --- | --- | --- | --- | --- | --- |
| D-001 | Container responsive visibility exists and the kit's 6 uses are valid | `includes/base/element-base.php:L1383` builds `hide_<device>` dynamically; `includes/elements/container.php:L1906` registers it | agent | VERIFIED (reverses the P0 note) | none — settled with source lines | P0 |
| D-002 | The button background keys are a switcher and its value, not two independent writes | `includes/widgets/traits/button-trait.php` is byte-identical between v3.35.9 and v4.0.8 | agent | VERIFIED | a Pro/free behavior difference found on a real install | P0.5 |
| D-003 | Elementor Templates/Content import runners expect WP post exports; the kit declares both empty | Import/export runner source read from the vendored archive | agent | VERIFIED | an import test on a real WP site contradicts it | P0 |
| D-004 | "40 documents" is retired: 39 templates + 1 Kit document | two different counters were conflated under one word | agent | SUPERSEDED by `docs/METRICS.md` | none | P0.5 |
| D-005 | The retired "18/18" colour-and-font figures are replaced by defined counters: 19 global colour entries, 15 typography presets, 3 font families | the axes were conflated; definitions in `docs/METRICS.md` §2 | agent | SUPERSEDED | none | P0.5 |
| D-006 | A CI artifact digest is not used as a determinism proof | digests differ across runs of the same commit; determinism is proven by rebuild diff + local zip sha256 | agent | VERIFIED | none | P0.5 |
| D-007 | The CI gate is hermetic: Elementor sources vendored, sha256 verified before extraction | a network clone lets upstream re-tags change the "verified" line numbers | agent | VERIFIED | a tag bump with re-recorded hashes | P0.5 |
| D-008 | `upload-artifact` moved to v7 (the brief said v5) | v5's own run annotation still named it as Node-20 deprecation | agent | VERIFIED (deviation recorded) | a v7 breakage on the runner | P0.5 |
| D-009 | The P0.5 turn cap was exceeded (13 batches against 8) to land a green gate | stopping mid-repair would have left a gate that fails on the next push | agent | RECORDED (deviation) | never — this is an honest deviation record | P0.5 |
| D-010 | Arad is not bundled and is referenced by family name only | licence UNVERIFIED; Vazirmatn (OFL-1.1) is the audited fallback | agent | SUPERSEDED by D-013 | Arad licence proof produced | P1 |
| D-011 | Dial alias `UI_DENSITY` vs `VISUAL_DENSITY` is not silently renamed | the taste skill's alias is `VISUAL_DENSITY`; the spec says `UI_DENSITY`; the difference is documented in `dials.toml` | human | OPEN-LOW (deferred to P2) | either name proves to have a downstream consumer | P1 |
| D-012 | `banlist_check.py` pitfalls (metrics inside price/field options; leading digits in numbered steps; unresolved global typography) are treated as detector bugs, not content bugs | false positives degrade trust in a gate | agent | FIXED | a re-occurrence with a counter-example | P1 |

## P-BRIEF decisions (this phase)

| id | decision | rationale | owner | status | reversal trigger | phase |
| --- | --- | --- | --- | --- | --- | --- |
| P-BRIEF-000 | Interview mode opened; no design artifacts produced until the brief is signed | P0/P1 were built against a brief nobody signed | human | OPEN | interview abandoned → P1 artifacts stay CONDITIONAL | P-BRIEF |
| P-BRIEF-001 | Dial alias deferred | naming only, no downstream consumer | human | DEFERRED (OPEN-LOW) | decide with the re-derived dials | P2 |
| P-BRIEF-002 | Arad licence escalated to a blocking question | an unlicensed embedded font is unsellable and a liability | human | ESCALATED → answered by B5 | B5 answer | P-BRIEF |
| P-BRIEF-003 | The 15 `dials.toml` values are VOID | calibrated against an unsigned brief | human | VOID | re-derived in P1-R | P1-R |
| P-BRIEF-004 | Placeholder policy converted into question B4 | fabrication is a labelling duty for a sold kit, not a taste choice | human | CONVERTED | B4 answer + list | P-BRIEF |
| P-BRIEF-005 | The top-3 P2 fixes are re-prioritised after B1–B5 | risk order depends on the product type | human | RE-PRIORITISED | re-ranked with the B4 list | P2 |
| P-BRIEF-006 | B1 ANSWERED — human selected *"A Template Kit to sell / distribute"* (`sell_kit`) | a product for third parties, not a live site | human | ANSWERED | reversal to own-site/client turns fabrication into legal exposure | P-BRIEF |
| P-BRIEF-007 | B2 ANSWERED — human selected *"Genuinely bilingual, equal parity"* (`equal_parity`) | EN and FA both stay first-class | human | ANSWERED | Persian-primary would void the EN half | P-BRIEF |
| P-BRIEF-008 | B3 ANSWERED — human selected *"Book a demo"* (`book_demo`); KPI = qualified demo requests | a single primary CTA across the kit | human | ANSWERED | a trial/checkout CTA changes IA and Pricing | P-BRIEF |
| P-BRIEF-009 | B4 ANSWERED (partial) — human selected *"Mixed — I will list what is real"* (`mixed`) | the real-vs-sample list is still pending | human | ANSWERED-PARTIAL | the list arrives, or every unevidenced item is cut/labelled | P-BRIEF |
| P-BRIEF-010 | B5 ANSWERED — human selected *"Switch the FA type system to Vazirmatn now"* (`switch_vazirmatn`) | deletes the Arad licence risk; OFL-1.1; self-host via Custom Fonts | human | ANSWERED | Arad licence proof arrives and the human asks for it | P-BRIEF |
| P-BRIEF-011 | Aurora is the kit's demo brand, not the owner's identity | follows from B1 = sell-kit; buyers rebrand | agent | ASSUMPTION (MED) | the kit must also be the human's live site | P-BRIEF |
| P-BRIEF-012 | Fabricated data is allowed only when visibly labelled SAMPLE/DEMO; otherwise removed | a sold kit owes buyers labelling, not a legal myth | agent | DECIDED (pending B4 list) | a channel's review rules forbid sample data | P2 |
| P-BRIEF-013 | FA type system = Vazirmatn (OFL-1.1); Arad removed from bundling | B5 answer | agent | DECIDED | Arad licence proof | P2 |
| P-BRIEF-014 | C1 ANSWERED — human selected *"Keep all nine + popup"* (`full_nine`) | breadth is the product for a sold kit | human | ANSWERED | a channel limits page count | P2 |
| P-BRIEF-015 | C2 ANSWERED (partial) — human selected *"I'll paste 3–6 references + 2–3 anti-references"* (`will_paste`) | links pending; DNA re-derivation is blocked on them | human | ANSWERED-PARTIAL | no links by gate 1 → derive from the brief, flagged as such | P1-R |
| P-BRIEF-016 | C3 ANSWERED (partial) — human selected *"I have a logo, no photography"* (`logo_only`) | logo file, distribution channel and maintainer still pending | human | ANSWERED-PARTIAL | no logo file → editable demo wordmark ships | P2 |
| P-BRIEF-017 | C4 ANSWERED — human selected *"I can install Elementor Pro on a staging site"* (`pro_available`) | Pro verification becomes a P2 acceptance criterion | human | ANSWERED | staging install lost → Pro controls stay UNVERIFIED | P2 |
| P-BRIEF-018 | C5 ANSWERED — human selected *"Assume EU buyers → WCAG 2.2 AA baseline + no-tracking posture documented"* (`eu_strict`) | accessibility baseline becomes a build gate; the consent hole is documented for the buyer | human | ANSWERED | non-EU distribution relaxes the framing, not the baseline | P2 |
| P-BRIEF-019 | Batch 3 was skipped by the human ("keep going"); its five questions are recorded as assumptions A4, A5+A6, A9, A10, A11 | the phase rule says a skip becomes an ASSUMPTION with risk + reversal trigger, not a silent default | human | RECORDED | the answers arrive at or before gate 1 | P-BRIEF |
| P-BRIEF-020 | The palette (charcoal + amber + coral) is UNRATIFIED and VOID as a build description | no human brand exists; coral = 15 of 2 136 colour refs vs amber-600 = 294 (`docs/p1/delta-table.md:60-61`) | agent | VOID | P1-R re-derives the palette with an accent budget | P1-R |
