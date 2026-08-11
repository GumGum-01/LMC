#!/usr/bin/env python3
"""Print a ready-to-paste <style> block that embeds Tuyen_german_3 as a base64 data URI.

Usage: python3 scripts/build_font_face.py
Paste the output into the artifact's <head> (or an inline <style> tag), then
reference `font-family: 'Tuyen_german_3'` wherever the handwriting face is used.
"""
import base64
from pathlib import Path

FONT_PATH = Path(__file__).resolve().parent.parent / "assets" / "Tuyen_german_3-Regular.ttf"


def main() -> None:
    data = FONT_PATH.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    print(f"""<style>
@font-face {{
  font-family: 'Tuyen_german_3';
  src: url(data:font/ttf;base64,{b64}) format('truetype');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}}
</style>""")


if __name__ == "__main__":
    main()
