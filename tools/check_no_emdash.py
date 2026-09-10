#!/usr/bin/env python3
"""Prohíbe la raya larga usada como delimitador de inciso en Proyecto I."""

from __future__ import annotations

import sys
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "reports/latex/ProyectoI_VisaPredictAI.tex"
EM_DASH = "—"


def aside_delimiter_hits(text: str) -> list[tuple[int, str]]:
    """Devuelve las rayas con espacio en exactamente uno de sus lados."""
    hits: list[tuple[int, str]] = []
    lines = text.splitlines()
    for index, char in enumerate(text):
        if char != EM_DASH:
            continue
        before = text[index - 1] if index > 0 else "\n"
        after = text[index + 1] if index + 1 < len(text) else "\n"
        if before.isspace() != after.isspace():
            line_no = text.count("\n", 0, index) + 1
            hits.append((line_no, lines[line_no - 1].strip()))
    return hits


def main() -> int:
    if not TARGET.is_file():
        print(f"check_no_emdash: no se encontró {TARGET}", file=sys.stderr)
        return 1
    hits = dict(aside_delimiter_hits(TARGET.read_text(encoding="utf-8")))
    if hits:
        print(f"✗ {len(hits)} línea(s) con raya larga usada como inciso:")
        for line_no, line in list(hits.items())[:40]:
            print(f"   L{line_no}: {line[:90]}")
        return 1
    print(f"✓ {TARGET.name}: sin raya larga como inciso")
    return 0


if __name__ == "__main__":
    sys.exit(main())
