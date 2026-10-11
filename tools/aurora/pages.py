"""
Aurora AI - full page compositions.

Each function returns (Doc, page_settings) ready to be serialised as an
Elementor template JSON with type = "page".
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from . import tokens as tk
from .components import (
    arrow_link, flexcol, flexrow, flex_item, grid, icon_card, icon_tile, section_head,
    stat_block, surface, tag_pill,
)
from .dsl import (
    Doc, button, divider, heading, icon, icon_box, icon_list, image, inner, posts,
    section, spacer, text, widget, dims, gap, slider,
)
from . import sections as S


def page_settings(*, full_width: bool = True, hide_title: bool = True,
                  extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if full_width:
        out["template"] = "elementor_header_footer"
    if hide_title:
        out["hide_title"] = "yes"
    out.update(extra or {})
    return out


# ---------------------------------------------------------------------------
# Home (EN)
# ---------------------------------------------------------------------------

def home(doc: Doc) -> List[Dict[str, Any]]:
    return [
        S.hero_split(doc),
        S.logo_cloud(doc),
        S.feature_grid(doc),
        S.feature_zigzag(doc),
        S.stats_band(doc),
        S.capability_cards(doc),
        S.process_steps(doc),
        S.case_studies(doc),
        S.testimonials(doc),
        S.pricing_table(doc),
        S.faq_accordion(doc),
        S.newsletter_band(doc),
        S.cta_band(doc),
    ]


# ---------------------------------------------------------------------------
# Home (FA / RTL)
# ---------------------------------------------------------------------------

def home_fa(doc: Doc) -> List[Dict[str, Any]]:
    return [
        S.hero_split(doc, fa=True),
        S.logo_cloud(doc, fa=True),
        S.feature_grid(doc, fa=True, eyebrow="چرا آرورا",
                       title="همهچیز برای ساخت هوش مصنوعی قابل اعتماد",
                       lead="یک پلتفرم یکپارچه از ایده تا انتشار - بدون نیاز به چسباندن "
                            "پنج سرویس جداگانه."),
        S.stats_band(doc, fa=True),
        S.capability_cards(doc, fa=True),
        S.feature_zigzag(doc, fa=True),
        S.process_steps(doc, fa=True),
        S.case_studies(doc, fa=True),
        S.testimonials(doc, fa=True),
        S.pricing_table(doc, fa=True),
        S.faq_accordion(doc, fa=True),
        S.newsletter_band(doc, fa=True),
        S.cta_band(doc, fa=True),
    ]


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

def about(doc: Doc) -> List[Dict[str, Any]]:
    values = [
        ("fas fa-handshake", "Warm by default", "Software about people should feel human, "
         "so we write like people and design for calm."),
        ("fas fa-microscope", "Evidence over hype", "Every claim in our product is backed by "
         "an evaluation you can run yourself."),
        ("fas fa-seedling", "Built to last", "Bootstrapped, profitable and independent - we "
         "answer to customers, not to a board."),
    ]
    value_cards = [
        icon_card(doc, icon_value=i, title=t, body=b, delay=n * 100)
        for n, (i, t, b) in enumerate(values)
    ]
    for c in value_cards:
        c["settings"].update(flex_item(3)["flex_item"])

    headline = S._band(doc, [
        section_head(doc, eyebrow="About Aurora", title="We build the calm layer for AI teams",
                     lead="Fourteen people, one product and a stubborn belief that AI tooling "
                          "should feel as considered as the design tools we grew up on."),
        grid(doc, value_cards, gap_value=26),
    ], bg=S.BG_WHITE, element_id="values")

    return [
        S.page_hero(doc, eyebrow="About us",
                    title="A small team building serious infrastructure",
                    lead="Aurora is made in Amsterdam by engineers who spent a decade shipping "
                         "ML to production and wanted better tools."),
        S.content_two_column(doc),
        S.stats_band(doc),
        headline,
        S.team_grid(doc),
        S.testimonials(doc),
        S.cta_band(doc),
    ]


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def services(doc: Doc) -> List[Dict[str, Any]]:
    eng = [
        ("fas fa-sitemap", "AI strategy & opportunity mapping",
         "We score every candidate use case on data readiness, payback and risk, then agree "
         "on the two worth building.", ["2-week discovery", "Prioritised backlog", "ROI model"]),
        ("fas fa-code", "Agent engineering",
         "Production-grade agents built with your stack, your guardrails and your review "
         "process - handed over with tests.", ["Reference implementation", "Evaluation suite", "Handover workshop"]),
        ("fas fa-gauge-high", "Performance & cost tuning",
         "Prompt compression, semantic caching and model routing that cut unit cost without "
         "touching answer quality.", ["Cost baseline", "Routing policy", "Monthly report"]),
    ]
    cards = []
    for n, (i, t, b, bullets) in enumerate(eng):
        cards.append(S.bullet_card(doc, icon_value=i, title=t, body=b, bullets=bullets,
                                   link_url="#contact", link_text="Scope this engagement",
                                   delay=n * 100, col_kw=flex_item(3)))

    engagements = S._band(doc, [
        section_head(doc, eyebrow="Engagements",
                     title="Three ways to work with us",
                     lead="Pick the shape that matches your stage - every engagement ends with "
                          "your team able to run it alone."),
        grid(doc, cards, gap_value=26),
    ], bg=S.BG_PAGE, element_id="engagements")

    comparison = S._band(doc, [
        section_head(doc, eyebrow="Deliverables", title="What you get in every engagement",
                     lead="The same artefacts, whether we build one agent or twelve."),
        grid(doc, [
            surface(doc, [
                icon(doc, "fas fa-file-signature", view="default", size=20, padding=0,
                     primary=tk.G["primary"]),
                heading(doc, "Architecture decision record", tag="h3",
                        global_style=tk.T["h3"], color=tk.G["secondary"]),
                text(doc, "<p>Every meaningful choice documented, with the trade-offs we "
                          "rejected and why.</p>", global_style=tk.T["text"],
                     color=tk.G["text"]),
            ], kind="card", pad=28, gap_v=14,
                extra={"flex_direction": "column"}, **flex_item(3)),
            surface(doc, [
                icon(doc, "fas fa-vial", view="default", size=20, padding=0,
                     primary=tk.G["primary"]),
                heading(doc, "Evaluation harness", tag="h3",
                        global_style=tk.T["h3"], color=tk.G["secondary"]),
                text(doc, "<p>A runnable golden set wired into your CI so quality cannot "
                          "silently regress.</p>", global_style=tk.T["text"],
                     color=tk.G["text"]),
            ], kind="card", pad=28, gap_v=14,
                extra={"flex_direction": "column"}, **flex_item(3)),
            surface(doc, [
                icon(doc, "fas fa-graduation-cap", view="default", size=20, padding=0,
                     primary=tk.G["primary"]),
                heading(doc, "Enablement sessions", tag="h3",
                        global_style=tk.T["h3"], color=tk.G["secondary"]),
                text(doc, "<p>Two hands-on workshops so your engineers own the agent after "
                          "we leave.</p>", global_style=tk.T["text"],
                     color=tk.G["text"]),
            ], kind="card", pad=28, gap_v=14,
                extra={"flex_direction": "column"}, **flex_item(3)),
        ], gap_value=26),
    ], bg=S.BG_WHITE, element_id="deliverables")

    return [
        S.page_hero(doc, eyebrow="Services",
                    title="AI services built around production, not demos",
                    lead="Strategy, engineering and optimisation delivered by the people who "
                         "wrote the platform."),
        S.capability_cards(doc, eyebrow="Capabilities", title="What we build",
                           lead="From customer-facing agents to internal research copilots."),
        engagements,
        comparison,
        S.process_steps(doc),
        S.faq_accordion(doc),
        S.cta_band(doc),
    ]


# ---------------------------------------------------------------------------
# Portfolio
# ---------------------------------------------------------------------------

def portfolio(doc: Doc) -> List[Dict[str, Any]]:
    extra_rows = [
        ("Lumen Logistics", "Routing assistant", "−27% empty kilometres",
         "A dispatcher copilot that reads load notes in five languages."),
        ("Orbital Media", "Editorial research", "6× faster desk research",
         "Writers query a grounded archive instead of hunting through folders."),
        ("Fieldnote Legal", "Contract review", "1,400 hours saved per year",
         "Clause extraction with a citation for every flag raised."),
    ]
    rows = []
    for i, (client, scope, metric, blurb) in enumerate(extra_rows):
        rows.append(surface(doc, [
            heading(doc, "%02d" % (i + 4), tag="span", global_style=tk.T["eyebrow"],
                    color=tk.G["muted"], letter_spacing=slider(0.8),
                    settings={"_element_width": "initial"}),
            flexcol(doc, [
                heading(doc, client, tag="h3", global_style=tk.T["h3"],
                        color=tk.G["secondary"]),
                text(doc, "<p>%s</p>" % blurb, global_style=tk.T["text"],
                     color=tk.G["text"], typography_font_size=slider(16)),
            ], gap_value=6, **flex_item(0, basis=52, tablet_basis=100, mobile_basis=100, grow=1)),
            flexcol(doc, [
                heading(doc, scope, tag="p", global_style=tk.T["eyebrow"],
                        color=tk.G["amber_600"], letter_spacing=slider(1),
                        typography_font_size=slider(12)),
                heading(doc, metric, tag="p", global_style=tk.T["h3"],
                        color=tk.G["accent"], letter_spacing=slider(-0.3)),
            ], gap_value=4, **flex_item(0, basis=40, tablet_basis=100, mobile_basis=100, grow=1)),
        ], kind="card", pad=26, gap_v=20, hover=True,
            extra={"flex_direction": "row", "flex_wrap": "wrap"},
            animation="fadeInUp", animation_delay=i * 90,
            **flex_item(1, basis=100, tablet_basis=100, mobile_basis=100, grow=0)))

    more = S._band(doc, [
        section_head(doc, eyebrow="More work", title="Selected engagements",
                     lead="A sample of the rollouts we can talk about publicly."),
        flexcol(doc, rows, gap_value=16),
    ], bg=S.BG_PAGE, element_id="more-work")

    return [
        S.page_hero(doc, eyebrow="Case studies",
                    title="Work measured in production, not in slide decks",
                    lead="Every engagement below shipped, and every metric was measured by the "
                         "client's own analytics."),
        S.case_studies(doc),
        more,
        S.testimonials(doc, dark=True),
        S.cta_band(doc),
    ]


# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------

def pricing(doc: Doc) -> List[Dict[str, Any]]:
    compare = [
        ("Active projects", "1", "10", "Unlimited"),
        ("Model calls / month", "50k", "2M", "Custom"),
        ("Evaluation suite", "—", "Included", "Advanced"),
        ("Guardrails & PII redaction", "—", "Included", "Custom policies"),
        ("Regional data residency", "—", "EU / US", "Your VPC"),
        ("Support SLA", "Community", "4 hours", "1 hour"),
    ]
    head_cells = []
    for label, col in [("", 46), ("Starter", 18), ("Growth", 18), ("Enterprise", 18)]:
        head_cells.append(inner(doc, [
            heading(doc, label, tag="p", global_style=tk.T["eyebrow"],
                    color=tk.G["muted"], letter_spacing=slider(0.8),
                    settings={"_element_width": "initial"}),
        ], direction="row", extra={}, **flex_item(0, basis=col, tablet_basis=col,
                                                  mobile_basis=col, grow=0)))
    table_rows = [inner(doc, head_cells, direction="row", align="center",
                        extra={"flex_wrap": "nowrap", "_element_width": "100%"})]

    for label, *vals in compare:
        cells = [inner(doc, [
            heading(doc, label, tag="p", global_style=tk.T["text"],
                    color=tk.G["secondary"],
                    settings={"_element_width": "100%"}),
        ], direction="row", extra={}, **flex_item(0, basis=46, tablet_basis=46,
                                                  mobile_basis=46, grow=0))]
        for v in vals:
            cells.append(inner(doc, [
                heading(doc, v, tag="p", global_style=tk.T["text"],
                        color=tk.G["text"] if v in ("—",) else tk.G["secondary"],
                        settings={"_element_width": "100%"}),
            ], direction="row", justify="center", extra={},
                **flex_item(0, basis=18, tablet_basis=18, mobile_basis=18, grow=0)))
        table_rows.append(divider(doc, color=tk.G["line"], width=100, weight=1, gap=0,
                                  _element_width="100%"))
        table_rows.append(inner(doc, cells, direction="row", align="center",
                                extra={"flex_wrap": "nowrap", "_element_width": "100%"}))

    compare_section = S._band(doc, [
        section_head(doc, eyebrow="Compare plans", title="Every capability, side by side",
                     lead="Scroll the table or ask us for a detailed comparison sheet."),
        surface(doc, table_rows, kind="card", pad=28, pad_mobile=18, gap_v=0,
                extra={"flex_direction": "column", "overflow": "auto"}),
    ], bg=S.BG_WHITE, element_id="compare")

    return [
        S.page_hero(doc, eyebrow="Pricing",
                    title="Pricing that scales with the value you ship",
                    lead="Start free, upgrade when your agent starts carrying real traffic."),
        S.pricing_table(doc),
        compare_section,
        S.faq_accordion(doc),
        S.testimonials(doc),
        S.cta_band(doc),
    ]


# ---------------------------------------------------------------------------
# Blog index
# ---------------------------------------------------------------------------

def blog(doc: Doc) -> List[Dict[str, Any]]:
    grid_widget = posts(
        doc, per_page=6, columns=3, columns_tablet=2, columns_mobile=1,
        excerpt_length=20, pagination="numbers", read_more_text="Read article",
        image_size="medium_large", title_color=tk.G["secondary"],
        text_color=tk.G["text"], meta_color=tk.G["muted"],
        card_bg_color=tk.G["white"], card_border_color=tk.G["line"],
        radius=20,
        _element_width="100%",
    )
    archive_block = S._band(doc, [
        section_head(doc, eyebrow="Journal", title="Notes from the build team",
                     lead="Engineering deep dives, evaluation patterns and release write-ups."),
        grid_widget,
    ], bg=S.BG_PAGE, element_id="posts")
    return [
        S.page_hero(doc, eyebrow="Journal",
                    title="Writing from the team building Aurora",
                    lead="Practical notes on agents, evaluation and shipping AI that survives "
                         "contact with real users."),
        archive_block,
        S.newsletter_band(doc),
    ]


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

def contact(doc: Doc) -> List[Dict[str, Any]]:
    return [
        S.page_hero(doc, eyebrow="Contact", title="Tell us what you want to build",
                    lead="A short brief is enough. You will hear from an engineer, not a "
                         "call centre, within one business day."),
        S.contact_section(doc),
        S.faq_accordion(doc, dark=True),
        S.cta_band(doc),
    ]


# ---------------------------------------------------------------------------
# 404
# ---------------------------------------------------------------------------

def not_found(doc: Doc) -> List[Dict[str, Any]]:
    card = surface(doc, [
        flexcol(doc, [
            inner(doc, [
                icon(doc, "fas fa-compass", view="default", size=30, padding=0,
                     primary=tk.G["amber_600"]),
            ], direction="row", align="center", justify="center",
                background={"background_background": "classic",
                            "background_color": tk.G["amber_100"]},
                radius=tk.RADIUS["pill"],
                extra={"padding": dims(22), "flex_direction": "row",
                       "_element_width": "initial", "_element_custom_width": slider(88)}),
            heading(doc, "404", tag="p", global_style=tk.T["eyebrow"],
                    color=tk.G["amber_600"], letter_spacing=slider(3), align="center"),
            heading(doc, "This page took an unplanned detour", tag="h1",
                    global_style=tk.T["h2"], color=tk.G["secondary"], align="center",
                    font_size=slider(48), font_size_mobile=slider(30)),
            text(doc, "<p>The link may be outdated, or the page has moved somewhere more "
                      "sensible. Try one of these instead.</p>",
                 global_style=tk.T["lead"], color=tk.G["text"], align="center"),
            flexrow(doc, [
                button(doc, "Back to homepage", "/", variant="primary", size="lg",
                       icon="fas fa-arrow-right", icon_align="right"),
                button(doc, "Browse case studies", "/portfolio/", variant="outline", size="lg"),
            ], gap_value=14, align="center", justify="center"),
            divider(doc, color=tk.G["line"], width=100, weight=1, gap=0, _element_width="100%"),
            icon_list(doc, [
                {"text": "Read the journal", "icon": "fas fa-arrow-right", "link": "/blog/"},
                {"text": "See pricing", "icon": "fas fa-arrow-right", "link": "/pricing/"},
                {"text": "Contact the team", "icon": "fas fa-arrow-right", "link": "/contact/"},
            ], space=12, icon_size=13, icon_color=tk.G["amber_600"],
                text_color=tk.G["secondary"], style=tk.T["text"],
                typography_font_size=slider(16)),
        ], gap_value=22, align="center", extra={"flex_direction": "column"}),
    ], kind="card", pad=56, pad_mobile=30, gap_v=0, shadow="md")

    row = flexrow(doc, [card], gap_value=0, justify="center")
    card["settings"].update(flex_item(0, basis=62, tablet_basis=90, mobile_basis=100, grow=0))
    return [
        section(doc, [inner(doc, [row], direction="column", align="center")],
                background=S.BG_GRADIENT_HERO, pad_y=(120, 88, 64), html_tag="section",
                element_id="error-404"),
    ]
