from flask import Flask, request
from flask import jsonify

import logging
import json
import base64
import google_datastore
from google.cloud import pubsub
import base64
import cloudstorage

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to Forte-Team endpoint.'

@app.route('/api/status', methods=['GET'])
def status():
    data = {}
    try:
        return jsonify(insert=True, fetch=True, delete=True, list=True, store=True, publish=True, query=False, search=False), 200
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500
        
@app.route('/api/capitals/<id>/publish', methods=['POST'])
def publish(id):
    try:
        received_json = request.get_json()
        my_dump = json.dumps(received_json)
        print my_dump

        pubsub_client = pubsub.Client()
        print 'got a pubsub client!!!'
        #topic_name = received_json['topic']
        topic_name = 'hack_test'
        print topic_name
        topic = pubsub_client.topic(topic_name)
        print 'get topic from client!!!!'
        #topic.create()

        print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()
        print 'fetching...'
        result = gds.fetch(id)
        print 'got the result:'
        print result
        if len(result) == 0:
            return jsonify(code=404, message='Capital record not found'), 404

        res =  str(result)
        print res
        #data=result.encode('utf-8')
        res1 = 'hi'
        data = base64.b64encode(res1) 
        data=data.encode('utf-8')
        print 'encoded result:' 
        print data  

        topic.publish(data)

    except Exception as e:
        print e
        return jsonify(code=500, message='Unexpected error'), 500


    return jsonify(messageId=id), 'Successfully published to topic', 200

        
@app.route('/api/capitals/<id>/store', methods=['POST'])
def store(id):
    try:
        gcs = cloudstorage.Storage()
        received_json = request.get_json()
        my_dump = json.dumps(received_json)
        print my_dump

        bucket_name = received_json['bucket']
        print bucket_name

        print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()
        print 'fetching...'
        result = gds.fetch(id)
        print 'got the result:'
        print result
        if len(result) == 0:
            return jsonify(code=404, message='Capital record not found'), 404

        print "Create Bucket...."
        gcs.store_file_to_gcs(bucket_name, str(result), str(id))
        print "Successfully stored in GCS"

    except Exception as e:
        print e
        return jsonify(code=500, message='Unexpected error'), 500


    return 'Successfully stored in GCS', 200

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