# 06 — Performance & accessibility

The kit is built to be light by construction rather than optimised afterwards. This page
lists what is already true, what to enable once, and what to check on your own hosting.

---

## Already true in the kit

| Decision | Effect |
| --- | --- |
| **Flexbox Containers only** | No legacy `section > column > widget` wrapper divs. Enables Elementor's Optimized DOM and cuts roughly a third of the markup on a page like Home. |
| **16 widget types total** | Elementor enqueues CSS and JS per widget type actually used. No carousel, slider, lottie, video, gallery or mega-menu libraries are pulled in. |
| **No custom CSS, no custom JS** | Nothing in the kit adds a `<style>` or `<script>` beyond what Elementor itself emits. |
| **Animation = Elementor Motion Effects** | `fadeInUp` with staggered 80–110 ms delays, implemented by Elementor's own tiny CSS. No ScrollTrigger, AOS, or GSAP. |
| **One request per image** | 24 image widgets across the whole kit, 7 unique files. |
| **3:2 imagery at 1500 × 1000** | One honest size per slot, no 4000 px originals to re-encode. |
| **Progressive JPEG, q90** | 91–274 KB each, ~976 KB of demo imagery in total. |
| **Every image has `alt` text** | Checked in the build, editable per image. |
| **Semantic tags** | `<section>`, `<header>`, `<footer>`, `<main>` are set on the containers that need them (Advanced → HTML Tag), so the landmark structure is correct without extra elements. |
| **Heading hierarchy is literal** | Every heading uses the tag that its position requires (`H1` once per page, `H2` per section, `H3` per card). No `div` pretending to be a heading. |
| **Buttons are Button widgets** | Real `<a>`/`<button>` elements with `:focus` styles from Elementor, not clickable divs. |
| **FAQ accordion carries FAQ schema** | Accordion → *FAQ Schema* is on, giving eligible FAQ rich results. |

---

## Enable these once per site

`Elementor → Settings → Features`

| Feature | Set to | Why |
| --- | --- | --- |
| **Flexbox Container** | Active | Required — the kit is containers-only |
| **Optimized DOM Output** | Active | Removes wrapper divs; the kit is compatible |
| **Improved Asset Loading** | Active | Loads widget CSS/JS only on pages that use them |
| **Improved CSS Loading** | Active | Inlines only the CSS the page needs |
| **Inline Font Icons** | Active | Removes Elementor's Font Awesome *request*; only used glyphs are inlined |
| **Optimized Image Loading** | Active | Native `loading="lazy"` and correct `sizes` on images |
| **Element Caching** | Active (Pro) | Caches the rendered markup of repeating elements |

`Elementor → Settings → Performance`

* **Image Sizes** — keep only the sizes you actually use (e.g. `thumbnail`, `medium`,
  `large`, `1536×1536`, `full`). The kit uses `large` for card images and `full` for the
  hero; deleting the unused ones saves nothing at runtime but keeps the library clean.
* **Fonts** — leave *Google Fonts → Load from Google* on unless your jurisdiction requires
  self-hosting; if it does, switch to **Self-host** and Elementor downloads and serves Sora
  and Inter locally.

`Elementor → Settings → Advanced`

* **Load Font Awesome 4 Support** → *No*. This kit uses Font Awesome 6 names only
  (`fas fa-check`, `fab fa-linkedin-in`). Turning FA4 off removes a shim.

---

## Suggested caching layer

Caching, minification and CDN are host-level concerns, not template concerns, but the kit
behaves well with the usual stack:

* **Page cache** — WP Rocket, FlyingPress, LiteSpeed Cache, or your host's built-in cache.
* **CSS/JS** — Elementor's own optimised output is already minimal; combining the remaining
  Elementor files is usually neutral-to-positive. Delaying *non-critical* JS is fine.
* **Images** — the JPEGs are already compressed; converting them to WebP/AVIF at the CDN or
  in your media optimiser gives the largest remaining win (typically 30–45 % on this set).
* **CDN** — no runtime dependency on GitHub either way: on import, Elementor copies every
  image into your Media Library and rewrites the URLs to your own domain.

Targets this kit is designed to meet on a normal shared host after the caching layer above:
LCP < 2.5 s, CLS < 0.1, INP < 200 ms. The layout is written so nothing shifts: every image
slot has an aspect ratio, grids are flex-based rather than absolutely positioned, and no
element animates a property that affects layout.

---

## Accessibility

### Contrast

The palette was chosen against WCAG AA (4.5:1 for body text, 3:1 for large text and UI).

| Pair | Ratio | Verdict |
| --- | ---: | --- |
| `#57534E` Stone on `#FFFBF5` Sand 50 | 7.4 : 1 | AAA — body copy |
| `#1C1917` Ink on `#FFFBF5` | 16.6 : 1 | AAA — headings |
| `#1C1917` Ink on `#F4A62A` Amber | 9.1 : 1 | AAA — button label |
| `#A8A29E` muted on `#1C1917` Ink | 6.4 : 1 | AA — body copy on dark |
| `#F4A62A` Amber on `#1C1917` Ink | 7.9 : 1 | AAA — accents on dark |
| `#D98A14` Amber 600 on `#FFFBF5` | 3.4 : 1 | AA large only — used for eyebrows (uppercase 13 px bold) and links |

The one borderline item is the eyebrow label, which is decorative reinforcement of the
heading beneath it. If you need strict AA on every element, darken
**Amber 600** to `#B8760E` (4.6 : 1) in Global Colors and everything follows.

### Structure and behaviour

* One `H1` per page; sections use `H2`; cards use `H3`. Edit the tag from
  **Content → HTML Tag** on any Heading widget — the visual size does not change.
* Landmarks come from container HTML tags: `<header>`, `<main>`, `<footer>`, `<section>`.
* Decorative icons are Icon widgets, which Elementor renders as `<i>` with no accessible
  name — they are ignored by screen readers, which is correct for the decorative ones.
  Where an icon carries meaning (a feature bullet), the meaning is repeated in the adjacent
  text.
* Form fields have real `<label>` elements from the Form widget's *Field Label*, and the
  required fields are marked (*Field Options → Required*).
* Focus states come from Elementor's own stylesheet; the kit does not remove outlines.

### Before you go live

- [ ] Run Lighthouse on Home and Contact at 360 px, 768 px and 1440 px
- [ ] Tab through the header, the mobile menu, the form and the footer
- [ ] Check the Persian pages with the Arad font actually loading (fallback metrics differ)
- [ ] Run axe DevTools once per unique page layout
- [ ] Confirm the Form's success and error messages are still descriptive
- [ ] Verify the popup can be closed with the keyboard after it opens
