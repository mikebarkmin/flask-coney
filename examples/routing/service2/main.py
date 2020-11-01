from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@coney.queue(queue_name="logs_error", exchange_name="logs", routing_key="error")
def error_queue(ch, method, props, body):
    print(body, flush=True)


@coney.queue(queue_name="logs_warning", exchange_name="logs", routing_key="warning")
def warning_queue(ch, method, props, body):
    print(body, flush=True)
