"""Guardas documentales de la integración semántica de A8."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "reports/latex/ProyectoI_VisaPredictAI.tex"


def _texto() -> str:
    return TEX.read_text(encoding="utf-8")


def _seccion_a8() -> str:
    texto = _texto()
    inicio = texto.index(r"\subsection{1.4.1 Implementación del modelo}")
    fin = texto.index(r"\subsection{1.4.2 ", inicio)
    return texto[inicio:fin]


def test_a8_integra_sus_cuatro_artefactos_documentales() -> None:
    """Consolidación 1.4.1 (29-oct-2026): los parámetros de A8 viven en tab:config_a10; la tabla de
    herramientas salió porque repetía las bibliotecas citadas en 1.3.2, y el entorno y los módulos
    quedan en prosa; la tabla de avances identifica el aporte de A8."""
    seccion = _seccion_a8()
    assert seccion.count(r"\label{fig:implementacion_a8}") == 1
    assert seccion.count(r"\label{alg:implementacion_a8}") == 1
    assert seccion.count(r"\label{tab:config_a10}") == 1
    assert "Python 3.14 con perfiles de dependencias fijados" in re.sub(r"\s+", " ", seccion)
    configuracion = seccion[seccion.index(r"\label{tab:config_a10}"):]
    configuracion = configuracion[: configuracion.index(r"\end{table}")]
    for parametro in ("Semilla global & 42", "Periodo estacional & 12 meses", "500 por objetivo",
                      r"calendario en $t$; máscara en $t-1$", "nunca se sustituye por uno"):
        assert parametro in configuracion, parametro
    avances = seccion[seccion.index(r"\label{tab:avances_a10}"):]
    assert r"\textbf{A8} & Convertir el diseño en cálculo reproducible" in avances[: avances.index(r"\end{table}")]


def test_a8_declara_el_protocolo_temporal_sin_usar_el_holdout_para_seleccion() -> None:
    seccion = _seccion_a8()
    assert "FAD: 60; DFF: 36 meses" in seccion
    assert "Conjunto reservado & 24 meses" in seccion
    assert "Pronóstico temporal & horizonte 1; paso 1" in seccion
    assert "el conjunto reservado nunca interviene" in seccion


def test_a8_documenta_fallo_cerrado_y_cobertura_derivada() -> None:
    seccion = _seccion_a8()
    assert "rejilla esperada se deriva del panel y del registro" in seccion
    assert "política de fallo cerrado" in seccion
    assert "un faltante, un duplicado, un mes sustituido" in seccion


def test_a8_no_presenta_la_campana_pendiente_como_resultado_final() -> None:
    seccion = _seccion_a8()
    assert "El objetivo de la implementación no es declarar un modelo definitivo" in seccion
    assert "la regeneración integral de resultados se mantuvo separada y" in seccion
    assert "sólo se ejecutó después de acreditar los insumos" in re.sub(r"\s+", " ", seccion)
    assert not re.search(r"campaña (?:completa )?(?:ejecutada|publicada)", seccion, re.IGNORECASE)

