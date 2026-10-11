"""
Aurora AI - build the whole Elementor template kit.

    python3 tools/build.py             # write templates/, dist/ and the index
    python3 tools/build.py --check     # validate only, write nothing

Outputs
-------
templates/**.json              one Elementor template JSON per document
templates/INDEX.md             generated catalogue of every template
dist/aurora-ai-templates.zip   flat ZIP  -> Elementor > Templates > Import Templates
dist/aurora-ai-kit.zip         kit ZIP   -> Elementor > Site Settings > Import/Export
dist/site-settings.json        the raw Kit payload for automation
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aurora import kit as kit_mod
from aurora import pages, sections, theme_parts, tokens as tk
from aurora.dsl import Doc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
if not os.path.isdir(os.path.join(ROOT, "templates")):
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Elementor widget inventory (used for validation)
# ---------------------------------------------------------------------------

FREE_WIDGETS = {
    "accordion", "alert", "audio", "button", "counter", "divider", "google_maps",
    "heading", "html", "icon", "icon-box", "icon-list", "image", "image-box",
    "image-carousel", "image-gallery", "menu-anchor", "nav-menu", "progress",
    "rating", "read-more", "shortcode", "sidebar", "social-icons", "spacer",
    "star-rating", "tabs", "testimonial", "text-editor", "toggle", "video",
    "wordpress", "sidebar", "search-form", "text-path", "blockquote", "reviews",
}
PRO_WIDGETS = {
    "nav-menu", "form", "posts", "portfolio", "archive-posts", "post-title",
    "post-content", "post-excerpt", "post-info", "post-comments", "post-navigation",
    "author-box", "breadcrumbs", "theme-post-title", "theme-post-content",
    "theme-post-excerpt", "theme-post-featured-image", "theme-page-title",
    "theme-archive-title", "theme-site-logo", "theme-site-title", "theme-post-comments-form",
    "table-of-contents", "price-list", "price-table", "countdown", "progress-tracker",
    "paypal-button", "stripe-button", "share-buttons", "blockquote", "animated-headline",
    "call-to-action", "flip-box", "hotspot", "lottie", "slides", "gallery",
    "media-carousel", "review", "reviews", "loop-carousel", "loop-grid",
}
THEME_WIDGETS = {
    "theme-site-logo", "theme-site-title", "theme-page-title", "theme-archive-title",
    "theme-post-title", "theme-post-content", "theme-post-excerpt",
    "theme-post-featured-image", "theme-post-comments-form",
}
KNOWN_WIDGETS = FREE_WIDGETS | PRO_WIDGETS | THEME_WIDGETS

# ---------------------------------------------------------------------------
# Document registry
# ---------------------------------------------------------------------------

# (relative path, template type, title, generator)
DOCS: List[Tuple[str, str, str, Callable[[Doc], Any]]] = [
    # ---- Pages -----------------------------------------------------------
    ("pages/aurora-home-en", "page", "Aurora | Home (English)", pages.home),
    ("pages/aurora-home-fa", "page", "Aurora | Home (Persian / RTL)", pages.home_fa),
    ("pages/aurora-about", "page", "Aurora | About", pages.about),
    ("pages/aurora-services", "page", "Aurora | Services", pages.services),
    ("pages/aurora-portfolio", "page", "Aurora | Case Studies", pages.portfolio),
    ("pages/aurora-pricing", "page", "Aurora | Pricing", pages.pricing),
    ("pages/aurora-blog", "page", "Aurora | Journal", pages.blog),
    ("pages/aurora-contact", "page", "Aurora | Contact", pages.contact),
    ("pages/aurora-404", "page", "Aurora | 404 Not Found", pages.not_found),
    # ---- Theme Builder ---------------------------------------------------
    ("headers/aurora-header-en", "header", "Aurora | Header (English)", theme_parts.header),
    ("footers/aurora-footer-en", "footer", "Aurora | Footer (English)", theme_parts.footer),
    ("loop/aurora-single-post", "single", "Aurora | Single Post", theme_parts.single_post),
    ("loop/aurora-archive", "archive", "Aurora | Blog Archive", theme_parts.archive),
    ("loop/aurora-search-results", "search-results", "Aurora | Search Results",
     theme_parts.search_results),
    # ---- Popups ----------------------------------------------------------
    ("popups/aurora-lead-magnet", "popup", "Aurora | Popup - AI Readiness Checklist",
     theme_parts.popup),
]

# Persian / RTL variants (header + footer use the fa flag)
FA_DOCS = [
    ("headers/aurora-header-fa", "header", "Aurora | سربرگ (فارسی)"),
    ("footers/aurora-footer-fa", "footer", "Aurora | پابرگ (فارسی)"),
]

# Reusable blocks: (path, title, builder)
BLOCKS: List[Tuple[str, str, Callable[[Doc], Any]]] = [
    ("blocks/hero-split", "Block | Hero - Split with product shot", sections.hero_split),
    ("blocks/logo-cloud", "Block | Logo Cloud - Trusted by", sections.logo_cloud),
    ("blocks/feature-grid", "Block | Feature Grid - Six icon cards", sections.feature_grid),
    ("blocks/feature-zigzag", "Block | Feature Zigzag - Two alternating rows",
     sections.feature_zigzag),
    ("blocks/stats-band", "Block | Stats Band - Dark counters", sections.stats_band),
    ("blocks/capability-cards", "Block | Capability Cards - Three services",
     sections.capability_cards),
    ("blocks/process-steps", "Block | Process Steps - Four numbered stages",
     sections.process_steps),
    ("blocks/case-studies", "Block | Case Studies - Three cards", sections.case_studies),
    ("blocks/testimonials", "Block | Testimonials - Three quotes", sections.testimonials),
    ("blocks/pricing-table", "Block | Pricing Table - Three plans", sections.pricing_table),
    ("blocks/faq-accordion", "Block | FAQ - Accordion", sections.faq_accordion),
    ("blocks/cta-band", "Block | Call To Action - Gradient card", sections.cta_band),
    ("blocks/team-grid", "Block | Team Grid - Four members", sections.team_grid),
    ("blocks/contact-section", "Block | Contact - Form + details", sections.contact_section),
    ("blocks/newsletter-band", "Block | Newsletter - Subscribe", sections.newsletter_band),
    ("blocks/content-two-column", "Block | Content - Two column story",
     sections.content_two_column),
    ("blocks/page-hero", "Block | Page Hero - Inner page header", sections.page_hero),
]

FA_BLOCKS = [
    ("blocks/fa-hero-split", "Block | قهرمان - دوقسمتی", lambda d: sections.hero_split(d, fa=True)),
    ("blocks/fa-feature-grid", "Block | شبکه ویژگیها (فارسی)",
     lambda d: sections.feature_grid(d, fa=True)),
    ("blocks/fa-pricing-table", "Block | جدول قیمت (فارسی)",
     lambda d: sections.pricing_table(d, fa=True)),
    ("blocks/fa-faq-accordion", "Block | پرسشهای پرتکرار (فارسی)",
     lambda d: sections.faq_accordion(d, fa=True)),
    ("blocks/fa-cta-band", "Block | فراخوان به اقدام (فارسی)",
     lambda d: sections.cta_band(d, fa=True)),
]

PAGE_SETTINGS = pages.page_settings

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?$")


class Issues:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def _walk(node: Dict[str, Any], path: str, issues: Issues, seen: Dict[str, str],
          counter: Dict[str, int]) -> None:
    el_id = node.get("id", "")
    if not el_id:
        issues.error("%s: element without id" % path)
    elif el_id in seen:
        issues.error("%s: duplicate element id %s (also at %s)" % (path, el_id, seen[el_id]))
    else:
        seen[el_id] = path

    el_type = node.get("elType")
    if el_type not in ("container", "widget"):
        issues.error("%s: bad elType %r" % (path, el_type))

    if el_type == "widget":
        wt = node.get("widgetType")
        counter[wt] = counter.get(wt, 0) + 1
        if wt not in KNOWN_WIDGETS:
            issues.error("%s: unknown widgetType %r" % (path, wt))
        if node.get("elements"):
            issues.error("%s: widget %s must have no children" % (path, wt))
    else:
        counter["container"] = counter.get("container", 0) + 1
        if "isInner" not in node:
            issues.error("%s: container missing isInner" % path)

    for key, value in (node.get("settings") or {}).items():
        if value is None:
            issues.error("%s: setting %r is None" % (path, key))

    for i, child in enumerate(node.get("elements") or []):
        _walk(child, "%s/%s[%d]" % (path, el_type, i), issues, seen, counter)


def validate(doc_slug: str, content: Sequence[Dict[str, Any]]) -> Tuple[Issues, Dict[str, int]]:
    issues = Issues()
    if not content:
        issues.error("%s: empty content" % doc_slug)
    seen: Dict[str, str] = {}
    counter: Dict[str, int] = {}
    for i, node in enumerate(content):
        _walk(node, "%s[%d]" % (doc_slug, i), issues, seen, counter)
    return issues, counter


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------

def elementor_payload(content: Sequence[Dict[str, Any]], title: str, doc_type: str,
                      page_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "content": list(content),
        "page_settings": page_settings or {},
        "version": "0.4",
        "title": title,
        "type": doc_type,
    }


def build(check_only: bool = False) -> int:
    out_templates = os.path.join(ROOT, "templates")
    out_dist = os.path.join(ROOT, "dist")
    if not check_only:
        for d in ("pages", "blocks", "headers", "footers", "loop", "popups", "kit"):
            os.makedirs(os.path.join(out_templates, d), exist_ok=True)
        os.makedirs(out_dist, exist_ok=True)

    files: List[Tuple[str, Dict[str, Any]]] = []
    index: List[Dict[str, Any]] = []
    total_issues = Issues()
    counter: Dict[str, int] = {}

    def emit(rel: str, doc_type: str, title: str, generator: Callable[[Doc], Any],
             page_settings: Optional[Dict[str, Any]] = None) -> None:
        slug = os.path.basename(rel)
        doc = Doc(slug, title, doc_type)
        result = generator(doc)
        if isinstance(result, list):
            content = result
        else:
            content = [result]

        issues, counts = validate(slug, content)
        total_issues.errors.extend(issues.errors)
        total_issues.warnings.extend(issues.warnings)
        for k, v in counts.items():
            counter[k] = counter.get(k, 0) + v

        payload = elementor_payload(content, title, doc_type, page_settings)
        files.append((rel + ".json", payload))
        index.append({
            "path": rel + ".json",
            "type": doc_type,
            "title": title,
            "containers": counts.get("container", 0),
            "widgets": sum(v for k, v in counts.items() if k != "container"),
            "widget_types": sorted(k for k in counts if k != "container"),
        })

    for rel, doc_type, title, generator in DOCS:
        emit(rel, doc_type, title, generator, PAGE_SETTINGS())

    # Persian header / footer
    emit(FA_DOCS[0][0], FA_DOCS[0][1], FA_DOCS[0][2], lambda d: theme_parts.header(d, fa=True))
    emit(FA_DOCS[1][0], FA_DOCS[1][1], FA_DOCS[1][2], lambda d: theme_parts.footer(d, fa=True))

    # Popup page settings carry the popup configuration
    for path, payload in list(files):
        if payload["type"] == "popup":
            payload["page_settings"] = theme_parts.POPUP_SETTINGS

    for rel, title, generator in BLOCKS + FA_BLOCKS:
        emit(rel, "section", title, generator)

    # ---- Kit -------------------------------------------------------------
    kit_payload = kit_mod.kit_document()
    files.append(("kit/aurora-site-settings.json", kit_payload))
    index.append({"path": "kit/aurora-site-settings.json", "type": "kit",
                  "title": tk.KIT_TITLE, "containers": 0, "widgets": 0,
                  "widget_types": []})

    # ---- report ----------------------------------------------------------
    print("Aurora AI kit build")
    print("  documents : %d" % len(files))
    print("  containers: %d" % counter.get("container", 0))
    print("  widgets   : %d" % sum(v for k, v in counter.items() if k != "container"))
    print("  widget mix: %s" % ", ".join(
        "%s x%d" % (k, v) for k, v in sorted(counter.items(), key=lambda kv: -kv[1])[:14]
        if k != "container"))
    if total_issues.warnings:
        print("  warnings  : %d" % len(total_issues.warnings))
        for w in total_issues.warnings[:20]:
            print("    - %s" % w)
    if total_issues.errors:
        print("  ERRORS    : %d" % len(total_issues.errors))
        for e in total_issues.errors[:40]:
            print("    ! %s" % e)
        return 1
    print("  validation: OK")

    if check_only:
        return 0

    # ---- write templates -------------------------------------------------
    for rel, payload in files:
        path = os.path.join(out_templates, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
            fh.write("\n")

    # ---- write site-settings + manifest ---------------------------------
    with open(os.path.join(out_dist, "site-settings.json"), "w", encoding="utf-8") as fh:
        json.dump(kit_mod.site_settings_file(), fh, ensure_ascii=False, indent=1)

    template_index: Dict[str, List[str]] = {}
    for item in index:
        if item["type"] == "kit":
            continue
        template_index.setdefault(item["type"], []).append(item["title"])
    with open(os.path.join(out_dist, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(kit_mod.manifest(template_index), fh, ensure_ascii=False, indent=1)

    # ---- ZIP 1: flat template archive -----------------------------------
    zip_templates = os.path.join(out_dist, "aurora-ai-templates.zip")
    with zipfile.ZipFile(zip_templates, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, payload in files:
            zf.writestr(rel.replace("/", "-"), json.dumps(payload, ensure_ascii=False, indent=1))

    # ---- ZIP 2: kit archive ---------------------------------------------
    zip_kit = os.path.join(out_dist, "aurora-ai-kit.zip")
    with zipfile.ZipFile(zip_kit, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json",
                    json.dumps(kit_mod.manifest(template_index), ensure_ascii=False, indent=1))
        zf.writestr("site-settings.json",
                    json.dumps(kit_mod.site_settings_file(), ensure_ascii=False, indent=1))
        for rel, payload in files:
            zf.writestr("templates-source/" + rel,
                        json.dumps(payload, ensure_ascii=False, indent=1))
        zf.writestr("README.txt", KIT_README)

    # ---- generated index -------------------------------------------------
    with open(os.path.join(out_templates, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write(render_index(index))

    print("  wrote     : templates/ (%d json) + dist/ (2 zips, 2 meta files)"
          % len(files))
    print("  zip sizes : templates %.1f KB, kit %.1f KB"
          % (os.path.getsize(zip_templates) / 1024.0, os.path.getsize(zip_kit) / 1024.0))
    return 0


KIT_README = """AURORA AI - ELEMENTOR TEMPLATE KIT
==================================

This archive is the Elementor "Export Kit" style package:

  manifest.json          kit manifest (what is inside, Elementor version)
  site-settings.json     global colors, global fonts, layout, button + form styles
  templates-source/*     every template as a standalone Elementor document

What this kit archive does
--------------------------
Importing it applies the Aurora design system to your site in one step:
global colors, global fonts, content width, breakpoints, heading/body/link
styles, button styles and form-field styles.

Recommended import order
------------------------
1. Templates > Saved Templates > Import Templates  ->  aurora-ai-templates.zip
   (this adds all 40 templates to your library)
2. Elementor > Tools > Import / Export Kit  ->  Import Kit  ->  this file
   (this applies the design system) - or apply the globals by hand following
   docs/02-design-system.md if your Elementor version is older than 3.x
3. Templates > Theme Builder: create a Header, a Footer, a Single Post, an
   Archive, a Search Results and a Popup document and insert the matching
   template from My Templates, then set the display conditions.
4. Create your pages (Home, About, Services, Case Studies, Pricing, Journal,
   Contact, 404) and drop the matching page template into each one.

Every file in templates-source/ is a standalone Elementor document - import
only what you need. Full instructions: docs/01-installation.md
"""


def render_index(index: List[Dict[str, Any]]) -> str:
    order = ["kit", "header", "footer", "page", "single", "archive", "search-results",
             "popup", "section"]
    by_type: Dict[str, List[Dict[str, Any]]] = {}
    for item in index:
        by_type.setdefault(item["type"], []).append(item)

    lines = [
        "# Aurora AI - Template Index",
        "",
        "> Generated by `python3 tools/build.py`. Do not edit by hand.",
        "",
        "| Type | Template | File | Containers | Widgets |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for t in order:
        for item in sorted(by_type.get(t, []), key=lambda i: i["path"]):
            lines.append("| `%s` | %s | `%s` | %d | %d |" % (
                item["type"], item["title"], item["path"], item["containers"], item["widgets"]))
    total_c = sum(i["containers"] for i in index)
    total_w = sum(i["widgets"] for i in index)
    lines += [
        "",
        "**Totals:** %d documents, %d containers, %d widgets." % (
            len(index), total_c, total_w),
        "",
        "Every template is built exclusively from Elementor Flexbox Containers and",
        "native Elementor / Elementor Pro widgets - there is no custom HTML widget and",
        "no custom CSS anywhere in the kit.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the Aurora AI Elementor kit")
    ap.add_argument("--check", action="store_true", help="validate without writing files")
    args = ap.parse_args()
    sys.exit(build(check_only=args.check))
