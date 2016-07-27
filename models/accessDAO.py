'''
Created on Apr 29, 2015

@author: jeydurai
'''

import models.dataHandler
import tornado.gen


class AccessDAO():

    @tornado.gen.coroutine
    def getCollectionAccess(self, db):
        raise tornado.gen.Return(db['master_access'])

    @tornado.gen.coroutine
    def getCollectionPeriodAccess(self, db):
        raise tornado.gen.Return(db['period_access'])

    @tornado.gen.coroutine
    def getCollectionProdSerAccess(self, db):
        raise tornado.gen.Return(db['prodser_access'])

    @tornado.gen.coroutine
    def getDesignations(self, client):
        desigArray = []
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionAccess(db)
        tempArray = yield collection.find({}).distinct('access_description')
        for element in tempArray:
            if element != '' and element is not None:
                desigArray.append(element)
        list.sort(desigArray)
        client.close()
        raise tornado.gen.Return(list(set(desigArray)))

    @tornado.gen.coroutine
    def getAccessCredentials(self, client, designation):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionAccess(db)
        obj = yield collection.find_one({"access_description" : designation})
        client.close()
        raise tornado.gen.Return(obj)

    @tornado.gen.coroutine
    def getPeriodAccessCredentials(self, client, period):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionPeriodAccess(db)
        obj = yield collection.find_one({"period" : period})
        client.close()
        raise tornado.gen.Return(obj)

    @tornado.gen.coroutine
    def getProdSerAccessCredentials(self, client, prod_ser):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionProdSerAccess(db)
        obj = yield collection.find_one({"prod_ser" : prod_ser})
        client.close()
        raise tornado.gen.Return(obj)
