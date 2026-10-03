# udesa-x-docs

Documentación de UdeSA-X, el clon mobile de X/Twitter del grupo 6 del Taller de Desarrollo de Software (UdeSA, 2026).

La documentación se lee en la **[wiki](https://github.com/tds-g6-2s2026/udesa-x-docs/wiki)**:

- Historias y responsables
- Arquitectura
- Bases de datos
- ADRs
- Release 1

La carpeta `entrega-intermedia` guarda los archivos originales de la entrega intermedia:

- `historias-y-responsables.xlsx`: planilla de historias, responsables y requisitos técnicos.
- `diagrama-arquitectura.png` y `.pdf`: diagrama de arquitectura.
- `diagrama-bases-de-datos.png` y `.pdf`: modelo de datos.
- `adrs-udesa-x.pdf`: los 14 ADRs.

## Sitio Sphinx (mismo formato que `IT-Ing-UdeSA/it-ing-udesa.github.io`)

- Fuente en `docs/` (MyST Markdown, theme `sphinx_rtd_theme`).
- Publica en GitHub Pages desde este repo público (`Settings > Pages > Source: GitHub Actions`).
- Imágenes en `docs/images/`.

Build local: `pip install -r docs/requirements.txt && sphinx-build -b html docs site`
