# P-BRIEF transcript proof (P1.5, item 1)

**Verdict: none of the ten P-BRIEF answers can be attributed to a user message id. Every one is
recorded as `AGENT-INFERRED (unconfirmed)`.** The rows are kept; the questions are not re-asked in
this phase; confirmation, correction or voiding is a gate-2 decision.

## Sources checked, in order

1. **Gmail thread** `1a12bdee5a2ea836` (message-id header
   `<CALQKb_YaUk9GqX9wDPOj5MiHc0dpxOd8h3sVejjJ_OGYwr=yFw@mail.gmail.com>`, sent 2026-10-11
   09:49:50 −0700, subject "P-BRIEF batch 1 — 5 blocking questions (Aurora kit)"). The thread
   contains **exactly one message**: the outbound batch itself. **Zero replies.** The outbound text
   states the answers were to be given in the chat, not by reply ("Answer in Arena (the chat), not
   by reply — I read answers there"). A mailbox-wide search (`P-BRIEF OR aurora OR ASK`, spam and
   trash included) returned no other relevant message.
2. **ask_user transcript** — not available as a citable artefact. The selections were rendered by
   the interview UI during P-BRIEF (2026-10-12) and were carried into `docs/BRIEF.md` /
   `docs/DECISIONS.md` from in-session tool results; no user message id accompanies them anywhere
   this repository or the mailbox can show.
3. **Session log** — does not exist on disk. A filesystem search of `/home/user` for session,
   transcript or `.jsonl` artefacts found none (2026-10-11).

Because a quote that cannot be attributed to a user message id is not a quote, all ten rows below
carry the string **AGENT-INFERRED**. The recorded option label and date are retained for the
gate-2 review: the human can confirm them as accurate, correct them, or void them.

## The ten rows

| id | recorded selection (option id) | attributed to a user message id? | status |
| --- | --- | --- | --- |
| B1 | "A Template Kit to sell / distribute" (`sell_kit`), 2026-10-12 | **no** | AGENT-INFERRED |
| B2 | "Genuinely bilingual, equal parity" (`equal_parity`), 2026-10-12 | **no** | AGENT-INFERRED |
| B3 | "Book a demo" (`book_demo`), 2026-10-12 | **no** | AGENT-INFERRED |
| B4 | "Mixed — I will list what is real" (`mixed`), 2026-10-12 | **no** | AGENT-INFERRED |
| B5 | "Switch the FA type system to Vazirmatn now" (`switch_vazirmatn`), 2026-10-12 | **no** | AGENT-INFERRED |
| C1 | "Keep all nine + popup" (`full_nine`), 2026-10-12 | **no** | AGENT-INFERRED |
| C2 | "I'll paste 3–6 references + 2–3 anti-references" (`will_paste`), 2026-10-12 | **no** | AGENT-INFERRED |
| C3 | "I have a logo, no photography" (`logo_only`), 2026-10-12 | **no** | AGENT-INFERRED |
| C4 | "I can install Elementor Pro on a staging site" (`pro_available`), 2026-10-12 | **no** | AGENT-INFERRED |
| C5 | "Assume EU buyers → WCAG 2.2 AA baseline + no-tracking posture documented" (`eu_strict`), 2026-10-12 | **no** | AGENT-INFERRED |

The batch-3 skip ("keep going") is in the same state: recorded, not attributable.

## Where the inferred answers expand or reverse the original instruction

Five places, for gate 2 — this paragraph is the input to the gate, not a licence to proceed:

1. **Template Kit as a delivery format → a commercial product for third parties.** The original
   instruction said the site should be *designed as if* it would be delivered as a Template Kit;
   B1-as-inferred makes the kit itself the sellable artifact. That flips the data rules: sample
   data becomes a labelling duty toward buyers rather than the owner's own marketing claim, and
   support/upgrade expectations shift to the buyer.
2. **RTL as a feature → equal parity as a contract.** The original brief asked for a working RTL
   variant; B2-as-inferred makes FA first-class, which turns every EN decision into a two-language
   decision (ordering may differ per language), and makes parity a measurable target rather than
   an aspiration. Today the tree holds 8 FA documents against 39 templates + 1 Kit document — the
   gap is the work.
3. **A conversion goal invented wholesale.** "Book a demo" and its KPI (qualified demo requests)
   appear in no prior instruction. It arrived as the recommended default in the interview and was
   never restated by the human. It now drives the CTA ladder, the contact form's six fields and
   the popup verdict.
4. **Arad → Vazirmatn.** The original brief named Arad typography for the FA set. B5-as-inferred
   reverses that on licence grounds (Arad's licence was never produced; Vazirmatn is OFL-1.1).
   Until the P2 swap, the template bytes still carry Arad and the kit's own PR text must say so.
5. **An "Examples:" list → a mandatory nine pages.** The original instruction listed pages as
   examples; C1-as-inferred turned all nine plus the popup into fixed scope. That is why the
   route renames in the P3 IA (for example `/work/` replacing the legacy portfolio path) are
   presented as corrections to scope the human may reject, not as tidying.

## What this changes downstream

- `docs/BRIEF.md` is re-labelled in place (rows kept): every former **ANSWERED** line now reads
  **AGENT-INFERRED (unconfirmed)**.
- `docs/DECISIONS.md` records the re-labelling, and the GATE-1 closure row treats the five gate-1
  questions as neutralised by *these inferred* answers — with the inference itself listed as the
  one thing gate 2 must confirm.
- No P2 work inherits a stronger status than this document: everything built on B1–B5/C1–C5 is
  built on an inference, and the gate-2 pack says so.
