# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import glob
import os.path
import pygments
import subprocess
from sphinx.errors import SphinxError, SphinxWarning

# -- Helper functions --------------------------------------------------------


def strip_ext(path):
    """ Remove the extension from a path. """
    return os.path.splitext(path)[0]


# -- Load our Pygments lexer -------------------------------------------------
def setup(app):
    from sphinx.highlighting import lexers

    this_dir = os.path.dirname(os.path.realpath(__file__))
    fish_indent_lexer = pygments.lexers.load_lexer_from_file(
        os.path.join(this_dir, "fish_indent_lexer.py"), lexername="FishIndentLexer"
    )
    lexers["fish-docs-samples"] = fish_indent_lexer
    # add_css_file only appears in Sphinx 1.8.0
    if hasattr(app, "add_css_file"):
        app.add_css_file("custom.css")
    else:
        app.add_stylesheet("custom.css")


# The default language to assume
highlight_language = "fish-docs-samples"

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "fish-shell"
copyright = "2020, fish-shell developers"
author = "fish-shell developers"

# Parsing FISH-BUILD-VERSION-FILE is possible but hard to ensure that it is in the right place
# fish_indent is guaranteed to be on PATH for the Pygments highlighter anyway
ret = subprocess.check_output(
    ("fish_indent", "--version"), stderr=subprocess.STDOUT
).decode("utf-8")
# The full version, including alpha/beta/rc tags
release = ret.strip().split(" ")[-1]
# The short X.Y version
version = release.rsplit(".", 1)[0]


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# !!! If you change this you also need to update the @import at the top
# of _static/fish-syntax-style.css
html_theme = "nature"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = {"**": ["globaltoc.html", "searchbox.html", "localtoc.html"]}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "fish-shelldoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "fish-shell.tex",
        "fish-shell Documentation",
        "fish-shell developers",
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------


def get_command_description(path, name):
    """ Return the description for a command, by parsing its synopsis line """
    with open(path) as fd:
        for line in fd:
            if line.startswith(name + " - "):
                _, desc = line.split(" - ", 1)
                return desc.strip()
    raise SphinxWarning("No description in file %s" % os.path.basename(path))


# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "fish-doc", "fish-shell Documentation", [author], 1),
    ("tutorial", "fish-tutorial", "fish-shell tutorial", [author], 1),
    ("CHANGELOG", "fish-changelog", "fish-shell changelog", [author], 1),
    ("completions", "fish-completions", "Writing fish completions", [author], 1),
    ("faq", "fish-faq", "fish-shell faq", [author], 1),
]
for path in sorted(glob.glob("cmds/*")):
    docname = strip_ext(path)
    cmd = os.path.basename(docname)
    man_pages.append((docname, cmd, get_command_description(path, cmd), "", 1))


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "fish-shell",
        "fish-shell Documentation",
        author,
        "fish-shell",
        "One line description of project.",
        "Miscellaneous",
    )
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]

# Disable smart-quotes to prevent double dashes from becoming emdashes.
smartquotes = False
