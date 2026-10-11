#!/usr/bin/env python3
"""Landmark + heading audit over every container and heading widget in templates/.

Evidence producer for docs/p3/landmark-audit.md. Read-only.
Writes docs/p3/landmark-audit.json and docs/p3/landmark-audit.md.

What it checks
  1. html_tag usage per document (which containers are landmarks)
  2. page-level documents (pages/**, loop/**) that lack a `main` landmark
  3. header/footer documents whose root is not marked header/footer
  4. heading levels from heading widgets (`header_size`): missing h1 / multiple h1
  5. honest limits: `nav` is provided by the Pro nav-menu widget's own tag default and
     is not stored in the JSON, so this audit reports it as "not visible in JSON" rather
     than pretending it passed. Verify on a real Pro install.

Non-empty assertion: >= MIN_DOCUMENTS documents and >= MIN_CONTAINERS containers,
else exit 1.

Usage: python3 tools/landmark_audit.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "templates")
OUT = os.path.join(ROOT, "docs", "p3")
MIN_DOCUMENTS = 30
MIN_CONTAINERS = 500

LANDMARKS = {"header", "nav", "main", "footer", "article", "aside", "section"}
PAGE_LEVEL_DIRS = ("pages", "loop")
TAG_RE = re.compile(r"<[^>]+>")


def walk(elements, containers, tags, headings):
    for e in elements:
        if e.get("elType") == "container":
            st = e.get("settings") or {}
            containers.append(st.get("html_tag") or "")
        if e.get("elType") == "widget":
            st = e.get("settings") or {}
            # Any widget carrying header_size is a heading, not only the `heading` widget:
            # theme widgets (theme-archive-title, theme-post-title) store the same key.
            size = (st.get("header_size") or "").lower()
            if size or e.get("widgetType") == "heading":
                title = TAG_RE.sub("", st.get("title") or st.get("text") or "").strip()[:60]
                level = size if re.fullmatch(r"h[1-6]", size) else ("p" if size else "unset")
                headings.append({"level": level, "text": title, "widget": e.get("widgetType")})
        walk(e.get("elements") or [], containers, tags, headings)
    return containers, tags, headings


def widget_types(elements, out):
    for e in elements:
        if e.get("elType") == "widget":
            out.add(e.get("widgetType"))
        widget_types(e.get("elements") or [], out)
    return out


def main():
    docs = []
    for dirpath, _dirnames, filenames in os.walk(TPL):
        for fn in sorted(filenames):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, TPL)
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
            if doc.get("type") == "kit":
                continue
            containers, _tags, headings = walk(doc.get("content") or [], [], {}, [])
            hist = {}
            for t in containers:
                if t:
                    hist[t] = hist.get(t, 0) + 1
            h1s = [h for h in headings if h["level"] == "h1"]
            wts = widget_types(doc.get("content") or [], set())
            gaps = []
            top = os.path.dirname(rel)
            if doc.get("type") == "single" and not (wts & {"theme-post-title", "post-title"}):
                gaps.append("no post-title widget - the post renders without its visible "
                            "title and without an `h1`")
            if top in PAGE_LEVEL_DIRS and hist.get("main", 0) == 0:
                gaps.append("no `main` landmark")
            if hist.get("main", 0) > 1:
                gaps.append("%d `main` landmarks (must be 1)" % hist["main"])
            if top == "headers" and hist.get("header", 0) == 0:
                gaps.append("header document without a `header` landmark")
            if top == "footers" and hist.get("footer", 0) == 0:
                gaps.append("footer document without a `footer` landmark")
            if top in PAGE_LEVEL_DIRS:
                if not h1s:
                    gaps.append("no `h1` heading")
                elif len(h1s) > 1:
                    gaps.append("%d `h1` headings (must be 1)" % len(h1s))
            docs.append({
                "path": rel,
                "type": doc.get("type"),
                "containers": len(containers),
                "tagged": sum(1 for t in containers if t),
                "tags": dict(sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))),
                "headings": {"count": len(headings), "levels": _levels(headings),
                             "h1": ["%s (%s)" % (h["text"], h["widget"]) for h in h1s],
                             "widget_types": sorted({h.get("widget") for h in headings}),
                             "widgets": sorted(wts)},
                "gaps": gaps,
            })
    docs.sort(key=lambda d: d["path"])
    total_containers = sum(d["containers"] for d in docs)
    total_tagged = sum(d["tagged"] for d in docs)
    if len(docs) < MIN_DOCUMENTS:
        print("landmark_audit: examined %d documents, floor is %d - non-empty assertion failed"
              % (len(docs), MIN_DOCUMENTS), file=sys.stderr)
        return 1
    if total_containers < MIN_CONTAINERS:
        print("landmark_audit: examined %d containers, floor is %d - non-empty assertion failed"
              % (total_containers, MIN_CONTAINERS), file=sys.stderr)
        return 1

    aggregate = {}
    for d in docs:
        for tag, n in d["tags"].items():
            aggregate[tag] = aggregate.get(tag, 0) + n
    gap_docs = [d for d in docs if d["gaps"]]

    payload = {
        "generated_by": "tools/landmark_audit.py",
        "floors": {"documents": MIN_DOCUMENTS, "containers": MIN_CONTAINERS},
        "stats": {"documents": len(docs), "containers": total_containers,
                  "tagged": total_tagged, "tag_histogram": dict(sorted(aggregate.items(),
                                                                       key=lambda kv: -kv[1])),
                  "documents_with_gaps": len(gap_docs)},
        "documents": docs,
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "landmark-audit.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    lines = ["# Landmark and heading audit (generated)", "",
             "Produced by `python3 tools/landmark_audit.py` over **%d documents** and "
             "**%d containers** (%d carry an `html_tag`). Do not hand-edit; re-run the tool."
             % (len(docs), total_containers, total_tagged), "",
             "## Tag histogram across the whole tree", "",
             "| html_tag | containers |", "| --- | ---: |"]
    for tag, n in sorted(aggregate.items(), key=lambda kv: -kv[1]):
        lines.append("| `%s` | %d |" % (tag, n))
    lines += ["", "## Per document", "",
              "| document | type | containers | tagged | landmarks | h1 | gaps |",
              "| --- | --- | ---: | ---: | --- | --- | --- |"]
    for d in docs:
        lm = ", ".join("%s×%d" % (t, n) for t, n in d["tags"].items() if t in LANDMARKS) or "—"
        lines.append("| `%s` | %s | %d | %d | %s | %s | %s |" % (
            d["path"], d["type"], d["containers"], d["tagged"], lm,
            d["headings"]["h1"][0] if d["headings"]["h1"] else "—",
            "; ".join(d["gaps"]) or "—"))
    lines += ["", "## Documents with gaps", ""]
    if not gap_docs:
        lines.append("None.")
    for d in gap_docs:
        lines.append("- `%s`: %s" % (d["path"], "; ".join(d["gaps"])))
    lines += ["", "## Honest limits", "",
              "- `nav` is not detectable here: the Pro `nav-menu` widget renders its own tag and "
              "does not store it in the template JSON. Verify on a real Pro install "
              "(see `docs/OPEN-QUESTIONS.md`).",
              "- `article` is expected only inside Loop Item templates; the kit ships none today, "
              "so 0 is correct, not a gap.",
              "- Popups render inside Elementor's own dialog wrapper; the audit judges only the "
              "template content it can see."]
    with open(os.path.join(OUT, "landmark-audit.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("landmark_audit: %d documents, %d containers, %d tagged, %d with gaps -> "
          "docs/p3/landmark-audit.{json,md}"
          % (len(docs), total_containers, total_tagged, len(gap_docs)))
    return 0


def _levels(headings):
    out = {}
    for h in headings:
        out[h["level"]] = out.get(h["level"], 0) + 1
    return dict(sorted(out.items()))


if __name__ == "__main__":
    sys.exit(main())
