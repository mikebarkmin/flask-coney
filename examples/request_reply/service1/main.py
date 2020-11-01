from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@app.route("/rpc", methods=["GET"])
def rpc():
    response = coney.publish_sync("Hi", routing_key="rpc")

    return response
