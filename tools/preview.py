#!/usr/bin/env python3
"""
Aurora AI - static design preview.

Reads the generated Elementor template JSON and renders an approximation of the
Elementor front-end so the design can be reviewed in a browser.

    python3 tools/preview.py            # -> preview/*.html
    python3 tools/preview.py --serve    # also start http://localhost:8080

IMPORTANT: this renderer is a *review tool only*. It is not part of the
deliverable and nothing in it ships to WordPress. The templates themselves stay
pure Elementor JSON - all real styling is produced by Elementor on the site from
the same settings this file reads.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aurora import tokens as tk  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
OUT = os.path.join(ROOT, "preview")

# ---------------------------------------------------------------------------
# token -> CSS
# ---------------------------------------------------------------------------

COLOR_HEX = {c["_id"]: c["color"] for c in tk.SYSTEM_COLORS + tk.CUSTOM_COLORS}
COLOR_HEX["muted-dark"] = "#A8A29E"
COLOR_HEX["line-dark"] = "rgba(255,255,255,0.12)"

SHADOWS = tk.SHADOW


def resolve_color(value: str) -> str:
    if not isinstance(value, str):
        return value
    if value.startswith("globals/colors?id="):
        key = value.split("=", 1)[1]
        return COLOR_HEX.get(key, "#000000")
    if value.startswith("globals/typography?id="):
        return value
    return value


TYPO = {}
for row in tk.SYSTEM_TYPOGRAPHY + tk.CUSTOM_TYPOGRAPHY:
    TYPO[row["_id"]] = row


def typo_css(settings: Dict[str, Any], prefix: str = "typography") -> Dict[str, str]:
    """Turn a typography group (already prefixed) into CSS declarations per device."""
    out: Dict[str, Dict[str, str]] = {"": {}, "tablet": {}, "mobile": {}}
    base = settings.get(prefix) or settings.get(prefix + "_typography")
    for dev, suffix in (("", ""), ("tablet", "_tablet"), ("mobile", "_mobile")):
        d = out[dev]
        ref = base if dev == "" else None
        if ref and isinstance(ref, str) and ref.startswith("globals/typography?id="):
            row = TYPO.get(ref.split("=", 1)[1], {})
            d = _apply_typo_row(row, d, dev)
        fam = settings.get("%s_font_family%s" % (prefix, suffix)) or (
            settings.get("%s_typography%s" % (prefix, suffix)) if dev else base)
        if dev and fam and str(fam).startswith("globals/typography?id="):
            d = _apply_typo_row(TYPO.get(str(fam).split("=", 1)[1], {}), d, dev)
        for field, css in (("font_family", "font-family"), ("font_weight", "font-weight"),
                           ("font_size", "font-size"), ("line_height", "line-height"),
                           ("letter_spacing", "letter-spacing"),
                           ("text_transform", "text-transform")):
            val = settings.get("%s_%s%s" % (prefix, field, suffix))
            if val is None:
                continue
            if isinstance(val, dict):
                d[css] = "%s%s" % (val.get("size"), val.get("unit") or "px")
            else:
                d[css] = str(val)
        out[dev] = d
    return {"": " ; ".join("%s:%s" % kv for kv in out[""].items()),
            "tablet": " ; ".join("%s:%s" % kv for kv in out["tablet"].items()),
            "mobile": " ; ".join("%s:%s" % kv for kv in out["mobile"].items())}


def _apply_typo_row(row: Dict[str, Any], d: Dict[str, str], dev: str) -> Dict[str, str]:
    suffix = "" if dev == "" else "_" + dev
    for field, css in (("font_family", "font-family"), ("font_weight", "font-weight"),
                       ("font_size", "font-size"), ("line_height", "line-height"),
                       ("letter_spacing", "letter-spacing"),
                       ("text_transform", "text-transform")):
        val = row.get("typography_%s%s" % (field, suffix))
        if val is None and dev:
            continue
        if isinstance(val, dict):
            d[css] = "%s%s" % (val.get("size"), val.get("unit") or "px")
        elif val is not None:
            d[css] = str(val)
    return d


def dims_css(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    u = value.get("unit", "px")
    return " ".join("%s%s" % (value.get(k, 0), u) for k in ("top", "right", "bottom", "left"))


def slider_css(value: Any) -> str:
    if isinstance(value, dict):
        return "%s%s" % (value.get("size"), value.get("unit") or "px")
    return str(value)


def gap_css(value: Any) -> str:
    if isinstance(value, dict):
        u = value.get("unit", "px")
        return "%s%s %s%s" % (value.get("row", 0), u, value.get("column", 0), u)
    return ""


# ---------------------------------------------------------------------------
# element renderers
# ---------------------------------------------------------------------------

def container_css(s: Dict[str, Any], device: str = "") -> List[str]:
    suffix = "_%s" % device if device else ""
    css: List[str] = []
    get = lambda k: s.get(k + suffix)  # noqa: E731

    d = get("flex_direction")
    if d:
        css.append("flex-direction:%s" % d)
    w = get("flex_wrap")
    if w:
        css.append("flex-wrap:%s" % w)
    j = get("flex_justify_content")
    if j:
        css.append("justify-content:%s" % j)
    a = get("flex_align_items")
    if a:
        css.append("align-items:%s" % a)
    ac = get("flex_align_content")
    if ac:
        css.append("align-content:%s" % ac)
    g = get("flex_gap")
    if g:
        css.append("gap:%s" % gap_css(g))
    pad = get("padding")
    if pad:
        css.append("padding:%s" % dims_css(pad))
    mar = get("margin")
    if mar:
        css.append("margin:%s" % dims_css(mar))
    bw = get("boxed_width")
    if bw:
        css.append("max-width:%s" % slider_css(bw))
        css.append("width:100%")
        css.append("margin-inline:auto")
    mh = get("min_height")
    if mh:
        css.append("min-height:%s" % slider_css(mh))
    return css


def container_base_css(s: Dict[str, Any]) -> List[str]:
    css: List[str] = []
    bg = s.get("background_background")
    if bg == "classic":
        css.append("background-color:%s" % resolve_color(s.get("background_color", "")))
    elif bg == "gradient":
        c1 = resolve_color(s.get("background_color", "#fff"))
        c2 = resolve_color(s.get("background_color_b", "#fff"))
        ang = s.get("background_gradient_angle") or {"size": 180, "unit": "deg"}
        css.append("background-image:linear-gradient(%s, %s 0%%, %s 100%%)"
                   % (slider_css(ang), c1, c2))
    elif bg == "none":
        css.append("background:transparent")

    if s.get("background_overlay_background") == "classic":
        css.append("background-color:%s" % resolve_color(s.get("background_overlay_color", "")))

    if s.get("border_border"):
        css.append("border:%s %s %s" % (slider_css(s.get("border_width", 0)),
                                        s["border_border"],
                                        resolve_color(s.get("border_color", ""))))
    if s.get("border_radius"):
        css.append("border-radius:%s" % dims_css(s["border_radius"]))
    if s.get("box_shadow_box_shadow_type") == "yes":
        sh = s.get("box_shadow_box_shadow") or {}
        css.append("box-shadow:%spx %spx %spx %spx %s" % (
            sh.get("horizontal", 0), sh.get("vertical", 0), sh.get("blur", 0),
            sh.get("spread", 0), sh.get("color", "rgba(0,0,0,.1)")))
    if s.get("overflow"):
        css.append("overflow:%s" % s["overflow"])
    if s.get("z_index") is not None:
        css.append("z-index:%s" % s["z_index"])
    if s.get("position") == "absolute":
        css.append("position:absolute")
    if s.get("content_width") == "full" or s.get("width"):
        css.append("width:100%")
    return css


def flex_item_css(s: Dict[str, Any]) -> List[str]:
    css: List[str] = []
    if s.get("_flex_size") == "grow":
        css.append("flex-grow:1")
        css.append("flex-shrink:0")
    elif s.get("_flex_size") == "shrink":
        css.append("flex-grow:0")
        css.append("flex-shrink:1")
    elif s.get("_flex_size") == "none":
        css.append("flex-grow:0")
        css.append("flex-shrink:0")
    if s.get("_flex_grow") is not None and s.get("_flex_size") == "custom":
        css.append("flex-grow:%s" % s["_flex_grow"])
    if s.get("_flex_shrink") is not None and s.get("_flex_size") == "custom":
        css.append("flex-shrink:%s" % s["_flex_shrink"])
    basis = s.get("_flex_basis")
    if basis:
        css.append("flex-basis:%s" % slider_css(basis))
    if s.get("_flex_align_self"):
        css.append("align-self:%s" % s["_flex_align_self"])
    if s.get("_element_width") == "100%":
        css.append("width:100%")
    elif s.get("_element_width") == "initial":
        css.append("width:auto")
    elif s.get("_element_custom_width"):
        css.append("max-width:%s" % slider_css(s["_element_custom_width"]))
        css.append("width:100%")
    return css


def widget_css(s: Dict[str, Any]) -> Tuple[str, Dict[str, str]]:
    """Return (inline style string, {'tablet':..,'mobile':..}) for a widget."""
    base = container_base_css(s) + flex_item_css(s)
    if s.get("align"):
        base.append("text-align:%s" % s["align"])
    if s.get("_margin"):
        base.append("margin:%s" % dims_css(s["_margin"]))
    t = typo_css(s)
    if t[""]:
        base.append(t[""])
    return " ; ".join(base), {"tablet": t["tablet"], "mobile": t["mobile"]}


def animation(s: Dict[str, Any], el_type: str) -> str:
    key = "animation" if el_type == "container" else "_animation"
    anim = s.get(key)
    if not anim:
        return ""
    return ' data-anim="%s" data-delay="%s"' % (anim, s.get("animation_delay", 0))


# ---------------------------------------------------------------------------
# widget bodies
# ---------------------------------------------------------------------------

ICON_LIST = []


def w_heading(s, doc=None):
    tag = s.get("header_size", "h2")
    style, dev = widget_css(s)
    color = resolve_color(s.get("title_color") or "")
    if color:
        style += " ; color:%s" % color
    link = s.get("link") or {}
    body = html.escape(s.get("title", ""))
    if link.get("url"):
        body = '<a href="%s">%s</a>' % (html.escape(link["url"]), body)
    return el(tag, body, style, dev)


def w_text(s, doc=None):
    style, dev = widget_css(s)
    color = resolve_color(s.get("text_color") or "")
    if color:
        style += " ; color:%s" % color
    return el("div", s.get("editor", ""), style, dev, cls="txt")


def w_button(s, doc=None):
    style, dev = widget_css(s)
    bg = "transparent"
    if s.get("background_background") == "classic":
        bg = resolve_color(s.get("background_color", "transparent"))
    color = resolve_color(s.get("button_text_color", "#000"))
    extra = ["background:%s" % bg, "color:%s" % color,
             "box-shadow:none", "border:none", "cursor:pointer",
             "display:inline-flex", "align-items:center", "gap:9px",
             "text-decoration:none", "font-weight:600"]
    if s.get("border_radius"):
        extra.append("border-radius:%s" % dims_css(s["border_radius"]))
    if s.get("text_padding"):
        extra.append("padding:%s" % dims_css(s["text_padding"]))
    else:
        extra.append("padding:14px 26px")
    if s.get("_element_width") == "100%":
        extra.append("justify-content:center")
    icon = ""
    if s.get("selected_icon"):
        v = s["selected_icon"].get("value", "")
        icon = '<i class="%s"></i>' % fa_class(v)
    label = '<span>%s</span>' % html.escape(s.get("text", ""))
    inner = icon + label if s.get("icon_align") != "left" else label + icon
    return el("a", inner, " ; ".join(extra), dev, cls="btn")


def fa_class(value: str) -> str:
    """'fas fa-check' -> 'fa-solid fa-check'; 'fab fa-x-twitter' -> 'fa-brands ...'"""
    if not value:
        return "fa-solid fa-circle"
    parts = value.split()
    mapping = {"fas": "fa-solid", "far": "fa-regular", "fab": "fa-brands"}
    out = []
    for p in parts:
        out.append(mapping.get(p, p))
    return " ".join(out)


def w_icon(s, doc=None):
    style, dev = widget_css(s)
    view = s.get("view", "default")
    size = s.get("size") or {"size": 26}
    color = resolve_color(s.get("primary_color", "#F4A62A"))
    extra = ["color:%s" % color,
             "font-size:%s" % slider_css(size),
             "display:inline-flex", "align-items:center", "justify-content:center"]
    if view in ("framed", "stacked"):
        pad = s.get("icon_padding") or {"size": 16}
        extra.append("width:%s" % slider_css(pad))
        extra.append("height:%s" % slider_css(pad))
        extra.append("padding:%s" % slider_css(pad))
        extra.append("box-sizing:content-box")
        if view == "framed":
            extra.append("background:transparent")
            extra.append("border:1px solid %s" % resolve_color(s.get("secondary_color", "#F4A62A")))
        else:
            extra.append("background:%s" % resolve_color(s.get("secondary_color", "#F4A62A")))
        shape = s.get("shape", "circle")
        extra.append("border-radius:%s" % ("50%" if shape == "circle" else "6px"))
    if s.get("_element_custom_width"):
        extra.append("width:%s" % slider_css(s["_element_custom_width"]))
        extra.append("height:%s" % slider_css(s["_element_custom_width"]))
        extra.append("box-sizing:border-box")
    return el("i", "", " ; ".join(extra), dev, cls=fa_class(s.get("selected_icon", {}).get("value", "")))


def w_image(s, doc=None):
    style, dev = widget_css(s)
    src = (s.get("image") or {}).get("url", "")
    alt = html.escape((s.get("image") or {}).get("alt", ""))
    r = ""
    if s.get("image_border_radius"):
        r = "border-radius:%s" % dims_css(s["image_border_radius"])
    if s.get("object_fit"):
        r += " ; object-fit:%s" % s["object_fit"]
    if s.get("width"):
        r += " ; width:%s" % slider_css(s["width"])
    if s.get("image_box_shadow_box_shadow_type") == "yes":
        sh = s["image_box_shadow_box_shadow"]
        r += " ; box-shadow:%spx %spx %spx %spx %s" % (
            sh.get("horizontal", 0), sh.get("vertical", 0), sh.get("blur", 0),
            sh.get("spread", 0), sh.get("color", "rgba(0,0,0,.1)"))
    return el("img", "", (style + " ; " + r) if r else style, dev, cls="img",
              attrs='src="%s" alt="%s" loading="lazy"' % (html.escape(src), alt))


def w_divider(s, doc=None):
    style, dev = widget_css(s)
    w = s.get("width") or {"size": 100, "unit": "%"}
    extra = ["border:none", "border-top:%s %s %s" % (
        s.get("weight", {}).get("size", 1) if isinstance(s.get("weight"), dict) else 1,
        s.get("style", "solid"), resolve_color(s.get("color", "#eee"))),
        "width:%s" % slider_css(w),
        "margin:%s auto" % slider_css(s.get("gap") or {"size": 15})]
    return el("hr", "", " ; ".join(extra), dev)


def w_icon_list(s, doc=None):
    style, dev = widget_css(s)
    items = []
    for it in s.get("icon_list", []):
        icon = '<i class="%s"></i>' % fa_class(it.get("selected_icon", {}).get("value", "fas fa-check"))
        color = resolve_color(s.get("icon_color", "#F4A62A"))
        sz = s.get("icon_size") or {"size": 15}
        txt = html.escape(it.get("text", ""))
        href = (it.get("link") or {}).get("url")
        body = '<a href="%s">%s</a>' % (html.escape(href), txt) if href else txt
        items.append('<li style="color:%s"><span class="ico" style="color:%s;font-size:%s">%s</span>%s</li>'
                     % (resolve_color(s.get("text_color", "#57534E")), color,
                        slider_css(sz), icon, body))
    space = s.get("space_between") or {"size": 10}
    return el("ul", "".join(items),
              (style + " ; display:flex ; flex-direction:column ; gap:%s" % slider_css(space)),
              dev, cls="icon-list", attrs='style2="inline"')


def w_counter(s, doc=None):
    style, dev = widget_css(s)
    num = "%s%s%s" % (s.get("prefix", ""), s.get("ending_number", 0), s.get("suffix", ""))
    nstyle = typo_css(s, "typography_number")[""] or ""
    tstyle = typo_css(s, "typography_title")[""] or ""
    block = ('<div class="counter" style="text-align:left">'
             '<div class="num" style="color:%s;%s">%s</div>'
             '<div class="lbl" style="color:%s;%s">%s</div></div>'
             % (resolve_color(s.get("number_color", "#F4A62A")), nstyle, html.escape(str(num)),
                resolve_color(s.get("title_color", "#8C8177")), tstyle,
                html.escape(s.get("title", ""))))
    return el("div", block, style, dev)


def w_accordion(s, doc=None):
    style, dev = widget_css(s)
    rows = []
    for i, t in enumerate(s.get("tabs", [])):
        open_attr = " open" if i == 0 else ""
        rows.append(
            '<details class="acc"%s><summary><span>%s</span><i class="fa-solid fa-plus"></i>'
            '<i class="fa-solid fa-minus"></i></summary><div class="acc-body">%s</div></details>'
            % (open_attr, html.escape(t.get("tab_title", "")), t.get("tab_content", "")))
    tstyle = typo_css(s, "title_typography")[""] or ""
    extra = style + " ; " + tstyle
    return el("div", "".join(rows), extra, dev, cls="acc-wrap")


def w_tabs(s, doc=None):
    style, dev = widget_css(s)
    rows = s.get("tabs", [])
    nav = "".join('<button class="tab%s">%s</button>' % (" active" if i == 0 else "",
                                                         html.escape(t.get("tab_title", "")))
                  for i, t in enumerate(rows))
    panels = "".join('<div class="tab-panel%s">%s</div>' % (" active" if i == 0 else "",
                                                            t.get("tab_content", ""))
                     for i, t in enumerate(rows))
    return el("div", '<div class="tab-nav">%s</div><div class="tab-panels">%s</div>' % (nav, panels),
              style, dev, cls="tabs-widget")


def w_social(s, doc=None):
    style, dev = widget_css(s)
    links = []
    for it in s.get("social_icon_list", []):
        icon = fa_class((it.get("social_icon") or {}).get("value", "fab fa-twitter"))
        pad = s.get("icon_padding") or {"size": 12}
        links.append('<a href="%s" style="width:calc(100%% - 0px);background:%s;color:%s;'
                     'width:%s;height:%s;display:inline-flex;align-items:center;'
                     'justify-content:center;border-radius:%s">'
                     '<i class="%s" style="font-size:%s"></i></a>'
                     % (html.escape((it.get("link") or {}).get("url", "#")),
                        resolve_color(s.get("icon_primary_color", "#1C1917")),
                        resolve_color(s.get("icon_secondary_color", "#fff")),
                        slider_css(pad), slider_css(pad),
                        ("50%" if s.get("shape", "circle") == "circle" else "6px"),
                        icon, slider_css(s.get("icon_size") or {"size": 15})))
    return el("div", "".join(links),
              style + " ; display:flex ; flex-wrap:wrap ; gap:%s" % slider_css(s.get("icon_spacing") or {"size": 10}),
              dev, cls="social")


def w_spacer(s, doc=None):
    style, dev = widget_css(s)
    return el("div", "", style + " ; height:%s" % slider_css(s.get("space") or {"size": 40}), dev)


def w_form(s, doc=None):
    style, dev = widget_css(s)
    rows = []
    for f in s.get("form_fields", []):
        t = f.get("field_type")
        label = f.get("field_label", "")
        ph = f.get("placeholder", "")
        head = '<label>%s%s</label>' % (html.escape(label), " *" if f.get("required") else "")
        if t == "textarea":
            ctrl = '<textarea rows="%s" placeholder="%s"></textarea>' % (f.get("field_rows", 4),
                                                                        html.escape(ph))
        elif t == "select":
            opts = "".join('<option>%s</option>' % html.escape(o)
                           for o in (f.get("field_options", "") or "").split("\n"))
            ctrl = '<select>%s</select>' % opts
        elif t == "acceptance":
            ctrl = ('<label class="check"><input type="checkbox"> <span>%s</span></label>'
                    % html.escape(f.get("acceptance_text", "")))
        else:
            ctrl = '<input type="%s" placeholder="%s">' % (t, html.escape(ph))
        rows.append('<div class="field" style="flex-basis:%s">%s%s</div>'
                    % (f.get("width", "100%") + "%", "" if t == "acceptance" else head, ctrl))
    btn = ('<button type="button" class="btn form-btn">%s</button>'
           % html.escape(s.get("button_text", "Submit")))
    return el("form", '<div class="form-grid">%s</div>%s' % ("".join(rows), btn),
              style, dev, cls="aurora-form", attrs='onsubmit="return false"')


def w_posts(s, doc=None):
    style, dev = widget_css(s)
    cards = []
    for i in range(3):
        cards.append('<article class="post-card"><div class="thumb"></div>'
                     '<span class="meta">Engineering</span>'
                     '<h3>How we evaluate an agent before it meets a customer</h3>'
                     '<p>A pragmatic walkthrough of golden sets, regression diffs and the '
                     'quality gate we run on every prompt change.</p>'
                     '<span class="more">Read article <i class="fa-solid fa-arrow-right"></i></span>'
                     '</article>')
    return el("div", "".join(cards), style, dev, cls="posts-grid")


def w_logo(s, doc=None):
    style, dev = widget_css(s)
    w = s.get("width") or {"size": 150}
    return el("div", '<span class="logo-mark"></span>',
              style + " ; width:%s" % slider_css(w), dev, cls="logo-widget",
              attrs='aria-label="Site logo placeholder"')


def w_site_title(s, doc=None):
    return w_heading({"title": "Aurora AI", "header_size": "span",
                      **{k: v for k, v in s.items() if k.startswith("typography")}},
                     doc)


def w_nav_menu(s, doc=None):
    style, dev = widget_css(s)
    items = ["Product", "Solutions", "Pricing", "Journal", "Company"]
    links = "".join('<a href="#" class="%s">%s</a>' % ("active" if i == 2 else "", it)
                    for i, it in enumerate(items))
    t = typo_css(s, "menu_typography")[""]
    return el("nav", links,
              "%s ; display:flex ; gap:%s ; align-items:center ; %s"
              % (style, slider_css(s.get("menu_space_between") or {"size": 30}), t),
              dev, cls="nav-menu")


def w_breadcrumbs(s, doc=None):
    style, dev = widget_css(s)
    return el("div", '<a href="#">Home</a> <span>/</span> <span>Journal</span>',
              style + " ; color:%s" % resolve_color(s.get("text_color", "#8C8177")),
              dev, cls="crumbs")


def w_post_info(s, doc=None):
    style, dev = widget_css(s)
    return el("div", "By Aurora Team &nbsp;·&nbsp; 14 July 2026 &nbsp;·&nbsp; 6 min read",
              style + " ; color:%s" % resolve_color(s.get("text_color", "#8C8177")),
              dev, cls="post-info")


def w_featured_image(s, doc=None):
    style, dev = widget_css(s)
    return el("div", "", style + " ; background:linear-gradient(135deg,#F3E9DB,#FDF0DA) ; "
                                 "aspect-ratio:3/2 ; border-radius:%s"
              % dims_css(s.get("image_border_radius", {"top": "22", "right": "22", "bottom": "22", "left": "22", "unit": "px"})),
              dev, cls="featured-image")


def w_post_content(s, doc=None):
    style, dev = widget_css(s)
    t = typo_css(s)[""]
    body = ("<p>Aurora gives product teams warm, human AI infrastructure. This article walks "
            "through the evaluation harness we run before any agent reaches a customer, and the "
            "quality gate that blocks a release when a metric regresses.</p>"
            "<h2>Why golden sets beat vibes</h2>"
            "<p>Every prompt change invalidates your previous confidence. A golden set is the "
            "cheapest insurance in the building: fifty representative cases, scored automatically, "
            "diffed on every pull request.</p>"
            "<blockquote>If you cannot show a number going up, you are not evaluating - you are "
            "hoping.</blockquote>"
            "<p>Wire the harness into CI, publish the score on the pull request and let the team "
            "argue about the cases that matter instead of arguing about feelings.</p>")
    return el("div", body, style + " ; " + t, dev, cls="prose")


def w_author_box(s, doc=None):
    style, dev = widget_css(s)
    return el("div", '<span class="avatar"></span><div><strong>Aurora Team</strong>'
                     '<p>Engineers and researchers building the calm layer for AI products. '
                     'We write about what we had to learn the hard way.</p></div>',
              style, dev, cls="author-box")


def w_post_nav(s, doc=None):
    style, dev = widget_css(s)
    return el("div", '<a href="#"><i class="fa-solid fa-arrow-left"></i> Previous</a>'
                     '<a href="#">Next <i class="fa-solid fa-arrow-right"></i></a>',
              style + " ; display:flex ; justify-content:space-between", dev, cls="post-nav")


def w_comments(s, doc=None):
    style, dev = widget_css(s)
    return el("div", '<h3>Join the conversation</h3>'
                     '<p class="muted">Comments are rendered by WordPress on the live site.</p>',
              style, dev, cls="comments")


def w_theme_page_title(s, doc=None):
    return w_heading({"title": "Page title", "header_size": "h1", **s}, doc)


def w_archive_title(s, doc=None):
    return w_heading({"title": "Journal", "header_size": "h1", **s}, doc)


def w_search_form(s, doc=None):
    style, dev = widget_css(s)
    return el("div", '<form class="aurora-form inline" onsubmit="return false">'
                     '<input type="search" placeholder="%s"><button class="btn">Search</button>'
                     '</form>' % html.escape(s.get("placeholder", "Search…")),
              style, dev, cls="search-form")


def w_archive_posts(s, doc=None):
    return w_posts(s, doc)


def w_testimonial(s, doc=None):
    style, dev = widget_css(s)
    body = ('<p class="quote">%s</p><div class="who"><strong>%s</strong><span>%s</span></div>'
            % (html.escape(s.get("testimonial_content", "")),
               html.escape(s.get("testimonial_name", "")),
               html.escape(s.get("testimonial_job", ""))))
    return el("div", body, style, dev, cls="testimonial")


def w_icon_box(s, doc=None):
    style, dev = widget_css(s)
    icon = '<i class="%s"></i>' % fa_class((s.get("selected_icon") or {}).get("value", "fas fa-star"))
    body = ('<div class="ib"><div class="ib-icon">%s</div><h3>%s</h3><p>%s</p></div>'
            % (icon, html.escape(s.get("title_text", "")), html.escape(s.get("description_text", ""))))
    return el("div", body, style, dev, cls="icon-box")


def w_unknown(s, doc=None):
    style, dev = widget_css(s)
    return el("div", '<div class="unknown">%s</div>' % html.escape(str(s)[:120]), style, dev)


WIDGETS = {
    "heading": w_heading, "text-editor": w_text, "button": w_button, "icon": w_icon,
    "image": w_image, "divider": w_divider, "icon-list": w_icon_list, "counter": w_counter,
    "accordion": w_accordion, "tabs": w_tabs, "social-icons": w_social, "spacer": w_spacer,
    "form": w_form, "posts": w_posts, "archive-posts": w_archive_posts,
    "theme-site-logo": w_logo, "theme-site-title": w_site_title, "nav-menu": w_nav_menu,
    "breadcrumbs": w_breadcrumbs, "post-info": w_post_info,
    "theme-post-featured-image": w_featured_image, "theme-post-content": w_post_content,
    "theme-post-excerpt": w_post_content, "theme-post-title": w_theme_page_title,
    "author-box": w_author_box, "post-navigation": w_post_nav, "post-comments": w_comments,
    "theme-page-title": w_theme_page_title, "theme-archive-title": w_archive_title,
    "search-form": w_search_form, "testimonial": w_testimonial, "icon-box": w_icon_box,
}

# ---------------------------------------------------------------------------
# element -> html
# ---------------------------------------------------------------------------

UID = [0]


def el(tag: str, body: str, style: str = "", dev: Optional[Dict[str, str]] = None,
       cls: str = "", attrs: str = "") -> str:
    UID[0] += 1
    uid = "e%d" % UID[0]
    css = ["#%s{%s}" % (uid, style)] if style else []
    if dev:
        for device in ("tablet", "mobile"):
            if dev.get(device):
                css.append("@media(max-width:%dpx){#%s{%s}}"
                           % (1024 if device == "tablet" else 767, uid, dev[device]))
    return '<style>%s</style><%s id="%s" class="%s"%s %s>%s</%s>' % (
        "".join(css), tag, uid, cls, attrs, "", body, tag)


def render_node(node: Dict[str, Any], depth: int = 0) -> str:
    s = node.get("settings") or {}
    if node.get("elType") == "widget":
        fn = WIDGETS.get(node.get("widgetType"), w_unknown)
        try:
            return fn(s)
        except Exception as exc:  # pragma: no cover
            return '<div class="unknown">%s failed: %s</div>' % (node.get("widgetType"), exc)

    tag = s.get("html_tag") or "div"
    if tag in ("section", "header", "footer", "main", "article", "aside"):
        pass
    css = container_css(s) + container_base_css(s) + flex_item_css(s)
    dev = {"tablet": " ; ".join(container_css(s, "tablet")),
           "mobile": " ; ".join(container_css(s, "mobile"))}
    kids = "".join(render_node(c, depth + 1) for c in node.get("elements") or [])
    inner_html = kids
    link = s.get("link") or {}
    if link.get("url"):
        inner_html = '<a class="c-link" href="%s">%s</a>' % (html.escape(link["url"]), kids)
    style = " ; ".join(css)
    if not style:
        style = "display:flex ; flex-direction:column"
    return el(tag, inner_html, style, dev,
              cls="e-con inner" if node.get("isInner") else "e-con root",
              attrs=animation(s, "container"))


# ---------------------------------------------------------------------------
# page shell
# ---------------------------------------------------------------------------

CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
body{margin:0;background:#FFFBF5;color:#57534E;font-family:Inter,system-ui,sans-serif;
  font-size:17px;line-height:1.75;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4,h5,h6{font-family:Sora,"Inter",system-ui,sans-serif;color:#1C1917;margin:0;
  line-height:1.12;letter-spacing:-.02em}
p{margin:0 0 1.05em}
a{color:inherit;text-decoration:none}
img{max-width:100%%;height:auto;display:block}
.e-con{display:flex;flex-wrap:wrap;min-width:0}
.e-con.root{width:100%%}
.c-link{display:contents}
.btn{transition:background .25s ease,color .25s ease,transform .25s ease}
.btn:hover{background:#D98A14 !important;transform:translateY(-1px)}
.txt a{color:#1C1917;text-decoration:underline;text-underline-offset:3px}
.txt>p:last-child{margin-bottom:0}
.icon-list{list-style:none;margin:0;padding:0}
.icon-list li{display:flex;gap:10px;align-items:flex-start}
.icon-list li .ico{flex:0 0 auto;line-height:1.5}
.acc-wrap{display:flex;flex-direction:column;gap:14px;width:100%%}
details.acc{background:#fff;border:1px solid #E8DCCC;border-radius:16px;overflow:hidden}
details.acc summary{display:flex;justify-content:space-between;align-items:center;gap:16px;
  padding:18px 22px;cursor:pointer;list-style:none;font-family:Sora,sans-serif;font-weight:600;
  color:#1C1917}
details.acc summary::-webkit-details-marker{display:none}
details.acc summary i.fa-minus{display:none}
details.acc[open] summary i.fa-plus{display:none}
details.acc[open] summary i.fa-minus{display:inline-block;color:#F4A62A}
details.acc[open] summary{color:#D98A14}
.acc-body{padding:0 22px 22px}
.tab-nav{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.tab{padding:12px 20px;border:1px solid #E8DCCC;background:#fff;border-radius:999px;
  cursor:pointer;font-family:Sora,sans-serif;font-weight:600}
.tab.active{background:#1C1917;color:#fff;border-color:#1C1917}
.tab-panel{display:none;padding-top:22px}
.tab-panel.active{display:block}
.social a{transition:background .2s ease,color .2s ease}
.social a:hover{background:#F4A62A !important;color:#1C1917 !important}
.aurora-form{width:100%%}
.form-grid{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:18px}
.field{display:flex;flex-direction:column;gap:7px}
.field label{font-size:13px;font-weight:600;color:#1C1917;letter-spacing:.02em}
input,textarea,select{width:100%%;padding:15px 17px;border:1px solid #E8DCCC;border-radius:12px;
  font:inherit;background:#fff;color:#1C1917}
input:focus,textarea:focus,select:focus{outline:none;border-color:#F4A62A;
  box-shadow:0 0 0 3px rgba(244,166,42,.18)}
.check{display:flex;gap:10px;align-items:flex-start;font-size:15px;color:#57534E}
.check input{width:auto;margin-top:4px}
.form-btn{padding:16px 28px;background:#F4A62A;color:#1C1917;border:none;border-radius:999px;
  font:inherit;font-weight:600;cursor:pointer;width:100%%}
.inline{display:flex;gap:10px}
.inline input{flex:1}
.logo-mark{display:block;width:100%%;aspect-ratio:1;border-radius:12px;
  background:linear-gradient(135deg,#F4A62A,#EF6C4D)}
.logo-widget{display:flex}
.nav-menu a{color:#1C1917;opacity:.82}
.nav-menu a.active{color:#D98A14;opacity:1}
.crumbs a{text-decoration:none;color:#8C8177}
.counter .num{line-height:1.05}
.counter .lbl{margin-top:6px}
.posts-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;width:100%%}
.post-card{background:#fff;border:1px solid #E8DCCC;border-radius:22px;padding:18px;
  display:flex;flex-direction:column;gap:10px}
.post-card .thumb{aspect-ratio:3/2;border-radius:16px;
  background:linear-gradient(135deg,#FDF0DA,#F3E9DB)}
.post-card h3{font-size:19px}
.post-card p{font-size:15.5px;margin:0}
.post-card .meta,.post-card .more{font-size:12px;letter-spacing:.1em;text-transform:uppercase;
  font-weight:700;color:#D98A14}
.post-card .more{display:inline-flex;gap:8px;align-items:center}
.post-info,.crumbs{font-size:14px}
.prose h2{margin:1.6em 0 .5em;font-size:28px}
.prose blockquote{margin:1.4em 0;padding:18px 24px;border-left:3px solid #F4A62A;
  background:#FAF4EA;border-radius:0 14px 14px 0;font-size:19px;color:#1C1917}
.author-box{display:flex;gap:16px;align-items:flex-start;background:#FAF4EA;border-radius:18px;
  padding:22px;width:100%%}
.author-box .avatar{width:64px;height:64px;border-radius:50%%;flex:0 0 64px;
  background:linear-gradient(135deg,#F4A62A,#EF6C4D)}
.author-box p{margin:6px 0 0;font-size:15px}
.post-nav a{font-weight:600;color:#1C1917}
.comments h3{font-size:22px}
.muted{color:#8C8177}
.testimonial .quote{font-size:18px}
.ib-icon{font-size:26px;color:#D98A14}
.unknown{background:#FDF0DA;border:1px dashed #F4A62A;padding:14px;border-radius:10px;
  font-size:13px;color:#8C8177}
[data-anim]{animation:reveal .7s ease both}
@keyframes reveal{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@media(max-width:1024px){.posts-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:767px){.posts-grid{grid-template-columns:1fr}.form-grid{gap:14px}}
/* preview chrome only */
.pv-bar{position:sticky;top:0;z-index:99;background:#141110;color:#fff;
  display:flex;gap:6px;align-items:center;padding:10px 16px;flex-wrap:wrap;
  font-family:Inter,sans-serif;font-size:13px}
.pv-bar a{color:#A8A29E;padding:6px 11px;border-radius:999px;white-space:nowrap}
.pv-bar a.on,.pv-bar a:hover{background:rgba(244,166,42,.18);color:#F4A62A}
.pv-bar .sp{flex:1}
.pv-note{font-size:12px;color:#57534E;background:#FDF0DA;padding:8px 14px;
  border-radius:8px;margin:14px 16px 0}
"""

SHELL = """<!doctype html>
<html lang="%(lang)s" dir="%(dir)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s - Aurora AI Elementor Kit preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<style>%(css)s</style>
</head>
<body>
<div class="pv-bar">%(nav)s<span class="sp"></span><span style="color:#57534E">preview of the Elementor JSON &mdash; not the deliverable</span></div>
%(body)s
<script>
document.querySelectorAll('.tab').forEach(function(b,i,n){
  b.addEventListener('click',function(){
    var w=b.closest('.tabs-widget');
    w.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active')});
    w.querySelectorAll('.tab-panel').forEach(function(x){x.classList.remove('active')});
    b.classList.add('active');w.querySelectorAll('.tab-panel')[i].classList.add('active');
  });
});
</script>
</body>
</html>
"""

PAGES = [
    ("index", "pages/aurora-home-en", "Home", "en", "ltr"),
    ("home-fa", "pages/aurora-home-fa", "خانه (فارسی)", "fa", "rtl"),
    ("about", "pages/aurora-about", "About", "en", "ltr"),
    ("services", "pages/aurora-services", "Services", "en", "ltr"),
    ("portfolio", "pages/aurora-portfolio", "Case Studies", "en", "ltr"),
    ("pricing", "pages/aurora-pricing", "Pricing", "en", "ltr"),
    ("blog", "pages/aurora-blog", "Journal", "en", "ltr"),
    ("contact", "pages/aurora-contact", "Contact", "en", "ltr"),
    ("404", "pages/aurora-404", "404", "en", "ltr"),
    ("header-footer", "kit/aurora-header-footer-preview", "", "en", "ltr"),
]


def build_preview() -> int:
    os.makedirs(OUT, exist_ok=True)
    nav_html = "".join(
        '<a href="%s.html" class="%s">%s</a>' % (slug, "on" if i == 0 else "", label)
        for i, (slug, _, label, _, _) in enumerate(PAGES) if label
    )

    written = 0
    for slug, rel, label, lang, direction in PAGES:
        path = os.path.join(TEMPLATES, rel + ".json")
        if slug == "header-footer":
            # compose a header/footer showcase
            header = json.load(open(os.path.join(TEMPLATES, "headers/aurora-header-en.json"),
                                    encoding="utf-8"))["content"]
            footer = json.load(open(os.path.join(TEMPLATES, "footers/aurora-footer-en.json"),
                                    encoding="utf-8"))["content"]
            head_fa = json.load(open(os.path.join(TEMPLATES, "headers/aurora-header-fa.json"),
                                     encoding="utf-8"))["content"]
            foot_fa = json.load(open(os.path.join(TEMPLATES, "footers/aurora-footer-fa.json"),
                                     encoding="utf-8"))["content"]
            body = "".join(render_node(n) for n in header)
            body += ('<div class="pv-note">Header above - Footer below. '
                     'Persian (RTL) header and footer follow.</div>')
            body += "".join(render_node(n) for n in footer)
            body += ('<div dir="rtl" style="font-family:Arad,Inter,sans-serif">'
                     + "".join(render_node(n) for n in head_fa)
                     + "".join(render_node(n) for n in foot_fa) + "</div>")
            title = "Header & Footer"
        else:
            if not os.path.exists(path):
                print("  ! missing %s" % rel)
                continue
            data = json.load(open(path, encoding="utf-8"))
            body = "".join(render_node(n) for n in data["content"])
            title = data["title"]

        out = os.path.join(OUT, slug + ".html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(SHELL % {
                "title": html.escape(title), "lang": lang, "dir": direction,
                "css": CSS, "nav": nav_html, "body": body,
            })
        written += 1
        print("  %-16s %s" % (slug + ".html", title))

    print("  preview written: %d pages -> preview/" % written)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    args = ap.parse_args()
    print("Aurora AI - design preview")
    build_preview()
    if args.serve:
        import http.server
        import socketserver
        os.chdir(OUT)
        with socketserver.TCPServer(("0.0.0.0", 8080), http.server.SimpleHTTPRequestHandler) as httpd:
            print("  serving http://0.0.0.0:8080")
            httpd.serve_forever()
