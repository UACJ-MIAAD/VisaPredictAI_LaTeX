# VisaPredictAI LaTeX

Repositorio documental de VisaPredictAI. Esta es la fuente que debe conectarse a
Overleaf y compilarse; el repositorio de datos ya no es el punto de entrada para
los documentos académicos.

## Documentos

| Entregable | Documento principal | Compilador |
|---|---|---|
| Proyecto I | `reports/latex/ProyectoI_VisaPredictAI.tex` | pdfLaTeX, 3 pasadas |
| Anteproyecto | `reports/latex/AnteproyectoVisaPredictAI.tex` | pdfLaTeX, 3 pasadas |
| Paper MICAI | `reports/paper_micai/paper.tex` | pdfLaTeX, 3 pasadas |

El workflow **LaTeX gate** compila los tres documentos desde un clon limpio,
comprueba referencias, citas, labels y overfulls, y conserva PDF y logs como
artefactos de CI. También ejecuta el guardarraíl tipográfico de Proyecto I.

## Uso con Overleaf

1. Importar o vincular este repositorio de GitHub.
2. Para la tesis, seleccionar
   `reports/latex/ProyectoI_VisaPredictAI.tex` como documento principal.
3. Para el anteproyecto, seleccionar
   `reports/latex/AnteproyectoVisaPredictAI.tex`.
4. Para el paper, seleccionar `reports/paper_micai/paper.tex`.
5. Usar pdfLaTeX. No editar únicamente en Overleaf: todo cambio durable vuelve
   por PR a este repositorio.

## Procedencia

La historia de `reports/latex/` y `reports/paper_micai/` fue extraída de
`UACJ-MIAAD/VisaPredictAI` sin reescribir el contenido. El punto exacto de corte
está registrado en [`MIGRATION_ORIGIN.json`](MIGRATION_ORIGIN.json).

Los hechos, tablas y figuras derivados siguen teniendo como autoridad los datos
del repositorio `VisaPredictAI`. La separación física no autoriza copiar cifras a
mano: cada actualización documental debe declarar el SHA de datos que consume y
pasar los contratos cross-repo.
