# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys

sys.path.insert(0, os.path.abspath('../blog'))

project = 'Blog'
copyright = '2023, Yeison Cardona'
author = 'Yeison Cardona'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'nbsphinx',
    'dunderlab.docs',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_logo = '_static/logo.svg'
# html_favicon = '_static/favico.ico'

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'caption_font_family': 'Noto Sans',
    'font_family': 'Noto Sans',
    'head_font_family': 'Noto Sans',
    'page_width': '1280px',
    'sidebar_width': '300px',
}

autodoc_mock_imports = [
    'timescale',
    'django',
    'django.db',
    'rest_framework',
    'django_filters',
]

dunderlab_maxdepth = 3
dunderlab_color_links = '#FF3131'
dunderlab_code_reference = True
dunderlab_github_repository = 'https://github.com/YeisonCardona/Prueba-Django-REST-Backend-Senior'

