# Landmark and heading audit (generated)

Produced by `python3 tools/landmark_audit.py` over **39 documents** and **962 containers** (95 carry an `html_tag`). Do not hand-edit; re-run the tool.

## Tag histogram across the whole tree

| html_tag | containers |
| --- | ---: |
| `section` | 90 |
| `footer` | 2 |
| `header` | 2 |
| `main` | 1 |

## Per document

| document | type | containers | tagged | landmarks | h1 | gaps |
| --- | --- | ---: | ---: | --- | --- | --- |
| `blocks/capability-cards.json` | section | 11 | 1 | section×1 | — | — |
| `blocks/case-studies.json` | section | 15 | 1 | section×1 | — | — |
| `blocks/contact-section.json` | section | 17 | 1 | section×1 | — | — |
| `blocks/content-two-column.json` | section | 6 | 1 | section×1 | — | — |
| `blocks/cta-band.json` | section | 8 | 1 | section×1 | — | — |
| `blocks/fa-cta-band.json` | section | 8 | 1 | section×1 | — | — |
| `blocks/fa-faq-accordion.json` | section | 4 | 1 | section×1 | — | — |
| `blocks/fa-feature-grid.json` | section | 17 | 1 | section×1 | — | — |
| `blocks/fa-hero-split.json` | section | 13 | 1 | section×1 | عاملهای هوش مصنوعی که واقعاً به محصول میرسند. (heading) | — |
| `blocks/fa-pricing-table.json` | section | 15 | 1 | section×1 | — | — |
| `blocks/faq-accordion.json` | section | 4 | 1 | section×1 | — | — |
| `blocks/feature-grid.json` | section | 17 | 1 | section×1 | — | — |
| `blocks/feature-zigzag.json` | section | 20 | 1 | section×1 | — | — |
| `blocks/hero-split.json` | section | 13 | 1 | section×1 | AI agents that actually ship. (heading) | — |
| `blocks/logo-cloud.json` | section | 3 | 1 | section×1 | — | — |
| `blocks/newsletter-band.json` | section | 6 | 1 | section×1 | — | — |
| `blocks/page-hero.json` | section | 4 | 1 | section×1 | — | — |
| `blocks/pricing-table.json` | section | 15 | 1 | section×1 | — | — |
| `blocks/process-steps.json` | section | 13 | 1 | section×1 | — | — |
| `blocks/stats-band.json` | section | 14 | 1 | section×1 | — | — |
| `blocks/team-grid.json` | section | 17 | 1 | section×1 | — | — |
| `blocks/testimonials.json` | section | 11 | 1 | section×1 | — | — |
| `footers/aurora-footer-en.json` | footer | 15 | 1 | footer×1 | — | — |
| `footers/aurora-footer-fa.json` | footer | 15 | 1 | footer×1 | — | — |
| `headers/aurora-header-en.json` | header | 6 | 1 | header×1 | — | — |
| `headers/aurora-header-fa.json` | header | 6 | 1 | header×1 | — | — |
| `loop/aurora-archive.json` | archive | 18 | 4 | section×4 |  (theme-archive-title) | no `main` landmark |
| `loop/aurora-search-results.json` | search-results | 12 | 3 | section×3 | Search results (heading) | no `main` landmark |
| `loop/aurora-single-post.json` | single | 10 | 2 | main×1, section×1 | — | no post-title widget - the post renders without its visible title and without an `h1`; no `h1` heading |
| `pages/aurora-404.json` | page | 7 | 1 | section×1 | This page took an unplanned detour (heading) | no `main` landmark |
| `pages/aurora-about.json` | page | 72 | 7 | section×7 | — | no `main` landmark; no `h1` heading |
| `pages/aurora-blog.json` | page | 15 | 3 | section×3 | — | no `main` landmark; no `h1` heading |
| `pages/aurora-contact.json` | page | 34 | 4 | section×4 | — | no `main` landmark; no `h1` heading |
| `pages/aurora-home-en.json` | page | 150 | 13 | section×13 | AI agents that actually ship. (heading) | no `main` landmark |
| `pages/aurora-home-fa.json` | page | 150 | 13 | section×13 | عاملهای هوش مصنوعی که واقعاً به محصول میرسند. (heading) | no `main` landmark |
| `pages/aurora-portfolio.json` | page | 53 | 5 | section×5 | — | no `main` landmark; no `h1` heading |
| `pages/aurora-pricing.json` | page | 83 | 6 | section×6 | — | no `main` landmark; no `h1` heading |
| `pages/aurora-services.json` | page | 60 | 7 | section×7 | — | no `main` landmark; no `h1` heading |
| `popups/aurora-lead-magnet.json` | popup | 5 | 1 | section×1 | — | — |

## Documents with gaps

- `loop/aurora-archive.json`: no `main` landmark
- `loop/aurora-search-results.json`: no `main` landmark
- `loop/aurora-single-post.json`: no post-title widget - the post renders without its visible title and without an `h1`; no `h1` heading
- `pages/aurora-404.json`: no `main` landmark
- `pages/aurora-about.json`: no `main` landmark; no `h1` heading
- `pages/aurora-blog.json`: no `main` landmark; no `h1` heading
- `pages/aurora-contact.json`: no `main` landmark; no `h1` heading
- `pages/aurora-home-en.json`: no `main` landmark
- `pages/aurora-home-fa.json`: no `main` landmark
- `pages/aurora-portfolio.json`: no `main` landmark; no `h1` heading
- `pages/aurora-pricing.json`: no `main` landmark; no `h1` heading
- `pages/aurora-services.json`: no `main` landmark; no `h1` heading

## Honest limits

- `nav` is not detectable here: the Pro `nav-menu` widget renders its own tag and does not store it in the template JSON. Verify on a real Pro install (see `docs/OPEN-QUESTIONS.md`).
- `article` is expected only inside Loop Item templates; the kit ships none today, so 0 is correct, not a gap.
- Popups render inside Elementor's own dialog wrapper; the audit judges only the template content it can see.
