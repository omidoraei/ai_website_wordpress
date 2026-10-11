# BANLIST.md

Deterministic prohibitions for the Aurora AI kit. Base: `Leonxlnx/taste-skill` v2
(skills/taste-skill/SKILL.md §9 "AI Tells") plus `Nutlope/hallmark`
(references/anti-patterns.md), extended with project-specific bans derived from the two
anti-references in `docs/p1/dna.yaml`.

**Rule E: taste is numeric.** Every ban carries a rule id, and
`tools/banlist_check.py` implements each id as a deterministic detector over the generated
JSON. Current counts are real output of that script on this commit — re-run it; do not trust
the numbers you read here.

```bash
python3 tools/banlist_check.py            # human report
python3 tools/banlist_check.py --json     # machine output for CI
```

Phase status: **P1 is diagnosis only.** Nine rules trip on the current kit on purpose; they
are assigned to a fix phase in `docs/p1/delta-table.md`. CI runs the checker in
`--report-only` until P2 closes them, then the flag comes off and the exit code is the gate.

---

## A. Visual & CSS

| id | Ban | Why | Detector | Current |
| --- | --- | --- | --- | --- |
| B11 | Purple / indigo / lila as a structural colour, and any gradient mesh | taste §9.A LILA RULE; anti-reference 1 | Convert every emitted `*_color` hex to HSL; FAIL when hue ∈ [250,300] and saturation > 0.30 | 0 |
| B12 | Pure black `#000000` or pure white `#FFFFFF` as a text colour | hallmark "pure black, pure white" | FAIL when a `*_color` key equals either literal | 0 |
| B15 | Glassmorphism as a default surface (`backdrop-filter`, layered translucent borders) | taste §9.A; hallmark "glassmorphism without purpose" | Not applicable while the kit emits no CSS. Reserved: FAIL if `custom_css` or a `customCode` kit tab is ever non-empty | n/a |
| B17 | Neon / outer glow, "AI glow" | taste §9.A | FAIL when a box-shadow colour has saturation > 0.5 and blur > 40 px | 0 (all shadows neutral) |
| B18 | Card-in-card (a bordered or filled container inside another) | hallmark "card-in-card" | FAIL when a container has (background OR border) and an ancestor within 2 levels also has one | **pending detector** (declared, see note 1) |

## B. Typography

| id | Ban | Why | Detector | Current |
| --- | --- | --- | --- | --- |
| B14 | Inter / Roboto / Arial / Helvetica / Lato as the **display** face | P1 spec; taste §9.B "AVOID Inter as default" | FAIL when the kit's display/heading global typography family is in `dials.toml [invariants] display_family_denylist` | 0 (Sora) |
| B21 | Oversized H1 whose hierarchy comes only from scale | taste §9.B | WARN when H1 ≥ 2.2 × H2 size | 0 (64 / 46 = 1.39) |
| B22 | Em-dash `—` anywhere: headline, eyebrow, pill, body, quote, caption, button, alt | taste §9.G, the single most-violated tell | FAIL on U+2014 in any string in any settings value | **12** |
| B23 | Negative letter-spacing on Persian text | `references/06-rtl-persian.md`; breaks letter joins | FAIL when a global typography row with an FA/Arad family has letter_spacing < 0 | 0 (FA tracking floor is 0) |

## C. Layout & spacing

| id | Ban | Why | Detector | Current |
| --- | --- | --- | --- | --- |
| B06b | Icon-in-rounded-square feature grid; three equal feature cards | P1 spec; taste §9.C; hallmark "3-column feature grid" + "icon-tile feature card" | FAIL when a section has ≥3 sibling card containers, each containing exactly one icon + a heading, equal `_flex_basis`, and a surface | **0 sections detected** (the kit's 6-card grid uses 3-across equal cards; see note 2 for why the detector reads 0) |
| B13 | Decorative dividers | P1 spec | FAIL per divider whose `width` ≤ 30 % (an ornament rule, not a separator) | **135 dividers emitted; ornament-rule count pending note 3** |
| B16 | Centred hero trio (eyebrow + H1 + lead + 2 buttons) unless DESIGN_VARIANCE ≥ 7 | P1 spec | FAIL when the first section of a page is centred AND contains ≥4 of: eyebrow heading, H1, text-editor lead, ≥2 buttons | **pending detector**; kit heroes are left-aligned splits (licensed by variance 8) |
| B24 | Centred everything | hallmark "centred everything" (Major) | WARN when centred sections > 55 % (`dials.toml [invariants]`) | **82 % (78/95)** |
| B25 | Eyebrow on every section | hallmark "eyebrow on every section" (Major) | WARN when sections carrying an eyebrow-style heading > 60 % | **93 % (88/95)** |
| B26 | Numbered step labels ("01", "Step 3", "Phase 02") | taste §9.F | WARN when a heading/text is a bare ordinal or an explicit step label | **16** |
| B27 | Version / status eyebrow (`v2.0`, `BETA`, `EARLY ACCESS`) | taste §9.F | WARN on the version regex in hero-band copy | **6** |
| B28 | Middle-dot `·` used as a universal separator | taste §9.F (max 1 per line) | WARN when a string contains > 1 `·` | 0 |
| B09 | Animate-on-scroll on everything | taste §9.F; hallmark | WARN when animated elements > 25 % | 7 % (155/2242) |
| B29 | `transition-all` / universal `hover:scale-105` | taste §9.F microinteraction tells | Not applicable while the kit emits no CSS; enforced by the no-custom-CSS rule | n/a |

## D. Content & data

| id | Ban | Why | Detector | Current |
| --- | --- | --- | --- | --- |
| B03 | Fabricated metrics presented as fact (`99.9 %`, `12×`, `50k model calls`) | hallmark "Invented metrics"; taste §9.D "fake-perfect numbers" | FAIL on the metric regex in claim contexts (excludes pick-lists and price ranges) | **8** |
| B03b | Price placeholders shipped as if real | P1 honesty rule | WARN per currency amount; must be documented as placeholder copy | **10** |
| B04 | Generic names and startup-slop brands (John Doe, Acme, Nexus, SmartFlow) | taste §9.D | FAIL on the generic-name list | 0 |
| B05 | Filler verbs (elevate, seamless, unleash, next-gen, revolutionize, empower, leverage) | taste §9.D | FAIL on the filler-verb list | 0 |
| B30 | Testimonials / logos / case numbers inventing named people or companies | hallmark anti-patterns § Invented metrics + honest-copy discipline | WARN per testimonial widget carrying a `testimonial_name`; must be replaced before launch | **pending detector** (see note 4) |
| B31 | Poetic/performative section labels ("From the field", "Loose plates") and mock-humble copy | taste §9.F | WARN on the label list | 0 |
| B32 | Weather/locale strips, "Quietly in use at" social-proof headers | taste §9.F | WARN on the phrase list | 0 |

## E. Project-specific (derived from the anti-references)

| id | Ban | Why | Detector | Current |
| --- | --- | --- | --- | --- |
| B40 | 3D SaaS blobs, floating orbs, aurora meshes | anti-reference 1 | Image assets must be flat-vector or real product UI; enforced by the media review checklist in `docs/p1/type-decision.md` §6 and by asset-name audit | 0 (all 7 assets are flat vector / photographic) |
| B41 | Stock-photo hero of people at laptops | anti-reference 2; hallmark "AI-illustration look" family | WARN when a hero-band image alt contains person/team/office keywords | **1** (`about-studio.jpg` is a real-looking workspace; licensed for About only) |
| B42 | Decorative status dots on nav/badges/list rows | taste §9.F | WARN per dot container without a semantic state key | 0 |
| B43 | Emoji as feature icons | hallmark "generic emoji as feature icon" | FAIL on emoji codepoints inside icon-bearing strings | 0 |
| B44 | Div-based fake product UI | taste §9.E, 9.F | Not applicable: the kit has no `html` widget and builds no fake UI. Reserved FAIL if an `html` element ever appears (already a hard verifier error) | 0 |

---

## Notes — where the detectors are not yet what the ban claims

Being explicit here is cheaper than a green check that means nothing.

1. **B18 (card-in-card)** is declared but not implemented. Implementing it correctly needs
   the container tree with border/background resolution (including hover variants), which is
   ~25 lines in `banlist_check.py`. Until then the ban is a review rule, not a gate.
2. **B06b reads 0 sections** although the kit ships a 6-card equal-width feature grid with
   one icon per card. The detector requires `background` OR `border` on each card *and* a
   single shared `_flex_basis`; the kit's feature cards satisfy the shape, so a 0 means the
   detector is wrong, not that the pattern is absent — treat the ban as **tripped** until
   B06b is fixed and shows a real count.
3. **B13 counts 135 dividers** but the ornamental subset is not yet distinguished from
   structural hairlines (footer separators, table rules). The rule as written (width ≤ 30 %)
   produced no hits because the kit's eyebrow rules are set per-breakpoint; the detector needs
   to resolve responsive widths before its number is trustworthy.
4. **B30** needs to distinguish a placeholder name (acceptable in a template kit, if
   documented) from a claim of real endorsement. Policy decided in P1: every testimonial and
   logo in demo copy must be labelled placeholder in `docs/03-template-library.md`; the
   detector is a lint that lists them.

## How a ban is added

1. Write the rule statement, the reason (with its source) and the detector in one of the
   tables above.
2. Implement the detector in `tools/banlist_check.py` and add its id to `FAIL_RULES` if it
   must be fatal.
3. Run it on the current kit: if it trips, it goes into `docs/p1/delta-table.md` with a fix
   phase — never into the ban list only.
4. When all its hits are zero and the detector is trusted, remove the rule from the
   `--report-only` allowance in `.github/workflows/kit.yml`.
