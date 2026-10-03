# Configuration file for the Sphinx documentation builder.
# Basado en IT-Ing-UdeSA/it-ing-udesa.github.io — mismo formato y estilo.

project = "UdeSA-X"
copyright = "2026, Grupo 6 TDS"
author = "Grupo 6 TDS"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Sin logo propio todavía: el amigo pone su PNG en _static/img/ y descomenta.
# html_logo = "_static/img/udesa-x-logo.png"
html_theme_options = {
    "logo_only": True,
}
