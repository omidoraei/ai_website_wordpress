# 07 — FAQ & troubleshooting

## General questions

**Do I need Elementor Pro?**
For all nine pages and all 22 blocks: no. For the header, footer, single-post, archive,
search and popup templates: yes — *assigning* a Theme Builder document is a Pro feature.
You also need Pro for the Forms, Nav Menu, Posts, Archive Posts and the dynamic post
widgets. On Free, those widgets simply render nothing, so a page still looks correct, it
just has no form and no post loop.

**Will it work with my theme?**
Yes. Set every page's layout to **Elementor Full Width** and the Theme Builder header and
footer take over the top and bottom of the page. Any theme that declares WordPress theme
supports correctly will work; page templates control the rest. If your theme adds a sidebar,
set the page template to **Elementor Full Width** (not *Default*) to remove it.

**Can I use it with WooCommerce?**
Yes. The design system is global, so WooCommerce blocks, the cart and checkout inherit your
colours and fonts as soon as they are set in Site Settings. Build product pages with a
**Single Product** Theme Builder document and reuse the card recipe from
`Block | Feature Grid - Six icon cards` as your product card.

**Can I use it with Gutenberg blocks?**
Yes — Elementor and Gutenberg coexist. A `.e-con` container carries its own styles, so
mixing a block-built page with an Elementor-built page is fine. Just don't put a Gutenberg
block *inside* an Elementor container; use an Elementor widget instead.

**Is anything hard-coded in HTML?**
No. There is no HTML widget, no `<style>` block, no `functions.php` snippet and no custom
CSS anywhere in the 40 documents. Text lives in Heading and Text Editor widgets, buttons in
Button widgets, images in Image widgets, and every other value is a standard Elementor
control.

**Is there any JavaScript?**
Only what Elementor itself ships (the accordion, tabs, sticky, motion effects and nav menu
behaviours). The kit adds none.

---

## Import problems

### “Invalid file” or the import silently does nothing

* Import **`dist/aurora-ai-templates.zip`** through **Templates → Saved Templates → Import
  Templates**. The kit archive (`dist/aurora-ai-kit.zip`) is a *different* format and is
  only accepted by **Elementor → Tools → Import / Export Kit**.
* Both zips contain JSON only and are well under the upload limit. If your host caps
  uploads very low, import the individual files from `templates/` instead — each one is a
  standalone Elementor document.

### “The package could not be installed. No valid templates found.”

Your Elementor version is older than the kit's document format, or the archive was
re-zipped by an operating system that added a `__MACOSX` folder. Download the zip directly
from `dist/` (do not un-zip and re-zip it) and try again on Elementor 3.16+.

### The design system did not apply

That is the **kit** archive, not the templates archive — import it under
**Elementor → Tools → Import / Export Kit → Import Kit**. On versions without that screen,
apply the values manually from
[02-design-system.md](02-design-system.md#applying-the-globals-by-hand).

Remember that on an existing site, custom colours are **appended**, not replaced. If your
palette now has duplicates, open **Site Settings → Global Colors** and delete the rows you
do not want.

### Images imported but look wrong, or did not import at all

* Elementor downloads the images over HTTP during import. If your host blocks outbound
  requests to `github.com`, the image widgets keep their remote URL and the pictures will
  still load in the browser (your server is not the one fetching them) — but the files are
  not in your Media Library. Upload the JPEGs from `media/` manually if you need local
  copies.
* If an image looks stretched, check **Image → Style → Object Fit** on that widget. The kit
  sets `cover` on card and hero media, `default` elsewhere.

---

## Editor problems

### Everything is stacked in one column

Flexbox Containers are not active. Go to **Elementor → Settings → Features**, set
**Flexbox Container** to *Active*, then reload the editor. All 962 containers in the kit
depend on it.

### My text edits look like they are being ignored

Elements are bound to a **global typography style**. Editing the *Content* tab changes the
words; editing *Style → Typography* overrides the family, size and weight for that one
element. If you want the change everywhere, edit the global style in
**Site Settings → Global Fonts** instead — that is what makes the kit consistent.

### The mobile version looks like a squeezed desktop version

It should not. Every grid in the kit sets explicit **tablet and mobile flex-basis** values,
so a 3-column grid becomes 2 columns at 1024 px and 1 column at 767 px. To verify: open the
editor, switch to the **Mobile** preview at the bottom, select the grid container and look
at **Layout → Gaps** and the flex-item **Size → Custom Width** fields. Each of them shows a
value per device; the desktop value is only a placeholder when you are on mobile.

### My Persian text overflows its box

The `FA / …` global styles already loosen line-height to 1.5–2.0 em. If a specific card
still overflows: select it, open **Style → Border** and give the container a little more
bottom padding, or reduce the heading's global size. Avoid negative letter-spacing on
Persian text — it breaks the joins between letters.

### The sticky header overlaps my content

Select the header shell → **Advanced → Motion Effects → Sticky** and increase
**Sticky Effects Offset** (currently 60). If the overlap is on a page with an anchor link,
move the anchor with a **Menu Anchor** widget a little higher up the page.

### The counter shows the wrong number

Counters animate to **Content → Ending Number**. The four statistics in
`Block | Stats Band - Dark counters` use a suffix instead of huge numbers
(`380` + `M`) so the digits stay readable at every screen width. Change the number or the
suffix freely; both are plain fields.

---

## Theme Builder problems

### The header and footer do not show up

Four common causes, in order of likelihood:

1. **No condition set.** Open `Templates → Theme Builder`, click the header document and
   set the condition to **Entire Site**. A document with no condition renders nowhere.
2. **The document is not published.** Drafts are not applied.
3. **The page layout is not Full Width.** Open the page → **Settings → Page Layout** →
   *Elementor Full Width*.
4. **Your theme hard-codes its own header.** Switch to Hello Elementor, or remove the
   theme's `get_header()` call — the latter needs code, which is why Hello is the standard
   recommendation for Elementor sites.

### The mobile hamburger does not open

Select the Nav Menu widget → **Content → Layout** and confirm **Toggle** is *Hamburger* and
the **Breakpoint** matches the width you are testing. If you set the breakpoint to *Mobile*
and test at 800 px, the desktop menu is intentionally still showing.

### The Nav Menu shows placeholder links

The widget has no menu assigned. **Appearance → Menus** → create a menu → tick a display
location → then in the editor set **Content → Menu** to that menu.

### Conditions conflict between the English and Persian headers

Give the **Persian** header an explicit **Include → Pages** list of only the Persian pages
and leave the English header on **Entire Site**. Specific includes beat the catch-all, so
the Persian pages pick up the Persian header and everything else falls through to English.

---

## Delivery questions

**Can I hand this to a client as a Kit Library file?**
Yes. `dist/aurora-ai-kit.zip` follows the Elementor Export Kit archive layout
(`manifest.json` + `site-settings.json` + `templates-source/`). The manifest declares only
what the archive really contains — global colours, global fonts, theme styles and general
settings — so the import reports clean results with no skipped files.

**Can I sell or redistribute the templates?**
Yes, under the MIT licence in [`LICENSE`](../LICENSE). Replace the demo imagery and the
placeholder copy first, and note that **Arad is not bundled** — it is a licensed commercial
typeface, so ship only a licence you hold.

**How do I regenerate the kit after editing `tokens.py`?**

```bash
python3 tools/build.py     # rewrites templates/, dist/ and templates/INDEX.md
python3 tools/preview.py   # optional: rewrites preview/*.html
```

`tools/build.py --check` validates without writing: unique element ids, known widget
types, explicit `isInner` on every container, and no `null` settings.

**Does the build touch WordPress?**
No. It only writes JSON and zip files. Nothing runs on your server, and nothing is
installed by the build.
