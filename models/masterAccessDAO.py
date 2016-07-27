'''
Created on Apr 29, 2015

@author: jeydurai
'''

import models.dataHandler
import tornado.gen

class MasterAccessDAO():

    @tornado.gen.coroutine 
    def getAccessDescription(self, client, accessCode):
        dho = models.dataHandler.DataHandler()
        db = dho.getDBTrueNorth(client)
        collection = db['master_access']
        doc = yield collection.find_one({"access_code": int(accessCode)}, {"_id":0})
        client.close()
        raise tornado.gen.Return(doc)
