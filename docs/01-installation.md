# 01 — Installation

This kit installs in **four steps** and takes about ten minutes. Nothing here requires
code; every step is a standard Elementor screen.

---

## Before you start — checklist

| Item | Where | Why |
| --- | --- | --- |
| Flexbox Containers **active** | `Elementor → Settings → Features → Flexbox Container` → *Active* | Every template is built from containers. Without it the layouts collapse into one column. |
| Elementor **3.16+** | `Dashboard → Plugins` | Older versions do not know container documents. |
| Elementor Pro **3.16+** | `Dashboard → Plugins` | Header, footer, single, archive, search, popup, Forms, Post/Archive widgets. |
| A **clean** site | — | Importing onto a site that already has global colours will **append** your custom colours, not replace them. On an existing site, always take a database backup first. |
| `upload_max_filesize` ≥ 8 MB | `Tools → Site Health → Info` | Not required for these files (both zips are under 200 KB) but needed for images. |
| Outbound HTTP allowed | Server | Elementor downloads the demo images on import. See the note at the end if your host blocks it. |

> **Elementor Pro?** The header, footer, single, archive, search and popup templates can
> only be *assigned* with Pro. On Elementor Free you can still use all nine pages and all
> 22 section blocks.

---

## Step 1 — Import the templates

1. Go to **Templates → Saved Templates**.
2. Click **Import Templates** at the top of the screen.
3. Choose `dist/aurora-ai-templates.zip` and confirm.
4. When the import finishes, click **View Library** — all **40 templates** are now under
   the *My Templates* tab, grouped by name:
   * `Aurora | …` — pages, headers, footers, layouts and the popup
   * `Block | …` — the 22 reusable section blocks

The importer accepts the whole zip at once. If you would rather import one document at a
time, every file under `templates/` is an independent Elementor JSON — import any of them
directly with the same *Import Templates* button.

### What happened to the images

Every template references its imagery by absolute URL:

```
https://github.com/omidoraei/ai_website_wordpress/raw/kit-assets-v1/media/hero-dashboard.jpg
```

That is a **permanent git tag**, so the URLs never change and never expire. On import
**Elementor downloads each image into your Media Library** and rewrites the template to
point at your own uploads folder — the same mechanism it uses for any Template Kit.
After import the images belong to you, live on your domain, and are fully editable.

If you would rather host the imagery yourself, upload the files from `media/` anywhere
public and replace the base URL — see
[02-design-system.md](02-design-system.md#hosting-the-imagery-yourself). See also
[the offline note](#if-your-server-cannot-reach-the-internet) if your host blocks
outbound requests.

---

## Step 2 — Apply the design system

1. Go to **Elementor → Tools → Import / Export Kit** (older versions: **Elementor →
   Tools → Import Kit**).
2. Open the **Import Kit** tab, drop in `dist/aurora-ai-kit.zip` and run the import.
3. Elementor applies the parts this kit declares: **Global Colours, Global Fonts,
   Theme Style Settings, General Settings**.

That single import sets:

* 4 system colours + 15 custom colours (19 total)
* 15 global typography styles (4 system slots + 11 named styles, 4 of them Persian)
* content width 1240 px and tablet/mobile breakpoints
* the H1–H6 ladder, body, link, button and form-field styles
* the page background

**If your Elementor version has no Import Kit screen**, apply the same values by hand —
the complete table is in [02-design-system.md](02-design-system.md#applying-the-globals-by-hand).
It is 19 colours and 15 typography styles and takes about four minutes.

Verify with **Elementor → Site Settings → Global Colors**: you should see *Amber*,
*Ink*, *Stone* and *Coral* as the four system colours.

---

## Step 3 — Build the Theme Builder parts

Go to **Templates → Theme Builder** (Elementor 3.0 and newer; on older Pro it is
**Elementor → Theme Builder**).

Create one document of each type and insert the matching template from *My Templates*:

| Create this document | Insert this template | Display condition |
| --- | --- | --- |
| **Header** | `Aurora \| Header (English)` — or `سربرگ (فارسی)` for Persian | `Entire Site` |
| **Footer** | `Aurora \| Footer (English)` — or `پابرگ (فارسی)` for Persian | `Entire Site` |
| **Single Post** | `Aurora \| Single Post` | `All Posts` |
| **Archive** | `Aurora \| Blog Archive` | `All Archive Pages` |
| **Search Results** | `Aurora \| Search Results` | `Search Results` |
| **Popup** | `Aurora \| Popup - AI Readiness Checklist` | `Entire Site`, trigger *On Page Exit* |

How to insert: open the document in the Theme Builder → **Add Template** (the folder
icon in the editor panel) → **My Templates** → pick the template → **Insert** →
**Publish**, then set the condition.

Full settings, including the sticky header and the popup trigger configuration:
[05-theme-builder.md](05-theme-builder.md).

### The logo

The header uses the **Site Logo** widget, so it follows your site identity. Set it once
in **Appearance → Customize → Site Identity → Logo** (or **Elementor → Site Settings →
Site Identity**) and both the header and any other logo spot update together. Until a
logo is uploaded, WordPress falls back to the site name.

---

## Step 4 — Create the pages

Importing a *page* template adds it to your library; it does not create a WordPress
page. Create each page, then drop the template in:

1. **Pages → Add New**, give it the title from the table below, **Publish**.
2. Click **Edit with Elementor**.
3. Click the **folder icon → My Templates**, choose the matching template, **Insert**.
4. In **Settings** (bottom-left gear) set:
   * **Page Layout → Elementor Full Width**
   * **Elementor Canvas** *not* needed — Full Width keeps your Theme Builder header/footer
   * **Hide Title → Yes** (the templates carry their own headings)
5. **Update**.

| Page | Template to insert | Suggested permalink |
| --- | --- | --- |
| Home | `Aurora \| Home (English)` or `Home (Persian / RTL)` | `/` |
| About | `Aurora \| About` | `/about/` |
| Services | `Aurora \| Services` | `/services/` |
| Case Studies | `Aurora \| Case Studies` | `/case-studies/` |
| Pricing | `Aurora \| Pricing` | `/pricing/` |
| Journal | `Aurora \| Journal` | `/journal/` |
| Contact | `Aurora \| Contact` | `/contact/` |
| 404 | `Aurora \| 404 Not Found` | — (assigned below) |

Then:

* **Home page:** `Settings → Reading → Your homepage displays → A static page`.
* **Contacts posts page:** ``Settings → Reading → Posts page`` → *Journal*.
* **404 page:** `Templates → Theme Builder → + Add New → Single` … actually use
  **`Templates → Theme Builder → 404`**, insert `Aurora | 404 Not Found` and set the
  condition to `404 Page`.

---

## Menus

The header and footer use the **Nav Menu** widget, which renders a real WordPress menu.

1. **Appearance → Menus → create a new menu**, name it `Primary`.
2. Add your pages: Home, Services, Case Studies, Pricing, Journal, Company, Contact.
3. Tick **Primary Menu** under *Display location* and save.
4. Edit the header with Elementor, select the Nav Menu widget, open **Content → Menu**
   and pick `Primary`.

If you leave the menu selector empty, the widget shows Elementor's placeholder links —
which is what you see in the preview. Assign a menu for the real thing.

The mobile hamburger is part of the same Nav Menu widget: open
**Content → Layout** and confirm **Toggle** is set to *Hamburger*, and that
**Breakpoint** is *Mobile (767 px)* or *Tablet* depending on how early you want it.

---

## If your server cannot reach the internet

Some managed hosts block outbound HTTP, so Elementor cannot download the demo images.
You have two options:

1. **Upload the images first.** Take the seven JPEGs from `media/` and upload them to
   **Media → Add New**. Then, in the Elementor editor, replace each image using the
   *Choose Image* button. The placeholders give you the exact aspect ratio (3:2) and the
   correct framing, so swaps are quick.
2. **Ask your host** to allow outbound requests to `github.com` and
   `objects.githubusercontent.com`, then re-import.

Either way the layout is unaffected — every image sits inside an Image widget with a
radius and an object-fit already applied.

---

## Uninstalling

* **Templates:** `Templates → Saved Templates` → tick the templates → *Delete*.
* **Design system:** `Elementor → Site Settings` and change the colours/fonts back, or
  restore from the backup you took before importing.
* **Pages:** delete them like any other page. The imported images remain in the Media
  Library; delete them from there if you do not want them.
