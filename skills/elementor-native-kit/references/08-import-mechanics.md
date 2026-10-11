# 08 — Import mechanics

Two different imports exist and they are not interchangeable. Getting them mixed up is the
single most common "the kit didn't work" report.

Provenance: `elementor/elementor@v3.35.9`, module
`app/modules/import-export-customization/` (runners and their base classes). Claims below are
from reading those runners; where a line number is not given, only the file path was
confirmed.

---

## The two paths

| | **Saved Templates** import | **Kit** import |
| --- | --- | --- |
| Admin screen | `Templates → Saved Templates → Import Templates` | `Elementor → Tools → Import / Export Kit → Import Kit` |
| Accepts | a `.zip` of template files, **or** a single `.json` | one kit archive |
| Runner | `Source_Local` template import | `import-export-customization` runners |
| What it creates | library documents (pages, headers, footers, blocks, popups) | site settings + optionally templates/content |
| This kit's file | `dist/aurora-ai-templates.zip` (40 documents) | `dist/aurora-ai-kit.zip` |

**Order matters.** Import the **templates first**, then the **kit**: the kit archive applies
the global colours and fonts that make those templates look correct.

## Standalone template JSON

Required top-level keys: `content`, `title`, `type`. `page_settings` is optional; Elementor's
own exports also add `version` (`DB::DB_VERSION`).

| Behaviour | Detail |
| --- | --- |
| Zip vs single file | both work; `__MACOSX` and dot-files are skipped |
| Per-file failures | **silent** — a bad file inside a zip does not fail the whole import, so verify by counting the templates that appear in *My Templates* |
| Unknown widget types | **survive the import**. A widget type your site does not have (a Pro widget on Free) is stored and renders nothing. This is why the kit can ship Pro widgets and still be imported on Free |
| Images | resolved local file → remote import (dedup by `sha1(url)` via `_elementor_source_image_hash`) → placeholder |
| Media zips | a media zip carries the files plus `media-mapping.json` (URL → filename); Elementor stores the mapping in a 1-hour transient (`elementor_media_mapping`) |

**Consequence for this kit:** image URLs are absolute and point at a permanent git tag
(`tokens.ASSET_BASE`). On import Elementor downloads each file into the Media Library and
rewrites the template to the local uploads URL. If the host blocks outbound HTTP, the widget
keeps the remote URL (the browser still loads it) but nothing is localised.

## Kit archive layout

The kit's own export writer produces:

| Path | Contents |
| --- | --- |
| `manifest.json` | format version + what is inside |
| `site-settings/<kit_data>` | the design system (the exporter's path is literally `site-settings/` + the kit document's data) |
| `templates/<id>.json` | **WordPress post exports** collected by the Templates runner |
| `content/<post_type>/<id>.json` | **WordPress post exports** collected by the Content runner |

Two runner contracts matter:

* **`Templates` runner** — `should_import()` requires Elementor **Pro**
  (`Utils::has_pro()`), an `include` list containing `templates`, an extracted directory and
  a non-empty `manifest['templates']`. It then walks `templates/<id>.json`.
* **`Elementor_Content` runner** — requires `include` to contain `content`, a non-empty
  `manifest['content']` and an extracted directory; it then walks
  `content/<post_type>/<id>.json` guided by `manifest['content'][ $post_type ]`.

### Why this kit declares empty `templates` / `content`

The kit is a **design system + template library**, not a WordPress post export. It has no
`<id>.json` post files to declare. Declaring `"templates": {}` and `"content": {}` makes both
runners skip cleanly; declaring nothing, or declaring rows whose files do not exist, surfaces
as skipped-file noise (or a partially applied import) with no benefit.

The kit's manifest therefore carries:

```json
{ "manifestVersion": …, "title": "Aurora AI", "description": …,
  "elementorVersion": "3.35.9",
  "site-settings": { … }, "templates": {}, "content": {}, "templateIndex": { … } }
```

`templateIndex` is an **additive** key for humans and docs; Elementor ignores unknown manifest
keys, and the kit's own verifier checks it.

### Site-settings import

* `should_import()` requires `include` to contain `settings` **and** a non-empty
  `site_settings['settings']`.
* The runner reads `$data['site_settings']['settings']`, plus `manifest['title']` and
  `manifest['site-settings']`.
* It merges into the active kit's meta (`PageManager::META_KEY`); `custom_colors` and
  `custom_typography` are **merged, not replaced**, when the manifest flags them true.
* `ALLOWED_SETTINGS` (export side) is the allow-list: theme, globalColors, globalFonts,
  themeStyleSettings, generalSettings, experiments, customCode, customIcons, customFonts,
  classes, variables (+ `defaultStyles` on export). The kit declares a deliberate subset —
  see `03-kit-site-settings.md` §5.
* `manifestVersion` is a constant of the module (`FORMAT_VERSION`) and is version-checked on
  import, so a kit from a much newer Elementor may be refused.

## Troubleshooting map

| Symptom | Cause | Fix |
| --- | --- | --- |
| "No valid templates found" | a kit archive fed to the *Saved Templates* importer (or vice versa) | use the matching screen |
| Import succeeds, nothing appears | you imported the kit (settings only) | import `dist/aurora-ai-templates.zip` first |
| Fewer than 40 templates after import | per-file failures are silent | count *My Templates*; re-import the missing file individually |
| Colours duplicated in Site Settings | custom colours merge, they do not replace | delete the rows you do not want |
| Design system did not apply | `include` had no `settings`, or `site_settings['settings']` was empty | use the kit screen; on old versions apply by hand (`docs/02`) |
| Images missing locally | outbound HTTP blocked | upload `media/*.jpg` manually, or allow `github.com` |
| Pro widgets render nothing | the site is on Elementor Free | expected — see `05-pro-vs-free.md` |

## UNVERIFIED — do not emit

* Exact `manifestVersion` integer values per Elementor release (the constant lives in
  `app/modules/import-export-customization/module.php` and changes between versions). Read it
  from the target site rather than assuming a number.
* The precise JSON shape of `content/<post_type>/<id>.json` post exports — this kit never
  writes them, and the shape was not exercised in this phase. If a future phase adds
  `content/`, read `Import_Runner_Base` / `Elementor_Content` first and state the version.
