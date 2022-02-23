import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np



from lxml import html
import os
import xlwt
import datetime
import time
import random
import csv
import functools
from pprint import pprint
import matplotlib.pyplot as plt
import xlsxwriter
from openpyxl import load_workbook
import re



# подключаем свои модули
from os_tools import *

def upload_file(table_name):
    tables = pd.read_html(table_name) # перед этим надо сделать pip install lxml
    #print(tables)
    print(f'Найдено {len(tables)} таблиц')
    for table in tables:
        df = table
        #len(table)
        names_columns = table.columns
        #print(names_columns)
        #df.iloc[0]
        for index,name in enumerate(names_columns):
            #print(name,table.iloc[0][index])
            df.rename(columns={f'{name}':f'{table.iloc[0][index]}'},inplace = True)
        new_col = []
        for count in table.iloc[0]:
            new_col.append(count)
        #print(new_col)
        table.columns = new_col
        table.drop(labels = [0],axis = 0,inplace=True)
        #print(df)
    return tables



def sber_osnovnor():
    dirs, files, prefs, forms = list_one_dir_sber()
    for file in files:
        #print(file)
        print(upload_file(file))





















def get_reports_sber():
    ''' Получаем словарь с именами файлов и полным путем к файлам '''
    files = list_dir_sber()
    data_n = {}
    for file in files:
        key1 = file.split('/')[2].split('_')[0]
        key3 = str(file.split('/')[2].split('.')[0].split('_')[1])+' '+str(file.split('/')[2].split('.')[0].split('_')[2])
        key2 = file.split('/')[2].split('.')[0].split('_')[3]
        if key1 not in data_n.keys():
            data_n[key1] = {f"{key2}" : {f"{key3}" : file}}
        elif key2 not in data_n[key1].keys():
            data_n[key1][key2] = {f"{key3}" : file}
        elif key3 not in data_n[key1][key2].keys():
            data_n[key1][key2][key3] = file
    return data_n


def pars_file(file):
    with open(file, "r", encoding='utf-8') as f:
        soup = bs(f.read(), 'lxml')
        '''
        print(soup.title.text.strip())
        """
        Отчет брокера S025NSG
        """
        date = soup.find_all('h3')[0].text.split('\n')
        d = ''
        for t in date:
            t = str(t) + ' '
            d += t
        print(d)
        '''
        trs = soup.find_all('table', class_='RatingAssets')[0].find_all('tr')
        keys = []
        dict = {}
        for tr in trs:
            if trs.index(tr) == 0:
                tds = tr.find_all('td')
                for td in tds:
                    keys.append(td.text)
            else:
                tds = tr.find_all('td')
                for td in tds:
                    td1 = td.text.strip()
                    print(td1)
                    ind = tds.index(td)
                    if ind != 0:
                        dict[key] = {f"{keys[ind]}" : f"{td1}"}
                    else:
                        key = td1
                        dict[td1] = td1

        '''
        key
        Торговая площадка
        Оценка портфеля ЦБ, руб.
        Денежные средства, руб.
        Оценка, руб.

        value
        Срочный рынок
        0.00
        0.00
        0.00

        value
        Валютный рынок
        0.00
        0.00
        0.00
        value

        Фондовый рынок
        102 325.10
        967.48
        103 292.58

        value
        Итого
        102 325.10
        967.48
        103 292.58
        '''

        print()
        print()
        print(keys)
        print()
        print()
        pprint(dict)





def split_for_scheta():
    reports_sber = get_reports_sber()
    pprint(reports_sber) # получен словарь с данными
    for key in reports_sber.keys():
        filename = 'otchet/' + key + '.xlsx'
        for period in reports_sber[key].keys():
            if period == 'D':
                for date in reports_sber[key][period].keys():
                    file = reports_sber[key][period][date]
                    print()
                    print()
                    print()
                    print(file)
                    dict = pars_file(file)



















sber_osnovnor()
