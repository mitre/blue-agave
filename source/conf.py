# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Blue Agave"
author = "The MITRE Corporation"
copyright_years = "2024"
copyright = "test"
prs_numbers = "[?]"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []

rst_prolog = f"""
.. |copyright_years| replace:: {copyright_years}
.. |prs_numbers| replace:: {prs_numbers}
"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_show_sourcelink = False
html_show_sphinx = False
html_context = {
    "copyright_years": copyright_years,
    "prs_numbers": prs_numbers,
}
html_theme_options = {}
