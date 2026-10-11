#!/usr/bin/env python3
"""Alt-text QUALITY check for image widgets (P1.7 item 2).

Presence is not quality. P1.6 proved `settings.image.alt` is non-empty on every image widget
(24/24, 13 distinct strings); this script measures what those strings are worth. It never edits
a template and never rewrites an alt: it measures, and the policy it measures against lives in
`docs/a11y-alt-policy.md` (rule ids R1..R4 checked by this script).

Storage path, measured not assumed: Elementor keeps the per-instance alt at
`settings.image.alt` (the earlier audit read `settings.alt`, which is always empty - see
docs/DECLARATIONS... in-repo: docs/CLAIMS.md C-017/C-027).

    python3 tools/alt_quality_check.py            # human report, exit 1 only on floor breach
    python3 tools/alt_quality_check.py --json     # machine-readable
    python3 tools/alt_quality_check.py --strict   # findings that are quality defects exit 1

Exit contract: non-empty assertion first. Fewer than FLOOR_IMAGE_WIDGETS image widgets scanned is
a scanner failure (exit 1), because "no findings" in an empty scan is not a pass.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
POLICY = ROOT / "docs" / "a11y-alt-policy.md"
ALT_PATH_USED = "settings.image.alt"
FLOOR_IMAGE_WIDGETS = 20          # measured 24; a drop below 20 means the walk broke
# A Latin-script alt that is nothing but Capitalised Words reads as a proper noun (a client, a
# place, a product) rather than a description. Persian alts cannot use case, so the check says so
# instead of guessing: R4 review covers those.
PROPER_NOUN_ONLY = re.compile(r"^([A-Z][a-zA-Z0-9]*( [A-Z][a-zA-Z0-9]*){0,3})$")
GENERIC = {"image", "photo", "picture", "banner", "screenshot", "graphic", "img", "thumbnail",
           "\u062a\u0635\u0648\u06cc\u0631", "\u0628\u0646\u0631", "\u0639\u06a9\u0633"}
DECORATIVE_FILENAME = re.compile(r"(bg|background|pattern|texture|shape|blob|decor|divider|noise|gradient|wave)",
                                 re.I)
BRAND = {"aurora ai", "aurora", "\u0622\u0631\u0648\u0631\u0627"}
POLICY_RULES = ("R1", "R2", "R3", "R4")


def elements(node, out):
    """Every node with an elType: widgets AND containers (P1.6 lesson)."""
    if isinstance(node, dict):
        if node.get("elType"):
            out.append(node)
        for value in node.values():
            elements(value, out)
    elif isinstance(node, list):
        for value in node:
            elements(value, out)


def bucket(text: str) -> str:
    n = len(text.strip())
    if n == 0:
        return "0 (empty)"
    if n <= 15:
        return "1-15"
    if n <= 40:
        return "16-40"
    if n <= 80:
        return "41-80"
    return "81+"


def measure() -> dict:
    """The report dict, importable: `tools/verify.py` and the invariant runner read THIS."""
    docs = sorted(TEMPLATES.rglob("*.json"))
    widgets = []          # (document, widget index, url, alt)
    for path in docs:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("type") == "kit":
            continue
        found = []
        elements(data, found)
        index = 0
        for node in found:
            if node.get("widgetType") != "image":
                continue
            index += 1
            settings = node.get("settings") or {}
            image = settings.get("image") if isinstance(settings.get("image"), dict) else {}
            alt = image.get("alt")
            widgets.append({
                "document": path.relative_to(ROOT).as_posix(),
                "locale": "fa" if path.name.startswith("fa-") or path.name.endswith("-fa.json") else "en",
                "slot": index,
                "file": str(image.get("url", "")).rsplit("/", 1)[-1],
                "alt": alt if isinstance(alt, str) else "",
                "alt_type": "missing-key" if alt is None else ("non-string" if not isinstance(alt, str) else "string"),
            })

    if len(widgets) < FLOOR_IMAGE_WIDGETS:
        raise SystemExit("alt_quality_check: FAIL - only %d image widget(s) scanned (floor %d)"
                         % (len(widgets), FLOOR_IMAGE_WIDGETS))
    if not POLICY.exists():
        raise SystemExit("alt_quality_check: FAIL - policy file missing: %s" % POLICY.relative_to(ROOT))
    policy_text = POLICY.read_text(encoding="utf-8")
    missing_rules = [r for r in POLICY_RULES if ("%s " % r) not in policy_text]

    nonempty = [w for w in widgets if w["alt"].strip()]
    empty = [w for w in widgets if not w["alt"].strip()]
    distinct = sorted({w["alt"] for w in nonempty})
    by_locale = {}
    for w in widgets:
        by_locale.setdefault(w["locale"], {"image_widgets": 0, "nonempty": 0})
        by_locale[w["locale"]]["image_widgets"] += 1
        if w["alt"].strip():
            by_locale[w["locale"]]["nonempty"] += 1
    lengths = {}
    for w in widgets:
        lengths[bucket(w["alt"])] = lengths.get(bucket(w["alt"]), 0) + 1
    lengths = dict(sorted(lengths.items(), key=lambda kv: kv[0]))

    decorative = []
    generic = []
    for w in widgets:
        alt = w["alt"].strip()
        if not alt:
            continue
        if alt.lower() in BRAND:
            decorative.append({"document": w["document"], "file": w["file"], "alt": alt,
                               "reason": "alt equals the brand name (brand mark; R3)"})
        elif DECORATIVE_FILENAME.search(w["file"]):
            decorative.append({"document": w["document"], "file": w["file"], "alt": alt,
                               "reason": "filename marker + non-empty alt (R2)"})
        if alt.lower() in GENERIC:
            generic.append({"document": w["document"], "file": w["file"], "alt": alt,
                            "reason": "generic word, no content described (R1)"})

    proper_noun = []
    for w in nonempty:
        alt = w["alt"].strip()
        if PROPER_NOUN_ONLY.match(alt) and not any(ch in alt for ch in "\u0600\u06ff"):
            proper_noun.append({"document": w["document"], "file": w["file"], "alt": alt,
                                "reason": "capitalised phrase only - names the subject, does not describe it (R1)"})

    locale_mismatch = []
    for w in nonempty:
        has_fa = bool(re.search(r"[\u0600-\u06FF]", w["alt"]))
        if w["locale"] == "en" and has_fa:
            locale_mismatch.append({"document": w["document"], "file": w["file"], "alt": w["alt"],
                                    "reason": "Persian-script alt in a document whose name carries no fa- marker"})
        elif w["locale"] == "fa" and not has_fa:
            locale_mismatch.append({"document": w["document"], "file": w["file"], "alt": w["alt"],
                                    "reason": "Latin-only alt in an fa-named document"})

    by_alt = {}
    for w in nonempty:
        by_alt.setdefault(w["alt"], set()).add(w["file"])
    repeated = [{"alt": alt, "files": sorted(files), "distinct_files": len(files)}
                for alt, files in sorted(by_alt.items()) if len(files) > 1]

    alt_lens = [len(w["alt"].strip()) for w in nonempty]
    report = {
        "image_widget_count": len(widgets),
        "alt_documents_scanned": len(docs),
        "alt_field_path_used": ALT_PATH_USED,
        "alt_nonempty_count": len(nonempty),
        "alt_empty_count": len(empty),
        "alt_distinct_count": len(distinct),
        "alt_by_document_locale": by_locale,
        "alt_length_distribution": lengths,
        "alt_length_min_max_mean": [min(alt_lens), max(alt_lens), round(sum(alt_lens) / len(alt_lens), 1)],
        "suspected_decorative_with_nonempty_alt": decorative,
        "suspected_content_with_generic_alt": generic,
        "suspected_proper_noun_only_alt": proper_noun,
        "alt_locale_mismatch": locale_mismatch,
        "repeated_alt_across_different_image_files": repeated,
        "alt_policy_documented": (not missing_rules),
        "alt_policy_missing_rules": missing_rules,
        "distinct_alt_strings": distinct,
        "alt_type_anomalies": [w for w in widgets if w["alt_type"] != "string"],
    }

    report["suspected_proper_noun_only_alt_distinct"] = len({row["alt"] for row in proper_noun})
    report["alt_locale_mismatch_distinct"] = len({row["alt"] for row in locale_mismatch})
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="generic/decorative findings are fatal")
    args = ap.parse_args()

    report = measure()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("alt_quality_check: %d image widget(s) scanned in %d document(s); alt path = %s"
              % (report["image_widget_count"], report["alt_documents_scanned"], ALT_PATH_USED))
        print("  non-empty=%d  empty=%d  distinct=%d  length min/max/mean=%s"
              % (report["alt_nonempty_count"], report["alt_empty_count"], report["alt_distinct_count"],
                 "/".join(str(v) for v in report["alt_length_min_max_mean"])))
        print("  by locale: %s" % json.dumps(report["alt_by_document_locale"], ensure_ascii=False))
        print("  length distribution: %s" % json.dumps(report["alt_length_distribution"]))
        print("  policy %s (%s): %s" % ("documented" if report["alt_policy_documented"] else "INCOMPLETE",
                                        POLICY.relative_to(ROOT), ",".join(POLICY_RULES)))
        for key, label in (("suspected_decorative_with_nonempty_alt", "decorative with non-empty alt (R2/R3)"),
                           ("suspected_content_with_generic_alt", "generic alt (R1)"),
                           ("suspected_proper_noun_only_alt", "proper-noun-only alt, no description (R1)"),
                           ("alt_locale_mismatch", "alt script vs document locale (R1/R4)")):
            rows = report[key]
            print("  suspected %s: %d instance(s), %d distinct"
                  % (label, len(rows), len({row["alt"] for row in rows})))
            for row in rows[:4]:
                print("    ! %s [%s] alt=%r" % (row["document"], row["file"], row["alt"]))
            if len(rows) > 4:
                print("    ... %d more" % (len(rows) - 4))
        repeated = report["repeated_alt_across_different_image_files"]
        print("  alt reused across different image files: %d" % len(repeated))
        for row in repeated:
            print("    ! %r on %d distinct file(s): %s" % (row["alt"], row["distinct_files"],
                                                           ", ".join(row["files"])))

    quality = sum(len(report[key]) for key in
                  ("suspected_decorative_with_nonempty_alt", "suspected_content_with_generic_alt",
                   "suspected_proper_noun_only_alt", "alt_locale_mismatch"))
    if args.strict and quality:
        print("alt_quality_check: --strict - %d quality finding(s)" % quality)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
