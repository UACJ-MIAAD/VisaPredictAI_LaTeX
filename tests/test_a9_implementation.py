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
    """Consolidación 1.4.1 (29-oct-2026): la orquestación de A9 se narra en prosa; sus parámetros
    entran en tab:config_a10 y sus módulos en la prosa de pruebas; la tabla de avances lo identifica."""
    seccion = _seccion_implementacion()
    for etiqueta in ("fig:implementacion_a8", "alg:implementacion_a8", "tab:avances_a10",
                     "tab:config_a10"):
        assert seccion.count(rf"\label{{{etiqueta}}}") == 1
    normal = _normalizada()
    avances = normal[normal.index(r"\label{tab:avances_a10}"):]
    assert r"\textbf{A9} & Integrar componentes sin mezclar procedencias" in avances[: avances.index(r"\end{table}")]
    for mecanismo in ("Un registro canónico sustituye las listas distintas",
                      "Un área de preparación aislada por campaña",
                      "Los recibos de cobertura se recalculan al leer",
                      r"una verificación previa (\textit{preflight}) bloquea la ejecución"):
        assert mecanismo in normal, mecanismo
    configuracion = normal[normal.index(r"\label{tab:config_a10}"):]
    configuracion = configuracion[: configuracion.index(r"\end{table}")]
    for condicion in ("Identificador único", "promoción atómica; detención inmediata",
                      "Cobertura exacta de claves", "rechaza faltantes, extras o archivos de otra campaña"):
        assert condicion in configuracion, condicion
    assert ("se organiza en módulos de configuración y registro, recorrido temporal, transporte y "
            "cobertura, exportación y promoción, y verificación previa y lanzamiento") in normal


def test_a9_distingue_persistencia_fuente_y_obligatoriedad() -> None:
    seccion = _normalizada()
    assert "SARIMA se incluye entre los modelos persistibles" in seccion
    assert "sus envoltorios automáticos no conservan un estado reutilizable" in seccion
    assert "Esta limitación técnica no los vuelve opcionales" in seccion


def test_a9_exige_grilla_y_semillas_exactas_con_fallo_cerrado() -> None:
    seccion = _normalizada()
    assert "25 series por 24 meses, es decir, 600 claves" in seccion
    assert r"el conjunto exacto de semillas $s_1,\ldots,s_5$" in seccion
    assert "después del primer fallo no se ejecutan agregaciones" in seccion
    assert "cinco archivos truncados de manera idéntica no pueden" in seccion


def test_a9_fecha_la_campana_despues_del_avance_sin_anticiparla() -> None:
    seccion = _normalizada()
    assert "La campaña integral no formaba parte del segundo avance y entonces no se había iniciado" in seccion
    assert "quedaba una auditoría independiente final" in seccion
    # el estado de entonces no se reescribe como si la campaña ya hubiera corrido
    assert "no se ha iniciado" not in seccion
