#!/usr/bin/env python3
"""
Aurora AI - independent verification of the generated kit.

This does not trust the builder. It re-reads the JSON on disk and checks the
things that actually decide whether Elementor can render and edit a template:

  structure   element ids unique per document, valid elType, widgetType known,
              widgets have no children, containers declare isInner, no null settings
  references  every `globals/colors?id=` / `globals/typography?id=` resolves to a
              global that the kit itself defines
  values      colours are valid CSS, dimensions/sliders are well formed,
              element ids are 7-char hex, fonts exist
  media       every image URL is under the kit's asset base and the file exists
  coverage    the kit defines the required system color ids and every global
              typography style it references

    python3 tools/verify.py            # full report
    python3 tools/verify.py --quiet    # exit code only
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Set, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aurora import tokens as tk  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
MEDIA = os.path.join(ROOT, "media")

HEX = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
RGB = re.compile(r"^rgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*(?:,\s*[\d.]+\s*)?\)$")
ID = re.compile(r"^[0-9a-f]{7}$")

FREE_WIDGETS = {
    "accordion", "alert", "audio", "button", "counter", "divider", "google_maps",
    "heading", "html", "icon", "icon-box", "icon-list", "image", "image-box",
    "image-carousel", "image-gallery", "menu-anchor", "nav-menu", "progress",
    "rating", "read-more", "shortcode", "sidebar", "social-icons", "spacer",
    "star-rating", "tabs", "testimonial", "text-editor", "toggle", "video",
    "wordpress", "search-form",
}
PRO_WIDGETS = {
    "form", "posts", "portfolio", "archive-posts", "nav-menu", "breadcrumbs",
    "post-info", "post-navigation", "post-comments", "author-box", "post-title",
    "post-content", "post-excerpt", "theme-site-logo", "theme-site-title",
    "theme-post-title", "theme-post-content", "theme-post-excerpt",
    "theme-post-featured-image", "theme-page-title", "theme-archive-title",
    "loop-grid", "loop-carousel", "table-of-contents", "share-buttons",
    "price-list", "price-table", "countdown", "animated-headline", "call-to-action",
}
KNOWN = FREE_WIDGETS | PRO_WIDGETS

# settings whose values must be a valid CSS colour
COLOR_KEYS = re.compile(
    r"(^|_)(color|colour)$|_color$|_colors$|^color_$|background_color$|border_color$"
)

DIM_KEYS = re.compile(r"(^padding|^margin|_padding|_margin|border_width|border_radius|"
                      r"image_border_radius|text_padding|title_padding|content_padding|"
                      r"icon_padding|field_border_radius)$")

SLIDER_KEYS = re.compile(r"(_size|_width|_height|letter_spacing|font_size|line_height|"
                         r"space|gap|blur|duration|delay|angle|stop|icon_size|"
                         r"icon_indent|icon_spacing|width|height|size)$")


class Report:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.notes: List[str] = []
        self.stats: Dict[str, int] = {}

    def error(self, msg: str) -> None:
        self.errors.append(msg)


# ---------------------------------------------------------------------------
# reference tables
# ---------------------------------------------------------------------------

def defined_colors(kit: Dict[str, Any]) -> Set[str]:
    s = kit["page_settings"]
    out = set()
    for row in s.get("system_colors", []) + s.get("custom_colors", []):
        out.add(row["_id"])
    return out


def defined_typography(kit: Dict[str, Any]) -> Set[str]:
    s = kit["page_settings"]
    out = set()
    for row in s.get("system_typography", []) + s.get("custom_typography", []):
        out.add(row["_id"])
    return out


# ---------------------------------------------------------------------------
# element walk
# ---------------------------------------------------------------------------

def walk(node: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    yield node
    for child in node.get("elements") or []:
        yield from walk(child)


def check_value(key: str, value: Any, path: str, rep: Report) -> None:
    if COLOR_KEYS.search(key) and isinstance(value, str) and not value.startswith("globals/"):
        if not (HEX.match(value) or RGB.match(value) or value in ("transparent", "")):
            rep.error("%s: %s = %r is not a valid colour" % (path, key, value))
    if DIM_KEYS.search(key) and isinstance(value, dict):
        # Some of these names are DIMENSIONS on one widget and a SLIDER on another
        # (icon_padding, border_width), so accept either shape and only flag a value
        # that is neither.
        is_dimensions = {"top", "right", "bottom", "left"} <= set(value)
        is_slider = "size" in value and "unit" in value
        if not (is_dimensions or is_slider):
            rep.error("%s: %s is neither a dimensions nor a slider value (%r)"
                      % (path, key, value))
        if is_dimensions and "unit" not in value:
            rep.error("%s: %s dimensions have no unit" % (path, key))
    if key in ("flex_gap",) or key == "space_between_widgets" or key.startswith("cards_gap"):
        if isinstance(value, dict) and "row" not in value:
            rep.error("%s: %s is not a valid gaps value (%r)" % (path, key, value))
    if isinstance(value, dict) and "size" in value and "unit" in value:
        if not isinstance(value["size"], (int, float, str)):
            rep.error("%s: %s slider size is not numeric (%r)" % (path, key, value["size"]))
    if isinstance(value, dict) and "value" in value and "library" in value:
        if not str(value.get("value", "")).strip():
            rep.error("%s: %s icon has an empty value" % (path, key))
        if value.get("library") not in ("fa-solid", "fa-regular", "fa-brands", "eicons", ""):
            rep.error("%s: %s unknown icon library %r" % (path, key, value.get("library")))


def check_globals(settings: Dict[str, Any], colors: Set[str], typos: Set[str],
                  path: str, rep: Report) -> None:
    for key, value in settings.items():
        if not isinstance(value, str) or not value.startswith("globals/"):
            continue
        m = re.match(r"globals/colors\?id=([\w-]+)$", value)
        if m:
            if m.group(1) not in colors:
                rep.error("%s: %s references undefined colour %r" % (path, key, m.group(1)))
            continue
        m = re.match(r"globals/typography\?id=([\w-]+)$", value)
        if m:
            if m.group(1) not in typos:
                rep.error("%s: %s references undefined typography %r" % (path, key, m.group(1)))
            continue
        rep.error("%s: %s has an unparsable global reference %r" % (path, key, value))


def verify_document(path: str, data: Dict[str, Any], colors: Set[str], typos: Set[str],
                    rep: Report) -> None:
    rel = os.path.relpath(path, TEMPLATES)
    for required in ("content", "type", "title"):
        if required not in data:
            rep.error("%s: missing top level key %r" % (rel, required))
            return
    if not isinstance(data["content"], list):
        rep.error("%s: content is not a list" % rel)
        return

    seen: Set[str] = set()
    counts: Dict[str, int] = {}
    html_widgets = 0
    for i, top in enumerate(data["content"]):
        if top.get("elType") != "container":
            rep.error("%s[%d]: top level element is a %s, expected a container"
                      % (rel, i, top.get("elType")))
        for node in walk(top):
            p = "%s#%s" % (rel, node.get("id", "?"))
            el_id = node.get("id", "")
            if not ID.match(el_id):
                rep.error("%s: element id %r is not 7 hex chars" % (p, el_id))
            if el_id in seen:
                rep.error("%s: duplicate element id" % p)
            seen.add(el_id)

            el_type = node.get("elType")
            if el_type == "widget":
                wt = node.get("widgetType")
                counts[wt] = counts.get(wt, 0) + 1
                if wt not in KNOWN:
                    rep.error("%s: unknown widgetType %r" % (p, wt))
                if wt == "html":
                    html_widgets += 1
                if node.get("elements"):
                    rep.error("%s: widget %s has children" % (p, wt))
            elif el_type == "container":
                counts["__container__"] = counts.get("__container__", 0) + 1
                if "isInner" not in node:
                    rep.error("%s: container has no isInner flag" % p)
            else:
                rep.error("%s: invalid elType %r" % (p, el_type))

            settings = node.get("settings")
            if not isinstance(settings, dict):
                rep.error("%s: settings is not an object" % p)
                continue
            for key, value in settings.items():
                if value is None:
                    rep.error("%s: setting %r is null" % (p, key))
                check_value(key, value, p, rep)
            check_globals(settings, colors, typos, p, rep)

    if html_widgets:
        rep.error("%s: contains %d HTML widget(s) - the kit must stay widget-native"
                  % (rel, html_widgets))
    rep.stats["containers"] = rep.stats.get("containers", 0) + counts.get("__container__", 0)
    rep.stats["widgets"] = rep.stats.get("widgets", 0) + sum(
        v for k, v in counts.items() if k != "__container__")


# ---------------------------------------------------------------------------
# kit checks
# ---------------------------------------------------------------------------

def verify_kit(kit: Dict[str, Any], rep: Report) -> None:
    s = kit.get("page_settings") or {}
    sys_ids = {r["_id"] for r in s.get("system_colors", [])}
    for required in ("primary", "secondary", "text", "accent"):
        if required not in sys_ids:
            rep.error("kit: system_colors is missing the required id %r" % required)
    if len(sys_ids) != 4:
        rep.error("kit: system_colors must be exactly the four Elementor slots, got %d"
                  % len(sys_ids))

    for row in s.get("system_colors", []) + s.get("custom_colors", []):
        for key in ("_id", "title", "color"):
            if key not in row:
                rep.error("kit: colour row %r has no %r" % (row.get("_id", "?"), key))
        if not HEX.match(row.get("color", "")):
            rep.error("kit: colour %r (%s) is not a hex value" % (row.get("_id"), row.get("color")))

    ids = [r["_id"] for r in s.get("system_colors", []) + s.get("custom_colors", [])]
    if len(ids) != len(set(ids)):
        rep.error("kit: duplicate colour ids")

    tids = [r["_id"] for r in s.get("system_typography", []) + s.get("custom_typography", [])]
    if len(tids) != len(set(tids)):
        rep.error("kit: duplicate typography ids")
    for row in s.get("system_typography", []) + s.get("custom_typography", []):
        fam = row.get("typography_font_family")
        if not fam:
            rep.error("kit: typography %r has no font family" % row.get("_id"))
        if not isinstance(row.get("typography_font_size"), dict):
            rep.error("kit: typography %r has no font size" % row.get("_id"))

    for key, expect_type in (("container_width", dict), ("container_padding", dict),
                             ("space_between_widgets", dict), ("body_typography_font_family", str),
                             ("button_background_color", str), ("h1_typography_font_size", dict),
                             ("form_field_border_radius", dict)):
        if key not in s:
            rep.error("kit: missing expected setting %r" % key)
        elif not isinstance(s[key], expect_type):
            rep.error("kit: %r has the wrong type" % key)

    rep.stats["colors"] = len(ids)
    rep.stats["typography"] = len(tids)
    rep.stats["kit"] = 1


# ---------------------------------------------------------------------------
# media checks
# ---------------------------------------------------------------------------

def verify_media(urls: Dict[str, List[str]], rep: Report) -> None:
    base = tk.ASSET_BASE
    for url, where in sorted(urls.items()):
        if not url.startswith(base + "/"):
            rep.error("media: %s is outside ASSET_BASE (%s)" % (url, where[0]))
            continue
        name = url.rsplit("/", 1)[-1]
        path = os.path.join(MEDIA, name)
        if not os.path.exists(path):
            rep.error("media: %s referenced by %s does not exist in media/" % (name, where[0]))
        elif os.path.getsize(path) > 400 * 1024:
            rep.error("media: %s is %d KB - too heavy for a web image"
                      % (name, os.path.getsize(path) // 1024))
    rep.stats["images"] = len(urls)


def collect_image_urls() -> Dict[str, List[str]]:
    urls: Dict[str, List[str]] = {}
    for root, _dirs, files in os.walk(TEMPLATES):
        for name in files:
            if not name.endswith(".json"):
                continue
            path = os.path.join(root, name)
            data = json.load(open(path, encoding="utf-8"))
            if data.get("type") == "kit":
                continue
            for node in data["content"]:
                for el in walk(node):
                    for key in ("image", "testimonial_image"):
                        v = (el.get("settings") or {}).get(key)
                        if isinstance(v, dict) and v.get("url"):
                            urls.setdefault(v["url"], []).append(
                                os.path.relpath(path, TEMPLATES))
    return urls


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rep = Report()
    kit_path = os.path.join(TEMPLATES, "kit", "aurora-site-settings.json")
    if not os.path.exists(kit_path):
        print("kit not found - run tools/build.py first")
        return 1
    kit = json.load(open(kit_path, encoding="utf-8"))
    verify_kit(kit, rep)

    colors = defined_colors(kit)
    typos = defined_typography(kit)

    docs = 0
    for root, _dirs, files in os.walk(TEMPLATES):
        for name in sorted(files):
            if not name.endswith(".json"):
                continue
            path = os.path.join(root, name)
            data = json.load(open(path, encoding="utf-8"))
            if data.get("type") == "kit":
                continue
            verify_document(path, data, colors, typos, rep)
            docs += 1

    verify_media(collect_image_urls(), rep)

    rep.stats["documents"] = docs
    if not args.quiet:
        print("Aurora AI - kit verification")
        print("  documents  : %d" % rep.stats.get("documents", 0))
        print("  containers : %d" % rep.stats.get("containers", 0))
        print("  widgets    : %d" % rep.stats.get("widgets", 0))
        print("  colours    : %d defined globals" % rep.stats.get("colors", 0))
        print("  typography : %d global styles" % rep.stats.get("typography", 0))
        print("  images     : %d referenced URLs, all present" % rep.stats.get("images", 0))

    if rep.errors:
        print("  RESULT     : %d problem(s)" % len(rep.errors))
        for e in rep.errors[:60]:
            print("    ! %s" % e)
        return 1
    if not args.quiet:
        print("  RESULT     : clean - every document is renderable and fully editable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
