# Type decision (P1)

Scope: the type system for the Aurora kit, the licence position for the Persian face, and the
rules a future phase must not break. Every claim carries its evidence; anything unprovable is
marked **UNVERIFIED**.

---

## 1. The split

| Role | Latin | Persian (FA) | Why |
| --- | --- | --- | --- |
| Display / headings | **Sora** 600/700 | **Arad** 700 (fallback **Vazirmatn**) | Role not appearance: the display face must carry personality at 46-64 px with tight tracking. Sora is a geometric grotesque with squarish terminals - technical without the Inter/Helvetica neutrality the ban list rejects. |
| Body / UI | **Inter** 400/500/600 | Arad / Vazirmatn 400 | Inter is permitted as the **body** face only. At 17 px / 1.75 line-height it is the most legible long-form option and is already present in WordPress admin. `BANLIST.md` B14 forbids it as the *display* face, and the verifier enforces that on the kit's global typography. |
| Labels / eyebrows | Inter 700, uppercase, +1.6 px | Arad 600, **transform: none** | Persian has no letter case; the FA label style replaces uppercase emphasis with weight and colour (`fa-label`). |
| Numerals (display) | Latin | Persian-Indic (۰-۹) in FA display copy | See §4. |

Machine-readable: `tools/aurora/tokens.py` (`SYSTEM_TYPOGRAPHY`, `CUSTOM_TYPOGRAPHY`) and the
generated kit document `templates/kit/aurora-site-settings.json` (15 global styles, of which
4 are FA).

## 2. Optical sizes and the ladder

| Token | Desktop | Tablet | Mobile | Line height (EN) | Tracking |
| --- | ---: | ---: | ---: | ---: | ---: |
| H1 (display) | 64 px | 48 px | 36 px | 1.06 | −1.6 px |
| H2 (section) | 46 px | 36 px | 28 px | 1.12 | −1.0 px |
| H3 (card) | 22 px | 22 px | 20 px | 1.30 | −0.3 px |
| H4 | 19 px | 19 px | 18 px | 1.35 | −0.2 px |
| H5 | 16 px | 16 px | 16 px | 1.40 | 0 |
| H6 | 13 px | 13 px | 13 px | 1.30 | +0.4 px (uppercase) |
| Body | 17 px | 17 px | 16 px | 1.75 | 0 |
| Lead | 19 px | 18 px | 17 px | 1.70 | 0 |
| Eyebrow | 13 px | 13 px | 13 px | 1.30 | +1.6 px |

Ratio check: H1/H2 = 1.39 and H1/body = 3.76. `BANLIST.md` B21 warns above 2.2 (scale-only
hierarchy); the kit passes. Hierarchy is carried by **weight and colour** as well as size, per
taste §9.B ("NO oversized H1s that just scream").

`rem` note: the ladder is authored in `px` because Elementor's typography controls store px,
mobile/tablet values and units per breakpoint. The kit does **not** emit `rem`; converting the
ladder to rem would require custom CSS (banned) or a filter in a child theme. This is a
deliberate, documented deviation from the "ladder in rem" instruction: it is unimplementable
inside the stack constraint without violating the no-custom-CSS rule.
**If a client requires rem scaling, the correct fix is a child-theme filter on Elementor's
typography values, not a change to this kit.**

## 3. Arad — licence position

| Question | Answer | Evidence |
| --- | --- | --- |
| Is Arad bundled with the kit? | **No.** No font binary ships in this repository. | `LICENSE` § THIRD-PARTY NOTICES; `skills/elementor-native-kit/references/06-rtl-persian.md` §6 |
| What licence does Arad carry? | **UNVERIFIED.** Arad is a commercial Iranian typeface; no authoritative licence text was retrievable in this environment (font foundries are not on the network allow-list, and GitHub hosts no canonical Arad release under an OSI licence). | Attempted: GitHub repository search for Arad Persian/Arabic fonts returned no repository carrying an SPDX licence for it |
| How is it referenced, then? | By **family name only**. The FA globals set `font-family: Arad`, which silently falls back if the family is absent. Nothing in the kit depends on the file existing. | `tokens.py` FA typography rows |
| What must a buyer do? | Upload their own licensed copy via **Elementor → Custom Fonts** (Pro) naming the family exactly `Arad`. | `docs/04-rtl-persian-setup.md` §2 |

**Rule:** because the licence is unverified, the kit must never be advertised as shipping or
licensing Arad, and the fallback path must remain fully functional. That is why §4 exists.

## 4. Vazirmatn — the audited fallback

| Property | Value | Evidence |
| --- | --- | --- |
| Licence | **SIL Open Font License 1.1 (OFL-1.1)** | `gh api repos/rastikerdar/vazirmatn` → `license.spdx_id = OFL-1.1`, `license.name = "SIL Open Font License 1.1"` (verified 2026-10-11) |
| Repo | `rastikerdar/vazirmatn` (3 256 ★) | same |
| Self-hostable through Elementor? | **Yes — Elementor → Custom Fonts** (Pro), upload the WOFF2 weights, family name `Vazirmatn`. No custom CSS is involved: Elementor writes the `@font-face` rules itself. | `docs/04-rtl-persian-setup.md` §2 |
| Weights needed | 400, 600, 700 | matches the FA globals |
| Cost | OFL permits commercial use, modification and redistribution; the only obligations are retaining the copyright notice and not selling the font by itself | OFL-1.1 terms |

### The swap path (exact, no code)

1. **Elementor → Custom Fonts → Add New**, title `Vazirmatn`, upload the three WOFF2 weights
   against 400 / 600 / 700, publish.
2. **Elementor → Site Settings → Global Fonts**, set the family of the four `FA / …` styles to
   `Vazirmatn`.
3. **Re-run** `python3 tools/verify.py && python3 tools/banlist_check.py` - B23 (negative
   tracking on Persian) must stay at 0 and the FA line-heights must be unchanged.
4. Update `tools/aurora/tokens.py` if you want the generated templates to name Vazirmatn
   directly (so a fresh import needs no manual step), then `python3 tools/build.py`.

**Do not** substitute Inter/Sora for Persian text: they lack the required glyph coverage for
Persian and the FA line-heights were tuned for Arad/Vazirmatn metrics.

## 5. Persian metrics rules (enforced, not advisory)

| Rule | Value | Enforced by |
| --- | --- | --- |
| Tracking floor | **≥ 0** for every FA style; negative tracking breaks letter joins | `BANLIST.md` B23 (FAIL) |
| FA heading line-height | 1.5-1.55 em (vs 1.12-1.30 EN) | `references/06-rtl-persian.md` |
| FA body line-height | 2.0 em (vs 1.75 EN) | same |
| Display size FA | 54 px (vs 64 EN) | same - Persian renders visually larger per point |
| Eyebrow transform | `none` (no case in Persian) | same |
| Uppercase | never applied to FA copy | same |

## 6. Numeral policy

| Context | Digits | Why |
| --- | --- | --- |
| FA display copy (headings, eyebrows, stat numbers, step labels) | Persian-Indic ۰-۹ | visual coherence with the script |
| Form fields, prices, counters, search, WooCommerce, any value WordPress parses | **Latin** | Persian digits break validation, sorting and payment flows |
| Mixed runs (a Latin product name inside a Persian sentence) | no control characters; let the bidi algorithm run | `tools/bidi_check.py` fails on embeddings/isolates in ids, control names and URLs |

## 7. Asset review rule (derived from anti-reference 1)

Photography and illustration: flat vector product surfaces and real workspace photography only
- no 3D blobs, no floating orbs, no aurora gradients, no AI-illustration look, no stock people
at laptops as a hero. Current kit: 6 flat-vector assets plus one workspace photograph
(`about-studio.jpg`, About page only, flagged as `B41` in `BANLIST.md` for review).

## 8. What P2 must not break

- Do not switch the display face to Inter/Roboto to "simplify" (B14 is fatal).
- Do not add letter-spacing to FA styles, even small negative values for "tightness" (B23).
- Do not move body copy out of the body face to increase "personality"; personality belongs to
  the display face and the palette.
- Do not introduce a third Latin family. Two families plus one Persian family is the budget.

## P2 carry-forward rule (P1.6)

**B5 is USER-CHOSEN and SUPERSEDES the original instruction's Arad mention. Do NOT reintroduce
Arad in P2 to honour the earlier wording.** Arad leaves the build; the FA system is Vazirmatn
(SIL OFL-1.1, self-hosted through Elementor Custom Fonts). Arad may return only as an optional
documented swap if the human produces licence proof.
