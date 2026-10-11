"""
Aurora AI - reusable Elementor component builders.

Every function returns a native Elementor container tree made only from
Elementor widgets. Components compose into sections (sections.py) and sections
into pages (pages.py); the same builders generate both the page layouts and the
standalone reusable "block" templates, so a duplicated block is identical to the
one used on the pages.

Rule enforced throughout: only controls that exist in Elementor are written.
  * widgets      -> includes/widgets/*.php
  * containers   -> includes/elements/container.php
  * flex grid    -> includes/controls/groups/flex-item.php  (group name "_flex")
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from . import tokens as tk
from .dsl import (
    Doc, accordion, button, container, counter, divider, heading, icon, icon_box,
    icon_list, image, inner, section, social_icons, spacer, tabs_widget, text,
    testimonial, widget, dims, gap, link, slider, typo, icon_val, post_info,
)

# ---------------------------------------------------------------------------
# Grid maths
#
# Equal columns are produced with flex-basis + flex-grow (both real Elementor
# controls from Group_Control_Flex_Item registered as `_flex`):
#     _flex_basis_type = custom -> --flex-basis
#     _flex_size       = grow   -> --flex-grow:1; --flex-shrink:0
# basis is the only knob needed for responsive column counts.
# ---------------------------------------------------------------------------

BASIS = {
    1: {"d": 100, "t": 100, "m": 100},
    2: {"d": 48, "t": 48, "m": 100},
    3: {"d": 31, "t": 48, "m": 100},
    4: {"d": 23, "t": 48, "m": 100},
    5: {"d": 18, "t": 31, "m": 100},
    6: {"d": 15, "t": 31, "m": 100},
}


def flex_item(n: int = 0, *, basis=None, tablet_basis=None, mobile_basis: Optional[int] = None,
              grow: int = 1, shrink: int = 1, align_self: Optional[str] = None,
              order: Optional[str] = None, order_mobile: Optional[int] = None,
              grow_mobile: Optional[int] = None, plain: bool = False) -> Dict[str, Any]:
    """Return `flex_item={...}` kwargs for container().

    n = desktop column count; explicit basis values win over the scheme table.
    `plain=True` returns natural sizing (auto basis, no grow) for flex rows
    whose children should keep their intrinsic width.
    """
    out: Dict[str, Any] = {}
    if plain:
        if align_self:
            out["_flex_align_self"] = align_self
        return {"flex_item": out}

    scheme = BASIS.get(n, BASIS[3]) if n else None
    d = basis if basis is not None else (scheme["d"] if scheme else None)
    t = tablet_basis if tablet_basis is not None else (scheme["t"] if scheme else d)
    m = mobile_basis if mobile_basis is not None else (scheme["m"] if scheme else 100)

    out["_flex_size"] = "custom"
    out["_flex_grow"] = grow
    out["_flex_shrink"] = shrink
    if d is not None:
        out["_flex_basis_type"] = "custom"
        out["_flex_basis"] = slider(d, "%")
    if t is not None:
        out["_flex_basis_type_tablet"] = "custom"
        out["_flex_basis_tablet"] = slider(t, "%")
    if m is not None:
        out["_flex_basis_type_mobile"] = "custom"
        out["_flex_basis_mobile"] = slider(m, "%")
    if grow_mobile is not None:
        out["_flex_grow_mobile"] = grow_mobile
    if align_self:
        out["_flex_align_self"] = align_self
    if order:
        out["_flex_order"] = order
    if order_mobile is not None:
        out["_flex_order_mobile"] = order_mobile
    return {"flex_item": out}


def grid(doc: Doc, cards: Sequence[Dict[str, Any]], *, cols: int = 3, gap_value: int = 28,
         gap_tablet: Optional[int] = None, gap_mobile: int = 22, align: str = "stretch",
         justify: str = "flex-start", extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """A wrapping flex row: `cards` are laid out `cols` per row on desktop."""
    return inner(
        doc, list(cards), direction="row", wrap="wrap", justify=justify, align=align,
        extra={
            "flex_gap": gap(gap_value),
            "flex_gap_tablet": gap(gap_tablet if gap_tablet is not None else gap_value),
            "flex_gap_mobile": gap(gap_mobile),
            **(extra or {}),
        },
    )


def flexrow(doc: Doc, children: Sequence[Dict[str, Any]], *, gap_value: int = 20,
            align: str = "center", justify: str = "flex-start", wrap: str = "wrap",
            extra: Optional[Dict[str, Any]] = None, **kw: Any) -> Dict[str, Any]:
    return inner(doc, list(children), direction="row", wrap=wrap, align=align, justify=justify,
                 gap_v=gap_value, extra=extra, **kw)


def flexcol(doc: Doc, children: Sequence[Dict[str, Any]], *, gap_value: int = 18,
            align: str = "flex-start", justify: Optional[str] = None,
            extra: Optional[Dict[str, Any]] = None, **kw: Any) -> Dict[str, Any]:
    return inner(doc, list(children), direction="column", align=align, justify=justify,
                 gap_v=gap_value, extra=extra, **kw)


# ---------------------------------------------------------------------------
# Surfaces
# ---------------------------------------------------------------------------

SURFACE = {
    "card": dict(
        background={"background_background": "classic", "background_color": tk.G["white"]},
        border={"border_border": "solid", "border_width": dims(1), "border_color": tk.G["line"]},
        radius=tk.RADIUS["lg"],
    ),
    "card_warm": dict(
        background={"background_background": "classic", "background_color": tk.G["sand_50"]},
        border={"border_border": "solid", "border_width": dims(1), "border_color": tk.G["line"]},
        radius=tk.RADIUS["lg"],
    ),
    "card_flat": dict(
        background={"background_background": "classic", "background_color": tk.G["sand_100"]},
        border={},
        radius=tk.RADIUS["lg"],
    ),
    "card_dark": dict(
        background={"background_background": "classic", "background_color": tk.G["ink_900"]},
        border={"border_border": "solid", "border_width": dims(1),
                "border_color": "rgba(255,255,255,0.10)"},
        radius=tk.RADIUS["lg"],
    ),
    "plain": dict(background={"background_background": "none"}, border={}, radius=None),
}


def surface(doc: Doc, children: Sequence[Dict[str, Any]], *, kind: str = "card",
            pad: Any = 34, pad_tablet: Optional[Any] = None, pad_mobile: Any = 24,
            shadow: Optional[str] = None, hover: bool = False, radius: Any = None,
            background: Optional[Dict[str, Any]] = None, border: Optional[Dict[str, Any]] = None,
            animation: Optional[str] = None, animation_delay: Optional[int] = None,
            extra: Optional[Dict[str, Any]] = None, **kw: Any) -> Dict[str, Any]:
    """Surface container. `background` / `border` override the named style."""
    style = dict(SURFACE[kind])
    if background is not None:
        style["background"] = background
    if border is not None:
        style["border"] = border
    merged: Dict[str, Any] = {
        "padding": dims(pad),
        "padding_tablet": dims(pad_tablet if pad_tablet is not None else pad),
        "padding_mobile": dims(pad_mobile),
    }
    if hover:
        merged.update({
            "border_hover_border": "solid",
            "border_hover_color": tk.G["primary"],
            "background_hover_transition": slider(0.3, "s"),
            "border_hover_transition": slider(0.3, "s"),
            "box_shadow_hover_box_shadow_type": "yes",
            "box_shadow_hover_box_shadow": tk.SHADOW["md"],
        })
    merged.update(extra or {})
    return container(doc, children, is_inner=True, shadow=shadow,
                     background=style["background"], border=style["border"],
                     radius=radius if radius is not None else style["radius"],
                     animation=animation, animation_delay=animation_delay,
                     extra=merged, **kw)


# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------

def eyebrow_row(doc: Doc, value: str, *, align: str = "center", color: Optional[str] = None,
                rule: bool = True, fa: bool = False) -> Dict[str, Any]:
    color = color or tk.G["amber_600"]
    items: List[Dict[str, Any]] = []
    if rule:
        items.append(widget(doc, "divider", {
            "style": "solid", "weight": slider(2), "color": color,
            "width": slider(26), "gap": slider(0),
        }))
    items.append(heading(doc, value, tag="p",
                         global_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                         color=color,
                         settings={"_element_width": "initial"},
                         letter_spacing=slider(0) if fa else None))
    justify = {"center": "center", "left": "flex-start", "right": "flex-end"}.get(align, "center")
    return flexrow(doc, items, gap_value=12, justify=justify, wrap="nowrap",
                   extra={"_element_width": "100%"} if align == "center" else None)


def section_head(doc: Doc, *, eyebrow: Optional[str] = None, title: str = "", lead: str = "",
                 align: str = "center", title_tag: str = "h2", title_style: Optional[str] = None,
                 lead_style: Optional[str] = None, title_color: Optional[str] = None,
                 lead_color: Optional[str] = None, fa: bool = False,
                 max_width: Optional[int] = 780, animation: str = "fadeInUp",
                 eyebrow_color: Optional[str] = None) -> Dict[str, Any]:
    children: List[Dict[str, Any]] = []
    if eyebrow:
        children.append(eyebrow_row(doc, eyebrow, align=align, fa=fa, color=eyebrow_color))
    if title:
        children.append(heading(
            doc, title, tag=title_tag,
            global_style=title_style or (tk.T["fa_heading"] if fa else tk.T["h2"]),
            color=title_color, align=align,
            animation=animation, delay=80))
    if lead:
        children.append(text(
            doc, "<p>%s</p>" % lead,
            global_style=lead_style or (tk.T["fa_body"] if fa else tk.T["lead"]),
            color=lead_color or tk.G["text"], align=align,
            animation=animation, delay=160))
    extra: Dict[str, Any] = {}
    if max_width:
        extra["boxed_width"] = slider(max_width)
        extra["boxed_width_mobile"] = slider(max_width)
    align_flex = {"center": "center", "left": "flex-start", "right": "flex-end"}.get(align, "center")
    return flexcol(doc, children, gap_value=18, align=align_flex, extra=extra)


def badge(doc: Doc, value: str, *, color: Optional[str] = None, bg: Optional[str] = None,
          icon_value: Optional[str] = None, fa: bool = False) -> Dict[str, Any]:
    kids: List[Dict[str, Any]] = []
    if icon_value:
        kids.append(icon(doc, icon_value, view="default", size=13, padding=0,
                         primary=color or tk.G["amber_600"]))
    kids.append(heading(doc, value, tag="span",
                        global_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                        color=color or tk.G["amber_600"],
                        letter_spacing=slider(0.8) if not fa else slider(0)))
    return flexrow(doc, kids, gap_value=8, wrap="nowrap",
                   extra={
                       "background_background": "classic",
                       "background_color": bg or tk.G["amber_100"],
                       "border_radius": dims(tk.RADIUS["pill"]),
                       "padding": dims(7, 16), "padding_mobile": dims(6, 13),
                       "_element_width": "initial",
                   })


def feature_pill(doc: Doc, value: str, *, fa: bool = False) -> Dict[str, Any]:
    return flexrow(doc, [
        icon(doc, "fas fa-check", view="default", size=13, padding=0, primary=tk.G["success"]),
        heading(doc, value, tag="span",
                global_style=tk.T["fa_label"] if fa else tk.T["text"],
                color=tk.G["secondary"], letter_spacing=slider(0)),
    ], gap_value=9, wrap="nowrap")


def icon_tile(doc: Doc, value: str, *, library: str = "fa-solid", size: int = 22,
              padding: int = 16, bg: Optional[str] = None, color: Optional[str] = None,
              radius: int = tk.RADIUS["md"], hover: bool = True) -> Dict[str, Any]:
    extra: Dict[str, Any] = {
        "padding": dims(padding),
        "_element_width": "initial",
        "_element_custom_width": slider(56),
    }
    if hover:
        extra.update({
            "background_hover_background": "classic",
            "background_hover_color": tk.G["amber_100"],
            "background_hover_transition": slider(0.25, "s"),
        })
    return flexrow(doc, [
        icon(doc, value, library=library, view="default", size=size, padding=0,
             primary=color or tk.G["amber_600"]),
    ], gap_value=0, align="center", justify="center", wrap="nowrap",
        extra={
            "background_background": "classic",
            "background_color": bg or tk.G["sand_100"],
            "border_radius": dims(radius),
            **extra,
        })


def arrow_link(doc: Doc, value: str, url: str, *, color: Optional[str] = None,
               fa: bool = False, hover: Optional[str] = None, align: Optional[str] = None) -> Dict[str, Any]:
    return button(doc, value, url, variant="link", size="sm",
                  icon="fas fa-arrow-right", icon_align="right", icon_indent=9,
                  padding=dims(0), radius=dims(0), align=align,
                  button_text_color=color or tk.G["secondary"],
                  hover_color=hover or tk.G["amber_600"],
                  background_color="rgba(255,255,255,0)",
                  background_background="classic",
                  button_background_hover_color="rgba(255,255,255,0)",
                  typography_typography=tk.T["fa_label"] if fa else tk.T["accent"])


def tag_pill(doc: Doc, value: str, *, fa: bool = False, bg: Optional[str] = None,
             color: Optional[str] = None) -> Dict[str, Any]:
    return flexrow(doc, [
        heading(doc, value, tag="span",
                global_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                color=color or tk.G["amber_600"],
                letter_spacing=slider(0.8) if not fa else slider(0)),
    ], gap_value=0, wrap="nowrap",
        extra={
            "background_background": "classic",
            "background_color": bg or tk.G["amber_100"],
            "border_radius": dims(tk.RADIUS["pill"]),
            "padding": dims(6, 14),
            "_element_width": "initial",
        })


# ---------------------------------------------------------------------------
# Composite cards
# ---------------------------------------------------------------------------

def icon_card(doc: Doc, *, icon_value: str, title: str, body: str,
              link_url: Optional[str] = None, link_text: str = "Learn more",
              delay: int = 0, fa: bool = False, kind: str = "card",
              pad: Any = 32) -> Dict[str, Any]:
    kids: List[Dict[str, Any]] = [
        icon_tile(doc, icon_value),
        heading(doc, title, tag="h3",
                global_style=tk.T["fa_heading"] if fa else tk.T["h3"],
                color=tk.G["secondary"]),
        text(doc, "<p>%s</p>" % body,
             global_style=tk.T["fa_body"] if fa else tk.T["text"],
             color=tk.G["text"]),
    ]
    if link_url:
        kids.append(arrow_link(doc, link_text, link_url, fa=fa))
    return surface(doc, kids, kind=kind, pad=pad, pad_mobile=24, hover=True,
                   animation="fadeInUp", animation_delay=delay, extra={"flex_direction": "column"},
                   **flex_item(1, basis=100, tablet_basis=100, mobile_basis=100, grow=0))


def bullet_card(doc: Doc, *, icon_value: str, title: str, body: str,
                bullets: Sequence[str] = (), link_url: Optional[str] = None,
                link_text: str = "Learn more", dark: bool = False, fa: bool = False,
                delay: int = 0, col_kw: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    kids: List[Dict[str, Any]] = [
        icon_tile(doc, icon_value,
                  bg=tk.G["ink_800"] if dark else tk.G["sand_100"],
                  color=tk.G["primary"]),
        heading(doc, title, tag="h3",
                global_style=tk.T["fa_heading"] if fa else tk.T["h3"],
                color=tk.G["white"] if dark else tk.G["secondary"]),
        text(doc, "<p>%s</p>" % body,
             global_style=tk.T["fa_body"] if fa else tk.T["text"],
             color=tk.G["muted_dark"] if dark else tk.G["text"]),
    ]
    if bullets:
        kids.append(icon_list(
            doc, [{"text": b, "icon": "fas fa-check"} for b in bullets],
            space=11, icon_size=15, icon_color=tk.G["primary"],
            text_color=tk.G["muted_dark"] if dark else tk.G["text"],
            style=tk.T["fa_body"] if fa else tk.T["text"],
            typography_font_size=slider(16)))
    if link_url:
        kids.append(arrow_link(doc, link_text, link_url,
                               color=tk.G["primary"] if dark else tk.G["secondary"], fa=fa))
    return surface(doc, kids, kind="card_dark" if dark else "card", pad=34, pad_mobile=26,
                   hover=True, animation="fadeInUp", animation_delay=delay,
                   extra={"flex_direction": "column"}, **(col_kw or {}))


def step_card(doc: Doc, index: str, title: str, body: str, *, delay: int = 0,
              fa: bool = False) -> Dict[str, Any]:
    return flexcol(doc, [
        flexrow(doc, [
            heading(doc, index, tag="span", global_style=tk.T["eyebrow"],
                    color=tk.G["amber_600"], letter_spacing=slider(0),
                    settings={"_element_width": "100%"}),
        ], gap_value=0, align="center", justify="center", wrap="nowrap",
            extra={
                "background_background": "classic",
                "background_color": tk.G["amber_100"],
                "border_radius": dims(tk.RADIUS["pill"]),
                "padding": dims(10, 0),
                "_element_width": "initial",
                "_element_custom_width": slider(46),
            }),
        heading(doc, title, tag="h3",
                global_style=tk.T["fa_heading"] if fa else tk.T["h3"],
                color=tk.G["secondary"]),
        text(doc, "<p>%s</p>" % body,
             global_style=tk.T["fa_body"] if fa else tk.T["text"],
             color=tk.G["text"], typography_font_size=slider(16)),
    ], gap_value=16, align="flex-start", animation="fadeInUp", animation_delay=delay,
        **flex_item(4))


def stat_block(doc: Doc, ending: int, label: str, *, suffix: str = "", prefix: str = "",
               dark: bool = False, fa: bool = False, delay: int = 0,
               decimals: Optional[int] = None) -> Dict[str, Any]:
    return flexcol(doc, [
        counter(doc, ending, label, prefix=prefix, suffix=suffix,
                number_color=tk.G["primary"],
                title_color=tk.G["muted_dark"] if dark else tk.G["muted"],
                number_style=tk.T["stat"],
                title_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                title_tag="p", align="left"),
    ], gap_value=6, align="flex-start", animation="fadeInUp", animation_delay=delay,
        **flex_item(4))


def case_card(doc: Doc, *, image_key: str, alt: str, tag: str, title: str, metric: str,
              metric_label: str, link_url: str = "#", delay: int = 0, fa: bool = False,
              link_text: str = "View case study", col_kw: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    kids: List[Dict[str, Any]] = [
        image(doc, tk.img_url(image_key), alt=alt, size="large", width=100, width_unit="%",
              radius=tk.RADIUS["md"], object_fit="cover"),
        tag_pill(doc, tag, fa=fa),
        heading(doc, title, tag="h3",
                global_style=tk.T["fa_heading"] if fa else tk.T["h3"],
                color=tk.G["secondary"]),
        flexrow(doc, [
            heading(doc, metric, tag="span", global_style=tk.T["h3"],
                    color=tk.G["accent"], letter_spacing=slider(-0.4),
                    settings={"_element_width": "initial"}),
            text(doc, "<p>%s</p>" % metric_label, global_style=tk.T["text"],
                 color=tk.G["muted"], typography_font_size=slider(15),
                 settings={"_element_width": "initial"}),
        ], gap_value=10, align="center"),
        arrow_link(doc, link_text, link_url, fa=fa),
    ]
    return surface(doc, kids, kind="card", pad=18, pad_mobile=16, hover=True, gap_v=16,
                   shadow="xs", animation="fadeInUp", animation_delay=delay,
                   extra={"flex_direction": "column"}, **(col_kw or {}))


def quote_card(doc: Doc, *, quote: str, name: str, role: str, delay: int = 0,
               fa: bool = False, dark: bool = False,
               col_kw: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return surface(doc, [
        icon(doc, "fas fa-quote-left", view="default", size=26, padding=0, primary=tk.G["primary"]),
        text(doc, "<p>%s</p>" % quote,
             global_style=tk.T["fa_body"] if fa else tk.T["text"],
             color=tk.G["muted_dark"] if dark else tk.G["text"],
             typography_font_size=slider(18), typography_line_height=slider(1.75, "em")),
        divider(doc, color="rgba(255,255,255,0.14)" if dark else tk.G["line"], width=100,
                weight=1, gap=0, _element_width="100%"),
        flexcol(doc, [
            heading(doc, name, tag="p", global_style=tk.T["h3"],
                    color=tk.G["white"] if dark else tk.G["secondary"],
                    letter_spacing=slider(-0.2)),
            text(doc, "<p>%s</p>" % role, global_style=tk.T["text"],
                 color=tk.G["muted_dark"] if dark else tk.G["muted"],
                 typography_font_size=slider(15)),
        ], gap_value=2),
    ], kind="card_dark" if dark else "card", pad=32, pad_mobile=24, gap_v=20, hover=True,
        animation="fadeInUp", animation_delay=delay,
        extra={"flex_direction": "column"}, **(col_kw or {}))


def pricing_card(doc: Doc, *, plan: str, price: str, period: str, blurb: str,
                 features: Sequence[str], cta: str = "Start free trial", cta_url: str = "#",
                 featured: bool = False, badge_text: str = "Most popular",
                 note: str = "", delay: int = 0, fa: bool = False) -> Dict[str, Any]:
    dark = featured
    kids: List[Dict[str, Any]] = []
    head: List[Dict[str, Any]] = [
        heading(doc, plan, tag="p", global_style=tk.T["eyebrow"],
                color=tk.G["primary"] if dark else tk.G["amber_600"],
                letter_spacing=slider(1.4) if not fa else slider(0),
                settings={"_element_width": "initial"}),
    ]
    if featured and badge_text:
        head.append(tag_pill(doc, badge_text, bg=tk.G["primary"], color=tk.G["ink_900"], fa=fa))
    kids.append(flexrow(doc, head, gap_value=12, justify="space-between"))
    kids.append(flexrow(doc, [
        heading(doc, price, tag="span", global_style=tk.T["display"],
                color=tk.G["white"] if dark else tk.G["secondary"],
                font_size=slider(46), font_size_mobile=slider(36),
                settings={"_element_width": "initial"}),
        text(doc, "<p>%s</p>" % period, global_style=tk.T["text"],
             color=tk.G["muted_dark"] if dark else tk.G["muted"],
             typography_font_size=slider(16),
             settings={"_element_width": "initial", "_margin": dims(8, 0, 0, 0)}),
    ], gap_value=10, align="flex-end"))
    kids.append(text(doc, "<p>%s</p>" % blurb, global_style=tk.T["text"],
                     color=tk.G["muted_dark"] if dark else tk.G["text"]))
    kids.append(divider(doc, color="rgba(255,255,255,0.14)" if dark else tk.G["line"],
                        width=100, weight=1, gap=0, _element_width="100%"))
    kids.append(icon_list(
        doc, [{"text": f, "icon": "fas fa-check"} for f in features],
        space=12, icon_size=15, icon_color=tk.G["primary"],
        text_color=tk.G["muted_dark"] if dark else tk.G["text"],
        style=tk.T["fa_body"] if fa else tk.T["text"],
        typography_font_size=slider(16)))
    kids.append(button(doc, cta, cta_url, variant="primary" if dark else "dark",
                       size="md", align="center", hover_animation="grow",
                       _element_width="100%", _element_custom_width=slider(100, "%")))
    if note:
        kids.append(text(doc, "<p>%s</p>" % note, global_style=tk.T["text"],
                         color=tk.G["muted_dark"] if dark else tk.G["muted"], align="center",
                         typography_font_size=slider(14)))

    return surface(doc, kids, kind="card_dark" if dark else "card",
                   pad=36 if dark else 32, pad_mobile=26, hover=not dark, gap_v=20,
                   shadow="lg" if dark else None,
                   animation="fadeInUp", animation_delay=delay,
                   extra={"flex_direction": "column"}, **flex_item(3))


def link_column(doc: Doc, title: str, items: Sequence[Dict[str, str]], *, fa: bool = False,
                col_kw: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return flexcol(doc, [
        heading(doc, title, tag="h3", global_style=tk.T["eyebrow"],
                color=tk.G["white"], letter_spacing=slider(1.2) if not fa else slider(0)),
        icon_list(doc, [{"text": i["text"], "icon": "fas fa-minus",
                         "link": i.get("url", "#")} for i in items],
                  space=13, icon_size=13, icon_color="rgba(244,166,42,0.65)",
                  indent=12, text_color=tk.G["muted_dark"],
                  style=tk.T["fa_body"] if fa else tk.T["text"],
                  typography_font_size=slider(16),
                  text_color_hover=tk.G["primary"]),
    ], gap_value=20, **(col_kw or {}))


def contact_line(doc: Doc, icon_value: str, label: str, value: str, url: str = "",
                 *, dark: bool = True, fa: bool = False) -> Dict[str, Any]:
    return flexrow(doc, [
        icon(doc, icon_value, view="default", size=17, padding=0, primary=tk.G["primary"]),
        flexcol(doc, [
            heading(doc, label, tag="p", global_style=tk.T["eyebrow"],
                    color=tk.G["muted_dark"], letter_spacing=slider(1.1) if not fa else slider(0),
                    typography_font_size=slider(12)),
            heading(doc, value, tag="p", global_style=tk.T["text"],
                    color=tk.G["white"] if dark else tk.G["secondary"],
                    letter_spacing=slider(0), link_url=url or None),
        ], gap_value=3),
    ], gap_value=14, align="flex-start", wrap="nowrap")


# ---------------------------------------------------------------------------
# Footer helpers
# ---------------------------------------------------------------------------

def brand_block(doc: Doc, *, fa: bool = False, text_value: str = "") -> Dict[str, Any]:
    return flexcol(doc, [
        heading(doc, tk.BRAND if not fa else tk.BRAND_FA, tag="p", global_style=tk.T["h3"],
                color=tk.G["white"]),
        text(doc, "<p>%s</p>" % (text_value or tk.TAGLINE),
             global_style=tk.T["fa_body"] if fa else tk.T["text"],
             color=tk.G["muted_dark"], typography_font_size=slider(16)),
        social_icons(doc, [
            {"icon": "fab fa-linkedin-in", "url": "#"},
            {"icon": "fab fa-x-twitter", "url": "#", "library": "fa-brands"},
            {"icon": "fab fa-github", "url": "#"},
            {"icon": "fab fa-youtube", "url": "#"},
        ], shape="circle", size="sm", padding=11, spacing=10, icon_size=15,
            icon_primary_color=tk.G["ink_800"], icon_secondary_color=tk.G["white"],
            hover_primary_color=tk.G["primary"], hover_secondary_color=tk.G["ink_900"],
            border_radius=dims(tk.RADIUS["pill"])),
    ], gap_value=18)
