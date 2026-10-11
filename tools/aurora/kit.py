"""
Aurora AI - the Kit document (Elementor > Site Settings).

Produces the `_elementor_page_settings` payload that carries the whole design
system: global colors, global fonts, layout width, breakpoints, body / heading /
link / button / form-field styles.

Every key below was checked against Elementor source:
  core/kits/documents/tabs/global-colors.php
  core/kits/documents/tabs/global-typography.php
  core/kits/documents/tabs/theme-style-typography.php
  core/kits/documents/tabs/theme-style-buttons.php
  core/kits/documents/tabs/theme-style-form-fields.php
  core/kits/documents/tabs/theme-style-images.php
  core/kits/documents/tabs/settings-layout.php
  core/kits/documents/tabs/settings-background.php
  core/kits/documents/tabs/settings-site-identity.php
"""

from __future__ import annotations

from typing import Any, Dict, List

from . import tokens as tk
from .dsl import dims, slider


def _typo(prefix: str, family: str, size: int, weight: str, line_height: float,
          letter_spacing: float = 0.0, *, size_mobile: int = 0,
          transform: str = "", extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "%s_typography_typography" % prefix: "custom",
        "%s_typography_font_family" % prefix: family,
        "%s_typography_font_weight" % prefix: weight,
        "%s_typography_font_size" % prefix: slider(size),
        "%s_typography_line_height" % prefix: slider(line_height, "em"),
        "%s_typography_letter_spacing" % prefix: slider(letter_spacing),
    }
    if size_mobile:
        out["%s_typography_font_size_mobile" % prefix] = slider(size_mobile)
    if transform:
        out["%s_typography_text_transform" % prefix] = transform
    out.update(extra or {})
    return out


def site_settings() -> Dict[str, Any]:
    """The full Kit settings array (stored in the kit's _elementor_page_settings)."""
    s: Dict[str, Any] = {}

    # -- Site identity ------------------------------------------------------
    s.update({
        "site_name": tk.BRAND,
        "site_description": tk.TAGLINE,
    })

    # -- Global colors ------------------------------------------------------
    s["system_colors"] = tk.SYSTEM_COLORS
    s["custom_colors"] = tk.CUSTOM_COLORS

    # -- Global fonts -------------------------------------------------------
    s["system_typography"] = tk.SYSTEM_TYPOGRAPHY
    s["custom_typography"] = tk.CUSTOM_TYPOGRAPHY
    s["default_generic_fonts"] = "Sans-serif"

    # -- Layout (settings-layout.php) --------------------------------------
    s.update({
        "container_width": slider(tk.W["content"]),
        "container_width_tablet": slider(100, "%"),
        "container_width_mobile": slider(100, "%"),
        "container_padding": dims(0),
        "space_between_widgets": {"row": "0", "column": "0", "unit": "px"},
        "page_title_selector": "h1.entry-title",
        "active_breakpoints": ["viewport_mobile", "viewport_tablet"],
        "viewport_md": tk.BREAKPOINTS["mobile"] + 1,   # 768
        "viewport_lg": tk.BREAKPOINTS["tablet"] + 1,   # 1025
        "default_page_template": "default",
    })

    # -- Background ---------------------------------------------------------
    s.update({
        "body_background_background": "classic",
        "body_background_color": tk.G["sand_50"],
    })

    # -- Style > Typography -------------------------------------------------
    s.update({
        "body_color": tk.G["text"],
        "paragraph_spacing": slider(1.15, "em"),
        "link_normal_color": tk.G["secondary"],
        "link_hover_color": tk.G["amber_600"],
        "link_normal_typography_typography": "custom",
        "link_normal_typography_font_family": tk.F_BODY,
        "link_hover_typography_typography": "custom",
        "link_hover_typography_font_family": tk.F_BODY,
    })
    s.update(_typo("body", tk.F_BODY, 17, "400", 1.75, 0, size_mobile=16))
    s.update(_typo("link_normal", tk.F_BODY, 17, "400", 1.75, 0))
    s.update(_typo("link_hover", tk.F_BODY, 17, "400", 1.75, 0))

    # Heading ladder: H1 → hero, H2 → section, H3 → card, H4-H6 → utility
    headings = [
        ("h1", tk.F_HEADING, 64, "700", 1.06, -1.6, 36),
        ("h2", tk.F_HEADING, 46, "700", 1.12, -1.0, 28),
        ("h3", tk.F_HEADING, 22, "600", 1.30, -0.3, 20),
        ("h4", tk.F_HEADING, 19, "600", 1.35, -0.2, 18),
        ("h5", tk.F_BODY, 16, "700", 1.40, 1.2, 15),
        ("h6", tk.F_BODY, 13, "700", 1.30, 1.6, 12),
    ]
    for name, family, size, weight, lh, ls, mob in headings:
        s["%s_color" % name] = tk.G["secondary"]
        s.update(_typo(name, family, size, weight, lh, ls, size_mobile=mob))
    # H5/H6 double as the "eyebrow" style
    s["h5_typography_text_transform"] = "none"
    s["h6_typography_text_transform"] = "uppercase"

    # -- Style > Buttons ----------------------------------------------------
    s.update({
        "button_text_color": tk.G["ink_900"],
        "button_background_background": "classic",
        "button_background_color": tk.G["primary"],
        "button_border_border": "solid",
        "button_border_width": dims(0),
        "button_border_color": "rgba(0,0,0,0)",
        "button_border_radius": dims(tk.RADIUS["pill"]),
        "button_padding": dims(17, 30),
        "button_hover_text_color": tk.G["ink_900"],
        "button_hover_background_background": "classic",
        "button_hover_background_color": tk.G["amber_600"],
        "button_hover_border_border": "solid",
        "button_hover_border_width": dims(0),
        "button_hover_border_color": "rgba(0,0,0,0)",
        "button_hover_border_radius": dims(tk.RADIUS["pill"]),
    })
    s.update(_typo("button", tk.F_HEADING, 15, "600", 1.2, 0.2))
    s["button_padding_mobile"] = dims(15, 24)

    # -- Style > Form fields ------------------------------------------------
    s.update({
        "form_field_text_color": tk.G["secondary"],
        "form_field_accent_color": tk.G["primary"],
        "form_field_background_color": tk.G["white"],
        "form_field_border_border": "solid",
        "form_field_border_width": dims(1),
        "form_field_border_color": tk.G["line"],
        "form_field_border_radius": dims(12),
        "form_field_padding": dims(15, 17),
        "form_field_focus_text_color": tk.G["secondary"],
        "form_field_focus_accent_color": tk.G["amber_600"],
        "form_field_focus_background_color": tk.G["white"],
        "form_field_focus_border_border": "solid",
        "form_field_focus_border_width": dims(1),
        "form_field_focus_border_color": tk.G["amber_600"],
        "form_field_focus_border_radius": dims(12),
        "form_field_focus_transition_duration": slider(200),
    })
    s.update(_typo("form_label", tk.F_BODY, 13, "600", 1.4, 0.2))
    s.update(_typo("form_field", tk.F_BODY, 16, "400", 1.5, 0))

    # -- Style > Images -----------------------------------------------------
    s.update({
        "image_border_border": "solid",
        "image_border_width": dims(0),
        "image_border_color": "rgba(0,0,0,0)",
    })

    # -- No custom CSS is required anywhere in this kit ---------------------
    s["custom_css"] = ""
    return s


def set_key(key: str, value: Any) -> Dict[str, Any]:
    return {key: value}


def kit_document() -> Dict[str, Any]:
    """Elementor 'kit' document payload.

    `page_settings` is what Elementor's template importer reads for kit-type
    documents; `settings` mirrors the shape used by the modern Export Kit
    (site-settings.json).
    """
    settings = site_settings()
    return {
        "content": [],
        "page_settings": settings,
        "settings": settings,
        "version": "0.4",
        "title": tk.KIT_TITLE,
        "type": "kit",
    }


def site_settings_file() -> Dict[str, Any]:
    """site-settings.json as produced by Elementor's Export Kit runner."""
    return {"content": [], "settings": site_settings()}


def manifest(template_index: Dict[str, List[str]]) -> Dict[str, Any]:
    """manifest.json as read by the Import Kit importer.

    `templates` and `content` are intentionally empty: Elementor's Templates and
    Elementor_Content runners expect WP post exports in `templates/<id>.json` /
    `content/<post_type>/<id>.json`, and this kit is a *design system + template
    library* rather than a post export. Declaring them empty keeps the import
    clean instead of surfacing skipped-file warnings, and the design system
    (global colors, fonts, layout, buttons, forms) still imports in one step.
    The elementor-post-type index is kept in `templateIndex` for the changelog
    and for the docs.
    """
    return {
        "manifestVersion": "2.0",
        "title": tk.KIT_TITLE,
        "description": (
            "Aurora AI - a warm, bilingual (EN/FA) Elementor template kit for AI and "
            "SaaS products. Flexbox containers, global colors, global fonts and "
            "Theme Builder header/footer."
        ),
        "elementorVersion": "3.30.0",
        "site-settings": {
            "theme": False,
            "globalColors": True,
            "globalFonts": True,
            "themeStyleSettings": True,
            "generalSettings": True,
            "experiments": False,
            "customCode": False,
            "customIcons": False,
            "customFonts": False,
            "classes": False,
            "variables": False,
        },
        "templates": {},
        "content": {},
        "templateIndex": template_index,
    }
