# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = 'AxterDB'
copyright = '2023, AxterDB'
author = 'ItsNeil'
release = '1.4.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("extensions"))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.duration",
    "sphinxcontrib_trio",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinx_autodoc_typehints",
]
always_document_param_types = True
toc_object_entries_show_parents = "hide"

autodoc_member_order = "bysource"
autodoc_typehints = "none"

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = "./images/axterdb_logo.png"
html_favicon = "./images/axterdb_logo.ico"

html_theme = 'furo'
html_static_path = ['_static']

html_theme_options = {
    "announcement": "Welcome to AxterDB Documentation! We are currently in limited beta.",
}