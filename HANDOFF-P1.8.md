# HANDOFF-P1.8 — CI contradiction resolution + attestation closure

**Phase:** P1.8 (mechanical; no P2, no design decisions, no gate-2 answers). **Cap:** 6 turns.
**Used:** 6/6, every turn narrated. **Gate 2 remains HOLD.**
**Frozen paths untouched:** `git diff --name-only d6ee888..HEAD -- templates tokens dist media
preview dials.toml dna.yaml BANLIST.md` prints nothing.

## 1. Turn ledger

| turn | action |
| ---: | --- |
| 1 | Item 0: reproduced the contradiction from raw API output before touching anything - run/step conclusions, `--log-failed` attempt, check-run annotation records, and the annotation-count history for the last 20 commits. Cause named: **F (other)** - a tolerated advisory step's exit code, not a failed gate. |
| 2 | Item 1: the advisory step rebuilt in `.github/workflows/kit.yml` (findings printed + summarised, **no annotation**; a crash still fails). Caught and fixed the known YAML trap (an unquoted `": "` in the new step name produced a `ScannerError`; the name is now quoted). Stub-tested both paths: exit 1 -> step exit 0, exit 3 -> step exit 3 with `::error::`. `docs/CLAIMS.md` C-031 + `docs/DECISIONS.md` P1.8-001. Commit `baa30d5`, pushed. |
| 3 | Item 2: new runs proved - `38163624987` (pull_request) and `38163621438` (push) on `baa30d5`: conclusion `success`, **annotations=0** on both check runs, 25/25 steps success, failed steps `[]`, artifact `aurora-ai-kit` 356 144 bytes `sha256:a61b0332…f048bf`. |
| 4 | Item 3: live PR body fetched and hashed; nine stale patterns 0 hits; two sentences refined (FA type system **user-chosen: Vazirmatn**, **Arad is not bundled**, no font binaries ship); PATCHed; re-fetched and re-proved; `docs/CLAIMS.md` C-032; guard re-run against the live body (exit 0). |
| 5 | Items 4 and 5: `docs/BRIEF-ATTESTATION.md` carries `ATTESTATION_INPUT_MISSING` (nothing fabricated, no row upgraded); `docs/DECISIONS.md` P1.8-002; `docs/P2-READINESS.md` written (7 of 8 boxes checked, attestation MISSING). |
| 6 | Final CI run on the P1.8 docs commit, annotations re-proved, this handoff. |

## 2. Item 0 — the actual CI state, from raw output

```
$ gh run view 38162832608 --json status,conclusion,jobs
{"conclusion":"success","status":"completed"}      # run-level
job gate: conclusion success, 25 of 25 steps success, failed steps: (none)

$ gh run view 38162832608 --log-failed
failed to get run log: ... results-receiver.actions.githubusercontent.com ... EOF      # log archive unavailable from here

$ gh api repos/omidoraei/ai_website_wordpress/commits/d6ee888…/check-runs
114539158333 gate success annotations=1
114539149380 gate success annotations=1

$ gh api repos/omidoraei/ai_website_wordpress/check-runs/114539158333/annotations
{"annotation_level":"failure","path":".github","start_line":102,
 "message":"Process completed with exit code 1."}
```

**Classification: F (other).** Not A/B/C/D/E: the asset step, the invariant ratchet, the retraction
guard, the reproducibility step and both P1.7 tools all concluded `success` in that run. The
annotation comes from the **only tolerated step**: `Control-name audit (advisory…)` with
`continue-on-error: true`, which exits 1 by design (228 unexplained settings keys, `docs/CLAIMS.md`
C-004). GitHub records the exit code of a tolerated step as a failure annotation even though the run
stays green.

The mechanism is identified, not guessed - the annotation count tracks the number of tolerated
failing steps across the entire history:

| commit | tolerated steps that exit 1 | annotations per check run |
| --- | ---: | ---: |
| `445c87a` … `aa2739e` (P0.5 - P1.5) | 1 (advisory control-name audit) | **1** |
| `1ca2175`, `918c348`, `3b6185d`, `d5f0abb` (P1.6) | 2 (+ the report-only invariant step) | **2** |
| `d6ee888` (P1.7) | 1 (the invariant step became a passing hard gate) | **1** |
| `baa30d5` (P1.8) | 0 | **0** |

**What P1.7 got wrong:** it reported the run as green from the run conclusion and step conclusions
alone, without checking annotations. The user's reading ("Annotations: 1 error") was correct and the
P1.7 close was incomplete. The acceptance rule is now explicit (C-031, P1.8-001): a phase is
CI-green only with conclusion `success` **AND 0 error annotations AND 0 failed steps**. A local
command is never CI proof, and an old run is never cited for a new commit.

## 3. Item 1 — the repair (workflow only)

```yaml
      - name: "Control-name audit (advisory, findings printed, no error annotation)"
        run: |
          set +e
          python3 skills/elementor-native-kit/scripts/audit_control_names.py > /tmp/audit.txt 2>&1
          code=$?
          set -e
          tail -40 /tmp/audit.txt
          ... job summary: "exit code: $code (1 = findings … not a gate failure)"
          if   [ "$code" -eq 0 ]; then echo "advisory audit: clean (exit 0)"
          elif [ "$code" -eq 1 ]; then echo "advisory audit: findings (exit 1) - advisory by decision, no error annotation raised"
          else echo "::error::advisory audit crashed (exit $code) - a crash is not a findings exit"; exit "$code"
          fi
```

`continue-on-error` is gone from the workflow (`grep -c continue-on-error` = 3, all in comments);
the advisory distinction now lives in the step body, where a **crash** still fails and **findings**
are printed, summarised, and never annotated. Paths touched: `.github/workflows/kit.yml`,
`docs/CLAIMS.md`, `docs/DECISIONS.md` only.

Verification of the repair, before pushing: YAML parsed (`21` steps, zero tolerated steps);
`bash -n` clean on the extracted step; stub run with exit 1 -> step exit 0; stub run with exit 3 ->
step exit 3 and one explicit `::error::`.

## 4. Item 2 — fresh green run (the only acceptance)

| field | value |
| --- | --- |
| new run id | `38163624987` (pull_request) and `38163621438` (push) |
| head sha | `baa30d5f2fe5f5de08c2ed3c5ebc83b7fa38d423` |
| status / conclusion | `completed` / `success` (both runs) |
| annotations | **0** error annotations (`114541518610`, `114541508171`, both `conclusion=success`) |
| failed steps | **none** (25 of 25 steps `success`) |
| artifact | `aurora-ai-kit`, 356 144 bytes, `sha256:a61b033256a929d71386745afcb2a665b121ac10ff866bf07512632617f048bf` |

The dist zips themselves are byte-deterministic and committed, so the CI `sha256sum dist/*.zip`
values equal the local ones; the job log archive was not retrievable from this environment (`EOF`
from `results-receiver`), which is recorded rather than worked around.

## 5. Item 3 — live PR body proof

```
before: sha256 132ddd165a2ce8c15b6f904cb796eb413250cfd725708052bc387ca7ce905d95  (6550 bytes)
        -> the body was ALREADY the P1.7 regeneration; the KB snapshot is stale (same pattern as P1.6 item 0)
after : sha256 d9b5ee59008f8ae8b4322b7ec31faaaa91f3b8e95f9d65ddadc71207e86f9f8d  (6638 bytes, PATCH 2026-10-11T18:25:03Z)
        (live returns one extra trailing newline; content identical after whitespace normalisation)
```

Nine stale patterns - ``all `alt` text present``, `Arad typography`, `4000`, `18 global fonts`,
`6 Theme Builder`, `FAQ schema enabled`, `immutable kit-assets-v1`, `background_background`,
`dual-write` - return **0 hits** on the live body. Required final state, checked item by item on the
live text: 39 templates + 1 Kit document with the METRICS definition named; 7 Theme Builder layouts;
19 colours / 15 typography styles / 3 font families; the alt sentence (24 non-empty
`settings.image.alt`, 13 distinct strings, `docs/a11y-alt-policy.md`); FAQ scoped to the widget-level
schema in the templates plus plugin configuration for site-wide data; **Vazirmatn user-chosen, Arad
not bundled** (no font binaries ship - verified: 0 font files under `templates/` + `dist/`); the tag
described as a movable ref with **commit-SHA URLs** as the target contract; no `4000` block; no
dual-write claim. The retraction guard, which reads the live body, re-ran green after the PATCH.

## 6. Item 4 — attestation: MISSING, not invented

`docs/BRIEF-ATTESTATION.md` now opens with **ATTESTATION_INPUT_MISSING**: the phase prompt and the
session contain no attestation text, so nothing was written into the ten rows, no row was upgraded,
and all ten remain **CLASS-B-PENDING**. Recorded as `docs/DECISIONS.md` P1.8-002
(BLOCKED-ON-HUMAN). The conversion path is unchanged: the human pastes the answers, the file is
committed, the commit hash + file sha256 go into `docs/CLAIMS.md`, and only the rows with text
become CLASS-A.

## 7. Item 5 — P2 readiness

`docs/P2-READINESS.md` carries the eight checks. State: **7 of 8 checked**; the attestation box is
**MISSING**. P2 may open only on an explicit human decision to proceed under CLASS-B-PENDING; the
recommendation on record is not to proceed without the attestation. The gate also records what P2
inherits: the asset repoint as the first commit, the 13-value ratchet as the regression net, the
numbered open defects, and the renderer-drift note (the two PR-body sentences refined here live in
the live body, recorded in `docs/CLAIMS.md` C-032, and must be re-applied if the PR template is
regenerated before it is updated).

## 8. Decisions

| id | decision | why |
| --- | --- | --- |
| P1.8-001 | CI-green = conclusion `success` **AND** 0 error annotations **AND** 0 failed steps; a tolerated advisory step must never raise an annotation | P1.7 cited the run conclusion alone while the check run carried one failure annotation; the annotation counts match the tolerated-step counts exactly across the history |
| P1.8-002 | `ATTESTATION_INPUT_MISSING`; ten rows stay CLASS-B-PENDING; P2 blocked on the human | the phase forbids fabricating or inferring attestation |

## 9. Files touched

`.github/workflows/kit.yml` · `docs/CLAIMS.md` (C-031, C-032) · `docs/DECISIONS.md`
(P1.8-001, P1.8-002) · `docs/BRIEF-ATTESTATION.md` (missing-input banner; ten rows untouched) ·
`docs/P2-READINESS.md` (new) · `HANDOFF-P1.8.md`. Live PR #1 body re-PATCHed.
No tool, no template, no frozen path, no gate-2 question, no P2 work.

## 10. Residue

1. **Attestation still the single blocker** for P2 (`docs/BRIEF-ATTESTATION.md`).
2. **Renderer drift**: the two refined PR-body sentences are recorded in C-032 and must be
   re-applied when `tools/render_docs.py`'s PR template is next regenerated (or the template is
   updated then - `tools/` was outside this phase's allowed paths).
3. **The advisory audit's 228 unexplained keys** remain advisory and are now visible in the job
   summary instead of as an error annotation; the real fix is the HANDOFF-P0 residue.
4. **Job-log retrieval** from this environment fails (`EOF`); CI evidence therefore comes from the
   API (conclusions, annotations, artifacts) and from byte-deterministic committed dist files.

## 11. Final acceptance for this commit's CI (turn 6)

The evidence above was gathered on `baa30d5` (the workflow fix). The phase's own evidence commit is
`13f40c1`, and its run was verified the same way, with the same acceptance rule:

| field | value |
| --- | --- |
| run ids | `38163793528` (pull_request) and `38163789038` (push) |
| head sha | `13f40c16f4a73b5fe62c6dab05de0c79cf285b96` |
| status / conclusion | `completed` / `success` (both) |
| annotations | **0** (`114542012998`, `114542001045`) |
| failed steps | none - 25 of 25 steps success in both runs |
| artifact | `aurora-ai-kit` 356 144 bytes `sha256:44c8b3945cf994a17e0ea725e7574419a438188e1161f9c2eaed3383ae45e21a` |
| deterministic dist payloads (committed, rebuild-stable) | `aurora-ai-kit.zip` `cc56ff3de26b84a580a48944a563fb0aeb9799b0678a813d29c05f2694c88354` · `aurora-ai-templates.zip` `c47837e071612d3efd3a72c74ef1b5cff920d126c30b4428f9dd628609deead1` |

The artifact-archive digest differs between the two runs of the same tree while the committed zip
payloads are byte-stable, which is why the payload digests - not the archive digest - are the ones
quoted as the artifact's identity.
