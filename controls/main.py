import os.path
import json
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import models.dataHandler
import models.userDAO
import models.locationDAO
import models.accessDAO
import models.popDAO
import models.mainDashboardDAO
import controls.constants
import datetime
from time import strftime
import models.helper
import sys
import pymongo
import controls.controlHelper



from tornado.options import define, options
from controls.constants import Constants
from smtplib import SMTPException

define("port", default=8000, help="run on the given port", type=int)

    
class BaseHandler(tornado.web.RequestHandler, controls.constants.Constants, controls.controlHelper.MainPageHelper):

    def get_current_user(self):
        return self.get_secure_cookie("username")


class LoginErrorHandler01(BaseHandler):

    def get(self):
        self.render('index.html', 
            err="Username does not exist",
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
        )


class LoginErrorHandler02(BaseHandler):

    def get(self):
        self.render('index.html', 
            err="User Account has not been approved",
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
        )


class LoginErrorHandler03(BaseHandler):

    def get(self):
        self.render('index.html', 
            err="Password does not exist",
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
        )

class LoginErrorHandler04(BaseHandler):

    def get(self):
        self.render('index.html', 
            err="Something Wrong happened, Please try again!",
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
        )


class WelcomeHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('index.html', 
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
            credentials = {"signup" : 1}
        )




class ComradeHandler(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        mod2 = models.mainDashboardDAO.MainDashboardDAO()
        mod = models.userDAO.UserDAO()
        mod3 = models.accessDAO.AccessDAO()
        self.username = self.get_secure_cookie("username")
        self.password = None
        self.comrade = self.get_arguments('comrade')[0]
        credentials = yield mod.getSession(client, self.username)
        if credentials:
            if self.comrade is not None:
                (status, statusDict2) = yield mod.validateUser(client, userName=self.comrade, password=self.password, isLogin=False)
                (status, statusDict) = yield mod.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict2['credentials']['accessibility']['access_description']
            else:
                (status, statusDict) = yield mod.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, None)
            (max_year, max_quarter, max_month, max_week) = yield mod2.getMaxPeriods(client)
            self.set_secure_cookie("username", self.username)
            sessionDict = {
                'username' : self.username,
                'comrade' : self.comrade,
                'prod_ser' : None,
                'firstname' : statusDict['credentials']['firstname'],
                'lastname' : statusDict['credentials']['lastname'],
                'maxYear' : max_year,
                'maxQuarter' : max_quarter,
                'maxMonth' : max_month,
                'maxWeek' : max_week,
                'fiscal_year' : max_year,
                'fiscal_quarter' : None,
                'fiscal_month' : None,
                'fiscal_week' : None,
                'container_no' : 0,
                'round_count' : 0,
                'access_code' : statusDict['credentials']['accessibility']['access_level'],
                'desig_chart_display' : access_credentials['chart_display'],
                'period_chart_display' : period_access_credentials['chart_display'],
                'prodser_chart_display' : prodser_access_credentials['chart_display'],
                'growth_chart_display' : prodser_access_credentials['growth_display'],
            }
            (howMany, stats) = yield mod.deleteSession(client, self.username)
            (isOK, stats) = yield mod.registerSession(client, sessionDict)
            responseData = {
                'status' : 'success',
                'err' : '',
            }
            self.write(json.dumps(responseData))
            self.finish()
        else:
            if statusDict['statusCode'] == 1:
                self.redirect('/loginError01')
            elif statusDict['statusCode'] == 2:
                self.redirect('/loginError02')
            elif statusDict['statusCode'] == 3:
                self.redirect('/loginError03')



class SessionRefresher(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        mod2 = models.mainDashboardDAO.MainDashboardDAO()
        mod = models.userDAO.UserDAO()
        mod3 = models.accessDAO.AccessDAO()
        self.username = self.get_secure_cookie("username")
        self.password = None
        self.comrade = None
        credentials = yield mod.getSession(client, self.username)
        if credentials:
            if self.comrade is not None:
                (status, statusDict2) = yield mod.validateUser(client, userName=self.comrade, password=self.password, isLogin=False)
                (status, statusDict) = yield mod.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict2['credentials']['accessibility']['access_description']
            else:
                (status, statusDict) = yield mod.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, None)
            (max_year, max_quarter, max_month, max_week) = yield mod2.getMaxPeriods(client)
            self.set_secure_cookie("username", self.username)
            sessionDict = {
                'username' : self.username,
                'comrade' : self.comrade,
                'prod_ser' : None,
                'firstname' : statusDict['credentials']['firstname'],
                'lastname' : statusDict['credentials']['lastname'],
                'maxYear' : max_year,
                'maxQuarter' : max_quarter,
                'maxMonth' : max_month,
                'maxWeek' : max_week,
                'fiscal_year' : max_year,
                'fiscal_quarter' : None,
                'fiscal_month' : None,
                'fiscal_week' : None,
                'container_no' : 0,
                'round_count' : 0,
                'access_code' : statusDict['credentials']['accessibility']['access_level'],
                'desig_chart_display' : access_credentials['chart_display'],
                'period_chart_display' : period_access_credentials['chart_display'],
                'prodser_chart_display' : prodser_access_credentials['chart_display'],
                'growth_chart_display' : prodser_access_credentials['growth_display'],
            }
            (howMany, stats) = yield mod.deleteSession(client, self.username)
            (isOK, stats) = yield mod.registerSession(client, sessionDict)
            responseData = {
                'status' : 'success',
                'err' : '',
            }
            self.write(json.dumps(responseData))
            self.finish()
        else:
            if statusDict['statusCode'] == 1:
                self.redirect('/loginError01')
            elif statusDict['statusCode'] == 2:
                self.redirect('/loginError02')
            elif statusDict['statusCode'] == 3:
                self.redirect('/loginError03')


class MyTeamHandler(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        username = self.get_secure_cookie("username")
        mod = models.userDAO.UserDAO()
        credentials = yield mod.getSession(client, username)
        allUsersArray = []
        (result, result_text) = yield mod.deleteTempCollectionDocs(client)
        (tempColl) = yield mod.getAllUsersData3(client, username, credentials['access_code'], True)
        cursorAllUsers = tempColl.find({}, {"_id":0})
        # cursorAllUsers.sort([(sort_option, sort_direction)])
        while (yield cursorAllUsers.fetch_next):
            doc = cursorAllUsers.next_object()
            allUsersArray.append(doc)
        dummyResult = yield tempColl.remove({})
        userData = yield mod.getUserCredentials(client, username)
        if userData:
            responseData = {
                'status' : 'success',
                'allUsers' : allUsersArray,
            }
            dthandler = lambda obj: (
                obj.isoformat()
                if isinstance(obj, datetime.datetime)
                or isinstance(obj, datetime.datetime.date())
                else None
            )
            self.write(json.dumps(responseData, default=dthandler))
            self.finish()
        else:
            (howMany, stats) = yield mod.deleteSession(client, username)
            self.clear_all_cookies()
            print username + " has logged out abnormally!"
            self.redirect('/loginError04')


class ProfileHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        self.username = self.get_secure_cookie("username")
        self.password = None
        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.mainDashboardDAO.MainDashboardDAO()
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, self.username)
        mod3 = models.accessDAO.AccessDAO()
        if credentials:
            client = yield models.dataHandler.DataHandler().getClient()
            self.set_secure_cookie("username", self.username)
            (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
            access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, None)
            self.render('myProfile.html',
                successMsg=statusDict['statusComment'], 
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
                credentials = statusDict['credentials'],
                currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        else: 
            self.render("index.html", 
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
                credentials = {'signup' : 0}
            )

    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        username = self.get_secure_cookie("username")
        mod = models.userDAO.UserDAO()
        action = self.get_arguments('action')[0]
        if action == 'get_userdata':
            userData = yield mod.getUserCredentials(client, username)
            if userData:
                responseData = {
                    'status' : 'success',
                    'username' : userData['username'],
                    'firstname' : userData['firstname'],
                    'lastname' : userData['lastname'],
                    'password' : userData['password'],
                    'email' : userData['email'],
                    'reportingto' : userData['reportingto'],
                    'subSCMS' : userData['accessibility']['location']['sub_scms'],
                    'gtmu' : userData['accessibility']['location']['gtmu'],
                    'region' : userData['accessibility']['location']['region'],
                    'salesLevel6' : userData['accessibility']['location']['sales_level_6'],
                    'salesAgents' : userData['accessibility']['location']['sales_agents'],
                    'op_location' : userData['op_location'],
                    'designation' : userData['accessibility']['designation'],
                    'created_by' : userData['modified']['created_by'],
                    'created_on' : userData['modified']['created_on'],
                    'edited_by' : userData['modified']['edited_by'],
                    'edited_on' : userData['modified']['edited_on'],
                    'approval_status' : userData['approval_status']['code'],
                }
                dthandler = lambda obj: (
                    obj.isoformat()
                    if isinstance(obj, datetime.datetime)
                    or isinstance(obj, datetime.datetime.date())
                    else None
                )
                self.write(json.dumps(responseData, default=dthandler))
                self.finish()
            else:
                (howMany, stats) = yield mod.deleteSession(client, username)
                self.clear_all_cookies()
                print username + " has logged out abnormally!"
                self.redirect('/loginError04')
        elif action == 'save_username':
            editedon = datetime.datetime.now()
            change_username = self.get_arguments('username')[0]
            change_email = self.get_arguments('email')[0]
            change_firstname = self.get_arguments('firstname')[0]
            change_lastname = self.get_arguments('lastname')[0]
            log_dic = {
                'updated_on' : editedon,
                'updated_by' : username,
                'activity' : 'update',
                'activity_description' : 'username and Name change',
                'reference_id' : username
            }
            change_doc = {
                'password' : '',
                'username' : username,
                'firstname' : change_firstname,
                'lastname' : change_lastname,
                'modified' : {
                    'edited_by' : username,
                    'edited_on' : editedon
                }
            }

            mod = models.userDAO.UserDAO()
            (status_text, err) = yield mod.changeUserName(client, change_doc, log_dic)
            userData = yield mod.getUserCredentials(client, username)
            if userData:
                responseData = {
                    'status' : 'success',
                    'username' : userData['username'],
                    'firstname' : userData['firstname'],
                    'lastname' : userData['lastname'],
                    'password' : userData['password'],
                    'email' : userData['email'],
                    'reportingto' : userData['reportingto'],
                    'subSCMS' : userData['accessibility']['location']['sub_scms'],
                    'gtmu' : userData['accessibility']['location']['gtmu'],
                    'region' : userData['accessibility']['location']['region'],
                    'salesLevel6' : userData['accessibility']['location']['sales_level_6'],
                    'salesAgents' : userData['accessibility']['location']['sales_agents'],
                    'op_location' : userData['op_location'],
                    'designation' : userData['accessibility']['designation'],
                    'created_by' : userData['modified']['created_by'],
                    'created_on' : userData['modified']['created_on'],
                    'edited_by' : userData['modified']['edited_by'],
                    'edited_on' : userData['modified']['edited_on'],
                    'approval_status' : userData['approval_status']['code'],
                }
                dthandler = lambda obj: (
                    obj.isoformat()
                    if isinstance(obj, datetime.datetime)
                    or isinstance(obj, datetime.datetime.date())
                    else None
                )
                self.write(json.dumps(responseData, default=dthandler))
                self.finish()
            else:
                (howMany, stats) = yield mod.deleteSession(client, username)
                self.clear_all_cookies()
                print username + " has logged out abnormally!"
                self.redirect('/loginError04')
        elif action == 'save_password':
            editedon = datetime.datetime.now()
            old_password= self.get_arguments('oldpassword')[0]
            new_password= self.get_arguments('newpassword')[0]
            new_password = yield models.dataHandler.DataHandler().hash_password(new_password)
            (status, statusDict) = yield mod.validateUser(client, userName=username, password=old_password)
            if status:
                log_dic = {
                    'updated_on' : editedon,
                    'updated_by' : username,
                    'activity' : 'update',
                    'activity_description' : 'username and Name change',
                    'reference_id' : username
                }
                change_doc = {
                    'password' : new_password,
                    'username' : username,
                    'modified' : {
                        'edited_by' : username,
                        'edited_on' : editedon
                    }
                }

                mod = models.userDAO.UserDAO()
                (status_text, err) = yield mod.changePassword(client, change_doc, log_dic)
                userData = yield mod.getUserCredentials(client, username)
                if userData:
                    responseData = {
                        'status' : 'success',
                        'username' : userData['username'],
                        'firstname' : userData['firstname'],
                        'lastname' : userData['lastname'],
                        'password' : userData['password'],
                        'email' : userData['email'],
                        'reportingto' : userData['reportingto'],
                        'subSCMS' : userData['accessibility']['location']['sub_scms'],
                        'gtmu' : userData['accessibility']['location']['gtmu'],
                        'region' : userData['accessibility']['location']['region'],
                        'salesLevel6' : userData['accessibility']['location']['sales_level_6'],
                        'salesAgents' : userData['accessibility']['location']['sales_agents'],
                        'op_location' : userData['op_location'],
                        'designation' : userData['accessibility']['designation'],
                        'created_by' : userData['modified']['created_by'],
                        'created_on' : userData['modified']['created_on'],
                        'edited_by' : userData['modified']['edited_by'],
                        'edited_on' : userData['modified']['edited_on'],
                        'approval_status' : userData['approval_status']['code'],
                    }
                    dthandler = lambda obj: (
                        obj.isoformat()
                        if isinstance(obj, datetime.datetime)
                        or isinstance(obj, datetime.datetime.date())
                        else None
                    )
                    self.write(json.dumps(responseData, default=dthandler))
                    self.finish()
                else:
                    (howMany, stats) = yield mod.deleteSession(client, username)
                    self.clear_all_cookies()
                    print username + " has logged out abnormally!"
                    self.redirect('/loginError04')
            else:
                responseData = {
                    'status' : 'failed',
                }
                dthandler = lambda obj: (
                    obj.isoformat()
                    if isinstance(obj, datetime.datetime)
                    or isinstance(obj, datetime.datetime.date())
                    else None
                )
                self.write(json.dumps(responseData, default=dthandler))
                self.finish()
        else:
            (howMany, stats) = yield mod.deleteSession(client, username)
            self.clear_all_cookies()
            print username + " has logged out abnormally due to wrong action!"
            self.redirect('/loginError04')



class MainPageOverallHandler(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = self.get_secure_cookie("username")
        responseData = yield self.getMainPageData(username)
        self.write(json.dumps(responseData))
        self.finish()


class MainPageProductHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        self.username = self.get_secure_cookie("username")
        self.password = None
        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.mainDashboardDAO.MainDashboardDAO()
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, self.username)
        comrade = None
        if credentials['comrade'] is not None:
            comrade = credentials['comrade']

        mod3 = models.accessDAO.AccessDAO()
        statusDict2 = None
        if credentials:
            client = yield models.dataHandler.DataHandler().getClient()
            self.set_secure_cookie("username", self.username)
            if comrade is not None:
                (status, statusDict2) = yield mod2.validateUser(client, userName=comrade, password=self.password, isLogin=False)
                (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict2['credentials']['accessibility']['access_description']
            else:
                (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, 'product')
            (max_year, max_quarter, max_month, max_week) = yield mod.getMaxPeriods(client)
            if statusDict2:
                self.render('mainDashboard.html',
                    successMsg=statusDict['statusComment'], 
                    page_title=self.PAGE_TITLE,
                    heading=self.LOGO_HEADING,
                    credentials = statusDict['credentials'],
                    credentials2 = statusDict2['credentials'],
                    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            else:
                self.render('mainDashboard.html',
                    successMsg=statusDict['statusComment'], 
                    page_title=self.PAGE_TITLE,
                    heading=self.LOGO_HEADING,
                    credentials = statusDict['credentials'],
                    credentials2 = None,
                    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            sessionDict = {
                'username' : self.username,
                'comrade' : comrade,
                'prod_ser' : 'product',
                'firstname' : statusDict['credentials']['firstname'],
                'lastname' : statusDict['credentials']['lastname'],
                'maxYear' : max_year,
                'maxQuarter' : max_quarter,
                'maxMonth' : max_month,
                'maxWeek' : max_week,
                'fiscal_year' : max_year,
                'fiscal_quarter' : None,
                'fiscal_month' : None,
                'fiscal_week' : None,
                'container_no' : 0,
                'round_count' : 0,
                'access_code' : statusDict['credentials']['accessibility']['access_level'],
                'desig_chart_display' : access_credentials['chart_display'],
                'period_chart_display' : period_access_credentials['chart_display'],
                'prodser_chart_display' : prodser_access_credentials['chart_display'],
                'growth_chart_display' : prodser_access_credentials['growth_display'],
            }

            (howMany, stats) = yield mod2.deleteSession(client, self.username)
            (isOK, stats) = yield mod2.registerSession(client, sessionDict)
        else: 
            self.render("index.html", 
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
                credentials = {'signup' : 0}
            )

    @tornado.gen.coroutine
    def post(self):
        username = self.get_secure_cookie("username")
        responseData = yield self.getMainPageData(username)
        self.write(json.dumps(responseData))
        self.finish()


class MainPageServiceHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        self.username = self.get_secure_cookie("username")
        self.password = None
        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.mainDashboardDAO.MainDashboardDAO()
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, self.username)
        comrade = None
        if credentials['comrade'] is not None:
            comrade = credentials['comrade']

        mod3 = models.accessDAO.AccessDAO()
        statusDict2 = None
        if credentials:
            client = yield models.dataHandler.DataHandler().getClient()
            self.set_secure_cookie("username", self.username)
            if comrade is not None:
                (status, statusDict2) = yield mod2.validateUser(client, userName=comrade, password=self.password, isLogin=False)
                (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict2['credentials']['accessibility']['access_description']
            else:
                (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, 'service')
            (max_year, max_quarter, max_month, max_week) = yield mod.getMaxPeriods(client)
            if statusDict2:
                self.render('mainDashboard.html',
                    successMsg=statusDict['statusComment'], 
                    page_title=self.PAGE_TITLE,
                    heading=self.LOGO_HEADING,
                    credentials = statusDict['credentials'],
                    credentials2 = statusDict2['credentials'],
                    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            else:
                self.render('mainDashboard.html',
                    successMsg=statusDict['statusComment'], 
                    page_title=self.PAGE_TITLE,
                    heading=self.LOGO_HEADING,
                    credentials = statusDict['credentials'],
                    credentials2 = None,
                    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            sessionDict = {
                'username' : self.username,
                'comrade' : comrade,
                'prod_ser' : 'service',
                'firstname' : statusDict['credentials']['firstname'],
                'lastname' : statusDict['credentials']['lastname'],
                'maxYear' : max_year,
                'maxQuarter' : max_quarter,
                'maxMonth' : max_month,
                'maxWeek' : max_week,
                'fiscal_year' : max_year,
                'fiscal_quarter' : None,
                'fiscal_month' : None,
                'fiscal_week' : None,
                'container_no' : 0,
                'round_count' : 0,
                'access_code' : statusDict['credentials']['accessibility']['access_level'],
                'desig_chart_display' : access_credentials['chart_display'],
                'period_chart_display' : period_access_credentials['chart_display'],
                'prodser_chart_display' : prodser_access_credentials['chart_display'],
                'growth_chart_display' : prodser_access_credentials['growth_display'],
            }

            (howMany, stats) = yield mod2.deleteSession(client, self.username)
            (isOK, stats) = yield mod2.registerSession(client, sessionDict)
        else: 
            self.render("index.html", 
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
                credentials = {'signup' : 0}
            )

    @tornado.gen.coroutine
    def post(self):
        username = self.get_secure_cookie("username")
        responseData = yield self.getMainPageData(username)
        self.write(json.dumps(responseData))
        self.finish()


class LoginHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        print "Get executed"
        self.username = self.get_secure_cookie("username")
        self.password = None
        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.mainDashboardDAO.MainDashboardDAO()
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, self.username)
        self.comrade = None
        try:
            if credentials['comrade'] is not None:
                self.comrade = credentials['comrade']
        except:
            pass

        mod3 = models.accessDAO.AccessDAO()
        statusDict2 = None
        if credentials:
            print "has got credentials in session"
            client = yield models.dataHandler.DataHandler().getClient()
            self.set_secure_cookie("username", self.username)
            if self.comrade is not None:
                (status, statusDict2) = yield mod2.validateUser(client, userName=self.comrade, password=self.password, isLogin=False)
                (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict2['credentials']['accessibility']['access_description']
            else:
                (status, statusDict) = yield mod2.validateUser(client, userName=self.username, password=self.password, isLogin=False)
                access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, None)
            (max_year, max_quarter, max_month, max_week) = yield mod.getMaxPeriods(client)
            if statusDict2:
                self.render('mainDashboard.html',
                    successMsg=statusDict['statusComment'], 
                    page_title=self.PAGE_TITLE,
                    heading=self.LOGO_HEADING,
                    credentials = statusDict['credentials'],
                    credentials2 = statusDict2['credentials'],
                    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            else:
                self.render('mainDashboard.html',
                    successMsg=statusDict['statusComment'], 
                    page_title=self.PAGE_TITLE,
                    heading=self.LOGO_HEADING,
                    credentials = statusDict['credentials'],
                    credentials2 = None,
                    currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            sessionDict = {
                'username' : self.username,
                'comrade' : self.comrade,
                'prod_ser' : None,
                'firstname' : statusDict['credentials']['firstname'],
                'lastname' : statusDict['credentials']['lastname'],
                'maxYear' : max_year,
                'maxQuarter' : max_quarter,
                'maxMonth' : max_month,
                'maxWeek' : max_week,
                'fiscal_year' : max_year,
                'fiscal_quarter' : None,
                'fiscal_month' : None,
                'fiscal_week' : None,
                'container_no' : 0,
                'round_count' : 0,
                'access_code' : statusDict['credentials']['accessibility']['access_level'],
                'desig_chart_display' : access_credentials['chart_display'],
                'period_chart_display' : period_access_credentials['chart_display'],
                'prodser_chart_display' : prodser_access_credentials['chart_display'],
                'growth_chart_display' : prodser_access_credentials['growth_display'],
            }

            (howMany, stats) = yield mod2.deleteSession(client, self.username)
            (isOK, stats) = yield mod2.registerSession(client, sessionDict)
        else: 
            print "does not have credentials in session"
            self.render("index.html", 
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
                credentials = {'signup' : 0}
            )


    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        mod2 = models.mainDashboardDAO.MainDashboardDAO()
        mod = models.userDAO.UserDAO()
        mod3 = models.accessDAO.AccessDAO()
        self.username = self.get_argument("userName")
        self.password = self.get_argument("password")
        (status, statusDict) = yield mod.validateUser(client, userName=self.username, password=self.password)
        if status:
            access_description = statusDict['credentials']['accessibility']['access_description']
            access_credentials = yield mod3.getAccessCredentials(client, access_description)
            period_access_credentials = yield mod3.getPeriodAccessCredentials(client, 'year')
            prodser_access_credentials = yield mod3.getProdSerAccessCredentials(client, None)
            (max_year, max_quarter, max_month, max_week) = yield mod2.getMaxPeriods(client)
            self.set_secure_cookie("username", self.username)
            self.render('mainDashboard.html',
                successMsg=statusDict['statusComment'], 
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
                credentials = statusDict['credentials'],
                currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            sessionDict = {
                'username' : self.username,
                'comrade' : None,
                'prod_ser' : None,
                'firstname' : statusDict['credentials']['firstname'],
                'lastname' : statusDict['credentials']['lastname'],
                'maxYear' : max_year,
                'maxQuarter' : max_quarter,
                'maxMonth' : max_month,
                'maxWeek' : max_week,
                'fiscal_year' : max_year,
                'fiscal_quarter' : None,
                'fiscal_month' : None,
                'fiscal_week' : None,
                'container_no' : 0,
                'round_count' : 0,
                'access_code' : statusDict['credentials']['accessibility']['access_level'],
                'desig_chart_display' : access_credentials['chart_display'],
                'period_chart_display' : period_access_credentials['chart_display'],
                'prodser_chart_display' : prodser_access_credentials['chart_display'],
                'growth_chart_display' : prodser_access_credentials['growth_display'],
            }
            (howMany, stats) = yield mod.deleteSession(client, self.username)
            (isOK, stats) = yield mod.registerSession(client, sessionDict)
        else:
            if statusDict['statusCode'] == 1:
                self.redirect('/loginError01')
            elif statusDict['statusCode'] == 2:
                self.redirect('/loginError02')
            elif statusDict['statusCode'] == 3:
                self.redirect('/loginError03')


class SignupHandler(BaseHandler):

    def get(self):
        self.render("signUp.html",
            err=None,
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
            message=''
        )

    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        createOn = datetime.datetime.now()
        username = self.get_arguments('userName')[0]
        firstname = self.get_arguments('firstName')[0]
        lastname = self.get_arguments('lastName')[0]
        password = self.get_arguments('password')[0]
        emailid = self.get_arguments('emailid')[0]
        reporting_to = self.get_arguments('reportingTo')[0]
        op_location = self.get_arguments('op_location')[0]
        designation = self.get_arguments('designation')[0]
        subSCMS = self.get_arguments('sub_scms')
        gtmu = self.get_arguments('gtmu')
        region = self.get_arguments('region')
        sl6 = self.get_arguments('sl6')
        sas = self.get_arguments('sas')
        approval_status = 0
        """ Fetch Access Description """
        mod = models.userDAO.UserDAO()
        user_status = yield mod.getUserStatusDescription(client, approval_status)
        approval_description = user_status['status_description']
        mod2 = models.accessDAO.AccessDAO()
        access_credentials = yield mod2.getAccessCredentials(client, designation)
        access_code = access_credentials['access_code']

        helper = models.helper.Helper()
        gtmu = helper.stringToList(gtmu)
        subSCMS = helper.stringToList(subSCMS)
        region = helper.stringToList(region)
        sl6 = helper.stringToList(sl6)
        sas = helper.stringToList(sas)
        sas = helper.specialCharToComma(sas)
        """ Password Encription """
        password = yield models.dataHandler.DataHandler().hash_password(password)
        
        log_dic = {
            'updated_on' : createOn,
            'updated_by' : username,
            'activity' : 'Sign up',
            'activity_description' : 'New sign up request',
            'reference_id' : username
        }
        signup_doc = {
            'username' : username,
            'firstname' : firstname,
            'lastname' : lastname,
            'password' : password,
            'email' : emailid,
            'reportingto' : reporting_to,
            'op_location' : op_location,
            'accessibility' : {
                'designation' : designation,
                "access_level" : access_code,
                "access_description" : designation,
                'location' : {
                    'sub_scms' : subSCMS,
                    'gtmu' : gtmu,
                    'region' : region,
                    'sales_level_6' : sl6,
                    'sales_agents' : sas
                },
            },
            'approval_status' : {
                'code' : approval_status,
                'description' :approval_description
            },
            'modified' : {
                'created_by' : username,
                'created_on' : createOn,
                'edited_by' : username,
                'edited_on' : createOn
            }
        }

        mod = models.userDAO.UserDAO()
        (status, err) = yield mod.insertDocumentsInUsers(client, signup_doc, log_dic)

        message = 'Congratulations ' + firstname + ' ' + lastname + '!, You have, successfully, sent a sign up request, Please do follow up with your reporting manager'
        responseData = {
            'status' : status,
            'err' : err,
            'message' : message
        }
        self.write(json.dumps(responseData))
        self.finish()
        
        
    
class UserValidator(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        action = self.get_arguments('action')[0]
        if action == 'username_check':
            username = self.get_arguments('username')[0]
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.locationDAO.LocationDAO()
            locations = yield mod.getLocations(client)
            mod = models.accessDAO.AccessDAO()
            desigArray = yield mod.getDesignations(client)
            mod = models.userDAO.UserDAO()
            userCredentials = yield mod.getUserCredentials(client, username)
            locArray = []
            for loc in locations:
                locArray.append(loc['location'])
            if userCredentials:
                status = 'error'
                err = '<span>You have already sent a request, please check with your reporting manager!</span>'
                responseData = {
                'status' : status,
                'err' : err,
                'locations' : locArray,
                'designations' : desigArray,
            }
            else:
                status = 'success'
                err=''
                responseData = {
                'status' : status,
                'err' : err,
                'locations' : locArray,
                'designations' : desigArray,
            }
        elif action == 'reporting_check':
            username = self.get_arguments('username')[0]
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.userDAO.UserDAO()
            userCredentials = yield mod.getUserCredentials(client, username)
            if userCredentials:
                status = 'success'
                err=''
                responseData = {
                'status' : status,
                'err' : err,
            }
            else:
                status = 'error'
                err = '<span>Reporting manager has NOT been created yet!</span>'
                responseData = {
                'status' : status,
                'err' : err,
            }
        elif action == 'subscms_fetch':
            helper = models.helper.Helper()
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.popDAO.PopDAO()
            subSCMSList = yield mod.getUniqueSubSCMS(client)
            responseData = {
                'status' : 'success',
                'err' : '',
                'sub_scms' : subSCMSList
            }
        elif action == 'gtmu_fetch':
            helper = models.helper.Helper()
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.popDAO.PopDAO()
            gtmuList = yield mod.getUniqueGTMu(client)
            responseData = {
                'status' : 'success',
                'err' : '',
                'gtmus' : gtmuList
            }
        elif action == 'region_fetch':
            subSCMS = self.get_arguments('sub_scms')
            gtmu = self.get_arguments('gtmu')
            
            helper = models.helper.Helper()
            gtmu = helper.stringToList(gtmu)
            subSCMS = helper.stringToList(subSCMS)
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.popDAO.PopDAO()
            regions = yield mod.getUniqueRegions(client, subSCMS, gtmu)
            responseData = {
                'status' : "success",
                'err' : "",
                'regions' : regions
            }
        elif action == 'sl6_fetch':
            subSCMS = self.get_arguments('sub_scms')
            gtmu = self.get_arguments('gtmu')
            region = self.get_arguments('region')
            
            helper = models.helper.Helper()
            gtmu = helper.stringToList(gtmu)
            subSCMS = helper.stringToList(subSCMS)
            region = helper.stringToList(region)
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.popDAO.PopDAO()
            sl6s = yield mod.getUniqueSL6(client, subSCMS, gtmu, region)
            responseData = {
                'status' : "success",
                'err' : "",
                'sl6s' : sl6s
            }
        elif action == 'salesagents_fetch':
            subSCMS = self.get_arguments('sub_scms')
            gtmu = self.get_arguments('gtmu')
            region = self.get_arguments('region')
            sl6 = self.get_arguments('sl6')
            
            helper = models.helper.Helper()
            gtmu = helper.stringToList(gtmu)
            subSCMS = helper.stringToList(subSCMS)
            region = helper.stringToList(region)
            sl6 = helper.stringToList(sl6)
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.popDAO.PopDAO()
            sales_agents = yield mod.getUniqueSalesAgents(client, subSCMS, gtmu, region, sl6)
            responseData = {
                'status' : "success",
                'err' : "",
                'sales_agents' : sales_agents
            }
        self.write(json.dumps(responseData))
        self.finish()


class LocationHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        """ Data Handle """
        client = yield models.dataHandler.DataHandler().getClient()

        """ Store Arguments in Variables """
        action = self.get_arguments('action')[0]
        location = self.get_arguments('locationString')[0]
        editedOn = datetime.datetime.now()

        """ Obtain secured cookie and set the same """
        cookie = self.get_secure_cookie("username")
        self.set_secure_cookie("username", cookie)
         
        """ Acquire session details """
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, cookie)


        """ Check for the correctness of cookies """
        if credentials['username']:
            if action == 'add':
                country = self.get_arguments('country')[0]
                gtmu = self.get_arguments('gtmu')[0]
                region = self.get_arguments('region')[0]
                """ Prepare Location Document """
                logDic = {
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Operation Location',
                    'activity_description' : 'New Location added',
                    'reference_id' : location.upper()
                }
                loc_doc = {
                    'country' : country.upper(),
                    'gtmu' : gtmu.upper(),
                    'location' : location.upper(),
                    'region' : region.upper(),
                    'purged' : 0,
                    'modified' : {
                        'created_by' : credentials['username'],
                        'created_on' : editedOn,
                        'edited_by' : credentials['username'],
                        'edited_on' : editedOn
                    }
                }
                mod = models.locationDAO.LocationDAO()
                doesUserExist = yield mod.locationExists(client, location)
                if not doesUserExist:
                    mod = models.locationDAO.LocationDAO()
                    (status, err) = yield mod.insertDocumentsInLocations(client, loc_doc, logDic)
                else:
                    err = location + " 's data already exists!"
                    status = 'error'
                responseData = {
                    'text' : status,
                    'err' : err
                }
            elif action == 'edit':
                oldlocation = self.get_arguments('oldlocation')[0]
                country = self.get_arguments('country')[0]
                gtmu = self.get_arguments('gtmu')[0]
                region = self.get_arguments('region')[0]
                """ Prepare User Document """
                logDic = {
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Operation Location',
                    'activity_description' : oldlocation + ' changed to ' + location.upper(),
                    'reference_id' : location.upper()
                }
                loc_doc = {
                    'oldlocation' : oldlocation,
                    'location' : location.upper(),
                    'country' : country.upper(),
                    'gtmu' : gtmu.upper(),
                    'region' : region.upper(),
                    'purged' : 0,
                    'modified' : {
                        'created_by' : credentials['username'],
                        'created_on' : editedOn,
                        'edited_by' : credentials['username'],
                        'edited_on' : editedOn
                    }
                }
                mod = models.locationDAO.LocationDAO()
                (status, err) = yield mod.editLocation(client, loc_doc, logDic)
                responseData = {
                    'text' : status,
                    'err' : err
                }
            elif action == 'remove':
                client = yield models.dataHandler.DataHandler().getClient()
                logDic = {
                    'edited_on' : editedOn,
                    'edited_by' : credentials['username'],
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Operation Location',
                    'activity_description' : location + ' purged',
                    'reference_id' : location
                }
                mod = models.locationDAO.LocationDAO()
                (status, err) = yield mod.removeLocation(client, location, logDic)
                responseData = {
                    'text' : status,
                    'err' : err
                }
            self.write(json.dumps(responseData))
            self.finish()
                
        else: # Or else log out and redirect to log in page
            print "Cookie and Session Credentials does not match!"
            self.set_status(400)
            raise tornado.gen.Return("") 
        

class UserHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        action = self.get_arguments('action')[0]
        client = yield models.dataHandler.DataHandler().getClient()
        print action
        username = self.get_arguments('userName')[0]
        cookie = self.get_secure_cookie("username")
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, cookie)
        createOn = datetime.datetime.now()
        editedBy = credentials['username']
        editedOn = datetime.datetime.now()
        self.set_secure_cookie("username", cookie)
        if credentials['username']:
            if action == 'remove':
                approval_status = -2
                """ Fetch Access Description """
                mod = models.userDAO.UserDAO()
                user_status = yield mod.getUserStatusDescription(
                    client, approval_status
                )
                approval_description = user_status['status_description']

                logDic = {
                    'edited_on' : editedOn,
                    'edited_by' : editedBy,
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Users',
                    'activity_description' : username + ' purged',
                    'reference_id' : username
                }
                (status, err) = yield mod.rejectOrPurgeUser(
                    client, username, approval_status, approval_description, logDic, 1
                )
                responseData = {
                    'status' : status,
                    'statusMessage' : err
                }
                self.write(json.dumps(responseData))
                self.finish()
            elif action == 'add':
                client = yield models.dataHandler.DataHandler().getClient()
                username = self.get_arguments('userName')[0]
                createdBy = credentials['username']
                firstname = self.get_arguments('firstName')[0]
                lastname = self.get_arguments('lastName')[0]
                password = self.get_arguments('password')[0]
                emailid = self.get_arguments('emailid')[0]
                reporting_to = self.get_arguments('reportingTo')[0]
                op_location = self.get_arguments('op_location')[0]
                designation = self.get_arguments('designation')[0]
                subSCMS = self.get_arguments('sub_scms')
                gtmu = self.get_arguments('gtmu')
                region = self.get_arguments('region')
                sl6 = self.get_arguments('sl6')
                sas = self.get_arguments('sas')
                approval_status = 0
                """ Fetch Access Description """
                mod = models.userDAO.UserDAO()
                user_status = yield mod.getUserStatusDescription(client, approval_status)
                approval_description = user_status['status_description']
        
                helper = models.helper.Helper()
                gtmu = helper.stringToList(gtmu)
                subSCMS = helper.stringToList(subSCMS)
                region = helper.stringToList(region)
                sl6 = helper.stringToList(sl6)
                sas = helper.stringToList(sas)
                sas = helper.specialCharToComma(sas)
                """ Password Encription """
                password = yield models.dataHandler.DataHandler().hash_password(password)
                
                log_dic = {
                    'edited_on' : editedOn,
                    'edited_by' : credentials['username'],
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Users',
                    'activity_description' : 'New sign up request',
                    'reference_id' : username
                }
                signup_doc = {
                    'username' : username,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'password' : password,
                    'email' : emailid,
                    'reportingto' : reporting_to,
                    'op_location' : op_location,
                    'accessibility' : {
                        'designation' : designation,
                        "access_level" : 0,
                        "access_description" : "USER",
                        'location' : {
                            'sub_scms' : subSCMS,
                            'gtmu' : gtmu,
                            'region' : region,
                            'sales_level_6' : sl6,
                            'sales_agents' : sas
                        },
                    },
                    'approval_status' : {
                        'code' : approval_status,
                        'description' :approval_description
                    },
                    'modified' : {
                        'created_by' : createdBy,
                        'created_on' : createOn,
                        'edited_by' : createdBy,
                        'edited_on' : createOn
                    }
                }
        
                mod = models.userDAO.UserDAO()
                (status, err) = yield mod.insertDocumentsInUsers(client, signup_doc, log_dic)
        
                message = 'Congratulations ' + firstname + ' ' + lastname + '!, You have, successfully, sent a sign up request, Please do follow up with your reporting manager'
                responseData = {
                    'status' : status,
                    'err' : err,
                    'message' : message
                }
                self.write(json.dumps(responseData))
                self.finish()

            elif action == 'approve':
                client = yield models.dataHandler.DataHandler().getClient()
                sl6 = self.get_arguments('sl6')
                sas = self.get_arguments('sas')
                editedOn = datetime.datetime.now()
                approval_status = 2 
                """ Fetch Access Description """
                mod = models.userDAO.UserDAO()
                user_status = yield mod.getUserStatusDescription(client, approval_status)
                approval_description = user_status['status_description']
        
                helper = models.helper.Helper()
                sl6 = helper.stringToList(sl6)
                sas = helper.stringToList(sas)
                sas = helper.specialCharToComma(sas)
                
                logDic = {
                    'edited_on' : editedOn,
                    'edited_by' : credentials['username'],
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Users',
                    'activity_description' : username + ' request approved',
                    'reference_id' : username
                }
                mod = models.userDAO.UserDAO()
                (status, err) = yield mod.approveUser(
                    client, username, sl6, sas, approval_status, approval_description,
                    logDic
                )
                responseData = {
                    'status' : status,
                    'statusMessage' : err
                }
                self.write(json.dumps(responseData))
                self.finish()
            elif action == 'update':
                print "Now updating"
                client = yield models.dataHandler.DataHandler().getClient()
                # First Remove the existing Data
                approval_status = -2
                """ Fetch Access Description """
                mod = models.userDAO.UserDAO()
                user_status = yield mod.getUserStatusDescription(
                    client, approval_status
                )
                approval_description = user_status['status_description']

                logDic = {
                    'edited_on' : editedOn,
                    'edited_by' : editedBy,
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Users-Redefine',
                    'activity_description' : username + ' purged',
                    'reference_id' : username
                }
                (status, err) = yield mod.rejectOrPurgeUser(
                    client, username, approval_status, approval_description, logDic, 1
                )
                # Now add the new Data
                createOn = datetime.datetime.now()
                username = self.get_arguments('userName')[0]
                firstname = self.get_arguments('firstName')[0]
                lastname = self.get_arguments('lastName')[0]
                password = self.get_arguments('password')[0]
                emailid = self.get_arguments('emailid')[0]
                reporting_to = self.get_arguments('reportingTo')[0]
                op_location = self.get_arguments('op_location')[0]
                designation = self.get_arguments('designation')[0]
                subSCMS = self.get_arguments('sub_scms')
                gtmu = self.get_arguments('gtmu')
                region = self.get_arguments('region')
                sl6 = self.get_arguments('sl6')
                sas = self.get_arguments('sas')
                approval_status = 0
                """ Fetch Access Description """
                mod = models.userDAO.UserDAO()
                user_status = yield mod.getUserStatusDescription(client, approval_status)
                approval_description = user_status['status_description']
        
                helper = models.helper.Helper()
                gtmu = helper.stringToList(gtmu)
                subSCMS = helper.stringToList(subSCMS)
                region = helper.stringToList(region)
                sl6 = helper.stringToList(sl6)
                sas = helper.stringToList(sas)
                sas = helper.specialCharToComma(sas)
                """ Password Encription """
                password = yield models.dataHandler.DataHandler().hash_password(password)
                
                log_dic = {
                    'updated_on' : createOn,
                    'updated_by' : username,
                    'activity' : 'Update',
                    'activity_description' : 'Update request',
                    'reference_id' : username
                }
                edit_doc = {
                    'username' : username,
                    'firstname' : firstname,
                    'lastname' : lastname,
                    'password' : password,
                    'email' : emailid,
                    'reportingto' : reporting_to,
                    'op_location' : op_location,
                    'accessibility' : {
                        'designation' : designation,
                        "access_level" : 0,
                        "access_description" : "USER",
                        'location' : {
                            'sub_scms' : subSCMS,
                            'gtmu' : gtmu,
                            'region' : region,
                            'sales_level_6' : sl6,
                            'sales_agents' : sas
                        },
                    },
                    'approval_status' : {
                        'code' : approval_status,
                        'description' :approval_description
                    },
                    'modified' : {
                        'created_by' : username,
                        'created_on' : createOn,
                        'edited_by' : username,
                        'edited_on' : createOn
                    }
                }
        
                mod = models.userDAO.UserDAO()
                (status, err) = yield mod.insertDocumentsInUsers(client, edit_doc, log_dic)
        
                message = 'Congratulations ' + firstname + ' ' + lastname + '!, You have, successfully, sent an update request, Please do follow up with your reporting manager'
                responseData = {
                    'status' : status,
                    'err' : err,
                    'message' : message
                }
                self.write(json.dumps(responseData))
                self.finish()
            elif action == 'reject':
                client = yield models.dataHandler.DataHandler().getClient()
                editedOn = datetime.datetime.now()
                approval_status = -1
                """ Fetch Access Description """
                user_status = yield models.dataHandler.DataHandler().getUserStatusDescription(client, approval_status)
                approval_description = user_status['status_description']
        
                logDic = {
                    'edited_on' : editedOn,
                    'edited_by' : credentials['username'],
                    'updated_on' : editedOn,
                    'updated_by' : credentials['username'],
                    'activity' : 'Users',
                    'activity_description' : username + ' request rejected',
                    'reference_id' : username
                }
                mod = models.userDAO.UserDAO()
                (status, err) = yield mod.rejectOrPurgeUser(
                    client, username, approval_status, approval_description,
                    logDic, 0
                )
                responseData = {
                    'status' : status,
                    'statusMessage' : err
                }
                self.write(json.dumps(responseData))
                self.finish()
            else:
                self.set_status(400)
        else:
            print "Cookie and Session Credentials does not match!"
            self.set_status(400)


class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        helpers = models.helper.Helper()
        cookie = self.get_secure_cookie("username")
        sort_option = "modified.edited_on"
        sort_direction = pymongo.DESCENDING;
        try:
            sort_option = self.get_argument('sort-option')
            sort_direction = pymongo.ASCENDING;
        except:
            print "Not Sort Handler: ", sys.exc_info()[0]
        
        client = yield models.dataHandler.DataHandler().getClient()
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, cookie)
        self.set_secure_cookie("username", cookie)
        sort_option_fields = ["op_location", "firstname", "lastname", "username", "reportingto", "modified.edited_on", "modified.created_on", "modified.edited_by", "modified.created_by"]
        list.sort(sort_option_fields)
        if credentials['username']:
            allUsersArray = []
            client = yield models.dataHandler.DataHandler().getClient()
            mod = models.userDAO.UserDAO()
            (result, result_text) = yield mod.deleteTempCollectionDocs(client)
            (tempColl) = yield mod.getAllUsersData3(client, credentials['username'], credentials['access_code'], True)
            cursorAllUsers = tempColl.find({}, {"_id":0})
            cursorAllUsers.sort([(sort_option, sort_direction)])
            while (yield cursorAllUsers.fetch_next):
                doc = cursorAllUsers.next_object()
                allUsersArray.append(doc)
            dummyResult = yield tempColl.remove({})
            if credentials['access_code'] != 1:
                (tempColl, selfData) = yield mod.getSelfData(client, credentials['username'], credentials['access_code'], True)
                allUsersArray.append(selfData)
                dummyResult = yield tempColl.remove({})
            mod = models.locationDAO.LocationDAO()
            allLocations = yield mod.getAllLocationsData(client, credentials['access_code'])
        
            dummyResult = yield tempColl.remove({})
            client.close()
            self.render("admin.html", 
                credentials = credentials,
                allUsers = allUsersArray,
                allLocations = allLocations,
                sort_options = sort_option_fields,
                err="",
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
            )
        
        elif str(cookie) != credentials['username']:
            errMsg = self.ERROR_SESSION_INVALID
            self.render("index.html", 
                session = credentials,
                err=errMsg,
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
            )
        else:
            errMsg = self.ERROR_ONLY_ADMIN
            self.render("index.html", 
                session = credentials,
                err=errMsg,
                page_title=self.PAGE_TITLE,
                heading=self.LOGO_HEADING,
            )

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        action = self.get_arguments('action')[0]
        username = self.get_arguments('username')[0]
        cookie = self.get_secure_cookie("username")
        client = yield models.dataHandler.DataHandler().getClient()
        mod2 = models.userDAO.UserDAO()
        credentials = yield mod2.getSession(client, cookie)
        self.set_secure_cookie("username", cookie)
        selfName = credentials['username']
        if credentials['username']:
            if action == 'display_container':
                location = self.get_arguments('locationString')[0]
                responseData = {
                    'text' : '',
                    'err' : ''
                }
                self.write(json.dumps(responseData))
                self.finish()
            elif action == 'fetch_location':
                location = self.get_arguments('locationString')[0]
                client = yield models.dataHandler.DataHandler().getClient()
                mod = models.locationDAO.LocationDAO()
                locationData = yield mod.getLocationCredentials(client, location)
                responseData = {
                    'locationString' : locationData['location'],
                    'country' : locationData['country'],
                    'gtmu' : locationData['country'],
                    'region' : locationData['region'],
                    'created_by' : locationData['modified']['created_by'],
                    'created_on' : locationData['modified']['created_on'],
                    'edited_by' : locationData['modified']['edited_by'],
                    'edited_on' : locationData['modified']['edited_on'],
                    'status' : 'success'
                }
                dthandler = lambda obj: (
                    obj.isoformat()
                    if isinstance(obj, datetime.datetime)
                    or isinstance(obj, datetime.datetime.date())
                    else None
                )
                self.write(json.dumps(responseData, default=dthandler))
                self.finish()
            elif action == 'fetch_user':
                allLocArray = []
                allSubSCMSArray = []
                client = yield models.dataHandler.DataHandler().getClient()
                mod = models.userDAO.UserDAO()
                userData = yield mod.getUserCredentials(client, username)
                mod = models.locationDAO.LocationDAO()
                locations = yield mod.getLocations(client)
                mod = models.popDAO.PopDAO()
                subSCMS = yield mod.getUniqueSubSCMS(client)

                for loc in locations:
                    allLocArray.append(loc['location'])

                allSubSCMSArray.extend(subSCMS)
                if selfName == userData['username']:
                    authenti_code = 1
                else:
                    authenti_code = 0
                responseData = {
                    'username' : userData['username'],
                    'firstname' : userData['firstname'],
                    'lastname' : userData['lastname'],
                    'password' : userData['password'],
                    'email' : userData['email'],
                    'reportingto' : userData['reportingto'],
                    'subSCMS' : userData['accessibility']['location']['sub_scms'],
                    'gtmu' : userData['accessibility']['location']['gtmu'],
                    'region' : userData['accessibility']['location']['region'],
                    'salesLevel6' : userData['accessibility']['location']['sales_level_6'],
                    'salesAgents' : userData['accessibility']['location']['sales_agents'],
                    'op_location' : userData['op_location'],
                    'designation' : userData['accessibility']['designation'],
                    'created_by' : userData['modified']['created_by'],
                    'created_on' : userData['modified']['created_on'],
                    'edited_by' : userData['modified']['edited_by'],
                    'edited_on' : userData['modified']['edited_on'],
                    'allLocations' : allLocArray,
                    'allSubSCMS' : allSubSCMSArray,
                    'approval_status' : userData['approval_status']['code'],
                    'authenti_code' : authenti_code
                }
                dthandler = lambda obj: (
                    obj.isoformat()
                    if isinstance(obj, datetime.datetime)
                    or isinstance(obj, datetime.datetime.date())
                    else None
                )
                self.write(json.dumps(responseData, default=dthandler))
                self.finish()
            else:
                self.set_status(400)
        else:
            print "Cookie and Session Credentials does not match!"
            self.set_status(400)

# ==================================================
# ==================================================
class PasswordHandler(BaseHandler):

    def get(self):
        self.render("pwdPage.html",
            err=None,
            page_title=self.PAGE_TITLE,
            heading=self.LOGO_HEADING,
            message=''
        )

    @tornado.gen.coroutine
    def post(self):
        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.userDAO.UserDAO()
        editedon = datetime.datetime.now()
        username = self.get_arguments('userName')[0]
        old_password = self.get_arguments('old_password')[0]
        new_password = self.get_arguments('new_password')[0]
        confirm_password = self.get_arguments('confirm_password')[0]
        message = ''

        if new_password == confirm_password:
            (status, statusDict) = yield mod.validateUser(client, userName=username, password=old_password)
            if status:
                print "Old password matches"
                """ Password Encription """
                new_password = yield models.dataHandler.DataHandler().hash_password(new_password)
                
                log_dic = {
                    'updated_on' : editedon,
                    'updated_by' : username,
                    'activity' : 'update',
                    'activity_description' : 'password change',
                    'reference_id' : username
                }
                change_doc = {
                    'password' : new_password,
                    'username' : username,
                    'modified' : {
                        'edited_by' : username,
                        'edited_on' : editedon
                    }
                }

                mod = models.userDAO.UserDAO()
                (status_text, err) = yield mod.changePassword(client, change_doc, log_dic)

                message = 'Password has been changed successfully!'
                print message
            else:
                status_text = "success"
                err = statusDict['statusComment']
                message = err
                print err
        else:
            status_text = "success"
            err = "New and Confirm password are not matching"
            message = err

        responseData = {
            'status' : status_text,
            'err' : err,
            'message' : message
        }
        self.write(json.dumps(responseData))
        self.finish()


# ==================================================
class UserModule(tornado.web.UIModule):

    def render(self, user):
        return self.render_string('modules/userList.html', user=user)

    def css_files(self):
        return "/static/css/admin.css"
    

class LocationModule(tornado.web.UIModule):

    def render(self, location):
        return self.render_string('modules/locationList.html', location=location)

    def css_files(self):
        return "/static/css/admin.css"

class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        username = self.get_secure_cookie("username")
        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.userDAO.UserDAO()
        (howMany, stats) = yield mod.deleteSession(client, username)
        self.clear_all_cookies()
        print username + " has logged out!"
        self.redirect('/')

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [(r'/', WelcomeHandler), 
                    (r'/main', LoginHandler),
                    (r'/comrade', ComradeHandler),
                    (r'/refresh-session', SessionRefresher),
                    (r'/product', MainPageProductHandler),
                    (r'/service', MainPageServiceHandler),
                    (r'/myprofile', ProfileHandler),
                    (r'/myteam', MyTeamHandler),
                    (r'/loginError01', LoginErrorHandler01),
                    (r'/loginError02', LoginErrorHandler02),
                    (r'/loginError03', LoginErrorHandler03),
                    (r'/loginError04', LoginErrorHandler04),
                    (r'/home', MainPageOverallHandler),
                    (r'/home-product', MainPageProductHandler),
                    (r'/home-service', MainPageServiceHandler),
                    (r'/login', LoginHandler),
                    (r'/logout', LogoutHandler),
                    (r'/signup', SignupHandler),
                    (r'/validation/user', UserValidator),
                    (r'/admin', AdminHandler),
                    (r'/admin/user', UserHandler),
                    (r'/admin/location', LocationHandler),
                    (r'/admin/profile', PasswordHandler),
        ]
        settings = {
            'template_path' : '../views/templates',
            'static_path' : '../views/static',
            'cookie_secret' : "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            'xsrf_cookies' : False,
            'login_url' : "/login",
            'ui_modules' : {"User" : UserModule,
                            "Location" : LocationModule},
            'debug' : False
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
