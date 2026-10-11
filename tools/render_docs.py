#!/usr/bin/env python3
"""
Inject the generated facts (tools/verify.py --report) into the documents, so no number in
README/CHANGELOG/docs is hand-typed (constitution rule B, docs/METRICS.md §1).

    python3 tools/verify.py --report      # produces docs/_generated/facts.json  (the only producer)
    python3 tools/render_docs.py          # writes the numbers into every marked slot
    python3 tools/render_docs.py --check  # fail if any slot is stale (CI uses this)
    python3 tools/render_docs.py --pr-body > docs/_generated/pr-body.md

A slot is an HTML comment pair, so it survives markdown rendering:

    | Elementor documents | <!--f:documents_total-->40<!--/f--> |

verify.py additionally fails if a metric phrase appears in a target file OUTSIDE a slot —
that is what a hand-typed number looks like.

Exit codes: 0 = injected (or --check clean), 1 = stale slot, missing fact, too few facts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "docs", "_generated", "facts.json")

TARGETS = (
    "README.md", "CHANGELOG.md",
    "docs/01-installation.md", "docs/02-design-system.md", "docs/03-template-library.md",
    "docs/04-rtl-persian-setup.md", "docs/05-theme-builder.md",
    "docs/06-performance-accessibility.md", "docs/07-faq-troubleshooting.md",
    "docs/METRICS.md", "docs/capability-matrix.md",
)

SLOT = re.compile(r"<!--f:([a-z_]+)-->(.*?)<!--/f-->", re.S)

# A run must inject at least this many slots, or the renderer is not looking at the docs
# (non-empty assertion, METRICS.md §3).
MIN_SLOTS = 10

# Blocks injected wholesale: a marker line on its own, replaced by a generated table.
BLOCK = re.compile(r"^<!--block:([a-z_]+)-->$", re.M)


def fmt(value) -> str:
    if isinstance(value, int):
        return "{:,}".format(value).replace(",", "\u00a0")
    return str(value)


def render_table(key: str, facts: dict) -> str:
    if key == "widget_mix":
        rows = ["| widget | count |", "| --- | ---: |"]
        rows += ["| `%s` | %s |" % (k, fmt(v)) for k, v in facts["widget_mix"].items()]
        return "\n".join(rows)
    if key == "metrics":
        order = ("documents_total", "template_documents", "kit_documents", "pages", "blocks",
                 "headers", "footers", "loop_templates", "popups", "theme_builder_layouts",
                 "fa_documents", "containers", "widgets", "global_colours", "typography_styles",
                 "font_families", "image_widgets", "images", "custom_html_widgets",
                 # P1.7 occurrence-level units (docs/METRICS-RECONCILIATION.md)
                 "dead_anchor_occurrences", "dead_anchor_documents", "dead_anchor_documents_scanned",
                 "main_containers", "main_page_level_documents",
                 "h1_zero_documents_pages_loop", "h1_not_exactly_one_documents",
                 "lang_mix_documents", "lang_mix_strings", "lang_mix_runs", "lang_mix_chars",
                 "fa_documents_by_content", "alt_nonempty_count", "alt_distinct_count",
                 "alt_quality_findings")
        rows = ["| counter | value | produced by |", "| --- | ---: | --- |"]
        for k in order:
            if k in facts:
                rows.append("| `%s` | %s | `python3 tools/verify.py --report` |" % (k, fmt(facts[k])))
        return "\n".join(rows)
    raise KeyError(key)


def pr_body(facts: dict) -> str:
    f = facts
    return PR_TEMPLATE.format(
        documents=fmt(f["documents_total"]),
        templates=fmt(f["template_documents"]),
        kit=fmt(f["kit_documents"]),
        pages=fmt(f["pages"]), blocks=fmt(f["blocks"]),
        blocks_fa=fmt(f["blocks_fa"]), blocks_en=fmt(f["blocks"] - f["blocks_fa"]),
        theme_builder=fmt(f["theme_builder_layouts"]), popups=fmt(f["popups"]),
        containers=fmt(f["containers"]), widgets=fmt(f["widgets"]),
        colours=fmt(f["global_colours"]), typography=fmt(f["typography_styles"]),
        families=fmt(f["font_families"]), images=fmt(f["images"]),
        image_widgets=fmt(f["image_widgets"]), fa_documents=fmt(f["fa_documents"]),
        html=fmt(f["custom_html_widgets"]),
        lang_mix_documents=fmt(f["lang_mix_documents"]),
        lang_mix_strings=fmt(f["lang_mix_strings"]), lang_mix_runs=fmt(f["lang_mix_runs"]),
        dead_anchor_occurrences=fmt(f["dead_anchor_occurrences"]),
        dead_anchor_documents=fmt(f["dead_anchor_documents"]),
        dead_anchor_documents_scanned=fmt(f["dead_anchor_documents_scanned"]),
        alt_distinct_count=fmt(f["alt_distinct_count"]),
        alt_quality_findings=fmt(f["alt_quality_findings"]),
        alt_proper_noun_only_distinct=fmt(f["alt_proper_noun_only_distinct"]),
    )


PR_TEMPLATE = """## What this is

A complete **Elementor-native** website for an AI/SaaS product company, delivered as a
Template Kit. Nothing is a coded imitation of Elementor: every section is a real Elementor
document that opens in the editor and is editable by a non-developer.

## Numbers (generated by `tools/verify.py --report`, injected by `tools/render_docs.py`)

| | |
| --- | ---: |
| Elementor documents | **{documents}** ({templates} templates + {kit} Kit document) |
| Pages | {pages} (8 EN + 1 FA/RTL) |
| Reusable section blocks | {blocks} ({blocks_en} EN + {blocks_fa} FA) |
| Theme Builder layouts | {theme_builder} (header EN/FA, footer EN/FA, single, archive, search) |
| Popup | {popups} (exit intent) |
| Flexbox Containers | {containers} |
| Widgets | {widgets} |
| Global colours | {colours} (4 system + 15 custom) |
| Typography styles | {typography} (4 system + 11 custom) |
| Font families | {families} (Sora, Inter; Arad still in the template bytes pending the P2 Vazirmatn swap) |
| Images / image widgets | {images} URLs / {image_widgets} widgets |
| Custom HTML widgets | **{html}** |
| Custom CSS / JS | **0** |

Definitions for every counter are in `docs/METRICS.md`; the ledger of what this project has
claimed and retracted is `docs/CLAIMS.md`.

## How it satisfies the brief

- **Elementor native** — Flexbox Containers + free and Pro widget types. No legacy
  Section/Column anywhere. Container landmarks are partly in place: 95 of 962 containers carry
  an `html_tag` (`section` 90, `header` 2, `footer` 2, `main` 1); the gap list — 11 page-level
  documents without `main`, 7 without `h1` — is in `docs/p3/landmark-audit.md`.
- **No hard coding** — enforced by `tools/verify.py`, which fails the build if a Custom HTML
  widget appears or if any `globals/colors?id=` / `globals/typography?id=` reference does not
  resolve to a global the kit defines. Text is in Heading/Text Editor widgets, CTAs in Button
  widgets, media in Image widgets, cards in containers.
- **Design system** — 4 system + 15 custom global colours, 4 system + 11 custom typography
  styles across {families} families, a 4-px spacing scale, radius and elevation scales, and
  button/form/heading/body styles set in the Kit document.
- **Responsive** — every grid stores its own tablet and mobile `flex-basis`; headings, padding,
  gaps, alignment and column direction carry per-breakpoint values.
- **Persian / RTL** — {fa_documents} Farsi documents by naming convention, in a parallel set;
  {lang_mix_documents} further documents embed Persian copy ({lang_mix_strings} leaf strings,
  {lang_mix_runs} script runs - a P8 defect, `docs/p1.7/lang-mix-audit.md`). The FA type system
  is decided to Vazirmatn (SIL OFL-1.1, decision B5), but the template bytes still carry Arad,
  whose licence is **UNVERIFIED**; the swap lands in P2 (`docs/p1/type-decision.md`).
- **Animations** — Elementor Motion Effects only (`fadeInUp`, staggered delays). No external
  animation library.
- **Performance** — no carousels, sliders or third-party libraries; {images} image files across
  {image_widgets} image widgets, and all {image_widgets} carry a non-empty `settings.image.alt`;
  {alt_distinct_count} distinct strings; descriptive quality audit tracked in
  `docs/a11y-alt-policy.md` (`tools/alt_quality_check.py` measures {alt_quality_findings} flagged
  instances, {alt_proper_noun_only_distinct} distinct, all client-name-only). FAQ answer
  blocks ship in the templates with the widget-level FAQ schema switched on; site-wide structured
  data is SEO-plugin configuration, and no Review markup is emitted because the testimonials are
  fictional (`docs/08-agent-legibility.md` §2).

- **Link honesty** — the CTA audit found `#contact` resolving on 1 of the 16 documents that use
  it, `#docs` on 0 of 12, two of the three header buttons pointing nowhere, and
  {dead_anchor_occurrences} dead in-page targets across {dead_anchor_documents} of
  {dead_anchor_documents_scanned} template documents (`docs/METRICS-RECONCILIATION.md` defines the
  unit). Clearing those links
  is the first P2 item after data labelling.

## Deliverables

- `templates/**/*.json` — one Elementor document per file, plus `templates/INDEX.md`
- `dist/aurora-ai-templates.zip` — **Templates → Saved Templates → Import Templates**
- `dist/aurora-ai-kit.zip` — **Elementor → Tools → Import/Export Kit** (applies the design system)
- `dist/site-settings.json` + `manifest.json`
- `media/*.jpg` — demo imagery served from the `kit-assets-v1` tag so Elementor can download it
  into the Media Library on import. The tag is a **movable ref**: CI pins its target commit, and the
  buyer-facing migration to commit-SHA URLs is prepared and tracked in `HANDOFF-P1.7.md` (item 4)
- `preview/*.html` — static rendering of the design for review
- `tools/` — token-driven generator, independent verifier, doc renderer, image pipeline
- `vendor/elementor/` — the Elementor source subset the control index is generated from,
  checksum-verified in CI (hermetic gate)
- `docs/` — the guides, plus `METRICS.md`, `CLAIMS.md` and the P1 design DNA

## Verification

```
$ python3 tools/build.py             # validation: OK
$ python3 tools/verify.py --report   # RESULT: clean, and writes docs/_generated/facts.md and facts.json
$ python3 tools/render_docs.py --check && python3 tools/bidi_check.py && python3 tools/banlist_check.py
$ sha256sum dist/*.zip               # byte-determinism: identical after a rebuild
```

Note on digests: the numbers GitHub reports for the *uploaded artifact* are not a
determinism proof - they differ between runs of the same commit (observed:
`4cc70c6f...`, `37b371f1...`, `7ea008fb...`). The stable, checkable number is
`sha256sum dist/*.zip`, which does not move across rebuilds. Full comparison:
`HANDOFF-P0.5.md`.

Control names are verified against the Elementor source rather than guessed:
`includes/elements/container.php`, `includes/widgets/*.php`,
`includes/controls/groups/{{flex-container,flex-item,typography,background}}.php`,
`includes/base/element-base.php` (responsive visibility) and `core/kits/documents/tabs/*.php`
(every Kit key). The source subset is vendored in `vendor/elementor/` with sha256 recorded in
`skills/elementor-native-kit/SKILL.md`, so the gate does not depend on the network.

## Reviewer notes

- Import order matters: templates first (Saved Templates), then the kit archive for the design
  system, then assign the Theme Builder documents. See `docs/01-installation.md`.
- The kit archive intentionally declares empty `templates` and `content` in its manifest:
  Elementor's Templates/Content import runner expects WordPress post exports, so the documents
  ship in `templates-source/` instead.
- CI carries one advisory failure-level annotation from the `continue-on-error` control-name
  audit; it does not fail the gate and is recorded in `docs/CLAIMS.md` row C-004.
"""


def apply_slots(path: str, facts: dict, check: bool) -> tuple[int, list]:
    text = open(path, encoding="utf-8").read()
    stale, injected = [], 0

    def sub(match: re.Match) -> str:
        nonlocal injected
        key = match.group(1)
        if key not in facts:
            raise KeyError("unknown fact key %r in %s" % (key, path))
        want = fmt(facts[key])
        have = match.group(2)
        if have != want:
            stale.append("%s: %s is %r, facts say %r" % (path, key, have, want))
        injected += 1
        return "<!--f:%s-->%s<!--/f-->" % (key, want)

    def block(match: re.Match) -> str:
        nonlocal injected
        key = match.group(1)
        injected += 1
        return render_table(key, facts)

    new = BLOCK.sub(block, text)
    new = SLOT.sub(sub, new)
    if new != text and not check:
        open(path, "w", encoding="utf-8").write(new)
    return injected, stale


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if a slot is stale")
    ap.add_argument("--pr-body", action="store_true", help="print the corrected PR body")
    args = ap.parse_args()

    if not os.path.exists(FACTS):
        print("missing %s - run tools/verify.py --report first" % os.path.relpath(FACTS, ROOT))
        return 1
    facts = json.load(open(FACTS, encoding="utf-8"))

    if args.pr_body:
        sys.stdout.write(pr_body(facts))
        return 0

    total, stale = 0, []
    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        n, s = apply_slots(rel, facts, args.check)
        total += n
        stale += s
    print("render_docs: %d slot(s) across %d file(s)" % (total, len(TARGETS)))
    if total < MIN_SLOTS:
        print("  ! only %d slots found, floor is %d - are the markers missing?"
              % (total, MIN_SLOTS))
        return 1
    if stale:
        print("  ! %d stale slot(s):" % len(stale))
        for row in stale:
            print("    - %s" % row)
        return 1
    print("  all slots agree with docs/_generated/facts.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
