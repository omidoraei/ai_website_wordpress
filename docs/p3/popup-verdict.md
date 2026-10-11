# Popup verdict + Journal card anatomy (P3, Part C)

## 1. Exit-intent popup — verdict

**KEEP the template. SHIP IT DORMANT. Fix the promise before anyone enables it.**

Ship state: `popups/aurora-lead-magnet.json` imports as a Pro popup with **no display conditions**,
so it never renders until the buyer sets a condition. That is the state the kit ships in.

Why not kill it: B1 is *a Template Kit to sell*, and C1 explicitly keeps the popup. The popup
builder is part of what a buyer evaluates, and deleting it removes a sellable feature. Killing it
would punish the product to fix a placement problem.

Why not enable it by default: the site's job (B3) is **book a demo**. An exit-intent that captures
an email for a checklist creates a *second* conversion goal, aimed at a colder intent, on pages
whose primary action is already competing with it. In 2026 an unconditional exit-intent on a
nine-page commercial site is a UX tax: it interrupts the one task the visitor came to do.

Two content defects that must be fixed first:

1. **The promise has no deliverable.** The popup says "The 18-point readiness checklist we run with
   every engagement" — no checklist asset ships in the kit, and the number is unlabelled sample
   data (B4 policy). Either ship a placeholder checklist (buyer replaces it) or rewrite the promise
   to something the site can actually deliver, aligned with the primary CTA ("we will send a
   30-minute demo agenda").
2. **The privacy line is good and must stay.** "We store your email only to send the checklist" is
   exactly the honesty line C5 requires; keep it verbatim in any rewrite.

### Measurement plan (only after the buyer adds consent-gated analytics)

The kit ships no tracking (C5), so the popup cannot be measured until the buyer installs an
analytics tool behind a consent banner. The plan is written for that state:

| element | value |
| --- | --- |
| events | `popup_shown`, `popup_dismissed`, `popup_submit` (+ the page path on each) |
| placement (test) | **one** page only — `/pricing/`, where an exit signal means price hesitation |
| window | 14 days after enabling, or 1 000 `popup_shown`, whichever comes first |
| decisions | submit rate = `popup_submit / popup_shown`; annoyance = `popup_dismissed / popup_shown` |
| starting guardrails | disable if submit rate < 0.5% of impressions, or if dismissals exceed 90%, or if exits from `/pricing/` rise against the previous 14-day baseline |
| rollback | remove the display condition (Elementor → Popups → Conditions) or unpublish; ~30 seconds, no template edit — `docs/07-faq-troubleshooting.md` gets the recipe |

Those thresholds are **starting guardrails, not predictions**: they exist so the enable/disable
decision is made on numbers rather than on taste. The first real week of data replaces them.

## 2. Journal — Loop card anatomy

**What ships today.** The listing widget is Elementor Pro's **Archive Posts** (`archive-posts`,
skin `cards`) — *not* Loop Grid. It is configured as: 3 columns → 2 (≤1024) → 1 (≤767), 9 posts per
page, numeric pagination, title on, excerpt on, read-more text on, meta colour set. There is **no
image setting in the card**: the current card is text-only (title · meta · excerpt · read-more).

**Recommended card anatomy** (applies to Archive Posts as-is, or to a Loop Grid + Loop Item if the
buyer switches):

| slot | rule |
| --- | --- |
| media | 3:2 image, full card width, radius from the card token set — enables when the card gains an image (Loop Grid) |
| title | `h3`, 2 lines max, links to the post |
| meta | date + author, muted colour; one line; tabular figures if a reading time is added |
| excerpt | ≤ 18 words, no ellipsis-only stubs |
| read-more | text link, same style everywhere ("Read the article") |
| card | `article` tag, one border, one radius, no nested card (BANLIST `cards_nested_max = 0`) |
| state | hover = border colour + link underline; nothing moves or scales |

**The three states** — every listing must have all three designed, not fallen back to:

1. **Empty (0 posts).** The search-and-subscribe state: one line explaining the archive is young,
   the search form, and the newsletter block. Applied to: fresh archive categories, the search
   page's zero-result case (which also needs the query echoed back: "No results for «X»").
2. **One post.** No grid: the single card renders at full content width with the image large; the
   pagination control hides itself; the CTA band stays.
3. **Many posts.** The grid, paginated; at 9-per-page the third row is the fold at 1920 and the
   second at 1024 — if the buyer raises `posts_per_page`, the number must be re-checked against the
   fold contract in `docs/p3/IA.md` §4.10.

**FA note.** The Persian listing uses the same anatomy with Vazirmatn and RTL ordering (media
first on the right); the missing piece is an FA archive surface — B2 parity is a P4 build item, and
today the FA set contains no listing template (8 FA documents: 1 page, 5 blocks, 1 header, 1
footer).
