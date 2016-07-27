import json, ast
import datetime
import tornado

class Helper():
    
    def stringToList(self, stringifiedList):
        for stringInList in stringifiedList:
            return stringInList.split(',')

    def specialCharToComma(self, arrayList):
        freshList = []
        for element in arrayList:
            element = element.replace("_|", ",")
            freshList.append(element)
        return freshList
    
    @tornado.gen.coroutine
    def calculateDiscount(self, booking_net, booking_list):
        discount = 0.0
        if booking_list == 0:
            discount = 0.0
        else:
            discount = 1-(booking_net/booking_list)
        
        raise tornado.gen.Return(discount)

    @tornado.gen.coroutine
    def calculateRatio(self, numero, dino):
        numero = float(numero)
        dino = float(dino)
        ratio = 0
        if dino == 0:
            ratio = 0
        else:
            ratio = numero/dino
        ratio = float(ratio)
        raise tornado.gen.Return(ratio)


    def unicodeObjAsStrings(self, obj):
        if isinstance(obj, dict):
            print "yes it is dict"
            return {self.unicodeObjAsStrings(key):self.unicodeObjAsStrings(value) for (key, value) in obj.items()}
        elif isinstance(obj, list):
            print "No it is list"
            return [self.unicodeObjAsStrings(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj

    def uniDictToStringDict(self, obj):
        dthandler = lambda obj2: (
            obj2.isoformat()
            if isinstance(obj2, datetime.datetime)
            or isinstance(obj2, datetime.datetime.date())
            else None
        )
        return ast.literal_eval(json.dumps(obj, default=dthandler))


