from flask import Flask, request
from flask import jsonify
from google.cloud import pubsub
from flask.globals import current_app
from flask import Blueprint, render_template, redirect, url_for

import logging
import json
import google_datastore
import cloudstorage

app = Flask(__name__)

@app.route('/map', methods=['GET'])
def map():
    # result = dict()
    # result['country'] = 'Brazil'
    # result['latidude'] = 0
    # result['longitude'] = 0
    # res = list()
    # res.append(result)
            
    gds = google_datastore.GoogleDataStore()
    all_entities = gds.fetch_allunique()

    res = list()
    for entity in all_entities:
        e = dict()
        e['id'] = entity['id']
        e['latitude'] = entity['location']['latitude']
        e['longitude'] = entity['location']['longitude']
        e['name'] = entity['name']
        res.append(e)
        #print res

    return render_template("maps.html", comment= None, results = res)


@app.route('/capitals', methods=['GET'])
def fetch_allUnique():
    try:
        #print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()

        result = list()
        print 'before gds.fetch_allUnique'
        result = gds.fetch_allunique()
        print 'after gds.fetch_allUnique'
        #print result
        j_result = jsonify(result)
        #print j_result
        return render_template('capitals.html', comment= None, results = result)
    except Exception as e:
        print e
        return jsonify(code=500, message='Unexpected error'), 500


@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to Forte-Team endpoint.'

@app.route('/api/status', methods=['GET'])
def status():
    data = {}
    try:
        return jsonify(insert=True, fetch=True, delete=True, list=True, storage=True, pubsub=True, query=True, search=True), 200
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500
        
@app.route('/api/capitals/<id>/publish', methods=['POST'])
def publish(id):
    try:
        received_json = request.get_json()
        my_dump = json.dumps(received_json)
        print my_dump

        # projects/the-depot/topic/hack-it 
        print received_json['topic'].split('/')[1]
        pubsub_client = pubsub.Client(project=received_json['topic'].split('/')[1])

        print 'got a pubsub client!!!', received_json['topic'].split('/')[3] 
        topic_name = received_json['topic'].split('/')[3]
        print topic_name
        topic = pubsub_client.topic(topic_name)
        print 'get topic from client!!!!'

        #topic_name_list = list()
        #for t in pubsub_client.list_topics():
            #topic_name_list.append(t.name)

        #if topic_name not in topic_name_list:
            #topic.create()

        print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()
        print 'fetching...'
        result = gds.fetch(id)
        print 'got the result:'
        print result

        if result == None:
            return jsonify(code=404, message='Capital record not found'), 404

        print json.dumps(result)
        data = json.dumps(result)
        data = data.encode('utf-8')

        print 'Publishing on topic {}...'.format(topic_name)
        message_id = topic.publish(data)
        print 'Published on topic {}'.format(topic_name)

        print('Message {} published.'.format(message_id))
        return current_app.response_class(('{ "messageId": ' + str(message_id) + ' }', '\n'), mimetype=current_app.config['JSONIFY_MIMETYPE']), 200

    except Exception as e:
        print e
        return jsonify(code=500, message='Unexpected error'), 500

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
        if result == None:
            return jsonify(code=404, message='Capital record not found'), 404

        print "Create Bucket...."
        gcs.store_file_to_gcs(bucket_name, str(json.dumps(result)), str(id))
        print "Successfully stored in GCS"

    except Exception as e:
        print e
        return jsonify(code=500, message='Unexpected error'), 500


    print 'final return!'
    return 'Successfully stored in GCS', 200

@app.route('/api/capitals/<id>', methods=['PUT'])
def insert(id):
    try:
        received_json = request.get_json()
        my_dump = json.dumps(received_json)
        print my_dump

        gds = google_datastore.GoogleDataStore()
        gds.insert(id, received_json)

        while (gds.fetch(id) == None):
            print 'waiting insert to be persisted...'
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500

    return 'Successfully stored the capital', 200    

@app.route('/api/capitals/<id>', methods=['DELETE'])
def delete(id):
    try:
        gds = google_datastore.GoogleDataStore()
        if gds.fetch(id) == None:
            return jsonify(code=404, message='Capital record not found'), 404
        gds.delete(id)

        while (gds.fetch(id) != None):
            print 'waiting delete to be persisted...'
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
        if result == None:
            return jsonify(code=404, message='Capital record not found'), 404

        return jsonify(result), 200
    except Exception as e:
        return jsonify(code=500, message='Unexpected error'), 500

@app.route('/api/capitals', methods=['GET'])
def fetch_all():
    try:
        #print 'Creating datastore facade'
        gds = google_datastore.GoogleDataStore()

        result = list()

        if 'query' in request.args:
            result = gds.query(request.args.get('query'))
        elif 'search' in request.args:
             result = gds.search(request.args.get('search'))
        else:
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