.. _patterns:

Patterns
========

.. currentmodule: flask_coney

Flask-Coney can be used to archive different messaging patterns. A
few typical patterns, found on `RabbitMQ Tutorials`_, will be
displayed here.

.. _RabbitMQ Tutorials: https://www.rabbitmq.com/getstarted.html

Hallo World
-----------

In this example we have two services (aka flask applications).
Service 1 will receive data from a http post request. It will send
this data to the message broker with the routing_key "process".
Service 2 will pick up any message with the routing key "process",
process and store the data. Service 2 also provides an api endpoint,
which allows a user to request the processed data.

Service 1
~~~~~~~~~

.. literalinclude:: ../examples/hello_world/service1/main.py

Serivce 2
~~~~~~~~~

.. literalinclude:: ../examples/hello_world/service2/main.py


Work queues
-----------

Publish/Subscribe
-----------------

Routing
-------

Topics
------

Request/Reply
-------------
