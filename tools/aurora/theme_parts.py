"""
Aurora AI - Theme Builder documents: header, footer, single post, archive and popup.

These are Elementor Pro Theme Builder templates (types: header, footer, single,
archive, popup) built from the same widgets and tokens as the pages.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import tokens as tk
from .components import (
    brand_block, contact_line, flexcol, flexrow, flex_item, grid, icon_tile,
    link_column, section_head, surface,
)
from .dsl import (
    Doc, archive_posts, button, container, divider, form, form_field, heading, icon,
    icon_list, image, inner, nav_menu, post_comments, post_content, post_excerpt,
    post_info, post_navigation, section, site_logo, social_icons, spacer, text, widget,
    dims, gap, slider,
)
from . import sections as S

HIDE = {"hide_tablet": "hidden-tablet", "hide_mobile": "hidden-mobile"}
HIDE_MOBILE = {"hide_mobile": "hidden-mobile"}


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

def header(doc: Doc, *, fa: bool = False) -> List[Dict[str, Any]]:
    def L(en: str, fa_text: str) -> str:
        return fa_text if fa else en

    brand = flexrow(doc, [
        widget(doc, "theme-site-logo", {
            "width": slider(46),
            "width_mobile": slider(38),
            "_element_width": "initial",
        }),
        heading(doc, tk.BRAND_FA if fa else tk.BRAND, tag="span",
                global_style=tk.T["fa_label"] if fa else tk.T["h3"],
                color=tk.G["secondary"], letter_spacing=slider(-0.2),
                settings={"_element_width": "initial"}),
    ], gap_value=10, align="center", wrap="nowrap",
        extra={"_element_width": "initial", "flex_gap_mobile": gap(8)})

    menu = nav_menu(
        doc, layout="horizontal", align="center", pointer="underline",
        pointer_color=tk.G["primary"],
        color=tk.G["secondary"], hover_color=tk.G["amber_600"],
        active_color=tk.G["amber_600"],
        style=tk.T["fa_label"] if fa else tk.T["nav"],
        gap=32,
        menu_typography_font_size=slider(16),
        toggle_color=tk.G["secondary"], toggle_size=22, toggle_align="end",
    )
    menu["settings"]["_flex_size"] = "grow"
    menu["settings"]["_flex_grow"] = 1
    menu["settings"]["_flex_shrink"] = 1

    cta = flexrow(doc, [
        button(doc, L("Sign in", "ورود"), "#login", variant="ghost", size="sm"),
        button(doc, L("Book a demo", "درخواست دمو"), "#contact", variant="primary",
               size="sm", hover_animation="grow"),
    ], gap_value=10, align="center", wrap="nowrap",
        extra={**_HIDE_TABLET_MOBILE, "_element_width": "initial"})

    bar = inner(doc, [brand, menu, cta], direction="row", align="center",
                justify="space-between", gap_v=24,
                extra={
                    "boxed_width": slider(tk.W["content"]),
                    "boxed_width_tablet": slider(100, "%"),
                    "boxed_width_mobile": slider(100, "%"),
                    "padding": dims(14, 24), "padding_tablet": dims(12, 20),
                    "padding_mobile": dims(10, 16),
                    "flex_wrap": "nowrap", "flex_gap_mobile": gap(12),
                    "_element_width": "100%",
                })

    announce = inner(doc, [
        flexrow(doc, [
            icon(doc, "fas fa-bolt", view="default", size=12, padding=0, primary=tk.G["primary"]),
            heading(doc, L("Aurora Agents 2.0 is live - evaluations, guardrails and routing.",
                           "آرورا ایجنت ۲.۰ منتشر شد - ارزیابی، محافظ و مسیریابی."),
                    tag="p", global_style=tk.T["fa_label"] if fa else tk.T["text"],
                    color=tk.G["muted_dark"], letter_spacing=slider(0),
                    typography_font_size=slider(14),
                    settings={"_element_width": "initial"}),
            button(doc, L("Read the release", "خواندن خبر"), "#release",
                   variant="link", size="sm", icon="fas fa-arrow-right", icon_align="right",
                   icon_indent=8,
                   button_text_color=tk.G["primary"], hover_color=tk.G["white"],
                   background_color="rgba(255,255,255,0)",
                   background_background="classic",
                   button_background_hover_color="rgba(255,255,255,0)",
                   typography_typography=tk.T["fa_label"] if fa else tk.T["accent"],
                   text_padding=dims(0),
                   **_element_hide_mobile),
        ], gap_value=12, align="center", wrap="nowrap", justify="center"),
    ], direction="row", justify="center", align="center",
        background={"background_background": "classic", "background_color": tk.G["ink_950"]},
        extra={"padding": dims(11, 24), "flex_direction": "row", "flex_wrap": "wrap",
               "flex_wrap_mobile": "wrap"})

    shell = inner(doc, [announce, bar], direction="column",
                  extra={
                      "padding": dims(0),
                      "flex_gap": gap(0),
                      "background_background": "classic",
                      "background_color": tk.G["sand_50"],
                      "border_border": "solid",
                      "border_width": dims(0, 0, 1, 0),
                      "border_color": tk.G["line"],
                      "sticky": "top",
                      "sticky_on": ["desktop", "tablet", "mobile"],
                      "sticky_effects_offset": 60,
                      "_element_width": "100%",
                  },
                  )
    # top level header element
    shell["isInner"] = False
    shell["settings"]["html_tag"] = "header"
    shell["settings"]["content_width"] = "full"
    return [shell]


# responsive-visibility helper values (Elementor "Hide On …" controls)
_element_hide_mobile = {"hide_mobile": "hidden-mobile"}
_HIDE_TABLET_MOBILE = {"hide_tablet": "hidden-tablet", "hide_mobile": "hidden-mobile"}


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

def footer(doc: Doc, *, fa: bool = False) -> List[Dict[str, Any]]:
    def L(en: str, fa_text: str) -> str:
        return fa_text if fa else en

    product_links = [
        {"text": L("Agent builder", "سازنده عامل"), "url": "#"},
        {"text": L("Evaluations", "ارزیابی"), "url": "#"},
        {"text": L("Guardrails", "محافظها"), "url": "#"},
        {"text": L("Integrations", "اتصالها"), "url": "#"},
        {"text": L("Changelog", "تغییرات"), "url": "#"},
    ]
    company_links = [
        {"text": L("About us", "درباره ما"), "url": "#"},
        {"text": L("Case studies", "پروندهها"), "url": "#"},
        {"text": L("Journal", "ژورنال"), "url": "#"},
        {"text": L("Careers", "فرصتهای شغلی"), "url": "#"},
        {"text": L("Contact", "تماس"), "url": "#"},
    ]
    resource_links = [
        {"text": L("Documentation", "مستندات"), "url": "#"},
        {"text": L("API reference", "مرجع API"), "url": "#"},
        {"text": L("Status", "وضعیت سرویس"), "url": "#"},
        {"text": L("Security", "امنیت"), "url": "#"},
    ]

    contact = flexcol(doc, [
        heading(doc, L("Talk to us", "تماس با ما"), tag="h3", global_style=tk.T["eyebrow"],
                color=tk.G["white"], letter_spacing=slider(1.2) if not fa else slider(0)),
        contact_line(doc, "fas fa-envelope", L("Email", "ایمیل"), "hello@aurora.example",
                     "mailto:hello@aurora.example", fa=fa),
        contact_line(doc, "fas fa-phone-alt", L("Phone", "تلفن"), "+31 20 123 4567",
                     "tel:+31201234567", fa=fa),
        contact_line(doc, "fas fa-map-marker-alt", L("Studio", "استودیو"),
                     "Keizersgracht 241, Amsterdam" if not fa else "کیزرزگراخت ۲۴۱، آمستردام",
                     "", fa=fa),
    ], gap_value=18, align="flex-start", **flex_item(4))

    cols = flexrow(doc, [
        flexcol(doc, [
            flexrow(doc, [
                heading(doc, tk.BRAND_FA if fa else tk.BRAND, tag="p",
                        global_style=tk.T["fa_label"] if fa else tk.T["h3"],
                        color=tk.G["white"], letter_spacing=slider(-0.2),
                        settings={"_element_width": "initial"}),
            ], gap_value=0, align="center", wrap="nowrap", extra={"_element_width": "initial"}),
            text(doc, "<p>%s</p>" % L(
                "Warm, human AI infrastructure for product teams. Built in Amsterdam, used "
                "in 14 countries.",
                "زیرساخت هوش مصنوعی گرم و انسانی برای تیمهای محصول. ساختهشده در آمستردام، "
                "مورد استفاده در ۱۴ کشور."),
                 global_style=tk.T["fa_body"] if fa else tk.T["text"],
                 color=tk.G["muted_dark"], typography_font_size=slider(16)),
            social_icons(doc, [
                {"icon": "fab fa-linkedin-in", "url": "#", "library": "fa-brands"},
                {"icon": "fab fa-x-twitter", "url": "#", "library": "fa-brands"},
                {"icon": "fab fa-github", "url": "#", "library": "fa-brands"},
                {"icon": "fab fa-youtube", "url": "#", "library": "fa-brands"},
            ], shape="circle", size="sm", padding=11, spacing=10, icon_size=15,
                icon_primary_color="rgba(255,255,255,0.08)",
                icon_secondary_color=tk.G["white"],
                hover_primary_color=tk.G["primary"],
                hover_secondary_color=tk.G["ink_900"]),
        ], gap_value=20, align="flex-start",
            extra={"flex_direction": "column"}, **flex_item(3, tablet_basis=100)),
        link_column(doc, L("Product", "محصول"), product_links, fa=fa,
                    col_kw=flex_item(4, tablet_basis=46)),
        link_column(doc, L("Company", "شرکت"), company_links, fa=fa,
                    col_kw=flex_item(4, tablet_basis=46)),
        contact,
    ], gap_value=40, align="flex-start", justify="space-between",
        extra={"flex_gap_mobile": gap(32)})

    bottom_left = heading(doc, L("© 2026 Aurora AI BV. All rights reserved.",
                                 "© ۲۰۲۶ آرورا ای آی. تمام حقوق محفوظ است."),
                          tag="p", global_style=tk.T["fa_label"] if fa else tk.T["text"],
                          color=tk.G["muted_dark"], letter_spacing=slider(0),
                          typography_font_size=slider(15),
                          settings={"_element_width": "initial"})
    legal = icon_list(doc, [
        {"text": L("Privacy", "حریم خصوصی"), "icon": "fas fa-minus", "link": "#"},
        {"text": L("Terms", "شرایط"), "icon": "fas fa-minus", "link": "#"},
        {"text": L("Cookies", "کوکیها"), "icon": "fas fa-minus", "link": "#"},
    ], space=0, icon_size=11, icon_color="rgba(244,166,42,0.55)", indent=10,
        text_color=tk.G["muted_dark"],
        style=tk.T["fa_label"] if fa else tk.T["text"],
        typography_font_size=slider(15),
        text_color_hover=tk.G["primary"],
        view="inline",
        extra={"space_between": slider(22)})

    bottom = flexrow(doc, [bottom_left, legal], gap_value=18, align="center",
                     justify="space-between", extra={"flex_gap_mobile": gap(14)})

    inner_col = inner(doc, [
        cols,
        divider(doc, color=tk.G["line_dark"], width=100, weight=1, gap=0,
                _element_width="100%"),
        bottom,
    ], direction="column", gap_v=44,
        extra={"boxed_width": slider(tk.W["content"]),
               "boxed_width_tablet": slider(100, "%"),
               "boxed_width_mobile": slider(100, "%"),
               "padding": dims(80, 24, 32, 24),
               "padding_tablet": dims(64, 24, 28, 24),
               "padding_mobile": dims(52, 20, 24, 20)})

    shell = container(doc, [inner_col], width="full", direction="column",
                      html_tag="footer", gap_v=0,
                      background={"background_background": "classic",
                                  "background_color": tk.G["ink_950"]})
    shell["settings"]["padding"] = dims(0)
    shell["settings"]["padding_tablet"] = dims(0)
    shell["settings"]["padding_mobile"] = dims(0)
    return [shell]


# ---------------------------------------------------------------------------
# Single post (Theme Builder -> Single)
# ---------------------------------------------------------------------------

def single_post(doc: Doc) -> List[Dict[str, Any]]:
    article = inner(doc, [
        widget(doc, "breadcrumbs", {
            "separator": "/", "show_home": "yes", "home_label": "Home",
            "text_color": tk.G["muted"],
            "typography_typography": tk.T["text"], "typography_font_size": slider(14),
        }),
        widget(doc, "post-info", {
            "meta_data": ["author", "date", "comments", "categories"],
            "text_color": tk.G["muted"],
            "typography_typography": tk.T["eyebrow"],
            "typography_font_size": slider(13),
            "typography_text_transform": "uppercase",
            "typography_letter_spacing": slider(1),
        }),
        widget(doc, "theme-post-featured-image", {
            "image_size": "full",
            "image_border_radius": dims(tk.RADIUS["lg"]),
            "_margin": dims(8, 0, 16, 0),
        }),
        post_content(doc, color=tk.G["text"], style=tk.T["text"]),
        divider(doc, color=tk.G["line"], width=100, weight=1, gap=0, _element_width="100%"),
        widget(doc, "author-box", {
            "show_avatar": "yes", "avatar_size": slider(68), "link_to": "posts",
            "name_text_color": tk.G["secondary"],
        }),
        widget(doc, "post-navigation", {
            "show_arrows": "yes", "show_text": "yes",
            "prev_text": "Previous", "next_text": "Next",
        }),
        widget(doc, "post-comments", {}),
    ], direction="column", gap_v=26,
        extra={"boxed_width": slider(820), "boxed_width_tablet": slider(100, "%"),
               "boxed_width_mobile": slider(100, "%"),
               "padding": dims(72, 24, 72, 24),
               "padding_tablet": dims(56, 24), "padding_mobile": dims(40, 20)})

    shell = container(doc, [article], width="full", direction="column",
                      html_tag="main", gap_v=0, background=S.BG_PAGE)
    shell["settings"]["padding"] = dims(0)
    shell["settings"]["padding_mobile"] = dims(0)
    return [shell, S.cta_band(doc)]


# ---------------------------------------------------------------------------
# Archive (Theme Builder -> Archive)
# ---------------------------------------------------------------------------

def archive(doc: Doc) -> List[Dict[str, Any]]:
    hero = S._band(doc, [
        widget(doc, "theme-archive-title", {
            "header_size": "h1", "title_color": tk.G["secondary"], "align": "left",
            "typography_typography": tk.T["display"],
            "typography_font_size": slider(48),
            "typography_font_size_mobile": slider(32),
        }),
        text(doc, "<p>Engineering notes, evaluation patterns and release write-ups from the "
                  "team building Aurora.</p>",
             global_style=tk.T["lead"], color=tk.G["text"]),
    ], bg=S.BG_GRADIENT_HERO, pad_y=(72, 56, 40))

    listing = S._band(doc, [
        widget(doc, "archive-posts", archive_posts(
            doc, skin="cards", per_page=9, pagination="numbers",
            card_bg=tk.G["white"], border_color=tk.G["line"], radius=20,
            title_color=tk.G["secondary"], text_color=tk.G["text"],
            meta_color=tk.G["muted"])["settings"] | {"_element_width": "100%"}),
    ], bg=S.BG_PAGE, element_id="archive-list")

    return [hero, listing, S.newsletter_band(doc), S.cta_band(doc)]


# ---------------------------------------------------------------------------
# Search results (Theme Builder -> Search Results)
# ---------------------------------------------------------------------------

def search_results(doc: Doc) -> List[Dict[str, Any]]:
    hero = S._band(doc, [
        heading(doc, "Search results", tag="h1", global_style=tk.T["h2"],
                color=tk.G["secondary"], align="left"),
        text(doc, "<p>Everything on aurora.example that matches your query.</p>",
             global_style=tk.T["lead"], color=tk.G["text"]),
        widget(doc, "search-form", {"skin": "classic", "placeholder": "Search the site…",
                                    "button_type": "text", "input_size": "md"}),
    ], bg=S.BG_GRADIENT_HERO, pad_y=(72, 56, 40))
    listing = S._band(doc, [
        widget(doc, "archive-posts", archive_posts(
            doc, skin="cards", per_page=9, pagination="numbers",
            card_bg=tk.G["white"], border_color=tk.G["line"], radius=20,
            title_color=tk.G["secondary"], text_color=tk.G["text"],
            meta_color=tk.G["muted"])["settings"] | {"_element_width": "100%"}),
    ], bg=S.BG_PAGE)
    return [hero, listing, S.cta_band(doc)]


# ---------------------------------------------------------------------------
# Popup - lead magnet (Theme Builder -> Popup)
# ---------------------------------------------------------------------------

def popup(doc: Doc) -> List[Dict[str, Any]]:
    form_widget = form(
        doc, [
            form_field("email", "Work email", kind="email",
                       placeholder="name@company.com", required=True, width="100"),
        ],
        button_text="Send me the checklist", form_name="Aurora AI readiness checklist",
        email_to="hello@aurora.example", email_subject="AI readiness checklist request",
        success_message="Check your inbox - the checklist is on its way.",
        button_align="center", button_size="lg", button_width="100",
        label_color=tk.G["secondary"], field_text_color=tk.G["secondary"],
        field_bg=tk.G["white"], field_border_color=tk.G["line"], radius=12,
        _element_width="100%",
    )
    card = surface(doc, [
        flexrow(doc, [
            icon_tile(doc, "fas fa-clipboard-check", size=20, padding=14),
            heading(doc, "Free checklist", tag="p", global_style=tk.T["eyebrow"],
                    color=tk.G["amber_600"], letter_spacing=slider(1.2),
                    settings={"_element_width": "initial"}),
        ], gap_value=12, align="center", wrap="nowrap"),
        heading(doc, "Is your product ready for AI?", tag="h2", global_style=tk.T["h2"],
                color=tk.G["secondary"], font_size=slider(34), font_size_mobile=slider(26)),
        text(doc, "<p>The 18-point readiness checklist we run with every new client, in a "
                  "single PDF. No webinar, no follow-up sequence.</p>",
             global_style=tk.T["lead"], color=tk.G["text"]),
        form_widget,
        text(doc, "<p>We store your email only to send the checklist. Unsubscribe any time.</p>",
             global_style=tk.T["text"], color=tk.G["muted"], align="center",
             typography_font_size=slider(13)),
    ], kind="card", pad=40, pad_mobile=26, gap_v=20, shadow="xl", radius=tk.RADIUS["xl"],
        extra={"flex_direction": "column"})
    card["settings"].update(flex_item(0, basis=100, grow=0)["flex_item"])

    shell = section(doc, [
        inner(doc, [card], direction="column", align="center", justify="center"),
    ], background={"background_background": "classic",
                   "background_color": "rgba(20,17,16,0.82)"},
        pad_y=(40, 40, 24), pad_x=(24, 20, 16), html_tag="section")
    return [shell]


POPUP_SETTINGS = {
    "popup_type": "exit_intent",
    "popup_entrance_animation": "fadeInUp",
    "popup_exit_animation": "fadeOutDown",
    "popup_entrance_animation_duration": {"unit": "px", "size": 0.4},
    "prevent_scroll": "yes",
    "close_button": "yes",
    "close_button_position": "outside",
    "close_button_delay": 300,
    "overlay_background_background": "classic",
    "overlay_background_color": "rgba(20,17,16,0.8)",
    "page_load_delay": 0,
    "exit_intent_behavior": "show",
    "avoid_multiple_popups": "yes",
    "popup_conditions": [],
}
