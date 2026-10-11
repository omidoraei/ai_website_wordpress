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
import collections
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

# non-empty assertions (docs/METRICS.md §3): a scanner that examines nothing must fail
MEDIA_FLOOR = 3
BANLIST_FLOORS = {"documents": 30, "sections": 50, "elements": 500}

FACT_TABLE_KEYS = ("documents_total", "template_documents", "kit_documents", "pages",
                   "blocks", "headers", "footers", "loop_templates", "popups",
                   "theme_builder_layouts", "fa_documents", "containers", "widgets",
                   "global_colours", "typography_styles", "font_families",
                   "image_widgets", "images", "custom_html_widgets")

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
    if len(urls) < MEDIA_FLOOR:
        rep.error("media: only %d image URL(s) examined, floor is %d - non-empty assertion "
                  "failed (docs/METRICS.md)" % (len(urls), MEDIA_FLOOR))
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
# generated facts (rule B: numbers in docs come from here, never from a hand)
# ---------------------------------------------------------------------------

FACT_FILES = ("README.md", "CHANGELOG.md", "docs/01-installation.md",
              "docs/02-design-system.md", "docs/03-template-library.md",
              "docs/04-rtl-persian-setup.md", "docs/05-theme-builder.md",
              "docs/06-performance-accessibility.md", "docs/07-faq-troubleshooting.md",
              "docs/METRICS.md", "docs/capability-matrix.md")

# (regex, fact key, human label). The number may contain spaces as a thousands
# separator ("1 280 widgets") because the docs use that style.
DOC_NUMBERS = (
    (r"(\d[\d\s\u00a0]{0,9})\s+Elementor documents", "documents_total", "Elementor documents"),
    (r"(\d[\d\s\u00a0]{0,9})\s+documents\b", "documents_total", "documents"),
    (r"(\d[\d\s\u00a0]{0,9})\s+importable templates", "template_documents", "importable templates"),
    (r"(\d[\d\s\u00a0]{0,9})\s+templates\b", "template_documents", "templates"),
    (r"(\d[\d\s\u00a0]{0,9})\s+containers", "containers", "containers"),
    (r"(\d[\d\s\u00a0]{0,9})\s+widgets", "widgets", "widgets"),
    (r"(\d[\d\s\u00a0]{0,9})\s+global (?:colours|colors)", "global_colours", "global colours"),
    (r"(\d[\d\s\u00a0]{0,9})\s+(?:global )?typography styles", "typography_styles",
     "typography styles"),
    (r"(\d[\d\s\u00a0]{0,9})\s+system (?:colours|colors)", "system_colours",
     "system colours"),
    (r"(\d[\d\s\u00a0]{0,9})\s+custom (?:colours|colors)", "custom_colours",
     "custom colours"),
    (r"(\d[\d\s\u00a0]{0,9})\s+reusable section blocks", "blocks", "reusable section blocks"),
    (r"(\d[\d\s\u00a0]{0,9})\s+font families", "font_families", "font families"),
    (r"(\d[\d\s\u00a0]{0,9})\s+image widgets", "image_widgets", "image widgets"),
    (r"(\d[\d\s\u00a0]{0,9})\s+pages\b", "pages", "pages"),
    (r"(\d[\d\s\u00a0]{0,9})\s+section blocks", "blocks", "section blocks"),
    (r"(\d[\d\s\u00a0]{0,9})\s+Theme Builder layouts", "theme_builder_layouts",
     "Theme Builder layouts"),
    (r"\((\d[\d\s\u00a0]{0,9})\s+total\)", "global_colours", "colours (X total)"),
)

# A number is generated only when it sits inside a slot: <!--f:key-->N<!--/f-->.
SLOT_SPAN = re.compile(r"<!--f:[a-z_]+-->.*?<!--/f-->", re.S)
SLOT_SPAN_GROUPED = re.compile(r"<!--f:([a-z_]+)-->(.*?)<!--/f-->", re.S)


def _document_files() -> List[Tuple[str, Dict[str, Any]]]:
    """Every *.json under templates/, as (path relative to templates/, data), sorted."""
    out = []
    for root, _dirs, names in os.walk(TEMPLATES):
        for name in sorted(names):
            if not name.endswith(".json"):
                continue
            path = os.path.join(root, name)
            out.append((os.path.relpath(path, TEMPLATES),
                        json.load(open(path, encoding="utf-8"))))
    return sorted(out, key=lambda pair: pair[0])


def _folder(rel: str) -> str:
    return rel.split(os.sep)[0] if os.sep in rel else ""


def _is_fa(rel: str) -> bool:
    base = os.path.basename(rel)
    return base.startswith("fa-") or base.endswith("-fa.json")


def compute_facts(kit: Dict[str, Any]) -> Dict[str, Any]:
    """The canonical counters - definitions in docs/METRICS.md. Never hand-count again."""
    docs = _document_files()
    templates = [(r, d) for r, d in docs if d.get("type") != "kit"]
    kits = [(r, d) for r, d in docs if d.get("type") == "kit"]
    containers = 0
    widget_mix: Dict[str, int] = {}
    for _rel, data in templates:
        for top in data.get("content") or []:
            for node in walk(top):
                if node.get("elType") == "container":
                    containers += 1
                elif node.get("elType") == "widget":
                    wt = node.get("widgetType", "?")
                    widget_mix[wt] = widget_mix.get(wt, 0) + 1
    by_folder = collections.Counter(_folder(rel) for rel, _ in templates)
    s = kit["page_settings"]
    families = sorted({
        row.get("typography_font_family")
        for row in (s.get("system_typography") or []) + (s.get("custom_typography") or [])
        if row.get("typography_font_family")
    })
    return {
        "documents_total": len(templates) + len(kits),
        "template_documents": len(templates),
        "kit_documents": len(kits),
        "containers": containers,
        "widgets": sum(widget_mix.values()),
        "widget_mix": dict(sorted(widget_mix.items(), key=lambda kv: (-kv[1], kv[0]))),
        "custom_html_widgets": widget_mix.get("html", 0),
        "image_widgets": widget_mix.get("image", 0),
        "images": len(collect_image_urls()),
        "global_colours": len(defined_colors(kit)),
        "system_colours": len(s.get("system_colors") or []),
        "custom_colours": len(s.get("custom_colors") or []),
        "system_typography_styles": len(s.get("system_typography") or []),
        "custom_typography_styles": len(s.get("custom_typography") or []),
        "typography_styles": len(defined_typography(kit)),
        "font_families": len(families),
        "font_family_names": families,
        "pages": by_folder.get("pages", 0),
        "blocks": by_folder.get("blocks", 0),
        "headers": by_folder.get("headers", 0),
        "footers": by_folder.get("footers", 0),
        "loop_templates": by_folder.get("loop", 0),
        "popups": by_folder.get("popups", 0),
        "theme_builder_layouts": (by_folder.get("headers", 0) + by_folder.get("footers", 0)
                                  + by_folder.get("loop", 0)),
        "fa_documents": sum(1 for rel, _ in templates if _is_fa(rel)),
        "blocks_fa": sum(1 for rel, _ in templates
                         if _folder(rel) == "blocks" and _is_fa(rel)),
    }


def _norm(value: str) -> str:
    return re.sub(r"[\s\u00a0]", "", value)


def check_doc_numbers(facts: Dict[str, Any], rep: Report) -> int:
    """Two legal states for a number in a doc: inside a generated slot, or absent.

    - a slot must hold the value the build produced (else run tools/render_docs.py)
    - a bare metric number is a hand-typed number: it is an error even when it happens
      to be correct today, because nothing regenerates it tomorrow.
    """
    checked = 0
    for rel in FACT_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        spans = []
        for m in SLOT_SPAN_GROUPED.finditer(text):
            key, inner = m.group(1), m.group(2)
            spans.append((m.start(), m.end()))
            line = text[:m.start()].count("\n") + 1
            checked += 1
            if key not in facts:
                rep.error("%s:%d uses unknown fact key %r" % (rel, line, key))
            elif _norm(inner) != _norm(str(facts[key])):
                rep.error("%s:%d slot %s holds %r but the build has %r "
                          "(run tools/render_docs.py)" % (rel, line, key, inner, facts[key]))
        for pattern, key, label in DOC_NUMBERS:
            expected = facts.get(key)
            if expected is None:
                continue
            for match in re.finditer(pattern, text):
                if any(a <= match.start() < b for a, b in spans):
                    continue
                stated = int(_norm(match.group(1)))
                line = text[:match.start()].count("\n") + 1
                checked += 1
                if stated != expected:
                    rep.error("%s:%d states %d %s but the build has %d "
                              "(run tools/verify.py --report && tools/render_docs.py)"
                              % (rel, line, stated, label, expected))
                else:
                    rep.error("%s:%d has a hand-typed %s (%d) - wrap the number as "
                              "<!--f:%s-->%d<!--/f--> and run tools/render_docs.py"
                              % (rel, line, label, stated, key, stated))
    if checked == 0:
        rep.error("doc numbers: 0 claims examined - non-empty assertion failed")
    return checked


def write_facts(facts: Dict[str, Any]) -> str:
    out_dir = os.path.join(ROOT, "docs", "_generated")
    os.makedirs(out_dir, exist_ok=True)
    rows = [
        "# Generated facts",
        "",
        "**Do not edit.** Written by `python3 tools/verify.py --report` from the JSON in",
        "`templates/`. Every number quoted in README, CHANGELOG and docs/ must match this file.",
        "",
        "| fact | value |",
        "| --- | ---: |",
    ]
    for key in FACT_TABLE_KEYS:
        rows.append("| `%s` | %s |" % (key, facts[key]))
    rows += ["", "## Widget mix", "", "| widget | count |", "| --- | ---: |"]
    for name, count in facts["widget_mix"].items():
        rows.append("| `%s` | %d |" % (name, count))
    rows.append("")
    with open(os.path.join(out_dir, "facts.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows))
    with open(os.path.join(out_dir, "facts.json"), "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=1, sort_keys=True)
    return os.path.relpath(os.path.join(out_dir, "facts.md"), ROOT)


# ---------------------------------------------------------------------------

def banlist_advisory(strict: bool, rep: "Report") -> Dict[str, int]:
    """Run BANLIST.md detectors (tools/banlist_check.py) and report the counts.

    P1 is diagnosis-only, so the current kit is EXPECTED to trip FAIL-level rules
    (they are the P2 worklist in docs/p1/delta-table.md). The enforcement path is
    real: `--strict-banlist` turns every FAIL-level hit into a verifier error, and
    CI flips to that flag the moment P2 empties the list.
    """
    import importlib
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        banlist = importlib.import_module("banlist_check")
    except Exception as exc:  # pragma: no cover
        rep.error("banlist_check.py could not be imported: %s" % exc)
        return {}
    violations, stats = banlist.run_rules()
    fails = {k: len(v) for k, v in violations.items() if k in banlist.FAIL_RULES}
    warns = {k: len(v) for k, v in violations.items() if k not in banlist.FAIL_RULES}
    if strict:
        for rule, count in fails.items():
            rep.error("BANLIST %s: %d violation(s) - see BANLIST.md" % (rule, count))
    return {"stats": stats, "fail": fails, "warn": warns}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--strict-banlist", action="store_true",
                    help="treat BANLIST FAIL-level violations as errors (P2 target)")
    ap.add_argument("--report", action="store_true",
                    help="write docs/_generated/facts.md from the current build, then verify")
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

    facts = compute_facts(kit)
    if args.report:
        path = write_facts(facts)
        if not args.quiet:
            print("  facts      : wrote %s" % path)
    checked = check_doc_numbers(facts, rep)

    ban = banlist_advisory(args.strict_banlist, rep)
    for key, floor in sorted(BANLIST_FLOORS.items()):
        seen = ban.get("stats", {}).get(key)
        if seen is None or seen < floor:
            rep.error("banlist: examined %s %s, floor is %d - non-empty assertion failed"
                      % (seen, key, floor))
    rep.stats["documents"] = docs
    if not args.quiet:
        print("Aurora AI - kit verification")
        print("  documents  : %d" % rep.stats.get("documents", 0))
        print("  containers : %d" % rep.stats.get("containers", 0))
        print("  widgets    : %d" % rep.stats.get("widgets", 0))
        print("  colours    : %d defined globals" % rep.stats.get("colors", 0))
        print("  typography : %d global styles" % rep.stats.get("typography", 0))
        print("  images     : %d referenced URLs, all present" % rep.stats.get("images", 0))
        print("  doc numbers: %d claims checked against generated facts" % checked)
        if ban:
            bs = ban["stats"]
            print("  banlist    : eyebrow %.0f%% of sections | centred %.0f%% | animated %.0f%%"
                  % (100 * bs.get("eyebrow_ratio", 0), 100 * bs.get("centred_ratio", 0),
                     100 * bs.get("animated_ratio", 0)))
            print("               FAIL rules tripped: %s"
                  % (", ".join("%s x%d" % (k, v) for k, v in sorted(ban["fail"].items()))
                     or "none"))
            print("               WARN rules tripped: %s"
                  % (", ".join("%s x%d" % (k, v) for k, v in sorted(ban["warn"].items()))
                     or "none"))

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
