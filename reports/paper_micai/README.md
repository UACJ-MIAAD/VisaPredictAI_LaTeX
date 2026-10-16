# Paper MICAI 2027 — paquete LaTeX

> **Borrador** del artículo para MICAI (Springer LNCS), derivado de la auditoría
> adversarial de 5 revisores. Números **honestos** ya verificados contra el pipeline.
> El cuerpo es un draft completo y defendible; la redacción final se pule con el asesor.

> ⚠️ **Provisional retrospective metrics:** the published campaign figures were derived
> with the protocol that predates the causal gap-fill correction (F1, 2026-07-12); the
> correction is in code and the full re-derivation (F2) is pending. **Status (audited
> 2026-07-12): interim fixes applied (title, leakage wording, significance table, MASE<1
> framing, backfill scope); do not submit until P0=0.**

## Contenido

```
reports/paper_micai/
├── paper.tex              # artículo LNCS doble-ciego (compila: 8 pp.)
├── llncs.cls              # clase oficial Springer (NO modificar)
├── splncs04.bst           # estilo de citas Springer (reservado; el draft usa bib inline)
├── Figures/               # PDFs vectoriales generados (no editar a mano)
│   ├── fig_prospective_horizon.pdf   # MAE+MASE vs horizonte (figura de la contribución)
│   ├── fig_calibration.pdf           # cobertura empírica 80/95 vs horizonte
│   └── fig_fanchart.pdf              # fan-chart de una serie piloto
├── make_paper_figures.py  # regenera Figures/ desde el pipeline (datos reales)
└── README.md
```

## Compilar (Overleaf)

1. Sube `paper.tex`, `llncs.cls` y la carpeta `Figures/`.
2. Compilador = **pdfLaTeX**; corre 2 pasadas (bibliografía **inline**, sin BibTeX).
3. No cargues `geometry` ni cambies márgenes (Springer rechaza desviaciones de `llncs.cls`).

## Regenerar las figuras

```bash
make paper-figures        # = ante/bin/python reports/paper_micai/make_paper_figures.py
```
Lee `reports/prospective/forecast_scorecard_meta.json` (evaluación prospectiva),
`reports/prospective/web_forecasts.csv` y `data/processed/visa_panel_long.csv`. Cero placeholders;
si los datos cambian, las figuras se actualizan. Estilo LNCS B/N-safe (líneas/marcadores
distintos, no solo color), PDF vectorial.

## Defensas de revisor ya incorporadas

(ver el análisis completo en `PAPER_PROSPECTIVE_DRAFT.md` (este directorio) y la auditoría)

- **Reencuadre como paper de aplicación** (dataset + protocolo prospectivo), no de métodos.
- **Números honestos:** hold-out MASE a un paso marcado como *señal de selección, no precisión live*;
  prospectivo MASE 0.347 / MAE 146 d (h=1..12, ambas tablas) como titular; el gap se **declara**
  sin resumirlo en un cociente, porque las dos cifras miden cantidades distintas.
- **cov95 = 0.92 < nominal** reportado como under-coverage honesta; banda 80 % calibrada en
  split disjunto (cov80 held-out 0.81), no circular; bandas desplegadas por **cuantil empírico
  por horizonte** + ACI (sustituye al heurístico √h, cuyo cov80 h12 caía a 0.72).
- **El piso del paseo aleatorio como HALLAZGO insignia** (campaña de re-derivación causal,
  oct-2026): con 45 % de avances mensuales nulos, el naïve-1 gana el hold-out entre los modelos
  que cubren las 25 series de cada tabla (FAD 0.157 media / 0.135 mediana; DFF 0.125, empate
  exacto con Theta); el MCS al 90 % es **{naive1} en FAD y {ETS, naive1} en DFF**. DM favorece al
  RW con significancia robusta en FAD (p≈0.0003 frente a AutoBiTCN); en DFF el contraste
  pre-registrado es BiTCN frente a ARIMA y no es significativo (p≈0.065). El deep AutoBiTCN
  (0.162) queda por debajo de ETS/Theta (0.167/0.171) pero no del piso; en DFF BiTCN (0.122)
  queda ligeramente por debajo de la media del naïve-1 (0.125), una diferencia descriptiva sin
  prueba que la respalde; el margen deep-DFF vs Auto-ARIMA justo (0.146 media / 0.138 mediana)
  es ~16 %. Gobernanza: en FAD el naïve-1 es apto a h=1; en DFF el apto es la mediana
  SARIMA+ETS+Theta; la promoción se **retiene** (el producto es h=1..12) + despliegue en sombra
  mensual.
- **`\paragraph{Causal gap handling and leakage controls}`** (relleno causal LOCF + máscaras
  MNAR rezagadas, ventana expansible, lags pre-origen, rollout recursivo, escala MASE
  pre-origen, congelado en fecha de origen) + máscara F-only explícita; las cifras ya proceden de
  la re-derivación causal (la nota de cifras provisionales se retiró con `retro_protocol: f2-causal`).
- **194 estructurales / 74 evaluables**; "deployed" → "evaluated"; demo RAG = artefacto, no contribución.
- **Ética/disponibilidad** (datos públicos agregados, sin IRB, no asesoría legal) + **apéndice de
  reproducibilidad** (versiones pin-eadas py3.14, semillas, walk-forward, provenance = scorecard+git SHA).
- **Amenazas de validez** declaradas: cuantiles por horizonte sin garantía multi-paso, n efectivo
  (3 añadas), pseudo-replicación RoW, dependencia hardware/semilla, supervivencia.

## Pendiente para la sesión con el asesor (no son cambios de código)

- [x] Tabla numérica **MCS + Friedman–Nemenyi** para el benchmark de 24 modelos (tab:significance).
- [x] **Auto-ARIMA afinado** como fila de baseline explícita bajo el mismo walk-forward
      (spec justa: drift + retrain mensual + AICc sobre F cruda).
- [ ] Rellenar el bloque de autor camera-ready + URLs de repo/sitio (hoy comentados para doble-ciego).
- [ ] Pulir los overfull hboxes menores y la prosa con el Dr. Chente.
