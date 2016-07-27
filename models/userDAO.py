'''
Created on Apr 29, 2015

@author: jeydurai
'''
import models.dataHandler
import tornado.gen

class UserDAO():

    @tornado.gen.coroutine
    def getCollectionUsers(self, db):
        raise tornado.gen.Return(db['users'])
    
    @tornado.gen.coroutine
    def getCollectionSession(self, db):
        raise tornado.gen.Return(db['session'])

    @tornado.gen.coroutine
    def getCollectionUserStatus(self, db):
        raise tornado.gen.Return(db['user_status'])

    @tornado.gen.coroutine
    def validateUser(self, client, userName, password, isLogin=True):
        # print "UserName: " + str(userName)
        # print "Password: " + str(password)
        doesExists = yield self.userExists(client, userName)
        if not doesExists:
            print "Yes, it is that the user does not exist"
            raise tornado.gen.Return((False, 
                {
                 "statusComment":"User does not exist",
                 "statusCode" : 1,
                }
            ))
        else:
            if isLogin:
                credential = yield self.getUserCredentials(client, userName)
                dho = models.dataHandler.DataHandler()
                password = yield dho.hash_password(password)
                if credential["password"] == password:
                    if credential['approval_status']['code'] == 1:
                        raise tornado.gen.Return((
                            True, 
                            {"statusComment":"Validation Success",
                             "credentials":credential
                            }
                        ))
                    else:
                        raise tornado.gen.Return((False,
                            {
                                "statusComment":"Your account has not been approved!",
                                "credentials":credential,
                                "statusCode" : 2,
                            }
                        ))
                else:
                    raise tornado.gen.Return((False,
                        {
                            "statusComment":"Password does not match",
                            "credentials":credential,
                            "statusCode" : 3,
                        }
                    ))
            else:
                credential = yield self.getUserCredentials(client, userName)
                raise tornado.gen.Return((
                    True, 
                    {"statusComment":"Validation Success",
                     "credentials":credential
                    }
                ))
                
        client.close()
    
    @tornado.gen.coroutine
    def userExists(self, client, userName):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        obj = yield collection.find_one({"username" : userName})
        client.close()
        if obj:
            raise tornado.gen.Return(True)
        else:
            raise tornado.gen.Return(False) 


    @tornado.gen.coroutine
    def registerSession(self, client, doc):
        try:
            dho = models.dataHandler.DataHandler()
            db = yield dho.getDBTrueNorth(client)
            collection = yield self.getCollectionSession(db)
            future = collection.insert(doc)
            result = yield future
            client.close()
            resultTuple = ('success', 'Inserted Successfully!')
        except:
            resultTuple = ('error', 'Record was not inserted!')
        raise tornado.gen.Return(resultTuple)

    @tornado.gen.coroutine
    def deleteSession(self, client, key):
        try:
            dho = models.dataHandler.DataHandler()
            db = yield dho.getDBTrueNorth(client)
            collection = yield self.getCollectionSession(db)
            result = yield collection.remove({'username': key})
            client.close()
            resultTuple = (result, 'Deleted Successfully!')
        except:
            resultTuple = (0, 'Record was not deleted!')
        raise tornado.gen.Return(resultTuple)


    @tornado.gen.coroutine
    def deleteTempCollectionDocs(self, client):
        try:
            dho = models.dataHandler.DataHandler()
            db = yield dho.getDBTrueNorth(client)
            collection = yield self.getCollectionTemp(db)
            result = yield collection.remove({})
            client.close()
            resultTuple = (result, 'Deleted Successfully!')
        except:
            resultTuple = (0, 'Record was not deleted!')
        raise tornado.gen.Return(resultTuple)

    @tornado.gen.coroutine
    def getSession(self, client, key):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionSession(db)
        obj = yield collection.find_one({"username" : key})
        raise tornado.gen.Return(obj)

    @tornado.gen.coroutine
    def updateSession(self, client, key, value):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionSession(db)
        result = yield collection.update(
            {'username' : key},
            {
             '$set' : value, 
            }
        )
        client.close()
        raise tornado.gen.Return(('success', 'Updated Successfully!'))

    @tornado.gen.coroutine
    def getUserCredentials(self, client, userName):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        obj = yield collection.find_one({"username" : userName, "approval_status.code" : {"$ne" : -2} })
        raise tornado.gen.Return(obj)

    @tornado.gen.coroutine
    def insertDocumentsInUsers(self, client, doc, logDic):
        try:
            dho = models.dataHandler.DataHandler()
            db = yield dho.getDBTrueNorth(client)
            collection = yield self.getCollectionUsers(db)
            future = collection.insert(doc)
            result = yield future
            doc = {
                'updated_on' : logDic['updated_on'],
                'updated_by' : logDic['updated_by'],
                'activity' : logDic['activity'],
                'activity_description' : logDic['activity_description'],
                'reference_id' : logDic['reference_id']
            }
            collection = yield dho.getCollectionAdminLog(db)
            future = collection.insert(doc)
            result = yield future
            client.close()
            resultTuple = ('success', 'Inserted Successfully!')
        except:
            resultTuple = ('error', 'Record was not inserted!')
        raise tornado.gen.Return(resultTuple)


    @tornado.gen.coroutine
    def getUserStatusDescription(self, client, status_code):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUserStatus(db)
        doc = yield collection.find_one({'approval_status' : status_code}, {'_id' : 0})
        client.close()
        raise tornado.gen.Return(doc)

    @tornado.gen.coroutine
    def changePassword(self, client, change_doc, logDic):
        print "inside change password"
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        collection.update(
            {'username' : change_doc['username'],
             'approval_status.code' : 1
            },
            {
             '$set' : {
                'modified.edited_by' : change_doc['modified']['edited_by'],
                'modified.edited_on' : change_doc['modified']['edited_on'],
                'password' : change_doc['password'],
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
        future = collection.insert(doc)
        result = yield future
        client.close()
        raise tornado.gen.Return(('success', 'Updated Successfully!'))


    @tornado.gen.coroutine
    def changeUserName(self, client, change_doc, logDic):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        collection.update(
            {'username' : change_doc['username'],
             'approval_status.code' : 1
            },
            {
             '$set' : {
                'modified.edited_by' : change_doc['modified']['edited_by'],
                'modified.edited_on' : change_doc['modified']['edited_on'],
                'firstname' : change_doc['firstname'],
                'lastname' : change_doc['lastname'],
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
        future = collection.insert(doc)
        result = yield future
        client.close()
        raise tornado.gen.Return(('success', 'Updated Successfully!'))


    @tornado.gen.coroutine
    def rejectOrPurgeUser(self, client, userName, 
            approval_status, approval_description, logDic, whatTo):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        collection.update(
            {'username' : userName,
             'approval_status.code' : whatTo
            },
            {
             '$set' : {
                'approval_status.code' : approval_status,
                'approval_status.description' : approval_description,
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
        future = collection.insert(doc)
        result = yield future
        client.close()
        raise tornado.gen.Return(('success', 'Updated Successfully!'))
    
    @tornado.gen.coroutine
    def getSelfData(self, client, userName, access_code=0, init=False):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        tempColl = yield dho.getCollectionTemp(db)
        docs = collection.find(
            {
             "username" : userName,
             "approval_status.code" : {"$ne" : -2}
            }, 
            {"_id":0}
        )

        for each in (yield docs.to_list(length=100)):
            tempColl.insert(each)

        resultDocs = tempColl.find({}, {"_id":0})
        resultDoc = {}
        for each in (yield resultDocs.to_list(length=100)):
            resultDoc.update(each)

        raise tornado.gen.Return((tempColl, resultDoc)) #return temporary collection 'tempColl' so that the caller can close it once the data is copied into an array

    @tornado.gen.coroutine
    def getAllUsersData3(self, client, userName, access_code=0, init=False):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        tempColl = yield dho.getCollectionTemp(db)
        if access_code == 1:
            cursor = collection.find({}, {"_id":0})
            while (yield cursor.fetch_next):
                doc = cursor.next_object()
                result = yield tempColl.insert(doc)
        else:
            cursor = collection.find(
                {
                 "reportingto" : userName, 
                 "accessibility.access_level" : {"$ne" : 1}, 
                 "approval_status.code" : {"$ne" : -2}
                }, 
                {"_id":0}
            )
            docs = []
            while (yield cursor.fetch_next):
                doc = cursor.next_object()
                result = yield tempColl.insert(doc)
                docs.append(doc)

            for doc in docs:
                (dummy) = yield self.getAllUsersData3(client, doc['username'])

        raise tornado.gen.Return(tempColl) #return temporary collection 'tempColl' so that the caller can close it once the data is copied into an array


    @tornado.gen.coroutine
    def getAllUsersData2(self, client, userName, access_code=0, init=False):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        tempColl = yield dho.getCollectionTemp(db)
        if access_code == 1:
            cursor = collection.find({}, {"_id":0})
            while (yield cursor.fetch_next):
                doc = cursor.next_object()
                result = yield tempColl.insert(doc)
        else:
            cursor = collection.find(
                {
                 "reportingto" : userName, 
                 "accessibility.access_level" : {"$ne" : 1}, 
                 "approval_status.code" : {"$ne" : -2}
                }, 
                {"_id":0}
            )
            while (yield cursor.fetch_next):
                doc = cursor.next_object()
                result = yield tempColl.insert(doc)
                self.getAllUsersData2(client, doc['username'])

        raise tornado.gen.Return(tempColl) #return temporary collection 'tempColl' so that the caller can close it once the data is copied into an array

    @tornado.gen.coroutine
    def __fetchUserDoc(self, collection, reportingTo, accessCode=0):
        raise tornado.gen.Return(collection.find({"reportingto" : reportingTo,
            "accessibility.access_level" : accessCode}, {"_id":0}))


    @tornado.gen.coroutine
    def editUser(self, client, credentials, logDic):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        result = yield collection.update(
            {"username" : credentials['oldusername']}, 
                {"$set" : {
                    "username" : credentials['username'],
                    "firstname" : credentials['firstname'],
                    "lastname" : credentials['lastname'],
                    "email" : credentials['email'],
                    "reporting_to" : credentials['reporting_to'],
                    "access_code" : int(credentials['access_code']),
                    "access_description" : credentials['access_description'],
                    "location" : credentials['location']
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
    def approveUser(self, client, userName, sl6, sas, approval_status, approval_description, logDic):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        result = yield collection.update(
            {'username' : userName,
             'approval_status.code' : 0
            },
            {
             '$set' : {
                'accessibility.location.sales_level_6' : sl6,
                'accessibility.location.sales_agents' : sas,
                'approval_status.code' : approval_status,
                'approval_status.description' : approval_description,
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
        future = collection.insert(doc)
        result = yield future
        client.close()
        raise tornado.gen.Return(('success', 'Approved Successfully!'))

    @tornado.gen.coroutine
    def updateUser(self, client, userName, sl6, sas, logDic):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionUsers(db)
        result = yield collection.update(
            {'username' : userName},
            {
             '$set' : {
                'accessibility.location.sales_level_6' : sl6,
                'accessibility.location.sales_agents' : sas,
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
        future = collection.insert(doc)
        result = yield future
        client.close()
        raise tornado.gen.Return(('success', 'Updated Successfully!'))
