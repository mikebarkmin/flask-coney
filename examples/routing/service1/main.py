from flask import Flask
from flask_coney import Coney

app = Flask(__name__)
app.config["CONEY_BROKER_URI"] = "amqp://guest:guest@rabbitmq"
coney = Coney(app)


@app.route("/warning", methods=["POST"])
def warning():
    coney.publish("This is a warning", exchange_name="logs", routing_key="warning")
    return "Warning published"


@app.route("/error", methods=["POST"])
def error():
    coney.publish("This is an error", exchange_name="logs", routing_key="error")
    return "Error published"


@app.route("/info", methods=["POST"])
def info():
    coney.publish("This is an info", exchange_name="logs", routing_key="info")
    return "Info published"
