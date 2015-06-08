# -*- coding: utf-8 -*-
import httplib
import traceback
import urllib
HTTP_OK = 200
HTTP_AUTHORIZATION_ERROR = 401
class Client:
    domain = 'api.wmcloud.com'
    port = 443
    token = ''
    httpClient = None
    def __init__( self ):
        self.httpClient = httplib.HTTPSConnection(self.domain, self.port)
    def __del__( self ):
        if self.httpClient is not None:
            self.httpClient.close()
    def encodepath(self, path):
        #转换参数的编码
        start=0
        n=len(path)
        re=''
        i=path.find('=',start)
        while i!=-1 :
            re+=path[start:i+1]
            start=i+1
            i=path.find('&',start)
            if(i>=0):
                for j in range(start,i):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]  
                re+='&'
                start=i+1
            else:
                for j in range(start,n):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]  
                start=n
            i=path.find('=',start)
        return re
    def init(self, token):
        self.token=token
    def getData(self, path):
        result = None
        path='/data'+path
        path=self.encodepath(path)
        print path
        try:
            #set http header here
            self.httpClient.request('GET', path, headers = {"Authorization": "Bearer " + self.token})
            #make request
            response = self.httpClient.getresponse()
            #read result
            if response.status == HTTP_OK:
                #parse json into python primitive object
                result = response.read()
            else:
                result = response.read()
            if(path.find('.csv?')==-1):
                result=result.decode('utf-8').encode('GB18030')
            return response.status, result
        except Exception, e:
            #traceback.print_exc()
            raise e
        return -1, result
    #获取csv头
    def getfields(self, json, pos):
        n=len(json)-1
        csv=''
        quotation=False
        isfield=True
        passonechar=False
        pos+=1
        for pos in range(pos,n):
            if(passonechar):
                passonechar=False
                continue
            if(isfield):
                if(json[pos]=='"'):
                    isfield=False
                    passonechar=True
                else:
                    csv+=json[pos]
            elif(quotation==False):
                if(json[pos]=='"'):
                    quotation=True
                if(json[pos]==','):
                    csv+=','
                    isfield=True;
                    passonechar=True
                if(json[pos]=='}' and (json[pos+1]=='}'or json[pos+1]==',')):
                    csv+='\n'
                    return csv
            else:
                if(json[pos]=='"'):
                    if(json[pos-1]!='\\'):
                        quotation=False
    #获取csv数据
    def jsondatatocsv(self, csv):
        json=csv
        n=len(json)-1;
        pos=json.find("data")
        if(pos==-1):
            return 
        pos+=8
        csv=self.getfields(json,pos)
        colon=False    #冒号
        quotation=False    #引号
        passonechar=False
        for pos in range(pos,n):
            if(passonechar):
                passonechar=False;
                continue
            if(colon==False):
                if(json[pos]==':'):
                    colon=True
                    if(json[pos+1]=='"'):
                        passonechar=True
                        csv+=json[pos+1]
                        quotation=True
            else:
                if(quotation):
                    if(json[pos]=='"' and json[pos-1]!='\\'):
                        csv+=json[pos]
                        quotation=False
                        passonechar=True
                        if(json[pos]=='}'):
                            csv+='\n'
                        else:
                            csv+=','
                        colon=False
                    else:
                        csv+=json[pos]
                else:
                    if(json[pos]==','):
                        csv+=','
                        colon=False
                    elif(json[pos]=='}'):
                        csv+='\n'
                        colon=False
                    else:
                        csv+=json[pos]
        return csv