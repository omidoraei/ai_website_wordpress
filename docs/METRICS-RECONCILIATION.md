# Metric reconciliation (P1.7)

**Why this file exists.** Three phases quoted numbers for the same defects and the numbers disagreed
(18 / 48 / 77 dead anchors; 21 / 9 / 63 language-mix strings; 7 / 6 missing `h1`). Every one of the
three measurements was arithmetically right **in a unit nobody named**. This file names the units,
supersedes the old numbers without erasing them, and points at the canonical field in
`docs/_generated/facts.json` that a future sentence must cite.

**Rule from here on:** a metric sentence that does not name its unit is a defect. `docs/METRICS.md`
now carries both the document-level and the occurrence-level counter for each of these, and
`python3 tools/verify.py --report` is still the only producer.

## 1. The reconciliation table

| metric | P3 said | P1.5 said | P1.6 said | P1.7 canonical (measured) | definition now | cause of the drift | canonical field |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dead in-page anchors | 18 of 39 docs | - | 48 | **48 occurrences across 18 documents** (39 scanned) | **occurrence** = one `settings.link.url` of the form `#x` whose `x` matches no element's `settings._element_id` in the same document; **document** = a document with at least one such occurrence | P3 counted **documents**, P1.6 counted **occurrences**, and P1.7's first pass counted **77** by reading a top-level `_element_id` key that this kit never writes (anchors live in `settings._element_id`) | `dead_anchor_occurrences`, `dead_anchor_documents`, `dead_anchor_documents_scanned` |
| dead anchors, per target | `#contact` 16 used / 1 resolves; `#docs` 12 / 0; `#demo` 5 / 0; `#about` 2 / 0; `#login` 2 / 0; `#release` 2 / 0; `#services` 4 / 4; `#portfolio` 4 / 4 | - | - | identical under the canonical rule | both columns are **documents** (not occurrences): documents that use the target / documents where it resolves | none - P3's table was correct; only the unit was implicit | `dead_anchor_target_documents` |
| `main` landmark | 11 page-level docs without `main` | - | 1 of 9 | **1 `main` container; 9 page-level documents; 11 documents missing it in the pages+loop scope** | counts are scope-bound: the `main` sits in the loop (single-post) document, so 0 of the 11 pages+archive+search docs carry one | different **denominator**: P3 used page-level = `pages/` + `loop/` (12 docs), the invariant used `pages/` (9) | `main_containers`, `main_page_level_documents` |
| missing `h1` | 7 docs | - | 6 docs | **7 with zero `h1` (pages+loop scope) and 6 with `h1 != 1` (pages+archive+search scope)** | scope **and** predicate differ: "missing" = zero `h1`; the invariant tests "exactly one" over a different document set | two different questions were both written as "docs without h1" | `h1_zero_documents_pages_loop`, `h1_zero_documents`, `h1_not_exactly_one_documents`, `h1_scope_documents` |
| language mixing | - | 21 "strings" each | 9 "strings" each; 63 "strings" total | **3 documents, 27 leaf strings, 63 runs, 318 chars** | leaf string value containing at least one Arabic-script character (P1.6's unit); maximal run of script characters (P1.5's unit) | "strings" was used for two units across two phases: P1.5 counted **runs** (21 per doc), P1.6 counted **leaf strings** (9 per doc) and then quoted the run total (63) as strings | `lang_mix_documents`, `lang_mix_strings`, `lang_mix_runs`, `lang_mix_chars` |
| Persian documents | - | 8 (naming) | 8 (naming) + "three further documents embed Persian copy" | **8 by the name predicate, 11 by content, 3 of the 11 are EN-named** | name predicate: basename starts `fa-` or ends `-fa.json`; content predicate: the document JSON contains at least one Arabic-script character | the two predicates answer different questions and never collided (FontAwesome classes are Latin) | `fa_documents`, `fa_documents_by_content` |
| alt-text quality | 24 of 24 "no alt" (wrong key) | repeated P3 | "all 24 carry alt; three client-name-only alts" | **24 non-empty, 13 distinct, 9 flagged instances of which 3 are distinct strings** | instance = one Image widget; distinct = one unique alt string | P3 measured `settings.alt` (always empty); the quality sentence mixed instances and distinct strings | `alt_nonempty_count`, `alt_distinct_count`, `alt_quality_findings`, `alt_proper_noun_only_distinct` |
| asset URL immutability | - | - | tag pinned by SHA in CI | **24 emitted URLs still address the movable tag; the immutable form is the commit-SHA raw URL** (see `docs/DECISIONS.md` P1.7-004) | the buyer-facing contract is the URL in the emitted template, not the CI check | the pin protects the repo, not the artifact a buyer imports | `docs/a11y-alt-policy.md` is unrelated; see `HANDOFF-P1.7.md` item 4 |

## 2. What the drift cost, in one line per case

* **Dead anchors.** P3's 18/39 and P1.6's 48 are the same defect in two units; nobody had to be
  wrong, and a single sentence naming the unit would have prevented two phases of "which is it".
* **`h1`.** 7 and 6 are both true; they are not the same question. The invariant keeps the stricter
  predicate (`h1 != 1`, scope = pages + archive + search) because "exactly one" is what the
  landmark audit wants; the P3 number stays in the tree as the page-level count.
* **Language mixing.** P1.5 was right (21 runs), P1.6 was right (9 leaf strings), and P1.6's own
  summary was wrong (63 is the run total, not a string total). This is the clearest case for the
  rule above.
* **Alt text.** The unit drift is the smaller half of the story: the first measurement read a key
  Elementor never writes, which is a *wrong measurement*, not a different unit. Both classes are
  recorded here because the reader needs to tell them apart.

## 3. The anchor rule, stated once (canonical)

Elementor stores the CSS id of an element in `settings._element_id`; the in-page link lives in
`settings.link.url`. Therefore:

> `#target` **resolves** in a document iff at least one element of that document has
> `settings._element_id == target`. Resolution is per document: the same `#contact` is live on one
> page and dead on another, and the count is only meaningful with the scope named.

Implementation: `tools/verify.py` (`compute_facts`), pinned by the invariant runner in
`tools/invariant_check.py`. The P1.6 CI heredoc that measured 48 by walking *all* JSON values (and
therefore found the ids by accident) is replaced by that single source, so the number can no longer
come from two implementations.

## 4. How to re-derive every number here

```
python3 tools/verify.py --report        # writes docs/_generated/facts.json (the canonical fields)
python3 tools/lang_mix_check.py --audit # the language-mix units, per document
python3 tools/alt_quality_check.py      # the alt units, per widget
python3 tools/landmark_audit.py         # html_tag / h1 / main, page-level scope (pages + loop)
python3 tools/ia_map.py                 # the per-target CTA table
```

Nothing in this file is hand-computed; if a value here disagrees with `facts.json`, `facts.json`
wins and this file is stale.
