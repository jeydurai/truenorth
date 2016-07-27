# import pymongo
import motor
import controls.constants
import tornado.gen

class DataHandler():

    @tornado.gen.coroutine
    def getClient(self):
        return motor.MotorClient(controls.constants.Constants.MONGO_CONNECTION_HOST, controls.constants.Constants.MONGO_CONNECTION_PORT)
                
    @tornado.gen.coroutine
    def getDBTrueNorth(self, client):
        raise tornado.gen.Return(client.truenorth)
        
    @tornado.gen.coroutine
    def getCollectionAdminLog(self, db):
        raise tornado.gen.Return(db['admin_log'])

    @tornado.gen.coroutine
    def getCollectionTemp(self, db):
        raise tornado.gen.Return(db['temp'])

    @tornado.gen.coroutine
    def removeCollection(self, coll):
        result = yield coll.remove()

    @tornado.gen.coroutine
    def hash_password(self, password):
        import hashlib
        print "inside hash_password method"
        hash_pass = hashlib.sha1(password.encode('utf-8')).digest()
        hash_pass = hashlib.sha1(hash_pass).hexdigest()
        hash_pass = '*' + hash_pass.upper()
        raise tornado.gen.Return(hash_pass)
    
