import models.dataHandler
from bson.son import SON
from models.constants import Constants
from models.dataStructures import MongoDataStructure
from models.helper import Helper
from pydoc import Doc
import models.mainDashboardDAO
import models.userDAO
import models.locationDAO
import models.accessDAO
import models.popDAO
import tornado.gen


class MainPageHelper():
    
    def __init__(self):
        self.jsonObj = models.dataStructures.MongoDataStructure()
        self.helper = Helper()
        

    @tornado.gen.coroutine
    def getMainPageData(self, username):

        client = yield models.dataHandler.DataHandler().getClient()
        mod = models.mainDashboardDAO.MainDashboardDAO()
        mod2 = models.userDAO.UserDAO()
        mod3 = models.accessDAO.AccessDAO()
        credentials = yield mod2.getSession(client, username)

        username = credentials['username']
        comrade = credentials['comrade']
        prod_ser = credentials['prod_ser']
        print "Product/Service Tag: " + str(prod_ser)
        max_year = credentials['maxYear']
        max_quarter = credentials['maxQuarter']
        max_month = credentials['maxMonth']
        max_week = credentials['maxWeek']
        fiscal_year = credentials['fiscal_year']
        fiscal_quarter = credentials['fiscal_quarter']
        fiscal_month = credentials['fiscal_month']
        fiscal_week = credentials['fiscal_week']
        container_no = credentials['container_no']
        round_count = credentials['round_count']
        access_code = credentials['access_code']
        firstname = credentials['firstname']
        lastname = credentials['lastname']
        desig_chart_display = credentials['desig_chart_display']
        period_chart_display = credentials['period_chart_display']
        prodser_chart_display = credentials['prodser_chart_display']
        growth_chart_display = credentials['growth_chart_display']

        dataUsername = None
        if (username is not None) and (comrade is not None):
            dataUsername = comrade
        elif (username is not None) and (comrade is None):
            dataUsername = username
        else:
            print "User Name is not defined"


        print "Cookie: " + username
        responseData = {}
        growth_data = {}
        updatable = {}

        status = 'success'
        errMessage = 'no more data avaibale'
        if int(fiscal_year)>2010:
            if round_count == 0:
                updatable['username'] = username
                updatable['comrade'] = comrade
                updatable['prod_ser'] = prod_ser
                updatable['firstname'] = firstname
                updatable['lastname'] = lastname
                updatable['maxYear'] = max_year
                updatable['maxQuarter'] = max_quarter
                updatable['maxMonth'] = max_month
                updatable['maxWeek'] = max_week
                updatable['fiscal_year'] = fiscal_year
                updatable['fiscal_quarter'] = max_quarter
                updatable['fiscal_month'] = None
                updatable['fiscal_week'] = None
                updatable['container_no'] = container_no+1
                updatable['round_count'] = round_count+1
                updatable['access_code'] = access_code
                period_access_credentials_temp = yield mod3.getPeriodAccessCredentials(client, 'quarter')
                prodser_access_credentials_temp = yield mod3.getProdSerAccessCredentials(client, prod_ser)
                updatable['prodser_chart_display'] = prodser_access_credentials_temp['chart_display']
                updatable['desig_chart_display'] = desig_chart_display
                updatable['period_chart_display'] = period_access_credentials_temp['chart_display']
                updatable['growth_chart_display'] = prodser_access_credentials_temp['growth_display']

                dataSet = yield mod.getGeneralDashboardYoYDataset(client,
                        fp_year=fiscal_year, fp_quarter= fiscal_quarter,
                        fp_month=fiscal_month, fp_week=fiscal_week,
                        user_name=dataUsername, prod_ser=prod_ser)
                status = 'success'
                errMessage = ""

                growth_data = {
                        'td_booking' : dataSet['booking_dict'],
                        'yld_per_cus' : dataSet['yield_per_customer'],
                        'bld_cus' : dataSet['bld_cus'],
                        'bld_par' : dataSet['bld_par'],
                        'tech_pen' : dataSet['tech_pen'],
                        'ent_nw' : dataSet['ent_nw'],
                        'security' : dataSet['security'],
                        'collab' : dataSet['collab'],
                        'dcv' : dataSet['dcv'],
                        'switching' : dataSet['switching'],
                        'wireless' : dataSet['wireless'],
                        'routing' : dataSet['routing'],
                        'ucs' : dataSet['ucs'],
                        'ts' : dataSet['ts'],
                        'as' : dataSet['as'],
                        'mfg' : dataSet['mfg'],
                        'edu' : dataSet['edu'],
                        'ecom' : dataSet['ecom'],
                        'at_attach' : dataSet['at_attach'],
                        'select' : dataSet['select'],
                        'mm' : dataSet['mm'],
                        'geo_n' : dataSet['geo_n'],
                        'geo_nn' : dataSet['geo_nn'],
                        'product' : dataSet['product'],
                        'service' : dataSet['service'],
                        'dis_overall' : dataSet['dis_overall'],
                        'dis_ent_nw' : dataSet['dis_ent_nw'],
                        'dis_security' : dataSet['dis_security'],
                        'dis_collab' : dataSet['dis_collab'],
                        'dis_dcv' : dataSet['dis_dcv'],
                        'dis_cloud' : dataSet['dis_cloud'],
                        'dis_service' : dataSet['dis_service'],
                        'dis_others' : dataSet['dis_others'],
                } 
            elif round_count == 1:
                updatable['username'] = username
                updatable['comrade'] = comrade
                updatable['prod_ser'] = prod_ser
                updatable['firstname'] = firstname
                updatable['lastname'] = lastname
                updatable['maxYear'] = max_year
                updatable['maxQuarter'] = max_quarter
                updatable['maxMonth'] = max_month
                updatable['maxWeek'] = max_week
                updatable['fiscal_year'] = fiscal_year
                updatable['fiscal_quarter'] = max_quarter
                updatable['fiscal_month'] = max_month
                updatable['fiscal_week'] = None
                updatable['container_no'] = container_no+1
                updatable['round_count'] = round_count+1
                updatable['access_code'] = access_code
                period_access_credentials_temp = yield mod3.getPeriodAccessCredentials(client, 'month')
                prodser_access_credentials_temp = yield mod3.getProdSerAccessCredentials(client, prod_ser)
                updatable['prodser_chart_display'] = prodser_access_credentials_temp['chart_display']
                updatable['desig_chart_display'] = desig_chart_display
                updatable['period_chart_display'] = period_access_credentials_temp['chart_display']
                updatable['growth_chart_display'] = prodser_access_credentials_temp['growth_display']
            elif round_count == 2:
                updatable['username'] = username
                updatable['comrade'] = comrade
                updatable['prod_ser'] = prod_ser
                updatable['firstname'] = firstname
                updatable['lastname'] = lastname
                updatable['maxYear'] = max_year
                updatable['maxQuarter'] = max_quarter
                updatable['maxMonth'] = max_month
                updatable['maxWeek'] = max_week
                updatable['fiscal_year'] = fiscal_year
                updatable['fiscal_quarter'] = max_quarter
                updatable['fiscal_month'] = max_month
                updatable['fiscal_week'] = max_week
                updatable['container_no'] = container_no+1
                updatable['round_count'] = round_count+1
                updatable['access_code'] = access_code
                period_access_credentials_temp = yield mod3.getPeriodAccessCredentials(client, 'week')
                prodser_access_credentials_temp = yield mod3.getProdSerAccessCredentials(client, prod_ser)
                updatable['prodser_chart_display'] = prodser_access_credentials_temp['chart_display']
                updatable['desig_chart_display'] = desig_chart_display
                updatable['period_chart_display'] = period_access_credentials_temp['chart_display']
                updatable['growth_chart_display'] = prodser_access_credentials_temp['growth_display']
            elif round_count == 3:
                updatable['username'] = username
                updatable['comrade'] = comrade
                updatable['prod_ser'] = prod_ser
                updatable['firstname'] = firstname
                updatable['lastname'] = lastname
                updatable['maxYear'] = max_year
                updatable['maxQuarter'] = max_quarter
                updatable['maxMonth'] = max_month
                updatable['maxWeek'] = max_week
                updatable['fiscal_year'] = str(int(fiscal_year)-1)
                updatable['fiscal_quarter'] = None
                updatable['fiscal_month'] = None
                updatable['fiscal_week'] = None
                updatable['container_no'] = container_no+1
                updatable['round_count'] = round_count+1
                updatable['access_code'] = access_code
                period_access_credentials_temp = yield mod3.getPeriodAccessCredentials(client, 'year')
                prodser_access_credentials_temp = yield mod3.getProdSerAccessCredentials(client, prod_ser)
                updatable['prodser_chart_display'] = prodser_access_credentials_temp['chart_display']
                updatable['desig_chart_display'] = desig_chart_display
                updatable['period_chart_display'] = period_access_credentials_temp['chart_display']
                updatable['growth_chart_display'] = prodser_access_credentials_temp['growth_display']
            elif round_count == 4:
                updatable['username'] = username
                updatable['comrade'] = comrade
                updatable['prod_ser'] = prod_ser
                updatable['firstname'] = firstname
                updatable['lastname'] = lastname
                updatable['maxYear'] = max_year
                updatable['maxQuarter'] = max_quarter
                updatable['maxMonth'] = max_month
                updatable['maxWeek'] = max_week
                updatable['fiscal_year'] = fiscal_year
                updatable['fiscal_quarter'] = max_quarter
                updatable['fiscal_month'] = None
                updatable['fiscal_week'] = None
                updatable['container_no'] = container_no+1
                updatable['round_count'] = 1
                updatable['access_code'] = access_code
                period_access_credentials_temp = yield mod3.getPeriodAccessCredentials(client, 'quarter')
                prodser_access_credentials_temp = yield mod3.getProdSerAccessCredentials(client, prod_ser)
                updatable['prodser_chart_display'] = prodser_access_credentials_temp['chart_display']
                updatable['desig_chart_display'] = desig_chart_display
                updatable['period_chart_display'] = period_access_credentials_temp['chart_display']
                updatable['growth_chart_display'] = prodser_access_credentials_temp['growth_display']
            isOK = mod2.updateSession(client, username, updatable)
            updatable = None

            year_last_two = fiscal_year[-2:]
            year_text = ''
            quarter_text = ''
            month_text = ''
            week_text = ''
            if (fiscal_quarter != None):
                quarter_text = '-' + fiscal_quarter
            if (fiscal_month != None):
                month_text = '-M' + fiscal_month
            if (fiscal_week != None):
                week_text = '-W' + fiscal_week
            if fiscal_quarter == None and fiscal_month == None and fiscal_week == None:
                year_text = '-YTD'
            container_header = 'FY' + year_last_two + quarter_text + month_text + week_text + year_text + ' At a glance'
            # print "Year: " + str(fiscal_year) + "|Quarter: " + str(fiscal_quarter) + "|Month: " + str(fiscal_month) + "|Week: " + str(fiscal_week) + "|||Container NO.: " + str(container_no) + "|Round Count: " + str(round_count)

            dataSet = yield mod.getGeneralDashboardDataset(client,
                    fp_year=fiscal_year, fp_quarter= fiscal_quarter,
                    fp_month=fiscal_month, fp_week=fiscal_week,
                    user_name=dataUsername, prod_ser=prod_ser)
            
            if 'booking_dict' in dataSet.keys():
                booking_dict = dataSet['booking_dict']
                billed_customers = dataSet['billed_customers']
                billed_partners = dataSet['billed_partners']
                if (fiscal_year is not None) and (fiscal_quarter is None) and (fiscal_month is None) and (fiscal_week is None):
                    new_accounts_ly = dataSet['new_accounts_ly']
                    new_accounts_l3y = dataSet['new_accounts_l3y']
                    repeat_accounts_ly = dataSet['repeat_accounts_ly']
                    repeat_accounts_l3y = dataSet['repeat_accounts_l3y']
                    dormant_accounts_ly = dataSet['dormant_accounts_ly']
                    dormant_accounts_l3y = dataSet['dormant_accounts_l3y']

                tech_pen = dataSet['tech_pen']
                yld_per_cus = dataSet['yld_per_cus']
                arch2_array, arch2_booking_array = dataSet['arch2_array'], dataSet['arch2_booking_array']
                year_array, year_booking_array = dataSet['year_array'], dataSet['year_booking_array']
                vertical_array, vertical_booking_array = dataSet['vertical_array'], dataSet['vertical_booking_array']
                tech_array, tech_booking_array = dataSet['tech_array'], dataSet['tech_booking_array']
                atAttach_array, atAttach_booking_array = dataSet['atAttach_array'], dataSet['atAttach_booking_array']
                subscms_array, subscms_booking_array = dataSet['subscms_array'],dataSet['subscms_booking_array']
                gtmu_array, gtmu_booking_array = dataSet['gtmu_array'], dataSet['gtmu_booking_array']
                region_array, region_booking_array = dataSet['region_array'], dataSet['region_booking_array']
                customer_array, customer_booking_array = dataSet['customer_array'], dataSet['customer_booking_array']
                topdeals_array, topdeals_booking_array = dataSet['topdeals_array'], dataSet['topdeals_booking_array']
                partner_array, partner_booking_array = dataSet['partner_array'], dataSet['partner_booking_array']
                sl6_array, sl6_booking_array = dataSet['sl6_array'], dataSet['sl6_booking_array']
                qoq_array, qoq_booking_array = dataSet['qoq_array'], dataSet['qoq_booking_array']
                mom_array, mom_booking_array = dataSet['mom_array'], dataSet['mom_booking_array']
                wow_array, wow_booking_array = dataSet['wow_array'], dataSet['wow_booking_array']
                prodSer_array, prodSer_booking_array = dataSet['prodSer_array'], dataSet['prodSer_booking_array']
                discount_array, discount_booking_array = dataSet['discount_array'], dataSet['discount_booking_array']
                discount_overall_array, discount_overall_booking_array = dataSet['discount_overall_array'], dataSet['discount_overall_booking_array']
                status = 'success'
                errMessage = "No Data avaibale"


                # Enable only the required charts to be displayed
                chart_display_config = {}
                how_many_charts = 0
                for key, value in desig_chart_display.iteritems():
                    if value == 1 and period_chart_display[key] == 1 and prodser_chart_display[key] == 1:
                            chart_display_config[key] = 1
                            how_many_charts += 1
                            # print key + "-" + str(how_many_charts)
                    else:
                        chart_display_config[key] = 0

                # Enable only the required growth charts to be displayed
                chart_display_config2 = {}
                for key, value in growth_chart_display.iteritems():
                    if value == 1:
                        chart_display_config2[key] = 1
                    else:
                        chart_display_config2[key] = 0
            else:
                new_accounts_ly=None
                new_accounts_l3y=None
                repeat_accounts_ly=None
                repeat_accounts_l3y=None
                dormant_accounts_ly=None
                dormant_accounts_l3y=None
                booking_dict=None
                billed_customers=None
                billed_partners=None
                tech_pen=None
                yld_per_cus=None
                arch2_array=None
                arch2_booking_array=None
                year_array=None
                year_booking_array=None
                vertical_array=None
                vertical_booking_array=None
                tech_array=None
                tech_booking_array=None
                atAttach_array=None
                atAttach_booking_array=None
                subscms_array=None
                subscms_booking_array=None
                gtmu_array=None
                gtmu_booking_array=None
                region_array=None
                region_booking_array=None
                customer_array=None
                customer_booking_array=None
                topdeals_array=None
                topdeals_booking_array=None
                partner_array=None
                partner_booking_array=None
                sl6_array=None
                sl6_booking_array=None
                qoq_array=None
                qoq_booking_array=None
                mom_array=None
                mom_booking_array=None
                wow_array=None
                wow_booking_array=None
                prodSer_array=None
                prodSer_booking_array=None
                discount_array=None
                discount_booking_array=None
                discount_overall_array=None
                discount_overall_booking_array=None
                container_no=None
                container_header=None
                growth_data=None
                round_count=None
                chart_display_config=None
                chart_display_config2=None
                how_many_charts=None
                status = 'failed'
                errMessage = 'no more data avaibale'

            if (fiscal_year is not None) and (fiscal_quarter is None) and (fiscal_month is None) and (fiscal_week is None):
                responseData = {
                    'status' : status,
                    'err' : errMessage,
                    'new_accounts_ly' : new_accounts_ly,
                    'new_accounts_l3y' : new_accounts_l3y,
                    'repeat_accounts_ly' : repeat_accounts_ly,
                    'repeat_accounts_l3y' : repeat_accounts_l3y,
                    'dormant_accounts_ly' : dormant_accounts_ly,
                    'dormant_accounts_l3y' : dormant_accounts_l3y,
                    'booking_data' : booking_dict,
                    'billed_customers' : billed_customers,
                    'billed_partners' : billed_partners,
                    'tech_pen' : tech_pen,
                    'yld_per_cus' : yld_per_cus,
                    'arch2_array' : arch2_array,
                    'arch2_booking_array' : arch2_booking_array,
                    'year_array' : year_array,
                    'year_booking_array' : year_booking_array,
                    'vertical_array' : vertical_array,
                    'vertical_booking_array' : vertical_booking_array,
                    'tech_array' : tech_array,
                    'tech_booking_array' : tech_booking_array,
                    'atAttach_array' : atAttach_array,
                    'atAttach_booking_array' : atAttach_booking_array,
                    'subscms_array' : subscms_array,
                    'subscms_booking_array' : subscms_booking_array,
                    'gtmu_array' : gtmu_array,
                    'gtmu_booking_array' : gtmu_booking_array,
                    'region_array' : region_array,
                    'region_booking_array' : region_booking_array,
                    'customer_array' : customer_array,
                    'customer_booking_array' : customer_booking_array,
                    'topdeals_array' : topdeals_array,
                    'topdeals_booking_array' : topdeals_booking_array,
                    'partner_array' : partner_array,
                    'partner_booking_array' : partner_booking_array,
                    'sl6_array' : sl6_array,
                    'sl6_booking_array' : sl6_booking_array,
                    'qoq_array' : qoq_array,
                    'qoq_booking_array' : qoq_booking_array,
                    'mom_array' : mom_array,
                    'mom_booking_array' : mom_booking_array,
                    'wow_array' : wow_array,
                    'wow_booking_array' : wow_booking_array,
                    'prodSer_array' : prodSer_array,
                    'prodSer_booking_array' : prodSer_booking_array,
                    'discount_array' : discount_array,
                    'discount_booking_array' : discount_booking_array,
                    'discount_overall_array' : discount_overall_array,
                    'discount_overall_booking_array' : discount_overall_booking_array,
                    'container_no': container_no,
                    'container_header' : container_header,
                    'growth_data' : growth_data,
                    'round_count' : round_count,
                    'chart_display_config' : chart_display_config,
                    'chart_display_config2' : chart_display_config2,
                    'how_many_charts' : how_many_charts,
                    'what_display' : prod_ser,
                }
            else:
                responseData = {
                    'status' : status,
                    'err' : errMessage,
                    'booking_data' : booking_dict,
                    'billed_customers' : billed_customers,
                    'billed_partners' : billed_partners,
                    'tech_pen' : tech_pen,
                    'yld_per_cus' : yld_per_cus,
                    'arch2_array' : arch2_array,
                    'arch2_booking_array' : arch2_booking_array,
                    'year_array' : year_array,
                    'year_booking_array' : year_booking_array,
                    'vertical_array' : vertical_array,
                    'vertical_booking_array' : vertical_booking_array,
                    'tech_array' : tech_array,
                    'tech_booking_array' : tech_booking_array,
                    'atAttach_array' : atAttach_array,
                    'atAttach_booking_array' : atAttach_booking_array,
                    'subscms_array' : subscms_array,
                    'subscms_booking_array' : subscms_booking_array,
                    'gtmu_array' : gtmu_array,
                    'gtmu_booking_array' : gtmu_booking_array,
                    'region_array' : region_array,
                    'region_booking_array' : region_booking_array,
                    'customer_array' : customer_array,
                    'customer_booking_array' : customer_booking_array,
                    'topdeals_array' : topdeals_array,
                    'topdeals_booking_array' : topdeals_booking_array,
                    'partner_array' : partner_array,
                    'partner_booking_array' : partner_booking_array,
                    'sl6_array' : sl6_array,
                    'sl6_booking_array' : sl6_booking_array,
                    'qoq_array' : qoq_array,
                    'qoq_booking_array' : qoq_booking_array,
                    'mom_array' : mom_array,
                    'mom_booking_array' : mom_booking_array,
                    'wow_array' : wow_array,
                    'wow_booking_array' : wow_booking_array,
                    'prodSer_array' : prodSer_array,
                    'prodSer_booking_array' : prodSer_booking_array,
                    'discount_array' : discount_array,
                    'discount_booking_array' : discount_booking_array,
                    'discount_overall_array' : discount_overall_array,
                    'discount_overall_booking_array' : discount_overall_booking_array,
                    'container_no': container_no,
                    'container_header' : container_header,
                    'growth_data' : growth_data,
                    'round_count' : round_count,
                    'chart_display_config' : chart_display_config,
                    'chart_display_config2' : chart_display_config2,
                    'how_many_charts' : how_many_charts,
                    'what_display' : prod_ser,
                }
        else:
            status = 'failed'
            errMessage = 'No More Data avaibale'
            responseData = {
                'status' : status,
                'err' : errMessage,
            }

        raise tornado.gen.Return(responseData)

