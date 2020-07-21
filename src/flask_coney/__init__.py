import json
import logging
import threading
import time
import uuid
from contextlib import contextmanager
from typing import Callable
from typing import Union

import pika
from flask import current_app
from flask import Flask
from retry import retry

from .consumer import ReconnectingConsumer
from .encoder import UUIDEncoder
from .exceptions import ExchangeTypeError
from .exceptions import SyncTimeoutError
from .exchange import ExchangeType

__version__ = "1.1.4"


def get_state(app):
    """Gets the state for the application"""
    assert "coney" in app.extensions, (
        "The coney extension was not registered to the current "
        "application. Please make sure to call init_app() first."
    )
    return app.extensions["coney"]


class _ConeyState:
    """Remembers configuration for the (coney, app) tuple."""

    def __init__(self, coney):
        self.coney = coney
        self.consumer_threads = []
        self.data = {}


class Coney:
    """
    This class is used to control the Coney integration to one or more Flask
    applications. Depending on how you initialize the object it is usable right
    away or will attach as needed to a Flask application.

    There are two usage modes which work very similarly. One is binding the
    instance to a very specific Flask application::

        app = Flask(__name__)
        coney = Coney(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        coney = Coney()

        def create_app():
            app = Flask(__name__)
            coney.init_app(app)
            return app

    To listen on a queue use::

        coney = Coney(app)

        @coney.queue(queue_name="test")
        def queue_test(ch, method, props, body):
            pass

    To publish a message use::

        coney = Coney(app)

        coney.publish({"test": 1})

    :param app: A flask app
    :param testing: Setup testing mode. This will not invoke threads
    """

    def __init__(self, app: Flask = None, testing: bool = False):
        self.app = app
        self.thread = None
        self.testing = testing
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        This callback can be used to initialize an application for the use
        with Coney.
        """
        # We intentionally don't set self.app = app, to support multiple
        # applications. If the app is passed in the constructor,
        # we set it and don't support multiple applications.

        # noqa: B950 CONEY_URI: see https://pika.readthedocs.io/en/stable/modules/parameters.html#pika.connection.URLParameters
        if not (app.config.get("CONEY_BROKER_URI")):
            raise RuntimeError("CONEY_BROKER_URI needs to be set")

        self.broker_uri = app.config.get("CONEY_BROKER_URI")

        app.extensions["coney"] = _ConeyState(self)

    def get_app(self, reference_app: Flask = None):
        """
        Helper method that implements the logic to look up an application.

        :param reference_app: A flask app
        """
        if reference_app is not None:
            return reference_app

        if current_app:
            return current_app._get_current_object()

        if self.app is not None:
            return self.app

        raise RuntimeError(
            "No application found. Either work inside a view function or push"
            " an application context. See"
            " http://mikebarkmin.github.io/flask-coney/contexts/."
        )

    @contextmanager
    def channel(self, app: Flask = None) -> pika.channel.Channel:
        """Provides context for a channel.

        Example::

            with channel(app) as ch:
                ch.basic_publish()

        :param app: A flask app
        """
        with self.connection() as c:
            yield c.channel()

    @contextmanager
    @retry(pika.exceptions.AMQPConnectionError, tries=4, delay=1, jitter=3)
    def connection(self, app: Flask = None) -> pika.BlockingConnection:
        """Provides context for a connection.

        Example::

            with connection(app) as c:
                c.channel()

        :param app: A flask app
        """
        app = self.get_app(app)
        params = pika.URLParameters(self.broker_uri)
        connection = pika.BlockingConnection(params)

        try:
            yield connection
        finally:
            connection.close()

    def queue(
        self,
        queue_name: str = "",
        exchange_name: str = "",
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        routing_key: str = None,
        app: Flask = None,
    ) -> Callable:
        """
        A decorator for consuming a queue. A thread will start in the
        background, if no other thread for this purpose was already started.
        There will only be one thread for every queue.

        Example::

            @coney.queue(queue_name="test")
            def queue_test(ch, method, props, body):
                pass

        :param type: ExchangeType
        :param queue_name: Name of the queue
        :param exchange_name: Name of the exchange
        :param exchange_type: Type of the exchange
        :param routing_key: The routing key
        :param app: A flask app
        """
        app = self.get_app(app)
        state = get_state(app)

        if (
            exchange_type == ExchangeType.FANOUT
            or exchange_type == ExchangeType.DIRECT
            or exchange_type == ExchangeType.TOPIC
            or exchange_type == ExchangeType.HEADERS
        ):
            if not queue_name:
                # If queue name is empty, then declare a temporary queue
                with self.channel(app) as channel:
                    result = channel.queue_declare(
                        queue=queue_name,
                        passive=False,
                        durable=False,
                        exclusive=False,
                        auto_delete=False,
                    )
                    queue_name = result.method.queue

            if exchange_name == "" and routing_key and routing_key != queue_name:
                # on default exchange it will be automaticaly bound ot quene_name
                raise RuntimeError(
                    """Routing key mismatch.
                    Queues on default exchange should
                    not have a routing key."""
                )
        else:
            raise ExchangeTypeError(f"Exchange type {exchange_type} is not supported")

        def decorator(func):
            consumer = ReconnectingConsumer(
                self.broker_uri,
                exchange=exchange_name,
                exchange_type=exchange_type,
                queue=queue_name,
                routing_key=routing_key,
                on_message=func,
            )
            thread = threading.Thread(target=consumer.run)
            state.consumer_threads.append((consumer, thread))
            thread.start()
            return func

        return decorator

    def _accept(self, corr_id: str, result: str, app: Flask = None):
        app = self.get_app(app)
        data = get_state(app).data
        data[corr_id]["is_accept"] = True
        data[corr_id]["result"] = result

        with self.channel(app) as channel:
            channel.queue_delete(data[corr_id]["reply_queue_name"])

    def _on_response(
        self,
        ch: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        props: pika.spec.BasicProperties,
        body: str,
        app=None,
    ):
        logging.info(f"on response => {body}")

        corr_id = props.correlation_id
        if props.content_type == "application/json":
            body = json.loads(body)

        self._accept(corr_id, body, app=app)

    def publish(
        self,
        body: Union[str, dict],
        exchange_name: str = "",
        routing_key: str = None,
        durable: bool = False,
        properties: dict = None,
        app: Flask = None,
    ):
        """
        Will publish a message

        Example::

            @app.route('/process'):
            def process():
                coney.publish({"text": "process me"})

        :param body: Body of the message, either a string or a dict
        :param exchange_name: The exchange
        :param exchange_type: The type of the exchange
        :param routing_key: The routing key
        :param durable: Should the exchange be durable
        :param app: A flask app
        """
        with self.channel(app) as channel:
            if properties is None:
                properties = {"content_type": "text/plain"}

            if isinstance(body, dict):
                body = json.dumps(body, cls=UUIDEncoder)
                properties["content_type"] = "application/json"

            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(**properties),
            )

    def reply_sync(
        self,
        ch: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: str,
        app=None,
    ):
        """
        Will reply to a message, which was send by :meth:`publish_sync`

        Example::

            @queue(queue_name="rpc")
            def concat_callback(ch, method, props, body):
                result = body["a"] + body["b"]
                body = {"result": result}
                coney.reply_sync(ch, method, props, body)

        This is a conveniences short hand method for::

            @queue(queue_name="rpc")
            def concat_callback(ch, method, props, body):
                result = body["a"] + body["b"]
                body = {"result": result}
                self.publish(
                    body,
                    routing_key=properties.reply_to,
                    properties={"correlation_id": properties.correlation_id},
                    app=app,
                )

        :parameter ch:
        :parameter method:
        :parameter properties:
        :parameter body: The message to send

        """
        self.publish(
            body,
            routing_key=properties.reply_to,
            properties={"correlation_id": properties.correlation_id},
            app=app,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def publish_sync(
        self,
        body: Union[str, dict],
        exchange_name: str = "",
        routing_key: str = None,
        properties: dict = None,
        timeout: float = 10,
        app: Flask = None,
    ):
        """
        Will publish a message and wait for the response

        Example::

            # client
            @app.route('/concat')
            def concat():
                a = request.args.get('a')
                b = request.args.get('b')

                body = {'a': a, 'b': b}
                result = coney.publish_sync(body, routing_key="rpc")
                return result

            # server
            @queue(queue_name="rpc")
            def concat_callback(ch, method, props, body):
                result = body["a"] + body["b"]
                body = {"result": result}
                coney.reply_sync(ch, method, props, body)

        :param body: Body of the message, either a string or a dict
        :param exchange_name: The exchange
        :param routing_key: The routing key
        :param properties: see :py:class:`pika.spec.BasicProperties`
        :param timeout: Timeout in seconds
        :param app: A flask app
        :raises:
            SyncTimeoutError: if no message received in timeout
        """

        app = self.get_app(app)
        with self.connection(app) as connection:
            corr_id = str(uuid.uuid4())
            channel = connection.channel()
            result = channel.queue_declare(queue="", exclusive=False, auto_delete=True)
            callback_queue = result.method.queue
            state = get_state(app)
            state.data[corr_id] = {
                "is_accept": False,
                "result": None,
                "reply_queue_name": callback_queue,
            }
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(callback_queue, self._on_response, auto_ack=True)

            if properties is None:
                properties = {"content_type": "text/plain"}

            if isinstance(body, dict):
                body = json.dumps(body, cls=UUIDEncoder)
                properties["content_type"] = "application/json"

            channel.basic_publish(
                exchange="",
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    **properties, reply_to=callback_queue, correlation_id=corr_id,
                ),
            )

            end = time.time() + timeout

            while time.time() < end:
                if state.data[corr_id]["is_accept"]:
                    logging.info("Got the RPC server response")
                    return state.data[corr_id]["result"]
                else:
                    connection.process_data_events()
                    time.sleep(0.3)
            raise SyncTimeoutError()
