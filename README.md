# udesa-x-docs

Documentación UdeSA-X con Sphinx + `sphinx_rtd_theme` (mismo formato que `IT-Ing-UdeSA/it-ing-udesa.github.io`).

- Fuente en `docs/` (MyST Markdown).
- Publica en GitHub Pages desde repo **público** (Pages con plan Free solo sale de público).
- Pegar `arquitectura.png` y `modelo-datos.png` en `docs/images/`.

Build local: `pip install -r docs/requirements.txt && sphinx-build -b html docs site`
