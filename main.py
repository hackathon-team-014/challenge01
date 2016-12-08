from flask import Flask, request
from flask import jsonify

import logging
import json
import base64
import google_datastore

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to Forte-Team endpoint.'

@app.route('/api/status', methods=['GET'])
def status():
    data = {}
    try:
        return jsonify(insert=True, fetch=True, delete=True, list=True), 200
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500
        
@app.route('/api/capitals/<id>', methods=['PUT'])
def insert(id):
    try:
        received_json = request.get_json()
        my_dump = json.dumps(received_json)
        print my_dump

        gds = google_datastore.GoogleDataStore()
        gds.insert(id, received_json)
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500

    return 'Successfully stored the capital', 200

@app.route('/api/capitals/<id>', methods=['DELETE'])
def delete(id):
    try:
        gds = google_datastore.GoogleDataStore()
        if len(gds.fetch(id)) == 0:
            return jsonify(code=404, message='Capital record not found'), 404
        gds.delete(id)
    except Exception as e:
        return jsonify(code=500, message=e), 500

    return 'Capital object delete status', 200

@app.route('/api/capitals/<id>', methods=['GET'])
def fetch(id):
    try:
        print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()
        print 'fetching...'
        result = gds.fetch(id)
        print result
        if len(result) == 0:
            return jsonify(code=404, message='Capital record not found'), 404

        return jsonify(result), 200
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500

@app.route('/api/capitals', methods=['GET'])
def fetch_all():
    try:
        #print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()
        #print 'fetching...'
        result = gds.fetch_all()
        #print result
        j_result = jsonify(result)
        #print j_result
        return j_result, 200
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500

if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)