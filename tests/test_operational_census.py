"""Operational tables must add up to the canonical export of their own cut."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "reports/latex"


def _fact(name: str) -> int:
    match = re.search(r"\\newcommand\{\\" + name + r"\}\{(\d+)\}", (ROOT / "key_facts.tex").read_text())
    assert match, name
    return int(match.group(1))


def _table(label: str) -> str:
    text = (ROOT / "ProyectoI_VisaPredictAI.tex").read_text()
    start = text.index(r"\label{" + label + "}")
    return text[start:text.index(r"\end{table}", start)]


def _number(value: str) -> int:
    if value.strip() == r"\factNObsFFmt{}":
        return _fact("factNObsF")
    digits = re.sub(r"\D", "", value)
    assert digits, value
    return int(digits)


def test_quality_status_counts_cover_the_current_panel() -> None:
    rows = [line.split("&") for line in _table("tab:calidad_obtencion").splitlines() if " & " in line]
    statuses = [row for row in rows if row[0].startswith("Observaciones ")]
    assert len(statuses) == 4
    assert sum(_number(row[1]) for row in statuses) == _fact("factNObs")


def test_sql_summary_dated_counts_cover_the_current_trainable_observations() -> None:
    rows = [line.split("&") for line in _table("tab:duckdb_query").splitlines() if re.match(r"(?:family|employment)\s+&", line)]
    assert len(rows) == 4
    assert sum(_number(row[3]) for row in rows) == _fact("factNObsF")
