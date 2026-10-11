#!/usr/bin/env python3
"""
Optimise the kit imagery.

    python3 tools/media.py            # process media/_raw/*.png -> media/*.jpg
    python3 tools/media.py --report    # list what would be produced

Source images live in media/_raw/ (kept out of the release download because the
raw PNGs are large). The optimised JPEGs in media/ are what the templates
reference and what gets uploaded as release assets.

Requires Pillow:  pip install pillow
"""

from __future__ import annotations

import argparse
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required:  pip install pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "media", "_raw")
OUT = os.path.join(ROOT, "media")

# target 3:2 landscape, matching the image slots used across the kit
TARGET_W, TARGET_H = 1500, 1000
QUALITY = 90

# raw filename -> optimised filename
MAP = {
    "hero-dashboard.png": "hero-dashboard.jpg",
    "highlight-agents.png": "highlight-agents.jpg",
    "highlight-insights.png": "highlight-insights.jpg",
    "case-retail.png": "case-retail.jpg",
    "case-fintech.png": "case-fintech.jpg",
    "case-health.png": "case-health.jpg",
    "about-studio.png": "about-studio.jpg",
}


def fit_cover(im: Image.Image, w: int, h: int) -> Image.Image:
    """Centre-crop to the target aspect ratio, then scale down to (w, h)."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    target_ratio = w / h
    src_ratio = im.width / im.height
    if src_ratio > target_ratio:                       # too wide -> crop sides
        new_w = int(round(im.height * target_ratio))
        left = (im.width - new_w) // 2
        im = im.crop((left, 0, left + new_w, im.height))
    elif src_ratio < target_ratio:                     # too tall -> crop top/bottom
        new_h = int(round(im.width / target_ratio))
        top = (im.height - new_h) // 2
        im = im.crop((0, top, im.width, top + new_h))
    if im.size != (w, h):
        im = im.resize((w, h), Image.LANCZOS)
    return im


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(RAW):
        sys.exit("missing %s" % RAW)

    total_in = total_out = 0
    missing = []
    print("Aurora AI - media pipeline  (%dx%d, JPEG q%d)" % (TARGET_W, TARGET_H, QUALITY))
    for src, dst in MAP.items():
        src_path = os.path.join(RAW, src)
        if not os.path.exists(src_path):
            missing.append(src)
            continue
        in_kb = os.path.getsize(src_path) / 1024.0
        total_in += in_kb
        if args.report:
            print("  %-26s -> %-24s %7.0f KB (source)" % (src, dst, in_kb))
            continue

        im = fit_cover(Image.open(src_path), TARGET_W, TARGET_H)
        dst_path = os.path.join(OUT, dst)
        im.save(dst_path, "JPEG", quality=QUALITY, optimize=True, progressive=True,
                subsampling=0)
        out_kb = os.path.getsize(dst_path) / 1024.0
        total_out += out_kb
        print("  %-26s -> %-24s %7.0f KB  (source %6.0f KB, -%d%%)"
              % (src, dst, out_kb, in_kb, round(100 - out_kb * 100 / in_kb)))

    if missing:
        print("  MISSING: %s" % ", ".join(missing))
    if not args.report:
        print("  total: %.0f KB -> %.0f KB (-%d%%)"
              % (total_in, total_out, round(100 - total_out * 100 / max(total_in, 1))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
