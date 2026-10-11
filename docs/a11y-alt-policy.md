# Alt-text policy (a11y)

**Scope:** every Image widget in `templates/**`. **Enforcement:** `tools/alt_quality_check.py`
(measures) plus the `alt_nonempty_count == image_widget_count` and `alt_policy_documented`
invariants in `docs/_generated/invariant-baseline.json`. **Owner of the copy:** P8 for the two
strings flagged below; nobody rewrites alt text in P1.7.

Presence was never the hard part. P1.6 proved `settings.image.alt` is non-empty on every image
widget; this file defines what the strings must *say*, so that "alt text present" stops being
mistaken for "accessibility done". Storage path is measured, not assumed:
`settings.image.alt` (an earlier audit read `settings.alt`, which Elementor always leaves empty -
see `docs/CLAIMS.md` C-017, C-027).

## Rules

**R1 content images** - descriptive, locale-matched, no "image of".

* Describe what the picture shows, in the language of the document it sits in: an EN page gets an
  EN alt, a FA page gets a FA alt. One string never does double duty across locales.
* Never open with "image of", "picture of", "photo of" ("تصویرِ ..." / "عکس از ..."): a screen
  reader already announces the role, so the phrase is noise.
* No keyword stuffing, no brand-plus-city stuffing, no repeated words for ranking. An alt is a
  sentence a blind user hears instead of seeing the image, not a meta tag.
* Do not describe what is already written next to the image. If the caption or a neighbouring
  heading already carries the meaning, keep the alt short.

**R2 decorative images** - `alt=""` (empty), no exceptions.

* A background texture, divider, glow, pattern or pure-aesthetic shape is decorative. Empty alt
  takes it out of the accessibility tree, which is the correct outcome; a *described* decorative
  image forces every screen-reader user to hear decoration.
* Elementor stores this as `"alt": ""` inside `settings.image`. The check reports any image whose
  filename carries a decorative marker (`bg`, `background`, `pattern`, `texture`, `shape`, `blob`,
  `decor`, `divider`, `noise`, `gradient`, `wave`) while its alt is non-empty, as
  `suspected_decorative_with_nonempty_alt`.
* The word is *suspected*: JSON cannot tell a stock texture from a diagram whose filename happens
  to contain one of those markers. The list is a review queue, not a verdict.

**R3 logo** - the brand name, or empty when adjacent text already names the brand.

* A logo that is the only text naming the company gets the brand name as alt (`Aurora AI`, not
  `logo`, and not a sentence).
* A logo that repeats a name already present as text in the same landmark is decorative: `alt=""`.
* The check flags an alt equal to the brand name (`suspected_decorative_with_nonempty_alt`,
  reason "alt equals the brand name"): when the header wordmark sits next to the site name, that
  alt should be empty. Site-logo widgets inherit the alt you set on the attachment in the Media
  Library, so the rule is applied there, not in the template.

**R4 FA (Farsi) alt** - natural Persian, not a literal translation.

* Write the Persian alt as a Persian sentence a Persian speaker would say out loud: `داشبورد
  تحلیل مکالمه` beats a word-for-word rendering of the English string's syntax.
* Keep the technical terms Persians actually use; transliterating an English compound
  (`داشبورد-مانیتورینگ-ریل-تایم`) is worse than the English term in Persian script.
* Persian alt strings must not contain Latin words unless the term genuinely has no Persian
  form, and never a Persian phrase inside an otherwise English document (the language-mix defect
  tracked in `docs/p1.7/lang-mix-audit.md`).

## Generic strings (a review queue, not a rule)

`image`, `photo`, `picture`, `banner`, `screenshot`, `graphic`, `img`, `thumbnail`, `تصویر`,
`بنر`, `عکس` describe the medium, not the content. The check reports them as
`suspected_content_with_generic_alt`; each hit must either be rewritten (R1) or moved to the
decorative bucket (R2) with a stated reason.

`repeated_alt_across_different_image_files` reports one alt string reused on two or more different
image files. Reuse on the *same* file is correct (one screenshot placed twice is still one
picture); reuse across different files means at least one of them is described wrongly.

## How to measure (the commands are the evidence)

```
python3 tools/alt_quality_check.py            # report; exit 1 only when the scan floor breaks
python3 tools/alt_quality_check.py --json     # the numbers quoted in the handoff come from here
python3 tools/alt_quality_check.py --strict   # R1/R2 findings exit 1 (flips at P8)
```

The tool asserts its own floor first (fewer image widgets scanned than the floor is a scanner
failure, exit 1): "no findings" in an empty scan is not a pass.

## Status at P1.7 (measured, not asserted)

* Every image widget carries a non-empty `settings.image.alt`; the distinct-string count is what
  the tool prints, and it is what the PR body quotes.
* One quality finding is measured and deliberately **not** fixed in this phase (no alt rewriting is
  in scope): nine widget instances - three distinct strings - carry a client-name-only alt
  (`Northwind Retail`, `Keystone Bank`, `Helios Health`, each reused across three documents), 0
  decorative suspects, 0 generic strings, 0 reused-across-different-files. P8 rewrites them per R1.
* A Persian-script alt inside a document whose name carries no `fa-` marker is **not** present:
  `alt_locale_mismatch` is 0. The Persian copy that does sit inside EN-named documents is Icon List
  text, measured in `docs/p1.7/lang-mix-audit.md` - a different defect with a different owner.
* `alt_policy_documented` is true when this file exists and contains the rule ids R1-R4; the
  checker fails if a rule is deleted.

## Ratchet

`docs/_generated/invariant-baseline.json` records the current counts for
`alt_nonempty_count`, `alt_distinct_count` and the quality findings. Coverage may **not** fall and
findings may **not** rise while the freeze is on. When P8 rewrites the copy, the baseline is
updated in the same commit - and only then does `--strict` become the CI step.
