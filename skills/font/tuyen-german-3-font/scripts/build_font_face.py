#!/usr/bin/env python3
"""Print a ready-to-paste <style> block that embeds Tuyen_formal_font_VN_EN_DE_final as a base64 data URI.

Usage: python3 scripts/build_font_face.py
Paste the output into the artifact's <head> (or an inline <style> tag), then
reference `font-family: 'Tuyen_formal_font_VN_EN_DE_final'` wherever the handwriting face is used.

Includes a --tuyen-formal-font-vn-en-de-final-scale custom property (see ARIAL_SCALE below):
Tuyen_formal_font_VN_EN_DE_final's actual ink is meaningfully smaller than Arial/system-sans at
the same declared font-size, so a bare `font-size: 32px` looks weaker than
Arial at 32px. Multiply the Arial-equivalent target size by this scale
whenever sizing this font -- e.g. `font-size: calc(32px * var(--tuyen-formal-font-vn-en-de-final-scale))`.
"""
import base64
from pathlib import Path

FONT_PATH = Path(__file__).resolve().parent.parent / "assets" / "Tuyen_formal_font_VN_EN_DE_final.ttf"

# Measured empirically (Chromium pixel measurement of rendered 'H'/'x' ink,
# cross-checked against fontTools glyph bounding boxes -- NOT the font's own
# OS/2 sxHeight/sCapHeight metadata, which overstates this font's x-height by
# ~24% relative to its actual hand-drawn ink and would under-compensate if
# trusted, e.g. via CSS `font-size-adjust: from-font`). x-height ratio to
# Liberation Sans (Arial-metric-compatible) was 1.336, cap-height 1.302;
# 1.34 is a good single default for mixed-case text. Re-measure instead of
# hand-editing this if the font asset is ever swapped for a redrawn version.
ARIAL_SCALE = 1.34


def main() -> None:
    data = FONT_PATH.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    print(f"""<style>
@font-face {{
  font-family: 'Tuyen_formal_font_VN_EN_DE_final';
  src: url(data:font/ttf;base64,{b64}) format('truetype');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}
:root {{
  --tuyen-formal-font-vn-en-de-final-scale: {ARIAL_SCALE};
}}
</style>""")


if __name__ == "__main__":
    main()
