"""
Aurora AI - the reusable Elementor section library.

Each builder returns ONE top level Elementor container of html_tag=section, ready
to be dropped on any page, or exported on its own as a reusable block template.
Content is bilingual: pass fa=True to switch to Persian copy + Arad typography.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from . import tokens as tk
from .components import (
    badge, arrow_link, bullet_card, case_card, contact_line, eyebrow_row, feature_pill,
    flexcol, flexrow, flex_item, grid, icon_card, icon_tile, link_column, pricing_card,
    quote_card, section_head, stat_block, step_card, surface, tag_pill, brand_block,
)
from .dsl import (
    Doc, accordion, button, container, counter, divider, form, form_field, heading,
    icon, icon_box, icon_list, image, inner, nav_menu, section, social_icons, spacer,
    tabs_widget, text, testimonial, widget, dims, gap, link, slider, typo, icon_val,
)

# ---------------------------------------------------------------------------
# Shared backdrops
# ---------------------------------------------------------------------------

BG_PAGE = {"background_background": "classic", "background_color": tk.G["sand_50"]}
BG_WHITE = {"background_background": "classic", "background_color": tk.G["white"]}
BG_WARM = {"background_background": "classic", "background_color": tk.G["sand_100"]}
BG_SUNKEN = {"background_background": "classic", "background_color": tk.G["sand_200"]}
BG_DARK = {"background_background": "classic", "background_color": tk.G["ink_900"]}
BG_GRADIENT_HERO = {
    "background_background": "gradient",
    "background_color": "#FFFBF5",
    "background_color_stop": slider(0, "%"),
    "background_color_b": "#F6E7D2",
    "background_color_b_stop": slider(100, "%"),
    "background_gradient_type": "linear",
    "background_gradient_angle": slider(155, "deg"),
}


def _band(doc: Doc, children: Sequence[Dict[str, Any]], *, bg: Dict[str, Any], pad_y=None,
          element_id: Optional[str] = None, **kw: Any) -> Dict[str, Any]:
    """Section wrapper that holds a centred, max-width content container."""
    wrap = container(
        doc, list(children), is_inner=True, direction="column",
        extra={"boxed_width": slider(tk.W["content"]),
               "boxed_width_tablet": slider(100, "%"),
               "boxed_width_mobile": slider(100, "%")},
    )
    return section(doc, [wrap], background=bg, pad_y=pad_y, element_id=element_id, **kw)


# ===========================================================================
# 1. HERO - split with product shot and proof chips
# ===========================================================================

def hero_split(doc: Doc, *, fa: bool = False, image_key: str = "hero",
               animation: bool = True) -> Dict[str, Any]:
    def L(en: str, fa_text: str) -> str:
        return fa_text if fa else en

    left = flexcol(doc, [
        badge(doc, L("Aurora Agents 2.0 - now generally available",
                     "عاملهای آرورا ۲.۰ - اکنون در دسترس عمومی"),
              bg=tk.G["amber_100"], icon_value="fas fa-bolt", fa=fa),
        heading(doc, L("AI agents that actually ship.",
                       "عاملهای هوش مصنوعی که واقعاً به محصول میرسند."),
                tag="h1",
                global_style=tk.T["fa_display"] if fa else tk.T["display"],
                color=tk.G["secondary"],
                animation="fadeInUp" if animation else None, delay=60),
        text(doc, "<p>%s</p>" % L(
            "Aurora gives product teams warm, human AI infrastructure: build agents, "
            "ground them in your own data, evaluate every release and ship to production "
            "in days - not quarters.",
            "آرورا زیرساخت هوش مصنوعی گرم و انسانی را در اختیار تیمهای محصول میگذارد: "
            "عامل بسازید، آنها را روی دادههای خودتان مستقر کنید، هر انتشار را ارزیابی کنید و "
            "در چند روز - نه چند فصل - به تولید برسانید."),
            global_style=tk.T["fa_body"] if fa else tk.T["lead"],
            color=tk.G["text"], animation="fadeInUp" if animation else None, delay=120),
        flexrow(doc, [
            button(doc, L("Start free trial", "شروع دوره آزمایشی رایگان"), "#contact",
                   variant="primary", size="lg", hover_animation="grow",
                   icon="fas fa-arrow-right", icon_align="right", icon_indent=10),
            button(doc, L("Book a live demo", "درخواست دموی زنده"), "#demo",
                   variant="outline", size="lg"),
        ], gap_value=14, align="center",
            animation="fadeInUp" if animation else None, animation_delay=180),
        flexrow(doc, [
            flexrow(doc, [icon(doc, "fas fa-star", view="default", size=13, padding=0,
                               primary=tk.G["primary"]) for _ in range(5)],
                    gap_value=4, wrap="nowrap"),
            heading(doc, L("4,000+ product teams build on Aurora",
                           "بیش از ۴٫۰۰۰ تیم محصول روی آرورا میسازند"),
                    tag="p", global_style=tk.T["fa_label"] if fa else tk.T["text"],
                    color=tk.G["muted"], letter_spacing=slider(0)),
        ], gap_value=14, align="center",
            animation="fadeInUp" if animation else None, animation_delay=240),
    ], gap_value=26, align="flex-start", extra={},
        **flex_item(0, basis=52, tablet_basis=100, mobile_basis=100, grow=0))

    proof = grid(doc, [
        flexrow(doc, [
            icon(doc, i, view="default", size=15, padding=0, primary=tk.G["accent"]),
            heading(doc, t_, tag="p", global_style=tk.T["fa_label"] if fa else tk.T["text"],
                    color=tk.G["secondary"], letter_spacing=slider(0),
                    typography_font_size=slider(15),
                    settings={"_element_width": "initial"}),
        ], gap_value=9, wrap="nowrap", extra={"_element_width": "initial"})
        for i, t_ in [
            ("fas fa-shield-alt", L("SOC 2 Type II", "SOC 2 نوع دو")),
            ("fas fa-server", L("EU + US regions", "مناطق اروپا و آمریکا")),
            ("fas fa-plug", L("40+ integrations", "بیش از ۴۰ اتصال")),
        ]
    ], gap_value=22, extra={"_element_width": "initial"})

    right = flexcol(doc, [
        flexcol(doc, [
            image(doc, tk.img_url(image_key),
                  alt=L("Aurora AI agent console showing a live evaluation run",
                        "کنسول عامل آرورا در حال اجرای ارزیابی"),
                  size="large", width=100, width_unit="%", object_fit="cover",
                  radius=tk.RADIUS["lg"]),
        ], gap_value=0, align="center",
            background={"background_background": "classic", "background_color": tk.G["white"]},
            border={"border_border": "solid", "border_width": dims(1), "border_color": tk.G["line"]},
            radius=tk.RADIUS["xl"], shadow="lg",
            extra={"padding": dims(12), "padding_mobile": dims(8)}),
        flexrow(doc, [
            surface(doc, [
                heading(doc, "−38%", tag="p", global_style=tk.T["h3"], color=tk.G["secondary"],
                        letter_spacing=slider(-0.5)),
                heading(doc, L("Support cost", "هزینه پشتیبانی"), tag="p",
                        global_style=tk.T["eyebrow"], color=tk.G["muted"],
                        letter_spacing=slider(1) if not fa else slider(0),
                        typography_font_size=slider(11)),
            ], kind="card", pad=16, pad_mobile=14, gap_v=2,
                animation="fadeInUp" if animation else None, animation_delay=320,
                extra={"flex_direction": "column", "_element_width": "initial"}),
            surface(doc, [
                heading(doc, "12 days", tag="p", global_style=tk.T["h3"], color=tk.G["secondary"],
                        letter_spacing=slider(-0.5)),
                heading(doc, L("To first release", "تا نخستین انتشار"), tag="p",
                        global_style=tk.T["eyebrow"], color=tk.G["muted"],
                        letter_spacing=slider(1) if not fa else slider(0),
                        typography_font_size=slider(11)),
            ], kind="card_warm", pad=16, pad_mobile=14, gap_v=2,
                animation="fadeInUp" if animation else None, animation_delay=380,
                extra={"flex_direction": "column", "_element_width": "initial"}),
        ], gap_value=12, justify="center", margin=dims(-34, 0, 0, 0), z_index=2,
            extra={"flex_wrap": "wrap"}),
    ], gap_value=0, align="center",
        **flex_item(0, basis=44, tablet_basis=100, mobile_basis=100, grow=0))

    row = flexrow(doc, [left, right], gap_value=56, align="center", justify="space-between",
                  extra={"flex_gap_mobile": gap(40)})

    return _band(doc, [row], bg=BG_GRADIENT_HERO, pad_y=(104, 72, 48), element_id="hero")


# ===========================================================================
# 2. LOGO CLOUD
# ===========================================================================

def logo_cloud(doc: Doc, *, fa: bool = False, dark: bool = False) -> Dict[str, Any]:
    names = ["NORTHWIND", "LUMEN", "ORBITAL", "HELIOS", "KOMMA", "FIELDNOTE"]
    items = [heading(doc, n, tag="span", global_style=tk.T["h3"],
                     color=tk.G["muted_dark"] if dark else tk.G["muted"],
                     letter_spacing=slider(1.4), align="center",
                     typography_font_size=slider(18),
                     settings={"_element_width": "initial"})
             for n in names]
    row = flexrow(doc, items, gap_value=44, align="center", justify="space-between",
                  extra={"flex_gap_mobile": gap(26)})
    return _band(doc, [
        heading(doc, "منتخب تیمهای پیشرو" if fa else "Trusted by teams shipping in production",
                tag="p", global_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                color=tk.G["muted"], align="center", letter_spacing=slider(1.4)),
        row,
    ], bg=BG_DARK if dark else BG_WHITE, pad_y=(56, 44, 40))


# ===========================================================================
# 3. FEATURE GRID
# ===========================================================================

FEATURES = [
    ("fas fa-diagram-project",
     "Visual agent builder", "معمار بصری عامل",
     "Compose multi-step agents on a canvas. Every step is versioned, reviewable and "
     "reversible from the Elementor-style editor your team already knows.",
     "عاملهای چندمرحلهای را روی یک بوم بسازید. هر مرحله نسخهبندی میشود، قابل بازبینی و "
     "قابل بازگشت است."),
    ("fas fa-database",
     "Grounded in your data", "مستقر روی داده شما",
     "Connect a warehouse, a PDF library or an API in minutes. Retrieval, chunking and "
     "re-ranking are handled for you, with citations on every answer.",
     "در چند دقیقه یک انبار داده، کتابخانه PDF یا API را وصل کنید. بازیابی و رتبهبندی "
     "خودکار انجام میشود و هر پاسخ منبع دارد."),
    ("fas fa-vial",
     "Evaluation built in", "ارزیابی درونساخت",
     "Ship with confidence using golden datasets, regression diffs and automated quality "
     "gates that run on every prompt change.",
     "با مجموعههای طلایی، مقایسه رگرسیون و دروازههای کیفیت خودکار، با اطمینان منتشر کنید."),
    ("fas fa-shield-alt",
     "Enterprise guardrails", "محافظهای سازمانی",
     "PII redaction, prompt-injection defence, per-tenant isolation and a full audit trail "
     "of every model call.",
     "حذف دادههای هویتی، دفاع در برابر تزریق دستور، جداسازی هر مستأجر و ردگیری کامل "
     "همه فراخوانیها."),
    ("fas fa-gauge-high",
     "Fast by default", "سریع بهصورت پیشفرض",
     "Streaming responses, semantic caching and regional routing keep first-token latency "
     "under 400 ms.",
     "پاسخهای جریانی، حافظه نهان معنایی و مسیریابی منطقهای، تأخیر نخستین توکن را زیر "
     "۴۰۰ میلیثانیه نگه میدارد."),
    ("fas fa-code-branch",
     "Developer-first API", "API برای توسعهدهندگان",
     "TypeScript and Python SDKs, webhooks, idempotency keys and a sandbox that mirrors "
     "production exactly.",
     "کتابخانههای تایپاسکریپت و پایتون، وبهوک، کلیدهای تکرارناپذیر و محیط آزمایشی "
     "همسان با تولید."),
]


def feature_grid(doc: Doc, *, fa: bool = False, dark: bool = False,
                 eyebrow: Optional[str] = None, title: Optional[str] = None,
                 lead: Optional[str] = None) -> Dict[str, Any]:
    p = "fa_" if fa else ""
    head = section_head(
        doc, fa=fa,
        eyebrow=eyebrow if eyebrow is not None else (
            "چرا آرورا" if fa else "Why Aurora"),
        title=title if title is not None else (
            "همهچیز برای ساخت هوش مصنوعی قابل اعتماد" if fa else
            "Everything you need to ship trustworthy AI"),
        lead=lead if lead is not None else (
            "یک پلتفرم یکپارچه که بازه ساخت تا انتشار را پوشش میدهد - بدون چسباندن "
            "پنج سرویس جداگانه." if fa else
            "One platform that covers the whole build-to-production arc - without stitching "
            "five vendors together."),
        lead_color=tk.G["muted_dark"] if dark else tk.G["text"])
    cards = [
        icon_card(doc, icon_value=i, title=t_, body=b_, fa=fa, delay=n * 90,
                  kind="card_dark" if dark else "card")
        for n, (i, en_t, fa_t, en_b, fa_b) in enumerate(FEATURES)
        for t_, b_ in [(fa_t if fa else en_t, fa_b if fa else en_b)]
    ]
    for c in cards:
        c["settings"].update(flex_item(3)["flex_item"])
        c["settings"]["padding"] = dims(30)
        if dark:
            c["settings"].update({"background_color": tk.G["ink_800"],
                                  "border_color": "rgba(255,255,255,0.10)"})
    return _band(doc, [head, grid(doc, cards, gap_value=26)], bg=BG_DARK if dark else BG_PAGE)


# ===========================================================================
# 4. FEATURE ZIGZAG
# ===========================================================================

def feature_zigzag(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    blocks = [
        (tk.img_url("highlight_agents"),
         "نویسندهسازی بصری" if fa else "Build",
         "بوم عاملها" if fa else "A canvas that reads like your product spec",
         "هر گره یک قابلیت است: فراخوانی مدل، ابزار، شرط یا انتقال انسانی. تیمها "
         "جریان کار را میسازند، آن را نسخهبندی میکنند و با یک کلیک به تولید میفرستند."
         if fa else
         "Every node is a capability: model call, tool, condition or human hand-off. Teams "
         "compose the flow, version it and promote it to production in one click.",
         ["نسخهبندی هر گره", "پیوند به مخزن کد", "انتشار تدریجی"] if fa else
         ["Versioned nodes", "Link to your repo", "Progressive rollout"]),
        (tk.img_url("highlight_insights"),
         "سنجش" if fa else "Measure",
         "ارزیابیهایی که واقعاً جلوی انتشار بد را میگیرند"
         if fa else "Evaluations that actually block bad releases",
         "مجموعههای طلایی را اجرا کنید، امتیازها را بین نسخهها مقایسه کنید و در صورت "
         "افت کیفیت، انتشار متوقف میشود." if fa else
         "Run golden sets, diff scores across versions and let the pipeline stop a release "
         "when quality regresses - automatically.",
         ["مجموعههای طلایی", "مقایسه رگرسیون", "دروازه کیفیت"] if fa else
         ["Golden datasets", "Regression diffs", "Quality gates in CI"]),
    ]

    rows: List[Dict[str, Any]] = []
    for n, (img, eyebrow, title, body, bullets) in enumerate(blocks):
        media = flexcol(doc, [
            image(doc, img, alt=title, size="large", width=100, width_unit="%",
                  object_fit="cover", radius=tk.RADIUS["lg"]),
        ], gap_value=0, align="center",
            background={"background_background": "classic", "background_color": tk.G["white"]},
            border={"border_border": "solid", "border_width": dims(1), "border_color": tk.G["line"]},
            radius=tk.RADIUS["xl"], shadow="md",
            extra={"padding": dims(10), "padding_mobile": dims(8)},
            **flex_item(0, basis=48, tablet_basis=100, mobile_basis=100, grow=0))

        copy = flexcol(doc, [
            eyebrow_row(doc, eyebrow, align="left", fa=fa),
            heading(doc, title, tag="h2",
                    global_style=tk.T["fa_heading"] if fa else tk.T["h2"],
                    color=tk.G["secondary"],
                    font_size=slider(38), font_size_tablet=slider(30), font_size_mobile=slider(26),
                    animation="fadeInUp"),
            text(doc, "<p>%s</p>" % body,
                 global_style=tk.T["fa_body"] if fa else tk.T["lead"],
                 color=tk.G["text"]),
            flexrow(doc, [feature_pill(doc, b, fa=fa) for b in bullets],
                    gap_value=18, align="center",
                    extra={"flex_gap_mobile": gap(12)}),
            button(doc, "بیشتر بدانید" if fa else "See it in action", "#demo",
                   variant="dark", size="md", icon="fas fa-arrow-right", icon_align="right"),
        ], gap_value=20, align="flex-start", extra={"flex_direction": "column"},
            **flex_item(0, basis=46, tablet_basis=100, mobile_basis=100, grow=0))

        order_media = [copy, media] if n % 2 == 1 else [media, copy]
        rows.append(flexrow(doc, order_media, gap_value=60, align="center",
                            justify="space-between", extra={"flex_gap_mobile": gap(32)}))

    head = section_head(
        doc, fa=fa,
        eyebrow="چطور کار میکند" if fa else "How it works",
        title="از ایده تا تولید، بدون آشفتگی" if fa else "From idea to production, without the mess",
        lead="یک مسیر روشن: بساز، بسنج، منتشر کن و پایش کن."
        if fa else "One clear path: build, measure, ship and observe.")
    return _band(doc, [head, *rows], bg=BG_WHITE, element_id="how")


# ===========================================================================
# 5. STATS BAND
# ===========================================================================

def stats_band(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    stats = [
        (380, "M", "فراخوانی مدل در ماه" if fa else "Model calls per month"),
        (38, "%", "کاهش هزینه پشتیبانی" if fa else "Lower support cost"),
        (99, ".98%", "دسترسپذیری قراردادشده" if fa else "Contracted uptime"),
        (12, "", "روز تا نخستین انتشار" if fa else "Days to first release"),
    ]
    blocks = [
        flexcol(doc, [
            flexrow(doc, [
                counter(doc, n, label, suffix=suf,
                        number_color=tk.G["white"], title_color=tk.G["muted_dark"],
                        number_style=tk.T["stat"],
                        title_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                        title_tag="p", align="left"),
            ], gap_value=0, wrap="nowrap"),
        ], gap_value=6, align="flex-start",
            animation="fadeInUp", animation_delay=idx * 100,
            **flex_item(4))
        for idx, (n, suf, label) in enumerate(stats)
    ]
    head = flexrow(doc, [
        flexcol(doc, [
            eyebrow_row(doc, "نتایج واقعی" if fa else "Proof, not promises", align="left", fa=fa),
            heading(doc, "اعدادی که مدیران محصول دوست دارند"
                    if fa else "Numbers your product leaders actually care about",
                    tag="h2", global_style=tk.T["fa_heading"] if fa else tk.T["h2"],
                    color=tk.G["white"],
                    font_size=slider(38), font_size_mobile=slider(26),
                    animation="fadeInUp"),
        ], gap_value=16, align="flex-start",
            **flex_item(0, basis=52, tablet_basis=100, mobile_basis=100, grow=0)),
    ], gap_value=0, justify="space-between")

    return _band(doc, [
        head,
        divider(doc, color="rgba(255,255,255,0.12)", width=100, weight=1, gap=0,
                _element_width="100%"),
        grid(doc, blocks, gap_value=32, extra={"flex_gap_mobile": gap(28)}),
    ], bg=BG_DARK, pad_y=(96, 72, 56), element_id="results")


# ===========================================================================
# 6. CAPABILITY CARDS (services)
# ===========================================================================

SERVICES_FA = [
    ("fas fa-robot", "Customer agents", "عاملهای مشتری",
     "Answer product and billing questions in 40 languages, escalate to a human with the "
     "full transcript attached.",
     "پاسخ به پرسشهای محصول و صورتحساب در ۴۰ زبان؛ در صورت نیاز با متن کامل گفتگو به "
     "کارشناس منتقل میشود.", ["حافظه مکالمه", "انتقال به انسان", "رضایتسنجی"]),
    ("fas fa-magnifying-glass-chart", "Research copilots", "همراه پژوهش",
     "Summarise thousands of documents with citations your analysts can verify in one click.",
     "خلاصهسازی هزاران سند با ارجاعهایی که تحلیلگر میتواند با یک کلیک بررسی کند.",
     ["خلاصه با ارجاع", "پرسش از اسناد", "خروجی ساختاریافته"]),
    ("fas fa-gears", "Workflow automation", "خودکارسازی فرایند",
     "Replace brittle RPA scripts with agents that read intent, call your tools and recover "
     "from failure.",
     "جایگزینی اسکریپتهای شکننده RPA با عاملهایی که قصد را میفهمند و از خطا "
     "بازیابی میشوند.", ["ابزار سفارشی", "تلاش مجدد هوشمند", "گزارش کامل"]),
]


def capability_cards(doc: Doc, *, fa: bool = False, eyebrow: Optional[str] = None,
                     title: Optional[str] = None, lead: Optional[str] = None,
                     cols: int = 3) -> Dict[str, Any]:
    cards = []
    for idx, (ic, en_t, fa_t, en_b, fa_b, bullets) in enumerate(SERVICES_FA):
        cards.append(bullet_card(
            doc, icon_value=ic,
            title=fa_t if fa else en_t,
            body=fa_b if fa else en_b,
            bullets=list(bullets),
            link_url="#services", link_text="جزئیات خدمات" if fa else "Explore the service",
            fa=fa, delay=idx * 100,
            col_kw=flex_item(cols)))
    head = section_head(
        doc, fa=fa,
        eyebrow=eyebrow if eyebrow is not None else ("خدمات" if fa else "Services"),
        title=title if title is not None else (
            "تیمهایی که هوش مصنوعی را در مقیاس اجرا میکنند"
            if fa else "Teams we help put AI into production"),
        lead=lead if lead is not None else (
            "از انتخاب مورد کاربرد تا پایش پس از انتشار، همراه شما هستیم."
            if fa else "From use-case selection to post-launch monitoring, we stay in the loop."))
    return _band(doc, [head, grid(doc, cards, gap_value=26)], bg=BG_PAGE, element_id="services")


# ===========================================================================
# 7. PROCESS STEPS
# ===========================================================================

def process_steps(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    steps = [
        ("۰۱" if fa else "01", "کشف" if fa else "Discover",
         "کارگاه یکروزه برای یافتن موردهای کاربرد با بالاترین بازده."
         if fa else "A one-day workshop to find the two or three use cases with real payback.",
         "شناسایی فرصتها" if fa else "Opportunity map"),
        ("۰۲" if fa else "02", "نمونه اولیه" if fa else "Prototype",
         "یک عامل کاری روی داده واقعی شما در ده روز کاری."
         if fa else "A working agent on your real data, live in ten business days.",
         "اثبات ارزش" if fa else "Proof of value"),
        ("۰۳" if fa else "03", "سختسازی" if fa else "Harden",
         "ارزیابی، محافظ و پایش پیش از انتشار گسترده."
         if fa else "Evaluations, guardrails and observability before you scale traffic.",
         "آماده تولید" if fa else "Production ready"),
        ("۰۴" if fa else "04", "مقیاس" if fa else "Scale",
         "انتشار تدریجی، بهینهسازی هزینه و انتقال دانش به تیم شما."
         if fa else "Progressive rollout, cost tuning and enablement for your team.",
         "رشد پایدار" if fa else "Sustainable growth"),
    ]
    return _band(doc, [
        section_head(doc, fa=fa,
                     eyebrow="فرایند" if fa else "Our process",
                     title="چهار مرحله، بدون غافلگیری" if fa else "Four steps, zero surprises",
                     lead="شفاف، زمانبندیشده و با خروجی روشن در هر مرحله."
                     if fa else "Transparent, time-boxed and with a clear deliverable at every stage."),
        grid(doc, [step_card(doc, i, t_, b_, fa=fa, delay=n * 100)
                   for n, (i, t_, b_, _) in enumerate(steps)], gap_value=34),
    ], bg=BG_WHITE, element_id="process")


# ===========================================================================
# 8. CASE STUDIES
# ===========================================================================

def case_studies(doc: Doc, *, fa: bool = False, limit: int = 3) -> Dict[str, Any]:
    cases = [
        ("case_retail", "خردهفروشی" if fa else "Retail",
         "فروشگاه شمال" if fa else "Northwind Retail",
         "عامل پشتیبانی چندزبانه، ۳۸٪ هزینه کمتر" if fa else
         "A multilingual support agent cut cost per ticket by 38%",
         "−38%", "هزینه هر تیکت" if fa else "Cost per ticket",
         "پرونده کامل" if fa else "Read the case study"),
        ("case_fintech", "فناوری مالی" if fa else "Fintech",
         "کیاستون بانک" if fa else "Keystone Bank",
         "بازبینی انطباق از ۹ روز به ۴ ساعت" if fa else
         "Compliance review went from 9 days to 4 hours",
         "۴ ساعت" if fa else "4 hrs", "زمان بازبینی" if fa else "Review time",
         "پرونده کامل" if fa else "Read the case study"),
        ("case_health", "سلامت" if fa else "Healthcare",
         "مرکز هلثلاین" if fa else "Helios Health",
         "صف تماس ۶۴٪ کوتاهتر با همراه بالینی" if fa else
         "A clinical copilot shortened the call queue by 64%",
         "−64%", "طول صف تماس" if fa else "Queue length",
         "پرونده کامل" if fa else "Read the case study"),
    ][:limit]
    cards = [
        case_card(doc, image_key=k, alt=t_, tag=tag, title=t_, metric=m,
                  metric_label=ml, link_url="#portfolio", delay=n * 110, fa=fa,
                  link_text=lt, col_kw=flex_item(3))
        for n, (k, tag, t_, _sub, m, ml, lt) in enumerate(cases)
    ]
    return _band(doc, [
        section_head(doc, fa=fa,
                     eyebrow="پروندهها" if fa else "Case studies",
                     title="نتیجه در عمل" if fa else "Outcomes, in production",
                     lead="سه پروژه واقعی با معیارهایی که تیم مالی هم قبول دارد."
                     if fa else "Three real rollouts, measured on metrics finance also signs off on."),
        grid(doc, cards, gap_value=26),
        flexrow(doc, [button(doc, "همه پروندهها" if fa else "Browse all case studies",
                             "#portfolio", variant="outline", size="md")],
                gap_value=0, justify="center"),
    ], bg=BG_PAGE, element_id="portfolio")


# ===========================================================================
# 9. TESTIMONIALS
# ===========================================================================

def testimonials(doc: Doc, *, fa: bool = False, dark: bool = False) -> Dict[str, Any]:
    data = [
        ("ما آرورا را برای یک کاربرد کوچک آوردیم و در یک فصل به ستون اصلی "
         "زیرساخت محصول تبدیل شد. تفاوت اصلی، ارزیابیهای درونساخت است."
         if fa else
         "We brought Aurora in for one narrow use case and it became our product "
         "infrastructure within a quarter. The built-in evaluations are the difference.",
         "لنا مارتین" if fa else "Lena Martin", "مدیر محصول، نورثویند" if fa else "Head of Product, Northwind"),
        ("نخستین انتشار در دوازده روز. مهندسان ما کد کمتری نوشتند و اعتماد بیشتری داشتند."
         if fa else
         "Twelve days to our first production release. Our engineers wrote less glue code "
         "and trusted the rollout far more.",
         "دکتر آرمان رضایی" if fa else "Dr. Arman Rezaei", "معمار ارشد، کیاستون" if fa else "Principal Architect, Keystone"),
        ("بازبینی انطباق از یک هفته به یک بعدازظهر رسید. تیم حقوقی از آنچه میبیند راضی است."
         if fa else
         "Compliance review went from a week to an afternoon. Legal can finally see exactly "
         "what the model saw.",
         "سارا چن" if fa else "Sara Chen", "مدیر انطباق، هلیوس" if fa else "Compliance Lead, Helios"),
    ]
    cards = [
        quote_card(doc, quote=q, name=n, role=r, delay=i * 110, fa=fa, dark=dark,
                   col_kw=flex_item(3))
        for i, (q, n, r) in enumerate(data)
    ]
    head_text = tk.G["muted_dark"] if dark else None
    return _band(doc, [
        section_head(doc, fa=fa,
                     eyebrow="نظر مشتریان" if fa else "Customer voices",
                     title="تیمها چه میگویند" if fa else "What teams say after a year",
                     lead="بدون عبارتهای تبلیغاتی - فقط نتیجه کار."
                     if fa else "No slogans, just what changed after the rollout.",
                     title_color=tk.G["white"] if dark else None,
                     lead_color=head_text),
        grid(doc, cards, gap_value=26),
    ], bg=BG_DARK if dark else BG_WHITE, element_id="testimonials")


# ===========================================================================
# 10. PRICING TABLE
# ===========================================================================

def pricing_table(doc: Doc, *, fa: bool = False, show_note: bool = True) -> Dict[str, Any]:
    plans = [
        dict(plan="شروع" if fa else "Starter", price="$0", period="برای همیشه رایگان" if fa else "free forever",
             blurb="برای ساخت نخستین عامل و آزمایش ایده."
             if fa else "For building your first agent and testing an idea.",
             features=["۱ پروژه فعال" if fa else "1 active project",
                       "۵۰٬۰۰۰ فراخوانی مدل در ماه" if fa else "50k model calls / month",
                       "عاملهای بصری" if fa else "Visual agent builder",
                       "پشتیبانی انجمن" if fa else "Community support"],
             cta="شروع کنید" if fa else "Start building"),
        dict(plan="رشد" if fa else "Growth", price="$490", period="/ ماه" if fa else "/ month",
             blurb="برای تیمهایی که در حال رساندن عامل به تولید هستند."
             if fa else "For teams taking an agent to production.",
             features=["۱۰ پروژه فعال" if fa else "10 active projects",
                       "۲ میلیون فراخوانی مدل" if fa else "2M model calls",
                       "ارزیابی و مجموعه طلایی" if fa else "Evaluations & golden sets",
                       "محافظهای سازمانی" if fa else "Guardrails & PII redaction",
                       "پشتیبانی ۲۴ ساعته" if fa else "Priority support, 4h SLA"],
             cta="شروع دوره" if fa else "Start 14-day trial",
             featured=True, badge_text="محبوبترین" if fa else "Most popular"),
        dict(plan="سازمانی" if fa else "Enterprise", price="تماس" if fa else "Talk to us",
             period="" if fa else "", blurb="برای سازمانهای با الزامات انطباقی."
             if fa else "For regulated organisations with bespoke needs.",
             features=["پروژه نامحدود" if fa else "Unlimited projects",
                       "حجم سفارشی" if fa else "Custom volume pricing",
                       "استقرار در منطقه شما" if fa else "Regional data residency",
                       "SSO و SCIM" if fa else "SSO & SCIM",
                       "مدیر موفقیت اختصاصی" if fa else "Dedicated success manager"],
             cta="گفتگو با فروش" if fa else "Contact sales"),
    ]
    cards = [
        pricing_card(doc, fa=fa, delay=i * 110, **p) for i, p in enumerate(plans)
    ]
    note = ("همه قیمتها بدون مالیات است. میتوانید هر زمان لغو کنید."
            if fa else
            "All prices exclude tax. Cancel any time - no lock-in contracts.")
    return _band(doc, [
        section_head(doc, fa=fa,
                     eyebrow="قیمتگذاری" if fa else "Pricing",
                     title="قیمت شفاف، بدون تله" if fa else "Straightforward pricing, no traps",
                     lead="شروع رایگان است؛ فقط وقتی رشد کردید پرداخت میکنید."
                     if fa else "Start free and pay only when the agent starts earning its keep."),
        grid(doc, cards, gap_value=26, align="stretch"),
        text(doc, "<p>%s</p>" % note, global_style=tk.T["fa_body"] if fa else tk.T["text"],
             color=tk.G["muted"], align="center") if show_note else spacer(doc, 1),
    ], bg=BG_PAGE, element_id="pricing")


# ===========================================================================
# 11. FAQ
# ===========================================================================

FAQ_EN = [
    ("What do we need to get started?",
     "A product owner, access to a representative dataset and one engineer. We run the "
     "first workshop inside your workspace, so nothing leaves your environment."),
    ("Which models can Aurora orchestrate?",
     "Aurora is model-agnostic. Route between OpenAI, Anthropic, Google, Mistral and your "
     "own fine-tunes per step, and switch providers without touching application code."),
    ("How do you handle data privacy?",
     "Data can stay in the EU or the US, is encrypted in transit and at rest, and PII is "
     "redacted before it reaches a model. We are SOC 2 Type II certified and GDPR ready."),
    ("Can we self-host?",
     "Yes. The Enterprise plan ships as a container image you can run inside your own VPC, "
     "with the control plane either managed or fully air-gapped."),
    ("What does onboarding cost?",
     "Growth includes a guided 30-day onboarding. Enterprise engagements include a named "
     "success manager and a quarterly review of your agent portfolio."),
    ("Is there a long-term contract?",
     "Monthly plans are month-to-month. Annual agreements include a discount and a "
     "commercial SLA with committed uptime and response times."),
]
FAQ_FA = [
    ("برای شروع به چه چیزی نیاز داریم؟",
     "یک مالک محصول، دسترسی به یک مجموعه داده نماینده و یک مهندس. نخستین کارگاه را "
     "داخل محیط خودتان برگزار میکنیم تا هیچ دادهای خارج نشود."),
    ("آرورا از چه مدلهایی پشتیبانی میکند؟",
     "آرورا مستقل از مدل است. میتوانید میان OpenAI، Anthropic، Google، Mistral و "
     "مدلهای آموزشدیده خودتان در هر مرحله جابهجا شوید."),
    ("امنیت داده چگونه تأمین میشود؟",
     "دادهها میتوانند در اروپا یا آمریکا بمانند، در انتقال و ذخیره رمزنگاری میشوند و "
     "دادههای هویتی پیش از ارسال به مدل حذف میشوند."),
    ("امکان میزبانی روی سرور خودمان وجود دارد؟",
     "بله. نسخه سازمانی بهصورت ایمیج کانتینری ارائه میشود که میتوانید داخل VPC خود "
     "اجرا کنید، بهصورت مدیریتشده یا کاملاً جدا از اینترنت."),
    ("هزینه راهاندازی چقدر است؟",
     "پلن رشد شامل ۳۰ روز راهاندازی هدایتشده است. قراردادهای سازمانی شامل مدیر موفقیت "
     "اختصاصی و بازبینی فصلی است."),
    ("آیا قرارداد بلندمدت لازم است؟",
     "پلنهای ماهانه بدون تعهد هستند. قرارداد سالانه شامل تخفیف و توافق سطح خدمت با "
     "زمان پاسخ تضمینشده است."),
]


def faq_accordion(doc: Doc, *, fa: bool = False, dark: bool = False,
                  items: Optional[Sequence[Dict[str, str]]] = None) -> Dict[str, Any]:
    source = items or [{"title": t, "content": c} for t, c in (FAQ_FA if fa else FAQ_EN)]
    content = accordion(
        doc, source,
        icon="fas fa-plus", active_icon="fas fa-minus",
        title_color=tk.G["white"] if dark else tk.G["secondary"],
        active_color=tk.G["primary"],
        content_color=tk.G["muted_dark"] if dark else tk.G["text"],
        title_style=tk.T["fa_heading"] if fa else tk.T["h3"],
        body_style=tk.T["fa_body"] if fa else tk.T["text"],
        title_bg="rgba(255,255,255,0.04)" if dark else tk.G["white"],
        content_bg="rgba(255,255,255,0.02)" if dark else tk.G["white"],
        border_color="rgba(255,255,255,0.12)" if dark else tk.G["line"],
        border_width=1, space=14, padding=dims(18, 22), faq_schema="yes",
    )
    head = section_head(doc, fa=fa,
                        eyebrow="پرسشهای پرتکرار" if fa else "FAQ",
                        title="پاسخ به پرسشهای رایج" if fa else "Questions we get every week",
                        lead="پاسخ خود را پیدا نکردید؟ تیم ما در دسترس است."
                        if fa else "Cannot find your answer? Our team replies the same day.",
                        title_color=tk.G["white"] if dark else None,
                        lead_color=tk.G["muted_dark"] if dark else None)
    return _band(doc, [head, content], bg=BG_DARK if dark else BG_WHITE, element_id="faq")


# ===========================================================================
# 12. CTA BAND
# ===========================================================================

def cta_band(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    inner_card = surface(doc, [
        flexcol(doc, [
            eyebrow_row(doc, "شروع کنیم" if fa else "Get started", align="left", fa=fa,
                        color=tk.G["primary"]),
            heading(doc, "آمادهاید نخستین عامل خود را منتشر کنید؟"
                    if fa else "Ready to ship your first agent?",
                    tag="h2", global_style=tk.T["fa_heading"] if fa else tk.T["h2"],
                    color=tk.G["white"],
                    font_size=slider(44), font_size_tablet=slider(34), font_size_mobile=slider(27),
                    animation="fadeInUp"),
            text(doc, "<p>%s</p>" % ("یک گفتگوی ۳۰ دقیقهای، بدون تعهد. مورد کاربرد خود را "
                                     "بیاورید و ما مسیر اجرا را روی همان ترسیم میکنیم."
                                     if fa else
                                     "A 30-minute call, no commitment. Bring one use case and we "
                                     "will sketch the path to production on it."),
                 global_style=tk.T["fa_body"] if fa else tk.T["lead"],
                 color=tk.G["muted_dark"], animation="fadeInUp", delay=80),
        ], gap_value=20, align="flex-start", extra={"flex_direction": "column", "boxed_width": slider(600)},
            **flex_item(0, basis=58, tablet_basis=100, mobile_basis=100, grow=0)),
        flexcol(doc, [
            button(doc, "رزرو جلسه" if fa else "Book the call", "#contact",
                   variant="primary", size="lg", align="center",
                   _element_width="100%", _element_custom_width=slider(100, "%"),
                   hover_animation="grow"),
            button(doc, "مشاهده مستندات" if fa else "Read the docs", "#docs",
                   variant="outline_light", size="lg", align="center",
                   _element_width="100%", _element_custom_width=slider(100, "%")),
            flexrow(doc, [
                icon(doc, "fas fa-clock", view="default", size=13, padding=0, primary=tk.G["primary"]),
                heading(doc, "پاسخ در همان روز کاری" if fa else "Same-day reply, Mon-Fri",
                        tag="p", global_style=tk.T["fa_label"] if fa else tk.T["text"],
                        color=tk.G["muted_dark"], letter_spacing=slider(0),
                        typography_font_size=slider(14)),
            ], gap_value=8, align="center", justify="center", wrap="nowrap"),
        ], gap_value=14, align="center", justify="center", extra={"flex_direction": "column"},
            **flex_item(0, basis=32, tablet_basis=100, mobile_basis=100, grow=0)),
    ], kind="card_dark", pad=48, pad_tablet=40, pad_mobile=28, gap_v=40,
        background={"background_background": "gradient",
                    "background_color": "#1C1917",
                    "background_color_b": "#2E2117",
                    "background_gradient_type": "linear",
                    "background_gradient_angle": slider(120, "deg")},
        border={"border_border": "solid", "border_width": dims(1),
                "border_color": "rgba(244,166,42,0.22)"},
        radius=tk.RADIUS["2xl"], shadow="xl")

    row = flexrow(doc, [inner_card], gap_value=0, align="stretch", justify="center",
                  extra={"flex_wrap": "wrap"})
    # make the CTA card fill the width on every device
    inner_card["settings"].update(flex_item(1, basis=100, grow=0)["flex_item"])
    return _band(doc, [row], bg=BG_PAGE, pad_y=(80, 64, 48), element_id="cta")


# ===========================================================================
# 13. TEAM
# ===========================================================================

TEAM = [
    ("Lena Martin", "لنا مارتین", "Founder & CEO", "بنیانگذار و مدیرعامل",
     "Previously product lead at two SaaS platforms.",
     "پیشتر مدیر محصول در دو شرکت SaaS."),
    ("Arman Rezaei", "آرمان رضایی", "CTO", "مدیر ارشد فناوری",
     "ML researcher and distributed-systems architect.",
     "پژوهشگر یادگیری ماشین و معمار سیستمهای توزیعشده."),
    ("Sara Chen", "سارا چن", "Head of Design", "سرپرست طراحی",
     "Designs data-dense products for technical teams.",
     "طراح تجربههای دادهمحور برای تیمهای فنی."),
    ("Navid Karimi", "نوید کریمی", "Head of Customer Success", "سرپرست موفقیت مشتری",
     "Guides teams from pilot to scale.", "همراه تیمها از پایلوت تا مقیاس."),
]


def team_grid(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    cards = []
    for idx, (en_name, fa_name, en_role, fa_role, en_bio, fa_bio) in enumerate(TEAM):
        name = fa_name if fa else en_name
        initials = "".join([p[0] for p in name.split()[:2]])
        cards.append(flexcol(doc, [
            flexrow(doc, [
                heading(doc, initials, tag="span", global_style=tk.T["h3"],
                        color=tk.G["amber_600"], letter_spacing=slider(0),
                        settings={"_element_width": "100%"}),
            ], gap_value=0, align="center", justify="center", wrap="nowrap",
                extra={"background_background": "classic",
                       "background_color": tk.G["amber_100"],
                       "border_radius": dims(tk.RADIUS["pill"]),
                       "padding": dims(14), "_element_width": "initial",
                       "_element_custom_width": slider(64)}),
            heading(doc, name, tag="h3",
                    global_style=tk.T["fa_heading"] if fa else tk.T["h3"],
                    color=tk.G["secondary"]),
            heading(doc, fa_role if fa else en_role, tag="p",
                    global_style=tk.T["fa_label"] if fa else tk.T["eyebrow"],
                    color=tk.G["amber_600"], letter_spacing=slider(1) if not fa else slider(0),
                    typography_font_size=slider(12)),
            text(doc, "<p>%s</p>" % (fa_bio if fa else en_bio),
                 global_style=tk.T["fa_body"] if fa else tk.T["text"],
                 color=tk.G["text"], typography_font_size=slider(16)),
            flexrow(doc, [
                icon(doc, "fab fa-linkedin-in", library="fa-brands", view="default",
                     size=15, padding=0, primary=tk.G["muted"]),
                icon(doc, "fab fa-x-twitter", library="fa-brands", view="default",
                     size=15, padding=0, primary=tk.G["muted"]),
            ], gap_value=14, align="center"),
        ], gap_value=14, align="flex-start",
            background={"background_background": "classic", "background_color": tk.G["white"]},
            border={"border_border": "solid", "border_width": dims(1),
                    "border_color": tk.G["line"]},
            radius=tk.RADIUS["lg"],
            animation="fadeInUp", animation_delay=idx * 100,
            extra={"padding": dims(28), "padding_mobile": dims(22),
                   "flex_direction": "column"},
            **flex_item(4)))
    return _band(doc, [
        section_head(doc, fa=fa,
                     eyebrow="تیم" if fa else "The team",
                     title="آدمهایی که پشت آرورا هستند" if fa else "The people behind Aurora",
                     lead="تیمی کوچک از مهندسان، پژوهشگران و طراحان با سابقه اجرا."
                     if fa else "A small team of engineers, researchers and designers who ship."),
        grid(doc, cards, gap_value=26),
    ], bg=BG_WHITE, element_id="team")


# ===========================================================================
# 14. CONTACT
# ===========================================================================

def contact_section(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    labels = {
        "eyebrow": "تماس" if fa else "Contact",
        "title": "گفتگو را شروع کنیم" if fa else "Let's start the conversation",
        "lead": "فرم را پر کنید یا مستقیماً تماس بگیرید؛ در همان روز کاری پاسخ میدهیم."
        if fa else "Fill in the form or reach us directly - we reply within one business day.",
        "name": "نام و نام خانوادگی" if fa else "Full name",
        "email": "ایمیل کاری" if fa else "Work email",
        "company": "نام شرکت" if fa else "Company",
        "budget": "بازه بودجه" if fa else "Budget range",
        "message": "درباره پروژه بگویید" if fa else "Tell us about the project",
        "consent": "با سیاست حفظ حریم خصوصی موافقم" if fa else
                   "I agree to the privacy policy and to being contacted about my enquiry.",
        "submit": "ارسال پیام" if fa else "Send message",
    }
    fields = [
        form_field("name", labels["name"], kind="text",
                   placeholder="نگار احمدی" if fa else "Jane Cooper", required=True, width="48"),
        form_field("email", labels["email"], kind="email",
                   placeholder="name@company.com", required=True, width="52"),
        form_field("company", labels["company"], kind="text",
                   placeholder="شرکت شما" if fa else "Your company", width="48"),
        form_field("budget", labels["budget"], kind="select", width="52",
                   options=(['— انتخاب کنید —', 'زیر ۱۰ هزار دلار', '۱۰ تا ۵۰ هزار دلار', 'بیش از ۵۰ هزار دلار']
                            if fa else ['— Select —', 'Under $10k', '$10k – $50k', 'Over $50k'])),
        form_field("message", labels["message"], kind="textarea", rows=5,
                   placeholder="کوتاه از هدف و زمانبندی بنویسید."
                   if fa else "A few lines about the goal and your timeline.",
                   required=True, width="100"),
        form_field("privacy", "privacy", kind="acceptance",
                   placeholder=labels["consent"], required=True, width="100"),
    ]
    form_widget = form(
        doc, fields, button_text=labels["submit"], form_name="Aurora contact",
        email_to="hello@aurora.example",
        email_subject="New project enquiry - aurora.example",
        button_align="center", button_size="lg", button_width="100",
        input_size="md",
        label_color=tk.G["secondary"], field_text_color=tk.G["secondary"],
        field_bg=tk.G["white"], field_border_color=tk.G["line"], radius=12,
        field_border_radius=dims(12), field_padding=dims(14, 16),
        _element_width="100%",
    )
    left = surface(doc, [form_widget], kind="card", pad=36, pad_mobile=24,
                   animation="fadeInUp",
                   **flex_item(0, basis=56, tablet_basis=100, mobile_basis=100, grow=0))

    info = flexcol(doc, [
        contact_line(doc, "fas fa-envelope", "ایمیل" if fa else "Email",
                     "hello@aurora.example", "mailto:hello@aurora.example", fa=fa),
        contact_line(doc, "fas fa-phone-alt", "تلفن" if fa else "Phone",
                     "+31 20 123 4567", "tel:+31201234567", fa=fa),
        contact_line(doc, "fas fa-comments", "پشتیبانی" if fa else "Support",
                     "support@aurora.example", "mailto:support@aurora.example", fa=fa),
        divider(doc, color="rgba(255,255,255,0.12)", width=100, weight=1, gap=0,
                _element_width="100%"),
        flexrow(doc, [
            icon(doc, "fas fa-map-marker-alt", view="default", size=17, padding=0,
                 primary=tk.G["primary"]),
            flexcol(doc, [
                heading(doc, "دفتر مرکزی" if fa else "Headquarters", tag="p",
                        global_style=tk.T["eyebrow"], color=tk.G["muted_dark"],
                        letter_spacing=slider(1.1) if not fa else slider(0),
                        typography_font_size=slider(12)),
                heading(doc, "Keizersgracht 241, Amsterdam" if not fa else
                        "کیزرزگراخت ۲۴۱، آمستردام", tag="p", global_style=tk.T["text"],
                        color=tk.G["white"], letter_spacing=slider(0)),
            ], gap_value=3),
        ], gap_value=14, align="flex-start", wrap="nowrap"),
        spacer(doc, 8),
        heading(doc, "ساعات پاسخگویی" if fa else "Response hours", tag="p",
                global_style=tk.T["eyebrow"], color=tk.G["muted_dark"],
                letter_spacing=slider(1.1) if not fa else slider(0),
                typography_font_size=slider(12)),
        heading(doc, "دوشنبه تا جمعه، ۹ تا ۱۸ (CET)" if fa else "Monday to Friday, 09:00-18:00 CET",
                tag="p", global_style=tk.T["text"], color=tk.G["white"],
                letter_spacing=slider(0)),
    ], gap_value=18, align="flex-start")

    right = surface(doc, [
        eyebrow_row(doc, "راههای ارتباطی" if fa else "Talk to us", align="left", fa=fa,
                    color=tk.G["primary"]),
        heading(doc, "پاسخ سریع، بدون بازاریابی" if fa else "A fast answer, no sales theatre",
                tag="h2", global_style=tk.T["fa_heading"] if fa else tk.T["h2"],
                color=tk.G["white"],
                font_size=slider(32), font_size_mobile=slider(25)),
        info,
        divider(doc, color="rgba(255,255,255,0.12)", width=100, weight=1, gap=0,
                _element_width="100%"),
        social_icons(doc, [
            {"icon": "fab fa-linkedin-in", "url": "#"},
            {"icon": "fab fa-x-twitter", "url": "#"},
            {"icon": "fab fa-github", "url": "#"},
        ], shape="circle", size="sm", padding=11, spacing=10, icon_size=15,
            icon_primary_color=tk.G["ink_800"], icon_secondary_color=tk.G["white"],
            hover_primary_color=tk.G["primary"], hover_secondary_color=tk.G["ink_900"]),
    ], kind="card_dark", pad=36, pad_mobile=26, gap_v=22, animation="fadeInUp",
        animation_delay=100,
        **flex_item(0, basis=42, tablet_basis=100, mobile_basis=100, grow=0))

    head = section_head(doc, fa=fa, eyebrow=labels["eyebrow"], title=labels["title"],
                        lead=labels["lead"])
    return _band(doc, [
        head,
        flexrow(doc, [left, right], gap_value=32, align="flex-start", justify="space-between",
                extra={"flex_gap_mobile": gap(24)}),
    ], bg=BG_PAGE, element_id="contact")


# ===========================================================================
# 15. NEWSLETTER
# ===========================================================================

def newsletter_band(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    copy = flexcol(doc, [
        eyebrow_row(doc, "خبرنامه" if fa else "Newsletter", align="left", fa=fa),
        heading(doc, "ماهانه یک ایمیل، بدون تبلیغ" if fa else "One email a month, zero fluff",
                tag="h2", global_style=tk.T["fa_heading"] if fa else tk.T["h2"],
                color=tk.G["secondary"],
                font_size=slider(34), font_size_mobile=slider(24),
                animation="fadeInUp"),
        text(doc, "<p>%s</p>" % ("یادداشتهای مهندسی، الگوهای ارزیابی و تحلیل انتشارها."
                                 if fa else
                                 "Engineering notes, evaluation patterns and release write-ups "
                                 "from the team building Aurora."),
             global_style=tk.T["fa_body"] if fa else tk.T["lead"],
             color=tk.G["text"]),
    ], gap_value=16, align="flex-start", extra={"flex_direction": "column"},
        **flex_item(0, basis=52, tablet_basis=100, mobile_basis=100, grow=0))

    form_widget = form(
        doc, [
            form_field("email", "ایمیل" if fa else "Email", kind="email",
                       placeholder="name@company.com", required=True, width="100"),
        ],
        button_text="عضویت" if fa else "Subscribe",
        form_name="Aurora newsletter", email_to="newsletter@aurora.example",
        email_subject="Newsletter signup", button_align="center", button_size="md",
        button_width="100", label_color=tk.G["secondary"],
        field_text_color=tk.G["secondary"], field_bg=tk.G["white"],
        field_border_color=tk.G["line"], radius=12,
        _element_width="100%",
    )
    right = surface(doc, [
        heading(doc, "بدون هرزنامه. هر زمان لغو کنید." if fa else "No spam. Unsubscribe in one click.",
                tag="p", global_style=tk.T["fa_label"] if fa else tk.T["text"],
                color=tk.G["muted"], letter_spacing=slider(0), typography_font_size=slider(14)),
        form_widget,
    ], kind="card", pad=28, pad_mobile=22, gap_v=14, animation="fadeInUp", animation_delay=100,
        **flex_item(0, basis=42, tablet_basis=100, mobile_basis=100, grow=0))

    return _band(doc, [
        flexrow(doc, [copy, right], gap_value=40, align="center", justify="space-between",
                extra={"flex_gap_mobile": gap(26)}),
    ], bg=BG_WARM, pad_y=(80, 64, 48), element_id="newsletter")


# ===========================================================================
# 16. CONTENT TWO COLUMN (about story)
# ===========================================================================

def content_two_column(doc: Doc, *, fa: bool = False) -> Dict[str, Any]:
    copy = flexcol(doc, [
        eyebrow_row(doc, "داستان ما" if fa else "Our story", align="left", fa=fa),
        heading(doc, "ساخت هوش مصنوعی باید انسانی و آرام باشد"
                if fa else "Shipping AI should feel calm, not chaotic",
                tag="h2", global_style=tk.T["fa_heading"] if fa else tk.T["h2"],
                color=tk.G["secondary"],
                font_size=slider(40), font_size_tablet=slider(32), font_size_mobile=slider(26),
                animation="fadeInUp"),
        text(doc, "<p>%s</p>" % ("آرورا در سال ۲۰۲۱ با یک ایده ساده شروع شد: ابزارهای هوش "
                                 "مصنوعی باید به اندازه ابزارهای طراحی امروزی دلپذیر باشند. "
                                 "امروز تیمهایی در ۱۴ کشور روی آرورا میسازند."
                                 if fa else
                                 "Aurora started in 2021 with a simple idea: AI tooling should be "
                                 "as pleasant to use as the design tools we already love. Today "
                                 "teams in 14 countries build on it."),
             global_style=tk.T["fa_body"] if fa else tk.T["lead"],
             color=tk.G["text"]),
        icon_list(doc, [
            {"text": "میانگین ۱۴ سال تجربه مهندسی" if fa else "Median 14 years of engineering experience",
             "icon": "fas fa-check"},
            {"text": "۱۴ کشور، ۹ زبان" if fa else "14 countries, 9 languages spoken",
             "icon": "fas fa-check"},
            {"text": "بدون سرمایهگذار خطرپذیر، سودآور" if fa else "Bootstrapped and profitable since 2023",
             "icon": "fas fa-check"},
        ], space=12, icon_size=15, icon_color=tk.G["primary"],
            text_color=tk.G["text"],
            style=tk.T["fa_body"] if fa else tk.T["text"],
            typography_font_size=slider(16)),
        button(doc, "درباره تیم" if fa else "Meet the team", "#about",
               variant="dark", size="md", icon="fas fa-arrow-right", icon_align="right"),
    ], gap_value=20, align="flex-start", extra={"flex_direction": "column"},
        **flex_item(0, basis=50, tablet_basis=100, mobile_basis=100, grow=0))

    media = flexcol(doc, [
        image(doc, tk.img_url("about"),
              alt="Aurora AI studio in Amsterdam" if not fa else "استودیوی آرورا در آمستردام",
              size="large", width=100, width_unit="%", object_fit="cover",
              radius=tk.RADIUS["lg"]),
    ], gap_value=0, align="center",
        background={"background_background": "classic", "background_color": tk.G["white"]},
        border={"border_border": "solid", "border_width": dims(1), "border_color": tk.G["line"]},
        radius=tk.RADIUS["xl"], shadow="md",
        extra={"padding": dims(10), "padding_mobile": dims(8)},
        **flex_item(0, basis=46, tablet_basis=100, mobile_basis=100, grow=0))

    return _band(doc, [
        flexrow(doc, [copy, media], gap_value=56, align="center", justify="space-between",
                extra={"flex_gap_mobile": gap(30)}),
    ], bg=BG_WHITE, element_id="story")


# ===========================================================================
# 17. PAGE HERO (inner pages)
# ===========================================================================

def page_hero(doc: Doc, *, fa: bool = False, eyebrow: str = "", title: str = "", lead: str = "",
              align: str = "center", breadcrumbs: bool = True) -> Dict[str, Any]:
    kids: List[Dict[str, Any]] = []
    if breadcrumbs:
        kids.append(widget(doc, "breadcrumbs", {
            "separator": "/", "show_home": "yes", "home_label": "خانه" if fa else "Home",
            "text_color": tk.G["muted"], "align": align,
            "typography_typography": tk.T["fa_label"] if fa else tk.T["text"],
            "typography_font_size": slider(14),
        }))
    kids.append(section_head(doc, fa=fa, eyebrow=eyebrow or None, title=title, lead=lead,
                             align=align, max_width=820))
    return _band(doc, [flexcol(doc, kids, gap_value=22,
                               align={"center": "center", "left": "flex-start"}.get(align, "center"))],
                 bg=BG_GRADIENT_HERO, pad_y=(72, 56, 40))
