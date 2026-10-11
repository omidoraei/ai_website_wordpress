# HANDOFF — P3 (IA + agent legibility)

## State

Phase complete, **HOLD for human gate 2** (2026-10-16, 16:00 UTC). The kit is untouched:
no file under `templates/`, `tokens/`, `preview/` or `dials.toml` was modified. Two new
read-only auditors and eight documents were added; the change set is documentation + tooling
plus one AGENTS.md pointer.

Commit `a480ad4` on `arena/1e298a1b-ai-website-wordpress`.
CI: push run **38159474444** success, PR run **38159477315** success.

## Deliverables and where the evidence is

| deliverable | path | what proves it |
| --- | --- | --- |
| IA, re-derived | `docs/p3/IA.md` | 17 documents mapped (question · answer units · CTA ladder · exits · fold contract · EN/FA), §6 section verdicts, §5 ranked findings |
| IA inventory (generated) | `docs/p3/ia-map.md` + `.json` | `python3 tools/ia_map.py` — 39 documents, 95 sections, 14 reused anchors, 18 documents with dead CTA targets |
| Agent-legibility spec | `docs/08-agent-legibility.md` | llms.txt drop-in, structured-data plugin map, landmark fixes, alt-text policy, robots + Content-Signal block, WebMCP contract, Agent Readiness procedure |
| Landmark audit (generated) | `docs/p3/landmark-audit.md` + `.json` | `python3 tools/landmark_audit.py` — 39 documents, 962 containers, 95 tagged, 12 with gaps |
| Alt-text sample | `docs/p3/alt-text-sample.md` | 10 drafts (EN/FA) covering all 7 files + logo + decorative case; measured 0/24 widgets have alt today |
| Popup verdict + rationale | `docs/p3/popup-verdict.md` | keep + ship dormant, promise defect, measurement plan, rollback; Journal card anatomy + empty/one/many states |

## Three corrections to the phase brief (evidence first)

1. **`dials.toml` has no breakpoints** (its header: "per-page-type taste calibration"). Real
   breakpoints: `tools/aurora/tokens.py:352` → mobile 767 / tablet 1024, and the Kit document's
   `active_breakpoints = ["viewport_mobile","viewport_tablet"]`, `viewport_md 768`, `viewport_lg 1025`.
   Three modes; the five design widths were stated as three desktop widths inside the base mode.
2. **All dial values are VOID** (`docs/P1-DISPOSITION.md`) — nothing in P3 used them as taste input.
3. **Seven Theme Builder documents, not six**: 2 headers + 2 footers + 3 loop. Tree total: 9 pages +
   22 blocks + 7 theme-builder + 1 popup = 39 templates + 1 Kit = 40.

## Headline findings (all machine-generated, all re-runnable)

1. **The primary CTA is a dead anchor almost everywhere**: `#contact` is used in 16 documents and
   resolves in 1; `#docs` is used in 12 and resolves in 0 (no docs page exists); `#demo` 5/0;
   `#login` 2/0; `#release` 2/0. **18 of 39 documents carry at least one dead in-page target.**
2. **11 page-level documents have no `main` landmark**; 7 have no `h1`; the Single Post template has
   **no post-title widget at all**, so a post renders without its title or an `h1`.
3. **Alt text: 0 of 24** image widgets have any.
4. **8 fabricated metrics** ship unlabelled (BANLIST B03 ×8), consistent with the B4 policy gap.
5. **Responsive reality**: 1 918 per-device declarations; hiding is used exactly 6 times. The mobile
   layout is a reflow (basis, width, spacing, type), which is the "real mobile layout" the brief
   demanded — pixel-level fold verification is a gate-5 item.
6. **Duplication**: `#cta` in 12 documents, `#faq` in 7 (with FAQPage schema enabled in both FAQ
   blocks → duplicate structured data risk), `#testimonials` in 6, `#newsletter` in 5. §6 of IA.md
   merges or rejects 12 duplicate instances without deleting a single block.
7. **Hallmark audit cross-check** (audit verb, anti-pattern list): the 3-column equal feature grid
   and the 93%-everywhere eyebrow are the two named tells present in this structure; both were
   already in the P1/BANLIST worklist, now with per-page locations.

## Skills: what was used, what is blocked

- `information-architecture` (designer-skills, at `.src/sk/grill/information-architecture`) — supplied
  the document method (site map, navigation model, per-page content hierarchy, user flows, naming).
  Adapted for a WP/Elementor kit: sitemap = documents + slugs; flows = CTA ladder + exits.
- `seo-audit` + `schema` + `ai-seo` (coreyhaines31/marketingskills, fetched to `.src/sk/marketingskills`)
  — priority order (crawlability → technical → on-page → content → authority), the JSON-LD detection
  warning (client-side injection makes fetch-based checks lie → use a rendered browser or Rich Results
  Test), and the agent-readiness/llms.txt/WebMCP framing.
- `wcag-accessibility-audit` (thebradking, fetched to `.src/sk/wcag`) — **runtime blocked**: it audits
  a live URL through Chrome's accessibility tree and emits PDF/HTML reports. No deployed site exists
  (same blocker as the Agent Readiness score). Its orientation (evidence from what assistive
  technology actually encounters, per page) is what justified auditing landmarks/headings at the JSON
  level with generated tables instead of by eye.
- `hallmark` (audit verb) — anti-pattern list cross-checked against the structure; no editing done.

Neither external skill repository is committed; they live under `/home/user/.src/`.

## Residue

- **Agent Readiness before/after is blocked** until a URL exists (owner: human deploys staging; then
  agent scores `/`, `/pricing/`, `/journal/{post}/`). No delta is predicted anywhere.
- **WebMCP** is documented as a contract only; platform support is still flag-level.
- `nav` landmarks cannot be verified from JSON (Pro `nav-menu` renders its own tag) — gate-5 item on
  the staging install, together with the whole C-014 Pro-control verification.
- **FA parity** remains a target: 8 FA documents against 39 templates; no FA listing template exists.
- The popup ships dormant with no display condition — that is the intended state, not an oversight.
- `docs/07-faq-troubleshooting.md` needs the popup rollback recipe added in P2 (written here, not yet
  in that file).

## Next 3 actions

1. **Human, gate 2 (2026-10-16):** review `docs/p3/IA.md`, the two generated audits and the section
   verdicts; approve or edit the 10 alt-text drafts.
2. **P2 (after gate 2), in this order:** data labelling (B4) → dead CTA targets → `main`/`h1`/post
   title → alt text → the §6 merge/reject list → then aesthetics.
3. **P4:** deploy the staging site; run the Agent Readiness before/after; measure the real fold at the
   five widths and replace the declared contract; build FA parity per page.

## Turn accounting

17 of the 18 allowed. Batches: recon (1–2) · skills fetch + skill reads (3–5) · mechanical
inspections (6–7, 9–11, 13) · auditor authoring and two bug fixes (8, 10) · IC/IA writing (12–14) ·
gate + commit + CI (15–17).
