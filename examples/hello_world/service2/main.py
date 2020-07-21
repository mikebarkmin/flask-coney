from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@coney.queue(queue_name="process")
def process_queue(ch, method, props, body):
    # do something with body
    processed_body = body
    print(processed_body, flush=True)
