"""
Aurora AI - Elementor JSON DSL.

A tiny, explicit builder that emits *native Elementor element trees*. Nothing
here bypasses Elementor: every helper maps 1:1 onto a real Elementor control.

Control names below were verified against Elementor source
(includes/elements/container.php, includes/widgets/*.php,
includes/controls/groups/flex-container.php, core/kits/documents/tabs/*.php),
so nothing lands in the template that the editor cannot render.

Compatibility notes baked into this DSL
---------------------------------------
* Containers  : flex_direction / flex_wrap / flex_justify_content /
                flex_align_items / flex_align_content / flex_gap (+ _tablet/_mobile)
                -> Group_Control_Flex_Container registered as `flex`,
                   prefix rule = args['name'] . '_' . field  (base.php:180)
* Container entrance animation uses `animation` / `animation_duration` /
  `animation_delay` (container.php:1826) while widgets use `_animation` /
  `animation_duration` / `_animation_delay` (common-base.php:852).
* Button background is written as BOTH `background_color` (3.x plain control and
  4.x group field) and `background_background: classic` (4.x group selector),
  because the 4.x group defaults `background` to 'classic' but 3.x ignores the
  extra key. Same trick for the hover state.
* Global references: colors -> globals/colors?id=<id>,
  typography -> globals/typography?id=<id>.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Iterable, List, Optional, Sequence

from . import tokens as tk

__all__ = [
    "Doc", "container", "section", "widget", "inner",
    "heading", "text", "button", "image", "icon", "icon_box", "icon_list",
    "counter", "testimonial", "accordion", "tabs_widget", "social_icons",
    "divider", "spacer", "menu_anchor", "nav_menu", "site_logo", "search_form",
    "theme_site_title", "form", "posts", "archive_posts", "post_title",
    "post_content", "post_excerpt", "featured_image", "author_box",
    "post_comments", "post_navigation", "breadcrumbs", "theme_page_title",
    "dims", "gap", "slider", "typo", "link", "icon_val",
]

# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

Number = int


class Doc:
    """Owns a single Elementor document (page/header/footer/block) and hands
    out deterministic, unique 7-char element ids."""

    def __init__(self, slug: str, title: str, doc_type: str = "page"):
        self.slug = slug
        self.title = title
        self.type = doc_type
        self._n = 0

    def uid(self) -> str:
        self._n += 1
        raw = "%s::%d" % (self.slug, self._n)
        return hashlib.md5(raw.encode("utf-8")).hexdigest()[:7]

    def next_id(self) -> str:
        return self.uid()


def dims(top: Any, right: Any = None, bottom: Any = None, left: Any = None, unit: str = "px") -> Dict[str, Any]:
    """Elementor DIMENSIONS control value."""
    if right is None:
        right = top
    if bottom is None:
        bottom = top
    if left is None:
        left = right
    return {
        "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
        "unit": unit, "isLinked": (top == right == bottom == left),
    }


def gap(row: Any, column: Any = None, unit: str = "px", linked: bool = True) -> Dict[str, Any]:
    """Elementor GAPS control value (used by flex_gap and space_between_widgets)."""
    if column is None:
        column = row
    return {"row": str(row), "column": str(column), "unit": unit, "isLinked": linked}


def slider(size: Any, unit: str = "px") -> Dict[str, Any]:
    """Elementor SLIDER control value."""
    return {"unit": unit, "size": size}


def link(url: str, new_tab: bool = False, nofollow: bool = False) -> Dict[str, str]:
    return {
        "url": url,
        "is_external": "on" if new_tab else "",
        "nofollow": "on" if nofollow else "",
    }


def icon_val(value: str, library: str = "fa-solid") -> Dict[str, str]:
    return {"value": value, "library": library}


def group_typo(global_style: Optional[str] = None, **overrides: Any) -> Dict[str, Any]:
    """Un-prefixed Group_Control_Typography field values.

    Field names come from includes/controls/groups/typography.php: the global
    selector is called `typography`, the rest are `font_size`, `font_weight`,
    `line_height`, `letter_spacing`, `text_transform`, ...
    """
    out: Dict[str, Any] = {"typography": global_style or "custom"}
    out.update({k: v for k, v in overrides.items() if v is not None})
    return out


def prefixed(group_name: str, global_style: Optional[str] = None, **overrides: Any) -> Dict[str, Any]:
    """Emit `<group>_<field>` keys for a typography group with a custom name.

    Elementor prefixes every group-control field with the group name, so the
    Counter widget ("typography_number") stores `typography_number_font_size`.
    """
    return {"%s_%s" % (group_name, k): v for k, v in group_typo(global_style, **overrides).items()}


def typo(global_style: Optional[str] = None, **overrides: Any) -> Dict[str, Any]:
    """Typography settings for widgets whose group is named `typography`."""
    return prefixed("typography", global_style, **overrides)


def _el(el_type: str, el_id: str, settings: Dict[str, Any], elements: Optional[list] = None,
        widget_type: Optional[str] = None, is_inner: Optional[bool] = None) -> Dict[str, Any]:
    node: Dict[str, Any] = {
        "id": el_id,
        "elType": el_type,
        "settings": settings,
        "elements": elements or [],
        "isInner": False if (is_inner is None and el_type == "container") else (is_inner or False),
    }
    if is_inner is None:
        node.pop("isInner")
        if el_type == "container":
            node["isInner"] = False
    if widget_type:
        node["widgetType"] = widget_type
    return node


def widget(doc: Doc, widget_type: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": doc.uid(),
        "elType": "widget",
        "settings": settings,
        "elements": [],
        "widgetType": widget_type,
    }


def container(
    doc: Doc,
    children: Sequence[Dict[str, Any]] = (),
    *,
    is_inner: bool = False,
    direction: Optional[str] = None,
    wrap: Optional[str] = None,
    justify: Optional[str] = None,
    align: Optional[str] = None,
    align_content: Optional[str] = None,
    gap_v: Any = None,
    gap_unit: str = "px",
    width: Optional[str] = None,
    boxed_width: Any = None,
    min_height: Any = None,
    min_height_unit: str = "px",
    html_tag: Optional[str] = None,
    background: Optional[Dict[str, Any]] = None,
    border: Optional[Dict[str, Any]] = None,
    radius: Any = None,
    shadow: Optional[str] = None,
    padding: Optional[Dict[str, Any]] = None,
    margin: Optional[Dict[str, Any]] = None,
    element_id: Optional[str] = None,
    css_classes: Optional[str] = None,
    animation: Optional[str] = None,
    animation_delay: Optional[int] = None,
    animation_duration: Optional[str] = None,
    overflow: Optional[str] = None,
    z_index: Optional[int] = None,
    sticky: Optional[str] = None,
    sticky_offset: Optional[int] = None,
    sticky_effects_offset: Optional[int] = None,
    sticky_on: Optional[Sequence[str]] = None,
    link_url: Optional[str] = None,
    flex_item: Optional[Dict[str, Any]] = None,
    target_device: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """A Flexbox Container (`elType: container`).

    `target_device` prefixes responsive keys with `_tablet` / `_mobile` so a
    second container call can supply device-specific layout values.
    """
    s: Dict[str, Any] = {}
    dev = "" if target_device is None else "_%s" % target_device

    if direction:
        s["flex_direction%s" % dev] = direction
    if wrap:
        s["flex_wrap%s" % dev] = wrap
    if justify:
        s["flex_justify_content%s" % dev] = justify
    if align:
        s["flex_align_items%s" % dev] = align
    if align_content:
        s["flex_align_content%s" % dev] = align_content
    if gap_v is not None:
        s["flex_gap%s" % dev] = gap(gap_v, unit=gap_unit)
    if width:
        s["content_width"] = width
        if width == "full":
            s["width"] = slider(100, "%")
    if boxed_width is not None:
        s["boxed_width%s" % dev] = slider(boxed_width)
    if min_height is not None:
        s["min_height%s" % dev] = slider(min_height, min_height_unit)
    if overflow:
        s["overflow"] = overflow
    if html_tag:
        s["html_tag"] = html_tag
    if padding is not None:
        s["padding%s" % dev] = padding
    if margin is not None:
        s["margin%s" % dev] = margin
    if background:
        s.update(background)
    if border:
        s.update(border)
    if radius is not None:
        if isinstance(radius, dict):
            s["border_radius"] = radius
        else:
            s["border_radius"] = dims(radius, unit="px")
    if shadow:
        s["box_shadow_box_shadow_type"] = "yes"
        s["box_shadow_box_shadow"] = tk.SHADOW[shadow]
    if z_index is not None:
        s["z_index"] = z_index
    if element_id:
        s["_element_id"] = element_id
    if css_classes:
        s["css_classes"] = css_classes
    if animation:
        s["animation%s" % dev] = animation
        if animation_duration:
            s["animation_duration"] = animation_duration
        if animation_delay:
            # NOTE: container animation_delay is NOT responsive / not prefixed
            s["animation_delay"] = animation_delay
    if sticky:
        s["sticky"] = sticky
        s["sticky_on"] = list(sticky_on or ["desktop", "tablet", "mobile"])
        if sticky_offset is not None:
            s["sticky_offset"] = sticky_offset
        if sticky_effects_offset is not None:
            s["sticky_effects_offset"] = sticky_effects_offset
    if link_url:
        s["link"] = link(link_url)
    if flex_item:
        s.update(flex_item)
    if extra:
        s.update(extra)

    return {
        "id": doc.uid(),
        "elType": "container",
        "settings": s,
        "elements": list(children),
        "isInner": bool(is_inner),
    }


def inner(doc: Doc, children: Sequence[Dict[str, Any]] = (), **kw: Any) -> Dict[str, Any]:
    kw["is_inner"] = True
    return container(doc, children, **kw)


def section(doc: Doc, children: Sequence[Dict[str, Any]] = (), *, pad_y=None, pad_x=None,
            background=None, element_id=None, **kw: Any) -> Dict[str, Any]:
    """Top level <section> container with the kit's responsive vertical rhythm.

    pad_y / pad_x are (desktop, tablet, mobile) tuples; Elementor responsive
    controls are written as `padding`, `padding_tablet`, `padding_mobile`, which
    this helper expands automatically.
    """
    pad_y = pad_y or tk.SECTION_PAD_Y
    pad_x = pad_x or tk.SECTION_PAD_X
    base = dims(pad_y[0], pad_x[0], pad_y[0], pad_x[0])
    tab = dims(pad_y[1], pad_x[1])
    mob = dims(pad_y[2], pad_x[2])

    kw.setdefault("width", "full")
    settings_extra = dict(kw.pop("extra", {}) or {})
    settings_extra["padding"] = base
    settings_extra["padding_tablet"] = tab
    settings_extra["padding_mobile"] = mob

    node = container(doc, children, background=background, element_id=element_id,
                     html_tag=kw.pop("html_tag", "section"), extra=settings_extra, **kw)
    return node


# ---------------------------------------------------------------------------
# Widget helpers  (free widgets first, then Elementor Pro)
# ---------------------------------------------------------------------------

def _base(**kw: Any) -> Dict[str, Any]:
    """Strip None values so we never write empty settings into the template."""
    return {k: v for k, v in kw.items() if v is not None}


def _anim(animation=None, delay=None, duration=None, dev=None) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if animation:
        key = "_animation" if not dev else "_animation_%s" % dev
        out[key] = animation
        if duration:
            out["animation_duration"] = duration
        if delay:
            out["_animation_delay"] = delay
    return out


def heading(doc: Doc, title: str, *, tag: str = "h2", global_style: Optional[str] = None,
            color: Optional[str] = None, align: Optional[str] = None, align_mobile: Optional[str] = None,
            animation: Optional[str] = None, delay: Optional[int] = None,
            duration: Optional[str] = None, element_id: Optional[str] = None,
            css_classes: Optional[str] = None, margin: Optional[Dict[str, Any]] = None,
            link_url: Optional[str] = None, settings: Optional[Dict[str, Any]] = None,
            **overrides: Any) -> Dict[str, Any]:
    """Heading widget. Keyword args become `typography_*` overrides; pass
    `settings={...}` for any other raw Elementor control."""
    s = _base(
        title=title,
        header_size=tag,
        title_color=color,
        align=align,
        align_mobile=align_mobile,
        _element_id=element_id,
        _css_classes=css_classes,
        _margin=margin,
        link=link(link_url) if link_url else None,
    )
    s.update(typo(global_style, **overrides))
    s.update(_anim(animation, delay, duration))
    s.update({k: v for k, v in (settings or {}).items() if v is not None})
    return widget(doc, "heading", s)


def text(doc: Doc, editor: str, *, global_style: Optional[str] = None, color: Optional[str] = None,
         align: Optional[str] = None, align_mobile: Optional[str] = None, animation: Optional[str] = None,
         delay: Optional[int] = None, duration: Optional[str] = None, margin: Optional[Dict[str, Any]] = None,
         css_classes: Optional[str] = None, link_color: Optional[str] = None,
         settings: Optional[Dict[str, Any]] = None, **overrides: Any) -> Dict[str, Any]:
    """Text Editor widget. `settings={...}` takes raw Elementor controls."""
    s = _base(
        editor=editor,
        text_color=color,
        align=align,
        align_mobile=align_mobile,
        _margin=margin,
        _css_classes=css_classes,
        link_color=link_color,
    )
    s.update(typo(global_style, **overrides))
    s.update(_anim(animation, delay, duration))
    s.update({k: v for k, v in (settings or {}).items() if v is not None})
    return widget(doc, "text-editor", s)


BTN = {
    "primary": dict(
        button_text_color=tk.G["ink_900"],
        background_background="classic",
        background_color=tk.G["primary"],
        hover_color=tk.G["ink_900"],
        button_background_hover_background="classic",
        button_background_hover_color=tk.G["amber_600"],
        box_shadow_box_shadow_type=None,
    ),
    "dark": dict(
        button_text_color=tk.G["white"],
        background_background="classic",
        background_color=tk.G["ink_900"],
        hover_color=tk.G["white"],
        button_background_hover_background="classic",
        button_background_hover_color=tk.G["ink_800"],
    ),
    "outline": dict(
        button_text_color=tk.G["secondary"],
        background_background="classic",
        background_color="rgba(255,255,255,0)",
        border_border="solid",
        border_width=dims(1),
        border_color=tk.G["line"],
        hover_color=tk.G["secondary"],
        button_background_hover_background="classic",
        button_background_hover_color=tk.G["sand_100"],
        button_hover_border_color=tk.G["secondary"],
    ),
    "outline_light": dict(
        button_text_color=tk.G["white"],
        background_background="classic",
        background_color="rgba(255,255,255,0)",
        border_border="solid",
        border_width=dims(1),
        border_color="rgba(255,255,255,0.35)",
        hover_color=tk.G["ink_900"],
        button_background_hover_background="classic",
        button_background_hover_color=tk.G["white"],
        button_hover_border_color=tk.G["white"],
    ),
    "light": dict(
        button_text_color=tk.G["ink_900"],
        background_background="classic",
        background_color=tk.G["white"],
        hover_color=tk.G["ink_900"],
        button_background_hover_background="classic",
        button_background_hover_color=tk.G["sand_200"],
    ),
    "coral": dict(
        button_text_color=tk.G["white"],
        background_background="classic",
        background_color=tk.G["accent"],
        hover_color=tk.G["white"],
        button_background_hover_background="classic",
        button_background_hover_color=tk.G["coral_600"],
    ),
    "ghost": dict(
        button_text_color=tk.G["secondary"],
        background_background="classic",
        background_color="rgba(255,255,255,0)",
        hover_color=tk.G["amber_600"],
        button_background_hover_background="classic",
        button_background_hover_color="rgba(255,255,255,0)",
    ),
    "link": dict(
        button_text_color=tk.G["secondary"],
        background_background="classic",
        background_color="rgba(255,255,255,0)",
        hover_color=tk.G["amber_600"],
        button_background_hover_background="classic",
        button_background_hover_color="rgba(255,255,255,0)",
    ),
}


def button(doc: Doc, text_value: str, url: str = "#", *, variant: str = "primary",
           size: str = "md", align: Optional[str] = None, align_mobile: Optional[str] = None,
           icon: Optional[str] = None, icon_library: str = "fa-solid", icon_align: str = "right",
           icon_indent: int = 10, full_width: bool = False, new_tab: bool = False,
           radius: Any = None, padding: Optional[Dict[str, Any]] = None,
           hover_animation: Optional[str] = None, animation: Optional[str] = None,
           delay: Optional[int] = None, css_id: Optional[str] = None,
           element_id: Optional[str] = None, css_classes: Optional[str] = None,
           margin: Optional[Dict[str, Any]] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        text=text_value,
        link=link(url, new_tab),
        size=size,
        align=align,
        align_mobile=align_mobile,
        button_css_id=css_id,
        _element_id=element_id,
        _css_classes=css_classes,
        _margin=margin,
        selected_icon=icon_val(icon, icon_library) if icon else None,
        icon_align=icon_align if icon else None,
        icon_indent=slider(icon_indent) if icon else None,
        hover_animation=hover_animation,
    )
    s.update({k: v for k, v in BTN[variant].items() if v is not None})
    if radius is not None:
        s["border_radius"] = radius if isinstance(radius, dict) else dims(radius)
    if padding is not None:
        s["text_padding"] = padding
    if full_width:
        s["_element_width"] = "100%"
        s["_element_custom_width"] = slider(100, "%")
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "button", s)


def image(doc: Doc, url: str, *, alt: str = "", size: str = "large", width: Any = None,
          width_unit: str = "px", max_width: Any = None, radius: Any = None, align: Optional[str] = None,
          link_url: Optional[str] = None, new_tab: bool = False, lightbox: bool = False,
          animation: Optional[str] = None, delay: Optional[int] = None,
          element_id: Optional[str] = None, css_classes: Optional[str] = None,
          object_fit: Optional[str] = None, margin: Optional[Dict[str, Any]] = None,
          shadow: Optional[str] = None, caption: Optional[str] = None,
          mobile_width: Any = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        image={"url": url, "id": "", "size": size, "alt": alt, "source": "library"},
        image_size=size,
        align=align,
        _element_id=element_id,
        _css_classes=css_classes,
        _margin=margin,
        link_to="custom" if link_url else ("file" if lightbox else None),
        link=link(link_url, new_tab) if link_url else None,
        open_lightbox="yes" if lightbox else None,
        object_fit=object_fit,
        caption_source="custom" if caption else None,
        caption=caption,
    )
    if width is not None:
        s["width"] = slider(width, width_unit)
    if mobile_width is not None:
        s["width_mobile"] = slider(mobile_width, width_unit)
    if max_width is not None:
        s["_element_custom_width"] = slider(max_width, width_unit)
        s["_element_width"] = "initial"
    if radius is not None:
        s["image_border_radius"] = radius if isinstance(radius, dict) else dims(radius)
    if shadow:
        s["image_box_shadow_box_shadow_type"] = "yes"
        s["image_box_shadow_box_shadow"] = tk.SHADOW[shadow]
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "image", s)


def icon(doc: Doc, value: str, *, library: str = "fa-solid", view: str = "framed",
         shape: str = "circle", size: int = 26, padding: int = 18, radius: Any = None,
         primary: Optional[str] = None, secondary: Optional[str] = None,
         hover_primary: Optional[str] = None, hover_secondary: Optional[str] = None,
         border_width: int = 0, border_radius: Any = None, align: Optional[str] = None,
         animation: Optional[str] = None, delay: Optional[int] = None,
         element_id: Optional[str] = None, css_classes: Optional[str] = None,
         **extra: Any) -> Dict[str, Any]:
    s = _base(
        selected_icon=icon_val(value, library),
        view=view,
        shape=shape,
        size=slider(size),
        icon_padding=slider(padding),
        primary_color=primary,
        secondary_color=secondary,
        hover_primary_color=hover_primary,
        hover_secondary_color=hover_secondary,
        border_width=slider(border_width) if border_width else None,
        border_radius=border_radius if isinstance(border_radius, dict) else (
            dims(border_radius) if border_radius is not None else (dims(radius) if radius is not None else None)),
        align=align,
        _element_id=element_id,
        _css_classes=css_classes,
    )
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "icon", s)


def icon_box(doc: Doc, title_value: str, description: str, *, icon_value: str,
             library: str = "fa-solid", position: str = "top", view: str = "framed",
             shape: str = "circle", icon_size: int = 26, icon_space: int = 22,
             icon_padding: int = 20, primary: Optional[str] = None, secondary: Optional[str] = None,
             title_color: Optional[str] = None, title_style: Optional[str] = None,
             title_tag: str = "h3", description_color: Optional[str] = None,
             body_style: Optional[str] = None, align: Optional[str] = None,
             content_align: Optional[str] = None, link_url: Optional[str] = None,
             border_width: int = 0, border_radius: Any = None, title_space: int = 12,
             animation: Optional[str] = None, delay: Optional[int] = None,
             element_id: Optional[str] = None, css_classes: Optional[str] = None,
             margin: Optional[Dict[str, Any]] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        title_text=title_value,
        description_text=description,
        selected_icon=icon_val(icon_value, library),
        position=position,
        title_size=title_tag,
        text_align=align,
        content_vertical_alignment=content_align,
        view=view,
        shape=shape,
        icon_size=slider(icon_size),
        icon_space=slider(icon_space),
        icon_padding=slider(icon_padding),
        primary_color=primary,
        secondary_color=secondary,
        title_color=title_color,
        description_color=description_color,
        title_bottom_space=slider(title_space),
        link=link(link_url) if link_url else None,
        border_width=slider(border_width) if border_width else None,
        border_radius=border_radius if isinstance(border_radius, dict) else (
            dims(border_radius) if border_radius is not None else None),
        _element_id=element_id,
        _css_classes=css_classes,
        _margin=margin,
    )
    s.update(prefixed("title_typography", title_style or tk.T["h3"]))
    s.update(prefixed("description_typography", body_style or tk.T["text"]))
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "icon-box", s)


def icon_list(doc: Doc, items: Iterable[Dict[str, Any]], *, space: int = 12, icon_size: int = 15,
              icon_color: Optional[str] = None, text_color: Optional[str] = None,
              style: Optional[str] = None, indent: int = 10, align: str = "left",
              icon_align: str = "left", animation: Optional[str] = None,
              delay: Optional[int] = None, element_id: Optional[str] = None,
              css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    rows = []
    for it in items:
        row = {
            "text": it["text"],
            "_id": it.get("_id") or hashlib.md5(it["text"].encode()).hexdigest()[:7],
            "selected_icon": icon_val(it.get("icon", "fas fa-check"),
                                      it.get("library", "fa-solid")),
        }
        if it.get("link"):
            row["link"] = link(it["link"], it.get("new_tab", False))
        rows.append(row)
    s = _base(
        icon_list=rows,
        space_between=slider(space),
        icon_size=slider(icon_size),
        icon_color=icon_color,
        text_color=text_color,
        text_indent=slider(indent),
        icon_align=icon_align,
        link_click="link",
        _element_id=element_id,
        _css_classes=css_classes,
    )
    s.update(prefixed("icon_typography", style or tk.T["text"]))
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "icon-list", s)


def counter(doc: Doc, ending: int, title_value: str, *, prefix: str = "", suffix: str = "",
            starting: int = 0, duration: int = 2000, number_color: Optional[str] = None,
            title_color: Optional[str] = None, number_style: Optional[str] = None,
            title_style: Optional[str] = None, title_tag: str = "p",
            title_position: str = "below", align: Optional[str] = None,
            animation: Optional[str] = None, delay: Optional[int] = None,
            css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        starting_number=starting,
        ending_number=ending,
        prefix=prefix,
        suffix=suffix,
        duration=duration,
        title=title_value,
        title_tag=title_tag,
        title_position=title_position,
        number_alignment=align,
        number_color=number_color,
        title_color=title_color,
        _css_classes=css_classes,
        thousand_separator=",",
    )
    s.update(prefixed("typography_number", number_style or tk.T["stat"]))
    s.update(prefixed("typography_title", title_style or tk.T["eyebrow"]))
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "counter", s)


def testimonial(doc: Doc, content: str, name: str, job: str, *, image_url: Optional[str] = None,
                image_alt: str = "", alignment: str = "center", image_position: str = "above",
                image_size: int = 72, content_color: Optional[str] = None,
                content_style: Optional[str] = None, name_color: Optional[str] = None,
                name_style: Optional[str] = None, job_color: Optional[str] = None,
                job_style: Optional[str] = None, animation: Optional[str] = None,
                delay: Optional[int] = None, css_classes: Optional[str] = None,
                element_id: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        testimonial_content=content,
        testimonial_name=name,
        testimonial_job=job,
        testimonial_image=({"url": image_url, "id": "", "size": "", "alt": image_alt, "source": "library"}
                           if image_url else None),
        testimonial_image_position=image_position if image_url else "aside",
        testimonial_alignment=alignment,
        content_content_color=content_color,
        name_text_color=name_color,
        job_text_color=job_color,
        _css_classes=css_classes,
        _element_id=element_id,
    )
    s.update(prefixed("content_typography", content_style or tk.T["text"]))
    s.update(prefixed("name_typography", name_style or tk.T["h3"]))
    s.update(prefixed("job_typography", job_style or tk.T["text"]))
    s.update(_anim(animation, delay))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "testimonial", s)


def accordion(doc: Doc, items: Iterable[Dict[str, str]], *, active: int = 0,
              icon: str = "fas fa-plus", active_icon: str = "fas fa-minus",
              title_color: Optional[str] = None, active_color: Optional[str] = None,
              content_color: Optional[str] = None, title_style: Optional[str] = None,
              body_style: Optional[str] = None, title_bg: str = "rgba(255,255,255,0)",
              content_bg: str = "rgba(255,255,255,0)", border_color: Optional[str] = None,
              border_width: int = 1, space: int = 14, padding: Optional[Dict[str, Any]] = None,
              css_classes: Optional[str] = None, element_id: Optional[str] = None,
              **extra: Any) -> Dict[str, Any]:
    rows = []
    for i, it in enumerate(items):
        rows.append({
            "_id": hashlib.md5(it["title"].encode()).hexdigest()[:7],
            "tab_title": it["title"],
            "tab_content": it["content"],
        })
    s = _base(
        tabs=rows,
        selected_icon=icon_val(icon),
        selected_active_icon=icon_val(active_icon),
        title_html_tag="h3",
        border_width=slider(border_width),
        border_color=border_color,
        title_background=title_bg,
        title_color=title_color,
        tab_active_color=active_color,
        content_background_color=content_bg,
        content_color=content_color,
        title_padding=padding or dims(20, 24),
        content_padding=dims(4, 24, 24),
        icon_color=title_color,
        icon_active_color=active_color,
        icon_space=slider(16),
        faq_schema="yes",
        _css_classes=css_classes,
        _element_id=element_id,
    )
    s.update(prefixed("title_typography", title_style or tk.T["h3"]))
    s.update(prefixed("content_typography", body_style or tk.T["text"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "accordion", s)


def tabs_widget(doc: Doc, items: Iterable[Dict[str, str]], *, kind: str = "horizontal",
                align: str = "center", title_color: Optional[str] = None,
                active_color: Optional[str] = None, content_color: Optional[str] = None,
                title_style: Optional[str] = None, body_style: Optional[str] = None,
                title_bg: str = "rgba(255,255,255,0)", content_bg: str = "rgba(255,255,255,0)",
                border_color: Optional[str] = None, padding: Optional[Dict[str, Any]] = None,
                css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    rows = [{"_id": hashlib.md5(i["title"].encode()).hexdigest()[:7],
             "tab_title": i["title"], "tab_content": i["content"]} for i in items]
    s = _base(
        tabs=rows,
        type=kind,
        tabs_align_horizontal=align,
        border_width=slider(1),
        border_color=border_color,
        background_color=title_bg,
        title_color=title_color,
        tab_active_color=active_color,
        content_color=content_color,
        title_padding=padding or dims(16, 22),
        title_align="center",
        _css_classes=css_classes,
    )
    s.update(prefixed("tab_typography", title_style or tk.T["h3"]))
    s.update(prefixed("content_typography", body_style or tk.T["text"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "tabs", s)


def social_icons(doc: Doc, items: Iterable[Dict[str, str]], *, shape: str = "circle",
                 size: str = "sm", padding: int = 12, spacing: int = 10, icon_size: int = 17,
                 align: Optional[str] = None, icon_color: Optional[str] = None,
                 primary: Optional[str] = None, secondary: Optional[str] = None,
                 hover_primary: Optional[str] = None, hover_secondary: Optional[str] = None,
                 border_radius: Any = None, css_classes: Optional[str] = None,
                 element_id: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    rows = []
    for it in items:
        rows.append({
            "_id": hashlib.md5(it["icon"].encode()).hexdigest()[:7],
            "social_icon": icon_val(it["icon"], it.get("library", "fa-brands")),
            "link": link(it.get("url", "#"), it.get("new_tab", True)),
            "item_icon_color": "custom" if it.get("color") else None,
            "item_icon_primary_color": it.get("color"),
        })
    rows = [{k: v for k, v in r.items() if v is not None} for r in rows]
    s = _base(
        social_icon_list=rows,
        shape=shape,
        size=size,
        icon_padding=slider(padding),
        icon_spacing=slider(spacing),
        icon_size=slider(icon_size),
        align=align,
        icon_color=icon_color,
        icon_primary_color=primary,
        icon_secondary_color=secondary,
        hover_primary_color=hover_primary,
        hover_secondary_color=hover_secondary,
        border_radius=border_radius if isinstance(border_radius, dict) else (
            dims(border_radius) if border_radius is not None else None),
        _css_classes=css_classes,
        _element_id=element_id,
    )
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "social-icons", s)


def divider(doc: Doc, *, style: str = "solid", weight: int = 1, color: Optional[str] = None,
            width: Any = 100, width_unit: str = "%", align: str = "center", gap: int = 16,
            css_classes: Optional[str] = None, margin: Optional[Dict[str, Any]] = None,
            element_id: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        style=style,
        weight=slider(weight),
        color=color,
        width=slider(width, width_unit),
        align=align,
        gap=slider(gap),
        _css_classes=css_classes,
        _element_id=element_id,
        _margin=margin,
    )
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "divider", s)


def spacer(doc: Doc, space: int = 40, *, space_mobile: Optional[int] = None,
           css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(space=slider(space), space_mobile=slider(space_mobile) if space_mobile is not None else None,
              _css_classes=css_classes)
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "spacer", s)


def menu_anchor(doc: Doc, anchor: str) -> Dict[str, Any]:
    return widget(doc, "menu-anchor", {"anchor": anchor})


def nav_menu(doc: Doc, *, layout: str = "horizontal", align: str = "center",
             pointer: str = "underline", pointer_color: Optional[str] = None,
             menu: str = "", style: Optional[str] = None, color: Optional[str] = None,
             hover_color: Optional[str] = None, active_color: Optional[str] = None,
             gap: int = 30, element_id: Optional[str] = None,
             css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    """Elementor Pro Nav Menu. `menu=""` -> assign your WP menu in the editor."""
    s = _base(
        menu=menu,
        layout=layout,
        align_items=align,
        pointer=pointer,
        pointer_color=pointer_color,
        color_menu=color,
        color_menu_hover=hover_color,
        color_menu_active=active_color,
        menu_space_between=slider(gap),
        submenu_space_between=slider(10),
        _element_id=element_id,
        _css_classes=css_classes,
    )
    s.update(prefixed("menu_typography", style or tk.T["nav"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "nav-menu", s)


def site_logo(doc: Doc, *, width: int = 150, width_mobile: int = 120,
              url: str = "https://aurora.example", element_id: Optional[str] = None,
              css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        width=slider(width),
        width_mobile=slider(width_mobile),
        link_to="custom",
        link=link(url),
        _element_id=element_id,
        _css_classes=css_classes,
    )
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-site-logo", s)


def theme_site_title(doc: Doc, *, tag: str = "span", style: Optional[str] = None,
                     color: Optional[str] = None, url: str = "",
                     css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        header_size=tag,
        site_title="Aurora AI",
        title_color=color,
        link=link(url) if url else None,
        _css_classes=css_classes,
    )
    s.update(typo(style or tk.T["h3"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-site-title", s)


def search_form(doc: Doc, *, skin: str = "classic", placeholder: str = "Search…",
                button_type: str = "icon", size: str = "md", **extra: Any) -> Dict[str, Any]:
    s = _base(skin=skin, placeholder=placeholder, button_type=button_type, input_size=size)
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "search-form", s)


# ---------------------------------------------------------------------------
# Elementor Pro: Form
# ---------------------------------------------------------------------------

FIELD = {"text": "text", "email": "email", "tel": "tel", "textarea": "textarea",
         "select": "select", "checkbox": "acceptance", "number": "number", "url": "url"}


def form_field(name: str, label: str, *, kind: str = "text", placeholder: str = "",
               required: bool = False, width: str = "100", options: Sequence[str] = (),
               rows: int = 4, css_id: Optional[str] = None) -> Dict[str, Any]:
    f = {
        "_id": hashlib.md5(("%s|%s" % (name, label)).encode()).hexdigest()[:7],
        "custom_id": css_id or name,
        "field_type": FIELD.get(kind, kind),
        "field_label": label,
        "field_name": name,
        "placeholder": placeholder,
        "required": "true" if required else "",
        "width": width,
        "width_mobile": "100",
    }
    if kind == "textarea":
        f["field_rows"] = str(rows)
    if kind == "select":
        f["field_options"] = "\n".join(options)
        f["allow_multiple"] = ""
    if kind == "acceptance":
        f["acceptance_text"] = placeholder
        f["checked_by_default"] = ""
    return {k: v for k, v in f.items() if v is not None}


def form(doc: Doc, fields: Sequence[Dict[str, Any]], *, button_text: str = "Send message",
         form_name: str = "Aurora Form", email_to: str = "hello@aurora.example",
         email_subject: str = "New enquiry from aurora.example", message: str = "[all-fields]",
         button_align: str = "start", button_size: str = "md", button_width: str = "100",
         button_variant: str = "primary", input_size: str = "md",
         label_color: Optional[str] = None, field_text_color: Optional[str] = None,
         field_bg: str = "rgba(255,255,255,1)", field_border_color: Optional[str] = None,
         radius: Any = None, css_classes: Optional[str] = None,
         element_id: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        form_name=form_name,
        form_fields=list(fields),
        button_text=button_text,
        button_size=button_size,
        button_align=button_align,
        button_width=button_width,
        email_to=email_to,
        email_subject=email_subject,
        email_content=message,
        email_from_name="Aurora AI",
        email_from="no-reply@aurora.example",
        email_reply_to="email",
        submit_actions=["email", "email2"],
        success_message="Thanks — we'll be in touch within one business day.",
        error_message="Something went wrong. Please try again.",
        input_size=input_size,
        label_color=label_color,
        field_text_color=field_text_color,
        field_background_color=field_bg,
        field_border_color=field_border_color,
        field_border_width=dims(1),
        field_border_radius=radius if isinstance(radius, dict) else (
            dims(radius or 12) if radius is not False else None),
        button_text_color=tk.G["ink_900"] if button_variant == "primary" else None,
        button_background_color=tk.G["primary"] if button_variant == "primary" else None,
        _css_classes=css_classes,
        _element_id=element_id,
    )
    s.update(prefixed("label_typography", tk.T["eyebrow"], text_transform="none",
                      font_size=slider(13), letter_spacing=slider(0.2)))
    s.update(prefixed("field_typography", tk.T["text"]))
    s.update(prefixed("button_typography", tk.T["accent"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "form", s)


# ---------------------------------------------------------------------------
# Elementor Pro: Posts / Loop / Theme Builder
# ---------------------------------------------------------------------------

def posts(doc: Doc, *, post_type: str = "post", per_page: int = 6, columns: int = 3,
          image_size: str = "medium_large", excerpt_length: int = 18,
          show_title: str = "yes", show_excerpt: str = "yes", show_read_more: str = "yes",
          read_more_text: str = "Read article", pagination: str = "numbers",
          columns_tablet: int = 2, columns_mobile: int = 1, skin: str = "classic",
          title_color: Optional[str] = None, text_color: Optional[str] = None,
          meta_color: Optional[str] = None, card_bg: Optional[str] = None,
          border_color: Optional[str] = None, radius: Any = None,
          css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(
        _skin=skin,
        posts_post_type=post_type,
        posts_per_page=per_page,
        classic_columns=columns,
        classic_columns_tablet=columns_tablet,
        classic_columns_mobile=columns_mobile,
        thumbnail_size=image_size,
        show_title=show_title,
        show_excerpt=show_excerpt,
        excerpt_length=excerpt_length,
        show_read_more=show_read_more,
        read_more_text=read_more_text,
        pagination_type=pagination,
        title_color=title_color,
        text_color=text_color,
        meta_color=meta_color,
        card_bg_color=card_bg,
        card_border_color=border_color,
        card_border_width=dims(1),
        card_border_radius=radius if isinstance(radius, dict) else (
            dims(radius) if radius is not None else None),
        _css_classes=css_classes,
    )
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "posts", s)


def archive_posts(doc: Doc, *, skin: str = "cards", columns: int = 3, per_page: int = 9,
                  columns_tablet: int = 2, columns_mobile: int = 1,
                  pagination: str = "numbers", show_title: str = "yes",
                  show_excerpt: str = "yes", read_more_text: str = "Read article",
                  **extra: Any) -> Dict[str, Any]:
    s = _base(
        _skin=skin,
        columns=columns,
        columns_tablet=columns_tablet,
        columns_mobile=columns_mobile,
        posts_per_page=per_page,
        pagination_type=pagination,
        show_title=show_title,
        show_excerpt=show_excerpt,
        show_read_more="yes",
        read_more_text=read_more_text,
        card_border_width=dims(1),
        card_border_radius=dims(20),
    )
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "archive-posts", s)


def post_title(doc: Doc, *, tag: str = "h1", style: Optional[str] = None,
               color: Optional[str] = None, align: Optional[str] = None,
               css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(header_size=tag, title_color=color, align=align, _css_classes=css_classes)
    s.update(typo(style or tk.T["display"], font_size=slider(52), font_size_mobile=slider(32)))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-post-title", s)


def post_content(doc: Doc, *, color: Optional[str] = None, style: Optional[str] = None,
                 **extra: Any) -> Dict[str, Any]:
    s = _base(text_color=color)
    s.update(typo(style or tk.T["text"], font_size=slider(18)))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-post-content", s)


def post_excerpt(doc: Doc, *, color: Optional[str] = None, style: Optional[str] = None,
                 **extra: Any) -> Dict[str, Any]:
    s = _base(text_color=color)
    s.update(typo(style or tk.T["lead"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-post-excerpt", s)


def featured_image(doc: Doc, *, radius: Any = None, size: str = "full",
                   css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(image_size=size, _css_classes=css_classes)
    if radius is not None:
        s["image_border_radius"] = radius if isinstance(radius, dict) else dims(radius)
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-post-featured-image", s)


def author_box(doc: Doc, *, avatar: str = "yes", avatar_size: int = 64,
               link_to: str = "posts", **extra: Any) -> Dict[str, Any]:
    s = _base(show_avatar=avatar, avatar_size=slider(avatar_size), link_to=link_to)
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "author-box", s)


def post_comments(doc: Doc, **extra: Any) -> Dict[str, Any]:
    s = _base()
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "post-comments", s)


def post_navigation(doc: Doc, *, arrows: str = "yes", text: str = "yes",
                    prev: str = "Previous", next_: str = "Next", **extra: Any) -> Dict[str, Any]:
    s = _base(show_arrows=arrows, show_text=text, prev_text=prev, next_text=next_)
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "post-navigation", s)


def breadcrumbs(doc: Doc, *, separator: str = "/", home: str = "Home",
                color: Optional[str] = None, style: Optional[str] = None,
                css_classes: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(separator=separator, show_home="yes", home_label=home,
              text_color=color, _css_classes=css_classes)
    s.update(typo(style or tk.T["text"], font_size=slider(14)))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "breadcrumbs", s)


def theme_page_title(doc: Doc, *, tag: str = "h1", style: Optional[str] = None,
                     color: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(header_size=tag, title_color=color)
    s.update(typo(style or tk.T["h2"]))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-page-title", s)


def theme_archive_title(doc: Doc, *, tag: str = "h1", style: Optional[str] = None,
                        color: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    s = _base(header_size=tag, title_color=color)
    s.update(typo(style or tk.T["display"], font_size=slider(48), font_size_mobile=slider(32)))
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "theme-archive-title", s)


def post_info(doc: Doc, **extra: Any) -> Dict[str, Any]:
    s = _base()
    s.update({k: v for k, v in extra.items() if v is not None})
    return widget(doc, "post-info", s)
