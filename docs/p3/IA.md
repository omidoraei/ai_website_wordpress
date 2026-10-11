# IA — information architecture (P3)

Re-derived against `docs/BRIEF.md` (signed 2026-10-12), not inherited from P1. Every number in
this document is produced by `tools/ia_map.py` (`docs/p3/ia-map.md`, `ia-map.json`) or
`tools/landmark_audit.py` (`docs/p3/landmark-audit.md`), both committed and re-runnable.

## 0. Three corrections to the phase brief (evidence first)

1. **`dials.toml` contains no breakpoints.** Its own header says "per-page-type taste calibration".
   Breakpoints live in `tools/aurora/tokens.py:352` — `BREAKPOINTS = {"mobile": 767, "tablet": 1024}`
   — and in the Kit document: `active_breakpoints = ["viewport_mobile", "viewport_tablet"]`,
   `viewport_md = 768`, `viewport_lg = 1025`. The tree therefore has **three Elementor breakpoint
   modes**; the five design widths named in the original brief (1920, 1440, 1024, 430, 360) map onto
   them as three desktop widths inside the base mode. Fold statements below are grouped that way,
   with the wider widths stated separately only where the layout actually differs (container 1240 px
   centred above 1025, 100% below).
2. **Every dial value in that file is VOID** (`docs/P1-DISPOSITION.md`, `P-BRIEF-003`). Nothing in
   this document uses them as taste input.
3. **The tree has seven Theme Builder documents, not six**: 2 headers + 2 footers + 3 loop
   (archive, search-results, single-post). Documents: 9 pages + 22 blocks + 2 headers + 2 footers +
   3 loop + 1 popup = 39 templates, +1 Kit document = 40 (`docs/METRICS.md` §1).

**The responsive mechanism, measured.** Across the 39 documents there are **1 918 per-device
declarations**: `_flex_basis_tablet` and `_flex_basis_mobile` (254 each), `padding_tablet` 222 /
`padding_mobile` 247, `boxed_width_mobile` 147 / `boxed_width_tablet` 93, `flex_gap_mobile` 72 /
`flex_gap_tablet` 36, `typography_font_size_mobile` 49 / `_tablet` 20, and **hiding only 6 times**
(`hide_mobile` 4, `hide_tablet` 2). So the mobile layout is a **reflow** (basis, spacing, type
scale, width), not a reduced page. Pixel-level fold verification needs the rendered build; that is
a gate-5 item, and this document states the *declared* contract, not a guess about pixels.

**Answer-unit classes.** Two kinds of number exist and they never mix:
- **Site answer units** — what the demo brand (Aurora) says. Every number is fictional, so under
  `docs/BRIEF.md` §5 it carries a **SAMPLE label at the section level**. None may be quotable as if
  it were a verified fact.
- **Kit answer units** — true of the artefact (39 templates, 7 Theme Builder layouts, OFL-1.1).
  These belong in the README, the listing and `docs/**`, **never on the demo pages**, because a
  demo page cannot quote the kit without breaking its own fiction.

## 1. Site map and slugs

| # | document | recommended slug | type | FA counterpart |
| ---: | --- | --- | --- | --- |
| 1 | `pages/aurora-home-en.json` | `/` | page | `pages/aurora-home-fa.json` → `/fa/` exists |
| 2 | `pages/aurora-about.json` | `/about/` | page | none (block-level only) |
| 3 | `pages/aurora-services.json` | `/services/` | page | none |
| 4 | `pages/aurora-portfolio.json` | `/work/` | page | none |
| 5 | `pages/aurora-pricing.json` | `/pricing/` | page | none |
| 6 | `pages/aurora-blog.json` | `/journal/` | page | none |
| 7 | `loop/aurora-single-post.json` | `/journal/{post}/` | single (Pro) | none |
| 8 | `pages/aurora-contact.json` | `/contact/` | page | none |
| 9 | `pages/aurora-404.json` | `/404` | page | none |
| 10 | `loop/aurora-archive.json` | `/journal/category/{cat}/` | archive (Pro) | none |
| 11 | `loop/aurora-search-results.json` | `/?s={query}` | search (Pro) | none |
| 12–13 | `headers/aurora-header-{en,fa}.json` | — | header (Pro) | both |
| 14–15 | `footers/aurora-footer-{en,fa}.json` | — | footer (Pro) | both |
| 16 | `popups/aurora-lead-magnet.json` | — | popup (Pro) | none |
| 17 | 22 blocks | — | reusable | 5 have FA twins |

**Parity statement (measured, not asserted):** 8 FA documents exist (1 page, 5 blocks, 1 header,
1 footer) against 39 templates. B2 asked for equal parity; parity is therefore a **P2/P4 build
target per page**, and today it is a block-level start, not a reality.

## 2. Navigation model

- **Primary nav** — one Elementor Pro `nav-menu` widget. Its `menu` setting is **empty** (`""`), so
  the nav renders nothing until a WordPress menu is assigned: an install step, not a design defect.
  The JSON cannot express the item list; recommended 5 items, in task order:
  Services · Work · Pricing · Journal · About.
- **Header actions** — three buttons today: *Read the release* → `#release` (dead, no release page),
  *Sign in* → `#login` (dead), *Book a demo* → `#contact` (dead on 15 of 16 documents that use it).
  Recommendation: **one primary action** (*Book a demo* → `/contact/`) plus at most one utility
  (*Sign in* → the buyer's real app URL, or remove). A 5-item nav + 2 buttons is the ceiling at 1240.
- **Mobile** — hamburger via the Pro nav-menu toggle; verify the toggle's tag/aria on the Pro
  install (`docs/OPEN-QUESTIONS.md` §1).
- **Footer** — 4 columns (brand + social · Product links · Company links · "Talk to us" with email,
  phone, address) plus a legal row. Every contact value is demo data and is labelled as such in the
  kit documentation.
- **Anchor rule (new, enforced by `tools/ia_map.py`)** — a `#target` resolves only in a document
  that carries that `_element_id`. The current tree violates this in 18 of 39 documents (§5).

## 3. The CTA ladder — one ladder, five rungs

| rung | role | label | target today | target it should have |
| --- | --- | --- | --- | --- |
| 1 | primary conversion | Book a demo / Book the call | `#contact` (resolves in 1 doc) | `/contact/` |
| 2 | self-education | Read the docs | `#docs` (**resolves nowhere**) | `/docs/` — or remove until a docs page exists |
| 3 | exploration | Explore the service / Read the case study | `#services`, `#portfolio` (resolve on 4 docs each) | `/services/`, `/work/` |
| 4 | utility | Sign in · Read the release | `#login`, `#release` (**resolve nowhere**) | real app/changelog URLs, or delete |
| 5 | recovery | Back to homepage · Browse all case studies | `/`, `/portfolio/` | correct as-is |

Measured usage vs resolution: `#contact` used in 16 documents / resolves in 1 · `#docs` 12 / 0 ·
`#demo` 5 / 0 · `#services` 4 / 4 · `#portfolio` 4 / 4 · `#login` 2 / 0 · `#release` 2 / 0 ·
`#about` 2 / 0. **18 of 39 documents contain at least one dead in-page target.** This is the single
highest-impact IA defect in the tree: the primary conversion path is a link to nowhere on every page
except `/contact/`.

## 4. Page by page

Legend: **Q** = the one question the page answers · **AU** = answer unit (subject + verb + number),
`SAMPLE` = fictional demo data that must carry a visible label, `REAL` = true of the kit and
therefore documented outside the demo pages · **CTA** = rungs used · **Exits** = where it hands off.

### 4.1 `/` Home (EN) — `pages/aurora-home-en.json`, 13 sections, 137 containers
- **Q:** "What does Aurora do, and can I get a demo?"
- **AU:** (1) "Aurora AI builds agents that ship to production" (positioning, no number — allowed);
  (2) "Aurora Agents 2.0 is generally available" `SAMPLE`; (3) "Production teams run Aurora agents
  in 3 sectors" `SAMPLE`; (4) "Aurora cut onboarding time by X%" `SAMPLE` — currently unlabelled and
  flagged by the BANLIST as a fabricated metric (8 uses tree-wide); (5) "Plans start at $X/month"
  `SAMPLE`.
- **CTA:** primary *Book the call* → must become `/contact/`; secondary *Read the docs* → needs
  `/docs/`; tertiary *Explore the service*, *Read the case study*; utility *Start building* → `#`.
- **Exits:** `/services/`, `/work/`, `/pricing/`, `/journal/`, `/contact/`.
- **Fold:** base mode — hero (padding 104 px) + logo band occupy the first viewport at 1920/1440;
  ≤1024 the hero's split re-bases (`_flex_basis_tablet`) and the padding drops to 72 px, so the hero
  alone fills the fold; ≤767 padding 48 px and mobile type sizes (49 overrides tree-wide) bring the
  hero plus the first band into view. Nothing is hidden on this page.
- **EN/FA:** FA home is a *re-order*, not a mirror — `#results` moves from position 5 to position 4
  (before `#services`/`#how`), i.e. proof before mechanics, which is legitimate and documented in
  `dials.toml` as intent (values VOID, intent retained).

### 4.2 `/about/` — `pages/aurora-about.json`, 7 sections
- **Q:** "Who is behind this and can I trust them?"
- **AU:** story line (no number, allowed); "Founded in 2021" `SAMPLE`; "A team of 24 people across 3
  countries" `SAMPLE`; "Serving X customers" `SAMPLE`; "Aurora operates from Amsterdam" `SAMPLE`.
- **CTA:** primary *Book the call* → `/contact/`; tertiary *Meet the team* → `#team` (dead: the
  anchor does not exist in this document — the team section carries `#team`, but the button sits in
  the hero and links to `#about`, which does not exist).
- **Exits:** `/work/`, `/contact/`, `/journal/`.
- **Fold:** base — hero + story split; ≤1024 the story split re-bases; ≤767 team grid single column.
- **Defect:** no `h1` (all 7 headings are `h2`/`h3`) → see §5.

### 4.3 `/services/` — `pages/aurora-services.json`, 7 sections
- **Q:** "What exactly can I buy, and how does an engagement run?"
- **AU:** "Aurora delivers 4 capability areas" `SAMPLE`; "Engagements run in 3 models (sprint,
  embedded, advisory)" `SAMPLE`; "A typical engagement starts in 2 weeks" `SAMPLE`; "Every
  engagement ships 3 deliverables" `SAMPLE`.
- **CTA:** *Scope this engagement* → `/contact/`; *Explore the service* → `#services` (resolves
  here); *Book the call*.
- **Exits:** `/pricing/`, `/work/`, `/contact/`.
- **Fold:** base — page hero + capability cards (3-up); ≤1024 cards 3→2 columns (cards_columns
  pattern); ≤767 single column; process steps stack.
- **Defect:** no `h1`.

### 4.4 `/work/` — `pages/aurora-portfolio.json`, 5 sections
- **Q:** "Has this been done for someone like me?"
- **AU:** "Aurora shipped 3 case studies in retail, fintech and health" `SAMPLE`; one metric per
  case (3 numbers) `SAMPLE`; "Each case ran for 12 weeks" `SAMPLE`.
- **CTA:** *Read the case study* → `#portfolio` (resolves here, and on the home page only); *Browse
  all case studies* → `/portfolio/` (a legacy slug: the recommended slug is `/work/`); *Book the
  call*.
- **Exits:** `/services/`, `/contact/`.
- **Fold:** base — hero + three full-bleed case bands; ≤1024 media re-bases below the text; ≤767
  bands stack, images full width.
- **Defect:** no `h1`; legacy `/portfolio/` slug must be aligned with `/work/`.

### 4.5 `/pricing/` — `pages/aurora-pricing.json`, 6 sections
- **Q:** "What does it cost, and which plan is mine?"
- **AU:** "Three plans: Starter, Growth, Scale" `SAMPLE`; "Growth costs $X per seat per month"
  `SAMPLE`; "All plans include 14-day trial" `SAMPLE`; "Annual billing saves 20%" `SAMPLE`;
  "The comparison table covers 8 rows" (structural, verifiable from the template itself).
- **CTA:** *Start 14-day trial* → `#` (**empty link**), *Contact sales* → `#`, *Book the call*.
- **Exits:** `/contact/`, `/journal/` (pricing FAQ), `/services/`.
- **Fold:** base — hero + 3-up plan grid + comparison table; ≤1024 plan grid 3→2→ then 1 at ≤767,
  table keeps horizontal fit by re-basing column widths (`boxed_width_mobile` 147 uses tree-wide);
  verify no horizontal scroll on a real device at gate 5.
- **Defect:** no `h1`; two buttons with `#` targets.

### 4.6 `/journal/` — `pages/aurora-blog.json`, 3 sections
- **Q:** "Is there anything here worth reading, and how do I keep up?"
- **AU:** "The journal publishes engineering notes on agent infrastructure" (no number, allowed);
  "The latest 3 posts are featured" `SAMPLE`; "One email a month" `SAMPLE` (the newsletter promise).
- **CTA:** newsletter submit; *Book the call*.
- **Exits:** `/journal/{post}/`, `/?s=`, `/contact/`.
- **Fold:** base — hero + post grid; ≤767 the newsletter form stacks under its copy.
- **Defect:** no `h1`.

### 4.7 Single post — `loop/aurora-single-post.json`, 2 sections
- **Q (reader):** "Is this article trustworthy and complete?"
- **AU:** one per post, authored by the buyer; the template must expose title, date, author, body.
- **CTA:** *Book the call* band after the post.
- **Exits:** next/previous post (`post-navigation`), `/journal/`, `/contact/`.
- **Fold:** base — breadcrumbs, meta, featured image, one 760 px prose measure; ≤767 image full
  width, measure 100%.
- **Defect (severe):** **there is no post-title widget in this template** — the post renders with
  no visible title and no `h1` (verified: `theme-post-title`/`post-title` absent from the file, and
  from the whole tree). Fix in P2.

### 4.8 `/contact/` — `pages/aurora-contact.json`, 4 sections
- **Q:** "How do I book the demo, and what happens next?"
- **AU:** "A 30-minute call, no commitment" `SAMPLE`; "Same-day reply, Mon–Fri" `SAMPLE`; "We store
  your email only to send the checklist/booking" (the template already says this — keep it, it is
  the honesty line B1 needs).
- **CTA:** form submit (6 fields incl. a privacy acceptance); *Book the call* → `#contact` (resolves
  here); *Get started* band (duplicate action — reject, §6).
- **Exits:** `/pricing/`, `/journal/`, mailto/phone in the footer.
- **Fold:** base — hero + split (form | dark details card); ≤1024 the split re-bases; ≤767 form
  first, details after.
- **Defect:** no `h1`; the page's own section duplicates `blocks/contact-section.json` (`#contact`
  in 2 documents).

### 4.9 404 — `pages/aurora-404.json`, 1 section
- **Q:** "The URL is wrong — where do I go?"
- **AU:** none (recovery page; no numbers belong here).
- **CTA:** *Back to homepage* → `/`; *Browse case studies* → `/portfolio/`.
- **Exits:** `/`, `/work/`, `/journal/`.
- **Fold:** single centred band at every width (one `h1`, two actions); mobile type scale only.
- **Note:** the only page whose `h1` and `main`-less structure are both correct except `main`.

### 4.10 Archive — `loop/aurora-archive.json` (Pro)
- **Q (reader):** "What has this team published on this topic?"
- **AU:** per card: title + date + reading time (3 fields currently: title, excerpt, read-more;
  `cards_meta_color` exists but no meta toggle is set).
- **CTA:** card → single post; newsletter; *Book the call*.
- **Fold:** base 3 columns / ≤1024 2 / ≤767 1 (`cards_columns*`), 9 posts per page, numeric
  pagination. Card anatomy and the three states are specified in `docs/p3/popup-verdict.md` §3.
- **Defect:** no `main` landmark.

### 4.11 Search results — `loop/aurora-search-results.json` (Pro)
- **Q:** "Does this site have what I typed?"
- **AU:** result count + per-card metadata; the empty state is the real answer unit ("0 results").
- **CTA:** card → post; search form; *Book the call*.
- **Fold:** base — query field + results grid; ≤767 single column.
- **Defect:** no `main` landmark.

### 4.12–4.15 Header (EN/FA) and Footer (EN/FA) — Theme Builder
- **Header Q:** "Where am I, where can I go, and what is the one action?" · **Footer Q:** "Who is
  this company, how do I reach them, and what are the legal links?"
- **AU (footer entity facts, all `SAMPLE`):** hello@aurora.example · +31 20 123 4567 ·
  Keizersgracht 241, Amsterdam · © 2026 Aurora AI BV. These four lines are also the Organization
  data in Part B and must be replaced by the buyer.
- **CTA:** header — one primary (*Book a demo*) + at most one utility; footer — link columns only.
- **Fold:** header is a single 1240 px row (logo 46 px → 38 px ≤767); footer 4 columns → 2 (≤1024)
  → 1 (≤767) by `_flex_basis_*`; nothing hidden.

### 4.16 Popup — `popups/aurora-lead-magnet.json` (Pro)
- **Q:** "Is there something free that proves competence?"
- **AU:** "The readiness checklist has 18 points" `SAMPLE` — **and the checklist itself does not
  exist in the kit**; the promise must be delivered or rewritten (Part C verdict).
- **CTA:** one email field + submit; privacy line already present.
- **Fold:** single centred card at all widths; entrance motion only.
- **Verdict, measurement plan and rollback:** `docs/p3/popup-verdict.md`.

### 4.17 The 22 blocks — reusable units, none is a page
Blocks are the composition vocabulary, not destinations, so the "one question" test applies at the
block level only as *which question does this block answer when placed*: `hero-split`,
`page-hero`, `fa-hero-split` (identity) · `feature-grid`, `feature-zigzag`, `capability-cards`,
`fa-feature-grid` (capability) · `process-steps` (method) · `stats-band` (proof) · `case-studies`,
`logo-cloud` (credibility) · `testimonials` (trust) · `pricing-table`, `fa-pricing-table`
(decision) · `faq-accordion`, `fa-faq-accordion` (objection) · `cta-band`, `fa-cta-band`
(conversion) · `contact-section` (task) · `newsletter-band` (capture) · `content-two-column`
(explanation) · `team-grid` (people). Blocks that duplicate another block's question are the
rejection candidates in §6.

## 5. Cross-cutting findings (ranked)

| # | finding | evidence | owner |
| ---: | --- | --- | --- |
| 1 | The primary CTA points at a dead anchor on every page except `/contact/` | `#contact` used in 16 docs, resolves in 1; 18/39 docs carry ≥1 dead target | P2 |
| 2 | `#docs` is a dead target in 12 documents and no docs page exists | `docs/p3/ia-map.md` CTA table | P2 (decide: page or delete) |
| 3 | 11 page-level documents have no `main` landmark | `docs/p3/landmark-audit.md` | P2 |
| 4 | 7 documents have no `h1` (about, blog, contact, portfolio, pricing, services, single post) | same | P2 |
| 5 | The Single Post template renders no post title at all | `theme-post-title` absent tree-wide | P2 |
| 6 | Alt text present on every image widget (corrected in P1.6: measured at `settings.image.alt`, not `settings.alt`); the P1.7 quality audit measures 9 flagged instances / 3 distinct strings, all client names, and 0 script/locale mismatches | `docs/a11y-alt-policy.md`, `tools/alt_quality_check.py` | P8 |
| 7 | 8 fabricated metrics appear unlabelled in 4 documents | BANLIST B03 ×8 | P2 (first fix, per B4) |
| 8 | The header nav is unbound (`menu: ""`) — install step, not a defect, but it is unverified | header JSON | P2 (Pro install) |

## 6. Sections judged against the "human task or answer-unit" test

| section | verdict | reason |
| --- | --- | --- |
| Home `#newsletter` | **MERGE** | The capture task belongs to `/journal/`; on the home page it competes with the demo CTA. Keep the block, drop the placement. |
| About `#results` (stats) | **REJECT** | Duplicates the home proof band with the same 8 unlabelled metrics; about's own proof is the team and the story. |
| Home `#process` × Services `#process` | **MERGE** | One process narrative (services); home keeps a 3-step summary at most. |
| Home `#faq`, `/pricing/` `#faq`, `/services/` `#faq`, `/contact/` `#faq` (7 instances) | **REJECT the duplicates** | FAQPage schema is enabled in both FAQ blocks, so identical Q&A on 4+ pages produces duplicate structured data. Keep one canonical FAQ per page *with different questions*. |
| `#testimonials` (6 instances) | **MERGE** | Trust belongs where the decision happens (home, pricing, about); on `/work/` the case studies are the proof. |
| Contact `#cta` "Get started" | **REJECT** | Second conversion goal on a task page that has the form. |
| Header *Read the release* → `#release` | **REJECT** | No release/changelog page exists; a dead utility link costs trust. |
| Header *Sign in* → `#login` | **REJECT unless bound** | For a kit demo, either point it at a real URL or remove it. |
| Popup "18-point checklist" | **REJECT the promise** | No deliverable ships; rewrite the promise or ship the asset (see `docs/p3/popup-verdict.md`). |
| `/work/` testimonials + 3 case studies | **MERGE** | Same answer unit twice. |
| Everything else (heroes, capability cards, process, pricing grid, contact form, 404, archive, search, footer) | **SURVIVE** | Each answers a distinct question and carries a task. |

## 7. What P2/P4 must do with this

1. **P2 first** (before aesthetics, per `docs/P1-DISPOSITION.md`): label the 8 SAMPLE metrics, fix
   the dead CTA targets, add `main` + `h1`, restore the post title, then the alt-text pass.
2. **P2 second**: apply §6 (merge/reject) — it removes 12 duplicate section instances without
   removing a single block.
3. **P4**: measure the real fold at the five widths on the preview build and replace the declared
   contract in §4 with measured values; FA parity per page is a P4 acceptance item.
4. **Gate 2 reads this document together with `docs/p3/ia-map.md`** (the generated inventory) and
   `docs/p3/landmark-audit.md`.
