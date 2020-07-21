import pytest
from flask import Flask
from pytest_rabbitmq import factories

from flask_coney import Coney
from flask_coney import get_state

rabbitmq_proc = factories.rabbitmq_proc()
rabbitmq = factories.rabbitmq("rabbitmq_proc")


@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@localhost:6789"
    return app


@pytest.fixture
def coney(app):
    with app.app_context():
        coney = Coney(app)
        yield coney

        for consumer, thread in get_state(app).consumer_threads:
            consumer.stop()
            thread.join()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
