"""Guardas editoriales para la retroalimentación académica J1--J5."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "reports/latex/ProyectoI_VisaPredictAI.tex"


def _texto() -> str:
    return TEX.read_text(encoding="utf-8")


def _normalizar(texto: str) -> str:
    return re.sub(r"\s+", " ", texto)


def feedback_violations(texto: str) -> list[str]:
    """Devuelve los residuos deterministas de J1, J2 y J4."""
    normalizado = _normalizar(texto)
    prohibidas = {
        "J1": "Cantidad de los datos obtenidos",
        "J2": r"p.\,ej.\ \texttt{01FEB18}",
        "J4": "el tipo de error que el EDA existe para prevenir",
    }
    return [identificador for identificador, frase in prohibidas.items() if frase in normalizado]


def _primera_aparicion_bilingue(texto: str, ingles: str, espanol: str) -> bool:
    """Exige español cerca de la primera mención inglesa, sin prohibir usos posteriores."""
    normalizado = _normalizar(texto)
    indice = normalizado.find(ingles)
    if indice < 0:
        return False
    contexto = normalizado[max(0, indice - 100) : indice]
    return espanol in contexto


def test_j1_j2_j4_no_reaparecen_en_el_documento_principal() -> None:
    assert feedback_violations(_texto()) == []


def test_los_tres_anglicismos_se_introducen_con_espanol_primero() -> None:
    texto = _texto()
    assert _primera_aparicion_bilingue(texto, "feature-based", "basado en características")
    assert _primera_aparicion_bilingue(texto, "hold-out", "conjunto reservado")
    assert _primera_aparicion_bilingue(texto, "leakage", "fuga de información")


def test_hold_out_solo_permanece_en_su_introduccion_bilingue() -> None:
    assert _texto().lower().count("hold-out") == 1


def test_la_guarda_no_prohibe_usos_tecnicos_posteriores() -> None:
    ejemplo = "conjunto reservado (\\textit{hold-out}); después, holdout_forecasts.csv"
    assert _primera_aparicion_bilingue(ejemplo, "hold-out", "conjunto reservado")


def test_la_tabla_de_a6_queda_reconciliada_en_el_maestro() -> None:
    assert r"\label{tab:modelos_a6}" in _texto()


def test_referencias_del_maestro_son_contiguas_y_todas_se_usan() -> None:
    texto = _texto()
    referencias = [int(valor) for valor in re.findall(r"\\item\\label\{bib:(\d+)\}", texto)]
    assert referencias == list(range(1, len(referencias) + 1))

    citadas = {int(valor) for valor in re.findall(r"\\cita\{(\d+)\}", texto)}
    for inicio, fin in re.findall(r"\\cita\{(\d+)\}\\textendash\\cita\{(\d+)\}", texto):
        citadas.update(range(int(inicio), int(fin) + 1))
    assert citadas == set(referencias)
