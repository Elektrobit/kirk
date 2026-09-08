# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

curdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(curdir, "..")))

project = "kirk"
copyright = "2025, Linux Test Project"
author = "Linux Test Project"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
]

templates_path = ["_templates"]
exclude_patterns = ["html*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = []


def run_apidoc(_):
    """
    Autogenerate API documentation.
    """
    doc_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(doc_dir, ".."))

    packages = {
        os.path.join(doc_dir, "kirk"): os.path.join(project_root, "libkirk"),
    }

    argv_list = []
    for output, source in packages.items():
        argv_list.append([
            "--implicit-namespaces",
            "-f",
            "-o",
            output,
            source,
            os.path.join(project_root, "libkirk", "tests"),
        ])

    try:
        # Sphinx 1.7+
        from sphinx.ext import apidoc

        for argv in argv_list:
            apidoc.main(argv)
    except ImportError:
        # Sphinx 1.6 (and earlier)
        from sphinx import apidoc

        for argv in argv_list:
            argv.insert(0, apidoc.__file__)
            apidoc.main(argv)


def setup(app):
    app.connect("builder-inited", run_apidoc)
