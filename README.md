# Aurora AI — Elementor Template Kit

A complete, **Elementor-native** website design for an AI / SaaS product company.
Everything is built from Elementor Flexbox Containers, native Elementor widgets and
Elementor Pro widgets — there is **no custom HTML widget, no custom CSS and no
JavaScript** anywhere in the kit.

* **40 Elementor documents** — 9 pages, 2 headers, 2 footers, a single-post and archive
  layout, a search-results layout, an exit-intent popup and 22 reusable section blocks
* **962 containers, 1 280 widgets** — every one of them editable in the Elementor panel
* **Global design system** — 4 system colours, 14 custom colours, 18 typography styles
* **Bilingual** — a full English (LTR) set and a full Persian (RTL) set
* **Theme Builder ready** — header, footer, single, archive, search and popup documents
* **Fully responsive** — separate desktop / tablet / mobile values, not a scaled-down desktop

---

## What is in this repository

```
templates/                 the kit itself - one Elementor JSON per document
  pages/                   9 page templates
  blocks/                  22 reusable section templates
  headers/  footers/       Theme Builder header + footer (EN and FA)
  loop/                    single post, blog archive, search results
  popups/                  lead-magnet popup
  kit/aurora-site-settings.json    the design system (global colours + fonts + layout)
  INDEX.md                 generated catalogue with container/widget counts

dist/                      ready-to-import packages
  aurora-ai-templates.zip  import into  Templates > Saved Templates
  aurora-ai-kit.zip        import into  Elementor > Tools > Import/Export Kit
  site-settings.json       the raw kit payload
  manifest.json            kit manifest

media/                     the demo imagery (optimised JPEG, 3:2)
media/_raw/                the original PNG renders (not needed to install)

tools/                     the generator that produced every JSON file
  build.py                 build + validate the whole kit
  media.py                 optimise media/_raw/*.png -> media/*.jpg
  preview.py               render a browser preview of the templates
  aurora/                  Elementor JSON DSL, tokens, sections, pages, theme parts

docs/                      full documentation (start at 01)
preview/                   static HTML preview of the design (review aid only)
```

> `preview/` and `tools/` exist so you can review, regenerate and re-brand the kit.
> Neither is installed on WordPress — the deliverable is `templates/` and `dist/`.

---

## Install in four steps

**1 — Import the templates**
WordPress admin → **Templates → Saved Templates → Import Templates** →
choose `dist/aurora-ai-templates.zip`. All 40 templates appear under *My Templates*.

**2 — Apply the design system**
WordPress admin → **Elementor → Tools → Import / Export Kit → Import Kit** →
choose `dist/aurora-ai-kit.zip`.
This sets the global colours, global fonts, content width, breakpoints, heading ladder,
button styles and form-field styles.

*(No import screen in your Elementor version? Follow the manual table in
[docs/02-design-system.md](docs/02-design-system.md). It takes about four minutes.)*

**3 — Build the Theme Builder parts**
**Templates → Theme Builder** → create a **Header**, a **Footer**, a **Single Post**,
an **Archive** and a **Search Results** document and insert the matching template from
*My Templates*. Then add the condition (`Entire Site` for the header and footer).

**4 — Create your pages**
Create a page → **Edit with Elementor** → *Add Template* → **My Templates** → insert
the matching page template. Set the page layout to *Elementor Full Width* and hide the
title for every page.

Full walkthrough, with the exact Template Kit Library → My Templates steps and the
*Pages* menu mapping: **[docs/01-installation.md](docs/01-installation.md)**.

---

## Documentation

| Doc | What it covers |
| --- | --- |
| [01 — Installation](docs/01-installation.md) | Import, page setup, Theme Builder conditions, menus |
| [02 — Design system](docs/02-design-system.md) | Global colours, global fonts, spacing, radius, shadows + rebranding |
| [03 — Template library](docs/03-template-library.md) | Every template, every section, what each block is for |
| [04 — RTL & Persian](docs/04-rtl-persian-setup.md) | Arad font install, RTL settings, Persian typography rules |
| [05 — Theme Builder](docs/05-theme-builder.md) | Header, footer, single, archive, search, popup configuration |
| [06 — Performance & a11y](docs/06-performance-accessibility.md) | Core Web Vitals, image sizes, contrast, focus states |
| [07 — FAQ & troubleshooting](docs/07-faq-troubleshooting.md) | Common import and editor issues |

---

## Requirements

| | |
| --- | --- |
| WordPress | 6.0 or newer |
| Elementor | 3.16 or newer **with Flexbox Containers active** (`Elementor → Settings → Features → Flexbox Container`) |
| Elementor Pro | 3.16 or newer for the header, footer, single, archive, search, popup, Post/Archive widgets and the Forms |
| PHP | 7.4 or newer (8.1+ recommended) |
| Memory | 128 MB minimum, 256 MB recommended |

The pages also work on **Elementor Free** — the call-to-action and contact sections
contain a Form widget that simply renders nothing until Elementor Pro is active, and
the header/footer/popup templates need Pro to be *assigned* through the Theme Builder.

---

## Design language

| Token | Value |
| --- | --- |
| Primary — Amber | `#F4A62A` |
| Secondary — Ink | `#1C1917` |
| Accent — Coral | `#EF6C4D` |
| Page background | `#FFFBF5` |
| Headings | Sora (600 / 700) |
| Body | Inter (400 / 500) |
| Persian | Arad |

Full swatch and type-scale tables: [docs/02-design-system.md](docs/02-design-system.md).

---

## Rebranding in one place

Every colour, font, image URL and spacing value comes from `tools/aurora/tokens.py`.
Change a value there and run:

```bash
python3 tools/build.py      # rebuild templates/ + dist/ + INDEX.md
python3 tools/media.py      # optional: re-optimise images
python3 tools/preview.py    # optional: re-render preview/
```

The build validates every document before writing it: unique element ids, a known
`widgetType` for every widget, containers with an explicit `isInner`, and no `null`
settings anywhere.

---

## Preview

```bash
python3 tools/preview.py --serve     # http://localhost:8080
```

The preview regenerates `preview/*.html` from the JSON, then serves it. It approximates
Elementor's front-end output so you can review the design in a browser; the real styling
on your site is produced by Elementor from the same settings.

---

## Licence

- **Templates, design system and documentation:** MIT — see [LICENSE](LICENSE).
- **Demo imagery in `media/`:** generated for this kit and released under the same MIT
  licence. Replace it with your own before going live.
- **Fonts:** Sora and Inter are Google Fonts (SIL Open Font License 1.1) and are loaded
  by Elementor from Google. **Arad is not bundled** — upload your licensed copy under
  *Elementor → Custom Fonts* (see [docs/04](docs/04-rtl-persian-setup.md)).
