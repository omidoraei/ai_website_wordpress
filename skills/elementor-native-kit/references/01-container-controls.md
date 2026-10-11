# 01 — Container controls

Provenance: `elementor/elementor@v3.35.9` and `@v4.0.8` — `includes/elements/container.php`
and `includes/controls/groups/{flex-container,flex-item,grid-container}.php`. Both tags are
byte-identical for these files (see `04-version-deltas.md`).

Ground rule: **container controls are unprefixed.** Widgets prefix theirs with `_`
(`02-widget-controls.md`). The two flex groups are the exception — they are registered on
containers under the short names `flex` and `_flex`, which is where the field prefix comes
from, not from a version.

---

## Where the flex fields come from

| Group class | Registered as | Line | Resulting field ids |
| --- | --- | --- | --- |
| `Group_Control_Flex_Container` | `flex` | `container.php:L507` | `flex_direction`, `flex_justify_content`, … |
| `Group_Control_Flex_Item` | `_flex` | `container.php:L1500` | `_flex_size`, `_flex_basis`, … |

## Flex container group — `includes/controls/groups/flex-container.php`

Every field below is `'responsive' => true`, so `_tablet` and `_mobile` variants are valid
for all of them.

| Line | Field id (prefixed) | Type | CSS var | Notes |
| --- | ---: | --- | --- | --- |
| 28 | `flex_direction` | CHOOSE | `--flex-direction` | `row`, `column`, `row-reverse`, `column-reverse`; gives Elementor's logical RTL flipping |
| 90 | `flex_justify_content` | CHOOSE | `--justify-content` | main axis |
| 127 | `flex_align_items` | CHOOSE | `--align-items` | cross axis |
| 155 | `flex_gap` | GAPS | `--gap` | value = `{row, column, unit}` — **not** a slider |
| 182 | `flex_wrap` | CHOOSE | `--flex-wrap` | `wrap` / `nowrap` / `wrap-reverse` |
| 203 | `flex_align_content` | CHOOSE | `--align-content` | only meaningful when wrapped |

### Grid variants

When `container_type` is `grid`, `Group_Control_Grid_Container` (`grid-container.php`, 10
fields) replaces the flex group and its fields are **unprefixed**: `grid_columns_grid`,
`grid_rows_grid`, `grid_auto_flow`, `grid_gap`, `grid_justify_items`, `grid_align_items`,
and their responsive variants. This kit uses flex only (rule 7), so none of these appear in
`templates/`.

## Flex item group — `includes/controls/groups/flex-item.php`

All responsive. This is the group the kit's per-breakpoint layout depends on.

| Line | Field id (prefixed `_flex_`) | Type | CSS var | Notes |
| --- | ---: | --- | --- | --- |
| 19 | `_flex_basis_type` | SELECT | — | `''` (Default) or `custom` |
| 29 | `_flex_basis` | SLIDER | `--flex-basis` | `condition: basis_type = custom`; units `px % em rem vw`; **renders as `flex-basis`, not `width`** |
| 50 | `_flex_align_self` | CHOOSE | `--align-self` | overrides the container's `align-items` |
| 79 | `_flex_order` | CHOOSE | `--order` | |
| 112 | `_flex_order_custom` | NUMBER | `--order` | `condition: order = custom` |
| 124 | `_flex_size` | CHOOSE | `--flex-grow` | `none` / `grow` / `shrink` / `custom` |
| 158 | `_flex_grow` | NUMBER | `--flex-grow` | `condition: size = custom` |
| 172 | `_flex_shrink` | NUMBER | `--flex-shrink` | `condition: size = custom` |

### Why this matters more than it looks

`_flex_basis` maps to `flex-basis`, so a "50 %" child in a `nowrap` or `wrap` row keeps
`flex-shrink: 1` unless `_flex_size` says otherwise. A card grid written as
`flex-basis: 31 %` **without** `_flex_size = none` can shrink unpredictably in a narrow
container. The kit therefore writes:

```json
"_flex_basis":      { "unit": "%", "size": 31 },
"_flex_basis_tablet": { "unit": "%", "size": 48 },
"_flex_basis_mobile": { "unit": "%", "size": 100 },
"_flex_basis_type": "custom"
```

Three explicit bases, one per breakpoint — this is rule 7, and
`tools/preview.py` emits the same three CSS values so preview and live site agree.

## Container's own controls — `includes/elements/container.php`

| Line | Control id | Notes |
| ---: | --- | --- |
| 372 | `container_type` | `flex` (default) / `grid` |
| 391 | `content_width` | `boxed` / `full` — **written before `boxed_width`** |
| 556 | `width` | custom width, `condition: content_width = full` |
| 589 | `boxed_width` | responsive slider; only applies when `content_width = boxed` |
| 598 | `min_height` | responsive slider |
| 610 | `overflow` | `default` / `hidden` |
| 664 | background group (`background_background`, `background_color`, …) | |
| 726 | `background_overlay` group | **containers only** — widgets have no overlay |
| 795 | `background_hover` group | |
| 834 | `border` group (`border_border`, `border_width`, `border_color`) | |
| 857 | `border_radius` | dimensions |
| 909 | `box_shadow` group | |
| 948 | `box_shadow_hover_box_shadow_type` | + `box_shadow_hover_box_shadow` |
| 971 | `border_hover` group | |
| 1012 | `background_overlay_hover` group | |
| 1049 | `css_filters` group | |
| 1068 | `css_filters_hover` group | |
| 1100 | `border_hover_transition` | |
| 1108 | `background_hover_transition` | |
| 1401 | `position` | `default` / `absolute` / `fixed` |
| 1499 | flex-item group (`_flex`) | see above |
| 1516 | `_offset_x` / `1517 _offset_y`? | only meaningful with `position` |
| 1531 | `z_index` | |
| 1556 | `_element_id` | CSS id |
| 1657 | `animation` | **unprefixed** — see `07-motion-effects.md` |
| 1767 | `animation_duration` | |
| 1785 | `animation_delay` | |

Line numbers above come from `references/_generated/control-index.md` (regenerate with
`scripts/extract_controls.py`); treat the generated file as authoritative if the two
disagree.

## Non-obvious behaviours

1. **`content_width` gates `boxed_width`.** Writing `boxed_width` without
   `content_width: "boxed"` silently does nothing. The kit's section pattern always sets
   `content_width` explicitly.
2. **Container padding/margin are plain groups** (`padding`, `margin`), unprefixed, with
   responsive variants — the same shape as widget `_padding` / `_margin`.
3. **Overlay is container-only.** `background_overlay_*` does not exist on widgets.
4. **`html_tag`** is on the container and is how this kit produces real landmark elements
   (`section`, `header`, `footer`, `main`) instead of nested `div`s (rule 6).
5. **Animation is unprefixed on containers** and `_animation` on widgets. Getting this
   backwards produces a dead setting, not an error.

## UNVERIFIED — do not emit

* **Responsive visibility.** The kit currently emits `hide_mobile` / `hide_tablet`
  (`"hidden-mobile"` / `"hidden-tablet"`) in 6 places. **No such control exists in
  `elementor/elementor@v3.35.9` or `@v4.0.8`** — `grep -rn "hide_mobile\|hidden-desktop"
  --include="*.php"` over both tags returns nothing, while the CSS classes
  (`elementor-hidden-desktop` etc.) do exist in
  `assets/dev/scss/frontend/_visibility.scss`. The class exists; the control that writes it
  does not appear in the free source. These 6 settings are recorded as a **defect** in
  `HANDOFF-P0.md` and are flagged by `scripts/audit_control_names.py`. Replacement strategy:
  restructure those elements so they do not need hiding (preferred), or hide them by hand in
  the Elementor panel and record it in `docs/capability-matrix.md`.
* `_element_custom_width` / `_element_width` on containers: the kit emits `_element_width`
  on containers in 167 places. It is confirmed as a **widget** control
  (`common-base.php:L335`); confirm container behaviour before relying on it.
