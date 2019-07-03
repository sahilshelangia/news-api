import requests
from bs4 import BeautifulSoup as soup
import datetime as dt
import json
import os
import re
import csv
import time
import logging
import hashlib
import MySQLdb
import justext
import requests
import warnings
import feedparser
import urllib.parse
import pandas as pd
import urllib.request
from goose3 import Goose
# from boilerpipe.extract import Extractor

def getInitPage(to_date,from_date,commCode,comm):
    url='http://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity='+commCode+'&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom='+from_date+'&DateTo='+to_date+'&Fr_Date='+(from_date)+'&To_Date='+(to_date)+'&Tx_Trend=0&Tx_CommodityHead='+comm+'&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    print(url)
    res = requests.get(url)
    return res.content

def getInitPageTon(to_date,from_date,commCode,comm):
    url='http://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity='+commCode+'&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom='+from_date+'&DateTo='+to_date+'&Fr_Date='+(from_date)+'&To_Date='+(to_date)+'&Tx_Trend=2&Tx_CommodityHead='+comm+'&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    print(url)
    res = requests.get(url)
    return res.content

def getNextPage(date,vs):
    from_date = date
    to_date = date
    uri ='http://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=17&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom='+from_date+'&DateTo='+to_date+'&Fr_Date='+(from_date)+'&To_Date='+(to_date)+'&Tx_Trend=0&Tx_CommodityHead=Apple&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
    #the http headers are useful to simulate a particular browser (some sites deny
    #access to non-browsers (bots, etc.)
    #also needed to pass the content type. 
    url = uri
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Origin':'http://agmarknet.gov.in',
        'Referer':url,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-MicrosoftAjax':'Delta=true',
        'X-Requested-With':'XMLHttpRequest'
    }

    # we group the form fields and their values in a list (any
    # iterable, actually) of name-value tuples.  This helps
    # with clarity and also makes it easy to later encoding of them.

    formFields = (
       # the viewstate is actualy 800+ characters in length! I truncated it
       # for this sample code.  It can be lifted from the first page
       # obtained from the site.  It may be ok to hardcode this value, or
       # it may have to be refreshed each time / each day, by essentially
       # running an extra page request and parse, for this specific value.
       (r'__VIEWSTATE',vs),

       # following are more of these ASP form fields
       (r'ctl00$ScriptManager1', r'ctl00$cphBody$UpdatePanel1|ctl00$cphBody$GridPriceData'),
        (r'ctl00$ddlLanguages',r'en'),
        (r'ctl00$ddlArrivalPrice',r'0'),
        (r'ctl00$ddlCommodity',r'17'),
        (r'ctl00$ddlState',r'0'),
        (r'ctl00$ddlDistrict',r'0'),
        (r'ctl00$ddlMarket',r'0'),
        (r'ctl00$txtDate',from_date),
        (r'ctl00$ValidatorExtender1_ClientState',to_date),
        (r'ctl00$ValidatorCalloutExtender2_ClientState',r''),
        (r'ctl00$cphBody$DDLPirceMearure',r'0'),
        (r'ctl00$cphBody$DDlExpression',r'0'),
        (r'ctl00$cphBody$Textserach',r''),
        (r'ctl00$cphBody$ddlCommodity',r'17'),
        (r'ctl00$cphBody$ddlfromyear',from_date[-4:]),
        (r'ctl00$cphBody$ddltoyear',to_date[-4:]),
        (r'ctl00$cphBody$DropDownDisplay',r'0'),
        (r'__EVENTTARGET',r'ctl00$cphBody$GridPriceData'),
        (r'__EVENTARGUMENT',r'Page$Next'),
        (r'__LASTFOCUS',r''),
        (r'__VIEWSTATEGENERATOR',r'B5EE7E14'),
        (r'__VIEWSTATEENCRYPTED',r''),
        (r'__ASYNCPOST',r'true')
    )

    formDict = {}
    for a,b in formFields:
        formDict[a] = b

    session = requests.Session()
    resp = session.post(uri,headers=headers,data=formDict)
    session.close()
    return resp.content


def populateDF(sp,df):
    nrows = df.shape[0]
    print("rows:",nrows)
    tr_temp=sp.findAll("tr")
    print("len: ",len(tr_temp))
    for i,tr in enumerate(tr_temp[1:]):
        coli = []
        for ival,td in enumerate(tr.find_all('td')):
            val = td.getText().strip()
            if ival == 9:
                val = val.replace(" ","-")
            coli.append(val)
        if len(coli) == 10:
            df.loc[i+nrows] = coli
            
def send(l):
    uri = 'http://www.agriiprince.com/test/aditya/loop_cron.php'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    formDict = {}
    formDict['values'] = json.dumps(l)
    formDict['rofl'] = 'Xz6mUMy4pFgMamyBu8hkWuq'

    session = requests.Session()
    resp = session.post(uri,headers=headers,data=formDict)
    session.close()
    print("Done")

    
def popLis(sp,lis):
    tr_temp=sp.findAll("tr")
    k=0
    for i,tr in enumerate(tr_temp[1:]):
        coli = []
        for ival,td in enumerate(tr.find_all('td')[1:]):
            val = td.getText().strip()
            if ival == 8:
                val = dt.datetime.strptime(val,"%d %b %Y").strftime('%Y-%m-%d')
            coli.append(val)
        print(k)
        k=k+1
        if len(coli) == 9:
            print(coli)
            query = """INSERT INTO main2 VALUES('{date}','{district}','{market}','{commodity}','{variety}','{grade}',NULL,{minP},{maxP},{modP},NULL) ON DUPLICATE KEY UPDATE grade = '{grade}';""".format(date = coli[8],district = coli[0],market = coli[1],commodity = coli[2],variety = coli[3],grade=coli[4]
                      , minP = coli[5],maxP = coli[6],modP = coli[7])
            lis.append(query)
            print("done")
            
            
def popLisTon(sp,lis,commInp):
    tr_temp=sp.findAll("tr")
    print("vnjudrsio")
    k=0
    for i,tr in enumerate(tr_temp[1:]):
        coli = []
        tds = tr.find_all('td')
        if tds[0].getText().strip() == '-':
            continue
        print(tds)
        for ival,td in enumerate(tds):
            val = td.getText().strip()
            if ival == 9:
                val = dt.datetime.strptime(val,"%d %b %Y").strftime('%Y-%m-%d')
            coli.append(val)
        #print(coli)
        if len(coli) == 10:
            print(coli)
            print(k)
            k=k-1
            query = """INSERT INTO main2 VALUES('{date}','{district}','{market}','{commodity}','{variety}',NULL,'{state}',{minP},{maxP},{modP},{tonnage}) ON DUPLICATE KEY UPDATE tonnage = {tonnage}, state = '{state}';""".format(date = coli[9],district = coli[1],market = coli[2],commodity = commInp,variety = coli[3]
                      , minP = coli[6],maxP = coli[7],modP = coli[8],tonnage = coli[5],state = coli[0])
            #cursor.execute(query)
            lis.append(query)
            print("inserted")

def findViewState(respContent):
    st = respContent.find('VIEWSTATE') + 10
    end = respContent[st:].find('|')
    return respContent[st:][:end]
