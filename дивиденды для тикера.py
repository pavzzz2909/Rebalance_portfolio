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
from TICKs import *

# допилить проверку актуальности дивидендов
# допилить функцию новые дивиденды отправка сообщения всем пользователям

filename = "data/TICKs.csv"
header = ("secid", "isin", "registryclosedate", "value", "currencyid","shortname")

###############################################################################

def seychas(): # создаем переменную СЕГОДНЯ
    #print("------------------------------------------------")
    #print("Применяем функцию seychas()")
    #print("Описание функции: создает и возвращает переменную СЕГОДНЯ")
    now = datetime.datetime.now()
    Ynow = str(now.year)
    Mnow  = str(now.month)
    Dnow = str(now.day)
    Datenow =Ynow+"-"+Mnow+"-"+Dnow
    Datedays = now.year*365+now.month*365/12+now.day
    return Datedays
    #                                       ПЕРЕМЕННАЯ СЕГОДНЯ СОЗДАНА



###############################################################################

def dividents_sozdanie_files(a, header, c): # функция для создания файла с дивидендами
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_sozdanie_files(a, header, c)")
    #print("Описание функции: создание файла с дивидендами по одному тикеру")
    with open (c, "w", newline = "") as csvfile:
        movies = csv.writer(csvfile)
        movies.writerow(header)
        for x in a:
            movies.writerow(x)

def dividents_parse(): # функция парсинга ММВБ создание списка дивидендов с использованием функции создания файлов
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_parse()")
    #print("Описание функции: парсинг ММВБ и запуск функции на создание всех файлов с дивидендами")
    TICKs = ticks_only_load(filename)
    count=1
    for TICK in TICKs:
        filename2 = "data/dividents/"+TICK[0]+".csv"
        shortname = TICK[1]
        soup = []
        URL = "http://iss.moex.com/iss/securities/"+TICK[0]+"/dividends.xml"
        r = requests.get(URL)
        soup = bs(r.text, "html.parser")
        dividents = soup.find_all('row')
        dividentscheck = list(dividents)
        if (len(dividentscheck) == 0):
            continue
        else:
            count +=1
            data=[]
            for divident in dividents:
                secid = divident.get('secid')
                isin = divident.get('isin')
                registryclosedate = divident.get('registryclosedate')
                value = divident.get('value')
                currencyid = divident.get('currencyid')
                val = (secid,isin,registryclosedate,value,currencyid,shortname)
                data.append(val)
            dividents_sozdanie_files(data, header, filename2)
    print("СОЗДАНИЕ ФАЙЛОВ С ДИВИДЕНДАМИ ЗАВЕРШЕНО")

def dividents_v_soobshenie(a): # выбрали предстоящие дивиденды сформировали в список
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_v_soobshenie()")
    #print("Описание функции: производит выборку из всех дивидендов за все периоды по условию больше чем сегодня")
    TICKs = ticks_only_load(filename)

    Datedays = seychas()
    values = []
    for divident in a:
        #print(divident)
        if (type(divident) == list):
            for div in divident:
                #print(div)
                secid = div[0]
                isin = div[1]
                registryclosedate = div[2]
                registryclosedate = registryclosedate.split("-")
                datepay = int(registryclosedate[0])*365+int(registryclosedate[1])*365/12+int(registryclosedate[2])
                datepay = int(datepay)
                registryclosedate = registryclosedate[2]+"."+registryclosedate[1]+"."+registryclosedate[0]
                value = div[3]
                currencyid = div[4]
                shortname = div[5]
                if datepay>Datedays:
                    val = "* "+shortname+" #"+secid+",\n дата закрытия реестра: "+registryclosedate+",\n сумма дивидендов на 1 акцию "+value+" "+currencyid
                    #val = shortname+" "+secid+" "+isin+" "+registryclosedate+" "+value+" "+currencyid
                    values.append(val)
    return values

def dividents_only_load(): # функция загрузки имеющегося в csv файлах списка всех дивидендов за все периоды
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_only_load()")
    #print("Описание функции: исполняет функцию dividents_proverka_files(filename2) для всех тикеров, возвращает список со всеми дивидендами")
    all_div = []
    TICKs = ticks_only_load(filename)
    for TICK in TICKs:
        filename2 = "data/dividents/"+TICK[0]+".csv"
        dividents_proverka_files(filename2)
        div = dividents_proverka_files(filename2)
        all_div.append(div)
    #print(all_div)
    return all_div

def dividents_proverka_files(c): # функция
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_proverka_files(c)")
    #print("Описание функции: проверяет наличие файла csv возвращает весь список дивидендов по одному тикеру")
    try:
        if os.stat(c).st_size > 0:
            spisok_dividents = []
            with open(c) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = row[0],row[1],row[2],row[3],row[4],row[5]
                        spisok_dividents.append(cid)
                        line_count += 1
                return spisok_dividents
    except FileNotFoundError:
        k =0

def dividents_only_parse(): # функция парсинга ММВБ
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_only_parse()")
    #print("Описание функции: парсинг ММВБ ")
    TICKs = ticks_only_load(filename)
    count=1
    dividents_all = []
    for TICK in TICKs:
        shortname = TICK[1]
        soup = []
        URL = "http://iss.moex.com/iss/securities/"+TICK[0]+"/dividends.xml"
        r = requests.get(URL)
        soup = bs(r.text, "html.parser")
        dividents = soup.find_all('row')
        dividentscheck = list(dividents)
        if (len(dividentscheck) == 0):
            dividents_all.append(None)
            continue
        else:
            count +=1
            data=[]
            for divident in dividents:
                secid = divident.get('secid')
                isin = divident.get('isin')
                registryclosedate = divident.get('registryclosedate')
                value = divident.get('value')
                currencyid = divident.get('currencyid')
                val = (secid,isin,registryclosedate,value,currencyid,shortname)
                data.append(val)
            dividents_all.append(data)
    return dividents_all

def dividents_new(): # функция обновления элементов в списке дивидендов по акциям
    #print("------------------------------------------------")
    #print("Применяем функцию dividents_new(filename)")
    #print("Описание функции: ")
    spisok_new = dividents_only_parse()
    spisok_dividents = dividents_only_load()
    spisokNew =[]
    for new in spisok_new:
        if new != None : # убираем значения None
            for new1 in new:
                spisokNew.append(new1)
    #print(spisokNew)
    spisokdividents =[]
    for dividents in spisok_dividents:
        if dividents != None : # убираем значения None
            for dividents1 in dividents:
                spisokdividents.append(dividents1)
    #print(spisokdividents)
    new_dividents = []
    for name in spisokNew:
        if name not in spisokdividents:
            new_dividents.append (name)
    dlina = len(new_dividents)
    #print(new_dividents)
    if dlina != 0:
        return new_dividents




#print(dividents_new())
#print(dividents_parse()) # список после парсинга всех дивидендов
#print(dividents_only_load())# список всех дивидендов в файлах csv
#print(ticks_only_load(filename))
#dividents_filename()
#print(dividents_v_soobshenie())


#DIVIDENTs()
