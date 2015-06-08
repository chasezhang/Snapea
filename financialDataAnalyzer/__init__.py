# -*- coding: utf-8 -*-
from dataapi import Client
import json
import csv

if __name__ == "__main__":
    try:
        client = Client()
        client.init('83fa105b3c49a4cfecdb7000cac6fbb80cca8618a8e9b17dc92905a767771040')
        marketData='/api/market/getMktEqud.json?field=&beginDate=20150506&endDate=20150606&secID=&ticker=600601&tradeDate='
        code, result = client.getData(marketData)
        if code==200:
            result = unicode(result, errors='ignore')
            decodedRes = json.loads(result)
            
            file = csv.writer(open("fzkj_mkt.csv", "wb+"))
            #file.writerow(["closePrice", "turnoverValue"
            #               "exchangeCD", "secID",
            #               "tradeDate", "marketValue",
            #               "turnoverRate", "highestPrice",
            #               "negMarketValue", "secShortName",
            #               "PE1", "PB",
            #               ""])
            file.writerow(decodedRes['data'][0].keys())
            for row in decodedRes['data']:
                file.writerow(row.values())
                print row
            #print result
        else:
            print code
            print result
    except Exception, e:
        #traceback.print_exc()
        raise e