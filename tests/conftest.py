import pytest
from flask import Flask
from pytest_rabbitmq import factories

from flask_coney import Coney

rabbitmq_proc = factories.rabbitmq_proc(port=8000)
rabbitmq = factories.rabbitmq("rabbitmq_proc")


@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@localhost:8000"
    return app


@pytest.fixture
def coney(app):
    return Coney(app, testing=True)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
