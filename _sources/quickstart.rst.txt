.. _quickstart:

Quickstart
==========

.. currentmodule: flask_coney

Queue up and come down the rabbit hole. Flask-Coney makes it very
easy to connect your flask application with eachother. On this page
examples on how to integrate Flask-Coney are shown. For the complete
guide, checkout the API documentation on the :class:`Coney` class.

A Minimal Application
---------------------

For the common case of having one Flask application all you have to
do is to create your Flask application, load the configuration of
choice and then create the :class:`Coney` object by passing it the
application.

Once created, that object can be used to decorate functions, which
consume messages send to certain queues and to publish message::

    from flask import Flask
    from flask_coney import Coney

    app = Flask(__name__)
    app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
    coney = Coney(app)

    @coney.queue(queue_name="test")
    def test_queue(ch, method, props, body):
        pass

    coney.publish("Hi", routing_key="test")
