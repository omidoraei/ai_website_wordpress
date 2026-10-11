#!/usr/bin/env python3
"""
Extract Elementor control ids, types and responsive flags from a pinned checkout
of the Elementor source, so every claim in this skill's references carries a
file:line provenance instead of a memory.

    git clone --depth 1 --branch v3.35.9 https://github.com/elementor/elementor /tmp/elementor
    python3 scripts/extract_controls.py --source /tmp/elementor --tag v3.35.9

Writes (relative to the skill root):
    references/_generated/control-index.md   every add_control / group field, with line numbers
    references/_generated/widget-taxonomy.md Free vs Pro widget types, by presence in the source
    references/_generated/summary.json       machine-readable counts, consumed by CI

Nothing here is hand-written knowledge: if a name is not in the output, it does not
exist for this skill (see SKILL.md rule 3).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(SKILL_ROOT, "references", "_generated")

# Control ids are always the first single-quoted string after add_control( / 'name' =>.
ADD_CONTROL = re.compile(r"add_control\(")
ADD_GROUP = re.compile(r"add_group_control\(")
FIRST_STRING = re.compile(r"'([A-Za-z0-9_\-]+)'")
NAME_KEY = re.compile(r"'name'\s*=>\s*'([A-Za-z0-9_\-]+)'")
GROUP_CLASS = re.compile(r"Group_Control_([A-Za-z]+)::get_type")
FIELD_KEY = re.compile(r"^\s*\$fields\['([A-Za-z0-9_\-]+)'\]\s*=\s*\[")
RESPONSIVE = re.compile(r"'responsive'\s*=>\s*true")
CSS_VAR = re.compile(r"'(--[a-z0-9\-]+):")
TYPE_SELECT = re.compile(r"'type'\s*=>\s*Controls_Manager::([A-Z_]+)")
SELECTOR_SELECT = re.compile(r"'selectors'\s*=>\s*\[")

# widget registry: the namespace declares a WIDGET_NAME / get_name() value
WIDGET_NAME = re.compile(r"public function get_name\(\)\s*\{?\s*\n?\s*return\s+'([^']+)'")
WIDGET_TITLE = re.compile(r"public function get_title\(\)\s*\{?\s*\n?\s*return\s+(?:esc_html__\(\s*)?'([^']+)'")


def read(path: str) -> List[str]:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def find_controls(lines: List[str]) -> List[Dict[str, Any]]:
    """Every add_control / add_group_control call with its id and line number."""
    out: List[Dict[str, Any]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*"):
            continue
        is_group = bool(ADD_GROUP.search(line))
        if not (is_group or ADD_CONTROL.search(line)):
            continue
        window = lines[i:i + 12]
        blob = "\n".join(window)
        if is_group:
            gclass = GROUP_CLASS.search(blob)
            name = NAME_KEY.search(blob)
            if not name:
                continue
            out.append({
                "line": i + 1,
                "id": name.group(1),
                "kind": "group",
                "group": ("Group_Control_%s" % gclass.group(1)) if gclass else "?",
                "responsive": bool(RESPONSIVE.search(blob[index_of_type(blob):]
                                                     if False else blob)),
            })
        else:
            m = FIRST_STRING.search(blob)
            if not m:
                continue
            cid = m.group(1)
            # skip the add_control( 'args' => ... ) style false positives
            if cid.startswith("elType") or len(cid) > 60:
                continue
            t = TYPE_SELECT.search(blob)
            out.append({
                "line": i + 1,
                "id": cid,
                "kind": "control",
                "type": t.group(1) if t else "",
                "responsive": bool(RESPONSIVE.search(blob)),
            })
    return out


def index_of_type(blob: str) -> int:  # pragma: no cover - helper kept for clarity
    m = TYPE_SELECT.search(blob)
    return m.end() if m else 0


def find_group_fields(lines: List[str]) -> List[Dict[str, Any]]:
    """$fields['x'] = [ ... ] blocks inside a group class."""
    out: List[Dict[str, Any]] = []
    for i, line in enumerate(lines):
        m = FIELD_KEY.match(line)
        if not m:
            continue
        # the field block ends at the next top-level $fields[ or the method end
        end = i + 1
        depth = line.count("[") - line.count("]")
        while end < len(lines) and depth > 0:
            depth += lines[end].count("[") - lines[end].count("]")
            end += 1
        blob = "\n".join(lines[i:end])
        var = CSS_VAR.search(blob)
        t = TYPE_SELECT.search(blob)
        out.append({
            "line": i + 1,
            "id": m.group(1),
            "type": t.group(1) if t else "",
            "responsive": bool(RESPONSIVE.search(blob)),
            "css_var": var.group(1) if var else "",
            "selectors": bool(SELECTOR_SELECT.search(blob)),
        })
    return out


def widget_files(root: str) -> List[str]:
    d = os.path.join(root, "includes", "widgets")
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".php")]


def element_files(root: str) -> List[str]:
    """includes/elements/*.php — container.php carries the container's own controls."""
    d = os.path.join(root, "includes", "elements")
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".php")]


def group_files(root: str) -> List[str]:
    d = os.path.join(root, "includes", "controls", "groups")
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".php")]


def kit_tab_files(root: str) -> List[str]:
    d = os.path.join(root, "core", "kits", "documents", "tabs")
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".php")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="path to an elementor checkout")
    ap.add_argument("--tag", default="unknown")
    args = ap.parse_args()

    root = os.path.abspath(args.source)
    if not os.path.isdir(os.path.join(root, "includes")):
        print("not an elementor checkout: %s" % root)
        return 1

    # non-empty assertion (docs/METRICS.md \u00a73): a source tree that yields no files
    # must fail loudly instead of writing a plausible-looking empty index.
    counts = {"widgets": len(widget_files(root)), "elements": len(element_files(root)),
              "groups": len(group_files(root)), "kit tabs": len(kit_tab_files(root))}
    floors = {"widgets": 10, "elements": 1, "groups": 8, "kit tabs": 5}
    print("source scan: " + ", ".join("%s=%d" % (k, counts[k]) for k in counts))
    short = {k: (counts[k], floors[k]) for k in counts if counts[k] < floors[k]}
    if short:
        for k, (got, floor) in sorted(short.items()):
            print("  ! %s: %d file(s), floor is %d" % (k, got, floor))
        return 1

    os.makedirs(GEN, exist_ok=True)
    summary: Dict[str, Any] = {"tag": args.tag}

    # ---- widgets ---------------------------------------------------------
    lines_out: List[str] = []
    lines_out.append("# Generated control index")
    lines_out.append("")
    lines_out.append("Source: `elementor/elementor@%s` — vendored in `vendor/elementor/` "
                     "(sha256 in `skills/elementor-native-kit/SKILL.md`; the gate verifies the "
                     "checksum before extraction)." % args.tag)
    lines_out.append("Regenerate with `scripts/extract_controls.py --source <extracted vendor "
                     "archive> --tag %s`." % args.tag)
    lines_out.append("")
    lines_out.append("**Do not edit.** If a control name is not in this file, this skill does "
                     "not know it, and neither should a template.")
    lines_out.append("")

    taxonomy: List[Dict[str, Any]] = []
    for path in widget_files(root) + element_files(root):
        rel = os.path.relpath(path, root)
        lines = read(path)
        blob = "\n".join(lines)
        name = WIDGET_NAME.search(blob)
        title = WIDGET_TITLE.search(blob)
        controls = find_controls(lines)
        taxonomy.append({
            "widget": name.group(1) if name else os.path.basename(path)[:-4],
            "title": title.group(1) if title else "",
            "file": rel,
            "controls": len(controls),
        })
        kind = "element" if "/elements/" in rel else "widget"
        lines_out.append("## `%s` — %s `%s`" % (rel, kind, name.group(1) if name else "?"))
        lines_out.append("")
        lines_out.append("| line | id | kind | type | responsive |")
        lines_out.append("| ---: | --- | --- | --- | --- |")
        for c in controls:
            lines_out.append("| %d | `%s` | %s | %s | %s |" % (
                c["line"], c["id"], c.get("group") or c["kind"],
                c.get("type", ""), "yes" if c["responsive"] else ""))
        lines_out.append("")

    # ---- groups ----------------------------------------------------------
    lines_out.append("# Control groups")
    lines_out.append("")
    lines_out.append("A group contributes controls whose final id is `<name>_<field>`, where "
                     "`<name>` is the group's `name` in the consuming widget.")
    lines_out.append("")
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for path in group_files(root):
        rel = os.path.relpath(path, root)
        lines = read(path)
        cls = re.search(r"class Group_Control_([A-Za-z_]+)\b", "\n".join(lines[:40]))
        gtype = cls.group(1).lower().replace("_", "-") if cls else None
        fields = find_group_fields(lines)
        groups[rel] = fields
        lines_out.append("## `%s` — group type `%s`" % (rel, gtype or "?"))
        lines_out.append("")
        lines_out.append("| line | field id | type | responsive | css var | selectors |")
        lines_out.append("| ---: | --- | --- | --- | --- | --- |")
        for f in fields:
            lines_out.append("| %d | `%s` | %s | %s | %s | %s |" % (
                f["line"], f["id"], f["type"], "yes" if f["responsive"] else "",
                "`%s`" % f["css_var"] if f["css_var"] else "", "yes" if f["selectors"] else ""))
        lines_out.append("")

    # ---- kit tabs --------------------------------------------------------
    lines_out.append("# Kit site-settings tabs")
    lines_out.append("")
    for path in kit_tab_files(root):
        rel = os.path.relpath(path, root)
        lines = read(path)
        blob = "\n".join(lines)
        controls = find_controls(lines)
        lines_out.append("## `%s`" % rel)
        lines_out.append("")
        lines_out.append("| line | id | kind | type |")
        lines_out.append("| ---: | --- | --- | --- |")
        for c in controls:
            lines_out.append("| %d | `%s` | %s | %s |" % (
                c["line"], c["id"], c.get("group") or c["kind"], c.get("type", "")))
        lines_out.append("")

    open(os.path.join(GEN, "control-index.md"), "w", encoding="utf-8").write(
        "\n".join(lines_out) + "\n")

    # ---- taxonomy --------------------------------------------------------
    free = sorted({t["widget"] for t in taxonomy})
    tax = ["# Widget taxonomy (Free vs Pro)", "",
           "Derived by presence: a widget type whose class exists in",
           "`elementor/elementor@%s` is **Free**; anything else the kit emits is **Pro**."
           % args.tag, "",
           "| widget type | class file | controls indexed | tier |",
           "| --- | --- | ---: | --- |"]
    for t in sorted(taxonomy, key=lambda x: x["widget"]):
        tax.append("| `%s` | `%s` | %d | free |" % (t["widget"], t["file"], t["controls"]))
    open(os.path.join(GEN, "widget-taxonomy.md"), "w", encoding="utf-8").write(
        "\n".join(tax) + "\n")

    summary["free_widgets"] = free
    summary["widget_files"] = len(taxonomy)
    summary["groups"] = {k: len(v) for k, v in groups.items()}
    summary["kit_tabs"] = [os.path.relpath(p, root) for p in kit_tab_files(root)]
    summary["control_count"] = sum(t["controls"] for t in taxonomy)

    with open(os.path.join(GEN, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)

    print("extracted from %s @ %s" % (root, args.tag))
    print("  widget classes : %d (%d controls indexed)"
          % (len(taxonomy), summary["control_count"]))
    print("  control groups : %d (%d fields)"
          % (len(groups), sum(len(v) for v in groups.values())))
    print("  kit tab files  : %d" % len(summary["kit_tabs"]))
    print("  free widget ids: %d" % len(free))
    print("  wrote          : %s" % os.path.relpath(GEN, SKILL_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
