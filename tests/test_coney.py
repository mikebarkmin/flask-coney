import json
import time

import pika
import pytest
from flask import Flask
from rabbitpy import Exchange
from rabbitpy import Message
from rabbitpy import Queue

from flask_coney import Coney
from flask_coney import ExchangeTypeError
from flask_coney import get_state
from flask_coney import SyncTimeoutError


def stop(app):
    time.sleep(1)
    for consumer, thread in get_state(app).consumer_threads:
        consumer.stop()
        thread.join()


def test_coney_broker_uri_not_set():
    app = Flask(__name__)
    with pytest.raises(RuntimeError):
        Coney(app)


def test_get_app_current_app(app, coney):
    my_app = coney.get_app()

    assert app == my_app


def test_get_app_property(app):
    coney = Coney(app)

    assert coney.app == app

    my_app = coney.get_app()

    assert my_app == app


def test_get_app_reference(app, coney):
    my_app = coney.get_app(reference_app=app)

    assert app == my_app


def test_get_app_missing():
    coney = Coney()

    with pytest.raises(RuntimeError):
        coney.get_app()


def test_connection(coney):
    with pytest.raises(pika.exceptions.AMQPConnectionError):
        with coney.connection():
            pass


def test_init_app(app):
    coney = Coney()
    coney.init_app(app)

    assert coney.app is None
    assert app.extensions["coney"] is not None


def test_queue_default_exchange(rabbitmq, rabbitmq_proc, app, coney):
    @coney.queue(queue_name="test")
    def test_queue(ch, method, props, body):
        pass

    time.sleep(1)

    queues = rabbitmq_proc.list_queues()
    assert "test" in queues

    stop(app)


def test_queue_default_exchange_routing_key_mismatch(coney, app):
    with pytest.raises(RuntimeError):

        @coney.queue(queue_name="test", routing_key="test2")
        def test_queue(ch, method, props, body):
            pass

    stop(app)


def test_queue_custom_exchange(rabbitmq, rabbitmq_proc, coney, app):
    @coney.queue(queue_name="hi", exchange_name="hu")
    def hi_queue(ch, method, props, body):
        assert b"dadada" == body

    time.sleep(1)

    exchanges = rabbitmq_proc.list_exchanges()
    assert "hu" in exchanges

    queues = rabbitmq_proc.list_queues()
    assert "hi" in queues

    channel = rabbitmq.channel()
    message = Message(channel, "dadada")
    message.publish("hu", "hi")

    stop(app)


def test_queue_custom_routing_key(rabbitmq, rabbitmq_proc, coney, app):
    @coney.queue(queue_name="hi", exchange_name="hu", routing_key="custom")
    def hi_queue(ch, method, props, body):
        assert b"dadada" == body

    time.sleep(1)

    exchanges = rabbitmq_proc.list_exchanges()
    assert "hu" in exchanges

    queues = rabbitmq_proc.list_queues()
    assert "hi" in queues

    channel = rabbitmq.channel()
    message = Message(channel, "dadada")
    message.publish("hu", "custom")

    stop(app)


def test_queue_json(rabbitmq, coney, app):
    @coney.queue(queue_name="hi", exchange_name="hu", routing_key="custom")
    def hi_queue(ch, method, props, body):
        response = {"Hi": "hu"}
        assert response == body

    time.sleep(1)

    channel = rabbitmq.channel()
    message = Message(
        channel,
        json.dumps({"Hi": "hu"}),
        properties={"content_type": "application/json"},
    )
    message.publish("hu", "custom")

    stop(app)


def test_queue_wrong_exchange_type(coney, rabbitmq, rabbitmq_proc, app):
    with pytest.raises(ExchangeTypeError):

        @coney.queue(exchange_name="hallo", exchange_type="not-right")
        def hallo_queue(ch, method, props, body):
            pass

    stop(app)


def test_publish(rabbitmq, coney):
    channel = rabbitmq.channel()
    exchange = Exchange(channel, "my-exchange", "direct")
    exchange.declare()
    queue = Queue(channel, "my-queue")
    queue.declare()
    queue.bind(exchange, "my-routing-key")

    coney.publish("Hi", exchange_name="my-exchange", routing_key="my-routing-key")

    for message in queue.consume():
        assert message.body == b"Hi"
        queue.stop_consuming()


def test_publish_sync(coney, app):
    @coney.queue(queue_name="echo", exchange_name="sync")
    def echo_queue(ch, method, props, body):
        body = {**body, "echo": True}
        coney.reply_sync(ch, method, props, body)

    time.sleep(1)

    result = coney.publish_sync({"Hi": "Ho"}, exchange_name="sync", routing_key="echo")

    assert result == {"Hi": "Ho", "echo": True}

    stop(app)


def test_publish_sync_timeout(coney, app):
    @coney.queue(queue_name="echo", exchange_name="sync")
    def echo_queue(ch, method, props, body):
        pass

    time.sleep(1)

    with pytest.raises(SyncTimeoutError):
        coney.publish_sync("Hi", routing_key="echo", timeout=0.01)

    stop(app)
