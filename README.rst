Flask-Coney
===========

.. image:: https://badge.fury.io/py/Flask-Coney.svg
    :target: https://pypi.org/project/Flask-Coney/
    :alt: PyPi

.. image:: https://img.shields.io/readthedocs/flask-coney
    :target: https://flask-coney.readthedocs.io/en/latest/
    :alt: Read the Docs

.. image:: https://github.com/mikebarkmin/flask-coney/workflows/Tests/badge.svg?branch=master
    :target: https://github.com/mikebarkmin/flask-coney/actions?query=workflow%3ATests
    :alt: Tests

.. image:: https://codecov.io/gh/mikebarkmin/flask-coney/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mikebarkmin/flask-coney
    :alt: Coverage


Flask-Coney is an extension for `Flask`_ that adds support for
`Pika`_ to your application. It aims to simplify using Pika
with Flask by providing useful defaults and extra helpers that make it
easier to accomplish common tasks.

.. _Flask: https://palletsprojects.com/p/flask/
.. _Pika: https://pika.readthedocs.io/en/stable/


Installing
----------

Install and update using `pip`_:

.. code-block:: text

  $ pip install -U Flask-Coney

.. _pip: https://pip.pypa.io/en/stable/quickstart/


A Simple Example
----------------

.. code-block:: python

    from flask import Flask
    from flask_coney import Coney

    app = Flask(__name__)
    app.config["CONEY_BROKER_URI"] = "sqlite:///example.sqlite"
    coney = Coney(app)

    @coney.queue(queue_name="test")
    def test_queue(ch, method, props, body):
        pass


    def publish_to_queue():
        coney.publish({"test": 1}, routing_key="test")

Contributing
------------

For guidance on setting up a development environment and how to make a
contribution to Flask-Coney, see the `contributing guidelines`_.

.. _contributing guidelines: https://github.com/mikebarkmin/flask-coney/blob/master/CONTRIBUTING.rst


Links
-----

-   Documentation: https://flask-coney.readthedocs.io
-   Releases: https://pypi.org/project/Flask-Coney/
-   Code: https://github.com/mikebarkmin/flask-coney
-   Issue tracker: https://github.com/mikebarkmin/flask-coney/issues
