# 04 — RTL & Persian setup

The kit ships **two complete sets**: an English (LTR) set and a Persian (RTL) set. The
Persian set is not a translation layer on top of the English one — it is a standalone set
of documents with Persian copy, Persian typography and mirrored layout values.

| Persian documents | File |
| --- | --- |
| خانه (Home) | `pages/aurora-home-fa.json` |
| سربرگ (Header) | `headers/aurora-header-fa.json` |
| پابرگ (Footer) | `footers/aurora-footer-fa.json` |
| قهرمان - دوقسمتی (Hero) | `blocks/fa-hero-split.json` |
| شبکه ویژگیها (Feature grid) | `blocks/fa-feature-grid.json` |
| جدول قیمت (Pricing) | `blocks/fa-pricing-table.json` |
| پرسشهای پرتکرار (FAQ) | `blocks/fa-faq-accordion.json` |
| فراخوان به اقدام (CTA) | `blocks/fa-cta-band.json` |

---

## 1. Set the site language

**Settings → General → Site Language → فارسی** (or `English (United States)` with a
Persian translation pack). WordPress then flips `is_rtl()` to `true`, which is what
Elementor reads to mirror its panels and its icons — `Direction: Row` renders
right-to-left automatically, and the row/column-reverse icons swap sides.

For a Persian-only site this is the whole RTL story: **you do not need to change a single
layout value.** Elementor and WordPress handle the mirroring.

---

## 2. Install the Arad font

The Persian templates reference a custom font family named exactly **`Arad`**. Arad is a
licensed Iranian typeface and is **not bundled** with this kit — upload the copy you are
licensed to use:

1. Go to **Elementor → Custom Fonts → Add New** (this is an Elementor Pro feature).
2. Title it `Arad`.
3. Upload the weights you have: `Arad-Regular.woff2` → weight 400, `Arad-SemiBold` → 600,
   `Arad-Bold` → 700. WOFF2 keeps the payload small; WOFF and TTF also work.
4. **Publish.** The family name in Elementor becomes the title you typed — so it must be
   `Arad` (capital A, no space, no “Persian” suffix) or the global styles will fall back
   to the next family in the stack.

Then check it took: **Elementor → Site Settings → Global Fonts → FA / Headings** should
show family **Arad**.

### Don't have Arad?

Two options, both zero code:

* **Substitute.** Open `Elementor → Site Settings → Global Fonts` and change the family of
  the four `FA / …` styles to whatever you do have. Iranian sites commonly use
  `IRANSansX`, `Vazirmatn`, `Estedad` or `Sahel`; all four are free and install the same
  way through *Custom Fonts*.
* **Use a hosted Persian font.** Vazirmatn is on Google Fonts. Type its name into the
  font-family field and Elementor will load it from Google — nothing to upload, but it adds
  a third-party request (see [06](06-performance-accessibility.md)).

### Arad fallback stack

If Arad fails to load, the Persian text falls back to the theme font rather than to a
broken render. To make the fallback explicit, edit the four `FA / …` global styles and
append your second choice after the family name — Elementor accepts a comma-separated
stack in the font-family field, e.g. `Arad, IRANSansX, Vazirmatn, sans-serif`.

---

## 3. Why Persian typography needs its own styles

The `FA / …` global styles differ from the Latin ones on purpose:

| | Latin style | Persian style | Why |
| --- | --- | --- | --- |
| Line height | 1.12 – 1.3 em for headings | **1.5 – 1.55 em** | Persian ascenders, descenders, dots and diacritics need vertical clearance; the same line-height that looks tight-and-modern in English clips Persian glyphs. |
| Body line height | 1.75 em | **2.0 em** | Makes long Persian paragraphs comfortable to read. |
| Letter spacing | −1.6 px on display | **0** | Negative tracking breaks the joins between Persian letters. |
| Text transform | uppercase on eyebrows | **none** | Persian has no letter case; `uppercase` is a no-op that only confuses editors. |
| Font size | 64 px display | **54 px display** | Persian glyphs are visually larger per point size, so the same nominal size looks heavier. |
| Weight | 700 display | **700** | Persian bold is less contrasty than Latin bold; keeping 700 preserves hierarchy. |

These four styles are bound per element, exactly like the Latin ones — so you can still
override any single heading (**Style → Typography**) without touching the rest.

---

## 4. Spacing and numerals

* **Spacing.** The kit keeps the same 4-px spacing scale in both languages. Persian text
  runs slightly wider, so if a card feels tight, increase the container's **Layout → Gaps**
  by 4 px — it is one control on one container.
* **Numerals.** The Persian templates use Persian-Indic digits for display text (۰۱، ۰۲،
  and so on). Form inputs, statistics and the pricing table keep Latin digits so that
  WordPress, Elementor counters, WooCommerce and search all keep working normally. If you
  want Persian digits in a specific spot, just type them into the heading — the counter
  widget takes a `prefix`/`suffix` field for that reason.
* **Mixed content.** Where a Persian paragraph contains a Latin product name or a URL,
  the browser handles the bidirectional run automatically. If you see an awkward line break
  in a mostly-Latin block, add a `&lrm;` (left-to-right mark) through the Text Editor
  widget's *Text* tab — no code, just a character.

---

## 5. RTL checklist

Run through this after building the Persian site:

- [ ] `Settings → General → Site Language` is a Persian locale
- [ ] The Arad (or substitute) family is published under `Elementor → Custom Fonts`
- [ ] `Site Settings → Global Fonts` shows the four `FA / …` styles bound to that family
- [ ] The Persian page uses **elementor_header_footer (Full Width)** page layout
- [ ] The header and footer **conditions** point at the Persian templates (see below)
- [ ] The Nav Menu widget is bound to the Persian menu
- [ ] Buttons read correctly — Elementor mirrors the icon automatically, so a *right* icon
      arrow points left in RTL. If you want an explicit direction, set **Icon → Position**
      per button.
- [ ] Logos, brand marks and any images containing Latin text are *not* mirrored — check
      the header, footer and case-study cards
- [ ] Phone numbers, email addresses and URLs still read left-to-right inside Persian
      paragraphs (browsers usually get this right; verify in the browser)

### Serving both languages at once

The cleanest approach with Elementor alone:

1. Build the English pages and the Persian pages as separate WordPress pages.
2. In **Templates → Theme Builder**, create **two** headers and **two** footers, and give
   each pair an **Include → Specific Pages** condition that lists only the pages of that
   language.
3. Install a multilingual plugin (WPML, Polylang or TranslatePress) if you need automatic
   language switching, hreflang tags and a language menu. The kit does not depend on any of
   them — the templates are plain Elementor documents, so they work the same either way.

Alternatively, put the whole Persian site on a subdomain with its own WordPress install and
its own per-locale `Site Language` setting. Many Iranian hosts prefer this because it keeps
the two RTL/LTR configurations completely independent.
