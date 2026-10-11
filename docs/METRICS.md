# Canonical metrics

The 39-vs-40 discrepancy happened because "document" was never defined before it was counted.
This file defines every counter **before** anyone counts it again.

**Rule:** `tools/verify.py --report` is the **only** producer of these numbers.
`tools/render_docs.py` injects them into `README.md`, `CHANGELOG.md`, `docs/01..07` and the PR
body. A hand-typed count anywhere in those files is a defect, and `verify.py --report` fails
`check_doc_numbers()` when a stated number disagrees with the generated one.

## 1. Counters

Counters are computed over the **working tree**, never over a zip. `templates/**` is walked
recursively, so nested directories (`templates/blocks`, `pages`, `headers`, `footers`, `loop`,
`popups`, `kit`) are all included. **A non-recursive glob is a bug** — it silently returns 0 and
a scanner that finds nothing in nothing must fail, not pass.

| counter | definition (exact) | shape of the answer |
| --- | --- | --- |
| `template_documents` | every `*.json` under `templates/**` whose top-level `type` is **not** `kit` | 39 |
| `kit_documents` | every `*.json` under `templates/**` whose top-level `type` **is** `kit` | 1 |
| `documents_total` | `template_documents + kit_documents` — the number quoted in prose as "N Elementor documents" | 40 |
| `containers` | recursive count of `elType == "container"` over `template_documents` | 962 |
| `widgets` | recursive count of `elType == "widget"` over `template_documents` | 1280 |
| `widget_mix` | the same walk, grouped by `widgetType`, sorted by `(-count, name)` for stable output | table |
| `global_colours` | Kit document colour tab: `system_colors + custom_colors`; always quoted as "N (4 system + M custom)" | 19 (4 + 15) |
| `typography_styles` | Kit document typography tab: `system_typography + custom_typography` — named **presets**, not fonts | 15 (4 + 11) |
| `font_families` | distinct `typography_font_family` values across all Kit typography entries | 3 (Sora, Inter, Arad) |
| `global_fonts` | deprecated alias of `typography_styles`. It was previously read as "fonts" and conflated the two axes; only `font_families` may be described as fonts | — |
| `image_widgets` | `widget_mix["image"]` | 24 |
| `images` | distinct image URLs referenced by any setting value under `templates/**` | 7 |
| `custom_html_widgets` | `widget_mix.get("html", 0)` — must be 0 (constitution) | 0 |
| `pages` / `blocks` / `headers` / `footers` / `loop_templates` / `popups` | file counts per `templates/<dir>` | 9 / 22 / 2 / 2 / 3 / 1 |
| `theme_builder_layouts` | `headers + footers + loop_templates` (Theme Builder documents: header, footer, single, archive, search) | 7 |
| `fa_documents` | templates whose basename starts with `fa-` or ends with `-fa.json` | 8 |
| `blocks_fa` | blocks whose basename starts with `fa-` | 5 |

**Not documents** (they are export artifacts, not Elementor documents): `dist/site-settings.json`,
`dist/manifest.json`, `preview/*.html`, `media/*`.

## 2. The two numbers that were conflated

`global_colours` and `typography_styles` count *Kit tab entries*. `font_families` counts
*typefaces*. The PR body said "19 / 15" under the heading "Global colours / fonts", which
silently equates 15 typography presets with 15 fonts; an earlier revision said "18 / 18" — both
are wrong under these definitions. Correct phrasing:

> <!--f:global_colours-->19<!--/f--> (4 system + 15 custom) · <!--f:typography_styles-->15<!--/f--> (4 system + 11 custom) ·
> <!--f:font_families-->3<!--/f--> (Sora, Inter, Arad)

## 3. Non-empty assertion (applies to **every** scanner in the repo)

Before reporting "0 findings", a scanner MUST print the number of inputs it examined, and MUST
exit non-zero when that number is 0 or below its floor. "Found nothing" is only a valid result
if there was something to look at.

| scanner | input counter printed | floor | on floor breach |
| --- | --- | ---: | --- |
| `tools/bidi_check.py` | JSON documents scanned | 30 | exit 1 |
| `tools/check_assets.py` | distinct image URLs tested | 5 | exit 1 |
| `tools/verify.py` (media rule) | image URLs checked | 3 | exit 1 |
| `tools/banlist_check.py` | documents / sections / elements | 30 / 50 / 500 | exit 1 |
| `skills/elementor-native-kit/scripts/extract_controls.py` | php files per group (widgets, elements, groups, kit tabs) | 10 / 1 / 8 / 5 | exit 1 |
| `skills/elementor-native-kit/scripts/audit_control_names.py` | template documents + settings keys examined | 30 / 500 | exit 1 |
| `tools/render_docs.py` | fact keys injected | 10 | exit 1 |

Every counter is printed on the happy path too, so the numbers in CI logs and in the docs are
the same numbers.

## 4. Generated values

| counter | value | produced by |
| --- | ---: | --- |
| `documents_total` | 40 | `python3 tools/verify.py --report` |
| `template_documents` | 39 | `python3 tools/verify.py --report` |
| `kit_documents` | 1 | `python3 tools/verify.py --report` |
| `pages` | 9 | `python3 tools/verify.py --report` |
| `blocks` | 22 | `python3 tools/verify.py --report` |
| `headers` | 2 | `python3 tools/verify.py --report` |
| `footers` | 2 | `python3 tools/verify.py --report` |
| `loop_templates` | 3 | `python3 tools/verify.py --report` |
| `popups` | 1 | `python3 tools/verify.py --report` |
| `theme_builder_layouts` | 7 | `python3 tools/verify.py --report` |
| `fa_documents` | 8 | `python3 tools/verify.py --report` |
| `containers` | 962 | `python3 tools/verify.py --report` |
| `widgets` | 1 280 | `python3 tools/verify.py --report` |
| `global_colours` | 19 | `python3 tools/verify.py --report` |
| `typography_styles` | 15 | `python3 tools/verify.py --report` |
| `font_families` | 3 | `python3 tools/verify.py --report` |
| `image_widgets` | 24 | `python3 tools/verify.py --report` |
| `images` | 7 | `python3 tools/verify.py --report` |
| `custom_html_widgets` | 0 | `python3 tools/verify.py --report` |
_(this block is written by `python3 tools/verify.py --report && python3 tools/render_docs.py`;
do not hand-edit — a hand-typed number here is a defect)_

## 5. Phase-scoped counters (P-BRIEF, 2026-10-12)

These counters describe the **interview and the phase's own artifacts**, not the kit. They are
deliberately **outside** the `verify.py` fact set and must never be injected into the 11 generated
files. Each value is counted from the artifact named in the last column, with the reproducing
command where one exists.

| counter | definition (exact) | value | counted from |
| --- | --- | --- | --- |
| `brief_questions_asked` | questions put to the human across all batches (batch 1 B1–B5, batch 2 C1–C5, batch 3 the five completion questions) | 15 | `HANDOFF-PBRIEF.md` transcript |
| `brief_questions_answered` | questions with a recorded human selection | 10 | ANSWERED rows in `docs/BRIEF.md` |
| `brief_questions_skipped` | questions skipped by the human ("keep going") | 5 | P-BRIEF-019 |
| `brief_assumptions` | ASSUMPTION rows carrying a risk rating and a reversal trigger | 11 | `grep -cE '^\| A[0-9]+ \|' docs/BRIEF.md` |
| `decision_rows_total` | rows in the decision ledger, both prefixes | 33 | `grep -cE '^\| (D-[0-9]+|P-BRIEF-[0-9]+) \|' docs/DECISIONS.md` |
| `p1_disposition_rows` | artifacts dispositioned, by verdict | 16 (VOID 4 · RE-DERIVE 1 · CONDITIONAL 3 · SURVIVES 8) | `docs/P1-DISPOSITION.md` |
| `notion_ledger_rows_written` | decision rows written to the Notion ledger page | 21 (P-BRIEF-000…020) | Notion page `3f68dd8c-323d-8119-8787-fe3ad7064d66`; three early appends failed on a parameter-shape error, then all rows were written — see `HANDOFF-PBRIEF.md` |
| `calendar_gate_events` | human-gate slots created | 5 | Google Calendar event ids in `HANDOFF-PBRIEF.md` |
| `gmail_messages_sent` | messages sent for this phase (batch 1 only, per the phase directive) | 1 | Gmail id `1a12bdee5a2ea836` |
