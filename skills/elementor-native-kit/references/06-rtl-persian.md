# 06 — RTL & Persian (FA)

Rule 9: RTL is a **system**, not a flag. The FA documents are re-laid-out for Persian
reading order and Persian metrics — not a mirrored copy of the English ones.

Kit-specific ground truth: `tools/aurora/tokens.py` defines the FA typography styles and
`tools/aurora/theme_parts.py` / `sections.py` contain the parallel FA blocks
(`FA_BLOCKS`). The FA set is: home, header, footer + 5 section blocks.

---

## 1. What Elementor mirrors for you (do nothing)

| Thing | Behaviour |
| --- | --- |
| `flex_direction: row` | flipped automatically when the document/page is RTL (`--flex-direction` is logical; Elementor swaps the `e-con` direction) |
| Row alignment options (Start/End) | interpreted logically |
| Icon position on Button / Icon List | mirrored with the row |
| Editor panel | mirrored when the WordPress locale is RTL |

So: **do not** rewrite `row` to `row-reverse` for FA documents. Doing so double-flips and
produces a right-to-left layout rendered left-to-right. This is the single most common FA
bug in an Elementor kit.

## 2. What you MUST change for FA (re-layout, not mirror)

| Concern | EN | FA | Where |
| --- | --- | --- | --- |
| Font family | Sora / Inter | **Arad** (`FA / *` global styles) | `tokens.py` FA styles |
| Heading line-height | 1.12–1.3 em | **1.5–1.55 em** | Persian ascenders/dots need the room; the Latin value clips glyphs |
| Body line-height | 1.75 em | **2.0 em** | readability |
| Letter-spacing | −1.6 px on display | **0** | negative tracking breaks Persian joins |
| Text transform | uppercase eyebrows | **none** | Persian has no case |
| Display size | 64 px | **54 px** | Persian renders visually larger per point |
| Reading order | zigzag media/copy as authored | re-ordered (stats band moved above the zigzag) | FA page composition |
| Numerals | 1, 2, 3 | ۰۱، ۰۲، ۰۳ in **display copy only** | never in form fields, counters or prices — WordPress, Elementor counters and WooCommerce are Latin-digit |

## 3. Logical properties only

| Use | Never | Why |
| --- | --- | --- |
| `margin-inline-start/end` (via Elementor padding/margin groups when available) | `margin-left/right` | logical props survive RTL |
| `text-align: start/end` | `left/right` in generated CSS | Elementor's own controls already emit logical values |
| Container `flex_direction: row` | `row-reverse` | see §1 |

The kit writes no raw CSS at all (rule 2), so "logical properties only" reduces to: **never
set a physical direction or alignment where Elementor offers a logical one**, and never
reverse a row to fake RTL.

## 4. Mirroring allow / deny list

**Mirror (let Elementor flip it):**

- Text blocks, button icon position, icon-list bullets, breadcrumb order, form field order.

**Do NOT mirror (verify by eye after any change):**

- Logos and wordmarks (`theme-site-logo`) — `example` must not read `elpmaxe`.
- Any Image widget containing Latin text or a chart with a "left/right" meaning.
- Numeric sequences in stats and prices (a mirrored `380M` reads as `M380`).
- Case-study screenshots.
- Decorative arrows used as *progress* indicators (`→` in a numbered process) must not point
  backwards in RTL; use a non-directional marker (numbers, dots) instead.

## 5. Bidi / Unicode safety (rule J)

Persian and Arabic strings must never be approved from a rendered diff — a rendered diff
reorders characters and hides damage. Approve at JSON level:

```bash
python3 tools/bidi_check.py            # human report
python3 tools/bidi_check.py --json     # CI
```

| Codepoint range | Name | Allowed in copy | Allowed in id/control-name/URL |
| --- | --- | --- | --- |
| U+202A–U+202E | LRE, RLE, PDF, LRO, RLO | intentional + annotated | **FAIL** |
| U+2066–U+2069 | LRI, RLI, FSI, PDI | intentional + annotated | **FAIL** |
| U+200E, U+200F | LRM, RLM | intentional + annotated | **FAIL** |
| U+061C | ALM | intentional + annotated | **FAIL** |

"Annotated" means a comment or a documented reason in the commit; otherwise it is a WARN.
Any RTL embedding/isolate/override character inside a control name, element id, CSS class or
URL is a **build failure**, because it corrupts the JSON contract rather than the prose.

### Known-safe practice for mixed runs

* A Latin product name inside a Persian sentence is handled by the bidi algorithm — no
  control characters needed. If a break looks wrong, insert a single LRM (`&lrm;`) through
  the Text Editor **Text** tab, where it is visible and removable.
* Persian digits in HTML are literal characters (۰-۹); no override is required.
* Never paste from a Persian PDF source that carries hidden U+202B/U+202C around every
  paragraph — run `bidi_check.py` after any paste-from-document operation.

## 6. Arad metrics

| Global style | Family | Weight | Desktop | Mobile | Line height | Tracking |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| FA / Headings | Arad | 700 | 40 px | 26 px | 1.5 em | 0 |
| FA / Hero Display | Arad | 700 | 54 px | 30 px | 1.55 em | 0 |
| FA / Body | Arad | 400 | 17 px | 16 px | 2.0 em | 0 |
| FA / Eyebrow & Nav | Arad | 600 | 15 px | — | 1.7 em | 0 |

Arad is a licensed commercial typeface and is **not bundled**. Installation and the
substitution procedure are in the kit's `docs/04-rtl-persian-setup.md`. If the family does
not resolve, Persian text falls back to the theme font with the same comfortable metrics —
the layout does not break.

## UNVERIFIED — do not emit

* Any claim about a specific Persian host or WordPress locale's mirroring behaviour beyond
  the two facts above (locale drives `is_rtl()`, Elementor emits logical flex direction).
* Arad's exact metrics (x-height, descender depth) beyond the four global style definitions:
  the font file itself is not available in this environment, so the values above are the
  kit's chosen settings, not measured font metrics. If you install a different Arad cut,
  re-check the display sizes by eye.
