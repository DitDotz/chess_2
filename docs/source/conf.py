# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('"C:\\Users\\Zhi Quan\\Documents\\chess_2.0\\src\\'))  # Add src to path

project = 'chess_2'
copyright = '2025, Zhi Quan'
author = 'Zhi Quan'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'autoapi.extension',
]

autoapi_type = 'python'
autoapi_dirs = ['./']  # path to your source code

html_theme = 'alabaster'
html_static_path = ['_static']
