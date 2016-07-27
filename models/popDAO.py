'''
Created on Apr 29, 2015

@author: jeydurai
'''

import models.dataHandler
import tornado.gen


class PopDAO():

    @tornado.gen.coroutine
    def getCollectionUniqueNodes(self, db):
        raise tornado.gen.Return(db['unique_nodes_all'])

    @tornado.gen.coroutine
    def getUniqueNodes(self, client, subSCMS):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUniqueNodes(db)
        client.close()
        result = collection.find({subSCMS:{'$exists':True}}, {'_id':0})
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def getUniqueSubSCMS(self, client):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUniqueNodes(db)
        subSCMS = yield collection.find({}).distinct('sub_scms')
        list.sort(subSCMS)    
        client.close()
        raise tornado.gen.Return(list(set(subSCMS)))

    @tornado.gen.coroutine
    def getUniqueGTMu(self, client):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUniqueNodes(db)
        gtmu = yield collection.find({}).distinct('gtmu')
        list.sort(gtmu)
        client.close()
        raise tornado.gen.Return(list(set(gtmu)))

    @tornado.gen.coroutine
    def getUniqueRegions(self, client, subSCMSList, gtmuList):
        regions = []
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUniqueNodes(db)
        for sub_scms in subSCMSList:
            for gtmu in gtmuList:
                q1 = {'sub_scms' : sub_scms,
                      'gtmu' : gtmu}
                tempArray = yield collection.find(q1).distinct('region')
                for element in tempArray:
                    if element != '' and element is not None:
                        regions.append(element)
        list.sort(regions)
        client.close()
        raise tornado.gen.Return (list(set(regions)))


    @tornado.gen.coroutine
    def getUniqueSL6(self, client, subSCMSList, gtmuList, regionList):
        sl6s = []
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUniqueNodes(db)
        for sub_scms in subSCMSList:
            for region in regionList:
                q1 = {'sub_scms' : sub_scms,
                      'region' : region}
                tempArray = yield collection.find(q1).distinct('sales_level_6')
                for element in tempArray:
                    if element != '' and element is not None:
                        sl6s.append(element)
        list.sort(sl6s)
        client.close()
        raise tornado.gen.Return(list(set(sl6s)))


    @tornado.gen.coroutine
    def getUniqueSalesAgents(self, client, subSCMSList, gtmuList, regionList, sl6List):
        sas = []
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUniqueNodes(db)
        for sl6 in sl6List:
            q1 = {'sales_level_6' : sl6}
            tempArray = yield collection.find(q1).distinct('sales_agents')
            for element in tempArray:
                if element != '' and element is not None:
                    sas.append(element)
        list.sort(sas)
        client.close()
        raise tornado.gen.Return(list(set(sas)))
    
