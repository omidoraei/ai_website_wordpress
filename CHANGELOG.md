# Changelog

All notable changes to the Aurora AI Elementor template kit.
This project follows [Keep a Changelog](https://keepachangelog.com/) and
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-11

First public release.

### Added
- **Design system** in `templates/kit/aurora-site-settings.json`:
  4 system global colours, 15 custom global colours <!--f:global_colours-->19<!--/f-->, <!--f:typography_styles-->15<!--/f--> global typography styles
  (including 4 Persian/Arad styles), content width 1240 px, tablet and mobile
  breakpoints, page background, H1-H6 ladder, body/link/button/form-field styles.
- **<!--f:pages-->9<!--/f-->**: Home (EN), Home (FA/RTL), About, Services, Case Studies, Pricing,
  Journal, Contact, 404.
- **<!--f:theme_builder_layouts-->7<!--/f-->**: header EN, header FA, footer EN, footer FA,
  single post, blog archive, search results.
- **1 popup**: exit-intent lead magnet with a single-field form.
- **<!--f:blocks-->22<!--/f--> reusable section blocks**, including 5 Persian variants, covering hero,
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
- <!--f:documents_total-->40<!--/f-->, <!--f:containers-->962<!--/f-->, <!--f:widgets-->1 280<!--/f-->280 in total.
- Demo imagery is generated, optimised to 3:2 JPEG at 1500x1000, and served from
  the permanent `kit-assets-v1` git tag so Elementor can download it on import:
  `https://github.com/omidoraei/ai_website_wordpress/raw/kit-assets-v1/media/`.
