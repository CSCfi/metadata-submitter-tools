"""Configuration file for the Sphinx documentation builder."""

import os
import sys
import datetime
# from typing import Callable

import validator

# Get the project root dir, which is the parent dir of this
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

current_year = str(datetime.date.today().year)
project = 'Metadata Submitter Tools'
copyright = f'{current_year}, CSC Developers'
author = 'CSC Developers'

# The short X.Y version.
version = str(validator.__version__)
# The full version, including alpha/beta/rc tags
release = '0.1.0-alpha'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.coverage',
              'sphinx.ext.ifconfig',
              'sphinx.ext.viewcode',
              'sphinx.ext.githubpages',
              'sphinx.ext.todo']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autosummary_generate = True


# -- Options for HTML output -------------------------------------------------

html_title = 'Metadata Submitter Tools'

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': True,
    'sticky_navigation': True,
    # 'navigation_depth': 4,
    'display_version': True,
    'prev_next_buttons_location': 'bottom'}


# def setup(app: Callable) -> None:
#     """Add custom stylesheet."""
#    app.add_css_file('custom.css')
