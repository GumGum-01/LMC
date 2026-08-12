---
name: tuyen-german-3-font
description: Applies the "Tuyen_german_3" font — a custom, personal handwritten typeface (single Regular weight, made with Calligraphr; full ASCII punctuation, the complete Vietnamese tone-mark alphabet, and German/Western-European accents) — as the default display/heading typeface for all artifacts (HTML, SVG, posters, dashboards, reports, slides, etc.) AND real documents (.docx, with genuine OOXML font embedding so it renders throughout the whole file for any reader, not just Gum's machine), pairing with the Tuyen_1 color theme skill. Default starting 2026-08-12 — before that date this is opt-in only, not automatic. Once active, use it automatically without asking, unless the user requests a different typeface for a specific piece. Trigger on "Tuyen_german_3", "handwriting font", "handwritten style", "custom font", "typeface", Vietnamese/"tiếng Việt" text wanting a personal touch, or any request to style/build an artifact or document.
compatibility: Core use (HTML/SVG artifacts, PIL, reportlab) is stdlib-only. scripts/embed_font_docx.py additionally needs `lxml` and `python-docx` (pip install lxml python-docx) — install them if missing rather than skipping real embedding.
---

# Tuyen_german_3 Font

A custom handwritten typeface, digitized with Calligraphr (`assets/Tuyen_german_3-Regular.ttf`).
It exists in a single Regular weight only — there is no bold or italic cut, so never set
`font-weight: bold` or `font-style: italic` on text using this family; browsers "fake" those by
squashing/slanting the glyphs, which looks broken on a handwriting face. Use size, color, or
letter-spacing for emphasis instead.

## Sizing: matching Arial's apparent size

At the same declared font-size, Tuyen_german_3 renders visibly smaller than Arial/system-sans — a
bare `font-size: 32px` looks noticeably weaker than Arial at 32px next to it. Measured directly
(fontTools glyph ink bounds, cross-checked by rendering both in Chromium and pixel-measuring the
result — **not** the font's own OS/2 `sxHeight`/`sCapHeight` metadata, which overstates this font's
x-height by ~24% versus its actual hand-drawn ink and would under-compensate if trusted, e.g. via
CSS `font-size-adjust: from-font`): x-height ratio 1.336, cap-height ratio 1.302 versus Liberation
Sans (the Arial-metric-compatible substitute used for the measurement). **Use 1.34** as the default
compensation — take the size you'd use for Arial/system-sans at the intended visual weight and
multiply it by 1.34 for Tuyen_german_3, by default, not just when someone complains it looks small.

`scripts/build_font_face.py`'s output already defines this as a `--tuyen-german-3-scale` CSS custom
property — use it instead of a bare `1.34` so a future re-measurement (e.g. if the font asset is
ever swapped for a redrawn version) only has to change in one place:

```css
font-size: calc(32px * var(--tuyen-german-3-scale)); /* 32px = the Arial-equivalent target size */
```

The same 1.34× applies wherever else a size is specified for this font — PIL `size=`, reportlab
point sizes, docx half-points — it's a property of the font's own proportions, not a CSS quirk, so
don't skip the compensation just because a particular surface isn't CSS.

## Scope: this is not a Claude-Code-only or "Artifact panel"-only thing

The font works anywhere Claude actually controls the byte-level output and can put the real font
data *inside* the deliverable: HTML/Markdown artifacts, inline SVG, generated images and PDFs, and
now `.docx` (see below) — all of these carry the font with them, so they display correctly for
anyone who opens them, on any device, not just this account.

The one real constraint is per-format, not per-surface: **can the library that builds this file type
actually embed the font bytes, or does it only let you write a font *name*?** That's the axis that
matters — "artifact vs. normal chat" isn't. A `.docx` produced in a normal chat reply and an HTML
artifact in the side panel are equally capable of carrying the real typeface; a `.pptx` is currently
the one exception (see below).

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

This prints a ready `<style>@font-face{...}</style>` block (including the `--tuyen-german-3-scale`
custom property from Sizing above). Put it in the artifact's `<head>` (or any `<style>` tag before
first use), then reference the family with a plain fallback for the rare character still outside
the set, and size it through the scale variable rather than a bare pixel value:

```css
font-family: 'Tuyen_german_3', ui-sans-serif, sans-serif;
font-size: calc(32px * var(--tuyen-german-3-scale)); /* 32px = the Arial-equivalent target size */
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

### Word documents (docx) — real embedding, applies throughout the whole file

`python-docx` alone only sets a font *name* on a run; it doesn't embed the file, so the document
falls back to a generic font for anyone without "Tuyen_german_3" installed — that used to be this
skill's default behavior here (name-only, heading-only, "ask Gum first"). That's fixed now:
`scripts/embed_font_docx.py` does real OOXML font embedding (the same mechanism Word itself uses —
ECMA-376 §17.8.6: the font bytes go into the package as an obfuscated part, declared in
`word/fontTable.xml`), **and** forces every run in the document to use it, not just headings. The
result displays the actual handwriting for any reader, in Word or LibreOffice, with nothing to
install.

Workflow: build the `.docx` normally first (the `docx` skill / `python-docx`), then post-process it:

```bash
python3 scripts/embed_font_docx.py input.docx output.docx assets/Tuyen_german_3-Regular.ttf Tuyen_german_3
```

The script self-checks before it prints success: the obfuscation round-trips back to the exact
original font bytes, every relationship it adds resolves to a real part, all touched XML is
well-formed, and `python-docx` — an independent reader — can re-open the result. Verified end-to-end
against LibreOffice (an independent, real OOXML consumer): both the heading and body render in the
actual handwriting, confirmed by rendering to PDF and reading the pages back, not just by the file
opening without error. If that self-check ever fails, don't hand back the file silently substituting
name-only mode — surface the failure so it gets fixed, since a wrong obfuscation key produces a
`.docx` that looks done but quietly falls back for the recipient, which is worse than the old honest
limitation.

### PowerPoint documents (pptx) — not yet extended, name-only for now

Same limitation the old docx guidance described: `python-pptx` sets a font name only. PPTX supports
real font embedding via the same ECMA-376 mechanism (under `ppt/fonts/` and
`ppt/presentation.xml`'s `<p:embeddedFontLst>` instead of Word's `fontTable.xml`), but that hasn't
been built or verified here yet — don't assume `embed_font_docx.py`'s approach transfers as-is
without checking the PPTX-specific XML shape first. If a deck needs the handwritten look throughout,
say so and offer to build + verify the pptx equivalent (same bug-fix/new-requirement authority as
everything else in this skill applies), rather than quietly shipping name-only and calling it done.

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

- **2026-08-12** — Gum asked for the default size to match Arial's. Measured the mismatch precisely
  instead of guessing a round number: fontTools glyph-ink bounds against Liberation Sans, cross-
  checked by rendering both fonts in Chromium and pixel-measuring the actual output (deliberately
  not trusting Tuyen_german_3's own OS/2 metadata, which turned out to overstate its x-height by
  ~24% versus real ink — would have produced a wrong, under-sized compensation). Landed on a 1.34×
  scale, exposed as `--tuyen-german-3-scale` in `build_font_face.py`'s output; see Sizing above.
- **2026-08-12** — Gum reported that `.docx` output only used the font on the heading and fell back
  everywhere else, and asked whether this skill even applies outside Claude Code artifacts (it does
  — see Scope above). Root cause was two things bundled together: a real technical gap
  (`python-docx` can't embed font files, only reference a name) and a design choice of mine
  (restricting it to headings) that I'd stated as if it were the same hard limitation. Added
  `scripts/embed_font_docx.py`: real OOXML font embedding, forced onto every run. Verified against
  LibreOffice end-to-end (rendered to PDF, read the pages back, confirmed heading *and* body both
  show the actual handwriting, not just that the file opens) — not merely "the code ran." PPTX still
  name-only; noted as available on request rather than silently left as-is.
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
- `scripts/embed_font_docx.py` — real OOXML font embedding for `.docx`, applied to every run (needs
  `lxml` + `python-docx`; see `compatibility` above).
