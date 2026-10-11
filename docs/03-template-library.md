# 03 — Template library

<!--f:documents_total-->40<!--/f-->: <!--f:pages-->9<!--/f-->, <!--f:theme_builder_layouts-->7<!--/f-->, 1 popup, 22 reusable section
blocks and the kit itself. The generated catalogue with live container and widget counts
is [`templates/INDEX.md`](../templates/INDEX.md).

Every `<sup>` marker below means the block can be dropped on any page with
**Add Template → My Templates**.

---

## Pages

| Template | File | Sections it stacks |
| --- | --- | --- |
| **Home (English)** | `pages/aurora-home-en.json` | Hero → Logo cloud → Feature grid → Feature zigzag → Stats band → Capability cards → Process steps → Case studies → Testimonials → Pricing → FAQ → Newsletter → CTA |
| **Home (Persian / RTL)** | `pages/aurora-home-fa.json` | Same order, re-ordered for Persian reading flow (stats band moves above the zigzag), all copy in Farsi |
| **About** | `pages/aurora-about.json` | Page hero → Story (two column) → Stats band → Values grid → Team → Testimonials → CTA |
| **Services** | `pages/aurora-services.json` | Page hero → Capability cards → Engagements → Deliverables → Process steps → FAQ → CTA |
| **Case Studies** | `pages/aurora-portfolio.json` | Page hero → Three featured cases → Selected engagements list → Testimonials (dark) → CTA |
| **Pricing** | `pages/aurora-pricing.json` | Page hero → Three plans → Comparison table → FAQ → Testimonials → CTA |
| **Journal** | `pages/aurora-blog.json` | Page hero → Post grid (Post widget) → Newsletter |
| **Contact** | `pages/aurora-contact.json` | Page hero → Contact (form + details) → FAQ (dark) → CTA |
| **404** | `pages/aurora-404.json` | Full-height card with a compass icon, recovery buttons and three suggested links |

Each page is a flat list of top-level `<section>` containers. Nothing is nested inside
another page and no page references another template, so you can delete a section, reorder
sections by drag-and-drop, or lift one section onto a different page without side effects.

---

## Theme Builder layouts

| Template | Type | File | Contents |
| --- | --- | --- | --- |
| **Header (English)** | header | `headers/aurora-header-en.json` | Sticky shell, dark announcement bar with a dismissible-feeling CTA link, logo + wordmark, Nav Menu, *Sign in* + *Book a demo* buttons |
| **سربرگ (فارسی)** | header | `headers/aurora-header-fa.json` | RTL variant: right-aligned logo, mirrored button order, Arad typography |
| **Footer (English)** | footer | `footers/aurora-footer-en.json` | Brand + blurb + social icons, two link columns, contact column, hairline, copyright + legal links |
| **پابرگ (فارسی)** | footer | `footers/aurora-footer-fa.json` | RTL variant of the same |
| **Single Post** | single | `loop/aurora-single-post.json` | Breadcrumbs, post meta, featured image, content, divider, author box, post navigation, comments — then a width-100 % CTA band |
| **Blog Archive** | archive | `loop/aurora-archive.json` | Page hero with `theme-archive-title`, Archive Posts widget (cards, 3/2/1 columns, numbered pagination), newsletter, CTA |
| **Search Results** | search-results | `loop/aurora-search-results.json` | Hero with a Search Form widget, Archive Posts widget, CTA |

Detailed configuration for each: [05-theme-builder.md](05-theme-builder.md).

---

## Popup

| Template | File | Contents |
| --- | --- | --- |
| **AI Readiness Checklist** | `popups/aurora-lead-magnet.json` | Centred card: icon tile, eyebrow, H2, lead paragraph, single-field email Form, privacy line |

Ship settings already stored in the template:

* Type **Exit Intent**, entrance animation **fadeInUp** (0.4 s), exit **fadeOutDown**
* **Prevent scroll** on, close button **outside** with a 300 ms delay
* Overlay `rgba(20,17,16,0.8)`
* **Avoid multiple popups** on

---

## Reusable section blocks (22)

### Structure blocks

| Block | What it contains | Typical use |
| --- | --- | --- |
| `Block \| Hero - Split with product shot` <sup>block</sup> | Badge, H1, lead, two buttons, rating row, 3-up proof chips, framed product image with two floating statistic cards | Home, product pages, landing pages |
| `Block \| Page Hero - Inner page header` <sup>block</sup> | Breadcrumbs, eyebrow, H2, lead, centred | Top of every inner page |
| `Block \| Logo Cloud - Trusted by` <sup>block</sup> | Six editable wordmarks in a flex row | Below the hero |
| `Block \| Call To Action - Gradient card` <sup>block</sup> | Gradient card, eyebrow, H2, lead, two buttons, response-time note | Bottom of every page |
| `Block \| Newsletter - Subscribe` <sup>block</sup> | Two columns: copy + single-field subscribe form in a card | Before the CTA |

### Content blocks

| Block | What it contains | Typical use |
| --- | --- | --- |
| `Block \| Feature Grid - Six icon cards` <sup>block</sup> | Section head + 6 cards in a 3/2/1 grid, staggered entrance | Feature overview |
| `Block \| Feature Zigzag - Two alternating rows` <sup>block</sup> | Two rows with the media on opposite sides, bullet pills and a button | “How it works”, deep dives |
| `Block \| Capability Cards - Three services` <sup>block</sup> | 3 tall cards with icon tile, copy, three check bullets and a link | Services, capabilities |
| `Block \| Process Steps - Four numbered stages` <sup>block</sup> | Four numbered pills with heading and copy, 4/2/1 columns | Onboarding, delivery process |
| `Block \| Content - Two column story` <sup>block</sup> | Copy column with a check list + framed image | About, story, “why us” |
| `Block \| Team Grid - Four members` <sup>block</sup> | Initial-avatar circle, name, role, bio, two social icons | About, company |
| `Block \| FAQ - Accordion` <sup>block</sup> | Accordion with FAQ schema markup on | Pricing, services, contact |
| `Block \| Contact - Form + details` <sup>block</sup> | Contact Form side by side with a dark info card (email, phone, support, address, hours, socials) | Contact page |

### Proof blocks

| Block | What it contains | Typical use |
| --- | --- | --- |
| `Block \| Stats Band - Dark counters` <sup>block</sup> | Dark band, H2 + 4 animated counters with labels | Anywhere you need credibility |
| `Block \| Case Studies - Three cards` <sup>block</sup> | Image, category pill, title, headline metric, link | Portfolio, home |
| `Block \| Testimonials - Three quotes` <sup>block</sup> | Quote icon, quote, hairline, name and role | Home, pricing, about |

### Commercial blocks

| Block | What it contains | Typical use |
| --- | --- | --- |
| `Block \| Pricing Table - Three plans` <sup>block</sup> | Three plans, the middle one inverted to ink with a “Most popular” badge | Pricing, home |

### Persian variants

| Block | Notes |
| --- | --- |
| `Block \| قهرمان - دوقسمتی` | Hero, Farsi copy, Arad display style |
| `Block \| شبکه ویژگیها (فارسی)` | Six-card feature grid in Farsi |
| `Block \| جدول قیمت (فارسی)` | Three-plan pricing in Farsi |
| `Block \| پرسشهای پرتکرار (فارسی)` | Accordion in Farsi |
| `Block \| فراخوان به اقدام (فارسی)` | CTA band in Farsi |

---

## Widgets used

The kit deliberately uses a small, well-supported widget set — sixteen free Elementor widgets (Pro-only widgets are documented per document; the control-name audit stays advisory - see `docs/CLAIMS.md` C-004)
plus 12 Elementor Pro widgets. Nothing else, and no HTML widget.

**Elementor Free**

`heading` · `text-editor` · `button` · `icon` · `icon-list` · `image` · `divider` ·
`spacer` · `counter` · `accordion` · `tabs` · `social-icons` · `icon-box` ·
`testimonial` · `search-form` · `menu-anchor`

**Elementor Pro**

`form` · `posts` · `archive-posts` · `nav-menu` · `breadcrumbs` · `post-info` ·
`post-navigation` · `post-comments` · `author-box` · `theme-site-logo` ·
`theme-post-featured-image` · `theme-post-content` · `theme-archive-title` ·
`theme-page-title`

**Containers**

Every layout — pages, sections, cards, badges, buttons rows, the grid — is a Flexbox
Container. There is no legacy Section/Column element anywhere in the kit.

---

## Duplicating and moving blocks

1. In the editor, hover the container handle and press **Ctrl/Cmd + C**.
2. Move to the target page, press **Ctrl/Cmd + V**.
3. Elementor regenerates the element ids and keeps every setting, including the global
   colour and font references — the block picks up the destination site's branding.

To reuse a block across many pages *and* keep them in sync, save it once to the library:
right-click the container handle → **Save as Template**, give it a name, then insert it
from *My Templates* everywhere. Editing the library copy will not retro-update inserted
copies (that is how Elementor works), but it keeps your insert flow consistent.
