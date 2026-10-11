# P1.7 - language-mix audit (measurement only)

**Status: MEASUREMENT. No string was moved, no template was touched, no fix was attempted.**
Owner of the fix: P8. Owner of the measurement: `tools/lang_mix_check.py --audit`.

## 1. Why this file exists

P1.5 reported *21 strings* per document. P1.6 reported *9 strings* per document. Both read the
same three documents. `docs/METRICS-RECONCILIATION.md` records the class of error; this file is the
measurement that proves which unit each phase was reading.

## 2. Counting units (the definition that was missing)

| unit | exact definition | value per document here | who quoted it |
| --- | --- | ---: | --- |
| `strings` | leaf JSON string values containing at least one Arabic-script character; one widget setting counts once however long it is | **9** | P1.6 |
| `runs` | maximal runs of Arabic-script characters; a setting with Latin text on both sides of a Persian phrase contributes 2 | **21** | P1.5 (as "strings") |
| `chars` | every character inside the Arabic-script ranges U+0600-U+06FF, U+0750-U+077F, U+FB50-U+FDFF, U+FE70-U+FEFF | **106** | P1.6 |
| `paths` | distinct jsonpaths (widget settings) holding at least one of those strings | **9** | P1.7 (new) |
| `documents` | non-FA-named documents with at least one hit | **3** | P1.5 + P1.6 |

A leaf setting that is a repeater row (`settings.icon_list[i].text`) is *one* string, *one* path,
and may hold *several* runs. Nothing is double-counted: the walk visits each leaf once.

Reproduce, from the repository root:

```
python3 tools/lang_mix_check.py                 # default: report-only, exit 0, floor 30 documents
python3 tools/lang_mix_check.py --audit         # units above, with sample jsonpaths
python3 tools/lang_mix_check.py --audit --json  # machine-readable, the source of this file
```

## 3. Reconciliation of the 21-vs-9 drift

| claim | phase | unit it was actually counting | verdict |
| --- | --- | --- | --- |
| "21 strings each" | P1.5 (`docs/DECISIONS.md` P1.5-005) | maximal script-character runs | **true in its unit, mislabelled**: measured `runs` = 21 on all three documents |
| "9 strings each" (+ 106 chars) | P1.6 (`DECISIONS.md` P1.6-004) | leaf JSON string values | **true in its unit**; the earlier "21" counted character runs, which is why the numbers looked contradictory |
| "63 mixed-language strings" (P1.6, all documents) | P1.6 | script-character **runs** across the three documents (3 x 21 = 63) | **true in the run unit, mislabelled as strings** - see note below |

> **Note on 63.** The tree holds 9 + 9 + 9 = **27** leaf strings, 21 + 21 + 21 = **63** runs and
> **318** characters. The P1.6 handoff and `DECISIONS.md` P1.6-004 call 63 "strings"; 63 is really
> the **run** total, and the string total is 27 - the same unit mix-up as P1.5, reused one phase
> later, which is why this reconciliation exists as a file rather than a footnote. **Superseded
> by: 27 strings / 63 runs / 318 chars across 3 documents.** `DECISIONS.md` P1.7-002 records the
> correction; the old sentence stays in the append-only ledger, void as a count.

## 4. Per-document measurement

| document | locale by name | strings | runs | chars | paths | script class of its strings |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `templates/blocks/capability-cards.json` | en | 9 | 21 | 106 | 9 | persian x6, shared letters (unclassified) x3 |
| `templates/pages/aurora-home-en.json` | en | 9 | 21 | 106 | 9 | persian x6, shared letters (unclassified) x3 |
| `templates/pages/aurora-services.json` | en | 9 | 21 | 106 | 9 | persian x6, shared letters (unclassified) x3 |

## 5. Where the strings actually live

All nine hits in each document are rows of the **same Icon List widget**, so the defect is one
repeated component, not scattered copy. The path set is identical across the three documents
apart from the top-level container index:

| # | jsonpath (relative to the document root, top index varies) |
| ---: | --- |
| 1 | `content[0].elements[0].elements[1].elements[0].elements[3].settings.icon_list[0].text` |
| 2 | `content[0].elements[0].elements[1].elements[0].elements[3].settings.icon_list[1].text` |
| 3 | `content[0].elements[0].elements[1].elements[0].elements[3].settings.icon_list[2].text` |
| 4 | `content[0].elements[0].elements[1].elements[1].elements[3].settings.icon_list[0].text` |
| 5 | `content[0].elements[0].elements[1].elements[1].elements[3].settings.icon_list[1].text` |
| 6 | `content[0].elements[0].elements[1].elements[1].elements[3].settings.icon_list[2].text` |
| 7 | `content[0].elements[0].elements[1].elements[2].elements[3].settings.icon_list[0].text` |
| 8 | `content[0].elements[0].elements[1].elements[2].elements[3].settings.icon_list[1].text` |
| 9 | `content[0].elements[0].elements[1].elements[2].elements[3].settings.icon_list[2].text` |

| sample text (from the tool output) | heuristic script class |
| --- | --- |
| حافظه مکالمه | persian |
| انتقال به انسان | shared letters (unclassified) |
| رضایتسنجی | persian |
| خلاصه با ارجاع | shared letters (unclassified) |

Across the three documents the classifier sees persian x18, shared letters (unclassified) x9.

**Limit of the heuristic, stated so it is not overread:** only فارسی-specific letters (پ چ ژ گ ک ی)
and Arabic-only letters (ي ك ة) separate the scripts; a string written entirely in letters shared
by both scripts is reported `shared letters (unclassified)` rather than guessed. The strings here
are Persian demo copy (the FA pages carry the same block), but this file does not claim a
language it cannot measure from the bytes.

## 6. Ratchet

`docs/_generated/invariant-baseline.json` records `lang_mix_documents: 3` and
`lang_mix_strings: 27`. The invariant is `lang_mix_hits_in_non_fa_documents == known_baseline`: the
number may not grow while the freeze is on, and when P8 cleans the copy the baseline must be
updated in the same commit. It is deliberately **not** zero-tolerance yet: a strict gate would
paint CI red for a defect this phase is forbidden to fix.

