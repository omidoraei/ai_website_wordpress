# 08 — Agent legibility

**Scope.** The kit stays 100% Elementor-native. Everything in this document is either
**configuration** (robots, plugin settings, hosting toggles) or **content structure** (llms.txt,
alt text, landmarks). Nothing here adds a script to the kit, and nothing here is speculative JS.
Where a deliverable needs a platform feature that does not exist yet, the contract and the enabling
condition are documented instead of shipped.

Companion evidence: `docs/p3/IA.md` (answer units per page) · `docs/p3/landmark-audit.md`
(generated) · `docs/p3/alt-text-sample.md` · `docs/p3/popup-verdict.md` · `docs/BRIEF.md`.

## 0. Posture, decided

| layer | posture | reason |
| --- | --- | --- |
| Search engines | **allow** | a marketing site that cannot be indexed has no job |
| AI retrieval (`ai-input`) | **allow** | the demo's purpose is to be quoted; citation is the KPI of AEO |
| AI training (`ai-train`) | **disallow** | the demo content is the product's shop window, not a free corpus; the EU DSM Art. 4 reservation wording is included in the preamble |
| llms.txt | **publish** | cheap, agent-readable; crawlers ignore it, agents read it |
| Structured data | **via the SEO plugin** | no code in templates; FAQPage already ships |
| WebMCP | **document only** | platform support is experimental; shipping JS would break the "Elementor-native, no unnecessary JS" rule |
| Agent Readiness score | **blocked until a URL exists** | the scanner needs a deployed site (procedure in §7) |
| Tracking | **none shipped** | C5: no-tracking posture; measurement is the buyer's consented choice |

## 1. `llms.txt` — drop-in content

Placement: **site root** (`https://example.com/llms.txt`). On WordPress this is a static file
upload (hosting file manager / SFTP), not a template: the kit documents it, the buyer uploads it.
Write it once per site; keep the structure when copy changes.

```markdown
# Aurora AI

> Aurora AI is a demo brand for an Elementor template kit — a fictional AI infrastructure
> company used to demonstrate the kit. Every metric on this site is sample data. The kit itself
> ships 39 Elementor templates + 1 Kit document (EN + FA/RTL).

## What this site is
- Demo site for the "Aurora AI" Elementor template kit (WordPress + Elementor Pro).
- Pages: Home, About, Services, Work, Pricing, Journal, Contact, 404, plus theme-builder
  header/footer/archive/search/single templates.
- Language: English and Persian (RTL). Persian pages live under /fa/.

## Answer units (each is a quotable sentence; SAMPLE = fictional demo figure)
- Home — "Aurora AI builds agents that ship to production." / "Plans start at $X per month (sample)."
- About — "Aurora AI is a team of 24 people across 3 countries (sample)."
- Services — "Aurora delivers 4 capability areas and 3 engagement models (sample)."
- Work — "Aurora has published 3 case studies in retail, fintech and health (sample)."
- Pricing — "Three plans: Starter, Growth, Scale; 14-day trial; annual billing saves 20% (sample)."
- Journal — "The journal publishes engineering notes on agent infrastructure."
- Contact — "A 30-minute call, no commitment; same-day reply Mon-Fri (sample)."

## Canonical URLs
- /            Home
- /about/      About
- /services/   Services
- /work/       Case studies
- /pricing/    Pricing
- /journal/    Blog index
- /contact/    Contact and demo booking
- /fa/         Persian home

## Entity facts (replace with the real company before launch)
- Name: Aurora AI BV (demo)
- Email: hello@aurora.example
- Phone: +31 20 123 4567
- Address: Keizersgracht 241, Amsterdam
- Language: en, fa

## Kit facts
- 39 Elementor templates + 1 Kit document; 7 Theme Builder layouts; 1 popup.
- Persian set uses Vazirmatn (SIL OFL-1.1), self-hosted via Elementor Custom Fonts.
- Requires WordPress + Elementor Free/Pro; Theme Builder and Forms are Pro features.

## Crawling
- Search: allowed. AI retrieval: allowed. AI training: not permitted (see robots.txt
  Content-Signal and the EU DSM Art. 4 reservation).
```

Two rules for whoever maintains it: every number stays either a **kit fact** or is marked
`(sample)`, and the answer units mirror `docs/p3/IA.md` §4 so the site and its machine-readable map
cannot drift apart.

## 2. Structured data — which plugin, which setting

No JSON-LD is written into the templates. Every type below is produced by the buyer's SEO plugin;
Elementor supplies two of them itself.

| type | where | produced by | prerequisite | Free fallback |
| --- | --- | --- | --- | --- |
| `Organization` + `WebSite` | site-wide | Rank Math / Yoast / AIOSEO → "Site basics" / "Knowledge graph" | logo file (C3 pending: placeholder wordmark), entity facts, same-as profiles | SEO plugin free tier covers both |
| `FAQPage` | Home, Pricing, Services, Contact | **already enabled**: both FAQ blocks set `faq_schema: "yes"` on Elementor Pro's Accordion widget | one FAQ per page with *different* questions (IA §6) | FAQ block + plugin's FAQ schema field |
| `BreadcrumbList` | Single post, Archive, Search | SEO plugin emits it for post types automatically; Elementor Pro's Breadcrumbs widget is already in the single template | permalink structure | plugin free tier |
| `Article` / `BlogPosting` | Single post | SEO plugin | author, date, featured image — and the **post title**, which the template currently lacks (P2 fix) | plugin free tier |
| `Product` / `SoftwareApplication` + `Offer` | Pricing | plugin schema editor, or WooCommerce if the buyer sells there | the price shown on the page must equal the price in markup; both are `SAMPLE` until B4 data arrives | plugin free tier |
| `Review` / `AggregateRating` | — | **do not ship** | the testimonials are fictional; marking them up would be a false claim | — |

**Detection warning (from the SEO-audit skill):** JSON-LD is frequently injected client-side, so
`curl`/fetch-based checks produce false "no schema" findings. Verify with a rendered browser
(`document.querySelectorAll('script[type="application/ld+json"]')`) or Google's Rich Results Test,
and record the result per URL at gate 5.

## 3. Semantic landmarks — audit result and fix list

Full table: `docs/p3/landmark-audit.md` (generated over **39 documents / 962 containers**).
Summary: 95 containers carry an `html_tag` — `section` 90, `header` 2, `footer` 2, `main` 1.

| gap | count | documents | fix (P2) |
| --- | ---: | --- | --- |
| no `main` landmark | 11 | 9 pages + archive + search | set `html_tag: main` on the page's content wrapper (the hero section stays `section`) |
| no `h1` | 7 | About, Journal, Contact, Work, Pricing, Services, Single post | promote the page hero's first heading to `h1`; add the missing post-title widget |
| no post-title widget | 1 | Single post | add Elementor Pro `theme-post-title`, tag `h1` |
| `nav` not visible in JSON | — | headers | Pro `nav-menu` renders its own tag; verify on the staging install |
| `article` in cards | 0 | — | optional: Loop Item container tag `article` if the listing moves to Loop Grid |

## 4. Alt-text policy

Rules (apply to every image the buyer keeps):
1. **Per instance, not per file** — the same photo in two contexts gets two different alts.
2. **Descriptive and specific** — say what the image shows, not what the business sells.
3. **No keyword stuffing, no filename, no "image of"** — never "hero-dashboard.jpg" or "AI, SaaS,
   agents, best".
4. **Decorative stays empty** — `alt=""` (background images set through Elementor Background
   settings render as CSS, so they need no alt at all — which is one more reason for the
   background-only rule).
5. **EN/FA paired** — same meaning in both languages, written for the reader, reviewed by a Persian
   speaker at gate 4; never machine-transliterated.
6. Length: aim ≤ 125 characters.

**Current state: 24 of 24 image widgets have no alt text** (measured; `docs/p3/alt-text-sample.md`).
The first 10 drafts are in that file for approval at gate 2; the remaining instances follow the same
pattern, batched per block.

## 5. Robots + Content Signals

Posture: search **yes**, AI retrieval **yes**, AI training **no** — with the EU rights reservation
wording, because from 2026-09-15 Cloudflare's defaults block mixed-use AI crawlers on ad-carrying
pages for new and free-plan sites, so a policy that is not written down is now a policy chosen by
default (announced 2026-07-01; defaults flipped 2026-09-15).

```txt
# As a condition of accessing this website, you agree to abide by the
# following content signals:

# (a)  If a content-signal = yes, you may collect content for the
#      corresponding use.
# (b)  If a content-signal = no, you may not collect content for the
#      corresponding use.
# (c)  If the website operator does not include a content signal for a
#      corresponding use, the website operator neither grants nor restricts
#      permission via content signal with respect to the corresponding use.

# The content signals and their meanings are:

# search: building a search index and providing search results (e.g., returning
#         hyperlinks and short excerpts from your website's contents). Search
#         does not include providing AI-generated search summaries.
# ai-input: inputting content into one or more AI models (e.g., retrieval
#           augmented generation, grounding, or other real-time taking of
#           content for generative AI search answers).
# ai-train: training or fine-tuning AI models.

# ANY RESTRICTIONS EXPRESSED VIA CONTENT SIGNALS ARE EXPRESS RESERVATIONS OF
# RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION DIRECTIVE 2019/790 ON COPYRIGHT
# AND RELATED RIGHTS IN THE DIGITAL SINGLE MARKET.

User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Notes: the vocabulary is `yes`/`no` only (`y`/`n` belong to the IETF `Content-Usage` rule, a
different draft). `use=reference` is a Cloudflare extension, not part of Content Signals — do not
mix vocabularies in one line. If the buyer runs Cloudflare, the managed robots.txt toggle and the
AI-crawl settings must be set to match this file, otherwise the dashboard default silently overrides
the intent.

## 6. WebMCP readiness (forward-looking, nothing shipped)

Status: the `navigator.modelContext` API is a W3C Web Machine Learning Community Group draft,
exposed in Chrome/Edge behind experimental flags as of 2026-04; no stable release date is committed.
The kit therefore ships **no** registration code.

The markup/copy contract to apply when the platform allows it (one tool per real form, mapped 1:1):

| form | tool name | inputs (from the form's own fields) | side effects |
| --- | --- | --- | --- |
| Contact / demo | `request_demo` | full_name, work_email, company, budget_range, message, consent | creates a lead; must hit the same server-side validation and consent requirement as the human form |
| Popup lead magnet | `get_readiness_checklist` | work_email, consent | sends the checklist (see `docs/p3/popup-verdict.md` — the asset must exist first) |
| Newsletter | `subscribe_newsletter` | email | double opt-in |
| Search | `search_site` | query | read-only |

Enabling condition: stable browser support **and** a maintained JS asset. Until both exist, the
contract above is documentation, and the human-visible forms remain the only capture surface. The
security note is part of the contract: an agent-callable form is a spam surface and must never skip
consent or server-side checks.

## 7. Agent Readiness — score before/after (blocked, with procedure)

The scanner is Cloudflare's Agent Readiness score: public at `isitagentready.com` since 2026-04-17,
integrated into the dashboard's URL Scanner since 2026-05-12, 0–100 across five categories
(Discoverability, Content, Bot Access Control, API/Auth/MCP, Commerce). It measures delivery, not
copy: robots, sitemap, Link headers, markdown negotiation, AI bot rules, Content Signals, Web Bot
Auth, MCP/API discovery, agent skills index, WebMCP.

**Blocker:** it needs a deployed URL, and the kit has none (the preview build is local). Owner:
human (deploy the staging site), then agent (run and record). Closes in P4. Expected deltas are
**not** predicted here; the three URLs (`/`, `/pricing/`, `/journal/{post}/`) are scored before and
after the P4 changes, and the before/after table is the evidence.

## 8. What P2/P4 must do

1. **P2:** landmarks (§3), alt text (§4), FAQ de-duplication (IA §6), post title, and the CTA
   targets from `docs/p3/IA.md` §5.
2. **P4:** upload `llms.txt`, configure the SEO plugin per §2, paste the robots block per §5, deploy
   the staging site, then run the Agent Readiness before/after and attach the table to the gate-5
   evidence.
