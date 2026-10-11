#!/usr/bin/env python3
"""Invariant ratchet (P1.7 item 6).

The eight invariants that P1.6 wired into CI ran with `continue-on-error: true`, which is a step
that can only ever print. This runner converts them into a **no-regression gate**:

  * a *contract* must hold now (alt coverage, Theme Builder count, colours/typography/families,
    zero Custom HTML widgets, the alt policy existing, no unqualified widget-type claim);
  * a *ratchet* is allowed to sit at a known-bad value recorded in
    `docs/_generated/invariant-baseline.json`; it fails when it gets **worse**, and it fails when
    it gets **better** too, because an improvement that does not update the baseline is an
    undocumented value change (update it in the same commit with `--write-baseline`).

    python3 tools/invariant_check.py                   # the gate (exit 1 on any FAIL)
    python3 tools/invariant_check.py --json            # machine-readable
    python3 tools/invariant_check.py --write-baseline  # record the CURRENT values (deliberate)

The value of a ratchet is that it never pretends a defect is fixed: `main` sits at 1 of 9, `h1` at
6 bad documents, `post_title` absent, 48 dead anchors, 3 language-mixed documents, 9 flagged alts,
24 asset URLs on a movable ref - all recorded, all allowed *today*, none of them invisible.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACTS = ROOT / "docs" / "_generated" / "facts.json"
BASELINE = ROOT / "docs" / "_generated" / "invariant-baseline.json"
TEMPLATES = ROOT / "templates"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alt_quality_check as altq  # noqa: E402  (single source for alt measurement)

# name -> (facts key or None, direction, note). "down" = lower is better, "up" = higher is better.
RATCHETS = (
    ("dead_anchor_occurrences", "down", "settings.link.url targets that resolve nowhere in their doc"),
    ("dead_anchor_documents", "down", "documents carrying at least one dead in-page target"),
    ("h1_zero_documents", "down", "pages+archive+search documents with no h1"),
    ("h1_zero_documents_pages_loop", "down", "the same predicate over pages+loop (the P3 scope)"),
    ("h1_not_exactly_one_documents", "down", "documents whose h1 count is not exactly one"),
    ("lang_mix_documents", "down", "non-FA-named documents embedding Arabic-script copy"),
    ("lang_mix_strings", "down", "leaf string values carrying Arabic-script characters"),
    ("lang_mix_runs", "down", "maximal runs of Arabic-script characters"),
    ("lang_mix_chars", "down", "Arabic-script characters"),
    ("alt_quality_findings", "down", "alt instances flagged by tools/alt_quality_check.py"),
    ("alt_proper_noun_only_distinct", "down", "distinct client-name-only alt strings"),
    ("asset_urls_on_mutable_tag", "down", "emitted image URLs addressing the movable git tag"),
    ("main_containers", "up", "containers with html_tag=main (the P2 accessibility target)"),
)
CONTRACTS = (
    ("alt_coverage", "alt_nonempty_count == image_widget_count"),
    ("theme_builder_layouts", "== 7"),
    ("colours_typography_families", "== 19 / 15 / 3"),
    ("custom_html_widgets", "== 0 (constitution: no content in Custom HTML)"),
    ("alt_policy_documented", "== true (docs/a11y-alt-policy.md carries R1-R4)"),
    ("unqualified_widget_type_claim", "== 0 documents"),
)


def claim_scan() -> list:
    """Surfaces that assert a widget-type count the control audit cannot support (P1.6 lesson)."""
    claim = re.compile(r"\b\d+\s+(free|Pro)\b[^\n]{0,40}widget", re.I)
    surfaces = ["README.md", "CHANGELOG.md", "templates/INDEX.md"]
    surfaces += [p.as_posix() for p in sorted((ROOT / "docs").rglob("*.md"))
                 if p.name != "CLAIMS.md" and not p.name.startswith("HANDOFF")]
    hits = []
    for rel in surfaces:
        path = ROOT / rel
        if path.exists() and claim.search(path.read_text(encoding="utf-8")):
            hits.append(rel)
    return hits


def post_title_present() -> bool:
    for path in TEMPLATES.rglob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("type") == "kit":
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if node.get("widgetType") in ("post-title", "theme-post-title"):
                    return True
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return False


def asset_urls_on_tag() -> int:
    n = 0
    for path in TEMPLATES.rglob("*.json"):
        n += path.read_text(encoding="utf-8").count("kit-assets-v1")
    return n


def asset_base_form() -> str:
    """'sha' when tokens.py already emits commit-SHA URLs, else 'tag'."""
    text = (ROOT / "tools" / "aurora" / "tokens.py").read_text(encoding="utf-8")
    block = text.split("ASSET_BASE", 1)[1].split(")", 1)[0] if "ASSET_BASE" in text else ""
    return "sha" if re.search(r"\b[0-9a-f]{40}\b", block) else "tag"


def measure(facts: dict) -> dict:
    alt = altq.measure()
    out = {key: facts[key] for key, _direction, _note in RATCHETS if key in facts}
    out["asset_urls_on_mutable_tag"] = asset_urls_on_tag()
    out["asset_url_form"] = asset_base_form()
    out["post_title_widget_present"] = post_title_present()
    out["widget_claim_documents"] = claim_scan()
    out["alt_nonempty_count"] = alt["alt_nonempty_count"]
    out["image_widget_count"] = alt["image_widget_count"]
    out["alt_policy_documented"] = alt["alt_policy_documented"]
    out["theme_builder_layouts"] = facts["theme_builder_layouts"]
    out["global_colours"] = facts["global_colours"]
    out["typography_styles"] = facts["typography_styles"]
    out["font_families"] = facts["font_families"]
    out["custom_html_widgets"] = facts["custom_html_widgets"]
    return out


def current_baseline(present: dict, contracts: list) -> dict:
    return {
        "generated_by": "python3 tools/invariant_check.py --write-baseline",
        "note": ("Known values are allowed; any worsening FAILS the gate; any improvement must "
                 "update this file in the same commit. Contracts are also recorded so that a "
                 "contract break is reported as a contract break, not as drift."),
        "ratchets": {name: present[name] for name, _d, _n in RATCHETS},
        "ratchets_not_in_facts": {"post_title_widget_present": present["post_title_widget_present"]},
        "contracts": {name: value for name, value, _ok in contracts},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-baseline", action="store_true")
    args = ap.parse_args()

    if not FACTS.exists():
        print("invariant_check: missing %s - run tools/verify.py --report first"
              % FACTS.relative_to(ROOT))
        return 1
    facts = json.loads(FACTS.read_text(encoding="utf-8"))
    present = measure(facts)
    if len(present) < 12:
        print("invariant_check: FAIL - only %d value(s) measured (non-empty assertion)" % len(present))
        return 1

    contracts = []
    contracts.append(("alt_coverage",
                      "%d/%d" % (present["alt_nonempty_count"], present["image_widget_count"]),
                      present["alt_nonempty_count"] == present["image_widget_count"] and
                      present["alt_nonempty_count"] > 0))
    contracts.append(("theme_builder_layouts", str(present["theme_builder_layouts"]),
                      present["theme_builder_layouts"] == 7))
    contracts.append(("colours_typography_families",
                      "%s / %s / %s" % (present["global_colours"], present["typography_styles"],
                                        present["font_families"]),
                      (present["global_colours"], present["typography_styles"],
                       present["font_families"]) == (19, 15, 3)))
    contracts.append(("custom_html_widgets", str(present["custom_html_widgets"]),
                      present["custom_html_widgets"] == 0))
    contracts.append(("alt_policy_documented", str(present["alt_policy_documented"]),
                      present["alt_policy_documented"] is True))
    contracts.append(("unqualified_widget_type_claim", str(len(present["widget_claim_documents"])),
                      not present["widget_claim_documents"]))

    if args.write_baseline:
        BASELINE.write_text(json.dumps(current_baseline(present, contracts), indent=1,
                                       sort_keys=True) + "\n", encoding="utf-8")
        print("invariant_check: baseline written -> %s" % BASELINE.relative_to(ROOT))
        return 0

    if not BASELINE.exists():
        print("invariant_check: FAIL - no baseline at %s (run --write-baseline and commit it)"
              % BASELINE.relative_to(ROOT))
        return 1
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    rows, fails = [], []

    for name, direction, note in RATCHETS:
        if name not in baseline.get("ratchets", {}):
            print("invariant_check: FAIL - %r missing from the baseline" % name)
            return 1
        base, now = baseline["ratchets"][name], present[name]
        if now == base:
            rows.append(("PASS (known value %s)" % base, name, now, note))
        elif (direction == "down" and now < base) or (direction == "up" and now > base):
            rows.append(("FAIL improvement - update baseline", name, now, note))
            fails.append(name)
        else:
            rows.append(("FAIL regression (baseline %s)" % base, name, now, note))
            fails.append(name)

    base_pt = baseline.get("ratchets_not_in_facts", {}).get("post_title_widget_present", False)
    now_pt = present["post_title_widget_present"]
    if now_pt == base_pt:
        rows.append(("PASS (known value %s)" % base_pt, "post_title_widget_present", now_pt,
                     "no post-title widget tree-wide (P2 target)"))
    elif now_pt:
        rows.append(("FAIL improvement - update baseline", "post_title_widget_present", now_pt,
                     "the post title appeared: record it"))
        fails.append("post_title_widget_present")
    else:
        rows.append(("FAIL regression", "post_title_widget_present", now_pt, "post title disappeared"))
        fails.append("post_title_widget_present")

    for name, measured, ok in contracts:
        rows.append(("PASS" if ok else "FAIL contract", name, measured, ""))
        if not ok:
            fails.append(name)

    # asset URLs: the ratchet degenerates into the strict guard the moment ASSET_BASE is repointed
    if present["asset_url_form"] == "sha" and present["asset_urls_on_mutable_tag"] != 0:
        rows.append(("FAIL contract", "asset_urls_use_commit_sha",
                     present["asset_urls_on_mutable_tag"],
                     "ASSET_BASE carries a commit SHA, so no emitted URL may address the tag"))
        fails.append("asset_urls_use_commit_sha")

    if args.json:
        print(json.dumps({"rows": [{"status": s, "name": n, "measured": str(m), "note": note}
                                   for s, n, m, note in rows],
                          "asset_base_form": present["asset_url_form"],
                          "fails": fails}, ensure_ascii=False, indent=2))
    else:
        print("invariant_check: %d value(s) measured, asset URLs use the %s form"
              % (len(present), present["asset_url_form"]))
        for status, name, measured, note in rows:
            print("  %-38s %-34s measured=%s%s" % (status, name, measured,
                                                   ("  # " + note) if note else ""))
        print("invariant_check: %d row(s) flagged" % len(fails))
        if fails:
            print("  ! %s" % ", ".join(fails))
            print("  ! a regression is a defect; an improvement means the baseline must be updated "
                  "in the same commit (tools/invariant_check.py --write-baseline)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
