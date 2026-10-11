"""
Aurora AI - Elementor Design System tokens.

Everything the kit emits (kit site-settings, global colors, global fonts,
spacing, radius, shadows, image URLs) is derived from this single module so the
whole template set stays consistent and re-brandable from one place.

Verified against Elementor source:
  core/kits/documents/tabs/global-colors.php   -> repeater field names (_id/title/color)
  core/kits/documents/tabs/global-typography.php -> system_typography / custom_typography
  core/kits/documents/tabs/theme-style-*.php   -> button / image / form field keys
  core/kits/documents/tabs/settings-layout.php -> container_width / container_padding /
                                                  space_between_widgets / active_breakpoints
"""

# ---------------------------------------------------------------------------
# Brand identity
# ---------------------------------------------------------------------------

BRAND = "Aurora AI"
BRAND_FA = "آرورا"
TAGLINE = "Warm, human AI infrastructure for product teams."

KIT_TITLE = "Aurora AI - Elementor Template Kit"
KIT_VERSION = "1.0.0"

# Release assets host every image. Change ASSET_BASE and re-run `tools/build.py`
# to point the kit at your own CDN / uploads folder.
GITHUB_USER = "omidoraei"
GITHUB_REPO = "ai_website_wordpress"
ASSET_TAG = "v1.0.0"
ASSET_BASE = (
    "https://github.com/%s/%s/releases/download/%s" % (GITHUB_USER, GITHUB_REPO, ASSET_TAG)
)

# ---------------------------------------------------------------------------
# Global Colors  (Elementor > Site Settings > Global Colors)
# ---------------------------------------------------------------------------

# System colors use the four fixed Elementor ids: primary / secondary / text / accent
SYSTEM_COLORS = [
    {"_id": "primary", "title": "Primary / Amber", "color": "#F4A62A"},
    {"_id": "secondary", "title": "Secondary / Ink", "color": "#1C1917"},
    {"_id": "text", "title": "Text / Stone", "color": "#57534E"},
    {"_id": "accent", "title": "Accent / Coral", "color": "#EF6C4D"},
]

# Custom colors extend the palette with the neutrals and tints the layout needs.
CUSTOM_COLORS = [
    {"_id": "ink-950", "title": "Ink 950", "color": "#141110"},
    {"_id": "ink-900", "title": "Ink 900", "color": "#1C1917"},
    {"_id": "ink-800", "title": "Ink 800", "color": "#292524"},
    {"_id": "amber-600", "title": "Amber 600", "color": "#D98A14"},
    {"_id": "amber-100", "title": "Amber 100", "color": "#FDF0DA"},
    {"_id": "coral-600", "title": "Coral 600", "color": "#D8553A"},
    {"_id": "coral-100", "title": "Coral 100", "color": "#FDECE7"},
    {"_id": "sand-50", "title": "Sand 50 / Page", "color": "#FFFBF5"},
    {"_id": "sand-100", "title": "Sand 100 / Surface", "color": "#FAF4EA"},
    {"_id": "sand-200", "title": "Sand 200 / Sunken", "color": "#F3E9DB"},
    {"_id": "line", "title": "Border", "color": "#E8DCCC"},
    {"_id": "muted", "title": "Muted Text", "color": "#8C8177"},
    {"_id": "muted-dark", "title": "Muted Text (on dark)", "color": "#A8A29E"},
    {"_id": "white", "title": "White", "color": "#FFFFFF"},
    {"_id": "success", "title": "Success", "color": "#2F9E6B"},
]

# Direct hex values (used for things Elementor cannot bind to a global, such as
# gradient stops, overlay colours and CSS filter values).
C = {
    "primary": "#F4A62A",
    "primary_hover": "#D98A14",
    "secondary": "#1C1917",
    "text": "#57534E",
    "accent": "#EF6C4D",
    "accent_hover": "#D8553A",
    "ink_950": "#141110",
    "ink_900": "#1C1917",
    "ink_800": "#292524",
    "amber_600": "#D98A14",
    "amber_100": "#FDF0DA",
    "coral_600": "#D8553A",
    "coral_100": "#FDECE7",
    "sand_50": "#FFFBF5",
    "sand_100": "#FAF4EA",
    "sand_200": "#F3E9DB",
    "line": "#E8DCCC",
    "line_dark": "rgba(255,255,255,0.12)",
    "muted": "#8C8177",
    "muted_dark": "#A8A29E",
    "white": "#FFFFFF",
    "success": "#2F9E6B",
}

# Shortcut references so widgets always use Global Colors instead of raw hex.
G = {
    "primary": "globals/colors?id=primary",
    "secondary": "globals/colors?id=secondary",
    "text": "globals/colors?id=text",
    "accent": "globals/colors?id=accent",
    "ink_950": "globals/colors?id=ink-950",
    "ink_900": "globals/colors?id=ink-900",
    "ink_800": "globals/colors?id=ink-800",
    "amber_600": "globals/colors?id=amber-600",
    "amber_100": "globals/colors?id=amber-100",
    "coral_600": "globals/colors?id=coral-600",
    "coral_100": "globals/colors?id=coral-100",
    "sand_50": "globals/colors?id=sand-50",
    "sand_100": "globals/colors?id=sand-100",
    "sand_200": "globals/colors?id=sand-200",
    "line": "globals/colors?id=line",
    "muted": "globals/colors?id=muted",
    "muted_dark": "globals/colors?id=muted-dark",
    # translucent overlays cannot be bound to a global solid colour
    "line_dark": "rgba(255,255,255,0.12)",
    "white": "globals/colors?id=white",
    "success": "globals/colors?id=success",
}

# ---------------------------------------------------------------------------
# Global Fonts  (Elementor > Site Settings > Global Fonts)
# ---------------------------------------------------------------------------

F_HEADING = "Sora"
F_BODY = "Inter"
F_FA = "Arad"          # Iranian typeface; upload via Elementor > Custom Fonts
F_FA_FALLBACK = "IRANSansX"

# System + custom typography. Each entry is a repeater row of the
# `system_typography` / `custom_typography` controls.
#   typography_*            -> Group_Control_Typography named "typography"
SYSTEM_TYPOGRAPHY = [
    {
        "_id": "primary",
        "title": "Primary / Headings",
        "typography_typography": "custom",
        "typography_font_family": F_HEADING,
        "typography_font_weight": "600",
        "typography_font_size": {"unit": "px", "size": 42},
        "typography_font_size_tablet": {"unit": "px", "size": 34},
        "typography_font_size_mobile": {"unit": "px", "size": 28},
        "typography_line_height": {"unit": "em", "size": 1.15},
        "typography_letter_spacing": {"unit": "px", "size": -0.6},
    },
    {
        "_id": "secondary",
        "title": "Secondary / Subheadings",
        "typography_typography": "custom",
        "typography_font_family": F_BODY,
        "typography_font_weight": "600",
        "typography_font_size": {"unit": "px", "size": 20},
        "typography_line_height": {"unit": "em", "size": 1.45},
        "typography_letter_spacing": {"unit": "px", "size": -0.1},
    },
    {
        "_id": "text",
        "title": "Text / Body",
        "typography_typography": "custom",
        "typography_font_family": F_BODY,
        "typography_font_weight": "400",
        "typography_font_size": {"unit": "px", "size": 17},
        "typography_font_size_mobile": {"unit": "px", "size": 16},
        "typography_line_height": {"unit": "em", "size": 1.75},
        "typography_letter_spacing": {"unit": "px", "size": 0},
    },
    {
        "_id": "accent",
        "title": "Accent / Buttons & Labels",
        "typography_typography": "custom",
        "typography_font_family": F_HEADING,
        "typography_font_weight": "600",
        "typography_font_size": {"unit": "px", "size": 15},
        "typography_line_height": {"unit": "em", "size": 1.2},
        "typography_letter_spacing": {"unit": "px", "size": 0.2},
    },
]

CUSTOM_TYPOGRAPHY = [
    {
        "_id": "display",
        "title": "Display / Hero H1",
        "typography_typography": "custom",
        "typography_font_family": F_HEADING,
        "typography_font_weight": "700",
        "typography_font_size": {"unit": "px", "size": 64},
        "typography_font_size_tablet": {"unit": "px", "size": 48},
        "typography_font_size_mobile": {"unit": "px", "size": 36},
        "typography_line_height": {"unit": "em", "size": 1.06},
        "typography_letter_spacing": {"unit": "px", "size": -1.6},
    },
    {
        "_id": "h2",
        "title": "Section Heading / H2",
        "typography_typography": "custom",
        "typography_font_family": F_HEADING,
        "typography_font_weight": "700",
        "typography_font_size": {"unit": "px", "size": 46},
        "typography_font_size_tablet": {"unit": "px", "size": 36},
        "typography_font_size_mobile": {"unit": "px", "size": 28},
        "typography_line_height": {"unit": "em", "size": 1.12},
        "typography_letter_spacing": {"unit": "px", "size": -1},
    },
    {
        "_id": "h3",
        "title": "Card Title / H3",
        "typography_typography": "custom",
        "typography_font_family": F_HEADING,
        "typography_font_weight": "600",
        "typography_font_size": {"unit": "px", "size": 22},
        "typography_font_size_mobile": {"unit": "px", "size": 20},
        "typography_line_height": {"unit": "em", "size": 1.3},
        "typography_letter_spacing": {"unit": "px", "size": -0.3},
    },
    {
        "_id": "eyebrow",
        "title": "Eyebrow / Overline",
        "typography_typography": "custom",
        "typography_font_family": F_BODY,
        "typography_font_weight": "700",
        "typography_font_size": {"unit": "px", "size": 13},
        "typography_line_height": {"unit": "em", "size": 1.3},
        "typography_letter_spacing": {"unit": "px", "size": 1.6},
        "typography_text_transform": "uppercase",
    },
    {
        "_id": "lead",
        "title": "Lead Paragraph",
        "typography_typography": "custom",
        "typography_font_family": F_BODY,
        "typography_font_weight": "400",
        "typography_font_size": {"unit": "px", "size": 19},
        "typography_font_size_mobile": {"unit": "px", "size": 17},
        "typography_line_height": {"unit": "em", "size": 1.7},
    },
    {
        "_id": "nav",
        "title": "Nav / Menu Item",
        "typography_typography": "custom",
        "typography_font_family": F_BODY,
        "typography_font_weight": "500",
        "typography_font_size": {"unit": "px", "size": 16},
        "typography_line_height": {"unit": "em", "size": 1.3},
    },
    {
        "_id": "stat",
        "title": "Stat Number",
        "typography_typography": "custom",
        "typography_font_family": F_HEADING,
        "typography_font_weight": "700",
        "typography_font_size": {"unit": "px", "size": 56},
        "typography_font_size_mobile": {"unit": "px", "size": 40},
        "typography_line_height": {"unit": "em", "size": 1.05},
        "typography_letter_spacing": {"unit": "px", "size": -1.5},
    },
    # ---- Persian / RTL type styles ----------------------------------------
    # `Arad` must be uploaded under Elementor > Custom Fonts with the exact
    # family name "Arad" (see docs/04-rtl-persian-setup.md). Persian copy is
    # 10-15% larger per point size, so the FA styles run a touch bigger and
    # with generous line-height for correct diacritic clearance.
    {
        "_id": "fa-heading",
        "title": "FA / Headings",
        "typography_typography": "custom",
        "typography_font_family": F_FA,
        "typography_font_weight": "700",
        "typography_font_size": {"unit": "px", "size": 40},
        "typography_font_size_tablet": {"unit": "px", "size": 32},
        "typography_font_size_mobile": {"unit": "px", "size": 26},
        "typography_line_height": {"unit": "em", "size": 1.5},
    },
    {
        "_id": "fa-display",
        "title": "FA / Hero Display",
        "typography_typography": "custom",
        "typography_font_family": F_FA,
        "typography_font_weight": "700",
        "typography_font_size": {"unit": "px", "size": 54},
        "typography_font_size_tablet": {"unit": "px", "size": 40},
        "typography_font_size_mobile": {"unit": "px", "size": 30},
        "typography_line_height": {"unit": "em", "size": 1.55},
    },
    {
        "_id": "fa-body",
        "title": "FA / Body",
        "typography_typography": "custom",
        "typography_font_family": F_FA,
        "typography_font_weight": "400",
        "typography_font_size": {"unit": "px", "size": 17},
        "typography_font_size_mobile": {"unit": "px", "size": 16},
        "typography_line_height": {"unit": "em", "size": 2},
    },
    {
        "_id": "fa-label",
        "title": "FA / Eyebrow & Nav",
        "typography_typography": "custom",
        "typography_font_family": F_FA,
        "typography_font_weight": "600",
        "typography_font_size": {"unit": "px", "size": 15},
        "typography_line_height": {"unit": "em", "size": 1.7},
        "typography_text_transform": "none",
    },
]

T = {
    "primary": "globals/typography?id=primary",
    "secondary": "globals/typography?id=secondary",
    "text": "globals/typography?id=text",
    "accent": "globals/typography?id=accent",
    "display": "globals/typography?id=display",
    "h2": "globals/typography?id=h2",
    "h3": "globals/typography?id=h3",
    "eyebrow": "globals/typography?id=eyebrow",
    "lead": "globals/typography?id=lead",
    "nav": "globals/typography?id=nav",
    "stat": "globals/typography?id=stat",
    "fa_heading": "globals/typography?id=fa-heading",
    "fa_display": "globals/typography?id=fa-display",
    "fa_body": "globals/typography?id=fa-body",
    "fa_label": "globals/typography?id=fa-label",
}

# ---------------------------------------------------------------------------
# Spacing / radius / shadow scale
# ---------------------------------------------------------------------------

SP = {
    "3xs": 4, "2xs": 8, "xs": 12, "sm": 16, "md": 24, "lg": 32,
    "xl": 40, "2xl": 48, "3xl": 64, "4xl": 80, "5xl": 96, "6xl": 120,
}

# Vertical rhythm for <section> level containers: desktop / tablet / mobile
SECTION_PAD_Y = (120, 80, 56)
SECTION_PAD_X = (24, 24, 20)

RADIUS = {"sm": 10, "md": 16, "lg": 22, "xl": 30, "2xl": 40, "pill": 999}

SHADOW = {
    "xs": {"horizontal": 0, "vertical": 1, "blur": 2, "spread": 0, "color": "rgba(28,25,23,0.06)"},
    "sm": {"horizontal": 0, "vertical": 2, "blur": 6, "spread": -1, "color": "rgba(28,25,23,0.08)"},
    "md": {"horizontal": 0, "vertical": 10, "blur": 24, "spread": -8, "color": "rgba(28,25,23,0.14)"},
    "lg": {"horizontal": 0, "vertical": 24, "blur": 48, "spread": -16, "color": "rgba(28,25,23,0.22)"},
    "xl": {"horizontal": 0, "vertical": 40, "blur": 80, "spread": -24, "color": "rgba(28,25,23,0.28)"},
    "amber": {"horizontal": 0, "vertical": 18, "blur": 36, "spread": -12, "color": "rgba(244,166,42,0.42)"},
}

# Standard content widths fed to the container `boxed_width` control.
W = {"wide": 1300, "content": 1240, "narrow": 900, "prose": 760}

BREAKPOINTS = {"mobile": 767, "tablet": 1024}

# ---------------------------------------------------------------------------
# Imagery
# ---------------------------------------------------------------------------

# (file, intrinsic width, intrinsic height) - all optimised to 3:2 landscape by
# tools/media.py, which keeps the containers' rendered heights consistent.
IMAGES = {
    "hero": ("hero-dashboard.jpg", 1500, 1000),
    "highlight_agents": ("highlight-agents.jpg", 1500, 1000),
    "highlight_insights": ("highlight-insights.jpg", 1500, 1000),
    "case_retail": ("case-retail.jpg", 1500, 1000),
    "case_fintech": ("case-fintech.jpg", 1500, 1000),
    "case_health": ("case-health.jpg", 1500, 1000),
    "about": ("about-studio.jpg", 1500, 1000),
}

# 1x1 transparent PNG used only if you prefer to import the kit without
# downloading the demo artwork (see docs/06). Not referenced by the templates.
PLACEHOLDER_URL = (
    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmci"
    "IHdpZHRoPSIxNTAwIiBoZWlnaHQ9IjEwMDAiPjxyZWN0IHdpZHRoPSIxNTAwIiBoZWlnaHQ9"
    "IjEwMDAiIGZpbGw9IiNGM0U5REIiLz48L3N2Zz4="
)


def img_url(key):
    """Public URL Elementor downloads on import (release asset)."""
    return "%s/%s" % (ASSET_BASE, IMAGES[key][0])
