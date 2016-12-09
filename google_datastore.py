from datetime import datetime
from google.cloud import datastore
from google.cloud.datastore.helpers import GeoPoint
#from google.appengine.ext import ndb

#class ForteTeamChallenge1(ndb.Model):
   # name = ndb.StringProperty()
   # country = ndb.StringProperty()
    #location = ndb.GeoPoint


class GoogleDataStore:
    def __init__(self):
        self.ds = datastore.Client(project='hackathon-team-014')
        self.kind = 'ForteTeamChallenge1'

    def insert(self, capitalId, received_json):
        # print 'retriving key'
        key = self.ds.key(self.kind, capitalId)
        # print 'getting entity'
        entity = datastore.Entity(key)

        print 'filling entity'
        entity['name'] = received_json['name']
        entity['countryCode'] = received_json['countryCode']
        entity['country'] = received_json['country']
        entity['id'] = received_json['id']
        entity['location'] = GeoPoint(received_json['location']['latitude'], received_json['location']['longitude'])
        entity['continent'] = received_json['continent']
        
        print entity

        #print 'put...'
        return self.ds.put(entity)

    def fetch_all(self):
        result = list()

        #print 'getting key'
        #key = self.ds.key(self.kind)

        #print 'getting query'
        query = self.ds.query(kind=self.kind)

        #print 'assembling list'
        for entity in list(query.fetch(20)):
            if 'location' in entity :
                location = dict()
                location['latitude'] = entity['location'].latitude
                location['longitude'] = entity['location'].longitude
                entity['location'] = location
            result.append(dict(entity))

        return result

    def fetch_allunique(self):
        result = []

       #print 'getting key'
        #key = self.ds.key(self.kind)

        print 'getting query'
  
        query = self.ds.query(kind=self.kind)

        print 'assembling list'

        for entity in list(query.fetch()):
            if 'location' in entity :
                location = dict()
                location['latitude'] = entity['location'].latitude
                location['longitude'] = entity['location'].longitude
                print location
                entity['location'] = location
            print 'before item def'
            item = {}
            print 'after item def'
            item['name'] = entity['name']
            item['country'] = entity['country']
            item['location'] = entity['location']  
            print 'after item' 
            if item not in result:     
                result.append(item)

        print 'end'

        return result

    def fetch(self, id):
        # print 'getting query'
        query = self.ds.query(kind=self.kind)

        # print 'add filter', id
        query.add_filter('id', '=', int(id))

        # print 'assembling list'
        for entity in list(query.fetch()):
            if 'location' in entity :
                location = dict()
                location['latitude'] = entity['location'].latitude
                location['longitude'] = entity['location'].longitude
                entity['location'] = location
            return dict(entity)

        # print result
        return None

    def delete(self, id):
        result = list()

        # print 'getting query'
        query = self.ds.query(kind=self.kind)

        # print 'add filter', id
        query.add_filter('id', '=', int(id) )

        # print 'assembling list'
        for entity in list(query.fetch()):
            # print entity.key
            self.ds.delete(entity.key)
            #entity.key.delete()

        return result

    def query(self, filter):
        result = list()

        #print 'getting key'
        key = self.ds.key(self.kind)

        print filter
        query = self.ds.query(kind=self.kind)
        prop, val = filter.split(':')
        print prop, val
        query.add_filter(prop, '=', val)

        #print 'assembling list'
        for entity in list(query.fetch()):
            if 'location' in entity :
                location = dict()
                location['latitude'] = entity['location'].latitude
                location['longitude'] = entity['location'].longitude
                print location
                entity['location'] = location
            result.append(dict(entity))

        return result
        
    def search(self, filter):
        result = list()

        #print 'getting key'
        key = self.ds.key(self.kind)

        print filter

        query = self.ds.query(kind=self.kind)
  
        #print 'assembling list'
        for entity in list(query.fetch()):
            if 'location' in entity :
                location = dict()
                location['latitude'] = entity['location'].latitude
                location['longitude'] = entity['location'].longitude
                print location
                entity['location'] = location
            if str(entity).find(filter) != -1:
                result.append(dict(entity))

        return result

    def fetch_allunique(self):
        result = []

       #print 'getting key'
        #key = self.ds.key(self.kind)

        #print 'getting query'
  
        query = self.ds.query(kind=self.kind)

        #print 'assembling list'

        for entity in list(query.fetch()):
            if 'location' in entity :
                location = dict()
                location['latitude'] = entity['location'].latitude
                location['longitude'] = entity['location'].longitude
                entity['location'] = location
            #print 'before item def'
            item = {}
            #print 'after item def'
            item['id'] = entity['id']
            item['name'] = entity['name']
            item['country'] = entity['country']
            item['location'] = entity['location']  
            #print 'after item' 
            if item not in result:     
                result.append(item)

        #print 'end'

        return result
