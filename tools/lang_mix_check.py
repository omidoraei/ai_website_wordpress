#!/usr/bin/env python3
"""Language-mixing check: English-named documents that embed Persian/Arabic-script copy.

Why this exists: `tools/bidi_check.py` cannot catch this class. Persian is valid bidi input and
needs no control characters, so a page that mixes Persian copy into an English document passes
the bidi scan silently (P1.5, three documents, 21 strings each). P8 owns the fix; this checker
owns the measurement.

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="any finding is fatal")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
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
