import requests, subprocess, json
from flask import Flask, request

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.json
    for alert in data.get("alerts", []):
        if alert["labels"]["alertname"] == "APIHighLatency":
            subprocess.run(["docker", "restart", "flask_api"])
        # You can add more actions for other alerts
        requests.post("http://mock-ticketing.local/incidents", json={"alert": alert})
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)