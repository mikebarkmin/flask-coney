from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@app.route("/pub", methods=["POST"])
def pub():
    coney.publish("A message", exchange_name="notify", routing_key="")
    return "It will be process by service2 and service3"
