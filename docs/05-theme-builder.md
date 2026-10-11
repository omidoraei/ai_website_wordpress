# 05 — Theme Builder

Six Elementor Pro Theme Builder documents ship with the kit. This page explains what each
one is made of, which settings matter, and the display conditions to assign.

**Where to find it:** `Templates → Theme Builder` (Elementor Pro 3.0+). Older versions:
`Elementor → Theme Builder`.

---

## Header

**Template:** `Aurora | Header (English)` — `headers/aurora-header-en.json`
**Persian:** `سربرگ (فارسی)` — `headers/aurora-header-fa.json`

```
Header shell  (full width, sticky, hairline bottom, Sand 50 background)
├── Announcement bar      dark #141110, row, centred  · icon + text + "Read the release" link
└── Main bar              boxed 1240, row, space-between, 14/24 padding
    ├── Brand             Site Logo widget (46 px) + wordmark heading  · stays together (nowrap)
    ├── Nav Menu          flex-grow: 1, horizontal, underline pointer
    └── Button group      "Sign in" (ghost) + "Book a demo" (primary)  · hidden ≤1024 px
```

### Settings already in the template

| Setting | Value | Where to change it |
| --- | --- | --- |
| Sticky | **top**, on desktop / tablet / mobile, effects offset 60 | Select the header shell → **Advanced → Motion Effects → Sticky** |
| Shell background | Sand 50 | Shell → **Style → Background** |
| Bottom hairline | 1 px, Border colour | Shell → **Style → Border** |
| Content width | 1240 px, 100 % on tablet and mobile | Main bar → **Layout → Content Width** |
| Padding | 14 / 24 desktop · 12 / 20 tablet · 10 / 16 mobile | Main bar → **Advanced → Padding** |
| Button group | hidden below 1025 px | Button group → **Advanced → Responsive → Hide On Tablet / Hide On Mobile** |

### Things to edit first

* **Logo** — the header uses the **Site Logo** widget, so it follows
  `Appearance → Customize → Site Identity`. Upload your logo there once and it updates in
  the header everywhere.
* **Menu** — select the Nav Menu widget → **Content → Menu** → choose your WordPress menu
  (`Primary`). Leaving it empty shows Elementor's placeholder links.
* **Mobile toggle** — Nav Menu → **Content → Layout**: Toggle = *Hamburger*, Breakpoint =
  *Mobile*. Set it to *Tablet* if your menu is long. The toggle colour, size and alignment
  are on the same tab.
* **Dropdowns** — style them under Nav Menu → **Style → Dropdown**: white background,
  1 px Border border, 14 px radius, `md` box shadow and hover colours are already set.

> The announcement bar hides only its call-to-action button on mobile (the text stays, so
> the message survives). To hide the entire bar on phones, select the announcement bar
> container → **Advanced → Responsive → Hide On Mobile** and clear the button's own
> visibility rule.

### Header display conditions

**Publish**, then set the condition:

* English header → **Entire Site**
* Persian header → **Include → Singular / Archive → Pages** and list only the Persian pages

---

## Footer

**Template:** `Aurora | Footer (English)` — `footers/aurora-footer-en.json`

```
Footer shell  (full width, Ink 950)
└── Inner     (boxed 1240, column, 44 px gap, 80/24/32 padding)
    ├── Columns row      4 columns, wrap
    │   ├── Brand        wordmark · blurb · 4 social icons (circle, ink 800 → amber hover)
    │   ├── Product      link column (Icon List widget, hover to Primary)
    │   ├── Company      link column
    │   └── Talk to us    email · phone · studio address (Icon + Heading widgets)
    ├── Divider          1 px rgba(255,255,255,.12), full width
    └── Bottom row       copyright  ·  Privacy / Terms / Cookies
```

* **Columns** are containers — drag one to reorder, duplicate one to add a fifth.
* **Mobile:** the 4-column row collapses to a single column at ≤767 px
  (each column's flex basis is set to 100 % for mobile), and the bottom row stacks.
* **Social icons** are one Social Icons widget: add or remove a network from the repeater.
* **Link columns** are Icon List widgets set to *inline* view with the icon set to the
  Primary colour at 13 px. To turn a column into plain text links, set the Icon colour to
  transparent.

### Footer display conditions

Same pattern as the header: **Entire Site** for English, or an explicit page list for the
Persian footer.

---

## Single Post

**Template:** `Aurora | Single Post` — `loop/aurora-single-post.json`

Top level: a `<main>` container with an 820 px boxed width, followed by a full-bleed CTA
band.

| Order | Widget | Why |
| --- | --- | --- |
| 1 | Breadcrumbs | Home / category / post |
| 2 | Post Info | Author · date · comments · categories, styled as an uppercase eyebrow |
| 3 | Featured Image | Full size, 22 px radius |
| 4 | Post Content | Body typography from the global *Text* style, 18 px |
| 5 | Divider | 1 px hairline |
| 6 | Author Box | 68 px avatar, links to the author's posts |
| 7 | Post Navigation | Previous / Next with arrows |
| 8 | Post Comments | Threaded comments + the comment form |

Every one of these is a **dynamic** Elementor Pro widget, so it renders the current post
automatically — you never edit content here.

**Condition:** `Include → Singular → All Posts` (or narrow it to a category).

**Optional extras** you can drag in: Table of Contents (Pro), Share Buttons (Pro),
Related posts (a Posts widget with *Related* query), a newsletter block from
`Block | Newsletter - Subscribe`.

---

## Blog Archive

**Template:** `Aurora | Blog Archive` — `loop/aurora-archive.json`

```
Page hero     breadcrumbs + theme-archive-title (H1) + lead text
Post list     Archive Posts widget, cards skin, 3 / 2 / 1 columns,
              numbered pagination, excerpt on, "Read article" link
Newsletter    Block | Newsletter - Subscribe
CTA           Block | Call To Action
```

* The heading is the **Archive Title** widget, so it changes with the taxonomy
  automatically (*Journal*, *Category: Engineering*, *Tag: Evaluation*…).
* The grid is the **Archive Posts** widget → **Layout → Columns**: 3 desktop, 2 tablet,
  1 mobile, and **Pagination → Numbers**.
* Card styling lives on **Style → Card**: white background, 1 px Border border, 20 px
  radius — already set.

**Condition:** `Include → Archive → All Archive Pages`.

If you prefer to build the loop by hand later, replace the Archive Posts widget with a
**Loop Grid** widget and design the card once with a Loop Item template — the container
patterns in the kit (image → category pill → H3 → metric → link) map straight onto it.

---

## Search Results

**Template:** `Aurora | Search Results` — `loop/aurora-search-results.json`

Hero → Search Form widget (classic skin, text button) → Archive Posts widget → CTA.

**Condition:** `Include → Archive → Search Results`.

---

## 404

There is no separate Theme Builder document type for 404 in older Pro versions, so the kit
ships it as a **page** template plus two ways to use it:

* **Elementor Pro 3.16+** has a **404** document type under `Templates → Theme Builder →
  Add New → 404`. Insert `Aurora | 404 Not Found` and set the condition to `404 Page`.
* **Any version:** create the page, insert the template as usual, then set it as your
  theme's 404 with your host's redirect rule or a small `404.php` — or simply paste the
  template's containers into your theme's 404 template file via Elementor's *Theme Builder →
  Single → 404* if available.

---

## Popup

**Template:** `Aurora | Popup - AI Readiness Checklist` — `popups/aurora-lead-magnet.json`

Ship settings stored in the document:

| Group | Setting | Value |
| --- | --- | --- |
| Layout | Type | **Exit Intent** |
| Layout | Entrance animation | `fadeInUp`, 0.4 s |
| Layout | Exit animation | `fadeOutDown` |
| Layout | Prevent scroll | On |
| Close button | Position | Outside |
| Close button | Delay | 300 ms |
| Overlay | Background | classic, `rgba(20,17,16,0.8)` |
| Advanced rules | Avoid multiple popups | On |

**After inserting:** select the **Form** widget and set *Email → To* to your address
(the template ships with `hello@aurora.example`), then edit the *Email* action's subject
line. Add a second action (Mailchimp, ActiveCampaign, webhook, etc.) from
**Actions After Submit** if you want the address in a list rather than (or as well as) in
your inbox.

**Condition:** `Entire Site` for a site-wide exit offer, or
`Include → Singular → Pages → Pricing` if you only want it on the pricing page.

> Use *On Page Load* with a 20 s delay instead of *Exit Intent* on mobile — mobile browsers
> do not fire exit intent reliably.

---

## Conditions cheat-sheet

| Document | Condition | Notes |
| --- | --- | --- |
| Header (EN) | `Entire Site` | Or add `Exclude → Pages → Persian pages` |
| Header (FA) | `Include → Pages` (Persian only) | Must be *above* the EN header in no order — conditions are exclusive, so the include list wins for those pages |
| Footer (EN) | `Entire Site` | — |
| Footer (FA) | `Include → Pages` (Persian only) | — |
| Single Post | `Include → Singular → All Posts` | — |
| Blog Archive | `Include → Archive → All Archive Pages` | — |
| Search Results | `Include → Archive → Search Results` | — |
| 404 | `404 Page` | Pro 3.16+ |
| Popup | `Entire Site`, Exit Intent | — |

Condition priority: the more **specific** include wins. If a page shows the wrong header,
open `Theme Builder → Conditions` and use **Edit Condition** on each document rather than
duplicating templates.
