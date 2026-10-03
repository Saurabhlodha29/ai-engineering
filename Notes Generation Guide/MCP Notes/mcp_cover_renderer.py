"""Canonical MCP cover renderer.

The geometry lives in mcp_cover_template.svg. This module only substitutes
controlled chapter text; it never redraws or reinterprets the cover.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
TEMPLATE = BASE / "mcp_cover_template.svg"
TITLE_MAX_CHARS = 23
SUBTITLE_MAX_CHARS = 58


def _wrap(text: str, max_chars: int, max_lines: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if not current or len(candidate) <= max_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        raise ValueError(
            f"Text requires {len(lines)} lines but the canonical cover permits {max_lines}. "
            "Shorten the text instead of changing the cover geometry."
        )
    return lines


def _fill(lines: list[str], n: int) -> list[str]:
    return lines + [""] * (n - len(lines))


def build_cover(*, chapter_num: str, title: str, subtitle: str) -> str:
    svg = TEMPLATE.read_text(encoding="utf-8")
    title_lines = _fill(_wrap(title, TITLE_MAX_CHARS, 3), 3)
    subtitle_lines = _fill(_wrap(subtitle, SUBTITLE_MAX_CHARS, 3), 3)
    replacements = {
        "{{CHAPTER_NUM}}": escape(chapter_num),
        "{{TITLE_LINE_1}}": escape(title_lines[0]),
        "{{TITLE_LINE_2}}": escape(title_lines[1]),
        "{{TITLE_LINE_3}}": escape(title_lines[2]),
        "{{SUBTITLE_LINE_1}}": escape(subtitle_lines[0]),
        "{{SUBTITLE_LINE_2}}": escape(subtitle_lines[1]),
        "{{SUBTITLE_LINE_3}}": escape(subtitle_lines[2]),
    }
    for token, value in replacements.items():
        svg = svg.replace(token, value)
    if re.search(r"{{[A-Z0-9_]+}}", svg):
        raise ValueError("Unresolved cover template token remains.")
    return svg
