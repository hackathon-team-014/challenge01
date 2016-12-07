import logging
import json
import base64

from flask import Flask, request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to Forte-Team endpoint.'

if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)