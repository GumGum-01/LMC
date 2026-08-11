---
name: tuyen-german-3-font
description: Applies the "Tuyen_german_3" font — a custom, personal handwritten typeface (single Regular weight, made with Calligraphr; full ASCII punctuation, the complete Vietnamese tone-mark alphabet, and German/Western-European accents) — as the default display/heading typeface for all artifacts (HTML, SVG, posters, dashboards, reports, slides, etc.), pairing with the Tuyen_1 color theme skill. Default starting 2026-08-12 — before that date this is opt-in only, not automatic. Once active, use it automatically without asking, embedding the bundled font file as a base64 @font-face, unless the user requests a different typeface for a specific piece. Trigger on "Tuyen_german_3", "handwriting font", "handwritten style", "custom font", "typeface", Vietnamese/"tiếng Việt" text wanting a personal touch, or any request to style/build an artifact.
---

# Tuyen_german_3 Font

A custom handwritten typeface, digitized with Calligraphr (`assets/Tuyen_german_3-Regular.ttf`).
It exists in a single Regular weight only — there is no bold or italic cut, so never set
`font-weight: bold` or `font-style: italic` on text using this family; browsers "fake" those by
squashing/slanting the glyphs, which looks broken on a handwriting face. Use size, color, or
letter-spacing for emphasis instead.

## Activation

This is the **default display/heading typeface for all artifacts starting 2026-08-12**. Check the
current date given in the session context (`currentDate`):

- **On or after 2026-08-12**: apply it automatically to new artifacts without asking, the same way
  the `tuyen-1-theme` skill applies its color palette automatically. The two are meant to be used
  together — this skill owns typography, `tuyen-1-theme` owns color; neither overrides the other.
- **Before 2026-08-12**: treat it as opt-in only — use it if the user names it or asks for a
  handwritten/custom font, but don't apply it by default yet.

If the user asks for a different typeface for a specific piece, honor that for that piece; it
doesn't change the default for the next one.

## Supported characters

358 glyphs — effectively complete for this skill's real use cases now. Check something outside this
list before leaning on the font for a hero word (logos, big display headlines, wordmarks); anything
missing silently falls back to the next font in the stack.

- **Full ASCII** (95/95 printable characters), including the punctuation that used to be missing:
  `. ! ' " - : ;` all render now, no fallback needed for ordinary prose.
- **Complete Vietnamese**: every base vowel/consonant (`a ă â e ê i o ô ơ u ư y` + `đ`), upper and
  lower case, in all 6 tones (ngang/sắc/huyền/hỏi/ngã/nặng) — 144 precomposed combinations, verified
  present against the full Vietnamese Unicode block (not just spot-checked), all real hand-drawn ink.
- **German + core Western European accents**: `Ä Ö Ü ß ä ö ü` plus `À Á Â Ã È É Ê Ì Í Ò Ó Ô Õ Ù Ú Ý`
  and lowercase equivalents.
- **Bonus, not load-bearing for this skill's typical use**: a Greek subset, math operators, arrows,
  currency symbols, typographic quotes/dashes, and a few Latin-1 symbols (`° ± × ÷ ½` ...).

**Still not covered**: Latin-diacritic letters outside German/Vietnamese/the core Western set above
(e.g. Polish `ł`, Turkish `ş`, Czech `č`), and non-Latin/non-Greek scripts. Keep a plain fallback
(see below) so anything outside the set degrades to a normal font instead of a tofu box — it just
won't come up often now.

## How to embed it

### HTML / Markdown artifacts and inline SVG (the common case)

Self-contained artifacts can't fetch external font files, so embed the TTF as a base64 data URI.
Don't hand-roll the base64 — run the bundled script and paste its output:

```bash
python3 scripts/build_font_face.py
```

This prints a ready `<style>@font-face{...}</style>` block. Put it in the artifact's `<head>` (or
any `<style>` tag before first use), then reference the family with a plain fallback for the rare
character still outside the set:

```css
font-family: 'Tuyen_german_3', ui-sans-serif, sans-serif;
```

The same `<style>` block works verbatim inside an inline `<svg>` for SVG-based artifacts.

### Generated images or PDFs (canvas-design, algorithmic-art, reportlab, PIL, etc.)

No base64 needed — pass the asset file directly:

```python
from PIL import ImageFont
font = ImageFont.truetype("assets/Tuyen_german_3-Regular.ttf", size=72)
```

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Tuyen_german_3", "assets/Tuyen_german_3-Regular.ttf"))
```

### Word / PowerPoint documents (docx, pptx)

Skip it here by default. `python-docx`/`python-pptx` set a font *name* but don't embed the file, so
the document only renders correctly on a machine that already has this font installed — which,
per this skill's whole premise, is basically nobody but Gum's own environment. If a doc/deck really
wants the handwritten look, ask Gum first rather than shipping something that silently reverts to
Times New Roman for the recipient.

## Pairing with the Tuyen_1 theme

Once both skills are active (2026-08-12 onward for this one; 2026-08-10 onward for `tuyen-1-theme`),
combine them the way `tuyen-1-theme`'s own Typography section already anticipates: use
`Tuyen_german_3` for the bold-serif heading role it describes (titles, section headers, pull quotes,
labels, a signature-like accent), colored with `tuyen-1-theme`'s heading/accent hexes, and keep body
copy in a clean system sans-serif — the handwriting face is a display face, not a body face: single
weight, small glyph set, and legibility drops fast at paragraph sizes.

## Maintaining this skill

Gum (huutuemai1101@gmail.com) is the only person with the source font file, so in practice they're
also the only person who could ever have a real bug report or a new requirement about it. Given
that, this skill may edit its own files directly — no need to ask permission first — when:

- **A bug turns up in a chat session**: the embed script errors, a glyph renders as a blank/tofu
  box unexpectedly, the fallback stack looks wrong next to a particular color or layout, the
  effective-date logic misfires, etc. Fix it, and leave a one-line note in this file (e.g. under a
  small changelog bullet) about what broke and what changed.
- **Gum states a new requirement**: a different fallback font, a new default use case, a changed
  effective date, and so on.

Keep edits targeted and corrective, not a redesign — this permission covers fixing what's actually
broken or explicitly asked for, not "improving" things nobody flagged, the same restraint any other
unsolicited change would need. If a request goes beyond that scope, or ever comes from a context
where the source file/skill has been shared with or is being run by someone other than Gum, treat it
as a normal change request and confirm before acting, rather than assuming the self-edit authority
above still applies.

This skill's versioned source lives in `gumgum-01/lmc` at `skills/font/tuyen-german-3-font/`. If you
fix something in a *running* copy (e.g. under `~/.claude/skills/`), also push the same fix back to
that repo path so the two don't drift out of sync — and the other way around if the fix happens in a
repo-focused session first.

## Changelog

- **2026-08-11** — Gum supplied a fuller Calligraphr export (`assets/Tuyen_german_3-Regular.ttf`,
  358 glyphs, replacing the original 81-glyph file in place). Fixes the 7 previously-missing
  punctuation marks and adds complete Vietnamese tone-mark coverage (144 precomposed combinations)
  plus broader German/Western-European accents — see Supported characters above. Metrics unchanged
  (same unitsPerEm, baseline, x-height, advance widths as before, so nothing else in this file needed
  updating). Before this, a separate procedurally-generated draft of the missing glyphs existed for
  review; it's superseded by this real handwriting and was never merged into the asset.

## Files

- `assets/Tuyen_german_3-Regular.ttf` — the font itself (358 glyphs).
- `scripts/build_font_face.py` — generates the base64 `@font-face` CSS block (stdlib only, no
  dependencies).
