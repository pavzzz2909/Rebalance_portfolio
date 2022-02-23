import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from lxml import html
import os
import xlwt
import datetime
import time
import random
import csv
import functools

#https://iss.moex.com/iss/engines/currency/markets/selt/securities.xml?iss.meta=off&iss.only=securities&securities.columns=SECID,OPEN,LOW,HIGH,LAST,WAPRICE

def currency_parse():
    soup = []
    spisok_currency = []
    URL ="https://iss.moex.com/iss/engines/currency/markets/selt/securities.xml?iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,OPEN,LOW,HIGH,LAST,WAPRICE,BOARDID"
    r = requests.get(URL)
    soup = bs(r.text, "html.parser")
    datas = soup.find_all('data')
    for data in datas:
        id_data = data.get('id')
        if id_data == "marketdata":
            dividents = data.find_all('row')
            #print(dividents)
            dividentscheck = list(dividents)
            kol = len(dividents)
            k = 0
            for currency in dividents:
                #print(currency)
                cid = []
                k+=1
                SECID = str(currency.get('secid'))
                OPEN = str(currency.get('open'))
                LOW = str(currency.get('low'))
                HIGH = str(currency.get('high'))
                LAST = str(currency.get('last')) # последняя цена
                WAPRICE = str(currency.get('waprice')) # средневзвешенная цена
                BOARDID = str(currency.get('boardid')) # средневзвешенная цена
                cid=(SECID,OPEN,LOW,HIGH,LAST,WAPRICE,BOARDID)
                #print(cid)
                spisok_currency.append(cid)
            return spisok_currency

def kursi():
    soob_kursi =[]
    spisok_currency = currency_parse()
    for currency in spisok_currency:
        SECID = currency[0]
        OPEN = currency[1]
        LOW = currency[2]
        HIGH = currency[3]
        LAST = currency[4]
        WAPRICE = currency[5]
        BOARDID = currency[6]
        if SECID == "USD000000TOD" and BOARDID =="CETS":
            soob_kursi.append("Курс Доллара 🇺🇸 "+LAST+" рублей")
        if SECID == "EUR_RUB__TOD" and BOARDID =="CETS":
            soob_kursi.append("Курс Евро 🇪🇺 "+LAST+" рублей")
        if SECID == "EURUSD000TOD" and BOARDID =="CETS":
            soob_kursi.append("Разница 🇪🇺/🇺🇸 "+LAST)
    return soob_kursi

def dollar():
    soob_dol = []
    spisok_currency = currency_parse()
    for currency in spisok_currency:
        SECID = currency[0]
        OPEN = currency[1]
        LOW = currency[2]
        HIGH = currency[3]
        LAST = currency[4]
        WAPRICE = currency[5]
        BOARDID = currency[6]
        if SECID == "USD000000TOD" and BOARDID =="CETS":
            soob_dol.append("За последний торговый день:")
            soob_dol.append("Цена открытия "+OPEN)
            soob_dol.append("Максимальная цена "+HIGH)
            soob_dol.append("Минимальная цена "+LOW)
            soob_dol.append("Средневзвешенная цена "+WAPRICE)
            soob_dol.append("На текущий момент актуальная стоимость "+LAST)
    return soob_dol

def euro():
    soob_eur = []
    spisok_currency = currency_parse()
    for currency in spisok_currency:
        SECID = currency[0]
        OPEN = currency[1]
        LOW = currency[2]
        HIGH = currency[3]
        LAST = currency[4]
        WAPRICE = currency[5]
        BOARDID = currency[6]
        if SECID == "EUR_RUB__TOD" and BOARDID =="CETS":
            soob_eur.append("За последний торговый день:")
            soob_eur.append("Цена открытия "+OPEN)
            soob_eur.append("Максимальная цена "+HIGH)
            soob_eur.append("Минимальная цена "+LOW)
            soob_eur.append("Средневзвешенная цена "+WAPRICE)
            soob_eur.append("На текущий момент актуальная стоимость "+LAST)
    return soob_eur

def eur_dol():
    soob_uerdol = []
    spisok_currency = currency_parse()
    for currency in spisok_currency:
        SECID = currency[0]
        OPEN = currency[1]
        LOW = currency[2]
        HIGH = currency[3]
        LAST = currency[4]
        WAPRICE = currency[5]
        BOARDID = currency[6]
        if SECID == "EURUSD000TOD" and BOARDID =="CETS":
            soob_uerdol.append("За последний торговый день:")
            soob_uerdol.append("Цена открытия "+OPEN)
            soob_uerdol.append("Максимальная цена "+HIGH)
            soob_uerdol.append("Минимальная цена "+LOW)
            soob_uerdol.append("Средневзвешенная цена "+WAPRICE)
            soob_uerdol.append("На текущий момент актуальная стоимость "+LAST)
    return soob_uerdol

#currency_parse()
#cur = currency_parse()
#for c in cur:
#    print(c)
#dollar()
#print(dollar())
#print(euro())
#print(eur_dol())
