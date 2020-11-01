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

In this example service1 publishes a message. This message it then
either processed by service2 or service3, depending on how reads the
message first. This can be useful, if you want to split up the
workload.

Service 1
~~~~~~~~~

.. literalinclude:: ../examples/work_queues/service1/main.py

Service 2
~~~~~~~~~

.. literalinclude:: ../examples/work_queues/service2/main.py

Service 3
~~~~~~~~~

.. literalinclude:: ../examples/work_queues/service3/main.py


Publish/Subscribe
-----------------

In this example service1 publishes a message to an exchange. Because
it is a fanout exchange all queues will receive a copy of this
message. Thus, service2 and service3 will process the message.

Service 1
~~~~~~~~~

.. literalinclude:: ../examples/publish_subscribe/service1/main.py

Service 2
~~~~~~~~~

.. literalinclude:: ../examples/publish_subscribe/service2/main.py

Service 3
~~~~~~~~~

.. literalinclude:: ../examples/publish_subscribe/service3/main.py


Routing
-------

Service 1
~~~~~~~~~

.. literalinclude:: ../examples/routing/service1/main.py

Service 2
~~~~~~~~~

.. literalinclude:: ../examples/routing/service2/main.py

Service 3
~~~~~~~~~

.. literalinclude:: ../examples/routing/service3/main.py

Topics
------

Service 1
~~~~~~~~~

.. literalinclude:: ../examples/topics/service1/main.py

Service 2
~~~~~~~~~

.. literalinclude:: ../examples/topics/service2/main.py

Service 3
~~~~~~~~~

.. literalinclude:: ../examples/topics/service3/main.py

Request/Reply
-------------

Service 1
~~~~~~~~~

.. literalinclude:: ../examples/request_reply/service1/main.py

Service 2
~~~~~~~~~

.. literalinclude:: ../examples/request_reply/service2/main.py
