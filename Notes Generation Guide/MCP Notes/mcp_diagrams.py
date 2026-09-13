"""Universal SVG helpers for MCP study-note diagrams.

Chapter-specific diagram functions may be appended below these fixed helpers.
Do not alter helper geometry or palette without project-level approval.
"""

PRIMARY = "#6A2148"
PRIMARY_DARK = "#44172E"
PLUM = "#7D3F68"
MAUVE = "#A86488"
DUSTY_ROSE = "#C995AB"
BLUSH = "#E7CFD7"
PAPER = "#F7F0EC"
SURFACE = "#FBF8F5"
TEXT = "#2B252B"
SECONDARY = "#645761"
CODE = "#241D24"
BORDER = "#D7BCC7"


def _wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def box(x, y, w, h, label, fill=BLUSH, stroke=PRIMARY_DARK, text_color=TEXT,
        font_size=13, bold=True, max_chars=18, sub=None, sub_color=SECONDARY):
    lines = _wrap_text(label, max_chars)
    n = len(lines)
    line_h = font_size + 3
    total_h = n * line_h + (10 if sub else 0)
    start_y = y + h / 2 - total_h / 2 + font_size - 2
    tspans = "".join(
        f'<tspan x="{x + w/2}" y="{start_y + i*line_h}">{ln}</tspan>'
        for i, ln in enumerate(lines)
    )
    sub_svg = ""
    if sub:
        sub_svg = (
            f'<text x="{x + w/2}" y="{start_y + n*line_h + 3}" '
            f'text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif" '
            f'font-size="9.5" fill="{sub_color}">{sub}</text>'
        )
    weight = "bold" if bold else "normal"
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
        f'<text text-anchor="middle" font-family="Liberation Sans, Arial, sans-serif" '
        f'font-size="{font_size}" font-weight="{weight}" fill="{text_color}">{tspans}</text>'
        f'{sub_svg}'
    )


def arrow_down(x, y1, y2, color=SECONDARY, label=None, label_dx=8):
    lbl = ""
    if label:
        lbl = (
            f'<text x="{x+label_dx}" y="{(y1+y2)/2+3}" '
            f'font-family="Liberation Sans, Arial, sans-serif" font-size="8.8" '
            f'fill="{SECONDARY}">{label}</text>'
        )
    return (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" '
        f'stroke="{color}" stroke-width="1.8" marker-end="url(#arrow)"/>{lbl}'
    )


def arrow_right(x1, x2, y, color=SECONDARY, label=None, label_dy=-6):
    lbl = ""
    if label:
        lbl = (
            f'<text x="{(x1+x2)/2}" y="{y+label_dy}" text-anchor="middle" '
            f'font-family="Liberation Sans, Arial, sans-serif" font-size="8.6" '
            f'fill="{SECONDARY}">{label}</text>'
        )
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
        f'stroke="{color}" stroke-width="1.8" marker-end="url(#arrow)"/>{lbl}'
    )


def arrow_diag(x1, y1, x2, y2, color=PLUM, label=None, dash=False):
    dasharray = 'stroke-dasharray="4,3"' if dash else ""
    lbl = ""
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        lbl = (
            f'<text x="{mx}" y="{my-6}" text-anchor="middle" '
            f'font-family="Liberation Sans, Arial, sans-serif" font-size="8.6" '
            f'fill="{color}">{label}</text>'
        )
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="1.6" {dasharray} '
        f'marker-end="url(#arrow2)"/>{lbl}'
    )


DEFS = '''<defs>
<marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L6,3 L0,6 Z" fill="#645761"/></marker>
<marker id="arrow2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L6,3 L0,6 Z" fill="#7D3F68"/></marker>
</defs>'''
