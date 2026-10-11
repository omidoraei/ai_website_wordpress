# Capability matrix

The contract for what this kit may emit, and what degrades. Rows = every widget, control
family and pattern the kit uses. **The Free/Pro column is evidence, not opinion**: "Free"
means the widget class exists in `elementor/elementor@v3.35.9` (public source, see
`skills/elementor-native-kit/references/_generated/widget-taxonomy.md`); "Pro" means the class
is absent there **and** Elementor Pro is closed source, so its control ids are never asserted.

Regenerate the evidence:

```bash
python3 skills/elementor-native-kit/scripts/extract_controls.py --source <checkout> --tag v3.35.9
python3 tools/verify.py --report
```

## Widgets

| Widget / pattern | Kit count | Tier | Version-safe | RTL-safe | Notes / Free fallback |
| --- | ---: | --- | --- | --- | --- |
| `heading` | 533 | **Free** | 3.35.9 = 4.0.8 (identical file) | ✅ logical by default | HTML tag via `header_size`; never a styled `div` |
| `text-editor` | 244 | **Free** | identical | ✅ | the only home for body copy |
| `icon` | 151 | **Free** | identical | ✅ decorative | `primary_color`/`secondary_color`; `icon_padding` is a **slider**, `border_width` a **dimension** |
| `divider` | 135 | **Free** | identical | ✅ | `style` is the live control; `separator_type` is `HIDDEN` |
| `button` | 94 | **Free** | identical | ✅ icon position mirrors | controls live in `traits/button-trait.php`; background group → `background_background` + `background_color` (**not** a 3.x/4.x split) |
| `icon-list` | 39 | **Free** | identical | ✅ | typography group is `icon` → `icon_typography_*` |
| `image` | 24 | **Free** | identical | ⚠️ never mirror Latin-text images | URLs under `tokens.ASSET_BASE`, 3:2, alt required |
| `counter` | 16 | **Free** | identical | ⚠️ Latin digits | typography groups `typography_number` / `typography_title` |
| `accordion` | 7 | **Free** | identical | ✅ | FAQ schema on; `title_html_tag` set |
| `social-icons` | 4 | **Free** | **only widget that differs 3.35.9→4.0.8** (a default value; no id change) | ✅ | group `image_border` |
| `spacer` | 2 | **Free** | — | ✅ | ⚠️ `spacer.php` indexed 0 controls → `space` is **UNVERIFIED** in this skill (extractor limitation, tracked in HANDOFF-P0) |
| `tabs`, `icon-box`, `testimonial`, `toggle`, `alert`, `rating`, `menu-anchor`, `video`, … | 0 | **Free** | — | ✅ | available if needed |
| `html` | 0 | **Free** | — | — | **FORBIDDEN** by rule 2; verifier fails the build if one appears |
| `form` | 8 | **Pro** | unknown (closed source) | ✅ | renders **nothing** on Free. Fallback: a form plugin's shortcode in a Text Editor, or accept inert blocks |
| `posts` | 1 | **Pro** | unknown | ✅ | renders nothing on Free; fallback: hand-built cards |
| `archive-posts` | 2 | **Pro** | unknown | ✅ | renders nothing on Free; archive becomes header-only |
| `nav-menu` | 2 | **Pro** | unknown | ✅ | Free has no menu widget; fallback: theme menu / third-party |
| `search-form` | 1 | **Pro** | unknown | ✅ | not in the free source at this tag |
| `breadcrumbs` | 8 | **Pro** | unknown | ⚠️ order handled by the plugin | harmless when empty |
| `post-info`, `post-navigation`, `author-box`, `post-comments` | 4 | **Pro** | unknown | ✅ | single-post degrades to title + content + featured image |
| `theme-site-logo`, `theme-site-title`, `theme-page-title`, `theme-archive-title`, `theme-post-*` | 12 | **Pro** | unknown | ⚠️ logos must not mirror | fallback: static Heading/Image |

## Non-widget capabilities

| Capability | Tier | Version-safe | RTL-safe | Notes / fallback |
| --- | --- | --- | --- | --- |
| Flexbox Containers (all 962 containers) | **Free**, behind an experiment | identical `container.php` | ✅ `flex_direction: row` flips logically | must be Active in `Settings → Features` |
| Global colors / fonts, Theme Style, Kit document | **Free** | `global-colors.php` / `global-typography.php` gained one `do_action` in 4.0.8; no control change | ✅ | `system_colors` = exactly 4 rows |
| Entrance animation (`animation` on containers, `_animation` on widgets) | **Free** | identical | ⚠️ use `fadeInUp`, not `fadeInLeft/Right` | the only animation mechanism |
| Responsive "Hide On" visibility (6 uses) | **Free** | identical | ✅ | `element-base.php:L1383` `add_hidden_device_controls()`; ids `hide_<device>`, value `hidden-<device>`, `prefix_class elementor-` |
| Per-breakpoint layout (`_flex_basis_tablet/_mobile`) | **Free** | identical `flex-item.php` | ✅ | rule 7 |
| **Theme Builder assignment** (header, footer, single, archive, search, 404) | **Pro** | — | ✅ | templates ship; assignment is a documented manual step |
| **Exit-intent popup** | **Pro** | — | ✅ | layout ships; trigger is manual |
| **Sticky** header | **Pro** | Free shows `sticky_pro` promotion lock | ✅ | **no `sticky*` key is emitted anywhere** |
| Scrolling / mouse / transform Motion Effects | **Pro** | `scrolling_effects_pro`, `mouse_effects_pro` locks | ✅ | never emitted |
| **Custom Fonts** (needed for Arad) | **Pro** | — | ✅ | without it, substitute a Google-hosted Persian family |
| Form actions (Mailchimp, webhook, …) | **Pro** | — | ✅ | documented manual step |
| Page settings (`hide_title`, `template`) | **Free** | — | ✅ | per-page manual step, not baked into templates |

## Unverifiable surface (never emitted)

| Item | Why not emitted |
| --- | --- |
| Every Pro widget control id (`form_*`, `nav_menu_*`, `post_*`, `theme_*`, `breadcrumbs_*`) | Pro is closed source; no public evidence available |
| `motion_fx_*`, `sticky*` | Pro, unverifiable |
| Elementor 4.x `variables` / `classes` / atomic-widget controls | not analysed in this phase |
| `spacer.space` | extractor indexed 0 controls for `spacer.php`; unproven here |
| `hide_*` **on widgets** (non-container elements) | verified only for containers via `element-base.php:L1383`; the kit's 6 uses are container-level |

## How a row changes

1. Add/alter the evidence: re-run `extract_controls.py` against a pinned tag.
2. Update this row with the file:line.
3. Re-run `python3 tools/verify.py` — it must exit 0.
4. If the row is Pro, state the Free fallback in the same commit.
