# AGENTS.md — Aurora AI Elementor template kit

Project skill: **`skills/elementor-native-kit/SKILL.md`** (read it before touching
`templates/` or `tools/aurora/`). Deep Elementor knowledge lives in that skill's
`references/` — load only the file you need.

## Stack (fixed — not a preference)

WordPress + Elementor Free/Pro only. The deliverable is Elementor template JSON that a
non-coder can edit in the Elementor panel.

## Commands

```bash
python3 tools/build.py                # regenerate templates/, dist/, templates/INDEX.md
python3 tools/build.py --check        # validate only, write nothing
python3 tools/verify.py               # THE GATE — must exit 0 before any commit
python3 tools/verify.py --report      # regenerate docs/_generated/facts.md, then verify
python3 tools/bidi_check.py           # bidi / Unicode safety (Persian strings)
python3 tools/media.py                # media/_raw/*.png -> media/*.jpg (1500x1000, q90)
python3 tools/preview.py [--serve]    # static review render -> preview/*.html
python3 skills/elementor-native-kit/scripts/audit_control_names.py   # control-name evidence
python3 skills/elementor-native-kit/scripts/extract_controls.py --source <checkout> --tag <tag>
```

There is no test framework: `tools/verify.py` *is* the test suite. It re-reads the generated
JSON and checks structure, global-reference resolution, value shapes, media existence and
(forbidden) HTML widgets. Exit code is the contract.

## Forbidden output (hard rules)

1. No static HTML website, no React/Next/Vue, no custom front-end app.
2. No `html` widget, no custom CSS, no custom JS, no external animation library.
3. No legacy `section`/`column` elements — Flexbox Containers only.
4. No hard-coded copy: all text in Heading / Text Editor widgets.
5. No guessed control names — a control id must exist in
   `skills/elementor-native-kit/references/_generated/control-index.md`.
6. No Pro-only control written into a Free-compatible document without a documented
   fallback and a `docs/capability-matrix.md` row.
7. No numbers hand-written into README/docs/CHANGELOG — they come from
   `tools/verify.py --report`.

## Code style

* Python 3.8+, stdlib only (the sandbox has no package network for the build).
* `tools/aurora/` is the only place templates are authored; never hand-edit
  `templates/*.json` — the build overwrites them.
* Tokens live in `tools/aurora/tokens.py`; nothing else may contain a raw hex, font name or
  spacing value.
* Prefer adding a component/helper over repeating a settings dict.
* Comments explain *why* (a rule, a source line, a failure mode) — never what the line does.
* Table-driven markdown over prose in `docs/` and `references/`.

## Gates (human review happens ONLY here, batched, at 80–85% completeness)

| Gate | Ship | Human decides |
| --- | --- | --- |
| G1 — DNA & design direction | palette, type scale, IA | visual identity |
| G2 — Design system & tokens | kit document, globals | brand fit |
| G3 — Page templates | 9 pages | content & layout |
| G4 — Theme Builder + FA/RTL | header/footer/single/archive/popup, FA set | RTL correctness |
| G5 — Release | zips, docs, changelog | go/no-go |

Between gates: proceed autonomously, log decisions in `HANDOFF-<phase>.md`, do not ask for
micro-decisions.

## Model routing & cost cap

| Work | Model tier |
| --- | --- |
| DNA, design direction, IA, tokens, arbitration, RTL decisions | frontier / high effort |
| Batch audits, count reconciliation, link checks, alt-text drafts | cheap subagent |

Each phase prompt states a turn cap. If the cap is reached, **stop and write the residue into
`HANDOFF-<phase>.md`** — do not silently continue or silently drop work.

## Handoff discipline

End every phase with `HANDOFF-<phase>.md`: state, open questions, next 3 actions, files
touched, decisions reversed. A decision reversed by evidence must be recorded as a
correction, with the command that reversed it (see `references/04-version-deltas.md` for the
pattern).

## Evidence rule

Never write "done", "verified", "responsive" or "accessible" without a command, an exit code
and a count. A claim without an artifact is not done. Numbers come from
`python3 tools/verify.py --report`.
