# udesa-x-docs

Documentación de UdeSA-X, el clon mobile de X/Twitter del grupo 6 del Taller de Desarrollo de Software (UdeSA, 2026).

La documentación se lee en la **[wiki](https://github.com/tds-g6-2s2026/udesa-x-docs/wiki)**:

- Historias y responsables
- Arquitectura
- Bases de datos
- ADRs
- Release 1
- Release 2

La carpeta `entrega-intermedia` guarda los archivos originales de la entrega intermedia:

- `historias-y-responsables.xlsx`: planilla de historias, responsables y requisitos técnicos.
- `diagrama-arquitectura.png` y `.pdf`: diagrama de arquitectura.
- `diagrama-bases-de-datos.png` y `.pdf`: modelo de datos.
- `adrs-udesa-x.pdf`: los 14 ADRs.

La carpeta `entrega-final` guarda la planilla de la entrega final (`historias-y-responsables.xlsx`): la planilla de historias de la cátedra completa (hojas Total, Obligatorias y Optativas), un Resumen con las historias y los puntos de cada integrante, y los Requisitos técnicos.

## Sitio Sphinx (mismo formato que `IT-Ing-UdeSA/it-ing-udesa.github.io`)

- Fuente en `docs/` (MyST Markdown, theme `sphinx_rtd_theme`).
- Publica en GitHub Pages desde este repo público (`Settings > Pages > Source: GitHub Actions`).
- Imágenes en `docs/images/`. Los diagramas tienen su fuente en SVG al lado del PNG; el PNG se exporta a 3440 px de ancho (`rsvg-convert -w 3440 arquitectura.svg -o arquitectura.png`).

Build local: `pip install -r docs/requirements.txt && sphinx-build -b html docs site`

El build deja afuera la entrega intermedia (`release-1.md` y lo que está entre `<!-- intermedia:inicio -->` y `<!-- intermedia:fin -->` en `docs/index.md`), así el sitio queda solo con la entrega final. Los archivos siguen en el repo; para incluirlos: `sphinx-build -t intermedia -b html docs site`.
