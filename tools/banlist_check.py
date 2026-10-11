#!/usr/bin/env python3
"""
BANLIST.md enforcement (constitution rule E: taste is numeric, not adjectival).

Every rule below is deterministic: it reads the generated Elementor JSON and either
counts a pattern or looks for a literal. No rule is a vibe.

    python3 tools/banlist_check.py            # human report + violations
    python3 tools/banlist_check.py --json     # machine output for CI
    python3 tools/banlist_check.py --report-only   # always exit 0 (diagnosis mode)

Rule levels
    FAIL  ships as slop; must be fixed before the ban can be considered enforced
    WARN  a tell; acceptable with a documented reason in BANLIST.md

Phase note: P1 is diagnosis only. The kit currently trips several FAIL rules on
purpose — they are the P2 worklist, listed in docs/p1/delta-table.md. CI therefore
runs this script in --report-only until P2 closes the gaps, at which point the flag
is dropped and the exit code becomes the gate.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Set, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")

# --------------------------------------------------------------------------
# literal bans
# --------------------------------------------------------------------------

EM_DASH = "\u2014"
MIDDLE_DOT = "\u00b7"

GENERIC_NAMES = ("john doe", "jane doe", "sarah chan", "jack su", "acme", "nexus",
                 "smartflow", "cloudly", "foo corp", "example inc")

FILLER_VERBS = ("elevate", "seamless", "unleash", "next-gen", "next gen",
                "revolutionize", "revolutionise", "empower", "leverage",
                "supercharge", "cutting-edge", "world-class", "best-in-class",
                "game-chang", "transform your", "take it to the next level",
                "in today's fast-paced")

VERSION_EYEBROW = re.compile(
    r"\b(v\d+\.\d+|\d+\.\d+\b|beta|alpha|early access|invite[- ]only|preview|rc\.\d+)",
    re.I)

# fabricated-metric shapes: 380M, 99.98 %, 12x, 4.9/5, $1.2B
FAKE_METRIC = re.compile(
    r"(\b\d{1,3}(?:[.,]\d+)?\s?(?:%|x|×|k|M|B)\b|\b\d\.\d\s?/\s?5\b|trusted by\b)")
# prices are placeholder product data, not a fabricated claim: reported separately
PRICE = re.compile(r"[$€£]\s?\d[\d.,]*")

# A step label is a bare ordinal ("03", "01") or an explicit "Step 3" - not any
# string that happens to start with a digit ("4 hrs", "14 countries").
NUMBERED_STEP = re.compile(r"^\s*(?:0[1-9]|1[0-2])\s*$|^\s*(?:step|stage|phase|pass)\s*\d+\b",
                           re.I)

# Strings under these keys are pick-lists / instructions, not marketing claims.
NON_CLAIM_KEYS = {"field_options", "options", "placeholder", "acceptance_text",
                  "success_message", "error_message", "redirect_to", "custom_messages"}

# hue window for the purple/indigo/lila ban (hue 250-300, saturation > 0.30)
def hex_to_hsl(value: str):
    v = value.strip()
    if not re.match(r"^#[0-9a-fA-F]{6}$", v):
        return None
    r, g, b = (int(v[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return (0.0, 0.0, l)
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return (h * 60, s, l)


# --------------------------------------------------------------------------
# collection helpers
# --------------------------------------------------------------------------

def walk(node: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    yield node
    for child in node.get("elements") or []:
        yield from walk(child)


def strings_in(value, key="") -> Iterable[Tuple[str, str]]:
    """Every (key, string) pair inside a settings value, including repeats."""
    if isinstance(value, str):
        yield key, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from strings_in(v, k)
    elif isinstance(value, list):
        for item in value:
            yield from strings_in(item, key)


def eyebrow_typography_ids() -> Set[str]:
    """Global typography ids that act as an eyebrow / overline label.

    Two evidence-based signatures: an uppercase transform (the Latin eyebrow) or a
    style whose title names it an eyebrow (the FA label, which cannot use uppercase
    because Persian has no letter case).
    """
    path = os.path.join(TEMPLATES, "kit", "aurora-site-settings.json")
    if not os.path.exists(path):
        return set()
    kit = json.load(open(path, encoding="utf-8"))
    ps = kit.get("page_settings") or {}
    out = set()
    for row in ps.get("system_typography", []) + ps.get("custom_typography", []):
        title = str(row.get("title", "")).lower()
        if str(row.get("typography_text_transform", "")).lower() == "uppercase" \
                or "eyebrow" in title or "overline" in title:
            out.add(row["_id"])
    return out


def load_docs():
    for root, _dirs, names in os.walk(TEMPLATES):
        for fn in sorted(names):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(root, fn)
            doc = json.load(open(path, encoding="utf-8"))
            if doc.get("type") == "kit":
                continue
            yield os.path.relpath(path, ROOT), doc


def sections(doc) -> List[Dict[str, Any]]:
    return [n for n in doc["content"] if n.get("elType") == "container"]


def is_icon_tile_grid(container: Dict[str, Any]) -> bool:
    """A row whose children are all: one icon widget + a heading (+ optional text),
    each with an equal flex-basis, and a card-ish surface (background or border)."""
    kids = container.get("elements") or []
    if len(kids) < 3 or not all(k.get("elType") == "container" for k in kids):
        return False
    bases, shaped = set(), 0
    for kid in kids:
        widgets = [w for w in walk(kid) if w.get("elType") == "widget"]
        kinds = [w.get("widgetType") for w in widgets]
        if kinds.count("icon") == 1 and ("heading" in kinds):
            has_surface = bool(
                (kid.get("settings") or {}).get("background_background")
                or (kid.get("settings") or {}).get("border_border"))
            if has_surface:
                shaped += 1
        basis = (kid.get("settings") or {}).get("_flex_basis")
        if isinstance(basis, dict):
            bases.add((basis.get("unit"), basis.get("size")))
    return shaped == len(kids) and len(bases) == 1


# --------------------------------------------------------------------------
# rules
# --------------------------------------------------------------------------

def run_rules() -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    v: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
    stats = collections.Counter()
    # values that would otherwise be absent from a plain-dict dump when the count is 0
    stats.update({"documents": 0, "sections": 0, "elements": 0, "dividers": 0,
                  "pure_white_surfaces": 0, "animated_widgets": 0, "eyebrows": 0,
                  "sections_with_eyebrow": 0, "centred_sections": 0})

    upper_ids = eyebrow_typography_ids()

    for rel, doc in load_docs():
        stats["documents"] += 1
        for top in doc["content"]:
            for node in walk(top):
                settings = node.get("settings") or {}
                el_type = node.get("elType")
                widget = node.get("widgetType", "")

                for key, text in strings_in(settings):
                    low = text.lower()

                    # B01 em-dash anywhere (taste §9.G)
                    if EM_DASH in text:
                        v["B01-em-dash"].append({"file": rel, "key": key, "text": text[:70]})

                    # B02 middle-dot over-rationed (taste §9.F)
                    if text.count(MIDDLE_DOT) > 1:
                        v["B02-middle-dot"].append({"file": rel, "key": key, "text": text[:70]})

                    # B03 fabricated metrics in copy
                    for m in (FAKE_METRIC.finditer(text)
                              if key not in NON_CLAIM_KEYS and "–" not in text and "\n" not in text
                              else ()):
                        v["B03-fake-metric"].append(
                            {"file": rel, "key": key, "match": m.group(0), "text": text[:60]})

                    # B03b price placeholders (WARN - must be replaced before launch)
                    if key not in NON_CLAIM_KEYS:
                        for m in PRICE.finditer(text):
                            v["B03b-price-placeholder"].append(
                                {"file": rel, "key": key, "match": m.group(0)})

                    # B04 generic names / startup-slop brands (taste §9.D)
                    for name in GENERIC_NAMES:
                        if name in low:
                            v["B04-generic-name"].append(
                                {"file": rel, "key": key, "match": name})

                    # B05 filler verbs (taste §9.D)
                    for verb in FILLER_VERBS:
                        if verb in low:
                            v["B05-filler-verb"].append(
                                {"file": rel, "key": key, "match": verb, "text": text[:60]})

                    # B06 version / status eyebrow in the hero band
                    if key in ("title", "editor", "text") and VERSION_EYEBROW.search(text):
                        v["B06-version-eyebrow"].append(
                            {"file": rel, "key": key, "match": VERSION_EYEBROW.search(text).group(0),
                             "text": text[:60]})

                    # B07 numbered step labels (taste §9.F)
                    if widget in ("heading", "text-editor") and NUMBERED_STEP.search(text):
                        v["B07-numbered-step"].append(
                            {"file": rel, "key": key, "text": text[:60]})

                    # B11 purple/indigo/lila (taste LILA rule)
                    if isinstance(text, str) and text.startswith("#"):
                        hsl = hex_to_hsl(text)
                        if hsl and 250 <= hsl[0] <= 300 and hsl[1] > 0.30:
                            v["B11-purple"].append(
                                {"file": rel, "key": key, "colour": text,
                                 "hsl": "h=%.0f s=%.2f" % (hsl[0], hsl[1])})

                    # B12 pure black / pure white as a text colour
                    if key.endswith("_color") and text.upper() in ("#000000", "#FFFFFF"):
                        v["B12-pure-black-white"].append(
                            {"file": rel, "key": key, "colour": text})

                # B12b backgrounds of pure white
                if isinstance(settings.get("background_color"), str) and \
                        settings["background_color"].upper() == "#FFFFFF":
                    stats["pure_white_surfaces"] += 1

                stats["elements"] += 1
                if widget == "divider":
                    stats["dividers"] += 1
                    w = settings.get("width")
                    if isinstance(w, dict) and isinstance(w.get("size"), (int, float)) \
                            and w.get("unit") == "%" and w["size"] <= 30:
                        v["B13-decorative-rule"].append(
                            {"file": rel, "width": "%s%s" % (w["size"], w.get("unit"))})

                if el_type == "widget" and settings.get("_animation"):
                    stats["animated_widgets"] += 1

        # per-section structure rules
        for sec in sections(doc):
            stats["sections"] += 1
            # an eyebrow anywhere in the section (its style is a global, so resolve refs)
            for w in walk(sec):
                if w.get("elType") != "widget" or w.get("widgetType") != "heading":
                    continue
                ref = str((w.get("settings") or {}).get("typography_typography", ""))
                if ref.startswith("globals/typography?id=") and \
                        ref.split("=", 1)[1] in upper_ids:
                    stats["sections_with_eyebrow"] += 1
                    break
            if is_icon_tile_grid(sec):
                v["B06-icon-tile-grid"].append({"file": rel})
            kids = sec.get("elements") or []
            centred = (sec.get("settings") or {}).get("flex_align_items") == "center"
            if not centred:
                for w in walk(sec):
                    if w.get("elType") == "widget" and (w.get("settings") or {}).get("align") == "center":
                        centred = True
                        break
            if centred:
                stats["centred_sections"] += 1
            # eyebrow heuristic: an eyebrow is a row whose first child is a short
            # heading in uppercase with tight letter-spacing
            for kid in kids:
                if kid.get("elType") != "container":
                    continue
                inner = [w for w in walk(kid) if w.get("elType") == "widget"]
                for w in inner:
                    s = w.get("settings") or {}
                    ref = str(s.get("typography_typography", ""))
                    is_upper = (str(s.get("typography_text_transform", "")).lower() == "uppercase"
                                or (ref.startswith("globals/typography?id=")
                                    and ref.split("=", 1)[1] in upper_ids))
                    if w.get("widgetType") == "heading" and is_upper:
                        v["B08-eyebrow"].append(
                            {"file": rel, "text": str(s.get("title", ""))[:40]})
                        stats["eyebrows"] += 1
                        section_has_eyebrow = True

    stats["animated_ratio"] = (stats["animated_widgets"] / stats["elements"]
                               if stats["elements"] else 0)
    stats["eyebrow_ratio"] = (stats["sections_with_eyebrow"] / stats["sections"]
                              if stats["sections"] else 0)
    stats["centred_ratio"] = (stats["centred_sections"] / stats["sections"]
                              if stats["sections"] else 0)

    # ratio-based rules
    if stats["eyebrow_ratio"] > 0.8:
        v["B08-eyebrow-everywhere"].append(
            {"rule": "eyebrow on >80%% of sections", "ratio": round(stats["eyebrow_ratio"], 2)})
    if stats["animated_ratio"] > 0.60:
        v["B09-animate-everything"].append(
            {"rule": "animated elements >60%% of all elements",
             "ratio": round(stats["animated_ratio"], 2)})
    return v, dict(stats)


FAIL_RULES = {"B01-em-dash", "B03-fake-metric", "B04-generic-name", "B05-filler-verb",
              "B06-icon-tile-grid", "B11-purple", "B12-pure-black-white"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report-only", action="store_true",
                    help="always exit 0 (P1 diagnosis mode)")
    args = ap.parse_args()

    violations, stats = run_rules()
    fails = {k: v for k, v in violations.items() if k in FAIL_RULES}
    warns = {k: v for k, v in violations.items() if k not in FAIL_RULES}

    if args.json:
        print(json.dumps({"stats": stats,
                          "fail": {k: len(v) for k, v in fails.items()},
                          "warn": {k: len(v) for k, v in warns.items()},
                          "violations": violations}, indent=1))
    else:
        print("BANLIST enforcement (deterministic detectors)")
        print("  documents       : %d" % stats.get("documents", 0))
        print("  sections        : %d" % stats.get("sections", 0))
        print("  elements        : %d" % stats.get("elements", 0))
        print("  eyebrow ratio   : %.0f%% of sections" % (100 * stats.get("eyebrow_ratio", 0)))
        print("  animated ratio  : %.0f%% of elements" % (100 * stats.get("animated_ratio", 0)))
        print("  centred sections: %.0f%%" % (100 * stats.get("centred_ratio", 0)))
        print()
        for label, group in (("FAIL", fails), ("WARN", warns)):
            if not group:
                continue
            print("  %s rules:" % label)
            for rule, rows in sorted(group.items()):
                print("    %-26s %d" % (rule, len(rows)))
                for row in rows[:3]:
                    detail = row.get("text") or row.get("match") or row.get("width") or row.get("rule") or ""
                    print("        %-42s %s" % (row.get("file", ""), str(detail)[:52]))
                if len(rows) > 3:
                    print("        ... %d more" % (len(rows) - 3))
    if args.report_only:
        return 0
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
