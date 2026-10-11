# 07 — Motion Effects

Motion Effects are Elementor's own entrance animations. They are the **only** animation
mechanism this kit may use (SKILL.md rule 8). No AOS, GSAP, ScrollTrigger, Lottie or
hand-written `@keyframes`.

Provenance: `elementor/elementor@v3.35.9` and `@v4.0.8` (identical, see
`04-version-deltas.md`).

---

## The two control names (this asymmetry is the #1 source of dead settings)

| Element | Control id | Where | Notes |
| --- | --- | --- | --- |
| **Container** | `animation` | `includes/elements/container.php` | **unprefixed** |
| **Widget** (any) | `_animation` | `includes/widgets/common-base.php:L838` | **prefixed with `_`** |

Consequences:

* A widget animated with `animation` gets nothing — the setting is stored and ignored.
* A container animated with `_animation` likewise does nothing.
* The kit writes `animation` for containers and `_animation` for widgets; `tools/preview.py`
  mirrors this exact rule so a mistake shows up in the preview, not only on the live site.

## Delay and duration

| Element | Duration | Delay |
| --- | --- | --- |
| Container | `animation_duration` | `animation_delay` |
| Widget | `animation_duration` | `animation_delay` |

Both are milliseconds, integer. There is no `_animation_delay` and no
`animation_delay_duration`; do not emit them.

## The closed set of entrance values

| Value | Movement |
| --- | --- |
| `fadeIn` | opacity only |
| `fadeInUp` | opacity + 20 px rise |
| `fadeInDown` | opacity + 20 px drop |
| `fadeInLeft` | opacity + slide from left |
| `fadeInRight` | opacity + slide from right |
| `fadeInUpBig` / `fadeInDownBig` / `fadeInLeftBig` / `fadeInRightBig` | larger travel |
| `zoomIn` / `zoomOut` | scale |
| `bounceIn`, `bounceInUp/Down/Left/Right` | bounce |
| `slideInUp/Down/Left/Right` | slide |
| `rotateIn`, `rotateInDownLeft/Right`, `rotateInUpLeft/Right` | rotate |
| `lightSpeedIn`, `rollIn` | novelty |

The list is generated, not recalled: read the `animation` options block in
`includes/widgets/common-base.php` (widgets) and `includes/elements/container.php`
(containers) at the pinned tag. Use `references/_generated/control-index.md` to confirm the
control exists before emitting it.

**RTL caveat.** `fadeInLeft` / `fadeInRight` are physical, not logical: in an RTL document a
"from the left" entrance reads as coming from the *trailing* edge. Use `fadeInUp` for FA
documents — that is why the FA templates only ever use `fadeInUp`.

## Stagger convention used by this kit

| Position in a row/grid | Delay |
| --- | --- |
| 1st | 0 ms |
| 2nd | 80–110 ms |
| 3rd | 160–220 ms |
| 4th | 240–330 ms |

Rules:

* Never exceed ~600 ms total; longer sequences feel broken on mobile.
* Only animate **above-the-fold or early** content. Off-screen animation delays perceived
  performance for no benefit (see `06-performance-accessibility.md` in the kit docs).
* Never animate `height`, `width`, `margin`, `padding`, `top/left` — Cumulative Layout Shift.
  The entrance values above only touch `opacity` and `transform`, which are composited.
* Respect reduced motion by **omitting** the animation rather than animating faster: if a
  block is important enough to need reveal, it is important enough to be visible without it.

## What NOT to emit here

| Not Motion Effects | Belongs to |
| --- | --- |
| `hover_animation` | the widget's own Style → Hover tab (a different control, valid on widgets) |
| `background_hover_transition` | widget/container Style → Background hover transition |
| `motion_fx_*` (mouse/scroll effects) | Elementor **Pro** — see `05-pro-vs-free.md` |
| `sticky`, `sticky_on`, `sticky_offset`, `sticky_effects_offset` | Elementor **Pro** motion effect |

## UNVERIFIED — do not emit

* `motion_fx_scrolling` / `motion_fx_mouse` / `motion_fx_transform_*` and every other
  `motion_fx_*` key: these are Elementor **Pro** controls and Elementor Pro is closed source.
  No public source was available to confirm their ids at this tag, so this skill never emits
  them. If a scroll/mouse effect is required, add it by hand in the Elementor panel and
  record it in `docs/capability-matrix.md`.
* `sticky*` keys: same reason. The header's sticky behaviour is documented as a manual
  Pro step in the kit's `docs/05-theme-builder.md`, not written into the template JSON.
