# P-BRIEF transcript proof (P1.5 finding, conclusion corrected in P1.6)

**Verdict (corrected 2026-10-12, P1.6): the ten P-BRIEF selections are USER-ATTESTED (class B).**
The human answered B1–B5 and C1–C5 in the Arena chat and confirms it. P1.5's conclusion that the
answers were AGENT-INFERRED was a **false negative**: it looked for evidence in three places that
could not contain the answers, because P-BRIEF itself instructed the human to answer in the chat.
The negative findings below are true and load-bearing; only the conclusion drawn from them was
wrong.

## The three locations searched (kept — they are the root cause)

1. **Gmail thread** `1a12bdee5a2ea836` (subject "P-BRIEF batch 1 — 5 blocking questions (Aurora
   kit)", sent 2026-10-11 09:49:50 −0700). The thread contains **exactly one message**: the
   outbound batch itself. **Zero replies.** The mail says: "Answer in Arena (the chat), not by
   reply — I read answers there." A mailbox-wide search (`P-BRIEF OR aurora OR ASK`, spam and
   trash included) returned no other relevant message.
2. **ask_user transcript** — no artefact on disk. The interview surface exposes the selection to
   the session, not as a durable, citable id.
3. **Session log** — does not exist on disk (searched `/home/user`, 2026-10-11).

**Root cause.** The audit channel was chosen by the agent — the human was told to answer in the
chat — and that channel is not agent-accessible. **Absence of evidence in a location the agent
itself chose as un-auditable is not evidence of absence.**

**Consequence, stated plainly:** no machine-addressable (class A) artifact exists for
chat-channel answers; therefore **class B (human attestation) is the only available evidence
class, and class A requires the bootstrap in `docs/BRIEF-ATTESTATION.md`** — the human pastes the
answers there, the agent commits the file, and the commit hash is recorded in `docs/CLAIMS.md`.

## The ten rows

| id | recorded selection (option id) | evidence class | note |
| --- | --- | --- | --- |
| B1 | "A Template Kit to sell / distribute" (`sell_kit`), 2026-10-12 | **B — USER-ATTESTED** | answered in the chat; class A pending the paste |
| B2 | "Genuinely bilingual, equal parity" (`equal_parity`), 2026-10-12 | **B — USER-ATTESTED** | same |
| B3 | "Book a demo" (`book_demo`), 2026-10-12 | **B — USER-ATTESTED** | same |
| B4 | "Mixed — I will list what is real" (`mixed`), 2026-10-12 | **B — USER-ATTESTED** (partial: the list never arrived) | same |
| B5 | "Switch the FA type system to Vazirmatn now" (`switch_vazirmatn`), 2026-10-12 | **B — USER-ATTESTED** | supersedes the original instruction's Arad mention |
| C1 | "Keep all nine + popup" (`full_nine`), 2026-10-12 | **B — USER-ATTESTED** | same |
| C2 | "I'll paste 3–6 references + 2–3 anti-references" (`will_paste`), 2026-10-12 | **B — USER-ATTESTED** (partial: the links never arrived) | same |
| C3 | "I have a logo, no photography" (`logo_only`), 2026-10-12 | **B — USER-ATTESTED** (partial: the file never arrived) | same |
| C4 | "I can install Elementor Pro on a staging site" (`pro_available`), 2026-10-12 | **B — USER-ATTESTED** | same |
| C5 | "Assume EU buyers → WCAG 2.2 AA baseline + no-tracking posture documented" (`eu_strict`), 2026-10-12 | **B — USER-ATTESTED** | same |

The batch-3 skip ("keep going") is also user-attested (class B).

## Where the user's answers expand or supersede the original instruction

Five places, for gate 2. **Owner in every row: HUMAN** — these are user decisions, not agent
inventions. Each EXPANDS the original instruction's scope; the fourth SUPERSEDES a specific
instruction:

1. **Template Kit as a delivery format → a commercial product for third parties (B1, user-chosen).**
   The original instruction said the site should be *designed as if* it would be delivered as a
   Template Kit; the human made the kit itself the sellable artifact. That flips the data rules:
   sample data becomes a labelling duty toward buyers rather than the owner's own marketing claim.
2. **RTL as a feature → equal parity as a contract (B2, user-chosen).** Every EN decision becomes
   a two-language decision (ordering may differ per language) and parity becomes a measurable
   target: today 8 FA documents run against 39 templates + 1 Kit document.
3. **A conversion goal added: "Book a demo" (B3, user-chosen).** The original instruction named no
   CTA; the human set the primary action and the KPI (qualified demo requests). It now drives the
   CTA ladder, the contact form's six fields and the popup verdict.
4. **Arad → Vazirmatn (B5, user-chosen, SUPERSEDING).** The original instruction mentioned Arad;
   the human chose Vazirmatn on licence grounds (Arad's licence was never produced; Vazirmatn is
   SIL OFL-1.1). **USER-CHOSEN, SUPERSEDING the original instruction's Arad mention. Do NOT
   reintroduce Arad in P2 to honour the earlier wording.**
5. **An "Examples:" list → a mandatory nine pages (C1, user-chosen).** The original instruction
   listed pages as examples; the human made all nine plus the popup fixed scope. That is why the
   route renames in the P3 IA (for example `/work/`) are presented as corrections the human may
   reject, not as tidying.

## What this changes downstream

- `docs/BRIEF.md` rows now read **USER-ATTESTED (class B)**; the header and the evidence rule were
  amended in P1.6 (classes A/B/C, `AGENTS.md`).
- `docs/DECISIONS.md` **P1.6-001** records the repair and **P-BRIEF-010** carries the
  anti-regression wording; `docs/p1/type-decision.md` carries the P2 carry-forward rule.
- Class A arrives only via `docs/BRIEF-ATTESTATION.md` (currently empty — the highest-priority
  input to gate 2).
