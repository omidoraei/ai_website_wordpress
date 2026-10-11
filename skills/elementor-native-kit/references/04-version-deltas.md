# 04 — Version deltas (Elementor 3.x vs 4.x)

Method: the pinned 3.x tip and the pinned 4.x tag were extracted side by side and the
files this kit depends on were diffed directly. Every claim below is a `diff` result, not a
recollection.

```bash
curl -sL -o el3.tar.gz https://codeload.github.com/elementor/elementor/tar.gz/refs/tags/v3.35.9
curl -sL -o el4.tar.gz https://codeload.github.com/elementor/elementor/tar.gz/refs/tags/v4.0.8
tar xzf el3.tar.gz && tar xzf el4.tar.gz
diff -rq elementor-3.35.9/includes/widgets elementor-4.0.8/includes/widgets
```

## Headline result: the kit's control surface does not drift

| Path | v3.35.9 vs v4.0.8 |
| --- | --- |
| `includes/controls/groups/` (all 12 group classes) | **identical** (0 differing entries) |
| `includes/elements/` (`container.php`, `section.php`, `column.php`, `repeater.php`) | **identical** |
| `includes/base/` (`element-base.php`, `controls-stack.php`, `widget-base.php`) | **identical** |
| `includes/widgets/` (35 classes) | 1 differing entry: `social-icons.php` |
| `core/kits/documents/tabs/` (13 files) | 2 differing: `global-colors.php`, `global-typography.php` |
| `includes/widgets/traits/button-trait.php` | **identical** |
| `includes/widgets/{heading,image,icon,icon-box,icon-list,counter,divider,tabs,accordion,testimonial,social-icons}.php` | **identical** |

## The three real deltas

### 1. `social-icons.php`

The only widget delta. A default value string changed; **no control id was added, removed or
renamed** (the diff introduces no new `'...'` key outside a `'value'` default). Safe.

### 2. `global-colors.php` / `global-typography.php` (+2 lines each)

```diff
134a135,136
> 		do_action( 'elementor/kit/global-colors/register_controls', $this );
```

A new extensibility hook. No control added, removed or renamed. Safe for the kit document.

### 3. That is the whole delta for the paths this kit emits

`includes/controls/groups/*`, `includes/elements/*` and `includes/base/*` — where every
container, flex, background, border, typography and motion control lives — are byte-identical
between the two tags.

## Refuted claim (correction of an earlier assertion)

An earlier change note in this repo claimed:

> "buttons write both the 3.x `background_color` and the 4.x `background_background` keys so
>  the hover state survives on either line"

**That is wrong, and this file corrects it.** There is no 3.x/4.x split here:

* `includes/widgets/traits/button-trait.php` is identical across the two tags.
* The button's Style → Background is `Group_Control_Background::get_type()` registered with
  `'name' => 'background'` at `includes/widgets/traits/button-trait.php:L355–357`.
* A group registered as `background` whose type-switcher field is `background`
  (`includes/controls/groups/background.php:L153`) produces exactly two ids:
  **`background_background`** (the switcher) and **`background_color`** (the colour).
  Both keys are correct on both lines; writing "one for 3.x and one for 4.x" was a
  misreading of the same group.
* The hover group is `button_background_hover` (`button-trait.php:L408`), so its keys are
  `button_background_hover_background` and `button_background_hover_color` — again identical
  on both lines.

Kit consequence: emit **both** keys because that is what Elementor itself stores (switcher +
value), **not** because of version differences. Any note claiming a 3.x/4.x dual-write
requirement for these controls should be treated as unverified.

## Asymmetries that are real (and are NOT version deltas)

These exist in **both** lines — they are architectural, and they are the ones that actually
bite:

| Asymmetry | Container id | Widget id | Source |
| --- | --- | --- | --- |
| Entrance animation | `animation` | `_animation` | `container.php` vs `common-base.php:L838` |
| Duration | `animation_duration` | `animation_duration` | same |
| Delay | `animation_delay` | `animation_delay` | same |
| Grid placement | `grid_column`, `grid_row` | `_grid_column`, `_grid_row` | container grid group vs `common-base.php:L387` |
| Flex child | group `flex-item` registered as `_flex` | group `flex-item` registered as `_flex` | both use the same group |
| Border radius | `border_radius` (container style group) | `_border_radius` on widgets | container border group vs `common-base.php` |

Rule of thumb this skill encodes: **container controls are unprefixed, widget controls are
prefixed with `_`**, except where a group is deliberately registered with an `_` name
(`_flex`, `_background`, `_border` on widgets).

## Verification recipe for a new tag

```bash
for f in includes/controls/groups incl:cludes/elements includes/base core/kits/documents/tabs; do
  diff -rq elementor-<old>/$f elementor-<new>/$f
done
```

If `includes/controls/groups/` or `includes/elements/container.php` shows changes, re-run
`scripts/extract_controls.py` and re-run `tools/verify.py` **before** trusting any existing
template, because container and flex controls are the backbone of all 962 containers.

## UNVERIFIED — do not emit

* Any control that exists **only** in Elementor 4.x's atomic/experimental widget system.
  This kit targets the classic widget + container API shared by 3.16+ and 4.x; the atomic
  system was not analysed and no atomic control id is emitted.
* Elementor 4.x "variables" and "classes" kit settings: no public source was diffed for
  their runtime behaviour, so the kit document declares neither (see `03-kit-site-settings.md`).
