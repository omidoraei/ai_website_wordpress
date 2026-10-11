#!/usr/bin/env python3
"""Language-mixing check: English-named documents that embed Persian/Arabic-script copy.

Why this exists: `tools/bidi_check.py` cannot catch this class. Persian is valid bidi input and
needs no control characters, so a page that mixes Persian copy into an English document passes
the bidi scan silently (P1.5, three documents, 21 strings each). P8 owns the fix; this checker
owns the measurement.

Counting units (the P1.5-vs-P1.6 drift, reconciled in P1.7 / docs/p1.7/lang-mix-audit.md):
  * `strings` = leaf JSON string values that contain >= 1 Arabic-script character.
    One widget setting counts once, however long it is. This is the P1.6 unit ("9 strings").
  * `runs`    = maximal runs of Arabic-script characters. A setting with Latin text on both
    sides of a Persian phrase contributes 2. This is the unit P1.5 was reading ("21").
  * `chars`   = every character in the Arabic-script ranges. This is the P1.6 unit ("106").
  * `paths`   = distinct jsonpaths (widget settings) holding at least one of those strings.
  None of the four is "wrong"; they answer different questions, so every report names its unit.

Exit contract:
  * exits 1 when the non-empty assertion floor fails (fewer than FLOOR documents scanned)
  * `--strict` makes any finding fatal (P8 flips the CI step to `--strict`)
  * default exits 0 and prints the per-document table (report-only, like banlist until P2)
"""

import argparse
import json
import re
import sys
from pathlib import Path

FLOOR = 30
ARABIC = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")
ARABIC_STRING = re.compile(r'"([^"]*[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF][^"]*)"')


def is_fa_name(name: str) -> bool:
    return name.startswith("fa-") or name.endswith("-fa.json")


# Letters that exist in Persian but not in Arabic (plus ZWNJ, a Persian typography marker):
# peh, tcheh, jeh, gaf, keheh, farsi yeh. Their presence is evidence for Persian.
PERSIAN_ONLY = "\u067e\u0686\u0698\u06af\u06a9\u06cc\u200c"
# Letters that exist in Arabic but not in Persian: alef maksura / farsi-less yeh / kaf / teh marbuta.
ARABIC_ONLY = "\u064a\u0643\u0629"


def classify(text: str) -> str:
    """Heuristic script classification for a string carrying Arabic-script characters.

    Shared letters (alef, beh, seen ...) are common to both scripts, so a short string of
    shared letters classifies as `shared` - the check never guesses a language it cannot see.
    """
    persian = any(ch in PERSIAN_ONLY for ch in text)
    arabic = any(ch in ARABIC_ONLY for ch in text)
    if persian and not arabic:
        return "persian"
    if arabic and not persian:
        return "arabic-script (non-Persian marker)"
    return "shared letters (unclassified)"


def runs_in(text: str) -> int:
    """Maximal runs of Arabic-script characters: "a \u0633\u0644\u0627\u0645 b \u062e\u062f\u0627 c" -> 2."""
    return len(re.findall(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+", text))


def walk_strings(node, path: str, out: list) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            walk_strings(value, ("%s.%s" % (path, key)) if path else str(key), out)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            walk_strings(value, "%s[%d]" % (path, index), out)
    elif isinstance(node, str) and ARABIC.search(node):
        out.append((path, node))


def audit_document(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    found: list = []
    walk_strings(data, "", found)
    per_class: dict = {}
    for _p, text in found:
        key = classify(text)
        per_class[key] = per_class.get(key, 0) + 1
    return {
        "document": path.as_posix(),
        "locale": "fa" if is_fa_name(path.name) else "en",
        "strings": len(found),
        "runs": sum(runs_in(s) for _p, s in found),
        "chars": sum(len(ARABIC.findall(s)) for _p, s in found),
        "paths": len({p for p, _s in found}),
        "classes": per_class,
        "samples": [
            {
                "path": p,
                "runs": runs_in(s),
                "class": classify(s),
                "text": (s[:60] + "...") if len(s) > 60 else s,
            }
            for p, s in found[:4]
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="any finding is fatal")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--audit", action="store_true",
                    help="per-document units (strings/runs/chars/paths) with jsonpaths")
    args = ap.parse_args()

    docs = sorted(p for p in Path("templates").rglob("*.json"))
    if len(docs) < FLOOR:
        print("lang_mix_check: FAIL - only %d document(s) scanned (floor %d)" % (len(docs), FLOOR))
        return 1

    rows = []
    for path in docs:
        if is_fa_name(path.name):
            continue
        text = path.read_text(encoding="utf-8")
        chars = len(ARABIC.findall(text))
        strings = ARABIC_STRING.findall(text)
        if chars:
            rows.append({"document": path.as_posix(), "chars": chars, "strings": len(strings)})

    if args.audit:
        audited = [audit_document(p) for p in docs if not is_fa_name(p.name)
                   and ARABIC.search(p.read_text(encoding="utf-8"))]
        payload = {"scanned": len(docs), "floor": FLOOR, "documents": audited}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print("lang_mix_check --audit: %d document(s) scanned, %d non-FA document(s) with script"
                  % (len(docs), len(audited)))
            for row in audited:
                print("  %s  strings=%d runs=%d chars=%d paths=%d"
                      % (row["document"], row["strings"], row["runs"], row["chars"], row["paths"]))
                for sample in row["samples"]:
                    print("     %-58s %-34s %s" % (sample["path"], sample["class"], sample["text"]))
        return 0

    if args.json:
        print(json.dumps({"scanned": len(docs), "findings": rows}, ensure_ascii=False, indent=2))
    else:
        print("lang_mix_check: %d document(s) scanned, %d non-FA document(s) embed Arabic-script copy"
              % (len(docs), len(rows)))
        for row in rows:
            print("  ! %-52s %4d char(s) in %2d string(s)"
                  % (row["document"], row["chars"], row["strings"]))
        if not rows:
            print("  (clean)")

    if args.strict and rows:
        print("lang_mix_check: --strict - %d finding(s) are fatal" % len(rows))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
