# Configuration file for the Sphinx documentation builder
# This file only contains a selection of the most common options
# For a full list see the documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html


from datetime import date
import os
import sys


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory, add these directories to sys.path here
# If the directory is relative to the documentation root, use os.path.abspath to make it absolute, like shown here

# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Art of Geometry'
author = 'Luong The Vinh'
copyright = f'{date.today().year}, {author}'


# The full version, including alpha/beta/rc tags
release = '0.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings
# They can be extensions coming with Sphinx (named sphinx.ext.*) or your custom ones
extensions = (
    'recommonmark',   # Markdown parser

    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.autodoc.typehints',

    'sphinx.ext.autosectionlabel',  # Allow reference sections using its title
    'sphinx.ext.autosummary',   # Generate autodoc summaries
    'sphinx.ext.coverage',   # Collect doc coverage stats
    'sphinx.ext.doctest',   # Test snippets in the documentation
    'sphinx.ext.duration',   # Measure durations of Sphinx processing
    'sphinx.ext.extlinks',   # Markup to shorten external links
    'sphinx.ext.githubpages',   # Publish HTML docs in GitHub Pages
    'sphinx.ext.graphviz',   # Add Graphviz graphs
    'sphinx.ext.ifconfig',   # Include content based on configuration
    'sphinx.ext.imgconverter',   # A reference image converter using Imagemagick
    'sphinx.ext.inheritance_diagram',   # Include inheritance diagrams
    'sphinx.ext.intersphinx',   # Link to other projects' documentation
    # 'sphinx.ext.linkcode',   # Add external links to source code

    # math support
    # 'sphinx.ext.imgmath',   # Render math as images
    # 'sphinx.ext.jsmath',   # Render math via JavaScript
    'sphinx.ext.mathjax',   # Render math via JavaScript

    'sphinx.ext.napoleon',   # Support for NumPy and Google style docstrings
    'sphinx.ext.todo',   # Support for todo items
    'sphinx.ext.viewcode'   # Add links to highlighted source code
)

# Add any paths that contain templates here, relative to this directory
templates_path = ['_templates']

# List of patterns, relative to source directory,
# that match files and directories to ignore when looking for source files
# This pattern also affects html_static_path and html_extra_path
exclude_patterns = []

# source parsers
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages (see the documentation for a list of built-in themes)
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here, relative to this directory
# They are copied after the built-in static files, so a file named default.css will overwrite the built-in default.css
html_static_path = ['_static']


# AutoDoc
autodoc_default_options = {
    # 'members': ...,
    'member-order': 'bysource',

    'exclude-members': '__weakref__',

    # 'imported-members': False,

    'show-inheritance': True,
    # 'inherited-members': False,

    'private-members': True,
    'special-members': '__init__',

    # 'undoc-members': False,   # *** HAVE TO MANUALLY REMOVE FROM GENERATED .RST FILES ***

    'ignore-module-all': False
}

autodoc_typehints = 'signature'
