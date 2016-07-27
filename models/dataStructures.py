'''
Created on Aug 28, 2015

@author: jeydurai
'''

class MongoDataStructure():
    def __init__(self):
        # Mongo Field Structure Assignment
        self.field_year = "periods.year"
        self.field_quarter = "periods.quarter"
        self.field_month = "periods.month"
        self.field_week = "periods.week"
        self.field_arch2 = "technologies.arch2"
        self.field_techName = "technologies.tech_name"
        self.field_atAttach = "technologies.at_attach"
        self.field_vertical = "business_nodes.industry_vertical"
        self.field_scms = "business_nodes.scms"
        self.field_subscms = "business_nodes.sub_scms"
        self.field_gtmu = "location_nodes.gtmu"
        self.field_region = "location_nodes.region"
        self.field_sl6 = "location_nodes.sales_level_6"
        self.field_salesAgent = "names.sales_agent.name"
        self.field_partnerName = "names.partner.unique_name"
        self.field_customerName = "names.customer.unique_name"
        self.field_prodSer = "prod_ser"
        self.field_bookingNet = "metric.booking_net"
        self.field_bookingList = "metric.base_list"
        
        # Mongo Field Structure as Group Assignment
        self.field_year_asGroup = "$periods.year"
        self.field_quarter_asGroup = "$periods.quarter"
        self.field_month_asGroup = "$periods.month"
        self.field_week_asGroup = "$periods.week"
        self.field_arch2_asGroup = "$technologies.arch2"
        self.field_techName_asGroup = "$technologies.tech_name"
        self.field_atAttach_asGroup = "$technologies.at_attach"
        self.field_bookingNet_asGroup = "$metric.booking_net"
        self.field_bookingList_asGroup = "$metric.base_list"
        self.field_scms_asGroup = "$business_nodes.scms"
        self.field_subscms_asGroup = "$business_nodes.sub_scms"
        self.field_gtmu_asGroup = "$location_nodes.gtmu"
        self.field_region_asGroup = "$location_nodes.region"
        self.field_sl6_asGroup = "$location_nodes.sales_level_6"
        self.field_salesAgent_asGroup = "$names.sales_agent.name"
        self.field_partnerName_asGroup = "$names.partner.unique_name"
        self.field_customerName_asGroup = "$names.customer.unique_name"
        self.field_prodSer_asGroup = "$prod_ser"
        self.field_vertical_asGroup = "$business_nodes.industry_vertical"
     
    # function to return Object for summing up Booking Net   

    
    def getGroupObjMaxYear(self):
        jsonObj = {
            "$max" : self.field_year_asGroup
        } 
        return jsonObj

    def getGroupObjMaxQuarter(self):
        jsonObj = {
            "$max" : self.field_quarter_asGroup
        } 
        return jsonObj

    def getGroupObjMaxMonth(self):
        jsonObj = {
            "$max" : self.field_month_asGroup
        } 
        return jsonObj

    def getGroupObjMaxWeek(self):
        jsonObj = {
            "$max" : self.field_week_asGroup
        } 
        return jsonObj

    def getGroupObjBooking(self):
        jsonObj = {
            "$sum" : self.field_bookingNet_asGroup
        } 
        return jsonObj

    def getGroupObjBaseList(self):
        jsonObj = {
            "$sum" : self.field_bookingList_asGroup
        } 
        return jsonObj
    
    # Matching Criteria (OR Query)
    def matchByYear(self, fiscal_year):
        jsonObj = {
            "$match" : {self.field_year : fiscal_year}
        }
        return jsonObj

    def matchByYearQuarter(self, fiscal_year, quarter):
        jsonObj = {
            "$match" : {
                self.field_year : fiscal_year,
                self.field_quarter : quarter,
            }
        }
        return jsonObj

    def matchByYearQuarterMonth(self, fiscal_year, quarter, month):
        jsonObj = {
            "$match" : {
                self.field_year : fiscal_year,
                self.field_quarter : quarter,
                self.field_month : month,
            }
        }
        return jsonObj
    
    def groupByPeriods(self):
        jsonObj = {
             "$group" : {
                "_id" : {
                    "fiscal_year": self.field_year_asGroup,
                    "fiscal_quarter": self.field_quarter_asGroup,
                    "fiscal_month": self.field_month_asGroup,
                    "fiscal_week": self.field_week_asGroup,
                },
            }
        }
        return jsonObj

    def groupBookingByArch2(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_arch2_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByTechName(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_techName_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByAtAttach(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_atAttach_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingBySubSCMS(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_subscms_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByGTMu(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_gtmu_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByRegion(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_region_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupExclusiveBooking(self):
        jsonObj = {
             "$group" : {
                "_id" : None,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupMaxYear(self):
        jsonObj = {
             "$group" : {
                "_id" : None,
                "period" : self.getGroupObjMaxYear() 
            }
        }
        return jsonObj

    def groupMaxQuarter(self):
        jsonObj = {
             "$group" : {
                "_id" : None,
                "period" : self.getGroupObjMaxQuarter() 
            }
        }
        return jsonObj

    def groupMaxMonth(self):
        jsonObj = {
             "$group" : {
                "_id" : None,
                "period" : self.getGroupObjMaxMonth() 
            }
        }
        return jsonObj

    def groupMaxWeek(self):
        jsonObj = {
             "$group" : {
                "_id" : None,
                "period" : self.getGroupObjMaxWeek() 
            }
        }
        return jsonObj

    
    def groupExclusiveBookingNetAndList(self):
        jsonObj = {
             "$group" : {
                "_id" : None,
                "booking" : self.getGroupObjBooking(), 
                "base_list" : self.getGroupObjBaseList() 
            }
        }
        return jsonObj

    def groupBookingByHistory(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_year_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByQoQ(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_quarter_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByVertical(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_vertical_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByCustomer(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_customerName_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByPartner(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_partnerName_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj
    
    def groupBookingBySL6(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_sl6_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByProductService(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_prodSer_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingByQuarters(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_quarter_asGroup,
                "booking" : self.getGroupObjBooking() 
            }
        }
        return jsonObj

    def groupBookingNetAndListByArchs(self):
        jsonObj = {
             "$group" : {
                "_id" : self.field_arch2_asGroup,
                "booking" : self.getGroupObjBooking(), 
                "base_list" : self.getGroupObjBaseList(), 
            }
        }
        return jsonObj

    
    def matchByMultipleParams(self, fiscal_year=None, quarter=None, fiscal_month=None, fiscal_week=None, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        jsonObj = {}
        if fiscal_year is not None:
            if quarter is not None:
                if fiscal_month is not None:
                    if fiscal_week is not None:
                        jsonObj = {
                            "$match" : {
                                self.field_year : fiscal_year,
                                self.field_quarter: quarter,
                                self.field_month: fiscal_month,
                                self.field_week: fiscal_week,
                            }
                        }
                    else:
                        jsonObj = {
                            "$match" : {
                                self.field_year : fiscal_year,
                                self.field_quarter: quarter,
                                self.field_month: fiscal_month
                            }
                        }
                else:
                    jsonObj = {
                        "$match" : {
                            self.field_year : fiscal_year,
                            self.field_quarter: quarter
                        }
                    }
            else:
                jsonObj.update({
                    "$match" : {self.field_year : fiscal_year}
                })
        elif quarter is not None:
            if fiscal_month is not None:
                if fiscal_week is not None:
                    jsonObj = {
                        "$match" : {
                            self.field_quarter: quarter,
                            self.field_month: fiscal_month,
                            self.field_week: fiscal_week,
                        }
                    }
                else:
                    jsonObj = {
                        "$match" : {
                            self.field_quarter: quarter,
                            self.field_month: fiscal_month
                        }
                    }
            else:
                jsonObj = {
                    "$match" : {
                        self.field_quarter: quarter
                    }
                }
        elif fiscal_month is not None:
            if fiscal_week is not None:
                jsonObj = {
                    "$match" : {
                        self.field_month: fiscal_month,
                        self.field_week: fiscal_week,
                    }
                }
            else:
                jsonObj = {
                    "$match" : {
                        self.field_month: fiscal_month
                    }
                }
        elif fiscal_week is not None:
            jsonObj = {
                "$match" : {
                    self.field_week: fiscal_week,
                }
            }
        else:
            jsonObj = None

        # Check if the Periods are updated in the Match Object.
        # Accordingly, update the other Match Criteria
        #print(jsonObj)
        jsonObj = self.matchByMultipleAnnexure(jsonObj, scms=scms, sub_scms=sub_scms, gtmu=gtmu, region=region, sl6=sl6, sales_agent=sales_agent, partner_name=partner_name, customer_name=customer_name)
        #print(jsonObj)
        return jsonObj
    
    # =================================================
    
    def matchByMultipleAnnexure(self, obj, scms=None, sub_scms=None, gtmu=None, region=None, sl6=None, sales_agent=None, partner_name=None, customer_name=None):
        if bool(obj):
            #print(obj)
            if scms is not None:
                if sub_scms is not None:
                    if gtmu is not None:
                        if region is not None:
                            if sl6 is not None:
                                if sales_agent is not None:
                                    if partner_name is not None:
                                        if customer_name is not None:
                                            obj['$match'].update({
                                                    self.field_scms : scms,
                                                    self.field_subscms: sub_scms,
                                                    self.field_gtmu: gtmu,
                                                    self.field_region: region,
                                                    self.field_sl6: sl6,
                                                    self.field_salesAgent: sales_agent,
                                                    self.field_partnerName: partner_name,
                                                    self.field_customerName: customer_name,
                                            })
                                        else:
                                            obj['$match'].update({
                                                    self.field_scms : scms,
                                                    self.field_subscms: sub_scms,
                                                    self.field_gtmu: gtmu,
                                                    self.field_region: region,
                                                    self.field_sl6: sl6,
                                                    self.field_salesAgent: sales_agent,
                                                    self.field_partnerName: partner_name,
                                            })
                                    else:
                                        obj['$match'].update({
                                                self.field_scms : scms,
                                                self.field_subscms: sub_scms,
                                                self.field_gtmu: gtmu,
                                                self.field_region: region,
                                                self.field_sl6: sl6,
                                                self.field_salesAgent: sales_agent,
                                        })
                                else:
                                    obj['$match'].update({
                                            self.field_scms : scms,
                                            self.field_subscms: sub_scms,
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                    })
                            else:           
                                obj['$match'].update({
                                        self.field_scms : scms,
                                        self.field_subscms: sub_scms,
                                        self.field_gtmu: gtmu,
                                        self.field_region: region,
                                })
                        else:
                            obj['$match'].update({
                                    self.field_scms : scms,
                                    self.field_subscms: sub_scms,
                                    self.field_gtmu: gtmu,
                            })
                    else:
                        obj['$match'].update({
                                self.field_scms : scms,
                                self.field_subscms: sub_scms,
                        })
                else:
                    obj['$match'].update({
                            self.field_scms : scms,
                    })
            elif sub_scms is not None:
                if gtmu is not None:
                    if region is not None:
                        if sl6 is not None:
                            if sales_agent is not None:
                                if partner_name is not None:
                                    if customer_name is not None:
                                        obj['$match'].update({
                                                self.field_subscms: sub_scms,
                                                self.field_gtmu: gtmu,
                                                self.field_region: region,
                                                self.field_sl6: sl6,
                                                self.field_salesAgent: sales_agent,
                                                self.field_partnerName: partner_name,
                                                self.field_customerName: customer_name,
                                        })
                                    else:
                                        obj['$match'].update({
                                                self.field_subscms: sub_scms,
                                                self.field_gtmu: gtmu,
                                                self.field_region: region,
                                                self.field_sl6: sl6,
                                                self.field_salesAgent: sales_agent,
                                                self.field_partnerName: partner_name,
                                        })
                                else:
                                    obj['$match'].update({
                                            self.field_subscms: sub_scms,
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                            self.field_salesAgent: sales_agent,
                                    })
                            else:
                                obj['$match'].update({
                                        self.field_subscms: sub_scms,
                                        self.field_gtmu: gtmu,
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                })
                        else:           
                            obj['$match'].update({
                                    self.field_subscms: sub_scms,
                                    self.field_gtmu: gtmu,
                                    self.field_region: region,
                            })
                    else:
                        obj['$match'].update({
                                self.field_subscms: sub_scms,
                                self.field_gtmu: gtmu,
                        })
                else:
                    print('It is inside the correct condition!')
                    obj['$match'].update({
                            self.field_subscms: sub_scms,
                    })
            elif gtmu is not None:
                if region is not None:
                    if sl6 is not None:
                        if sales_agent is not None:
                            if partner_name is not None:
                                if customer_name is not None:
                                    obj['$match'].update({
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                            self.field_salesAgent: sales_agent,
                                            self.field_partnerName: partner_name,
                                            self.field_customerName: customer_name,
                                    })
                                else:
                                    obj['$match'].update({
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                            self.field_salesAgent: sales_agent,
                                            self.field_partnerName: partner_name,
                                    })
                            else:
                                obj['$match'].update({
                                        self.field_gtmu: gtmu,
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                        self.field_salesAgent: sales_agent,
                                })
                        else:
                            obj['$match'].update({
                                    self.field_gtmu: gtmu,
                                    self.field_region: region,
                                    self.field_sl6: sl6,
                            })
                    else:           
                        obj['$match'].update({
                                self.field_gtmu: gtmu,
                                self.field_region: region,
                        })
                else:
                    obj['$match'].update({
                            self.field_gtmu: gtmu,
                    })
            elif region is not None:
                if sl6 is not None:
                    if sales_agent is not None:
                        if partner_name is not None:
                            if customer_name is not None:
                                obj['$match'].update({
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                        self.field_salesAgent: sales_agent,
                                        self.field_partnerName: partner_name,
                                        self.field_customerName: customer_name,
                                })
                            else:
                                obj['$match'].update({
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                        self.field_salesAgent: sales_agent,
                                        self.field_partnerName: partner_name,
                                })
                        else:
                            obj['$match'].update({
                                    self.field_region: region,
                                    self.field_sl6: sl6,
                                    self.field_salesAgent: sales_agent,
                            })
                    else:
                        obj['$match'].update({
                                self.field_region: region,
                                self.field_sl6: sl6,
                        })
                else:           
                    obj['$match'].update({
                            self.field_region: region,
                    })
            elif sl6 is not None:
                if sales_agent is not None:
                    if partner_name is not None:
                        if customer_name is not None:
                            obj['$match'].update({
                                    self.field_sl6: sl6,
                                    self.field_salesAgent: sales_agent,
                                    self.field_partnerName: partner_name,
                                    self.field_customerName: customer_name,
                            })
                        else:
                            obj['$match'].update({
                                    self.field_sl6: sl6,
                                    self.field_salesAgent: sales_agent,
                                    self.field_partnerName: partner_name,
                            })
                    else:
                        obj['$match'].update({
                                self.field_sl6: sl6,
                                self.field_salesAgent: sales_agent,
                        })
                else:
                    obj['$match'].update({
                            self.field_sl6: sl6,
                    })
            elif sales_agent is not None:
                if partner_name is not None:
                    if customer_name is not None:
                        obj['$match'].update({
                                self.field_salesAgent: sales_agent,
                                self.field_partnerName: partner_name,
                                self.field_customerName: customer_name,
                        })
                    else:
                        obj['$match'].update({
                                self.field_salesAgent: sales_agent,
                                self.field_partnerName: partner_name,
                        })
                else:
                    obj['$match'].update({
                            self.field_salesAgent: sales_agent,
                    })
            elif partner_name is not None:
                if customer_name is not None:
                    obj['$match'].update({
                            self.field_partnerName: partner_name,
                            self.field_customerName: customer_name,
                    })
                else:
                    obj['$match'].update({
                            self.field_partnerName: partner_name,
                    })
            elif customer_name is not None:
                obj['$match'].update({
                        self.field_customerName: customer_name,
                })
            else:
                obj['$match'].update({})
        else:
            obj = {}
            if scms is not None:
                if sub_scms is not None:
                    if gtmu is not None:
                        if region is not None:
                            if sl6 is not None:
                                if sales_agent is not None:
                                    if partner_name is not None:
                                        if customer_name is not None:
                                            obj = {
                                                '$match' : {
                                                    self.field_scms : scms,
                                                    self.field_subscms: sub_scms,
                                                    self.field_gtmu: gtmu,
                                                    self.field_region: region,
                                                    self.field_sl6: sl6,
                                                    self.field_salesAgent: sales_agent,
                                                    self.field_partnerName: partner_name,
                                                    self.field_customerName: customer_name,
                                                } 
                                            }
                                        else:
                                            obj = {
                                                '$match' : {
                                                    self.field_scms : scms,
                                                    self.field_subscms: sub_scms,
                                                    self.field_gtmu: gtmu,
                                                    self.field_region: region,
                                                    self.field_sl6: sl6,
                                                    self.field_salesAgent: sales_agent,
                                                    self.field_partnerName: partner_name,
                                                } 
                                            }
                                    else:
                                        obj = {
                                            '$match' : {
                                                self.field_scms : scms,
                                                self.field_subscms: sub_scms,
                                                self.field_gtmu: gtmu,
                                                self.field_region: region,
                                                self.field_sl6: sl6,
                                                self.field_salesAgent: sales_agent,
                                            } 
                                        }
                                else:
                                    obj = {
                                        '$match' : {
                                            self.field_scms : scms,
                                            self.field_subscms: sub_scms,
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                        } 
                                    }
                            else:           
                                obj = {
                                    '$match' : {
                                        self.field_scms : scms,
                                        self.field_subscms: sub_scms,
                                        self.field_gtmu: gtmu,
                                        self.field_region: region,
                                    } 
                                }
                        else:
                            obj = {
                                '$match' : {
                                    self.field_scms : scms,
                                    self.field_subscms: sub_scms,
                                    self.field_gtmu: gtmu,
                                } 
                            }
                    else:
                        obj = {
                            '$match' : {
                                self.field_scms : scms,
                                self.field_subscms: sub_scms,
                            } 
                        }
                else:
                    obj = {
                        '$match' : {
                            self.field_scms : scms,
                        } 
                    }
            elif sub_scms is not None:
                if gtmu is not None:
                    if region is not None:
                        if sl6 is not None:
                            if sales_agent is not None:
                                if partner_name is not None:
                                    if customer_name is not None:
                                        obj = {
                                            '$match' : {
                                                self.field_subscms: sub_scms,
                                                self.field_gtmu: gtmu,
                                                self.field_region: region,
                                                self.field_sl6: sl6,
                                                self.field_salesAgent: sales_agent,
                                                self.field_partnerName: partner_name,
                                                self.field_customerName: customer_name,
                                            } 
                                        }
                                    else:
                                        obj = {
                                            '$match' : {
                                                self.field_subscms: sub_scms,
                                                self.field_gtmu: gtmu,
                                                self.field_region: region,
                                                self.field_sl6: sl6,
                                                self.field_salesAgent: sales_agent,
                                                self.field_partnerName: partner_name,
                                            } 
                                        }
                                else:
                                    obj = {
                                        '$match' : {
                                            self.field_subscms: sub_scms,
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                            self.field_salesAgent: sales_agent,
                                        } 
                                    }
                            else:
                                obj = {
                                    '$match' : {
                                        self.field_subscms: sub_scms,
                                        self.field_gtmu: gtmu,
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                    } 
                                }
                        else:           
                            obj = {
                                '$match' : {
                                    self.field_subscms: sub_scms,
                                    self.field_gtmu: gtmu,
                                    self.field_region: region,
                                } 
                            }
                    else:
                        obj = {
                            '$match' : {
                                self.field_subscms: sub_scms,
                                self.field_gtmu: gtmu,
                            } 
                        }
                else:
                    obj = {
                        '$match' : {
                            self.field_subscms: sub_scms,
                        } 
                    }
            elif gtmu is not None:
                if region is not None:
                    if sl6 is not None:
                        if sales_agent is not None:
                            if partner_name is not None:
                                if customer_name is not None:
                                    obj = {
                                        '$match' : {
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                            self.field_salesAgent: sales_agent,
                                            self.field_partnerName: partner_name,
                                            self.field_customerName: customer_name,
                                        } 
                                    }
                                else:
                                    obj = {
                                        '$match' : {
                                            self.field_gtmu: gtmu,
                                            self.field_region: region,
                                            self.field_sl6: sl6,
                                            self.field_salesAgent: sales_agent,
                                            self.field_partnerName: partner_name,
                                        } 
                                    }
                            else:
                                obj = {
                                    '$match' : {
                                        self.field_gtmu: gtmu,
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                        self.field_salesAgent: sales_agent,
                                    } 
                                }
                        else:
                            obj = {
                                '$match' : {
                                    self.field_gtmu: gtmu,
                                    self.field_region: region,
                                    self.field_sl6: sl6,
                                } 
                            }
                    else:           
                        obj = {
                            '$match' : {
                                self.field_gtmu: gtmu,
                                self.field_region: region,
                            } 
                        }
                else:
                    obj = {
                        '$match' : {
                            self.field_gtmu: gtmu,
                        } 
                    }
            elif region is not None:
                if sl6 is not None:
                    if sales_agent is not None:
                        if partner_name is not None:
                            if customer_name is not None:
                                obj = {
                                    '$match' : {
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                        self.field_salesAgent: sales_agent,
                                        self.field_partnerName: partner_name,
                                        self.field_customerName: customer_name,
                                    } 
                                }
                            else:
                                obj = {
                                    '$match' : {
                                        self.field_region: region,
                                        self.field_sl6: sl6,
                                        self.field_salesAgent: sales_agent,
                                        self.field_partnerName: partner_name,
                                    } 
                                }
                        else:
                            obj = {
                                '$match' : {
                                    self.field_region: region,
                                    self.field_sl6: sl6,
                                    self.field_salesAgent: sales_agent,
                                } 
                            }
                    else:
                        obj = {
                            '$match' : {
                                self.field_region: region,
                                self.field_sl6: sl6,
                            } 
                        }
                else:           
                    obj = {
                        '$match' : {
                            self.field_region: region,
                        } 
                    }
            elif sl6 is not None:
                if sales_agent is not None:
                    if partner_name is not None:
                        if customer_name is not None:
                            obj = {
                                '$match' : {
                                    self.field_sl6: sl6,
                                    self.field_salesAgent: sales_agent,
                                    self.field_partnerName: partner_name,
                                    self.field_customerName: customer_name,
                                } 
                            }
                        else:
                            obj = {
                                '$match' : {
                                    self.field_sl6: sl6,
                                    self.field_salesAgent: sales_agent,
                                    self.field_partnerName: partner_name,
                                } 
                            }
                    else:
                        obj = {
                            '$match' : {
                                self.field_sl6: sl6,
                                self.field_salesAgent: sales_agent,
                            } 
                        }
                else:
                    obj = {
                        '$match' : {
                            self.field_sl6: sl6,
                        } 
                    }
            elif sales_agent is not None:
                if partner_name is not None:
                    if customer_name is not None:
                        obj = {
                            '$match' : {
                                self.field_salesAgent: sales_agent,
                                self.field_partnerName: partner_name,
                                self.field_customerName: customer_name,
                            } 
                        }
                    else:
                        obj = {
                            '$match' : {
                                self.field_salesAgent: sales_agent,
                                self.field_partnerName: partner_name,
                            } 
                        }
                else:
                    obj = {
                        '$match' : {
                            self.field_salesAgent: sales_agent,
                        } 
                    }
            elif partner_name is not None:
                if customer_name is not None:
                    obj = {
                        '$match' : {
                            self.field_partnerName: partner_name,
                            self.field_customerName: customer_name,
                        } 
                    }
                else:
                    obj = {
                        '$match' : {
                            self.field_partnerName: partner_name,
                        } 
                    }
            elif customer_name is not None:
                obj = {
                    '$match' : {
                        self.field_customerName: customer_name,
                    } 
                }
            else:
                obj = {}
            
        return obj
        
