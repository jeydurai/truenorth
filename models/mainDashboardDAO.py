'''
Created on Aug 21, 2015

@author: jeydurai
'''

import models.dataHandler
from bson.son import SON
from models.constants import Constants
from models.dataStructures import MongoDataStructure
from models.helper import Helper
from pydoc import Doc
import tornado.gen


class MainDashboardDAO():

    MILLION = 1000000
    
    def __init__(self):
        self.jsonObj = models.dataStructures.MongoDataStructure()
        self.helper = Helper()
        
    @tornado.gen.coroutine
    def getCollectionBookingData(self, db):
        raise tornado.gen.Return(db['booking_dump2'])

    @tornado.gen.coroutine
    def getCollectionGeneralDashboard(self, db):
        raise tornado.gen.Return(db['general_dashboard'])

    @tornado.gen.coroutine
    def getCollectionGeneralDashboardProdSer(self, db):
        raise tornado.gen.Return(db['general_dashboard_prodser'])

    @tornado.gen.coroutine
    def getCollectionGeneralDashboardYoY(self, db):
        raise tornado.gen.Return(db['general_dashboard_yoy'])

    @tornado.gen.coroutine
    def getCollectionGeneralDashboardProdYoY(self, db):
        raise tornado.gen.Return(db['general_dashboard_prod_yoy'])

    @tornado.gen.coroutine
    def getCollectionGeneralDashboardSerYoY(self, db):
        raise tornado.gen.Return(db['general_dashboard_ser_yoy'])

    @tornado.gen.coroutine
    def getAllPeriods(self, client):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.groupByPeriods()
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        periodDict = {}
        year_array = []
        quarter_array = []
        month_array = []
        week_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            sub_doc = doc["_id"]
            year_array.append(sub_doc['fiscal_year'])
            quarter_array.append(sub_doc['fiscal_quarter'])
            month_array.append(sub_doc['fiscal_month'])
            week_array.append(sub_doc['fiscal_week'])
        year_array = list(set(year_array))
        list.sort(year_array)
        quarter_array = list(set(quarter_array))
        list.sort(quarter_array)
        month_array = list(set(month_array))
        list.sort(month_array)
        week_array = list(set(week_array))
        list.sort(week_array)
        periodDict = {
            "year_list": year_array,
            "quarter_list": quarter_array,
            "month_list": month_array,
            "week_list": week_array,
        }
        raise tornado.gen.Return(periodDict)

    @tornado.gen.coroutine
    def getMaxPeriods(self, client):
        max_year = ''
        max_quarter = ''
        max_month = ''
        max_week = ''
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionGeneralDashboard(db)
        client.close()
        
        #Find Max Year
        aggregateQuery = [
            self.jsonObj.groupMaxYear()
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})

        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            max_year = doc['period']
        
        #Find Max Quarter
        aggregateQuery = None
        aggregateQuery = [
            self.jsonObj.matchByYear(fiscal_year=max_year),
            self.jsonObj.groupMaxQuarter()
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})

        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            max_quarter = doc['period']

        #Find Max Month
        aggregateQuery = None
        aggregateQuery = [
            self.jsonObj.matchByYearQuarter(fiscal_year=max_year, quarter=max_quarter),
            self.jsonObj.groupMaxMonth()
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            max_month = doc['period']

        #Find Max Week
        aggregateQuery = None
        aggregateQuery = [
            self.jsonObj.matchByYearQuarterMonth(fiscal_year=max_year, quarter=max_quarter, month=max_month),
            self.jsonObj.groupMaxWeek()
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            max_week = doc['period']
       
        raise tornado.gen.Return((max_year, max_quarter, max_month, max_week))


    @tornado.gen.coroutine
    def getBookingHistory(self, client, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        if self.jsonObj.matchByMultipleParams(fiscal_year=None, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week):
            aggregateQuery = [
                self.jsonObj.matchByMultipleParams(fiscal_year=None, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
                self.jsonObj.groupBookingByHistory(),
                {
                 "$sort" : SON([("_id", 1)])
                }
            ]
        else:
            aggregateQuery = [
                self.jsonObj.groupBookingByHistory(),
                {
                 "$sort" : SON([("_id", 1)])
                }
            ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getGeneralDashboardDataset(self, client, user_name=None, fp_year=None,
            fp_quarter=None, fp_month=None, fp_week=None, scms=None,
            sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None,
            partner_name=None, customer_name=None, prod_ser=None):
        dataSet = {}
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        if prod_ser is None:
            collection = yield self.getCollectionGeneralDashboard(db)
        else:
            collection = yield self.getCollectionGeneralDashboardProdSer(db)
        client.close()
        matchObj = {
                "username" : user_name
        }
        if fp_year is not None:
            matchObj["periods.year"] = fp_year
        if fp_year is not None:
            matchObj["periods.quarter"] = fp_quarter
        if fp_year is not None:
            matchObj["periods.month"] = fp_month
        if fp_year is not None:
            matchObj["periods.week"] = fp_week
        if prod_ser is not None:
            matchObj["periods.prod_ser"] = prod_ser

        cursor = collection.find(matchObj)
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            for element in doc['tdBooking']['yAxis']:
                dataSet['booking_dict'] =  {'booking' : element}
            for element in doc['billedCustomers']['yAxis']:
                dataSet['billed_customers'] =  {'booking' : element}
            for element in doc['billedPartners']['yAxis']:
                dataSet['billed_partners'] =  {'booking' : element}
            for element in doc['techPenetration']['yAxis']:
                dataSet['tech_pen'] =  {'booking' : element}
            for element in doc['yieldPerCustomer']['yAxis']:
                dataSet['yld_per_cus'] =  {'booking' : element}


            if (fp_year is not None) and (fp_quarter is None) and (fp_month is None) and (fp_week is None):
                z = yield self.helper.calculateRatio(doc['newAccounts']['yAxis2'], doc['newAccounts']['yAxis0'])
                dataSet['new_accounts_ly'] = {
                        'y' : doc['newAccounts']['yAxis2'],
                        'x' : doc['newAccounts']['yAxis3'],
                        'z' : z * 100,
                        'name' : 'N1',
                        'description' : 'New Accounts'
                }
                z = yield self.helper.calculateRatio(doc['newAccounts']['yAxis4'], doc['newAccounts']['yAxis0'])
                dataSet['new_accounts_l3y'] = {
                        'y' : doc['newAccounts']['yAxis4']/3,
                        'x' : doc['newAccounts']['yAxis5']/3,
                        'z' : z * 100,
                        'name' : 'N3',
                        'description' : 'New Accounts'
                }
                z = yield self.helper.calculateRatio(doc['repeatAccounts']['yAxis2'], doc['repeatAccounts']['yAxis0'])
                dataSet['repeat_accounts_ly'] = {
                        'y' : doc['repeatAccounts']['yAxis2'],
                        'x' : doc['repeatAccounts']['yAxis3'],
                        'z' : z * 100,
                        'name' : 'R1',
                        'description' : 'Repeat Accounts'
                }
                z = yield self.helper.calculateRatio(doc['repeatAccounts']['yAxis4'], doc['repeatAccounts']['yAxis0'])
                dataSet['repeat_accounts_l3y'] = {
                        'y' : doc['repeatAccounts']['yAxis4']/3,
                        'x' : doc['repeatAccounts']['yAxis5']/3,
                        'z' : z * 100,
                        'name' : 'R3',
                        'description' : 'Repeat Accounts'
                }
                z = yield self.helper.calculateRatio(doc['dormantAccounts']['yAxis2'], doc['dormantAccounts']['yAxis0'])
                dataSet['dormant_accounts_ly'] = {
                        'y' : doc['dormantAccounts']['yAxis2'],
                        'x' : doc['dormantAccounts']['yAxis3'],
                        'z' : z * 100,
                        'name' : 'D1',
                        'description' : 'Dormant Accounts'
                }
                z = yield self.helper.calculateRatio(doc['dormantAccounts']['yAxis5'], doc['dormantAccounts']['yAxis4'])
                dataSet['dormant_accounts_l3y'] = {
                        'y' : doc['dormantAccounts']['yAxis5']/3,
                        'x' : doc['dormantAccounts']['yAxis6']/3,
                        'z' : z * 100,
                        'name' : 'D3',
                        'description' : 'Dormant Accounts'
                }

            dataSet['arch2_array'] = doc['archBooking']['xAxis']
            dataSet['arch2_booking_array'] = doc['archBooking']['yAxis']
            dataSet['year_array'] = doc['bookingHistory']['xAxis']
            dataSet['year_booking_array'] = doc['bookingHistory']['yAxis']
            dataSet['vertical_array'] = doc['verticalBooking']['xAxis']
            dataSet['vertical_booking_array'] = doc['verticalBooking']['yAxis']
            dataSet['tech_array'] = doc['techBooking']['xAxis']
            dataSet['tech_booking_array'] = doc['techBooking']['yAxis']
            dataSet['atAttach_array'] = doc['atAttachBooking']['xAxis']
            dataSet['atAttach_booking_array'] = doc['atAttachBooking']['yAxis']
            dataSet['subscms_array'] = doc['subSCMSBooking']['xAxis']
            dataSet['subscms_booking_array'] = doc['subSCMSBooking']['yAxis']
            dataSet['gtmu_array'] = doc['gtmuBooking']['xAxis']
            dataSet['gtmu_booking_array'] = doc['gtmuBooking']['yAxis']
            dataSet['region_array'] = doc['regionBooking']['xAxis']
            dataSet['region_booking_array'] = doc['regionBooking']['yAxis']
            dataSet['customer_array'] = doc['topCustomerBooking']['xAxis']
            dataSet['customer_booking_array'] = doc['topCustomerBooking']['yAxis']
            dataSet['topdeals_array'] = doc['topDeals']['xAxis']
            dataSet['topdeals_booking_array'] = doc['topDeals']['yAxis']
            dataSet['partner_array'] = doc['topPartnerBooking']['xAxis']
            dataSet['partner_booking_array'] = doc['topPartnerBooking']['yAxis']
            dataSet['sl6_array'] = doc['topSL6Booking']['xAxis']
            dataSet['sl6_booking_array'] = doc['topSL6Booking']['yAxis']
            dataSet['qoq_array'] = doc['qoqBooking']['xAxis']
            dataSet['qoq_booking_array'] = doc['qoqBooking']['yAxis']
            dataSet['mom_array'] = doc['momBooking']['xAxis']
            dataSet['mom_booking_array'] = doc['momBooking']['yAxis']

            momDict = dict(zip(dataSet['mom_array'], dataSet['mom_booking_array']))
            dataSet['mom_array'] = []
            dataSet['mom_booking_array'] = []
            for key in sorted(momDict, key=self._keyify):
                # print "Month: " + str(key)
                dataSet['mom_array'].append(key) 
                dataSet['mom_booking_array'].append(momDict[key])

            dataSet['wow_array'] = doc['wowBooking']['xAxis']
            dataSet['wow_booking_array'] = doc['wowBooking']['yAxis']
            dataSet['prodSer_array'] = doc['prodSerBooking']['xAxis']
            dataSet['prodSer_booking_array'] = doc['prodSerBooking']['yAxis']
            dataSet['discount_array'] = doc['disArchsBooking']['xAxis']
            dataSet['discount_booking_array'] = doc['disArchsBooking']['yAxis']
            dataSet['discount_overall_array'] = doc['disAllBooking']['xAxis']
            dataSet['discount_overall_booking_array'] = doc['disAllBooking']['yAxis']
        raise tornado.gen.Return(dataSet)

    def _keyify(self, x):
        try:
            xi = int(x)
        except ValueError:
            return 'S{0}'.format(x)
        else:
            return 'I{0:0{1}}'.format(xi, Constants.MAX_DIGITS)




    @tornado.gen.coroutine
    def getGeneralDashboardYoYDataset(self, client, user_name=None,
            fp_year=None, fp_quarter=None, fp_month=None, fp_week=None,
            scms=None, sub_scms=None, gtmu=None, region=None, sl6=None,
            sales_agent=None, partner_name=None, customer_name=None,
            prod_ser=None):
        dataSet = {}
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        if prod_ser is None:
            collection = yield self.getCollectionGeneralDashboardYoY(db)
        elif prod_ser == 'product':
            collection = yield self.getCollectionGeneralDashboardProdYoY(db)
        elif prod_ser == 'service':
            collection = yield self.getCollectionGeneralDashboardSerYoY(db)

        client.close()
        matchObj = {
                "username" : user_name
        }

        print "User Name: " + user_name

        booking_color_config = {
            'positive' : [0,255,0,1],
            'negative' : [255,0,0,1],
            'neutral' : [255,255,0,1],
        }
        discount_color_config = {
            'negative' : [0,255,0,1],
            'positive' : [255,0,0,1],
            'neutral' : [255,255,0,1],
        }
        cursor = collection.find(matchObj)
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            for element in doc['tdBooking']['yAxis']:
                dataSet['booking_dict'] =  {
                    'booking' : element*100,
                    'unit' : '%',
                    'series_name' : 'YTD',
                    'color_config' : booking_color_config,
                }
            for element in doc['yieldPerCustomer']['yAxis']:
                dataSet['yield_per_customer'] =  {
                    'booking' : element*100,
                    'unit' : '%',
                    'series_name' : 'Yld/Cus',
                    'color_config' : booking_color_config,
                }
            for element in doc['billedCustomers']['yAxis']:
                dataSet['bld_cus'] =  {
                    'booking' : element*100,
                    'unit' : '%',
                    'series_name' : 'Bld.Cus',
                    'color_config' : booking_color_config,
                }
            for element in doc['billedPartners']['yAxis']:
                dataSet['bld_par'] =  {
                    'booking' : element*100,
                    'unit' : '%',
                    'series_name' : 'Bld.Par',
                    'color_config' : booking_color_config,
                }
            for element in doc['techPenetration']['yAxis']:
                dataSet['tech_pen'] =  {
                    'booking' : element*100,
                    'unit' : '%',
                    'series_name' : 'Tech Pen',
                    'color_config' : booking_color_config,
                }
            tech_name = 'ENT_NW'
            try:
                tempIndex = doc['archBooking']['xAxis'].index(tech_name)
                dataSet['ent_nw'] = {
                    'booking' : doc['archBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['ent_nw'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }

            tech_name = 'Security'
            try:
                tempIndex = doc['archBooking']['xAxis'].index(tech_name)
                dataSet['security'] = {
                    'booking' : doc['archBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['security'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            tech_name = 'Collab'
            try:
                tempIndex = doc['archBooking']['xAxis'].index(tech_name)
                dataSet['collab'] = {
                    'booking' : doc['archBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['collab'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            tech_name = 'DCV'
            try:
                tempIndex = doc['archBooking']['xAxis'].index(tech_name)
                dataSet['dcv'] = {
                    'booking' : doc['archBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['dcv'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            tech_name = 'LAN Switching'
            try:
                tempIndex = doc['techBooking']['xAxis'].index(tech_name)
                dataSet['switching'] = {
                    'booking' : doc['techBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Switching',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['switching'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Switching',
                    'color_config' : booking_color_config,
                }
            tech_name = 'Wireless LAN'
            try:
                tempIndex = doc['techBooking']['xAxis'].index(tech_name)
                dataSet['wireless'] = {
                    'booking' : doc['techBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Wireless',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['wireless'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Wireless',
                    'color_config' : booking_color_config,
                }
            tech_name = 'Routing'
            try:
                tempIndex = doc['techBooking']['xAxis'].index(tech_name)
                dataSet['routing'] = {
                    'booking' : doc['techBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['routing'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            tech_name = 'UCS'
            try:
                tempIndex = doc['techBooking']['xAxis'].index(tech_name)
                dataSet['ucs'] = {
                    'booking' : doc['techBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['ucs'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : booking_color_config,
                }
            tech_name = 'Technical Services'
            try:
                tempIndex = doc['techBooking']['xAxis'].index(tech_name)
                dataSet['ts'] = {
                    'booking' : doc['techBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'TS',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['ts'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'TS',
                    'color_config' : booking_color_config,
                }
            tech_name = 'Advanced Services'
            try:
                tempIndex = doc['techBooking']['xAxis'].index(tech_name)
                dataSet['as'] = {
                    'booking' : doc['techBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'AS',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['as'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'AS',
                    'color_config' : booking_color_config,
                }
            tech_name = 'manufacturing'
            try:
                tempIndex = doc['verticalBooking']['xAxis'].index(tech_name)
                dataSet['mfg'] = {
                    'booking' : doc['verticalBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Mfg',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['mfg'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Mfg',
                    'color_config' : booking_color_config,
                }
            tech_name = 'education- public/private'
            try:
                tempIndex = doc['verticalBooking']['xAxis'].index(tech_name)
                dataSet['edu'] = {
                    'booking' : doc['verticalBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Edu',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['edu'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Edu',
                    'color_config' : booking_color_config,
                }
            tech_name = 'e-commerce'
            try:
                tempIndex = doc['verticalBooking']['xAxis'].index(tech_name)
                dataSet['ecom'] = {
                    'booking' : doc['verticalBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Ecom',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['ecom'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Ecom',
                    'color_config' : booking_color_config,
                }
            tech_name = 'Sales AT'
            try:
                tempIndex = doc['atAttachBooking']['xAxis'].index(tech_name)
                dataSet['at_attach'] = {
                    'booking' : doc['atAttachBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'AT-Attach',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['at_attach'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'AT-Attach',
                    'color_config' : booking_color_config,
                }
            tech_name = 'COMM_SELECT'
            try:
                tempIndex = doc['subSCMSBooking']['xAxis'].index(tech_name)
                dataSet['select'] = {
                    'booking' : doc['subSCMSBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'SELECT',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['select'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'SELECT',
                    'color_config' : booking_color_config,
                }
            tech_name = 'COM-MM'
            try:
                tempIndex = doc['subSCMSBooking']['xAxis'].index(tech_name)
                dataSet['mm'] = {
                    'booking' : doc['subSCMSBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Mid-Mrkt',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['mm'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Mid-Mrkt',
                    'color_config' : booking_color_config,
                }
            tech_name = 'COMM_GEO_NAMED'
            try:
                tempIndex = doc['subSCMSBooking']['xAxis'].index(tech_name)
                dataSet['geo_n'] = {
                    'booking' : doc['subSCMSBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'GEO-N',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['geo_n'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'GEO-N',
                    'color_config' : booking_color_config,
                }
            tech_name = 'COMM_GEO_NON_NA'
            try:
                tempIndex = doc['subSCMSBooking']['xAxis'].index(tech_name)
                dataSet['geo_nn'] = {
                    'booking' : doc['subSCMSBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'GEO-NN',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['geo_nn'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'GEO-NN',
                    'color_config' : booking_color_config,
                }
            tech_name = 'product'
            try:
                tempIndex = doc['prodSerBooking']['xAxis'].index(tech_name)
                dataSet['product'] = {
                    'booking' : doc['prodSerBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Product',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['product'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Product',
                    'color_config' : booking_color_config,
                }
            tech_name = 'service'
            try:
                tempIndex = doc['prodSerBooking']['xAxis'].index(tech_name)
                dataSet['service'] = {
                    'booking' : doc['prodSerBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Service',
                    'color_config' : booking_color_config,
                }
            except:
                dataSet['service'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Service',
                    'color_config' : booking_color_config,
                }
            try:
                dataSet['dis_overall'] = {
                    'booking' : doc['disAllBooking']['yAxis'][0]*100,
                    'unit' : '%',
                    'series_name' : 'Overall',
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_overall'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Overall',
                    'color_config' : discount_color_config,
                }
            tech_name = 'ENT_NW'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_ent_nw'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_ent_nw'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            tech_name = 'Security'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_security'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_security'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            tech_name = 'Collab'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_collab'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_collab'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            tech_name = 'DCV'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_dcv'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_dcv'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            tech_name = 'Cloud'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_cloud'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_cloud'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            tech_name = 'Others - Service'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_service'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : 'Service',
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_service'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : 'Service',
                    'color_config' : discount_color_config,
                }
            tech_name = 'Others'
            try:
                tempIndex = doc['disArchsBooking']['xAxis'].index(tech_name)
                dataSet['dis_others'] = {
                    'booking' : doc['disArchsBooking']['yAxis'][tempIndex]*100,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
            except:
                dataSet['dis_others'] = {
                    'booking' : 0.00,
                    'unit' : '%',
                    'series_name' : tech_name,
                    'color_config' : discount_color_config,
                }
                
        raise tornado.gen.Return(dataSet)


    @tornado.gen.coroutine
    def getBookingByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler()
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupExclusiveBooking()
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        dict_data = {}
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            dict_data = {
                "booking" : doc['booking']/Constants.MILLION
            }
            #print(doc)
        raise tornado.gen.Return((dict_data))
    

    @tornado.gen.coroutine
    def getArch2ByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByArch2(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getTechsByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByTechName(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getAtAttachByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByAtAttach(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getVerticalsByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByVertical(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getSubSCMSByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingBySubSCMS(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getGTMuByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByGTMu(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getRegionByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByRegion(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))
    
    @tornado.gen.coroutine
    def getTopCustomersByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByCustomer(),
            {
             "$sort" : SON([("booking", -1)])
            },
            {
             "$limit" : 10
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))
    
    @tornado.gen.coroutine
    def getTopPartnersByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByPartner(),
            {
             "$sort" : SON([("booking", -1)])
            },
            {
             "$limit" : 10
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getTopSL6ByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingBySL6(),
            {
             "$sort" : SON([("booking", -1)])
            },
            {
             "$limit" : 5
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getQuartersByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByQuarters(),
            {
             "$sort" : SON([("_id", 1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getProductServiceByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingByProductService(),
            {
             "$sort" : SON([("booking", -1)])
            }
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(doc['booking']/Constants.MILLION)
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))

    @tornado.gen.coroutine
    def getDiscountOfArchsByParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupBookingNetAndListByArchs(),
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(self.helper.calculateDiscount(doc['booking'], doc['base_list']))
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))
    
    @tornado.gen.coroutine
    def getDiscountOverallParams(self, client, fp_year=None, fp_quarter=None, fp_month=None, fp_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        dho = models.dataHandler.DataHandler();
        db = yield dho.getDBTrueNorth(client)
        collection = yield self.getCollectionBookingData(db)
        client.close()
        aggregateQuery = [
            self.jsonObj.matchByMultipleParams(fiscal_year=fp_year, quarter=fp_quarter, fiscal_month=fp_month, fiscal_week=fp_week),
            self.jsonObj.groupExclusiveBookingNetAndList(),
        ]
        cursor = yield collection.aggregate(aggregateQuery, cursor={})
        key_array = []
        value_array = []
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            key_array.append(doc['_id'])
            value_array.append(self.helper.calculateDiscount(doc['booking'], doc['base_list']))
            #print(doc)
        raise tornado.gen.Return((key_array, value_array))
