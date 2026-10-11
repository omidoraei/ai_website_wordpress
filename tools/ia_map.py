#!/usr/bin/env python3
"""IA map - every Elementor template document, and the sections it contains, in order.

Evidence producer for docs/p3/IA.md. Read-only: it never edits templates/.
It writes docs/p3/ia-map.json (machine) and docs/p3/ia-map.md (reading copy).

Non-empty assertion (constitution): the walk must find at least MIN_DOCUMENTS
templates and MIN_SECTIONS top-level sections, or the tool exits 1. "No output"
is only a valid result if there was something to look at.

Usage: python3 tools/ia_map.py
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "templates")
OUT = os.path.join(ROOT, "docs", "p3")
MIN_DOCUMENTS = 30
MIN_SECTIONS = 50

TAG_RE = re.compile(r"<[^>]+>")


def text_of(settings, keys=("title", "editor", "text", "shortcode")):
    for k in keys:
        v = settings.get(k)
        if isinstance(v, str) and v.strip():
            return html.unescape(TAG_RE.sub("", v)).strip()
    return ""


def first_heading(elements):
    for e in elements:
        if e.get("elType") == "widget" and e.get("widgetType") in ("heading", "text-editor"):
            t = text_of(e.get("settings") or {})
            if t:
                return t[:60]
        r = first_heading(e.get("elements") or [])
        if r:
            return r
    return ""


def walk_counts(elements, acc):
    for e in elements:
        et = e.get("elType")
        if et == "container":
            acc["containers"] += 1
        elif et == "widget":
            acc["widgets"] += 1
            wt = e.get("widgetType")
            acc["widget_types"].add(wt)
            if wt == "button":
                acc["buttons"] += 1
            elif wt == "image":
                acc["images"] += 1
            elif wt in ("form", "search-form"):
                acc["forms"] += 1
        walk_counts(e.get("elements") or [], acc)
    return acc


def walk_buttons(elements, out):
    for e in elements:
        if e.get("elType") == "widget" and e.get("widgetType") == "button":
            st = e.get("settings") or {}
            out.append({"label": text_of(st)[:40], "link": (st.get("link") or {}).get("url", "")})
        walk_buttons(e.get("elements") or [], out)
    return out


def lang_of(rel):
    base = os.path.splitext(os.path.basename(rel))[0]
    return "fa" if (base.startswith("fa-") or base.endswith("-fa")) else "en"


def main():
    docs = []
    skipped = []
    for dirpath, _dirnames, filenames in os.walk(TPL):
        for fn in sorted(filenames):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, TPL)
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
            if doc.get("type") == "kit":
                skipped.append(rel)
                continue
            sections = []
            for idx, el in enumerate(doc.get("content") or []):
                st = el.get("settings") or {}
                acc = walk_counts([el], {"containers": 0, "widgets": 0, "buttons": 0,
                                         "images": 0, "forms": 0, "widget_types": set()})
                sections.append({
                    "index": idx,
                    "anchor": st.get("_element_id", ""),
                    "html_tag": st.get("html_tag", ""),
                    "responsive_keys": sorted(k for k in st
                                              if k.endswith("_tablet") or k.endswith("_mobile")),
                    "hidden": [k for k in ("hide_desktop", "hide_tablet", "hide_mobile")
                               if st.get(k)],
                    "first_heading": first_heading([el]),
                    "widget_types": sorted(acc["widget_types"]),
                    "counts": {"containers": acc["containers"], "widgets": acc["widgets"],
                               "buttons": acc["buttons"], "images": acc["images"],
                               "forms": acc["forms"]},
                    "buttons": walk_buttons([el], []),
                })
            tot = walk_counts(doc.get("content") or [], {"containers": 0, "widgets": 0,
                                                         "buttons": 0, "images": 0, "forms": 0,
                                                         "widget_types": set()})
            docs.append({
                "path": rel,
                "type": doc.get("type"),
                "title": doc.get("title", ""),
                "lang": lang_of(rel),
                "sections": sections,
                "totals": {"containers": tot["containers"], "widgets": tot["widgets"],
                           "buttons": tot["buttons"], "images": tot["images"], "forms": tot["forms"]},
            })
    docs.sort(key=lambda d: (d["type"], d["path"]))
    sections_total = sum(len(d["sections"]) for d in docs)
    if len(docs) < MIN_DOCUMENTS:
        print("ia_map: examined %d documents, floor is %d - non-empty assertion failed"
              % (len(docs), MIN_DOCUMENTS), file=sys.stderr)
        return 1
    if sections_total < MIN_SECTIONS:
        print("ia_map: examined %d sections, floor is %d - non-empty assertion failed"
              % (sections_total, MIN_SECTIONS), file=sys.stderr)
        return 1

    reuse = {}
    for d in docs:
        for s in d["sections"]:
            if s["anchor"]:
                reuse.setdefault(s["anchor"], []).append(d["path"][:-5])
    reuse = {k: sorted(v) for k, v in sorted(reuse.items()) if len(v) > 1}

    # CTA target audit: an in-page `#target` must exist as an _element_id in the SAME
    # document, otherwise the button is a dead anchor on that page.
    target_use = {}
    dead_docs = []
    for d in docs:
        anchors = {s["anchor"] for s in d["sections"] if s["anchor"]}
        used = set()
        for s in d["sections"]:
            for b in s["buttons"]:
                link = (b["link"] or "").strip()
                if link.startswith("#") and len(link) > 1:
                    used.add(link)
        d["cta_targets"] = {"in_page": sorted(used),
                            "dead": sorted(t for t in used if t[1:] not in anchors)}
        if d["cta_targets"]["dead"]:
            dead_docs.append(d["path"])
        for t in used:
            rec = target_use.setdefault(t, {"used_in": [], "resolves_in": []})
            rec["used_in"].append(d["path"])
            if t[1:] in anchors:
                rec["resolves_in"].append(d["path"])
    target_use = {t: {"used_in": sorted(v["used_in"]), "resolves_in": sorted(v["resolves_in"])}
                  for t, v in sorted(target_use.items())}

    payload = {
        "generated_by": "tools/ia_map.py",
        "floors": {"documents": MIN_DOCUMENTS, "sections": MIN_SECTIONS},
        "stats": {"documents": len(docs), "sections": sections_total,
                  "kit_documents": skipped, "documents_with_dead_cta_targets": len(dead_docs)},
        "anchor_reuse": reuse,
        "cta_targets": target_use,
        "documents": docs,
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "ia-map.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")

    lines = ["# IA map (generated)", "",
             "Produced by `python3 tools/ia_map.py`. Do not hand-edit; re-run the tool.",
             "",
             "Documents: **%d** · top-level sections: **%d** · kit documents skipped: %d"
             % (len(docs), sections_total, len(skipped)), "",
             "## Section inventory", ""]
    for d in docs:
        lines.append("### `%s` — %s (%s, %s)" % (d["path"], d["title"], d["type"], d["lang"]))
        lines.append("")
        lines.append("| # | anchor | tag | first heading | widgets | containers | buttons | images |")
        lines.append("| ---: | --- | --- | --- | --- | ---: | ---: | ---: |")
        for s in d["sections"]:
            lines.append("| %d | `%s` | %s | %s | %s | %d | %d | %d |" % (
                s["index"], s["anchor"] or "-", s["html_tag"] or "-",
                s["first_heading"].replace("|", "\\|") or "-",
                ", ".join(t for t in s["widget_types"] if t) or "-",
                s["counts"]["containers"], s["counts"]["buttons"], s["counts"]["images"]))
        lines.append("")
    lines.append("## Anchors reused across documents")
    lines.append("")
    lines.append("| anchor | documents |")
    lines.append("| --- | --- |")
    for anchor, where in reuse.items():
        lines.append("| `%s` | %d — %s |" % (anchor, len(where), ", ".join(w[:-5] for w in where)))
    lines.append("")
    lines.append("## In-page CTA targets")
    lines.append("")
    lines.append("A `#target` resolves only where the same document carries that `_element_id`.")
    lines.append("")
    lines.append("| target | used in (docs) | resolves in (docs) |")
    lines.append("| --- | ---: | ---: |")
    for t, v in target_use.items():
        lines.append("| `%s` | %d | %d |" % (t, len(v["used_in"]), len(v["resolves_in"])))
    lines.append("")
    lines.append("Documents with at least one dead in-page target: **%d**" % len(dead_docs))
    lines.append("")
    with open(os.path.join(OUT, "ia-map.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print("ia_map: %d documents, %d sections, %d reused anchors, %d docs with dead CTA "
          "targets -> docs/p3/ia-map.{json,md}"
          % (len(docs), sections_total, len(reuse), len(dead_docs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
