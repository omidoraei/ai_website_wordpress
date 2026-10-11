#!/usr/bin/env python3
"""
Bidi / Unicode safety scan (constitution rule J).

Persian and Arabic strings must never be approved from a rendered diff — a rendered
diff reorders characters and hides damage. This scan reads the JSON instead and
classifies every bidi codepoint by where it sits.

    python3 tools/bidi_check.py            # human report
    python3 tools/bidi_check.py --json     # machine output for CI
    python3 tools/bidi_check.py --strict   # WARN also fails (use once copy is annotated)

Classification
    FAIL  codepoint inside an element id, a settings KEY (control name), a CSS class
          or a URL — this corrupts the JSON contract, not the prose
    WARN  codepoint inside copy (an editor's text) without an annotation
    INFO  codepoint inside copy that is listed in the annotation file

Annotations live in skills/elementor-native-kit/bidi-annotations.json:
    { "allow": [ { "path": "templates/pages/aurora-home-fa.json",
                   "codepoint": "U+200C", "reason": "ZWNJ between Persian words" } ] }

Exit codes: 0 = no FAIL (and no WARN when --strict), 1 otherwise.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNOTATIONS = os.path.join(ROOT, "skills", "elementor-native-kit", "bidi-annotations.json")

# Every codepoint that can reorder, override or isolate a run of text.
BIDI = {
    "\u202a": "LRE", "\u202b": "RLE", "\u202c": "PDF", "\u202d": "LRO", "\u202e": "RLO",
    "\u2066": "LRI", "\u2067": "RLI", "\u2068": "FSI", "\u2069": "PDI",
    "\u200e": "LRM", "\u200f": "RLM", "\u061c": "ALM",
    # zero-width joiners are not bidi controls but are the classic copy-paste hazard
    "\u200c": "ZWNJ", "\u200d": "ZWJ", "\ufeff": "BOM",
}

# keys whose VALUE is a URL / identifier / class list -> a bidi char there is a FAIL
IDENT_KEYS = ("url", "link", "_element_id", "css_classes", "id", "widgetType", "elType",
              "template", "element_id")

COPY_HINT = ("title", "editor", "text", "content", "description", "label", "alt",
             "caption", "placeholder", "tab_title", "tab_content", "acceptance_text",
             "testimonial", "message", "success_message", "error_message")


def classify(point: str) -> str:
    return BIDI[point]


def is_ident_key(key: str) -> bool:
    k = key.lower()
    return any(h in k for h in IDENT_KEYS)


def scan_string(value: str):
    for ch in value:
        if ch in BIDI:
            yield ch


def walk(node, path, findings, counts, annotate):
    if not isinstance(node, dict):
        return
    el_id = node.get("id")
    if isinstance(el_id, str) and any(c in BIDI for c in el_id):
        for c in scan_string(el_id):
            findings.append(("FAIL", path, "element id", "U+%04X %s" % (ord(c), classify(c))))
            counts["FAIL"] += 1

    settings = node.get("settings") or {}
    if isinstance(settings, dict):
        for key, val in settings.items():
            if any(c in BIDI for c in str(key)):
                for c in scan_string(str(key)):
                    findings.append(("FAIL", path, "control name %r" % key,
                                     "U+%04X %s" % (ord(c), classify(c))))
                    counts["FAIL"] += 1
            for sub, sval in _flatten(val):
                if not isinstance(sval, str):
                    continue
                hits = list(scan_string(sval))
                if not hits:
                    continue
                where = "url" if (is_ident_key(key) or is_ident_key(sub)) else "copy"
                for c in hits:
                    label = "U+%04X %s" % (ord(c), classify(c))
                    if where == "url":
                        findings.append(("FAIL", path, "url/identifier in %r" % key, label))
                        counts["FAIL"] += 1
                    elif annotate(path, label):
                        findings.append(("INFO", path, "annotated %r" % key, label))
                        counts["INFO"] += 1
                    elif key.lower().endswith(tuple(COPY_HINT)) or key in COPY_HINT:
                        findings.append(("WARN", path, "copy %r" % key, label))
                        counts["WARN"] += 1
                    else:
                        findings.append(("WARN", path, "value of %r" % key, label))
                        counts["WARN"] += 1

    for child in node.get("elements") or []:
        walk(child, path, findings, counts, annotate)


def _flatten(value, key=""):
    if isinstance(value, str):
        yield key, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _flatten(v, k)
    elif isinstance(value, list):
        for item in value:
            yield key, item if isinstance(item, str) else ""
            if isinstance(item, dict):
                yield from _flatten(item, key)


def load_annotations():
    if not os.path.exists(ANNOTATIONS):
        return set()
    try:
        data = json.load(open(ANNOTATIONS, encoding="utf-8"))
    except Exception:
        return set()
    return {(row.get("path"), row.get("codepoint"))
            for row in data.get("allow", []) if isinstance(row, dict)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    allowed = load_annotations()
    annotate = lambda path, label: (path, label.split()[0]) in allowed  # noqa: E731

    findings = []
    counts = collections.Counter()
    scanned = 0
    for folder in ("templates", "dist"):
        base = os.path.join(ROOT, folder)
        if not os.path.isdir(base):
            continue
        for root, _dirs, names in os.walk(base):
            for fn in sorted(names):
                if not fn.endswith(".json"):
                    continue
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, ROOT)
                try:
                    doc = json.load(open(full, encoding="utf-8"))
                except Exception as exc:
                    findings.append(("FAIL", rel, "invalid JSON", str(exc)))
                    counts["FAIL"] += 1
                    continue
                scanned += 1
                if doc.get("type") == "kit":
                    # kit settings: global color/font titles may legitimately be Persian
                    for row in (doc.get("page_settings") or {}).get("custom_colors", []) + \
                            (doc.get("page_settings") or {}).get("custom_typography", []):
                        for c in scan_string(json.dumps(row, ensure_ascii=False)):
                            findings.append(("WARN", rel, "kit label", "U+%04X" % ord(c)))
                            counts["WARN"] += 1
                    continue
                for top in doc.get("content") or []:
                    walk(top, rel, findings, counts, annotate)

    by_class = collections.Counter(f[0] for f in findings)
    if args.json:
        print(json.dumps({
            "scanned": scanned,
            "counts": dict(by_class),
            "findings": [{"class": c, "file": f, "where": w, "codepoint": p}
                         for c, f, w, p in findings],
            "annotations_loaded": len(allowed),
        }, indent=1, ensure_ascii=False))
    else:
        print("bidi / Unicode safety scan")
        print("  files scanned : %d" % scanned)
        print("  FAIL          : %d" % counts["FAIL"])
        print("  WARN          : %d" % counts["WARN"])
        print("  INFO          : %d (annotated)" % counts["INFO"])
        if findings:
            print()
            for c, f, w, p in findings[:30]:
                print("  %-5s %-46s %-28s %s" % (c, f, w[:28], p))
            if len(findings) > 30:
                print("  ... %d more (use --json)" % (len(findings) - 30))
        else:
            print("  clean: no bidi control characters in id, control name, URL or copy")
    if counts["FAIL"]:
        return 1
    if args.strict and counts["WARN"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
