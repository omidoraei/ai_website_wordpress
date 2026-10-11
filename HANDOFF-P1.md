# HANDOFF — P1 (design DNA + taste calibration)

Phase scope: extract the design DNA, calibrate taste numerically, and **diagnose** the current
kit against it. **No template, token, palette or type value was changed in P1.** Every claim
below has a command behind it.

Status: **artifacts complete — waiting on human gate 1.** P2 (tokens/copy structure) must not
start until that gate passes.

## 1. Deliverables

| File | What it is |
| --- | --- |
| `docs/p1/dna.yaml` | 4 admired (Anthropic, Linear, Stripe, Vercel) + 2 anti-references on the six mandated axes; tone pick = **technical-warm** |
| `dials.toml` | `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `UI_DENSITY` 1-10 + rationale for all 15 page types, plus `[invariants]` |
| `BANLIST.md` | 100+ banned patterns in bands A-E with a deterministic detector rule per ban |
| `docs/p1/type-decision.md` | Sora display / Inter body-only; Arad licence status; Vazirmatn fallback + 4-step swap path; numeral policy; H1-H6 ladder |
| `docs/p1/delta-table.md` | Axis \| current kit \| DNA target \| evidence \| severity \| fix-phase — the P2 worklist |
| `tools/banlist_check.py` | The detectors (new): `--json`, `--report-only` |
| `tools/verify.py` | Now runs the ban list as part of the gate: `--strict-banlist` fails on FAIL-level rules |
| `.github/workflows/kit.yml` | New step: BANLIST report-only + job-summary block (P1 diagnosis; flips to fatal at P2) |

## 2. Evidence (re-run these; do not trust prose)

```bash
python3 tools/verify.py --report      # exit 0  -> 39 documents, 962 containers, 1280 widgets,
                                      #           19 colours, 15 typography, 13 doc-number claims
                                      #           banlist: eyebrow 93% | centred 82% | animated 7%
python3 tools/verify.py --strict-banlist   # exit 1 -> B01-em-dash x12, B03-fake-metric x8
                                           # (correct for P1: those ARE the P2 worklist)
python3 tools/bidi_check.py           # exit 0  -> 42+ files, 0 findings
python3 tools/banlist_check.py --report-only
```

Measurement base: 39 template documents, 95 sections, 2 242 elements, 1 280 widgets, 135
dividers, 310 elements carrying `fadeInUp`, 2 136 global colour-token references.

## 3. Headline diagnosis (full detail in `docs/p1/delta-table.md`)

- **7 BANLIST rules tripped by working detectors: 2 FAIL-level, 5 WARN-level** (`B01` x12,
  `B03` x8 / `B03b` x10, `B06` x6, `B07` x16, `B08` x204, `B08-eyebrow-everywhere` x1),
  plus 4 rules tripped-or-unproven with a declared detector gap (§5).
- **S1 (ship-blocker, credibility):** 8 fabricated metrics, 10 unlabelled placeholder prices,
  and named testimonials/logos presented as real.
- **S2 (AI tell):** 82 % of sections centred, 93 % carrying an eyebrow, 12 em-dashes, 6
  version/status eyebrows, a 6-card equal-width icon grid that is explicitly on the ban list,
  and the accent colour used at primary-token volume (294 refs).
- **Already correct:** warm paper ground with **0 pure-white surfaces**, **0** purple/indigo/lila
  structure, **0** neon glow, motion confined to one direction (`fadeInUp`), **7 %** of elements
  animated, Inter used for body but **not** as a display face, H1/H2 ratio 1.39, Persian tracking
  ≥ 0.
- The motion style is a single family with a 90-110 ms stagger already present; `animation_duration`
  is unset everywhere, so duration is Elementor's default to this day — recorded as an S3 gap.

## 4. Open questions for the reviewer (gate 1)

1. **Dial naming.** The spec says `UI_DENSITY`; the source taste skill (v2 §1.C) says
   `VISUAL_DENSITY` and forbids inventing aliases. Resolution taken: keep the spec name, record
   the alias in the `dials.toml` header, never blend the two. Confirm or overrule.
2. **Arad licence is UNVERIFIED.** It is therefore *not* bundled and not advertised;
   Vazirmatn (OFL-1.1, confirmed via `gh api repos/rastikerdar/vazirmatn`) is the audited
   fallback with a documented 4-step swap. Do you have the Arad licence file?
3. **`dials.toml` values are a proposal.** The tolerant reading of `MOTION_INTENSITY ≤ 4` is
   enforced in `[invariants]` (animated ≤ 25 %; today 7 %). If you want a stricter number, say
   so before P2 pins motion.
4. **Placeholder policy.** Are demo metrics/prices/logos to be *removed*, or kept but
   *explicitly labelled as sample data*? The ban list permits the second; only you know which
   the shop wants.
5. **Scope of P2.** The delta table ranks 10 fixes; confirm the first three before P2 runs.

## 5. Detector debt — declared, not hidden

`BANLIST.md` carries four written "the detector is not yet what the ban claims" notes:

| Rule | State |
| --- | --- |
| B13 decorative dividers | 135 dividers counted, not yet split structural vs ornamental |
| B18 card-in-card | not implemented |
| B30 testimonial/logo endorsement | not implemented |
| B06b icon-tile feature grid | **reads 0 although the banned 6-card grid exists** — treat as tripped until fixed |

This is deliberate: a heuristic that reports a false 0 would make the ban list worthless.

## 6. Next 3 actions

1. Human gate 1: review `docs/p1/dna.yaml`, `dials.toml`, `BANLIST.md`, `type-decision.md`,
   `delta-table.md`; answer §4.
2. P2 (after gate): clear the two S1 items (fabricated metrics, placeholder prices/endorsements),
   then S2 items 2-8 in ranked order; implement B13/B18/B30 detectors in the same phase.
3. Flip the CI BANLIST step from `--report-only` to fatal (and `verify.py --strict-banlist`)
   only once P2 empties the FAIL list.

## 7. Residue carried over from P0 (untouched this phase)

- `scripts/audit_control_names.py` false positives (`container.padding`, `heading.typography_typography`,
  `icon.size`) — CI step stays advisory.
- Pro control-name policy not finalised.
- `spacer.space` / `_element_width` unproven against extractor output.
- Generated doc numbers depend on `verify.py --report`; any hand-written count remains a defect.

## 8. Decisions reversed this phase

None. One convention clarified: the FA dial set differs from EN (`home.fa` 7/3/4 vs `home.en` 8/4/4)
justified on Persian line-height and RTL flow, **not** as "same but mirrored".

## 9. Files touched (uncommitted before this handoff; committed with it)

```
new : tools/banlist_check.py, docs/p1/dna.yaml, dials.toml, BANLIST.md,
      docs/p1/type-decision.md, docs/p1/delta-table.md, HANDOFF-P1.md
edit: tools/verify.py, .github/workflows/kit.yml
none: templates/**, dist/**, media/**, tools/aurora/**
```
