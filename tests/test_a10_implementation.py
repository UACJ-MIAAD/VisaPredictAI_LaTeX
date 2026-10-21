"""Guardas documentales del cierre semántico de A10."""

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


def test_a10_conserva_los_avances_previos_y_anade_el_cierre() -> None:
    seccion = _seccion_implementacion()
    for etiqueta in (
        "fig:implementacion_a8",
        "alg:implementacion_a8",
        "fig:orquestacion_a9",
        "alg:orquestacion_a9",
        "tab:avances_a10",
        "fig:estados_a10",
        "alg:cierre_a10",
        "tab:fallos_a10",
        "tab:config_a10",
        "tab:pruebas_a10",
    ):
        assert seccion.count(rf"\label{{{etiqueta}}}") == 1


def test_a10_define_estados_y_prohibe_transiciones_por_existencia() -> None:
    seccion = _normalizada()
    for estado in ("running", "computed", "validated", "published", "failed"):
        assert rf"\texttt{{{estado}}}" in seccion
    assert "nunca se interpreta la mera existencia de un archivo" in seccion
    assert "Sólo una campaña calculada y validada puede publicarse" in seccion


def test_a10_preserva_persistencia_transporte_y_clasificacion_multietiqueta() -> None:
    seccion = _normalizada()
    assert "SARIMA utiliza serialización comprimida" in seccion
    assert "ETS y Theta, en cambio, no se presentan como objetos reutilizables" in seccion
    assert "incompleto y contaminado al mismo tiempo" in seccion
    assert "también inspecciona punteros DVC" in seccion


def test_a10_consolida_el_protocolo_sin_confundirlo_con_hiperparametros() -> None:
    seccion = _normalizada()
    assert "25 series elegibles" in seccion
    assert "24 objetivos mensuales" in seccion
    assert r"Cinco semillas, $s_1$--$s_5$" in seccion
    assert "Los valores de aceptación no se optimizan junto con el modelo" in seccion


def test_a10_mantiene_auditoria_y_campana_como_fronteras_explicitas() -> None:
    seccion = _normalizada()
    assert "la campaña prolongada no se había ejecutado" in seccion
    assert "la publicación quedaba fuera del avance" in seccion
    assert "auditoría final de sólo lectura" in seccion
    assert "la finalización del software de la obtención de evidencia experimental nueva" in seccion
    # lo ocurrido después se declara con su orden: auditoría, validación humana, reconciliación, publicación
    assert "La campaña causal se ejecutó después, en octubre de 2026, una vez superada esa auditoría" in seccion
    assert "validación con revisión humana" in seccion
    assert "no se ha ejecutado" not in seccion
