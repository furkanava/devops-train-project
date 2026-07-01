import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_ENV = os.environ.get("APP_ENV", "development")


@app.route("/")
def index():
    return jsonify({
        "message": "Hello from DevOps Intern Project!",
        "env": APP_ENV
    })


@app.route("/ping")
def ping():
    return jsonify({"pong": True})


# TODO (Görev - Hafta 2): /health endpoint'ini buraya ekle

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=(APP_ENV == "development")) 