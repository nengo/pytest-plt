#!/usr/bin/env python3

import os
import sys

try:
    import pytest_plt
    import nengo_sphinx_theme  # noqa: F401 pylint: disable=unused-import
except ImportError:
    print("To build the documentation, pytest_plt and nengo_sphinx_theme must "
          "be installed in the current environment. Please install these and "
          "their requirements first. A virtualenv is recommended!")
    sys.exit(1)


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'nengo_sphinx_theme',
]

# -- sphinx.ext.autodoc
autoclass_content = 'both'  # class and __init__ docstrings are concatenated
autodoc_default_options = {"members": None}
autodoc_member_order = 'bysource'  # default is alphabetical

# -- sphinx.ext.intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- sphinx.ext.todo
todo_include_todos = True

# -- sphinx
needs_sphinx = '1.3'
nitpicky = True
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'

project = u"pytest_plt"
authors = u"Applied Brain Research"
copyright = pytest_plt.__copyright__
version = '.'.join(pytest_plt.__version__.split('.')[:2])  # Short X.Y version
release = pytest_plt.__version__  # Full version, with tags

# -- Options for HTML output --------------------------------------------------

pygments_style = "friendly"
templates_path = []
html_static_path = ["_static"]

html_theme = "nengo_sphinx_theme"

html_title = "pytest-plt {0} docs".format(release)
htmlhelp_basename = project
html_last_updated_fmt = ''  # Suppress 'Last updated on:' timestamp
html_show_sphinx = False
html_favicon = os.path.join("_static", "favicon.ico")
html_sidebars = {"**": ["sidebar.html"]}
html_theme_options = {
    "sidebar_logo_width": 200,
    "nengo_logo": "general-full-light.svg",
}

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '11pt',
    # 'preamble': '',
}

latex_documents = [
    # (source start file, target, title, author, documentclass [howto/manual])
    (master_doc, 'pytest_plt.tex', html_title, authors, 'manual'),
]

# -- Options for manual page output -------------------------------------------

man_pages = [
    # (source start file, name, description, authors, manual section).
    (master_doc, project, html_title, [authors], 1)
]

# -- Options for Texinfo output -----------------------------------------------

texinfo_documents = [
    (master_doc,  # source start file
     "pytest_plt",  # target name
     project,  # title
     authors,  # author
     "pytest_plt",  # dir menu entry
     "Fixtures for quickly making Matplotlib plots in tests",  # description
     "Miscellaneous"),  # category
]
