# Alt-text sample — first 10 drafts for approval (gate 2)

Measured state (corrected 2026-10-12, P1.6): **24 image widgets across 39 documents; all 24 carry
alt text at `settings.image.alt`** (13 distinct strings). P3 measured `settings.alt`, which is
always empty - the presence claim was wrong. Re-measured in P1.7 with
`tools/alt_quality_check.py`: 24 non-empty, 13 distinct, nine instances (three distinct strings)
carry a client-name-only alt, 0 decorative/generic/locale findings. The drafts below are therefore a
**quality upgrade proposal**, not a fix for missing text. Rule from `docs/08-agent-legibility.md` §4: per instance, descriptive,
≤125 characters, EN/FA paired, decorative stays empty.

The ten drafts below cover all seven files plus the logo and the decorative case. Approve or edit
these ten; the remaining ~14 instances follow the same pattern per context and are batched after
gate 2.

| # | file | document · section | EN alt (draft) | FA alt (draft) | type |
| ---: | --- | --- | --- | --- | --- |
| 1 | `hero-dashboard.jpg` | home EN · `#hero` | Aurora's agent console: a run list beside a live status panel with three active agents. | کنسول عاملهای آرورا: فهرست اجراها کنار پنل وضعیت زنده با سه عامل فعال. | informative |
| 2 | `hero-dashboard.jpg` | home FA · `#hero` | Aurora's agent console, Persian interface: a run list beside a live status panel. | کنسول عاملهای آرورا با رابط فارسی: فهرست اجراها کنار پنل وضعیت زنده. | informative |
| 3 | `highlight-agents.jpg` | home EN · `#how` | A pipeline view: three agents handing a task to each other, each with a success badge. | نمای خط تولید: سه عامل که یک کار را به هم میسپارند، هرکدام با نشان موفقیت. | informative |
| 4 | `highlight-insights.jpg` | home EN · `#how` | An insights panel charting task outcomes over one week, with two annotations. | پنل بینشها با نمودار نتایج کارها در یک هفته و دو یادداشت. | informative |
| 5 | `highlight-agents.jpg` | home FA · `#how` | A pipeline view, Persian labels: three agents passing a task along a chain. | نمای خط تولید با برچسبهای فارسی: سه عامل که یک کار را زنجیرهای پیش میبرند. | informative |
| 6 | `case-retail.jpg` | home EN · `#portfolio` and `/work/` | Retail case study: a storefront operations dashboard showing order volume. | مطالعه موردی خردهفروشی: داشبورد عملیات فروشگاه با نمایش حجم سفارشها. | informative |
| 7 | `case-fintech.jpg` | home EN · `#portfolio` and `/work/` | Fintech case study: a risk-review queue with three flagged transactions. | مطالعه موردی فینتک: صف بازبینی ریسک با سه تراکنش نشانهگذاریشده. | informative |
| 8 | `case-health.jpg` | home EN · `#portfolio` and `/work/` | Health case study: a scheduling view with patient slots and an intake summary. | مطالعه موردی سلامت: نمای زمانبندی با نوبتهای بیماران و خلاصه پذیرش. | informative |
| 9 | `about-studio.jpg` | about · `#story` | The Aurora studio: a shared desk with two monitors and a whiteboard of flow diagrams. | استودیوی آرورا: میز مشترک با دو نمایشگر و وایتبردی از نمودارهای جریان. | informative |
| 10 | site logo (`theme-site-logo`) / any decorative divider | header, footer | `alt="Aurora AI"` for the logo; **`alt=""`** for decorative rules and background images | `alt="آرورا"` برای لوگو؛ **`alt=""`** برای جداکنندهها و تصاویر پسزمینه | logo / decorative |

Two review notes for gate 2:

- Drafts 2, 5 and 9 are Persian: they need a native read-through at gate 4, not just an approval
  click — alt text is copy, and `tools/bidi_check.py` only guarantees the encoding, not the prose.
- The same file gets different alt text per context (1 vs 2, 3 vs 5): that is the rule, not an
  inconsistency. A single alt string reused across contexts is the defect this policy exists to
  prevent.
