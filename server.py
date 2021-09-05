from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/health')
def health():
    config = json.load('./config.json')
    r = requests.get(config["server"])
    return "OK"
