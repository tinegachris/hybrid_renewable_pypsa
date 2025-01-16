# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Hybrid Renewable PyPSA'
author = 'Chrispine Tinega and Contributors'
release = '0.2.0'
version = '0.2.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',      # Include documentation from docstrings
    'sphinx.ext.napoleon',     # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode',     # Add links to highlighted source code
    'sphinx.ext.todo',         # Support for todo items
    'sphinx.ext.coverage',     # Collect doc coverage stats
    'sphinx.ext.intersphinx',  # Link to other projects' documentation
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for todo extension ----------------------------------------------

todo_include_todos = True

# -- Master document ---------------------------------------------------------

master_doc = 'index'

# -- Intersphinx mapping -----------------------------------------------------

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}