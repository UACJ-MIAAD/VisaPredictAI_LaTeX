"""A monthly census must not silently move the retrospective evaluation window."""

import re
from pathlib import Path

TEXT = (Path(__file__).resolve().parents[1] / "reports/latex/ProyectoI_VisaPredictAI.tex").read_text()
START = TEXT.index(r"\paragraph{Vigencia de las cifras retrospectivas.}")
RETROSPECTIVE = TEXT[START:TEXT.index("Las cuatro métricas reportadas", START)]
ABSTRACT = TEXT[TEXT.index(r"\chapter*{Resumen}"):TEXT.index(r"\chapter{Desarrollo de la propuesta de solución}")]


def test_retrospective_window_does_not_follow_live_census_macros() -> None:
    for macro in (r"\factNMonths", r"\factDateLast", r"\factNObs"):
        assert macro not in RETROSPECTIVE, macro


def test_retrospective_cut_and_execution_month_are_distinct() -> None:
    assert re.search(r"septiembre\s+de\s+2026", RETROSPECTIVE)
    assert re.search(r"octubre\s+de\s+2026", RETROSPECTIVE)


def test_abstract_names_the_operational_and_scientific_vintages() -> None:
    assert re.search(r"octubre\s+de\s+2026", ABSTRACT)
    assert re.search(r"septiembre\s+de\s+2026", ABSTRACT)
    assert "operativo" in ABSTRACT and "sellados" in ABSTRACT


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Scientific vintage guard requires assertions enabled")
    for check in (
        test_retrospective_window_does_not_follow_live_census_macros,
        test_retrospective_cut_and_execution_month_are_distinct,
        test_abstract_names_the_operational_and_scientific_vintages,
    ):
        check()
    print("Scientific vintage: three checks passed")
