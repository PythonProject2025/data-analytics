# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DataAnalytics'
copyright = '2025, MAIT24-25'
author = 'Team GUI'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../..'))

extensions = [
'sphinx.ext.autodoc',
'sphinx.ext.napoleon',
'sphinx.ext.viewcode',
'sphinx_autodoc_typehints'
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_mock_imports = [
    "rest_framework",
    "rest_framework.views",
    "rest_framework.response",
    "rest_framework.schemas",
    "django",
    "django.conf"
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,  # Adjust based on how deep your headings go
    "titles_only": False
}
