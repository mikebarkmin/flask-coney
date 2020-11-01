from flask import Flask
from flask_coney import Coney, ExchangeType

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@coney.queue(
    queue_name="service2.notify",
    exchange_name="notify",
    exchange_type=ExchangeType.FANOUT,
)
def notify_queue(ch, method, props, body):
    print(body, flush=True)
