import time
import bs4
import requests
import lxml.html as lh
from bs4 import BeautifulSoup

yahoo_01 = [
            "cryptocurrencies",
            "currencies",
            "world-indices",
            "etfs",
            "commodities"
          ]

yahoo_60 = [
            "sector/ms_healthcare",
            "sector/ms_real_estate",
            "sector/ms_industrials",
            "sector/ms_energy",
            "sector/ms_technology",
            "sector/ms_basic_materials",
            "sector/ms_financial_services",
            "sector/ms_consumer_defensive",
            "sector/ms_consumer_cyclical",
            "sector/ms_communication_services",
            "sector/ms_utilities"
          ] 


def requestYahoo(date, page):

    url = "https://finance.yahoo.com/" + page
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    trackers = ["symbol", "name", "price"]

    page = requests.get(url, headers=headers)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr') 

    cols  = {}
    width = 0

    for t in tr_elements[0]:
        for tracker in trackers:
            if tracker in t.text_content().lower():
                cols[str(width)] = tracker          
        width+=1

    for x in range(1,len(tr_elements)):
        T=tr_elements[x]
        if len(T)!=width:
            
            # @todo 
            # hier moet ik op de hoogte worden gesteld

            break

        y=0
        value_dict = {}

        for t in T.iterchildren():

            if str(y) in cols.keys():
                value_dict[cols[str(y)]] = t.text_content()
            y+=1
        value_dict['date'] = date
        with open("data/yahoo_finance.txt", 'a') as tf:
            tf.write(str(value_dict) + "\n")
        



m_check = h_check = ""

while True:

    cur_m = time.strftime("%m/%d/%Y, %H:%M", time.localtime())
    if cur_m != m_check:
        m_check = cur_m

        for page in yahoo_01:

            requestYahoo(cur_m, page)

        cur_h = time.strftime("%m/%d/%Y, %H:00", time.localtime())
        if cur_h != h_check:
            h_check = cur_h

            for page in yahoo_60:

                requestYahoo(cur_h, page)

    time.sleep(2)