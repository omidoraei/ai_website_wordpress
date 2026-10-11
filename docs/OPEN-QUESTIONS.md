# Open questions

Each item: what is unknown, who owns the answer, and the phase that must close it.
Items marked **[blocking]** stop the named phase until closed.

## 1. Pro-key policy — **[blocking for P2 verification]**

*Unknown:* whether P2 verifies Pro-only control names on a **real Elementor Pro install**
(C4: the human can install Pro on a staging site) or strips the kit to Free defaults with
documented fallbacks. Also unknown: which Pro version the staging site will run, and whether the
licence seat is available for the whole verification window.

*Owner:* human (staging URL + licence), agent (runs and records the verification).
*Closes in:* P2, first week. Until then every Pro-only control stays **UNVERIFIED** in
`docs/CLAIMS.md` (C-014) and in `skills/elementor-native-kit/references/`.

## 2. `audit_control_names.py` hard-gate conversion — **[blocking for P2 gate health]**

*Unknown:* when the advisory control-name audit (`continue-on-error: true` today, 228 unexplained
keys) becomes a required gate step. The audit cannot gate until either (a) the unexplained keys are
triaged into intentional/harmless, or (b) its floor and matching rules are tightened so the
remaining unknowns are genuinely zero.

*Owner:* agent (triage), human (accepting the new floor at gate 3).
*Closes in:* P2. Related residue is recorded in `HANDOFF-P0.5.md`.

## 3. Reduced-motion baseline — **[blocking for gate 5]**

*Unknown:* what "respects `prefers-reduced-motion`" means when Motion Effects are the only
animation mechanism permitted (constitution) and Elementor Free/Pro expose different motion
controls. Is the baseline: no entry animations at all under reduced motion, or a documented
"switch everything to opacity-only" recipe?

*Owner:* agent (protocol), human (sign-off).
*Closes in:* P2 design, verified at gate 5.

## 4. Dark-mode token set — **[blocking for token freeze]**

*Unknown:* whether the kit ships a dark palette at all. If yes: a second set of globals
(Elementor has no native dark-mode switch) or an opt-in documented recipe, and how it interacts
with the C5 no-tracking/WCAG baseline (contrast must be re-checked in dark).

*Owner:* human (decides), agent (implements).
*Closes in:* P1-R, before tokens are frozen. Default if unanswered: **no dark mode**, recorded as
an assumption in the brief.

## 5. Skipped interview items — **[blocking for gate 1]**

Batch 3 was skipped ("keep going"); the affected brief entries are assumptions A4–A11. The
specific missing inputs:

| missing input | brief row | assumption id | owner | closes in |
| --- | --- | --- | --- | --- |
| B4 split: which datasets are REAL vs SAMPLE vs CUT | §5 | A4 (HIGH) | human | gate 1 |
| C2 references: 3–6 "yes" + 2–3 "never" | §9 | A9 (HIGH) | human | gate 1 |
| C3: logo file; distribution channel; maintainer | §6 | A5, A6 | human | gate 1 |
| C6: definition-of-done confirmation or edit | §10 | A10 | human | gate 1 |
| C7: gate schedule confirmation | §11 | A11 | human | gate 1 |

If any of these are still open at gate 1, the affected artifact does not proceed: DNA stays
RE-DERIVED-from-brief-only, and the labelling policy stays "label everything unevidenced".
