"""Guardas documentales de la integración semántica de A9."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "reports/latex/ProyectoI_VisaPredictAI.tex"


def _seccion_implementacion() -> str:
    texto = TEX.read_text(encoding="utf-8")
    inicio = texto.index(r"\subsection{1.4.1 Implementación del modelo}")
    fin = texto.index(r"\subsection{1.4.2 ", inicio)
    return texto[inicio:fin]


def _normalizada() -> str:
    return re.sub(r"\s+", " ", _seccion_implementacion())


def test_a9_conserva_a8_y_anade_los_artefactos_del_segundo_avance() -> None:
    seccion = _seccion_implementacion()
    for etiqueta in (
        "fig:implementacion_a8",
        "alg:implementacion_a8",
        "fig:orquestacion_a9",
        "alg:orquestacion_a9",
        "tab:registro_a9",
        "tab:parametros_a9",
        "tab:modulos_a9",
    ):
        assert seccion.count(rf"\label{{{etiqueta}}}") == 1


def test_a9_distingue_persistencia_fuente_y_obligatoriedad() -> None:
    seccion = _normalizada()
    assert "SARIMA se incluye entre los modelos persistibles" in seccion
    assert "ETS y Theta no conservan un estado reutilizable" in seccion
    assert "Esta limitación técnica no los vuelve opcionales" in seccion


def test_a9_exige_grilla_y_semillas_exactas_con_fallo_cerrado() -> None:
    seccion = _normalizada()
    assert "25 series por 24 meses, es decir, 600 claves" in seccion
    assert r"el conjunto exacto de semillas $s_1,\ldots,s_5$" in seccion
    assert "después del primer fallo no se ejecutan agregaciones" in seccion
    assert "cinco archivos truncados de manera idéntica no pueden" in seccion


def test_a9_no_declara_ejecutada_la_campana_pendiente() -> None:
    seccion = _normalizada()
    assert "La campaña integral no forma parte de A9 y no se ha iniciado" in seccion
    assert "queda una auditoría independiente final" in seccion
