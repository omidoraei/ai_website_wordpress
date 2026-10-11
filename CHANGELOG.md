# Changelog

All notable changes to the Aurora AI Elementor template kit.
This project follows [Keep a Changelog](https://keepachangelog.com/) and
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-11

First public release.

### Added
- **Design system** in `templates/kit/aurora-site-settings.json`:
  4 system global colours, 14 custom global colours, 18 global typography styles
  (including 4 Persian/Arad styles), content width 1240 px, tablet and mobile
  breakpoints, page background, H1-H6 ladder, body/link/button/form-field styles.
- **9 pages**: Home (EN), Home (FA/RTL), About, Services, Case Studies, Pricing,
  Journal, Contact, 404.
- **6 Theme Builder layouts**: header EN, header FA, footer EN, footer FA,
  single post, blog archive, search results.
- **1 popup**: exit-intent lead magnet with a single-field form.
- **22 reusable section blocks**, including 5 Persian variants, covering hero,
  logo cloud, feature grid, feature zigzag, stats band, capability cards,
  process steps, case studies, testimonials, pricing, FAQ, CTA, team, contact,
  newsletter, content two-column and page hero.
- **Build tooling** in `tools/`: `build.py` (build + validate), `media.py`
  (image pipeline), `preview.py` (browser preview) and the `aurora/` package
  that contains the Elementor JSON DSL, design tokens, components and layouts.
- **Documentation** in `docs/`: installation, design system, template library,
  RTL/Persian setup, Theme Builder configuration, performance & accessibility,
  and FAQ/troubleshooting.

### Notes
- Built entirely from Elementor Flexbox Containers and native Elementor /
  Elementor Pro widgets. No HTML widget, no custom CSS, no custom JavaScript,
  no external animation library.
- 40 documents, 962 containers, 1 280 widgets in total.
- Demo imagery is generated, optimised to 3:2 JP/JPEG at 1500x1000 and imported
  by Elementor from the release assets at
  `releases/download/v1.0.0/`.
