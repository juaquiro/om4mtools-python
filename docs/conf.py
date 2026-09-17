"""Sphinx configuration for om4mtools documentation."""

project = "om4mtools"
copyright = "2026, om4mtools-python contributors"
author = "om4mtools-python contributors"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True
templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "alabaster"
