#!/usr/bin/env python3

import os

import pytest_plt

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "nengo_sphinx_theme.ext.versions",
]

# -- sphinx
nitpicky = True
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = ".rst"
source_encoding = "utf-8"
master_doc = "index"
project = "pytest_plt"
copyright = pytest_plt.__copyright__
author = "Applied Brain Research"
version = ".".join(pytest_plt.__version__.split(".")[:2])  # X.Y version
release = pytest_plt.__version__  # Full version with tags

# -- sphinx.ext.todo
todo_include_todos = True

# -- nengo_sphinx_theme
html_theme = "nengo_sphinx_theme"
pygments_style = "friendly"
templates_path = []
html_favicon = ""
html_static_path = ["_static"]
html_logo = os.path.join("_static", "logo.svg")
html_sidebars = {"**": ["sidebar.html"]}
html_context = {
    "css_files": [os.path.join("_static", "custom.css")],
}

# -- other
htmlhelp_basename = project

latex_elements = {
    # "papersize": "letterpaper",
    # "pointsize": "11pt",
    # "preamble": "",
    # "figure_align": "htbp",
}

latex_documents = [
    (master_doc,  # source start file
     "pytest_plt.tex",  # target name
     project,  # title
     author,  # author
     "manual"),  # documentclass
]

man_pages = [
    # (source start file, name, description, authors, manual section).
    (master_doc, "pytest_plt", project, [author], 1)
]

texinfo_documents = [
    (master_doc,  # source start file
     "pytest_plt",  # target name
     project,  # title
     author,  # author
     "pytest_plt",  # dir menu entry
     "Fixtures for quickly making Matplotlib plots in tests",  # description
     "Miscellaneous"),  # category
]
