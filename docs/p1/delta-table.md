# P1 delta table — current kit vs DNA target

Diagnosis only. **Nothing was fixed in P1** (phase constraint). Severity is assigned by
impact on the buyer, not by effort. Numbers are live output of the tools named in each row —
re-run them; do not trust this file.

```bash
python3 tools/banlist_check.py --json      # B-rules + ratios
python3 tools/verify.py                    # structure, references, media
```

Measurement base: 39 template documents, 95 sections, 2 242 elements, 1 280 widgets, 135
dividers, 310 animated elements.

## Legend

| Severity | Meaning |
| --- | --- |
| **S1** | Ship-blocker: reads as dishonesty or breaks the product promise |
| **S2** | Major: a recognised AI tell that a designer would flag in a review |
| **S3** | Polish: inconsistent with the DNA but does not damage credibility |

Fix phases: **P2** tokens + copy + structure, **P3** page composition, **P4** RTL/FA,
**P5** release.

Counts below are per-rule hits from `banlist_check.py`; a rule with a broken detector reports 0
and is marked ⚠️ rather than counted as passing.

---

## macrostructure

| Axis target | Current kit | Evidence | Δ | Sev | Fix |
| --- | --- | --- | --- | --- | --- |
| Section cadence ladder 120/80/56 px | Implemented (`SECTION_PAD_Y` in `tokens.py`) | `tools/verify.py` clean | ✅ | — | — |
| Band temperatures alternate; dark band ≤ 2 per long page | Dark band used on home (stats), services (FAQ), contact, single, popup overlay | `tokens.py` `state -> ink_950` usages | ⚠️ verify | S3 | P3 |
| Feature detail alternates asymmetric split with full-width grid | 6-card equal-width icon grid is the primary feature block | `B06b` tripped (detector limitation noted in BANLIST) | ❌ **violates** | **S2** | P2 |
| Hierarchy by type + space, not nested containers | 3-level nesting honoured; no card-in-card found in spot checks, but `B18` detector not implemented | `BANLIST.md` note 1 | ⚠️ unproven | S2 | P2 |
| Statement > ONE proof element > detail | Home runs: hero > logo cloud > feature grid > zigzag > stats > bento | `sections.py` block order | ⚠️ 2 features before proof | S3 | P3 |
| Left-aligned authority (not centred) | **82 % of sections centred** (78/95) | `banlist_check --json` → `centred_ratio 0.82` | ❌ **violates** | **S2** | P2/P3 |

## type-pairing

| Axis target | Current kit | Evidence | Δ | Sev | Fix |
| --- | --- | --- | --- | --- | --- |
| Geometric display face, not Inter | Sora 600/700 for all headings | kit doc `system_typography.primary`; `B14` = 0 | ✅ | — | — |
| Inter permitted for body only | Inter 400/500/600 body + labels | kit doc `Text / Body`, `Eyebrow / Overline` | ✅ | — | — |
| Hierarchy not carried by scale alone | H1/H2 = 1.39; weight + colour also used | `B21` = 0 | ✅ | — | — |
| Tracking tight on display, ≥ 0 on Persian | EN −1.6/−1.0/−0.3 px; FA tracking 0 | kit doc; `B23` = 0 | ✅ | — | — |
| Case policy: uppercase for eyebrows only | 88/95 sections carry an uppercase-style eyebrow | `sections_with_eyebrow 88/95 (93 %)` | ❌ **overused** | S2 | P2 |
| FA has its own metrics (not scaled EN) | 4 dedicated FA styles, line-height 1.5-2.0, size 54/40 | kit doc FA rows | ✅ | — | — |

## colour-anchors

| Axis target | Current kit | Evidence | Δ | Sev | Fix |
| --- | --- | --- | --- | --- | --- |
| Warm paper ground, never pure white | Page ground `#FFFBF5`; **0 pure-white surfaces** | `pure_white_surfaces 0` | ✅ | — | — |
| No purple/indigo/lila structure | 0 hits in hue 250-300 | `B11` = 0 | ✅ | — | — |
| No neon/outer glow | All shadows neutral, low saturation | `B17` = 0 | ✅ | — | — |
| Accent budget: ≤ 1 amber area larger than a button per section | Accent token `amber-600` referenced **294 times** vs `primary` 299 and `secondary` 272 — i.e. the accent is used at primary-token volume, so no budget is enforced | token census over 40 documents, 2 136 colour refs | ❌ **overused** | S2 | P2 |
| Coral as the single warm-cool counterpoint for data | `accent` (coral) referenced **15 times** out of 2 136 — present in tokens, effectively decorative | same census | ⚠️ underused | S3 | P2 |

## motion-signature

| Axis target | Current kit | Evidence | Δ | Sev | Fix |
| --- | --- | --- | --- | --- | --- |
| One direction (up), opacity + transform only | **`fadeInUp` is the only family used** (310 elements) | motion scan of all settings | ✅ | — | — |
| Duration 450-700 ms | Not set → Elementor default applies | `animation_duration` absent everywhere | ⚠️ undescribed | S3 | P2 |
| Stagger 80-110 ms, hard stop after 4th | Delays: 90/100/110/180/200/220/240/270/300/320/360/380/450 ms | delay histogram | ⚠️ tail beyond 4th | S3 | P2 |
| Animated ≤ 25 % of elements | **7 %** (155/2242) | `animated_ratio 0.07` | ✅ | — | — |
| Nothing moves above the fold / while reading | Not measured per-fold | — | ⚠️ unmeasured | S3 | P3 |
| Reduced-motion honoured | Not expressed (Elementor emits its own media query for Motion Effects) | — | ⚠️ verify on site | S2 | P5 |

## component-grammar

| Axis target | Current kit | Evidence | Δ | Sev | Fix |
| --- | --- | --- | --- | --- | --- |
| Radius scale honoured | 10/16/22/30/40/pill implemented | `tokens.py RADIUS` | ✅ | — | — |
| Separation by hairline, elevation only for interaction | 135 dividers, one colour; shadows on hover/hero only | `dividers 135` | ⚠️ see next row | S3 | P2 |
| No decorative dividers | Ornamental eyebrow rules exist; detector cannot yet separate them from structural hairlines | `B13` note 3 | ⚠️ unproven | **S2** | P2 |
| Icon tiles only when the tile is a link | Icon tiles used decoratively inside feature cards | `B06b` tripped | ❌ **violates** | **S2** | P2 |
| No card-in-card | Not proven either way | `B18` not implemented | ⚠️ unproven | S2 | P2 |
| Forms: label above field, one action | Implemented (Elementor form fields) | kit form section | ✅ | — | — |
| Data: tables first-class | Comparison table exists on pricing | `pricing` template | ✅ | — | — |

## tonal-temperature (technical-warm)

| Axis target | Current kit | Evidence | Delta | Sev | Fix |
| --- | --- | --- | --- | --- | --- |
| No hype verbs | 0 filler verbs found | `B05` = 0 | ✅ | — | — |
| No invented metrics or endorsement | **8 fabricated metric claims** (e.g. "50k model calls / month", "2M model calls") | `B03` = 8 | ❌ **violates** | **S1** | P2 |
| No placeholder prices presented as real | **10 currency amounts** ($0, $490 …) | `B03b` = 10 | ❌ undocumented placeholder | S2 | P2 |
| Testimonials/logos not claiming real people | Named quotes + company logos shipped as demo copy; detector pending (`B30`) | `BANLIST.md` note 4 | ❌ **unlabelled** | **S1** | P2 |
| No em-dash flourish | **12 em-dashes** in copy, incl. form success messages | `B01` = 12 | ❌ **violates** | S2 | P2 |
| Precise, unhurried voice | Otherwise consistent; no exclamation marks, no mock-humble copy | `B05`, `B31`, `B32` = 0 | ✅ | — | — |
| No version/status eyebrow in hero | **6 hits** ("Aurora Agents 2.0 - now generally available", 3 EN + 3 FA) | `B06` = 6 | ❌ **violates** | S2 | P2/P4 |
| No generic step labels | **16 hits** — process steps labelled 01-04 | `B07` = 16 | ❌ violates | S3 | P2/P3 |

---

## Summary — the P2 worklist, ranked

| Rank | Item | Sev | Rules | Phase |
| ---: | --- | --- | --- | --- |
| 1 | Remove or explicitly label every fabricated claim: 8 metrics, 10 prices, all named testimonials/logos | **S1** | B03, B03b, B30 | P2 |
| 2 | Replace the 6-card equal icon grid with an asymmetric composition (and fix the B06b detector to prove it) | S2 | B06b | P2 |
| 3 | Cut centred sections from 82 % to ≤ 55 %; keep the three genuinely centred moments (404, CTA, popup) | S2 | B24 | P2/P3 |
| 4 | Cut eyebrow coverage from 93 % to ≤ 60 % — keep it where it labels something specific | S2 | B25 | P2 |
| 5 | Remove all 12 em-dashes | S2 | B22 | P2 |
| 6 | Remove the 6 version/status eyebrows (EN + FA) | S2 | B27 | P2/P4 |
| 7 | Resolve decorative dividers (implement B13 properly, then fix what it finds) | S2 | B13 | P2 |
| 8 | Implement B18 (card-in-card) and B30 (placeholder endorsement) detectors, then fix findings | S2 | B18, B30 | P2 |
| 9 | Set explicit motion durations 500-600 ms and cap stagger at the 4th item | S3 | — | P2 |
| 10 | Rename numbered process steps to verb-noun labels ("Connect", "Evaluate", "Ship") | S3 | B26 | P3 |

**Total: 7 rules tripped by working detectors (2 FAIL-level, 5 WARN-level), plus 4 rules
(B13, B18, B30, B06b) that are tripped-or-unproven with an honest detector gap. 10 ranked fixes.**

## What P1 deliberately did NOT do

- No template was modified (`git diff --stat templates/` is empty for this phase).
- No token, palette or type value changed.
- The detector gaps (B13, B18, B30) were left as gaps with a written note rather than papered
  over with a heuristic that would report a false 0. **B06b currently reports 0 while the
  banned pattern is present** - that row is marked tripped until the detector is fixed.
