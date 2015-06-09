# -*- coding: utf-8 -*-
from dataapi import Client
from datetime import date
from datetime import timedelta
import json
import csv
import code

if __name__ == "__main__":
    try:
        client = Client()
        
        ticker = '601988' # ZGYH
        lookBack = 60
        today = date.today()
        endDate = today.strftime('%Y%m%d')
        beginDate = (today - timedelta(days=lookBack)).strftime('%Y%m%d')
        exchangeCD = "XSHG"
        
        code, mktResult = client.getMarketDataByTicker(ticker, beginDate, endDate)
        if code==200:
            mktResult = unicode(mktResult, errors='ignore')
            decodedRes = json.loads(mktResult)
            
            mktFile = csv.writer(open("601988_mkt.csv", "wb+"))

            mktFile.writerow(decodedRes['data'][0].keys())
            for row in decodedRes['data']:
                mktFile.writerow(row.values())
        else:
            print code
            print mktResult
            
        # get news data
        code, result = client.getNewsByTicker(ticker, beginDate, endDate, exchangeCD)
        if code==200:
            result = unicode(result, errors='ignore')
            decodedRes = json.loads(result)
            
            file = csv.writer(open("601988_news.csv", "wb+"))

            file.writerow(decodedRes['data'][0].keys())
            for row in decodedRes['data']:
                file.writerow(row.values())
        else:
            print code
            print result
    except Exception, e:
        raise e
    

