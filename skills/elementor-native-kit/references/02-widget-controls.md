# 02 — Widget controls

Provenance: `elementor/elementor@v3.35.9` (= `@v4.0.8`, identical for every widget below
except `social-icons.php`, see `04-version-deltas.md`). Line numbers are from
`references/_generated/control-index.md`, which is machine-written by
`scripts/extract_controls.py`. The generated file is authoritative; this page is the curated
subset the kit actually uses.

**These are the 16 Free widget types the kit emits. Pro widget control ids are *not* in this
file** — see `05-pro-vs-free.md` for why and what happens instead.

---

## Naming rules (the part that causes dead settings)

| Rule | Example |
| --- | --- |
| A widget's own control id is written verbatim | `title`, `editor`, `ending_number` |
| A **group** control's ids are `<group name>_<field>` | group `typography` + field `font_size` → `typography_font_size` |
| The group's own selector field is also prefixed | group `typography` + field `typography` → `typography_typography` (this holds the `globals/typography?id=…` reference) |
| Responsive controls take `_tablet` / `_mobile` suffixes | `typography_font_size_mobile` |
| Base controls are shared by every widget and start with `_` | `_margin`, `_padding`, `_element_width`, `_animation` |

### Group-typography names differ per widget (get this wrong and the size never applies)

| Widget | Group names | Resulting keys |
| --- | --- | --- |
| heading, text-editor, button, image (caption) | `typography` | `typography_*` |
| icon-list | `icon` (`includes/widgets/icon-list.php`) | `icon_typography_typography`, `icon_typography_font_size` |
| counter | `typography_number`, `typography_title` | `typography_number_font_size`, `typography_title_font_size` |
| icon-box | `title`, `description` | `title_typography_*`, `description_typography_*` |
| accordion | `title`, `content` | `title_typography_*`, `content_typography_*` |
| tabs | `tab`, `content` | `tab_typography_*`, `content_typography_*` |
| testimonial | `content`, `name`, `job` | `content_typography_*`, `name_typography_*`, `job_typography_*` |

---

## The kit's widget set, with verified control ids

### `heading` — `includes/widgets/heading.php`

| Line | Control | Type | Notes |
| ---: | --- | --- | --- |
| 181 | `title` | TEXTAREA | the visible text |
| 197 | `link` | URL | wraps the heading in an `<a>` |
| 211 | `size` | SELECT | **visual size preset**, not the tag |
| 231 | `header_size` | SELECT | **HTML tag** (`h1`…`h6`, `div`, `span`, `p`) — rule 6 uses this |
| 299 | `typography` group | TYPOGRAPHY | `typography_typography` holds the global reference |
| 352 | `separator` | DIVIDER | UI separator only, no output |
| 368 | `title_color` | COLOR | |
| 391 | `title_hover_color` | COLOR | only meaningful with `link` |

### `text-editor` — `includes/widgets/text-editor.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 137 | `editor` | WYSIWYG; the only place body copy should live |
| 146 | `drop_cap` | switcher |
| 290 | `typography` group | |
| 345 | `text_color` | |
| 360 | `link_color` | |
| 380 | `link_hover_color` | |

### `button` — `includes/widgets/button.php` + `includes/widgets/traits/button-trait.php`

`button.php` registers 0 content controls — everything lives in the trait. This is why a
naive per-file extraction reports the button as empty.

| Trait line | Control | Notes |
| ---: | --- | --- |
| — | `text`, `link`, `size`, `align`, `selected_icon`, `icon_align`, `icon_indent` | content tab |
| 355–357 | group `background` | → `background_background` (switcher) + `background_color` |
| 408 | group `button_background_hover` | → `button_background_hover_background` + `button_background_hover_color` |
| — | `typography` group, `button_text_color`, `hover_color`, `border_radius`, `text_padding` | style tab |

Correction recorded in `04-version-deltas.md`: the two background keys are **not** a 3.x/4.x
split; they are the switcher and its value, identical on both lines.

### `icon` — `includes/widgets/icon.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 115 | `selected_icon` | ICONS; value + `library` |
| 128 | `view` | default / stacked / framed |
| 143 | `shape` | circle / square (with view) |
| 161 | `link` | |
| 222 / 239 | `primary_color`, `secondary_color` | icon colour / background or border |
| 265 / 279 | `hover_primary_color`, `hover_secondary_color` | |
| 345 | `icon_padding` | **SLIDER** — with `view: framed` it sets the box size |
| 394 | `border_width` | **DIMENSIONS** — same name, different shape per widget; a shape-agnostic checker must accept both (this is why `tools/verify.py` accepts either) |

### `icon-list` — `includes/widgets/icon-list.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 114 | `view` | |
| 139 | `text` | repeater item field |
| 153 | `selected_icon` | repeater item field |
| 166 | `link` | repeater item field |
| 177 | `icon_list` | REPEATER (items carry the three fields above) |
| 284 | `divider` | switcher |
| 434 | `icon_color` | |

### `counter` — `includes/widgets/counter.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 140 | `ending_number` | digits are Latin (see `06-rtl-persian.md` §4) |
| 152 / 167 | `prefix` / `suffix` | use these for `380` + `M` |
| 182 | `duration` | ms |
| 222 | `title` | label |
| 496 | `number_color` | |
| 510 | `typography_number` group | → `typography_number_*` |
| 550 | `title_color`, + `typography_title` group | → `typography_title_*` |

### `divider` — `includes/widgets/divider.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 382 | `style` | the visible style selector |
| 396 | `separator_type` | **type HIDDEN** — a legacy/mirror control; writing it is harmless but pointless |
| 493 | `look` | line / line_text / line_icon / … |
| 520 / 558 | `text` / `icon` | with `look` |
| 586 | `color` | |
| 602 | `weight` | **SLIDER** (thickness) |
| 730 | `text_color`, 744 `typography` group | |

### `image` — `includes/widgets/image.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 130 | `image` | MEDIA — the control the kit's `tokens.IMAGES` URLs land in |
| 155 | `caption_source` | none / attachment / custom |
| 189 | `link_to` | none / file / custom |
| 206 | `link` | |
| 443 | `opacity` | |
| — | `image_border_radius`, `width`, `object_fit`, `align`, `hover_animation` | style tab |

### `social-icons` — `includes/widgets/social-icons.php`

The only widget that differs between v3.35.9 and v4.0.8, and the diff changes **no control
id** (a default `'value'` string).

| Line | Control | Notes |
| ---: | --- | --- |
| 247 | `social_icon_list` | REPEATER; items carry `social_icon` (L113), `link` (L191), `item_icon_color` (L205), `item_icon_primary_color` (L218), `item_icon_secondary_color` (L232) |
| 277 | `shape` | |
| 368 / 382 | `icon_primary_color`, `icon_secondary_color` | |
| 494 | `image_border` group | → `image_border_border`, `image_border_width`, `image_border_color` |

### `accordion` — `includes/widgets/accordion.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 162 | `tabs` | REPEATER; items carry `tab_title` (L129), `tab_content` (L142) |
| 182 / 210 | `selected_icon`, `selected_active_icon` | |
| 240 | `title_html_tag` | tag for the question — set it, do not leave a `div` |
| 259 | `faq_schema` | switcher — the kit turns FAQ schema **on** |
| 278 / 300 | `border_width`, `border_color` | |
| 334 / 349 | `title_color`, `tab_active_color` | |
| 364 | `title_typography` group | → `title_typography_*` |

### `tabs` — `includes/widgets/tabs.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 161 | `tabs` | REPEATER; `tab_title` (L124), `tab_content` (L138) |
| 181 | `type` | horizontal / vertical |
| 203 | `tabs_align_horizontal` | |
| 393 | `tab_typography` group | → `tab_typography_*` |

### `testimonial` — `includes/widgets/testimonial.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 136 | `testimonial_content` | |
| 149 | `testimonial_image` | MEDIA |
| 171 / 186 | `testimonial_name`, `testimonial_job` | |
| 201 | `link` | |
| 296 | `content_typography` group | → `content_typography_*` |
| 394 | `name_typography` group | → `name_typography_*` |

### `icon-box` — `includes/widgets/icon-box.php`

`selected_icon` (114), `view` (127), `shape` (145), `title_text` (164), `description_text`
(178), `link` (192), `primary_color` (419), `secondary_color` (435), and — note the naming —
group `title` and group `description`, i.e. `title_typography_*` / `description_typography_*`.

---

## Base controls shared by every widget — `includes/widgets/common-base.php`

| Line | Control | Notes |
| ---: | --- | --- |
| 335 | `_element_width` | `initial` / `100%` / custom |
| 387 | `_grid_column` | responsive |
| 838 | `_animation` | **the widget animation id has an underscore** (rule 8) |
| 308 / 320 | `_margin` / `_padding` | responsive dimensions |
| — | `_element_id`, `_css_classes`, `_z_index`, `_position` | advanced |

Groups on every widget: `_background`, `_background_hover`, `_border`, `_border_hover`,
`_box_shadow`, `_box_shadow_hover`, `_css_filters`, and the `_flex` flex-item group.

---

## UNVERIFIED — do not emit

* **`spacer`.** `spacer.php` indexed **0 controls**, yet the kit emits `space` on 2 Spacer
  widgets. The control is real in Elementor's UI, so this is an **extractor limitation**, not
  proof the key is wrong — but this skill may not claim a verified line for it. See the
  residue list in `HANDOFF-P0.md`.
* **Pro widget control ids** (`form`, `posts`, `archive-posts`, `nav-menu`, `breadcrumbs`,
  `post-*`, `theme-*`, `author-box`, `search-form`): closed source, no public evidence. The
  templates do contain structural keys for some of them; they are recorded for re-verification
  and are inert-if-wrong rather than fatal (`05-pro-vs-free.md`).
* **`menu-anchor`** and the remaining Free widgets the kit does not use: indexed, but not
  curated here — read `references/_generated/control-index.md` if you need them.
