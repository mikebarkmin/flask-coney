from flask import Flask, request
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    # validation ...
    coney.publish(data, routing_key="process")

    return "will be processed, check service2"
