How to contribute to Flask-Coney
=====================================

Thank you for considering contributing to Flask-Coney!


Reporting issues
----------------

Include the following information in your post:

-   Describe what you expected to happen.
-   If possible, include a `minimal reproducible example`_ to help us
    identify the issue. This also helps check that the issue is not with
    your own code.
-   Describe what actually happened. Include the full traceback if there
    was an exception.
-   List your Python, Flask-Coney, and Pika versions. If
    possible, check if this issue is already fixed in the latest
    releases or the latest code in the repository.

.. _minimal reproducible example: https://stackoverflow.com/help/minimal-reproducible-example


Submitting patches
------------------

If there is not an open issue for what you want to submit, prefer
opening one for discussion before working on a PR. You can work on any
issue that doesn't have an open PR linked to it or a maintainer assigned
to it. These show up in the sidebar. No need to ask if you can work on
an issue that interests you.

Include the following in your patch:

-   Use `Black`_ to format your code. This and other checks will run
    automatically if you install `pre-commit`_ using the instructions
    below.
-   Include tests if your patch adds or changes code. Make sure the test
    fails without your patch.
-   Update any relevant docs pages and docstrings. Docs pages and
    docstrings should be wrapped at 72 characters.
-   Add an entry in ``CHANGES.rst``. Use the same style as other
    entries. Also include ``.. versionchanged::`` inline changelogs in
    relevant docstrings.

.. _Black: https://black.readthedocs.io
.. _pre-commit: https://pre-commit.com


First time setup
~~~~~~~~~~~~~~~~

-   Download and install the `latest version of git`_.
-   Configure git with your `username`_ and `email`_.

    .. code-block:: text

        $ git config --global user.name 'your name'
        $ git config --global user.email 'your email'

-   Make sure you have a `GitHub account`_.
-   Fork Flask-Coney to your GitHub account by clicking the `Fork`_
    button.
-   `Clone`_ the main repository locally.

    .. code-block:: text

        $ git clone https://github.com/mikebarkmin/flask-coney
        $ cd flask-coney

-   Add your fork as a remote to push your work to. Replace
    ``{username}`` with your username.

    .. code-block:: text

        git remote add fork https://github.com/{username}/flask-coney

-   Create a virtualenv.

    .. code-block:: text

        $ python3 -m venv env
        $ . env/bin/activate

    On Windows, activating is different.

    .. code-block:: text

        > env\Scripts\activate

-   Install Flask-Coney in editable mode with development
    dependencies.

    .. code-block:: text

        $ pip install -e . -r requirements/dev.txt

-   Install the pre-commit hooks.

    .. code-block:: text

        $ pre-commit install

.. _latest version of git: https://git-scm.com/downloads
.. _username: https://help.github.com/en/articles/setting-your-username-in-git
.. _email: https://help.github.com/en/articles/setting-your-commit-email-address-in-git
.. _GitHub account: https://github.com/join
.. _Fork: https://github.com/pallets/flask/fork
.. _Clone: https://help.github.com/en/articles/fork-a-repo#step-2-create-a-local-clone-of-your-fork


Start coding
~~~~~~~~~~~~

-   Create a branch to identify the issue you would like to work on. If
    you're submitting a bug or documentation fix, branch off of the
    latest ".x" branch.

    .. code-block:: text

        $ git checkout -b your-branch-name origin/2.x

    If you're submitting a feature addition or change, branch off of the
    "master" branch.

    .. code-block:: text

        $ git checkout -b your-branch-name origin/master

-   Using your favorite editor, make your changes,
    `committing as you go`_.
-   Include tests that cover any code changes you make. Make sure the
    test fails without your patch. Run the tests as described below.
-   Push your commits to your fork on GitHub and
    `create a pull request`_. Link to the issue being addressed with
    ``fixes #123`` in the pull request.

    .. code-block:: text

        $ git push --set-upstream fork your-branch-name

.. _committing as you go: https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes
.. _create a pull request: https://help.github.com/en/articles/creating-a-pull-request


Running the tests
~~~~~~~~~~~~~~~~~

You need to have rabbitmq installed on your system.

.. code-block:: text

  $ RABBITMQ_VERSION=3.8.5
  $ wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v$RABBITMQ_VERSION/rabbitmq-server-generic-unix-$RABBITMQ_VERSION.tar.xz
  $ tar -xf rabbitmq-server-generic-unix-$RABBITMQ_VERSION.tar.xz
  $ mv rabbitmq_server-$RABBITMQ_VERSION rabbitmq_server
  $ rm rabbitmq-server-generic-unix-$RABBITMQ_VERSION.tar.xz

Run the basic test suite with pytest.

.. code-block:: text

    $ python -m mypy
    $ pytest

This runs the tests for the current environment, which is usually
sufficient. CI will run the full suite when you submit your pull
request. You can run the full test suite with tox if you don't want to
wait.

.. code-block:: text

    $ tox


Running test coverage
~~~~~~~~~~~~~~~~~~~~~

Generating a report of lines that do not have test coverage can indicate
where to start contributing. Run ``pytest`` using ``coverage`` and
generate a report.

.. code-block:: text

    $ pip install -r requirements/tests.txt
    $ pytest --cov --cov-append --cover-report=term-missing

Open ``htmlcov/index.html`` in your browser to explore the report.

Read more about `coverage <https://coverage.readthedocs.io>`__.


Building the docs
~~~~~~~~~~~~~~~~~

Build the docs in the ``docs`` directory using Sphinx.

.. code-block:: text

    $ cd docs
    $ make html

Open ``_build/html/index.html`` in your browser to view the docs.

Read more about `Sphinx <https://www.sphinx-doc.org/en/stable/>`__.

Release
~~~~~~~

Change ``__version__`` in ``src/flask_coney/__init__.py``.

.. code-block:: text

  $ python setup.py sdist
  $ pip install twine
  $ twine upload dist/*
