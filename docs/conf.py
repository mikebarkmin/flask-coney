from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# Project ---------------------------------------------------------------------

project = "Flask Coney"
copyright = "2020, Mike Barkmin"
author = "Mike Barkmin"
release, version = get_version("Flask-Coney", version_length=1)

# General ---------------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
    "sphinx_issues",
]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "flask": ("https://flask.palletsprojects.com/en/1.1.x/", None),
    "pika": ("https://pika.readthedocs.io/en/stable/", None),
}

issues_github_path = "mikebarkmin/flask-coney"


# -- Options for HTML output ----------------------------------------------

html_theme = "flask"
html_context = {
    "project_links": [
        ProjectLink("Website", "https://www.barkmin.eu"),
        ProjectLink("PyPI releases", "https://pypi.org/project/Flask-Coney/"),
        ProjectLink("Source Code", "https://github.com/mikebarkmin/flask-coney/"),
        ProjectLink(
            "Issue Tracker", "https://github.com/mikebarkmin/flask-coney/issues/"
        ),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_favicon = "_static/flask-coney-logo.png"
html_logo = "_static/flask-coney-logo.png"
html_title = f"Flask-Coney Documentation ({version})"
html_static_path = ["_static"]
html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [
    (master_doc, f"Flask-Coney-{version}.tex", html_title, author, "manual",)
]
