"""Contrato del guardarraíl tipográfico que pertenece al repo documental."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_no_emdash", ROOT / "tools/check_no_emdash.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_aside_delimiters_are_rejected() -> None:
    assert [line for line, _ in MODULE.aside_delimiter_hits("texto —inciso— texto")] == [1, 1]


def test_ranges_and_spaced_separators_are_allowed() -> None:
    assert MODULE.aside_delimiter_hits("Agosto—Diciembre · A — B") == []


def test_the_live_deliverable_passes() -> None:
    assert MODULE.main() == 0
