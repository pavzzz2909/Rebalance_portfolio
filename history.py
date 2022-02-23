import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from lxml import html
import os
import xlwt
import datetime
import time                             # импорт времени
import random                           # импорт рандома
from MOEX_TICKs import *
#from functools import reduce
from statistics import mean


header = ("tradedate","secid","shortname","numtrades","open","high","low","volume","close")
# файл создает csv файлы на каждую акцию с историей и проверяет наличие обновлений
# и добавляет новые данные
#

def datenow(): # создание переменной СЕГОДНЯ
    now = datetime.datetime.now()
    Ynow = str(now.year)
    Mnow  = str(now.month)
    Dnow = str(now.day)
    Datenow =Ynow+"-"+Mnow+"-"+Dnow
    Dpred = int(Dnow)
    Dpred = Dpred-1
    if Dpred == 0:
        Mpred = int(Mnow)
        Mpred = Mpred-1
        if Mpred == 0:
            Dpred = str(31)
            Mpred = str(12)
            #print(Mpred)
            Ypred = int(Ynow)
            Ypred = Ypred-1
            Ypred = str(Ypred)
            pred_date = Ypred+"-"+Mpred+"-"+Dpred
            #print(Ypred)
            return pred_date
        else:
            if Mpred==4 and Mpred==6 and Mpred==9 and Mpred==11:
                Dpred=30
            elif Mpred==2 and Ynow % 4 != 0:
                Dpred=28
            elif Mpred==2 and Ynow % 4 == 0:
                Dpred=29
            else:
                Dpred=31
            Dpred = str(Dpred)
            Mpred = str(Mpred)
            Ynow = str (Ynow)
            pred_date = Ynow+"-"+Mpred+"-"+Dpred
            return pred_date
    else:
        Dpred = str(Dpred)
        pred_date = Ynow+"-"+Mnow+"-"+Dpred
        return pred_date

def calendar(): # создание КАЛЕНДАРЯ для целей парсинга
    now = datetime.datetime.now()
    Datenow = datenow()
    Dates_his = []
    y=2013
    flag = False
    while y <= now.year:
        m=1
        while m <=12:
            i =1
            while i <= 31:
                y1 = str(y)
                m1 = str(m)
                i1 = str(i)
                Date_history = y1+"-"+m1+"-"+i1
                Dates_his.append(Date_history)
                #print(Date_history)
                if i==30 and m==4:
                    break
                if i==30 and m==6:
                    break
                if i==30 and m==9:
                    break
                if i==30 and m==11:
                    break
                if i==28 and m==2 and y % 4 != 0:
                    break
                if i==29 and m==2 and y % 4 == 0:
                    break
                if Date_history == Datenow:
                    flag = True
                    break
                i += 1
            if flag:
                break
            m+=1
        y+=1
    Dates_his.reverse()
    return Dates_his

######################
def history_cozdanie_files(a, header, c):# функция проверки наличия файла для пропуска даты
    with open (c, "w", newline = "") as csvfile:
        movies = csv.writer(csvfile)
        movies.writerow(header)
        for x in a:
            movies.writerow(x)

def history_parse_all(): # функция перехода по датам
    Dates_his = calendar()
    for Date_his in Dates_his:
        #print(Date_his)
        history_parse_one_day(Date_his)

def history_parse_one_day(date): # функция парсинга ММВБ создание списка истории цен
    TICKs = ticks_only_load(filename)
    filename2 = "data/history/dates/"+date+".csv"
    if os.path.isfile(filename2) != True:
        values = []
        count=1
        # TRADEDATE # tradedate # Торговая дата
        # SHORTNAME # secid # Короткое название
        # NUMTRADES # shortname # Количество сделок за день, штук
        # VOLUME    # numtrades # Объем сделок за день, штук ценных бумаг
        # OPEN      # opn # цена открытия
        # LOW       # low # минимальная цена
        # HIGH      # high # максимальная цена
        # CLOSE     # close # цена закрытия
        # итого нужны столбцы SECID,TRADEDATE,SHORTNAME,NUMTRADES,VOLUME,OPEN,LOW,HIGH,CLOSE
        day_history_prices = []
        soup = []
        starts = [0,100,200,300,400]
        for start in starts:
            URL = "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities.xml?iss.meta=off&iss.only=history&history.columns=SECID,TRADEDATE,SHORTNAME,NUMTRADES,VOLUME,OPEN,LOW,HIGH,CLOSE&start="+str(start)+"&date="+date
            #URL = "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities.xml?iss.meta=off&iss.only=history&history.columns=SECID,TRADEDATE,SHORTNAME,NUMTRADES,VOLUME,OPEN,LOW,HIGH,CLOSE&start="+start+"&date="+Date_his
            #print(URL)
            r = requests.get(URL)
            soup = bs(r.text, "html.parser")
            #print(soup)
            prices = soup.find_all('row')
            #print(prices)
            pricescheck = list(prices)
            #print(pricescheck)
            if (len(pricescheck) == 0):
                continue
            else:
                for price in prices:
                    tradedate = price.get('tradedate')
                    secid = price.get('secid')
                    shortname = price.get('shortname')
                    numtrades = price.get('numtrades')
                    opn = price.get('open')
                    low = price.get('low')
                    high = price.get('high')
                    volume = price.get('volume')
                    close = price.get('close')
                    for TICK in TICKs:
                        #print(TICK[0])
                        ticker = TICK[0]
                        if secid == ticker:
                            row = (tradedate,secid,shortname,numtrades,opn,high,low,volume,close)
                            #print(row)
                            day_history_prices.append(row)
                            break
        #print(day_history_prices)
        history_cozdanie_files(day_history_prices, header, filename2)
        #print(date," день завершен")
        #time.sleep(random.randrange(1, 2))
        return day_history_prices
    #else:
        #print(date," файл с указанным днем имеется")

#######################
def history_cozdanie_files_all_TICK(a, header, c):# функция проверки наличия файла для пропуска даты
    with open (c, "w", newline = "") as csvfile:
        movies = csv.writer(csvfile)
        movies.writerow(header)
        for x in a:
            movies.writerow(x)

def history_poisk_all_TICK(): # функция перехода по датам
    TICKs = ticks_only_load(filename)
    for TICK in TICKs:
        ticker = TICK[0]
        hystory_poisk_TICK(ticker)

def hystory_poisk_TICK(TICK): # открываем все файлы с датами ищем ТИКЕР
    Dates_his = calendar()
    filename3 = "data/history/TICKs/prices/"+TICK+".csv"
    spisok_hystory = []
    for Date_his in Dates_his:
        filename2 = "data/history/dates/"+Date_his+".csv"
        with open(filename2) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if row[1] == TICK:
                        if row[2] != None:
                            if row[3] != str(0):
                                if row[4] != "":
                                    if row[5] != "":
                                        if row[6] != "":
                                            if row[7] != str(0):
                                                if row[8] != "":
                                                    cid = row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]
                                                    spisok_hystory.append(cid)
                                                    line_count += 1
    history_cozdanie_files_all_TICK(spisok_hystory, header, filename3)
    #print(TICK," завершен")

#######################
def history_cozdanie_files_all_TICK_perc(a, header, c):# функция проверки наличия файла для пропуска даты
    with open (c, "w", newline = "") as csvfile:
        movies = csv.writer(csvfile)
        movies.writerow(header)
        for x in a:
            movies.writerow(x)

def history_poisk_all_TICK_perc(): # функция перехода по датам
    TICKs = ticks_only_load(filename)
    for TICK in TICKs:
        ticker = TICK[0]
        hystory_poisk_TICK_perc(ticker)

def hystory_poisk_TICK_perc(TICK): # открываем все файлы с датами ищем ТИКЕР
    Dates_his = calendar()
    filename2 = "data/history/TICKs/prices/"+TICK+".csv"
    filename3 = "data/history/TICKs/percents/all/"+TICK+".csv"
    spisok_hystory = []
    with open(filename2) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                spisok_hystory.append(cid)
                line_count += 1
    spisok = []
    i=0
    a = 1
    b = 2
    #print(len(spisok_hystory))
    for spis in spisok_hystory:
        if len(spisok_hystory) == 1 or len(spisok_hystory) == 2:
            break
        day1 = spisok_hystory[i][0]
        day1 = day1.split("-")
        day11 = datetime.date(int(day1[0]), int(day1[1]), int(day1[2]))
        day2 = spisok_hystory[a][0]
        day2 = day2.split("-")
        day21 = datetime.date(int(day2[0]), int(day2[1]), int(day2[2]))
        days = day11-day21
        days = int(days.days)
        numtrades = round((float(spisok_hystory[i][3])/float(spisok_hystory[a][3])-1)*100/days,2)
        open_perc = round((float(spisok_hystory[i][4])/float(spisok_hystory[a][4])-1)*100/days,2)
        high_perc = round((float(spisok_hystory[i][5])/float(spisok_hystory[a][5])-1)*100/days,2)
        low_perc = round((float(spisok_hystory[i][6])/float(spisok_hystory[a][6])-1)*100/days,2)
        volume_perc = round((float(spisok_hystory[i][7])/float(spisok_hystory[a][7])-1)*100/days,2)
        close_perc = round((float(spisok_hystory[i][8])/float(spisok_hystory[a][8])-1)*100/days,2)
        row = (spisok_hystory[i][0],spisok_hystory[i][1],spisok_hystory[i][2],numtrades,open_perc,high_perc,low_perc,volume_perc,close_perc)
        #print(i,a,row)
        a += 1
        i += 1
        b += 1
        spisok.append(row)
        if len(spisok_hystory)==b:
            break
    history_cozdanie_files_all_TICK_perc(spisok, header, filename3)
    #print(TICK," завершен")

#######################
#def average(list1):
#    (lambda a, b: a + b, list1)/len(list1)
#    print(avg)
#    return avg

def history_cozdanie_files_sred_pokazatel_TICKs(a, header, c):# функция проверки наличия файла для пропуска даты
    with open (c, "w", newline = "") as csvfile:
        movies = csv.writer(csvfile)
        movies.writerow(header)
        movies.writerow(a)

def history_poisk_sred_pokazatel_TICKs(): # функция перехода по датам
    TICKs = ticks_only_load(filename)
    for TICK in TICKs:
        ticker = TICK[0]
        hystory_poisk_sred_pokazatel_TICK(ticker)

def hystory_poisk_sred_pokazatel_TICK(TICK): # открываем все файлы с датами ищем ТИКЕР
    filename2 = "data/history/TICKs/percents/all/"+TICK+".csv"
    filename3 = "data/history/TICKs/percents/srednee/"+TICK+".csv"
    spisok_hystory = []
    with open(filename2) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                spisok_hystory.append(cid)
                line_count += 1
    spisok = []
    i = 0
    a = 1
    b = 2
    kol = len(spisok_hystory)-1
    #print(len(spisok_hystory))
    if len(spisok_hystory) > 1:
        for spis in spisok_hystory:
            if len(spisok_hystory) == 1 or len(spisok_hystory) == 2:
                break
            day1 = spisok_hystory[i][0]
            day1 = day1.split("-")
            day11 = datetime.date(int(day1[0]), int(day1[1]), int(day1[2]))
            day2 = spisok_hystory[kol][0]
            day2 = day2.split("-")
            day21 = datetime.date(int(day2[0]), int(day2[1]), int(day2[2]))
            days = day11-day21
            days = int(days.days)
            #print(days)

        i = 0
        a = 1
        b = 2
        numtrades_spisok = []
        for spis in spisok_hystory:
            numtrades = float(spisok_hystory[i][3])
            #print(i,a,row)
            a += 1
            i += 1
            b += 1
            numtrades_spisok.append(numtrades)
            if len(spisok_hystory)==b:
                break
        #print(numtrades_spisok)
        sum_numtrade = sum(numtrades_spisok)
        sr_numtrade = round(sum_numtrade/len(numtrades_spisok),2)
        #print(sr_numtrade)

        i = 0
        a = 1
        b = 2
        open_spisok = []
        for spis in spisok_hystory:
            open_perc = float(spisok_hystory[i][4])
            #print(i,a,row)
            a += 1
            i += 1
            b += 1
            open_spisok.append(open_perc)
            if len(spisok_hystory)==b:
                break
        #print(open_spisok)
        sum_open = sum(open_spisok)
        sr_open = round(sum_open/len(open_spisok),2)
        #print(sr_open)

        i=0
        a = 1
        b = 2
        high_spisok = []
        for spis in spisok_hystory:
            high_perc = float(spisok_hystory[i][5])
            #print(i,a,row)
            a += 1
            i += 1
            b += 1
            high_spisok.append(high_perc)
            if len(spisok_hystory)==b:
                break
        #print(high_spisok)
        sum_high = sum(high_spisok)
        sr_high = round(sum_high/len(high_spisok),2)
        #print(sr_high)

        i=0
        a = 1
        b = 2
        low_spisok = []
        for spis in spisok_hystory:
            low_perc = float(spisok_hystory[i][6])
            #print(i,a,row)
            a += 1
            i += 1
            b += 1
            low_spisok.append(low_perc)
            if len(spisok_hystory)==b:
                break
        #print(high_spisok)
        low_high = sum(low_spisok)
        sr_low = round(low_high/len(low_spisok),2)
        #print(sr_high)

        i=0
        a = 1
        b = 2
        volume_spisok = []
        for spis in spisok_hystory:
            volume_perc = float(spisok_hystory[i][7])
            #print(i,a,row)
            a += 1
            i += 1
            b += 1
            volume_spisok.append(volume_perc)
            if len(spisok_hystory)==b:
                break
        #print(high_spisok)
        volume_high = sum(volume_spisok)
        sr_volume = round(volume_high/len(volume_spisok),2)
        #print(sr_high)

        i=0
        a = 1
        b = 2
        close_spisok = []
        for spis in spisok_hystory:
            close_perc = float(spisok_hystory[i][8])
            #print(i,a,row)
            a += 1
            i += 1
            b += 1
            close_spisok.append(close_perc)
            if len(spisok_hystory)==b:
                break
        #print(high_spisok)
        close_high = sum(close_spisok)
        sr_close = round(close_high/len(close_spisok),2)
        #print(sr_high)

        row = (days,spisok_hystory[1][1],spisok_hystory[1][2],sr_numtrade,sr_open,sr_high,sr_low,sr_volume,sr_close)
        #print(row)
        history_cozdanie_files_sred_pokazatel_TICKs(row, header, filename3)
        #print(TICK," завершен")

################################
def spisok_max(a,c):
    maxim = 0
    maxim = float(maxim)
    max1 = []
    for number in a:
        number1 = float(number[c])
        if number1 > maxim:
            maxim = number1
            max1 = number
    return max1


def hystory_soobshenie_numtrade_top():
    TICKs = ticks_only_load(filename)
    spisok_hystory = []
    for TICK in TICKs:
        ticker = TICK[0]
        filename2 = "data/history/TICKs/percents/srednee/"+ticker+".csv"
        if os.path.isfile(filename2) == True:
            with open(filename2) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        spisok_hystory.append(cid)
                        line_count += 1
    #print(spisok_hystory)
    max1 = spisok_max(spisok_hystory,3)
    spisok_hystory.remove(max1)
    max2 = spisok_max(spisok_hystory,3)
    spisok_hystory.remove(max2)
    max3 = spisok_max(spisok_hystory,3)
    spisok_hystory.remove(max3)
    max4 = spisok_max(spisok_hystory,3)
    spisok_hystory.remove(max4)
    max5 = spisok_max(spisok_hystory,3)
    spisok_hystory.remove(max5)
    #print("Большие показатели ",max1,max2,max3,max4,max5)
    massiv = []
    massiv.append(max1)
    massiv.append(max2)
    massiv.append(max3)
    massiv.append(max4)
    massiv.append(max5)
    massiv2 = []
    for a1 in massiv:
        #print(a1)
        tradedate = a1[0]
        secid = a1[1]
        shortname = a1[2]
        numtrades = a1[3]
        opn = a1[4]
        high = a1[5]
        low = a1[6]
        volume =a1[7]
        close = a1[8]
        val = "* "+shortname+" #"+secid+",\nТоргуется на бирже "+tradedate+" дней,\nИзменение количества сделок в день"+numtrades+"%\nИзменение цены открытия в день "+opn+"%\nИзменение максимальной цены в день "+high+"%\nИзменение минимальной цены в день "+low+"%\nИзменение объёмов сделок в день "+volume+"%\nИзменение цены закрытия в день "+close
        massiv2.append(val)
    return massiv2

def hystory_soobshenie_open_top():
    TICKs = ticks_only_load(filename)
    spisok_hystory = []
    for TICK in TICKs:
        ticker = TICK[0]
        filename2 = "data/history/TICKs/percents/srednee/"+ticker+".csv"
        if os.path.isfile(filename2) == True:
            with open(filename2) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        spisok_hystory.append(cid)
                        line_count += 1
    #print(spisok_hystory)
    max1 = spisok_max(spisok_hystory,4)
    spisok_hystory.remove(max1)
    max2 = spisok_max(spisok_hystory,4)
    spisok_hystory.remove(max2)
    max3 = spisok_max(spisok_hystory,4)
    spisok_hystory.remove(max3)
    max4 = spisok_max(spisok_hystory,4)
    spisok_hystory.remove(max4)
    max5 = spisok_max(spisok_hystory,4)
    spisok_hystory.remove(max5)
    #print("Большие показатели ",max1,max2,max3,max4,max5)
    massiv = []
    massiv.append(max1)
    massiv.append(max2)
    massiv.append(max3)
    massiv.append(max4)
    massiv.append(max5)
    massiv2 = []
    for a1 in massiv:
        #print(a1)
        tradedate = a1[0]
        secid = a1[1]
        shortname = a1[2]
        numtrades = a1[3]
        opn = a1[4]
        high = a1[5]
        low = a1[6]
        volume =a1[7]
        close = a1[8]
        val = "* "+shortname+" #"+secid+",\nТоргуется на бирже "+tradedate+" дней,\nИзменение количества сделок в день"+numtrades+"%\nИзменение цены открытия в день "+opn+"%\nИзменение максимальной цены в день "+high+"%\nИзменение минимальной цены в день "+low+"%\nИзменение объёмов сделок в день "+volume+"%\nИзменение цены закрытия в день "+close
        massiv2.append(val)
    return massiv2

def hystory_soobshenie_high_top():
    TICKs = ticks_only_load(filename)
    spisok_hystory = []
    for TICK in TICKs:
        ticker = TICK[0]
        filename2 = "data/history/TICKs/percents/srednee/"+ticker+".csv"
        if os.path.isfile(filename2) == True:
            with open(filename2) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        spisok_hystory.append(cid)
                        line_count += 1
    #print(spisok_hystory)
    max1 = spisok_max(spisok_hystory,5)
    spisok_hystory.remove(max1)
    max2 = spisok_max(spisok_hystory,5)
    spisok_hystory.remove(max2)
    max3 = spisok_max(spisok_hystory,5)
    spisok_hystory.remove(max3)
    max4 = spisok_max(spisok_hystory,5)
    spisok_hystory.remove(max4)
    max5 = spisok_max(spisok_hystory,5)
    spisok_hystory.remove(max5)
    #print("Большие показатели ",max1,max2,max3,max4,max5)
    massiv = []
    massiv.append(max1)
    massiv.append(max2)
    massiv.append(max3)
    massiv.append(max4)
    massiv.append(max5)
    massiv2 = []
    for a1 in massiv:
        #print(a1)
        tradedate = a1[0]
        secid = a1[1]
        shortname = a1[2]
        numtrades = a1[3]
        opn = a1[4]
        high = a1[5]
        low = a1[6]
        volume =a1[7]
        close = a1[8]
        val = "* "+shortname+" #"+secid+",\nТоргуется на бирже "+tradedate+" дней,\nИзменение количества сделок в день"+numtrades+"%\nИзменение цены открытия в день "+opn+"%\nИзменение максимальной цены в день "+high+"%\nИзменение минимальной цены в день "+low+"%\nИзменение объёмов сделок в день "+volume+"%\nИзменение цены закрытия в день "+close
        massiv2.append(val)
    return massiv2

def hystory_soobshenie_low_top():
    TICKs = ticks_only_load(filename)
    spisok_hystory = []
    for TICK in TICKs:
        ticker = TICK[0]
        filename2 = "data/history/TICKs/percents/srednee/"+ticker+".csv"
        if os.path.isfile(filename2) == True:
            with open(filename2) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        spisok_hystory.append(cid)
                        line_count += 1
    #print(spisok_hystory)
    max1 = spisok_max(spisok_hystory,6)
    spisok_hystory.remove(max1)
    max2 = spisok_max(spisok_hystory,6)
    spisok_hystory.remove(max2)
    max3 = spisok_max(spisok_hystory,6)
    spisok_hystory.remove(max3)
    max4 = spisok_max(spisok_hystory,6)
    spisok_hystory.remove(max4)
    max5 = spisok_max(spisok_hystory,6)
    spisok_hystory.remove(max5)
    #print("Большие показатели ",max1,max2,max3,max4,max5)
    massiv = []
    massiv.append(max1)
    massiv.append(max2)
    massiv.append(max3)
    massiv.append(max4)
    massiv.append(max5)
    massiv2 = []
    for a1 in massiv:
        #print(a1)
        tradedate = a1[0]
        secid = a1[1]
        shortname = a1[2]
        numtrades = a1[3]
        opn = a1[4]
        high = a1[5]
        low = a1[6]
        volume =a1[7]
        close = a1[8]
        val = "* "+shortname+" #"+secid+",\nТоргуется на бирже "+tradedate+" дней,\nИзменение количества сделок в день"+numtrades+"%\nИзменение цены открытия в день "+opn+"%\nИзменение максимальной цены в день "+high+"%\nИзменение минимальной цены в день "+low+"%\nИзменение объёмов сделок в день "+volume+"%\nИзменение цены закрытия в день "+close
        massiv2.append(val)
    return massiv2

def hystory_soobshenie_volume_top():
    TICKs = ticks_only_load(filename)
    spisok_hystory = []
    for TICK in TICKs:
        ticker = TICK[0]
        filename2 = "data/history/TICKs/percents/srednee/"+ticker+".csv"
        if os.path.isfile(filename2) == True:
            with open(filename2) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        spisok_hystory.append(cid)
                        line_count += 1
    #print(spisok_hystory)
    max1 = spisok_max(spisok_hystory,7)
    spisok_hystory.remove(max1)
    max2 = spisok_max(spisok_hystory,7)
    spisok_hystory.remove(max2)
    max3 = spisok_max(spisok_hystory,7)
    spisok_hystory.remove(max3)
    max4 = spisok_max(spisok_hystory,7)
    spisok_hystory.remove(max4)
    max5 = spisok_max(spisok_hystory,7)
    spisok_hystory.remove(max5)
    #print("Большие показатели ",max1,max2,max3,max4,max5)
    massiv = []
    massiv.append(max1)
    massiv.append(max2)
    massiv.append(max3)
    massiv.append(max4)
    massiv.append(max5)
    massiv2 = []
    for a1 in massiv:
        #print(a1)
        tradedate = a1[0]
        secid = a1[1]
        shortname = a1[2]
        numtrades = a1[3]
        opn = a1[4]
        high = a1[5]
        low = a1[6]
        volume =a1[7]
        close = a1[8]
        val = "* "+shortname+" #"+secid+",\nТоргуется на бирже "+tradedate+" дней,\nИзменение количества сделок в день"+numtrades+"%\nИзменение цены открытия в день "+opn+"%\nИзменение максимальной цены в день "+high+"%\nИзменение минимальной цены в день "+low+"%\nИзменение объёмов сделок в день "+volume+"%\nИзменение цены закрытия в день "+close
        massiv2.append(val)
    return massiv2

def hystory_soobshenie_close_top():
    TICKs = ticks_only_load(filename)
    spisok_hystory = []
    for TICK in TICKs:
        ticker = TICK[0]
        filename2 = "data/history/TICKs/percents/srednee/"+ticker+".csv"
        if os.path.isfile(filename2) == True:
            with open(filename2) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cid = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                        spisok_hystory.append(cid)
                        line_count += 1
    #print(spisok_hystory)
    max1 = spisok_max(spisok_hystory,8)
    spisok_hystory.remove(max1)
    max2 = spisok_max(spisok_hystory,8)
    spisok_hystory.remove(max2)
    max3 = spisok_max(spisok_hystory,8)
    spisok_hystory.remove(max3)
    max4 = spisok_max(spisok_hystory,8)
    spisok_hystory.remove(max4)
    max5 = spisok_max(spisok_hystory,8)
    spisok_hystory.remove(max5)
    #print("Большие показатели ",max1,max2,max3,max4,max5)
    massiv = []
    massiv.append(max1)
    massiv.append(max2)
    massiv.append(max3)
    massiv.append(max4)
    massiv.append(max5)
    massiv2 = []
    for a1 in massiv:
        #print(a1)
        tradedate = a1[0]
        secid = a1[1]
        shortname = a1[2]
        numtrades = a1[3]
        opn = a1[4]
        high = a1[5]
        low = a1[6]
        volume =a1[7]
        close = a1[8]
        val = "* "+shortname+" #"+secid+",\nТоргуется на бирже "+tradedate+" дней,\nИзменение количества сделок в день"+numtrades+"%\nИзменение цены открытия в день "+opn+"%\nИзменение максимальной цены в день "+high+"%\nИзменение минимальной цены в день "+low+"%\nИзменение объёмов сделок в день "+volume+"%\nИзменение цены закрытия в день "+close
        massiv2.append(val)
    return massiv2

def HYSTORYs(): # НАДО ДУМАТЬ НАД ФУНКЦИОНАЛОМ ИЛИ ВООБЩЕ ЭТО ЗДЕСЬ НИ К ЧЕМУ...
    try: # пробуем
        history_parse_all() #
    except FileNotFoundError: #
        dividents_parse()

#hystory_soobshenie_close_top()
#print(hystory_soobshenie_numtrade_top())
#print(history_poisk_sred_pokazatel_TICKs())
#print(history_poisk_all_TICK_perc())
#print(history_poisk_all_TICK())
#print(history_parse_all())
