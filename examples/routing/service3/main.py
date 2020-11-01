from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@coney.queue(queue_name="logs_info", exchange_name="logs", routing_key="info")
def info_queue(ch, method, props, body):
    print(body, flush=True)
