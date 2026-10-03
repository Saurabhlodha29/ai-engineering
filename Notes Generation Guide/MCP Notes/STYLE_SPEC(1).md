# MCP Transcript-to-Notes PDF Styling Specification — Wine / Burgundy / Plum Editorial System

This is the complete mechanical styling and PDF-build specification for the **MCP AI Engineering Roadmap study-notes series**. It is designed for a fresh Claude session with no prior conversation memory. Follow it literally. Do not redesign, reinterpret, restyle, or “improve” the approved system.

This file controls **visual design and PDF build mechanics**. Lecture-specific content, chapter structure, explanation depth, source precedence, code handling, diagrams, Quick Revision, Key Takeaways, Revision Sheet, Interview Questions, Further Reading, QA, and Project Memory behavior are supplied by the separate generation prompt.

## 0. Non-Negotiable Project Rules

1. The MCP series uses a **wine / burgundy / plum / mauve** single-family visual identity.
2. Do not introduce blue, cyan, teal, green, emerald, or other cool-spectrum accents.
3. Do not introduce a new color family merely to create variety.
4. Normal pages use warm paper and pale blush/plum surfaces.
5. Code blocks may use a dark aubergine editor surface for readability.
6. The document is a premium technical textbook, not a dashboard, slide deck, poster, or generic documentation template.
7. The **cover is an immutable composition**. Never redesign it from prose or from visual intuition.
8. The canonical cover geometry lives in `mcp_cover_template.svg`.
9. The canonical MCP symbol lives in `mcp_symbol.svg`.
10. `mcp_cover_renderer.py` is the only approved mechanism for substituting chapter-specific text into the cover template.
11. `mcp_style.css` is the canonical stylesheet. Copy/use it as supplied. Do not rewrite its visual values from memory.
12. `mcp_diagrams.py` contains the shared SVG diagram helpers. Reuse them rather than inventing a separate helper system.
13. `mcp_cover_reference.png` is a visual QA reference only. It is not a license to redesign or recompose the cover.

## 1. Tech Stack & Environment

- Output format: PDF.
- Rendering engine: **WeasyPrint**.
- HTML + CSS + inline SVG are the canonical build technologies.
- Do not use ReportLab, pdfkit, wkhtmltopdf, PowerPoint, browser screenshots, or image-first PDF generation for ordinary interior pages.
- Use A4 portrait.
- Use only locally available fonts; do not use internet-hosted fonts.

### Approved fonts

- Headings / labels / UI / diagram text: `Liberation Sans`.
- Body text: `Liberation Serif`.
- Serif fallback: `DejaVu Serif`.
- Code: `Liberation Mono` with `DejaVu Sans Mono` fallback.

Do not reference Google Fonts, `@import url(...)`, or a web font.

## 2. Project Files — Locked Asset Set

The MCP project should contain these shared files alongside the generation prompt:

```text
STYLE_SPEC.md
mcp_style.css
mcp_diagrams.py
mcp_cover_template.svg
mcp_cover_renderer.py
mcp_symbol.svg
mcp_cover_reference.png
```

### File responsibilities

| File | Purpose | Can chapter generation modify it? |
|---|---|---|
| `STYLE_SPEC.md` | Mechanical visual/build specification | **No** |
| `mcp_style.css` | Canonical interior stylesheet | **No** |
| `mcp_diagrams.py` | Shared SVG primitives | **No**, except appending new chapter-specific functions when explicitly instructed |
| `mcp_cover_template.svg` | Canonical cover geometry | **Never** |
| `mcp_cover_renderer.py` | Safe text substitution into cover | **Never** |
| `mcp_symbol.svg` | Canonical MCP symbol asset | **Never** |
| `mcp_cover_reference.png` | Approved visual reference for QA | **Never** |

Never create `PROJECT_MEMORY.md`. Project Memory belongs in Claude's Project Memory textbox.

## 3. Color System — Locked

### 3.1 Palette

Use only the following palette for ordinary pages, components, diagrams, headings, borders, and metadata.

| Token | Hex | Semantic role |
|---|---|---|
| Primary Burgundy | `#6A2148` | Main identity, structural emphasis, strong headings |
| Deep Wine | `#44172E` | Dark structural surfaces, section bars, summary boxes |
| Plum | `#7D3F68` | Secondary structural accent, headings, diagrams |
| Muted Mauve | `#A86488` | Functional/revision accents, secondary borders |
| Dusty Rose | `#C995AB` | Highlights, numbered accents, code emphasis |
| Blush | `#E7CFD7` | Diagram nodes, light structural surfaces |
| Pale Blush | `#F1E0E6` | Important/attention surfaces |
| Soft Rose | `#F3E5EB` | Interview/secondary surfaces |
| Warm Paper | `#F7F0EC` | Primary page and cover background |
| White-Warm | `#FBF8F5` | Neutral cards, Quick Revision surfaces, diagram canvas |
| Warm Border | `#D7BCC7` | Borders, dividers, table rules |
| Primary Text | `#2B252B` | Body and structural text |
| Secondary Text | `#645761` | Supporting copy and labels |
| Code Background | `#241D24` | Code blocks |
| Code Text | `#F8F0EC` | Code text |

### 3.2 Semantic usage

- Burgundy / deep wine = structure and identity.
- Plum = section/subsection emphasis.
- Mauve = functional and revision-oriented information.
- Dusty rose = subtle emphasis and numbering.
- Blush / pale blush = large light surfaces.
- Warm paper = page canvas.
- Aubergine = code only.

Do not introduce yellow, orange, red-orange, teal, turquoise, blue, green, or cyan into ordinary non-code content.

Do not use gradients on ordinary pages.

## 4. Page Geometry

### Interior pages

- Page size: **A4 portrait**.
- Margins: `20mm 16mm 20mm 16mm` (top, right, bottom, left).
- Footer centered at the bottom.
- Footer text must be dynamically patched per chapter by the build script.
- Format:

```text
Chapter <N> · <Chapter Title>  —  <page number>
```

The canonical stylesheet contains the placeholder `__MCP_FOOTER__`. Do not hardcode a chapter-specific footer into `mcp_style.css`.

### Page composition

Treat the PDF as one continuous book. Do not insert page breaks merely because a new component starts. Reflow content globally to produce dense, balanced, readable pages.

Avoid:

- large empty areas;
- orphan headings;
- tiny components isolated on a page;
- diagrams separated from their explanation;
- code pushed to a new page while a large portion of the previous page is unused;
- accidental blank pages.

Do not over-compress simply to reduce page count.

## 5. COVER PAGE — IMMUTABLE DESIGN CONTRACT

The cover is the permanent visual identity of the MCP series. **Do not redesign it.**

### 5.1 Canonical asset

The only approved cover composition is `mcp_cover_template.svg`.

The file already contains:

- exact page background;
- left burgundy series rail;
- canonical MCP symbol position;
- vertical series navigation;
- upper-right geometric decoration;
- chapter label and divider;
- three-line title area;
- subtitle position;
- fixed Host / Client → MCP → MCP Server architecture diagram;
- fixed MCP symbol inside the central protocol block;
- fixed annotation beneath the diagram;
- lower metadata area;
- footer decoration.

Do not redraw these pieces in HTML/CSS/Python.

Do not replace the architecture diagram with Mermaid.

Do not use a different icon library.

Do not approximate the symbol with an icon font or Unicode character.

### 5.2 Cover dimensions

The SVG uses a fixed viewBox of `0 0 794 1123` and is rendered at exactly:

```text
210mm × 297mm
```

Do not change the viewBox, width, height, or aspect ratio.

### 5.3 Cover placement map

These coordinates are part of the canonical design and must remain unchanged:

| Element | Fixed region |
|---|---|
| Left rail | x = 0..136, full height |
| Main content start | x = 168 |
| Top kicker | y ≈ 64 |
| Chapter label | y ≈ 176 |
| Title block | y ≈ 270..404 |
| Title divider | y = 441 |
| Subtitle | y ≈ 488..538 |
| Architecture diagram | y ≈ 602..785 |
| Diagram annotation | y ≈ 829..883 |
| Lower metadata divider | y = 933 |
| Premium Revision Notes | y ≈ 973 |
| Metadata row | y ≈ 996..1058 |
| Bottom identity | y ≈ 1080..1102 |

These coordinates are not suggestions. They define the composition.

### 5.4 Cover asymmetry rule

The cover intentionally uses controlled asymmetry:

- heavy burgundy rail on the left;
- pale geometric arc in the upper right;
- small right-side BUILD / CONNECT / EXTEND labels;
- central MCP architecture centered within the main content field;
- lower-left rail arc and small dot field;
- lower-right identity line.

Do not "correct" this into a symmetrical layout.

### 5.5 Cover typography lock

The canonical cover uses:

- `Liberation Sans` for kicker, chapter label, title, labels, metadata, and diagram text;
- `Liberation Serif` for subtitle and Premium Revision Notes.

Do not substitute fonts.

Do not change title font size, weight, line height, or coordinates.

### 5.6 Cover variable content

Only these fields are allowed to change from chapter to chapter:

1. `CHAPTER_NUM` — e.g. `01`, `02`, `03`.
2. `TITLE` — chapter title, wrapped into **at most 3 lines**.
3. `SUBTITLE` — chapter promise, wrapped into **at most 3 lines**.

The cover's MCP architecture, symbols, side-rail labels, footer metadata labels, decorative shapes, and all geometry remain unchanged.

### 5.7 Cover text constraints

The approved renderer uses conservative wrapping because the cover must not change composition.

- Title wrapping limit: approximately 23 characters per line.
- Maximum title lines: 3.
- Subtitle wrapping limit: approximately 58 characters per line.
- Maximum subtitle lines: 3.

If a chapter title exceeds the available space, **shorten the chapter title**. Do not reduce font size, move the title, widen its region, or alter the diagram position.

If a subtitle exceeds three lines, rewrite it more concisely. Do not shrink it or move it.

### 5.8 Cover renderer contract

Use `mcp_cover_renderer.py`.

The build script should call:

```python
from mcp_cover_renderer import build_cover

cover_svg = build_cover(
    chapter_num=CHAPTER_NUM_PADDED,
    title=CHAPTER_TITLE,
    subtitle=CHAPTER_SUBTITLE,
)
```

Then place it inside:

```html
<div class="cover-svg-wrap">{cover_svg}</div>
```

Do not manually substitute SVG tokens in the chapter build script.

### 5.9 Cover anti-drift rules

Never:

- change the logo/symbol geometry;
- change connector routes;
- change arrowheads;
- change panel widths/heights;
- change title font size;
- add extra decorative lines or shapes;
- add chapter-specific diagrams to the cover;
- move the MCP block;
- replace the fixed MCP diagram with a different architecture;
- use Mermaid, CSS pseudo-elements, or flexbox to reconstruct the cover;
- crop the SVG differently;
- stretch the SVG non-proportionally.

The build script may substitute only the approved variable text fields.

## 6. Interior Visual System

The interior should visually connect to the cover while remaining calm enough for long reading sessions.

### Chapter header

Use the canonical `.chapter-header` from `mcp_style.css`.

### Major section heading

Use:

```html
<h2 class="section"><span class="num">1.</span>Section Title</h2>
```

The section bar is deep wine with white text and a dusty-rose section number.

### Subheading

Use `<h3 class="sub">...</h3>`.

Subheadings use Burgundy/Plum with a left plum rule.

### Micro heading

Use `<h4 class="micro">...</h4>` only for short flat sub-points.

## 7. Callouts

Use exactly these five kinds:

| Class | Label | Meaning |
|---|---|---|
| `important` | IMPORTANT | Core conceptual clarification |
| `interview` | INTERVIEW TIP | Interview framing |
| `mistake` | COMMON MISTAKE | Specific misconception or implementation error |
| `practice` | BEST PRACTICE | Actionable engineering guidance |
| `insight` | REAL WORLD INSIGHT | Contextual / practical implication |

Typical density: 1–3 per major section. Do not stack identical callouts back-to-back.

## 8. Tables

Use `<table>` for side-by-side comparisons. Use 2–4 columns where practical. Keep cells concise. Do not turn a comparison into prose when a table is clearly more useful.

## 9. Code Blocks

Use `.codeblock` for code.

- Full-width code: 8.6pt.
- Side-by-side comparison: `.code-compare`, 7.7pt.
- Use `.cmt` for comments / highlighted literals.
- Use `.kw` for highlighted syntax.
- Escape HTML-significant characters.

Do not shrink code below the canonical size merely to keep it on the current page.

## 10. Diagrams

All diagrams must be programmatic inline SVG.

Use the helpers in `mcp_diagrams.py`:

- `_wrap_text`
- `box`
- `arrow_down`
- `arrow_right`
- `arrow_diag`
- `DEFS`

Do not introduce another diagram framework.

### Diagram design principles

- topology before decoration;
- one technical idea per diagram;
- explicit node roles;
- clean, deliberate routing;
- no text over connector paths;
- no connector crossing through labels;
- no arbitrary icon clutter;
- no oversized empty viewBox;
- no decorative diagram whose only purpose is filling space.

### Diagram colors

Use the MCP palette consistently. Color must communicate semantic role rather than simply alternating for visual variety.

### Captions

Every diagram gets:

```html
<div class="diagram-wrap">
  {SVG}
  <div class="diagram-caption">Figure X.Y — concise caption.</div>
</div>
```

Figure numbers are sequential within the chapter.

## 11. Quick Revision

Every major topic ends with exactly one `.quick-revision` component. It should contain 3–5 concise, standalone facts.

## 12. Closing Components

Use the established order:

1. Key Takeaways
2. Revision Sheet
3. Interview Questions
4. Further Reading

These are flowing document components. Do not force each one onto a separate page.

## 13. Build Procedure

Every chapter build should follow this sequence:

```text
Inspect source files
      ↓
Determine chapter structure
      ↓
Generate HTML content
      ↓
Load mcp_style.css unchanged
      ↓
Generate chapter-specific SVG diagrams with mcp_diagrams.py helpers
      ↓
Generate canonical cover with mcp_cover_renderer.py
      ↓
Patch __MCP_FOOTER__ with chapter-specific footer text in memory
      ↓
Render with WeasyPrint
      ↓
Render every PDF page to PNG at 100 DPI
      ↓
Visually inspect every page
      ↓
Fix content/layout issues
      ↓
Render again
      ↓
Deliver only the final PDF
```

### Footer patch

The shared CSS must remain unchanged on disk.

Use:

```python
css_text = Path("mcp_style.css").read_text(encoding="utf-8")
css_text = css_text.replace(
    'content: "__MCP_FOOTER__";',
    f'content: "Chapter {CHAPTER_NUM} · {CHAPTER_TITLE}  —  " counter(page);'
)
```

Use the patched CSS only in the HTML string. Do not overwrite `mcp_style.css`.

## 14. Visual QA — Mandatory

After PDF generation, render **every page** to PNG and inspect every page.

### Cover QA

The cover fails QA if any of the following occurs:

- title overlaps subtitle or divider;
- title wraps into more than 3 lines;
- subtitle wraps into more than 3 lines;
- architecture panels move from their fixed positions;
- connectors overlap labels or panels incorrectly;
- the central MCP block changes size or location;
- the canonical symbol is replaced or redrawn;
- any decorative geometry changes;
- the lower metadata row moves significantly;
- the entire SVG is stretched or cropped.

### Interior QA

Check:

- no clipping or overflow;
- no awkward page breaks;
- code remains readable;
- code does not split at invalid logical boundaries;
- tables remain readable;
- diagrams remain close to their explanatory text;
- no orphan headings;
- no large avoidable blank areas;
- chapter number is correct;
- footer is correct;
- figure numbering is correct;
- color system remains wine/burgundy/plum;
- no cool-spectrum accents slipped into the interior.

If a visual problem appears, correct the build output. Do not weaken this specification to excuse the problem.

## 15. Reference Asset Usage

`mcp_cover_reference.png` is the approved visual reference corresponding to the selected MCP cover direction.

Use it only for visual QA/comparison. It does not replace the vector template and must not be traced manually for each chapter.

## 16. Output Convention

Use:

```text
/mnt/user-data/outputs/MCP_Chapter{N}_{Slug}_Notes.pdf
```

where `{Slug}` is the chapter title in `Title_Case_With_Underscores`.

Do not deliver HTML, CSS, Python, SVG, QA images, or internal logs unless explicitly requested. The user-facing deliverable is the completed PDF.

## 17. Final Anti-Drift Rule

When a chapter-generation decision conflicts with this styling specification:

> **Preserve the canonical MCP visual system.**

Do not reinterpret the cover. Do not modernize the palette. Do not switch fonts. Do not alter the geometry to fit a difficult title. Rewrite the chapter text to fit the fixed system instead.
