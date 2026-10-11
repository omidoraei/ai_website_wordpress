# HANDOFF — P-BRIEF (lock the purpose)

## State

The purpose is now signed: **10 of the 15 mandated questions were answered by the human on
2026-10-12**, and the five questions of batch 3 were **skipped** ("keep going"), so they are
recorded as ASSUMPTION rows with a risk rating and a reversal trigger rather than silent defaults.

The phase is **stopped** on purpose. No P2 work has begun; nothing under `templates/`, `tokens/`,
`preview/`, `tools/`, `dials.toml`, `dna.yaml`, `BANLIST.md` or `type-decision.md` was touched.
The deliverable whitelist was respected: the only repository changes are the six documents listed
below (`git show --stat bd46eae`).

Commit `bd46eae` on `arena/1e298a1b-ai-website-wordpress`. CI: push run **38158655668**
success (22/22 steps), PR run **38158658329** success. The single failure-level annotation on the
gate is the known advisory control-name audit (`continue-on-error: true`), unchanged from P0.5.
The **Retraction guard passed** with the new documents in scope.

## Deliverables (all six, whitelist only)

| file | what it holds |
| --- | --- |
| `docs/BRIEF.md` | purpose, audience, primary CTA, KPI, language/RTL weight, page+block scope, data policy, brand/type decision, compliance posture, definition of done, budget, maintainer, gate schedule; every line ANSWERED (quoted) or ASSUMPTION (risk + reversal trigger) |
| `docs/DECISIONS.md` | append-only ledger: 12 retroactive P0/P0.5/P1 rows + 21 P-BRIEF rows = 33 |
| `docs/P1-DISPOSITION.md` | 16 artifacts: VOID 4 (incl. the 15 dial values and the palette) · RE-DERIVE 1 · CONDITIONAL 3 · SURVIVES 8; carry-forward rule stated |
| `docs/OPEN-QUESTIONS.md` | Pro-key policy, control-audit hard-gate conversion, reduced-motion baseline, dark-mode token set, plus the five skipped interview items — each with owner and closing phase |
| `docs/CLAIMS.md` | extended with C-011…C-016 (reference approval UNAPPROVED; palette VOID as build description; Pro names still UNVERIFIED) |
| `docs/METRICS.md` | §5 phase-scoped counters with counting commands; explicitly outside the injected fact set |

## Literal Q&A transcript (verbatim selections)

Batch 1 (blocking) — human selected:

- **B1** `sell_kit` — "A Template Kit to sell / distribute"
- **B2** `equal_parity` — "Genuinely bilingual, equal parity"
- **B3** `book_demo` — "Book a demo"
- **B4** `mixed` — "Mixed — I will list what is real" (the list never arrived)
- **B5** `switch_vazirmatn` — "Switch the FA type system to Vazirmatn now"

Batch 2:

- **C1** `full_nine` — "Keep all nine + popup"
- **C2** `will_paste` — "I'll paste 3–6 references + 2–3 anti-references" (the links never arrived)
- **C3** `logo_only` — "I have a logo, no photography" (the file never arrived)
- **C4** `pro_available` — "I can install Elementor Pro on a staging site"
- **C5** `eu_strict` — "Assume EU buyers → WCAG 2.2 AA baseline + no-tracking posture documented"

Batch 3 — **skipped**: the interview UI returned `answers: []`, `skipped: true`; the human's message
was "keep going". The five questions (B4 list, C2 references, C3 logo/channel/maintainer, C6
definition of done, C7 gate confirmation) became assumptions A4, A5+A6, A9, A10, A11.

No artifact is described as approved anywhere: the only approvals in this phase are the ten
selections quoted above.

## Assumptions re-surfaced at gate 1

A1 Aurora = demo brand (MED) · A2 visitor = technical evaluator (LOW) · A3 audience baseline (MED) ·
A4 every unevidenced dataset carries a SAMPLE label (HIGH) · A5 editable demo wordmark until the
logo arrives (LOW) · A6 store distribution, buyer maintains (MED) · A7 no crawler policy baked in
(LOW) · A8 no deadline/cash budget recorded (MED) · A9 DNA re-derived from the brief only (HIGH) ·
A10 definition of done = five proposed criteria (MED) · A11 five gates as booked (LOW).
Full table: `docs/BRIEF.md` §12.

## Evidence at close

- **Six files** — paths above; commit `bd46eae`.
- **Verifier** — `python3 tools/build.py --check` → validation OK, `templates/` 40 json;
  `python3 tools/verify.py --report` → exit 0, "36 claims checked";
  `python3 tools/render_docs.py --check` → 36 slots across 11 files agree;
  `python3 tools/bidi_check.py` → exit 0, 0 findings.
- **Notion decision count** — page "Aurora AI — Decision Ledger (P-BRIEF)" created
  (`app.notion.com/p/Aurora-AI-Decision-Ledger-P-BRIEF-3f68dd8c323d81198787fe3ad7064d66`) with
  **5 decision rows** (P-BRIEF-000…005). Subsequent appends failed three times at the connector
  level ("Something went wrong. Please try again." and one tool-availability error), so rows
  006–020 exist only in `docs/DECISIONS.md`, which is the authoritative copy. This is an honest
  deviation from "log every decision row as it is made" — recorded here, not hidden.
- **Calendar** — five gate events created on the human's primary calendar (16:00–16:45 UTC):
  gate 1 `asijgn5u9tp5kt9g4am2u90388` (10-14) · gate 2 `30t2ijlajhvinad50t4qa6u0vs` (10-16) ·
  gate 3 `h467fetc0dk14b8jhl9692f2o4` (10-19) · gate 4 `cmsots7ajq5h4qlmrah5gnu1bg` (10-21) ·
  gate 5 `btfn82a79noe57ikgus99ge8ao` (10-23).
- **Gmail** — exactly one message, batch-1 questions only: id `1a12bdee5a2ea836`.
- **Turn counter at stop** — 5 action batches of the 12 allowed: (1) connectors + gates + email +
  batch 1; (2) batch 2 + Notion retry; (3) evidence sweep + four documents; (4) ledger extensions +
  commit `bd46eae` + CI verification; (5) this handoff.
- **What I did NOT ask, judged non-blocking** — hosting/domain, SEO and analytics providers,
  newsletter tooling, WooCommerce/checkout, support SLA and marketplace pricing, and Persian copy
  tone: none of them change the brief's decisions (product type, language weight, CTA, data policy,
  type licence, scope), and all can be re-surfaced at gates 2–3 if they become load-bearing.

## Next 3 actions

1. **Human, at gate 1 (2026-10-14 16:00 UTC):** answer the five skipped items, or explicitly
   confirm assumptions A4/A5/A6/A9/A10/A11. The brief cannot leave "partially signed" without this.
2. **P1-R:** re-derive DNA, the 15 dial values, the palette (with an accent budget) and the FA type
   ladder per `docs/P1-DISPOSITION.md`. No P2 specification may cite a VOID row.
3. **P2, in this order:** data labelling (B4 policy) → structure/rhythm → aesthetics; schedule the
   Pro-control verification the moment the staging URL and licence arrive (closes C-014).

## Residue

- Notion append failures (above) — retried once more before stopping; if still failing, the ledger
  lives in `docs/DECISIONS.md` and the Notion page must be reconciled later.
- Batch-3 skip → 11 assumptions; gate 1 is the only place they can be closed.
- `banlist_check.py` cosmetic `>80%%` print bug (carried from P0.5).
- Pro control names remain UNVERIFIED until the staging install exists (C-014).
- The palette finding (coral 15 vs amber-600 294 of 2 136 refs) has no enforcement yet; P1-R owns
  the re-derivation and P2 owns the detector.
