import logging
import json
import base64

from flask import Flask, request
from flask import jsonify

app = Flask(__name__)



@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to Forte-Team endpoint.'

@app.route('/api/status', methods=['GET'])
def status():
    data = {}
    try:
        return jsonify(insert=False, fetch=False, delete=False, list=False), 200
    except Exception as e:
        return jsonify(code=0, message=e), 500

if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)