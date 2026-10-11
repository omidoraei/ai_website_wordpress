#!/usr/bin/env python3
"""
Audit every control key the kit's templates emit against the pinned Elementor
source. A key that cannot be explained by the source is either a Pro control
(no public source: see references/05-pro-vs-free.md) or a defect.

    python3 scripts/audit_control_names.py            # human report
    python3 scripts/audit_control_names.py --json     # machine output for CI

Reads references/_generated/control-index.md (produced by extract_controls.py),
so this never touches the network and never guesses.

Exit codes: 0 = no unexplained keys, 1 = unexplained keys found.
Anything unexplained is printed with the templates that use it, so a fix is a
one-line change in tools/aurora/.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(SKILL_ROOT))
INDEX = os.path.join(SKILL_ROOT, "references", "_generated", "control-index.md")
TEMPLATES = os.path.join(REPO, "templates")

# Keys owned by Elementor's page/document settings, not by elements.
PAGE_SETTINGS = {"hide_title", "template", "post_status", "custom_css"}

# Traits that contribute controls to a widget whose own file registers none.
TRAIT_OF = {"button": "button"}


def parse_index() -> tuple[dict, dict]:
    """-> ({file: [(line, id, kind, type, responsive)]}, {group_type: [(field, responsive)]})"""
    txt = open(INDEX, encoding="utf-8").read()
    files: dict = {}
    groups: dict = {}
    parts = re.split(r"\n## ", txt)
    for part in parts:
        head = part.split("\n", 1)[0]
        m = re.match(r"`(includes/(?:widgets|controls/groups|elements)/[\w\-/]+\.php)` "
                     r"— (?:widget|element|group type) `([^`]+)`", head)
        if not m:
            continue
        path, token = m.group(1), m.group(2)
        rows = []
        for line in part.split("\n"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) >= 3 and re.match(r"^\d+$", c[0]):
                rows.append((int(c[0]), c[1].strip("`"), c[2] if len(c) > 2 else "",
                             c[3] if len(c) > 3 else "", (c[4] if len(c) > 4 else "") == "yes"))
        if "/groups/" in path:
            groups[token] = [(r[1], r[4]) for r in rows if r[2] and r[2] != "HEADING"]
        else:
            files[path] = rows
    return files, groups


CLASS_TO_TYPE = {
    "Group_Control_Background": "background",
    "Group_Control_Border": "border",
    "Group_Control_Box_Shadow": "box-shadow",
    "Group_Control_Css_Filter": "css-filter",
    "Group_Control_Flex_Container": "flex-container",
    "Group_Control_Flex_Item": "flex-item",
    "Group_Control_Grid_Container": "grid-container",
    "Group_Control_Image_Size": "image-size",
    "Group_Control_Text_Shadow": "text-shadow",
    "Group_Control_Text_Stroke": "text-stroke",
    "Group_Control_Typography": "typography",
}


def expand(rows, groups) -> set:
    """Control ids a file can legitimately write, including group fields."""
    ok = set()
    for _line, cid, kind, _type, resp in rows:
        ok.add(cid)
        if cid.startswith(("_",)):
            continue
        gtype = CLASS_TO_TYPE.get(kind)
        if not gtype:
            continue
        for field, f_resp in groups.get(gtype, []):
            ok.add("%s_%s" % (cid, field))
            if f_resp or resp:
                ok.add("%s_%s_tablet" % (cid, field))
                ok.add("%s_%s_mobile" % (cid, field))
    return ok


def widget_pool(files, groups) -> dict:
    base = set()
    for path in ("includes/widgets/common-base.php", "includes/widgets/common-optimized.php",
                 "includes/elements/container.php"):
        if path in files:
            base |= expand(files.get(path, []), groups)

    pool = {"container": set(base), "__base__": base}
    for path, rows in files.items():
        if "/widgets/" not in path:
            continue
        m = re.search(r"widget `([^`]+)`", "")
        name = os.path.basename(path)[:-4]
        ids = expand(rows, groups)
        trait = TRAIT_OF.get(name)
        if trait:
            tpath = "includes/widgets/traits/%s-trait.php" % trait
            if tpath in files:
                ids |= expand(files[tpath], groups)
        pool[name] = ids | base
    return pool


def walk(node):
    yield node
    for child in node.get("elements") or []:
        yield from walk(child)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(INDEX):
        print("missing %s - run scripts/extract_controls.py first" % INDEX)
        return 1

    files, groups = parse_index()
    pool = widget_pool(files, groups)

    unknown = collections.Counter()
    where = collections.defaultdict(set)
    per_file: dict = {}
    templates_seen = 0
    keys_seen = 0
    for root, _dirs, names in os.walk(TEMPLATES):
        for fn in sorted(names):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(root, fn)
            doc = json.load(open(path, encoding="utf-8"))
            if doc.get("type") == "kit":
                continue
            templates_seen += 1
            total = matched = 0
            misses = collections.Counter()
            for top in doc["content"]:
                for el in walk(top):
                    wt = el.get("widgetType") if el.get("elType") == "widget" else "container"
                    allowed = pool.get(wt, pool["__base__"] | {""})
                    for key in (el.get("settings") or {}):
                        total += 1
                        keys_seen += 1
                        if key in PAGE_SETTINGS or key in allowed:
                            matched += 1
                            continue
                        stem = re.sub(r"_(tablet|mobile|widescreen|laptop)$", "", key)
                        if stem in allowed:
                            matched += 1
                            continue
                        misses[key] += 1
                        unknown[(wt, key)] += 1
                        where[(wt, key)].add(os.path.relpath(path, REPO))
            per_file[os.path.relpath(path, REPO)] = (total, matched, misses)

    MIN_TEMPLATES, MIN_KEYS = 30, 500
    index_elements = sorted(p for p in files if "/elements/" in p)
    print("index coverage: %d file(s) in control-index.md, of which %d are "
          "includes/elements/ : %s"
          % (len(files), len(index_elements), ", ".join(os.path.basename(p) for p in index_elements)))
    print("template scan: %d document(s), %d settings key(s)" % (templates_seen, keys_seen))
    if templates_seen < MIN_TEMPLATES or keys_seen < MIN_KEYS:
        print("  ! non-empty assertion failed (floors: %d documents, %d keys) - "
              "a scan of nothing is not a pass" % (MIN_TEMPLATES, MIN_KEYS))
        return 1
    print("per file  settings_total  matched  unmatched_by_name")
    for rel in sorted(per_file):
        total, matched, misses = per_file[rel]
        names = ", ".join("%s x%d" % (k, n) for k, n in sorted(misses.items())[:3]) or "-"
        print("  %-46s %5d %8d  %s" % (rel, total, matched, names))

    result = {
        "unexplained_keys": len(unknown),
        "occurrences": sum(unknown.values()),
        "widgets_with_unexplained": sorted({w for w, _ in unknown}),
        "keys": [{"widget": w, "key": k, "count": n,
                  "templates": sorted(where[(w, k)])} for (w, k), n in unknown.most_common()],
    }
    if args.json:
        print(json.dumps(result, indent=1))
    else:
        print("control-name audit against the pinned source")
        print("  unexplained keys : %d" % result["unexplained_keys"])
        print("  occurrences      : %d" % result["occurrences"])
        print("  widgets involved : %s" % ", ".join(result["widgets_with_unexplained"]))
        print()
        for row in result["keys"][:40]:
            print("  %-16s %-38s x%-4d %s"
                  % (row["widget"], row["key"], row["count"],
                     ", ".join(os.path.basename(t) for t in row["templates"][:2])))
        if len(result["keys"]) > 40:
            print("  ... %d more (use --json)" % (len(result["keys"]) - 40))
    return 1 if unknown else 0


if __name__ == "__main__":
    sys.exit(main())
