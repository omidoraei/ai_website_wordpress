# P2 readiness gate (P1.8)

Every box is verified by a command, not by memory. P2 opens only when all eight are checked; the
attestation box may be carried as **MISSING** on an explicit human decision to proceed under
CLASS-B-PENDING (not recommended - see `docs/BRIEF-ATTESTATION.md`).

| | check | state | evidence |
| --- | --- | --- | --- |
| [x] | fresh CI run success, 0 errors | PASS | runs `38163624987` (pull_request) and `38163621438` (push) on `baa30d5`, both conclusion `success`; check runs `114541518610` / `114541508171` report `annotations=0`; 25 of 25 steps success, failed steps `[]` |
| [x] | live PR body proof green | PASS | live sha256 `d9b5ee59008f8ae8b4322b7ec31faaaa91f3b8e95f9d65ddadc71207e86f9f8d`; all nine stale patterns return 0 hits; retraction guard `30 file(s), 23 phrase(s), pr=scanned`, exit 0; records: `docs/CLAIMS.md` C-032 |
| [ ] | attestation file committed or explicitly missing | **MISSING** | `docs/BRIEF-ATTESTATION.md` carries `ATTESTATION_INPUT_MISSING`; no row upgraded; `docs/DECISIONS.md` P1.8-002 |
| [x] | invariant baseline reconciled to P1.7 units | PASS | `docs/_generated/invariant-baseline.json`: dead anchors 48 occurrences / 18 documents / 39 scanned; main 1 of 9 page-level documents; h1 7 zero in pages+loop and 6 not-exactly-one in pages+archive+search; post_title absent; lang mix 27 strings / 63 runs / 318 chars / 3 documents; fa_documents 8 by name, 11 by content; alt 24 non-empty / 13 distinct / 9 flagged (3 distinct) |
| [x] | asset URL contract recorded | PASS | tag ratchet at 24 today (`asset_urls_on_mutable_tag`), hard failure on any increase, and the step degenerates to "no emitted URL may address the tag" as soon as `ASSET_BASE` carries the commit SHA; decision `docs/DECISIONS.md` P1.7-004; CI step "Asset URL immutability"; repoint deferred to P2 because `templates/**` is frozen |
| [x] | B5 anti-regression sentence intact | PASS | `docs/BRIEF.md:133`, `docs/DECISIONS.md` P-BRIEF-010, `docs/p1/type-decision.md:120` all carry the SUPERSEDING + do-not-reintroduce wording |
| [x] | no frozen design paths touched | PASS | `git diff --name-only d6ee888..HEAD -- templates tokens dist media preview dials.toml dna.yaml BANLIST.md` prints nothing |
| [x] | HANDOFF-P1.8.md written | PASS | committed with this file; the phase's turn ledger is 6/6 with no silent jumps |

## What P2 inherits

1. **First P2 commit: the asset repoint** - `ASSET_BASE` to the commit-SHA raw URL, rebuild
   `templates/**` + `dist/**` committed together, then the asset step proves 0 tag URLs. The
   migration is already build-proven (24 SHA URLs, 0 tag URLs in a scratch copy).
2. **The ratchet is the regression net**: any worsening of the 13 recorded values fails CI, and any
   improvement must update `invariant-baseline.json` in the same commit.
3. **Open defects are numbered, not hidden**: `main` 1/9, h1 6 bad (7 in the page-level scope), no
   post-title widget, 48 dead anchors, 3 language-mixed documents, 9 flagged alt instances, and the
   two PROVISIONAL SAMPLE rows carried from P1-DISPOSITION.
4. **Renderer drift to re-sync**: the two PR-body sentences refined in P1.8 item 3 live in the live
   body and are recorded in `docs/CLAIMS.md` C-032; `tools/render_docs.py`'s PR template still emits
   the previous wording, so the next regeneration must re-apply them (or the template is updated
   when it is next in scope).

## Decision required before P2

The attestation box is the only unchecked item. Either paste the ten answers into
`docs/BRIEF-ATTESTATION.md` (converting them to CLASS-A), or state explicitly that P2 proceeds under
CLASS-B-PENDING. The recommendation on record: **do not proceed without the attestation.**
