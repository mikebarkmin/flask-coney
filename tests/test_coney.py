import json
import time

import pytest
from rabbitpy import Exchange
from rabbitpy import Message
from rabbitpy import Queue

from flask_coney import Coney


def test_init_app(app):
    coney = Coney()
    coney.init_app(app)

    assert coney.app is None
    assert app.extensions["coney"] is not None


def test_queue_temporary(coney, rabbitmq_proc):
    @coney.queue()
    def tmp():
        pass

    gen = [q for q in rabbitmq_proc.list_queues() if "amq.gen" in q]

    assert len(gen) == 1


def test_queue_default_exchange(rabbitmq, rabbitmq_proc, app, coney):
    @coney.queue(queue_name="test")
    def test_queue(ch, method, props, body):
        pass

    queues = rabbitmq_proc.list_queues()
    assert "test" in queues


def test_queue_default_exchange_routing_key_mismatch(coney):
    with pytest.raises(RuntimeError):

        @coney.queue(queue_name="test", routing_key="test2")
        def test_queue(ch, method, props, body):
            pass


def test_queue_custom_exchange(rabbitmq, rabbitmq_proc, coney):
    @coney.queue(queue_name="hi", exchange_name="hu")
    def hi_queue(ch, method, props, body):
        assert b"dadada" == body
        coney._stop_consuming()

    exchanges = rabbitmq_proc.list_exchanges()
    assert "hu" in exchanges

    queues = rabbitmq_proc.list_queues()
    assert "hi" in queues

    channel = rabbitmq.channel()
    message = Message(channel, "dadada")
    message.publish("hu", "hi")

    coney._consuming()


def test_queue_custom_routing_key(rabbitmq, rabbitmq_proc, coney):
    @coney.queue(queue_name="hi", exchange_name="hu", routing_key="custom")
    def hi_queue(ch, method, props, body):
        assert b"dadada" == body
        coney._stop_consuming()

    exchanges = rabbitmq_proc.list_exchanges()
    assert "hu" in exchanges

    queues = rabbitmq_proc.list_queues()
    assert "hi" in queues

    channel = rabbitmq.channel()
    message = Message(channel, "dadada")
    message.publish("hu", "custom")

    coney._consuming()


def test_queue_json(rabbitmq, coney):
    @coney.queue(queue_name="hi", exchange_name="hu", routing_key="custom")
    def hi_queue(ch, method, props, body):
        response = {"Hi": "hu"}
        assert response == body
        coney._stop_consuming()

    channel = rabbitmq.channel()
    message = Message(
        channel,
        json.dumps({"Hi": "hu"}),
        properties={"content_type": "application/json"},
    )
    message.publish("hu", "custom")
    coney._consuming()


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


def test_publish_sync(coney):
    @coney.queue(queue_name="echo", exchange_name="sync")
    def echo_queue(ch, method, props, body):
        body = {**body, "echo": True}
        coney.reply_sync(ch, method, props, body)

    coney.testing = False
    coney.run()

    time.sleep(1)

    result = coney.publish_sync({"Hi": "Ho"}, exchange_name="sync", routing_key="echo")

    assert result == {"Hi": "Ho", "echo": True}
