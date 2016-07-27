'''
Created on Apr 29, 2015

@author: jeydurai
'''

import models.dataHandler
import tornado.gen


class LocationDAO():

    @tornado.gen.coroutine
    def getCollectionLocations(self, db):
        raise tornado.gen.Return(db['master_location'])

    @tornado.gen.coroutine
    def insertDocumentsInLocations(self, client, doc, logDic):
        try:
            dho = models.dataHandler.DataHandler()
            db = yield dho.getDBTrueNorth(client)
            collection = yield self.getCollectionLocations(db)
            result = yield collection.insert(doc)
            doc = {
                'updated_on' : logDic['updated_on'],
                'updated_by' : logDic['updated_by'],
                'activity' : logDic['activity'],
                'activity_description' : logDic['activity_description'],
                'reference_id' : logDic['reference_id']
            }
            collection = yield dho.getCollectionAdminLog(db)
            result = yield collection.insert(doc)
            client.close()
            raise tornado.gen.Return(('success', 'Inserted Successfully!'))
        except:
            raise tornado.gen.Return(('error', 'Record was not inserted'))

    @tornado.gen.coroutine
    def locationExists(self, client, location):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionLocations(db)
        obj = yield collection.find_one({"location" : location})
        client.close()
        if obj:
            raise tornado.gen.Return(True)
        else:
            raise tornado.gen.Return(False)

    @tornado.gen.coroutine
    def editLocation(self, client, locDetails, logDic):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionLocations(db)
        result = yield collection.update(
            {"location" : locDetails['oldlocation']}, 
                {"$set" : {
                    "location" : locDetails['location'],
                    "country" : locDetails['country'],
                    "gtmu" : locDetails['gtmu'],
                    "region" : locDetails['region'],
                    'modified.edited_by' : logDic['edited_by'],
                    'modified.edited_on' : logDic['edited_on']
                }
            }
        )
        doc = {
            'updated_on' : logDic['updated_on'],
            'updated_by' : logDic['updated_by'],
            'activity' : logDic['activity'],
            'activity_description' : logDic['activity_description'],
            'reference_id' : logDic['reference_id']
        }
        collection = yield dho.getCollectionAdminLog(db)
        result = yield collection.insert(doc)
        client.close()
        raise tornado.gen.Return(('success', 'Updated Successfully'))

    @tornado.gen.coroutine
    def removeLocation(self, client, location, logDic):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionLocations(db)
        result = yield collection.update(
            {'location' : location},
                {'$set' : {
                    'purged' : 1,
                    'modified.edited_by' : logDic['edited_by'],
                    'modified.edited_on' : logDic['edited_on']
                }
            }
        )
        doc = {
            'updated_on' : logDic['updated_on'],
            'updated_by' : logDic['updated_by'],
            'activity' : logDic['activity'],
            'activity_description' : logDic['activity_description'],
            'reference_id' : logDic['reference_id']
        }
        collection = yield dho.getCollectionAdminLog(db)
        result = yield collection.insert(doc)
        client.close()
        raise tornado.gen.Return(('success', 'Successfully removed the location'))

    @tornado.gen.coroutine
    def getLocations(self, client):
        locArray = []
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionLocations(db)
        cursor = collection.find({}, {"location" : 1, "_id" : 0})
        client.close()
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            locArray.append(doc)
        raise tornado.gen.Return(locArray)

    @tornado.gen.coroutine
    def getLocationCredentials(self, client, location):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionLocations(db)
        obj = yield collection.find_one({"location" : location})
        client.close()
        raise tornado.gen.Return(obj)
    
    @tornado.gen.coroutine
    def getAllLocationsData(self, client, access_code=0):
        locArray = []
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionLocations(db)
        if access_code == 1:
            cursor = collection.find({}, {'_id' : 0})
        else:
            cursor = collection.find({'purged' : 0}, {'_id' : 0})
        client.close()
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            locArray.append(doc)
        raise tornado.gen.Return(locArray)
