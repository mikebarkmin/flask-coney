.. currentmodule:: flask_coney

Configuration
=============

The following configuration values exist for Flask-Coney.
Flask-Coney loads these values from your main Flask config which can
be populated in various ways.  Note that some of those cannot be modified
after the engine was created so make sure to configure as early as
possible and to not modify them at runtime.

Configuration Keys
------------------

A list of configuration keys currently understood by the extension:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================== =========================================
``CONEY_BROKER_URI``               The broker URI that should be used for
                                   the connection.  Examples:

                                   - ``amqp://username:password@host:80``
================================== =========================================

Connection URI Format
---------------------

For a complete list of connection URIs head over to the Pika
documentation under (`Supported Databases
<https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.URLParameters>`_).
