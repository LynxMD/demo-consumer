import json

import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/health')
def health():
    with open("./config.json") as config_file:
        config = json.load(config_file)
    requests.get(config["server"])
    return "OK"
