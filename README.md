# VisaPredictAI LaTeX

Repositorio documental de VisaPredictAI. Esta es la autoridad de fuentes para
la compilación y revisión locales; el repositorio de datos ya no es el punto de
entrada para los documentos académicos. Overleaf no es una dependencia de entrega.

## Documentos

| Entregable | Documento principal | Compilador |
|---|---|---|
| Proyecto I | `reports/latex/ProyectoI_VisaPredictAI.tex` | pdfLaTeX, 3 pasadas |
| Anteproyecto | `reports/latex/AnteproyectoVisaPredictAI.tex` | pdfLaTeX, 3 pasadas |
| Paper MICAI | `reports/paper_micai/paper.tex` | pdfLaTeX, 3 pasadas |

El workflow **LaTeX gate** compila los tres documentos desde un clon limpio,
comprueba referencias, citas, labels y overfulls, y conserva PDF y logs como
artefactos de CI. También ejecuta el guardarraíl tipográfico de Proyecto I.

## Compilación local

Desde la carpeta del documento, ejecutar tres veces
`pdflatex -interaction=nonstopmode -halt-on-error <archivo.tex>` con TeX Live local.
Comprobar después los logs con `tools/check_latex_log.sh`: los umbrales son
`0 0` para Proyecto I y Anteproyecto, y `3 15` para el paper. Ejecutar también
`python3 tools/check_no_emdash.py` y las pruebas documentales.

Antes de entregar, revisar las páginas renderizadas, conservar el SHA de las
fuentes, la versión del compilador, los logs y el SHA-256 del PDF. Los paquetes
DOCX y PPTX se exportan a PDF localmente. Una compilación correcta no sustituye
la revisión del autor, el aval del asesor ni el acuse de entrega.

## Procedencia

La historia de `reports/latex/` y `reports/paper_micai/` fue extraída de
`UACJ-MIAAD/VisaPredictAI` sin reescribir el contenido. El punto exacto de corte
está registrado en [`MIGRATION_ORIGIN.json`](MIGRATION_ORIGIN.json).

Los hechos, tablas y figuras derivados siguen teniendo como autoridad los datos
del repositorio `VisaPredictAI`. La separación física no autoriza copiar cifras a
mano: cada actualización documental debe declarar el SHA de datos que consume y
pasar los contratos cross-repo.
