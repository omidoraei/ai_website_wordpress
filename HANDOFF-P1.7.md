# HANDOFF-P1.7 — pre-gate precision repair

**Phase:** P1.7 (mechanical; no design decisions, no P2 work, no gate-2 answers).
**Date:** 2026-10-12. **Cap:** 8 turns. **Used:** 8/8 — every turn narrated, no silent jumps.
**Gate 2 remains HOLD.** Freeze respected: `templates/**`, `dials.toml`, `dna.yaml`, `BANLIST.md`,
`preview/**`, `media/**`, `dist/**` are untouched (`git status` shows no changes in any of them;
`tools/aurora/tokens.py` gained comments only, and a rebuild produces **no diff**).

## 1. Turn ledger

| turn | action |
| ---: | --- |
| 1 | Recon: git state, `ASSET_BASE` / `kit-assets-v1` references, `BRIEF-ATTESTATION.md` (empty), METRICS/facts keys, `kit.yml` step map, `grep -ro kit-assets-v1 templates/` = 24 hits / 9 files. |
| 2 | Item 1: labels and status table in `docs/BRIEF.md` + `docs/PBRIEF-TRANSCRIPT.md`; `AGENTS.md` gains the CLASS-B-PENDING definition; `DECISIONS.md` P1.7-001; `CLAIMS.md` C-012 re-graded. |
| 3 | Item 5: `tools/lang_mix_check.py` extended (`--audit`, `--json`, unit definitions, script classifier, jsonpath walk); audit measured 9 strings / 21 runs / 106 chars per document. |
| 4 | Item 5 doc: `docs/p1.7/lang-mix-audit.md` generated from the tool's own JSON; item 2 instrument: `tools/alt_quality_check.py` refactored around `measure()`; `docs/a11y-alt-policy.md` written (rules R1-R4). |
| 5 | Item 3: extracted the CI invariant heredoc and ran it (4/8 FAIL, dead anchors 48); censused all three dead-anchor producers (18 documents / 48 occurrences / the 77 first-pass artifact); read `settings._element_id`, the key this kit actually writes. |
| 6 | Item 3 delivery: canonical anchor rule in `tools/verify.py` + 20 new facts; `docs/METRICS-RECONCILIATION.md`; `docs/METRICS.md` §6 with both units; item 2's claim repairs (`CLAIMS.md` C-017/C-028/C-030, four new blocklist phrases, `alt-text-sample.md`, `08-agent-legibility.md`, `02-design-system.md`, `IA.md`); PR #1 body regenerated and PATCHed (`132ddd16…`); guard clean at 30 files / 23 phrases. |
| 7 | Items 4 and 6: repoint proven in a scratch copy (24 URLs on the SHA, 0 on the tag, build exit 0) + host check; `tools/invariant_check.py` + `docs/_generated/invariant-baseline.json`; the report-only CI step replaced by the ratchet and a dedicated asset-URL step; `kit.yml` validated (21 steps). |
| 8 | Full local chain, fresh-clone guard/invariant run, CI, this handoff. |

No turn was merged; nothing was skipped. The cap was reached exactly, so the residue in §6 is the
phase's residue, not a stopped-work artifact.

## 2. Item-by-item result

**Item 1 — attribution down-graded.** `docs/BRIEF.md` now reads **HUMAN-ASSERTED (chat) -
CLASS-B-PENDING file attestation** in the header, the evidence rule and all ten rows, plus a
per-row status table (`id | option | current class | what is missing | conversion action`).
`docs/PBRIEF-TRANSCRIPT.md` carries the same label in the verdict and all ten table rows.
`AGENTS.md` defines the label ("grade a chat-only answer CLASS-B-PENDING, never B"). The ten
answers were not deleted, not re-asked, and the B5 anti-regression sentence is unchanged
(`BRIEF.md` §6, `DECISIONS.md` P-BRIEF-010, `docs/p1/type-decision.md`).
`docs/BRIEF-ATTESTATION.md` is still empty — nothing was fabricated.

**Item 2 — alt presence measured as *quality*.** `tools/alt_quality_check.py` (new, floor 20 image
widgets, `measure()` importable so `verify.py` and the ratchet share one implementation) reports:
`image_widget_count 24`, `alt_field_path_used settings.image.alt`, `alt_nonempty_count 24`,
`alt_empty_count 0`, `alt_distinct_count 13`, by locale `en 17/17 · fa 7/7`, length distribution
`1-15: 10 · 16-40: 7 · 41-80: 7` (min/max/mean 10/53/26.2), `suspected_decorative_with_nonempty_alt
0`, `suspected_content_with_generic_alt 0`, `alt_locale_mismatch 0`,
`suspected_proper_noun_only_alt 9 instances / 3 distinct strings`, `repeated_alt_across_different_image_files 0`.
`docs/a11y-alt-policy.md` defines R1 content / R2 decorative / R3 logo / R4 FA alt; the tool fails
if a rule disappears. No alt text was rewritten.

**Item 3 — drift reconciled by definition, not by erasure.** `docs/METRICS-RECONCILIATION.md`:
dead anchors **48 occurrences across 18 of 39 documents** (P3's 18 was the document unit, P1.6's 48
the occurrence unit, and P1.7's first pass printed 77 because it read a top-level `_element_id`
that this kit never writes); the per-target table reproduces P3's numbers exactly
(`#contact 16/1 · #docs 12/0 · #demo 5/0 · #about 2/0 · #login 2/0 · #release 2/0 · #services 4/4 ·
#portfolio 4/4`); `main` = 1 container / 9 page-level documents (P3's 11 is the pages+loop scope);
`h1` = 7 (pages+loop, zero) and 6 (pages+archive+search, not exactly one); language mix = **3
documents, 27 leaf strings, 63 runs, 318 chars** (P1.5's 21 = runs, P1.6's 9 = strings, P1.6's 63
= the run total); `fa_documents` = 8 by name, 11 by content (3 EN-named). Old numbers are kept in
place with their units named. `docs/METRICS.md` §6 adds both units as generated fields;
`docs/_generated/facts.json` carries the new keys.

**Item 4 — asset URLs: proven migration, explicit blocker, strict-on-repoint guard.**
*Proven:* in a scratch copy (`/tmp/p17probe`), repointing `ASSET_BASE` to
`raw.githubusercontent.com/<sha>/media` builds cleanly (exit 0) and emits **24 SHA URLs, 0 tag
URLs**. *Network fact:* the direct raw host is unreachable from this sandbox
(`SSL_ERROR_SYSCALL`, HTTP 000), while `github.com/<user>/<repo>/raw/<sha>/media/<file>` answers
**302** from the sandbox and redirects to exactly the raw URL above.
*Blocker (governance, not sandbox):* this phase freezes `templates/**`, and CI's reproducibility
step requires any rebuild to be committed with the generator change, so the repoint cannot land
here without committing 24 rewritten image settings and the dist rebuild. The honest delivery is
therefore the one the phase prescribes: a **CI step that fails when an emitted URL addresses the
movable tag** (`Asset URL immutability`, next to the tag pin and above `Asset URLs are live`),
plus a **buyer-facing warning** in `docs/01-installation.md`, `docs/02-design-system.md` and the PR
body (which no longer calls the tag immutable). The step is a ratchet at the recorded 24 today and
becomes the strict guard automatically the moment `ASSET_BASE` carries a 40-hex commit.
`CLAIMS.md` C-030 records that the immutability contract is the commit-SHA URL, not the pin.

**Item 5 — language-mix measurement only.** `docs/p1.7/lang-mix-audit.md`: per document the tool
reports strings / runs / chars / paths (9 / 21 / 106 / 9), the nine jsonpaths (all
`settings.icon_list[i].text` of one Icon List widget repeated across the three documents), a
Persian-vs-Arabic heuristic with its limit stated, and the 21-vs-9 reconciliation. No string was
moved; `templates/**` untouched.

**Item 6 — report-only becomes a ratchet.** `tools/invariant_check.py` + `docs/_generated/invariant-baseline.json`
record the known FAILs (main 1/9, h1 6 bad + 7 page-level, post-title absent, 48 dead anchors,
27/63/318 language mix, 9 flagged alt instances, 24 tag URLs) and the contracts that must hold now
(alt coverage 24/24, Theme Builder 7, colours/typography/families 19/15/3, Custom HTML 0, alt
policy documented, 0 unqualified widget-type claims). A worsening fails; an improvement must update
the baseline **in the same commit** (`--write-baseline`). The CI step is a hard gate (no
`continue-on-error`).

## 3. Evidence at close

```
python3 tools/verify.py --report      -> RESULT clean; 36 doc-number claims checked
python3 tools/render_docs.py --check  -> 51 slot(s) across 11 file(s), all agree
python3 tools/invariant_check.py      -> 24 value(s) measured, 0 row(s) flagged (exit 0)
python3 tools/lang_mix_check.py       -> 40 scanned, 3 non-FA documents (report-only, exit 0)
python3 tools/alt_quality_check.py    -> 24 widgets, 24 non-empty, 13 distinct (exit 0)
python3 tools/bidi_check.py           -> clean (exit 0)
documents/*_number* chain             -> all green
retraction guard (fresh clone)        -> 30 file(s), 23 phrase(s), 2 commit line(s), pr=scanned, exit 0
```

* `docs/BRIEF.md` — attribution status table with CLASS-B-PENDING labels.
* `docs/a11y-alt-policy.md` + `tools/alt_quality_check.py` — the alt measurement and its rules.
* `docs/METRICS-RECONCILIATION.md` — dead anchors and language mix resolved by definition.
* `docs/p1.7/lang-mix-audit.md` — per-document units and jsonpaths.
* `docs/_generated/invariant-baseline.json` — the recorded known values.
* `.github/workflows/kit.yml` — `Invariant ratchet` (hard) + `Asset URL immutability` (hard) +
  the tag pin (unchanged) — 21 steps, YAML validated.
* Live PR #1 body regenerated and PATCHed; sha256 of the PATCHed body `132ddd16…` (local and live
  agree).

## 4. Decisions taken / reversed

| id | decision | why |
| --- | --- | --- |
| P1.7-001 | The ten selections are CLASS-B-PENDING, not class B | class B requires the file review + confirmation; `BRIEF-ATTESTATION.md` is empty. P1.5 under-read, P1.6 over-read |
| P1.7-002 | Language-mix numbers are reconciled by unit | the word "strings" meant runs in P1.5 and leaf strings in P1.6 |
| P1.7-003 | Canonical anchor rule = `settings._element_id`; dead anchors 48/18; the 77 first-pass reading is void | the top-level key does not exist in this kit; the P1.6 CI heredoc found the right key only by accident, so the invariant now has one implementation |
| P1.7-004 | The immutability contract is the commit-SHA URL; the tag pin is secondary; the repoint is deferred to P2 | a git tag is movable and the buyer imports URLs, not CI checks; `templates/**` is frozen this phase |
| P1.7-005 | Alt quality measured; the "Persian alt inside the EN set" claim retracted | the checker measures 0 locale mismatches; the Persian copy in EN-named documents is Icon List text |
| P1.7-006 | Invariants become a no-regression ratchet | report-only produced a red-by-design step nobody reads; a ratchet catches regressions without pretending defects are fixed |

Reversals recorded against earlier phases: **P1.6's class-B grading** (P1.7-001), **P1.6's
"immutable tag" wording** (C-030, PR body + two docs), **P1.6's alt quality sentence** (C-017/C-028),
**P1.7's own first-pass anchor count** (77 → void, P1.7-003).

## 5. Files touched

`AGENTS.md` · `docs/BRIEF.md` · `docs/PBRIEF-TRANSCRIPT.md` · `docs/CLAIMS.md` ·
`docs/DECISIONS.md` · `docs/METRICS.md` · `docs/METRICS-RECONCILIATION.md` (new) ·
`docs/a11y-alt-policy.md` (new) · `docs/p1.7/lang-mix-audit.md` (new) ·
`docs/01-installation.md` · `docs/02-design-system.md` · `docs/08-agent-legibility.md` ·
`docs/p3/IA.md` · `docs/p3/alt-text-sample.md` · `docs/_generated/{facts.json,facts.md,invariant-baseline.json}` ·
`tools/verify.py` · `tools/render_docs.py` · `tools/lang_mix_check.py` ·
`tools/alt_quality_check.py` (new) · `tools/invariant_check.py` (new) · `tools/aurora/tokens.py`
(comments + `ASSET_SHA`) · `.github/workflows/kit.yml` · `HANDOFF-P1.7.md`.

Not touched (frozen): `templates/**`, `preview/**`, `media/**`, `dist/**`, `dials.toml`,
`dna.yaml`, `BANLIST.md`.

## 6. Residue and open questions (gate-2 bundle, no answers given here)

1. **`docs/BRIEF-ATTESTATION.md` is still empty** — the highest-priority gate-2 input; a committed
   paste converts rows to class A without touching anything else.
2. **Item 4's repoint is deferred**: P2 must change `ASSET_BASE` to the SHA form, commit the
   rebuild, and watch the strict asset step (already in CI) go green on 0 tag URLs. The raw host
   cannot be HEAD-checked from this sandbox; CI's existing `Asset URLs are live` step covers it
   after the repoint.
3. **P2/P8 defects stay open and are now numbered in the ratchet**: `main` 1/9, `h1` 6 bad (7
   page-level), no post-title widget, 48 dead anchors, 3 language-mixed documents, 9 flagged alts.
4. **Gate-2 questions untouched** (SAMPLE policy, parity shape, footer entity, image licences,
   `#demo`), no P2 work started, no new detectors beyond the two the phase named.
5. Next 3 actions after gate 2: (a) apply the asset repoint as the first P2 commit, (b) land the P2
   fix order from `docs/p1/delta-table.md` with the ratchet as the regression net, (c) drive the
   baseline to zero and flip `--strict` on the alt and language checks at P8.
