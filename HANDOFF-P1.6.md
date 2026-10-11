# HANDOFF — P1.6 (attribution repair + guard proof)

## State

Complete. Gate 2 remains **HOLD**; no P2 work, no gate-2 answers, nothing on the forbidden list
touched (`templates/`, `tokens/`, `dials.toml`, `dna.yaml`, `BANLIST.md`, `preview/`, `media/`,
`dist/` all unmodified; the SAMPLE policy, parity shape, footer entity, image licences and `#demo`
fix are untouched).

## Turn ledger (item 6 — continuous, no holes)

| turn | batch | outcome |
| ---: | --- | --- |
| 1 | item 0 live-surface proof | live PR body grep = 0 hits; sha256 recorded |
| 2 | locating rule surfaces | constitution/rule locations mapped |
| 3 | reading AGENTS.md + OPEN-QUESTIONS.md + tag probe | tag target SHA read; rulesets listed (none) |
| 4 | attribution + evidence classes + disposition rows | BRIEF/DECISIONS/P1-DISPOSITION repaired (one script aborted mid-way on a bad assertion — the remaining files were applied in turn 5, not separately) |
| 5 | remaining repairs + lang-mix detector | type-decision/AGENTS/CLAIMS edited; `lang_mix_check.py` written |
| 6 | alt-path measurement + detector first run | **24/24 alt present at `settings.image.alt`** — the P1.5 retraction was wrong |
| 7 | alt-truth correction + PR re-patch + guard | PR body patched; guard 0 hits |
| 8 | invariants wired + tag pin + commit | 8 assertions; 5 fail (report-only) |
| 9 | invariant walk fix + fresh-clone guard proof + CI | clone guard 0 hits; CI run 38161492842 success |
| 10 | claim qualifier + handoff + push | this file |

No turn was unlabelled; the only merge is noted in turn 4.

## Item 0 — the live surface was already fixed

```
$ gh api repos/omidoraei/ai_website_wordpress/pulls/1 --jq .body | grep -n -e 'all `alt` text present' \
    -e 'Arad typography' -e '4000' -e '18 global fonts' -e '6 Theme Builder'
(no output; grep exit 1)
$ gh api repos/omidoraei/ai_website_wordpress/pulls/1 --jq .body | sha256sum
521de4492c8d34d60c3fe9d2bccf9796d9a5fd6a62222818b8a08e1eca804df4
```
Live title: `Aurora AI — Elementor-native template kit (39 templates + 1 Kit document, EN + FA/RTL)`.
Live body equals the locally regenerated body after whitespace normalisation (6196 vs 6195 chars =
trailing newline only), i.e. **the P1.5 PATCH did land**; the snapshot in the phase prompt predates
it. **After** the P1.6 re-patch the live body hash is `4b53f5f0…`-class (see the PR; the guard reads
it live). No further re-patch was needed for the defects — one was needed for the alt correction
(below).

## Item 1 — attribution repaired

- `docs/BRIEF.md`: ten rows now read **USER-ATTESTED (class B)** (header restored, evidence rule
  replaced with classes A/B/C). Rows and content unchanged.
- `docs/PBRIEF-TRANSCRIPT.md`: **conclusion rewritten**, three negative findings kept verbatim
  (Gmail `1a12bdee5a2ea836`: 1 outbound, 0 replies; ask_user: no artefact; session log: none on
  disk) plus the root cause: *the audit channel was chosen by the agent and is not agent-accessible;
  absence of evidence in a location the agent itself chose as un-auditable is not evidence of
  absence.* Stated plainly: no machine-addressable artefact exists for chat-channel answers, so
  class B is the only available class and class A requires the bootstrap.
- **B5 anti-regression sentence** in three places (`docs/BRIEF.md` §6, `docs/DECISIONS.md`
  P-BRIEF-010, `docs/p1/type-decision.md` "P2 carry-forward rule"): *"USER-CHOSEN, SUPERSEDING the
  original instruction's Arad mention. Do NOT reintroduce Arad in P2 to honour the earlier
  wording."*
- The other four expansions are re-owned as **HUMAN** decisions in the transcript document, each
  still marked as expanding the original instruction's scope.

## Item 2 — evidence classes

`AGENTS.md` now carries the three-class rule (A machine-addressable · B human-attested ·
C agent-inferred, with the risk+reversal obligation) and the absence-of-evidence clause; the turn
ledger rule is in its own section. `docs/CLAIMS.md` C-011 re-graded to class C, C-012 to
"VERIFIED (class B)".

## Item 3 — the bootstrap

`docs/BRIEF-ATTESTATION.md`: skeleton only — header, the ten rows with their recorded options, an
empty "human attestation (paste here):" block each, and the rule that a paste committed by the
agent (hash recorded in CLAIMS) is what converts a row to class A. **Nothing fabricated; flagged as
the highest-priority gate-2 input.**

## Item 4 — guard safety, and the finding it surfaced

Restoring the wording did **not** trip the guard — but the check exposed a worse problem: the
P1.5 alt retraction was itself false.

| claim | P1.5 said | measured (P1.6) |
| --- | --- | --- |
| alt text | "24 of 24 have none" (read `settings.alt`) | **24/24 carry `settings.image.alt`**, 13 distinct strings; the preview render exposes them (`alt="Aurora AI studio in Amsterdam"`, Persian alts in the FA set) |
| PR body | "none of which carries alt text yet" | corrected |

Actions: `all \`alt\` text present` **removed** from the retracted block (it is true);
`none of which carries alt text` **added** (the false P1.5 sentence); CLAIMS **C-017 corrected**,
**C-027 added**; PR body regenerated + re-patched; the same false claim fixed in
`docs/p3/alt-text-sample.md`, `docs/08-agent-legibility.md` §4 and `docs/p3/IA.md` finding 6.

**Fresh-clone guard proof (after the repair):**
```
retraction guard: 27 file(s), 19 phrase(s), 2 commit line(s), pr=scanned, run=scanned
exit=0
```

## Item 5 — the four holes

**5a. Invariants (8, wired as a CI step, report-only until P2).** First result, printed:

```
alt_text == image_widgets        PASS  24/24
main == page_level_docs          FAIL  1/9
h1_per_doc == 1                  FAIL  6 bad (about, blog, contact, portfolio, pricing, services)
post_title_widget_present        FAIL  False
theme_builder_docs == 7          PASS  7
colours/type/families == 19/15/3 PASS  19/15/3
dead_anchor_count == 0           FAIL  48 dead
no unqualified widget-type claim FAIL  1 surface (docs/03; qualified in the same turn)
invariants: 5 of 8 fail
```
The step flips to fatal when the P2 fixes land (same pattern as BANLIST). Justification: P7 rewrites
the 22 blocks and every count will move; only these invariants survive that rewrite.

**5b. Immutability.** Measured: `kit-assets-v1 → 96149fa9233a4ba14f1c1aa539f406f3023843cd`; all 24
image widgets depend on that movable tag. Attempted protection: `POST /repos/…/rulesets` →
**403 "Resource not accessible by integration"** (the token has no ruleset/admin scope). Decision
recorded (DECISIONS **P1.6-003**): the tag is **pinned by SHA in CI** — a new step fails the build
if `refs/tags/kit-assets-v1` no longer points at the recorded commit. A ruleset or a full-SHA
repoint remains a P2 item.

**5c. Language mixing.** `tools/lang_mix_check.py`: floor 30 documents, `--strict` at P8, first run
`40 document(s) scanned, 3 non-FA document(s) embed Arabic-script copy` — `capability-cards.json`,
`aurora-home-en.json`, `aurora-services.json`, 106 chars in 9 strings each (the earlier "21" counted
character runs, not strings; both numbers are in the handoff record). Strings untouched, per scope.

**5d. Disposition rows.** `docs/P1-DISPOSITION.md` gains two **CONDITIONAL-BY-S8** rows for
`docs/08-agent-legibility.md` and `docs/p3/alt-text-sample.md`: structure sound, **entity data**
(demo company name, address, phone, email) must be neutralised before either file touches a live
site — nothing in them may be copied live until then.

## Commits and CI

`1ca2175` (attribution + alt truth + invariants) · `918c348` (invariant walk widened) · plus the
claim qualifier and this handoff. CI run **38161492842** success: reproducibility, verify, render,
**Retraction guard**, **Invariant assertions** (continue-on-error), tag-pin step.

## Residue

- **Gate 2** owns: the human's paste into `docs/BRIEF-ATTESTATION.md` (class A), the alt-quality
  decision (client-name-only alts), the 63 mixed-language strings (P8), the tag-protection choice,
  and every item the FORBIDDEN list reserved.
- The invariant step is report-only; 5 of 8 currently fail by design.
- `docs/03-template-library.md` claim qualified; the control-name audit stays advisory (C-004).
