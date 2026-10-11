---
name: elementor-native-kit
description: Build, modify, audit or extend the Aurora AI Elementor template kit — the 40 Elementor documents, the kit design system (global colors/fonts), the EN and FA/RTL template sets, the Theme Builder layouts, the reusable section blocks and the JSON generator in tools/aurora/. Use when a task touches templates/*.json, tools/aurora/*.py, tools/verify.py, the kit archives in dist/, Elementor control names, global color/typography references, responsive (per-breakpoint) values, Elementor Motion Effects, RTL/Persian layout, import/export mechanics, or when a control name, widget type or kit setting must be confirmed against the Elementor source before being emitted.
version: 0.1.0
provenance: "verified against Elementor includes/... on 2026-10-11"
elementor_source:
  v3_35_9: sha256:d4a235a93dd60bf9dbde78786aa95afe842de54c1e8375da1bdef71258b0a564
  v4_0_8: sha256:643a604f07e0f3c542fba95af39bd04400b9a2f8193bd54086b2d685fd4bce05
  archive: "vendor/elementor/elementor-<tag>-src.tar.gz - includes/** plus core/kits/documents/tabs/** only"
  regenerate: "cd <elementor checkout> && tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - includes core/kits/documents/tabs | gzip -n -9 > <archive>"
  verified: "CI verifies both sha256s before extraction; the gate never clones from the network"
---

# Elementor-native kit skill

Provenance: every control name in this skill was extracted from
`elementor/elementor` at tags **v3.35.9** and **v4.0.8** on **2026-10-11** by
`scripts/extract_controls.py`; the output lives in `references/_generated/`. The
source subsets are vendored in `vendor/elementor/` and checksum-verified in CI, so the
line numbers below cannot drift with the network.
Nothing here is recalled from memory. If a name is absent from the generated
index, it does not exist for this project.

## When to invoke

- Editing, generating or reviewing `templates/**/*.json`.
- Changing `tools/aurora/` (tokens, DSL, components, sections, pages, theme parts).
- Anything about global colors / global fonts / kit `site-settings`.
- Anything about responsive values, Motion Effects, RTL/Farsi layout or bidi.
- Before emitting a control name that is not already used in the repo.
- Auditing Free/Pro capability, import mechanics, or docs numbers.

## When NOT to invoke

- Writing prose that does not touch Elementor semantics.
- Front-end performance work outside Elementor's own settings.
- Anything requiring a plugin other than Elementor Free/Pro (the stack is fixed).

## The 12 non-negotiable rules

1. **Native only.** Flexbox Containers plus Elementor widgets. No legacy `section`/`column`.
2. **No HTML widget, no custom CSS, no custom JS, no external animation library.** Ever.
3. **No invented control names.** A control id must exist in
   `references/_generated/control-index.md`. `scripts/audit_control_names.py` enforces this.
4. **Tokens only.** Colors and fonts are referenced as `globals/colors?id=<id>` and
   `globals/typography?id=<id>`, and every referenced id must be defined by the kit document.
5. **Structure.** Element ids are unique 7-hex per document; every container states
   `isInner`; no `null` settings; widgets have no children.
6. **Landmarks and headings.** Containers carry `html_tag` (`section`/`main`/`header`/`footer`);
   exactly one `H1` per page; heading levels are literal, never a `div` styled as a heading.
7. **Per-breakpoint layout.** Every grid item carries its own `_flex_basis_tablet` /
   `_flex_basis_mobile`. Mobile is re-laid-out, never a scaled desktop.
8. **Motion Effects only.** Containers animate with `animation`, widgets with `_animation`
   (see `04-version-deltas.md`); stagger 80–110 ms; never animate layout-affecting properties.
9. **RTL is a system.** FA documents are re-laid-out, not mirrored. Logical properties only;
   Arad metrics live in separate global styles; no negative tracking on Persian text; a bidi
   scan is mandatory before any Persian string is approved.
10. **Free/Pro honesty.** A Pro-only control never enters a Free-compatible document without a
    documented fallback and a `docs/capability-matrix.md` row.
11. **Media.** Images are absolute URLs under `tokens.ASSET_BASE`, 3:2, with alt text; hero
    backgrounds are set through Elementor Background settings only, never as an `<img>`.
12. **Numbers are generated.** Every count in README/docs/CHANGELOG comes from
    `python3 tools/verify.py --report`. A hand-written count is a defect.

## Verifier: the gate

```bash
python3 tools/verify.py --report   # regenerate docs facts, then verify
python3 tools/verify.py            # verify only; exit 0 required before any commit
python3 tools/bidi_check.py        # bidi / Unicode safety (rule 9)
python3 skills/elementor-native-kit/scripts/audit_control_names.py
```

Failure classes and what they mean:

| Message contains | Meaning | Fix in |
| --- | --- | --- |
| `duplicate element id` | two elements share an id inside one document | `tools/aurora/dsl.py` id generation |
| `unknown widgetType` | a widget type no Elementor build in the pinned set defines | `dsl.py` helper |
| `references undefined colour/typography` | a global was emitted that the kit never defines | `tools/aurora/tokens.py` + `kit.py` |
| `is neither a dimensions nor a slider value` | a control got the wrong value shape | the component that emitted it |
| `contains N HTML widget(s)` | forbidden output (rule 2) | rewrite as containers + widgets |
| `is not a valid colour` / `not a valid dimensions value` | malformed value | `tokens.py` / component |
| `does not exist in media/` | an image URL points at a missing file | `tools/media.py`, then rebuild |
| `bidi control found in id/control-name/url` | forbidden codepoint outside copy | the generator that wrote the string |
| `UNEXPLAINED CONTROL KEY` | likely invented name or undocumented Pro control | `dsl.py`, or add a capability-matrix row |

## References (load on demand — never inline)

| File | Load when |
| --- | --- |
| `references/01-container-controls.md` | container flex/flex-item fields, responsive eligibility, grid |
| `references/02-widget-controls.md` | any widget's control ids, defaults, group-typography naming |
| `references/03-kit-site-settings.md` | global colors/fonts/layout/buttons/forms, kit document shape |
| `references/04-version-deltas.md` | 3.x vs 4.x divergence, `animation` vs `_animation`, dual-write rules |
| `references/05-pro-vs-free.md` | Free/Pro capability, fallbacks, what may not be emitted |
| `references/06-rtl-persian.md` | FA layout, Arad metrics, mirroring allow/deny lists, bidi hazards |
| `references/07-motion-effects.md` | the closed set of Motion Effects + stagger conventions |
| `references/08-import-mechanics.md` | Saved Templates vs Kit import, manifest expectations |
| `references/_generated/control-index.md` | **the source of truth for control names** (machine-written) |

Regenerate the generated layer when the pinned tag changes:

```bash
git clone --depth 1 --branch v3.35.9 https://github.com/elementor/elementor /tmp/elementor
python3 scripts/extract_controls.py --source /tmp/elementor --tag v3.35.9
```

## UNVERIFIED surface

Anything under an `UNVERIFIED — do not emit` heading in a reference file is a name or
behaviour this skill could not confirm against a public source (Elementor **Pro** is closed
source). Those names are never emitted into templates; the capability matrix records the
fallback instead. Do not promote an unverified name to a fact by copying it into a template.
