from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@coney.queue(queue_name="rpc")
def rpc_queue(ch, method, props, body):
    result = f"{body.decode('utf-8')} touched by me"
    print(result, flush=True)
    coney.reply_sync(ch, method, props, result)
