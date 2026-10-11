# HANDOFF — P0 (memory bootstrap)

Date: 2026-10-11 · Branch: `arena/1e298a1b-ai-website-wordpress` · Phase cap: 25 turns
**Cap status: OVERRUN (~35 turns).** Cause and cost are recorded below rather than hidden.

## State — what exists and is proven

| Deliverable | Path | Status |
| --- | --- | --- |
| Skill | `skills/elementor-native-kit/SKILL.md` | ✅ written |
| References (8 concerns + generated index) | `skills/elementor-native-kit/references/` | ✅ all 8 written |
| Machine-generated control index | `references/_generated/control-index.md` | ✅ 39 source files, 575 controls, 12 groups / 76 fields, 13 kit tabs |
| Free/Pro taxonomy | `references/_generated/widget-taxonomy.md` | ✅ derived from source presence |
| Agent entry point | `AGENTS.md` | ✅ written |
| Capability contract | `docs/capability-matrix.md` | ✅ written |
| Bidi scanner | `tools/bidi_check.py` | ✅ 42 files scanned, 0 FAIL / 0 WARN |
| CI gate | `.github/workflows/kit.yml` | ✅ written |
| Generated numbers | `docs/_generated/facts.md` + `facts.json` | ✅ produced by `verify.py --report` |

Evidence (all run on this branch):

```
python3 tools/build.py            -> validation: OK, 40 documents written
python3 tools/verify.py --report  -> RESULT: clean; 13 doc number claims checked
python3 tools/bidi_check.py       -> FAIL 0, WARN 0, exit 0
```

Provenance: `elementor/elementor` at **v3.35.9** and **v4.0.8**, fetched from codeload,
extracted under `/home/user/.src/` (outside the repo, deliberately not committed).

## Decisions reversed by evidence (do not re-litigate)

1. **Container responsive visibility is REAL — an earlier "defect" claim was WRONG.**
   A naive `grep` for `hide_mobile` finds nothing, but the ids are built dynamically:
   `includes/base/element-base.php:L1383 add_hidden_device_controls()` →
   `'hide_' . $breakpoint_key`, `return_value: 'hidden-' . $breakpoint_key`,
   `prefix_class: 'elementor-'`; called from `container.php:L1906` inside the
   "Responsive → Visibility" section. The kit's 6 uses are **valid**. Do not "fix" them.
2. **There is no 3.x/4.x dual-write for button backgrounds.** `button-trait.php` is
   byte-identical between the two tags; `background` group → `background_background`
   (switcher) + `background_color` (value), `button_background_hover` → `…_background` +
   `…_color`. The earlier note claiming a version split is retracted in
   `references/04-version-deltas.md`. **The PR #1 body still contains that retracted claim —
   fix it before merge.**
3. **`includes/controls/groups/`, `includes/elements/`, `includes/base/` are identical
   across the two tags.** Only `social-icons.php` (a default string) and two kit tab files
   (a `do_action`) differ. The kit's control surface does not drift.

## Open questions (need a decision, not more digging)

1. **Pro widget control names.** `05-pro-vs-free.md` documents the tiers, but the templates
   contain structural keys for Pro widgets (`form_*`, `posts_*`, `archive-posts` `cards_*`,
   `nav-menu`, `breadcrumbs`, `theme-*`) that **could not be verified** because Elementor Pro
   is closed source. Options: (a) verify against a real Pro install and record
   `elementor-pro@<version>` as provenance; (b) strip every Pro style key and leave Pro
   widgets at their defaults; (c) keep them and label them unverified in the matrix.
   Recommendation: (a) if a Pro licence is available, otherwise (b) — the templates stay
   useful and the honesty surface stays clean.
2. **`spacer.space`.** `spacer.php` indexed 0 controls, so the key the kit emits on 2 Spacer
   widgets is unproven by this pipeline. Likely an extractor limitation (the control may be
   registered through a path the regex misses). Either fix the extractor or drop the Spacer
   widgets for `divider` + padding.
3. **`_element_width` on containers** (167 uses). Confirmed as a **widget** control
   (`common-base.php:L335`); container behaviour not proven. Affects the header button group.

## Residue — explicitly NOT done

| Item | Why it matters | Next action |
| --- | --- | --- |
| `scripts/audit_control_names.py` has a high false-positive rate | Flags `container.padding`, `heading.typography_typography`, `icon.size` as unknown although they are real | Finish the pool: resolve base controls from `common-base.php` + `container.php` via the index instead of the ad-hoc `group_uses()` regex; add repeater-item fields and per-state prefixes. It is `continue-on-error: true` in CI until then |
| Doc-number coverage is 7 patterns / 13 claims | Rule B is only partially enforced | Expand `DOC_NUMBERS` in `verify.py`; add marker-block replacement so docs are *generated* rather than checked |
| `docs/02`, `docs/03` still describe counts by hand | Same | Replace with `<!-- facts:start -->` blocks written by `--report` |
| Preview suite is a page-count smoke test | P6 visual suite is not implemented | Add per-breakpoint screenshots + diffing |
| `references/02` and `01` carry UNVERIFIED rows for `spacer` and `_element_width` | A reader could mistake them for facts | Close questions 2 and 3 above |
| `PINNED_TAG` file referenced nowhere | Tag is in `kit.yml` env only | Either add `skills/elementor-native-kit/PINNED_TAG` or drop the reference |

## Files touched this phase

```
AGENTS.md
docs/capability-matrix.md
docs/_generated/facts.md, facts.json
skills/elementor-native-kit/SKILL.md
skills/elementor-native-kit/references/{01-container-controls,02-widget-controls,
  03-kit-site-settings,04-version-deltas,05-pro-vs-free,06-rtl-persian,
  07-motion-effects,08-import-mechanics}.md
skills/elementor-native-kit/references/_generated/{control-index.md,widget-taxonomy.md,summary.json}
skills/elementor-native-kit/scripts/{extract_controls,audit_control_names}.py
tools/bidi_check.py, tools/check_assets.py, tools/verify.py (facts + doc-number gate)
.github/workflows/kit.yml
HANDOFF-P0.md
```

No file under `templates/` was modified in this phase (phase constraint honoured).

## Next 3 actions (in order)

1. **Close the audit false positives** (`scripts/audit_control_names.py`), then flip its CI
   step from `continue-on-error: true` to a hard gate. Expect the unknown-key list to shrink
   to the Pro keys only — that reduced list *is* the answer to open question 1.
2. **Decide Pro-key policy** (question 1) and either verify against a Pro install or strip the
   keys; update `docs/capability-matrix.md` rows accordingly.
3. **Make docs numbers generated, not checked** (marker blocks + `--report`), then extend
   `DOC_NUMBERS` to CHANGELOG and every `docs/*.md` table.

## Why the cap was exceeded (honest accounting)

Two mis-steps, both in service of the constitution rather than against it:

1. The control-name audit was not a listed deliverable, but rule "never invent control
   names" made it the only way to *prove* the templates comply. Building it cost ~6 turns and
   it is still not finished (residue above). A cheaper path existed: extract first, audit
   later, and write the 8 references before touching the audit.
2. The "container visibility is a defect" conclusion cost 2 extra turns to disprove. The
   lesson is recorded as rule: **dynamic control ids break naive greps — confirm via the
   registering function, not the string.**
