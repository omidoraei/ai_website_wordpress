# 02 — Design system

Everything visual in this kit is driven by Elementor's **Site Settings** — global
colours, global fonts and the style tabs. No element carries a hard-coded hex that is
not first defined as a global. Change a global once and the whole site follows.

---

## Global colours

`Elementor → Site Settings → Global Colors`

### System colours (the four slots Elementor reserves)

| Slot | Name in kit | Hex | Used for |
| --- | --- | --- | --- |
| Primary | Amber | `#F4A62A` | Buttons, links on hover, accents, statistics, icons |
| Secondary | Ink | `#1C1917` | Headings, dark surfaces, secondary buttons |
| Text | Stone | `#57534E` | Body copy |
| Accent | Coral | `#EF6C4D` | Metric highlights, product-shot detail |

### Custom colours (the rest of the palette)

| Name | Hex | Role |
| --- | --- | --- |
| Ink 950 | `#141110` | Footer surface, announcement bar |
| Ink 900 | `#1C1917` | Dark sections, dark cards |
| Ink 800 | `#292524` | Dark card tops, buttons on dark |
| Amber 600 | `#D98A14` | Button hover, eyebrow text |
| Amber 100 | `#FDF0DA` | Badges, icon-tile backgrounds |
| Coral 600 | `#D8553A` | Accent hover |
| Coral 100 | `#FDECE7` | Soft accent surfaces |
| Sand 50 | `#FFFBF5` | Page background |
| Sand 100 | `#FAF4EA` | Secondary surface |
| Sand 200 | `#F3E9DB` | Sunken surface |
| Border | `#E8DCCC` | 1 px hairlines, card borders, inputs |
| Muted Text | `#8C8177` | Captions, meta, small labels |
| Muted Text (on dark) | `#A8A29E` | Body copy on dark surfaces |
| White | `#FFFFFF` | Cards, form fields |
| Success | `#2F9E6B` | Check icons in feature lists |

> Two values are intentionally **not** globals because Elementor globals are solid
> colours only: the translucent borders on dark surfaces (`rgba(255,255,255,0.12)`) and
> the gradient stops. They are defined in `tools/aurora/tokens.py` as `C["line_dark"]`
> and the `SHADOW` table.

### Rebranding with one global

Want a blue brand instead of amber? Open **Site Settings → Global Colors**, change
**Primary**, and set **Amber 600** to a darker blue and **Amber 100** to a very light
blue. Because every amber element references one of those three globals, the entire site
re-skins in three edits — including buttons, badges, icon tiles, statistics and hovers.

---

## Global fonts

`Elementor → Site Settings → Global Fonts`

| Slot / style | Family | Weight | Desktop | Mobile | Line height | Tracking |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| **Primary** — Headings | Sora | 600 | 42 px | 28 px | 1.15 em | −0.6 px |
| **Secondary** — Subheadings | Inter | 600 | 20 px | — | 1.45 em | −0.1 px |
| **Text** — Body | Inter | 400 | 17 px | 16 px | 1.75 em | 0 |
| **Accent** — Buttons & labels | Sora | 600 | 15 px | — | 1.2 em | 0.2 px |
| Display — Hero H1 | Sora | 700 | 64 px | 36 px | 1.06 em | −1.6 px |
| Section Heading — H2 | Sora | 700 | 46 px | 28 px | 1.12 em | −1.0 px |
| Card Title — H3 | Sora | 600 | 22 px | 20 px | 1.30 em | −0.3 px |
| Eyebrow / Overline | Inter | 700 | 13 px | — | 1.30 em | 1.6 px, uppercase |
| Lead Paragraph | Inter | 400 | 19 px | 17 px | 1.70 em | 0 |
| Nav / Menu Item | Inter | 500 | 16 px | — | 1.30 em | 0 |
| Stat Number | Sora | 700 | 56 px | 40 px | 1.05 em | −1.5 px |
| **FA / Headings** | Arad | 700 | 40 px | 26 px | **1.5 em** | 0 |
| **FA / Hero Display** | Arad | 700 | 54 px | 30 px | **1.55 em** | 0 |
| **FA / Body** | Arad | 400 | 17 px | 16 px | **2.0 em** | 0 |
| **FA / Eyebrow & Nav** | Arad | 600 | 15 px | — | 1.7 em | 0 |

The four `FA / …` styles are what the Persian templates bind to. They use looser
line-heights and drop the uppercase transform, because Persian script needs the vertical
room for dots and diacritics and has no letter case. See
[04-rtl-persian-setup.md](04-rtl-persian-setup.md).

### The heading ladder

`Site Settings → Theme Style → Typography` also sets `H1…H6` for any heading that is not
bound to a global — for example a heading you add yourself later:

| | Size | Weight | Line height |
| --- | ---: | --- | ---: |
| H1 | 64 px | 700 | 1.06 em |
| H2 | 46 px | 700 | 1.12 em |
| H3 | 22 px | 600 | 1.30 em |
| H4 | 19 px | 600 | 1.35 em |
| H5 | 16 px | 700 | 1.40 em |
| H6 | 13 px | 700 (uppercase) | 1.30 em |

---

## Spacing scale

All padding, margin and gap values in the kit come from one 4-px based scale. Elementor
containers expose it through **Layout → Gaps** and the **Advanced** tab, so every value is
still editable — the scale just keeps the design consistent.

| Token | px | Typical use |
| --- | ---: | --- |
| 3xs | 4 | icon-to-text nudge |
| 2xs | 8 | badge inner padding |
| xs | 12 | tight stacks |
| sm | 16 | card inner gap |
| md | 24 | card grid gap (mobile) |
| lg | 32 | section inner gap |
| xl | 40 | card grid gap (desktop) |
| 2xl | 48 | hero card padding |
| 3xl | 64 | large component padding |
| 4xl | 80 | desktop section padding (compact) |
| 5xl | 96 | dark band padding |
| 6xl | 120 | desktop section padding (standard) |

### Section rhythm

| Breakpoint | Vertical padding | Horizontal padding |
| --- | --- | --- |
| Desktop | 120 px | 24 px |
| Tablet (≤1024) | 80 px | 24 px |
| Mobile (≤767) | 56 px | 20 px |

Content width is **1240 px** on desktop and `100%` on tablet and mobile, set once in
`Site Settings → Layout → Content Width`. Every section wraps its content in a boxed
container that inherits it.

### Radius scale

| Token | px | Use |
| --- | ---: | --- |
| sm | 10 | inputs, small chips |
| md | 16 | icon tiles, images inside cards |
| lg | 22 | cards |
| xl | 30 | feature media frames |
| 2xl | 40 | the call-to-action card |
| pill | 999 | buttons, badges |

### Elevation

| Token | Value | Use |
| --- | --- | --- |
| xs | `0 1px 2px rgba(28,25,23,.06)` | card resting state |
| sm | `0 2px 6px -1px rgba(28,25,23,.08)` | subtle lift |
| md | `0 10px 24px -8px rgba(28,25,23,.14)` | card hover |
| lg | `0 24px 48px -16px rgba(28,25,23,.22)` | hero frame, featured plan |
| xl | `0 40px 80px -24px rgba(28,25,23,.28)` | popup, CTA card |

Cards lift to `md` on hover with a 0.3 s transition, and their border turns Primary —
both are ordinary Elementor controls on the container (**Style → Border → Hover** and
**Style → Box Shadow → Hover**), not CSS.

---

## Component recipes

These are the reusable patterns the kit is assembled from. Each one is a container you can
copy anywhere and edit entirely from the panel.

**Card** — container, `1px solid Border`, radius 22, padding 34 (desktop) / 24 (mobile),
white background. Children stacked with a 16–18 px gap.

**Icon tile** — container with an Icon widget inside. Background `Sand 100`, radius 16,
padding 16, icon 22 px in `Amber 600`. Hover swaps the background to `Amber 100`.

**Eyebrow** — a row containing a 26 × 2 px Divider and a paragraph Heading styled with the
*Eyebrow* global. Delete the divider for a naked label.

**Badge / pill** — container with `pill` radius, `Amber 100` background, 7 × 16 px padding,
optional 13 px icon.

**Button** — the theme-style default is a pill in `Primary` with ink text. The kit uses
five variants, all from the Button widget's own style tab:

| Variant | Background | Text | Where |
| --- | --- | --- | --- |
| Primary | `#F4A62A` | Ink | main calls to action |
| Dark | Ink | White | secondary calls to action |
| Outline | transparent + `1px Border` | Ink | paired buttons |
| Outline light | transparent + white 35 % | White | dark surfaces |
| Link | transparent | Ink → Amber on hover | “Learn more”, nav-ish links |

---

## Applying the globals by hand

If your Elementor version has no **Import Kit** screen, open
**Elementor → Site Settings** and enter these values directly.

1. **Global Colors** — click each of the four system swatches and paste the hex from the
   *System colours* table above, then add the custom colours with **+ Add Color**,
   matching the **names** exactly (the names are what the templates' references resolve
   to). Order does not matter, names do.
2. **Global Fonts** — set the four system slots from the *Global fonts* table, then add
   the remaining eleven styles with **+ Add Style** using the same names.
3. **Layout** — Content Width `1240`, **Gaps** `0` (the kit sets its own gaps per section).
4. **Theme Style → Typography** — paste the H1–H6 ladder, set Body colour to
   `globals/colors?id=text`, and set the Link colours to Ink and hover Amber 600.
5. **Theme Style → Buttons** — background `Primary`, text `Ink 900`, radius `999`,
   padding `17 / 30`, hover background `Amber 600`.
6. **Theme Style → Form Fields** — background `White`, border `1px Border`, radius `12`,
   padding `15 / 17`, focus border `Amber 600`.
7. **Background** — set the page background to `Sand 50`.

The `dist/site-settings.json` file lists every value in the exact shape Elementor stores
it, if you would rather copy from the source.

---

## Hosting the imagery yourself

Every image widget stores a plain URL. The kit points at a permanent git tag:

```
https://github.com/omidoraei/ai_website_wordpress/raw/kit-assets-v1/media/hero-dashboard.jpg
```

Elementor downloads each file into your Media Library **on template import**, so your
live site never requests GitHub — but you can host the source files yourself if you
prefer. Two ways, neither of which needs code:

1. **After import (recommended).** Because Elementor already localised every image,
   nothing to do — the widgets point at your uploads folder.
2. **Before import.** Upload the seven JPEGs from `media/` to your Media Library or CDN,
   note the URLs, then edit each Image widget in the editor and pick your file. Or change
   `ASSET_BASE` in `tools/aurora/tokens.py` to your own base path, run
   `python3 tools/build.py`, and import the resulting templates — every image widget then
   carries your URL from the start.

Image slots are all 3:2 landscape (1500 × 1000). If you replace them, keep that ratio so
the containers keep their intended height, or adjust the container's
**Style → Height** afterwards.

---

## Where the tokens live

`tools/aurora/tokens.py` is the single source of truth:

```python
C = {"primary": "#F4A62A", ...}          # raw values
G = {"primary": "globals/colors?id=primary", ...}   # global references
T = {"h2": "globals/typography?id=h2", ...}         # global font references
SP / RADIUS / SHADOW / W / SECTION_PAD_Y            # spacing, radius, elevation, widths
```

Change a value, run `python3 tools/build.py`, and every one of the <!--f:documents_total-->40<!--/f--> is
regenerated with the new token — including the kit's own `site-settings.json`.
