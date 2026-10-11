# P1 disposition — what survives the signed brief

P1 was executed against a brief nobody had signed. This table is the accounting: every P1 artifact
gets a verdict, a reason, and the condition the brief would have to state for it to survive.
**No VOID or CONDITIONAL row may be used as input to P2** until P1-R (re-derivation) replaces it;
P2 must cite the replacement, not the original.

Verdicts: **SURVIVES** (brief-independent) · **VOID** (built on unsigned assumptions) ·
**RE-DERIVE** (the work is needed, the content is not) · **CONDITIONAL** (survives only if the
brief says a specific thing).

| artifact | verdict | reason | what the brief must say for it to survive |
| --- | --- | --- | --- |
| `docs/p1/dna.yaml` | **RE-DERIVE** | Derived from skill defaults plus admired references chosen by the agent; the human never supplied a reference (C2 = `will_paste`, links never arrived) | The brief must name the reference set, or explicitly accept category-derived DNA. Until then the DNA is a proposal, not a baseline |
| `dials.toml` — 15 page-type dial values | **VOID** | Calibrated against the unsigned assumption (AI-SaaS, premium, animation-forward). Acceptance rule: the 15 values must be marked VOID | Re-derive in P1-R from the signed brief: B1 sell-kit (the demo must be vivid), B3 demo CTA, B2 parity, C5 a11y baseline |
| `dials.toml` — invariants (animated ≤ 0.25, centred ≤ 0.55, eyebrow ≤ 0.60, zero em-dash, no fake metrics) | **CONDITIONAL** | Measurable guardrails, cheap to keep; but "no fake metrics" must become "no *unlabelled* fake metrics" under a sold kit with labelled sample data | Keep the invariants, re-express the fake-metrics rule as a labelling rule (P-BRIEF-012) |
| `BANLIST.md` | **SURVIVES** | Deterministic detectors are brief-independent; the anti-pattern bands describe generic AI tell-tales, not taste | Keep as-is; update the fabricated-metric rule text in P2 to match the labelling policy |
| `docs/p1/type-decision.md` — the Arad block | **VOID** | B5 = switch to Vazirmatn now; the licence risk is deleted rather than documented away | Vazirmatn metrics replace Arad in P1-R/P2; Arad returns only with licence proof |
| `type-decision.md` — the size ladder (H1 64/48/36, H2 46/36/28, H3 22, body 17/1.75, eyebrow 13) | **CONDITIONAL** | Chosen against the unsigned brief and Arad's metrics; Vazirmatn has different metrics | Re-derive the ladder for Vazirmatn; keep the three-breakpoint structure as a requirement |
| `docs/p1/delta-table.md` — the ranking | **CONDITIONAL** | Ranked aesthetics ahead of content honesty; under a sold kit with a pending B4 list, labelling defects outrank every visual fix | Re-rank: (1) data labelling + legal surface, (2) structure/rhythm, (3) aesthetics (P-BRIEF-005) |
| 22 blocks (17 EN + 5 FA) | **SURVIVES** | C1 = "Keep all nine + popup": breadth is the sellable surface, so the block library stays | No change; FA blocks adopt Vazirmatn and re-measure parity |
| 9 pages | **SURVIVES** | C1 answer | As-is |
| Exit-intent popup (`aurora-lead-magnet.json`, Pro) | **SURVIVES as a Pro demo feature** | C1 keeps it; buyers can switch it off. On a sold kit it is a demonstrable feature, not a UX tax | Label it as a Pro/demo feature; document the Free fallback |
| FA parallel set (1 FA page + 5 FA blocks + FA header/footer = 8 documents) | **SURVIVES** | B2 = equal parity | The brief's parity target demands FA equivalents for the remaining pages in later phases; today's 8 documents are the start, not parity |
| Theme-builder parts (2 headers, 2 footers, 3 loop = 7) | **SURVIVES** | Required for any Pro-compatible kit; C4 keeps Pro in the loop | Pro-only assignment steps documented for buyers |
| Palette: charcoal + amber + coral | **VOID** | No human brand exists (B5 has no brand book; C3 = logo only), and the build contradicts the declared system: coral = 15 of 2 136 colour refs, amber-600 = 294 |
| Accent-budget finding ("≤ 1 amber area larger than a button per section") | **SURVIVES** | A measurable system rule, independent of taste; the finding that it is violated (amber at primary-token volume) is evidence | Keep as a P2 target with a detector; enforce only against the re-derived palette |
| Colour census (2 136 refs, per-token counts) and the P1 baseline metrics (eyebrow 93% / centred 82% / animated 7%) | **SURVIVES** | These are measurements, not taste; they remain true whatever the brief says | Nothing — re-measure after P2 |
| Fabricated metrics (8), placeholder prices, unlabelled testimonials in copy | **VOID (content)** | Unlabelled fabricated data in a product sold to third parties; B4 list still pending | Replace with real data + sources, or visible SAMPLE labels; P2's first fix |
| `docs/08-agent-legibility.md` | **CONDITIONAL-BY-S8** | The structure (llms.txt shape, structured-data map, policy posture) is sound and B1-agnostic; what is unsafe is the ENTITY DATA inside it - the demo company name, address, phone and email are drop-in ready and would publish a fabricated Organization into schema.org and llms.txt | **Neither file may be copied to a live site until the entity data is neutralised.** Keep the structure; neutralise the entity |
| `docs/p3/alt-text-sample.md` | **CONDITIONAL-BY-S8** | Same condition, sharper: the ten drafts describe Aurora-specific content on demo imagery, so the pattern is reusable but the text is not buyer-ready | Same rule: entity/content neutralisation before live-site use; gate 2 still approves the pattern |

**Verdict counts (16 rows):** VOID = 4 · RE-DERIVE = 1 · CONDITIONAL = 3 · SURVIVES = 8.

**Carry-forward rule.** P2 may cite only artifacts marked SURVIVES, or their P1-R replacements.
The 15 dial values and the palette are explicitly VOID and must not reappear in P2 specifications
without a new decision row in `docs/DECISIONS.md`.
