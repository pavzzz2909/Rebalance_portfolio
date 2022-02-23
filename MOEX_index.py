import requests
import json
import pandas as pd
from progress.bar import IncrementalBar

from MOEX_dates import *
from os_tools import *

# на время запила
from pprint import pprint


def get_index():
    '''
    Возвращает словарь с индексами торгуемыми на ММВБ
    {1: {'from': '2001-01-03',
         'indexid': 'IMOEX',
         'shortname': 'Индекс МосБиржи',
         'till': '2021-12-29'},
     2: {'from': '2008-05-27',
         'indexid': 'MOEX10',
         'shortname': 'Индекс МосБиржи 10',
         'till': '2021-12-29'},
     '''
    slovar_index = {}
    URL = 'http://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics.json'
    response = requests.get(URL).json()
    #pprint(response)
    number_index = 1
    for row in response['indices']['data']:
        slovar_index[number_index] = {
            f"{response['indices']['columns'][0]}" : row[0],
            f"{response['indices']['columns'][1]}" : row[1],
            f"{response['indices']['columns'][2]}" : row[2],
            f"{response['indices']['columns'][3]}" : row[3]
            }
        number_index +=1
    print(f'Получен словарь с индексами в количестве {len(slovar_index)} шт.')
    return slovar_index

def get_index_info(index):
    dict = {}
    URL = f'http://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/{index}.json?iss.meta=off&limit=200'
    response = requests.get(URL).json()
    #pprint(response)
    number_index = 1
    for row in response['analytics']['data']:
        dict[number_index] = {
            f"{response['analytics']['columns'][0]}" : row[0],
            f"{response['analytics']['columns'][1]}" : row[1],
            f"{response['analytics']['columns'][2]}" : row[2],
            f"{response['analytics']['columns'][3]}" : row[3],
            f"{response['analytics']['columns'][4]}" : row[4],
            f"{response['analytics']['columns'][5]}" : row[5],
            f"{response['analytics']['columns'][6]}" : row[6]
            }
        number_index +=1
    #pprint(dict)
    return dict

def get_all_index_weight():
    dict = get_index()
    return_dict = {}
    #bar = IncrementalBar('Загрузка индексов', max = len(dict.keys()))
    for key in dict.keys():
        #bar.next()
        index = dict[key]['indexid']
        return_dict[index] = get_index_info(index)
        time.sleep(0.1)
    #bar.finish()
    return return_dict

def json_create_index(dictionary):
    '''    Создает json словарь со всеми акциями торгуемыми на бирже
    ******************** РАБОТАЕТ, доработки не требуется ********************'''
    s1 = get_now()
    jsonData = json.dumps(dictionary)
    filename = 'data/index/index.json'
    with open(filename,'w',encoding ='utf-8') as file:
        file.write(jsonData)
    s5 = get_now()
    ss = s5 - s1

def xlsx_create_MOEX_index(data):
    '''    Создает xlsx книгу со всеми ценными бумагами торгуемыми на Московской бирже    '''
    dir = 'data/'
    mk_dir(dir)
    dir = dir + 'index/'
    mk_dir(dir)
    for key in data.keys():
        count = len(list(data[key].keys()))
        df = pd.DataFrame(data[key])
        data_in_file = df.transpose()
        filename = dir+f'{key}.xlsx'
        s1 = get_now()
        data_in_file = data_in_file.sort_values(by='weight', ascending=False)
        data_in_file.to_excel(filename, sheet_name='operation', index=False)
        s5 = get_now()
        ss = s5 - s1
        print('Время создания xlsx файла со всеми операциями составляет: ',ss)

def write_MOEX_index():
    print('Создаем файлы с тикерами')
    dictionary = get_all_index_weight()
    json_create_index(dictionary)
    xlsx_create_MOEX_index(dictionary)

# http://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.xml?iss.meta=off&limit=100
# выводит бумаги в индексе ММВБ

# http://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/MOEXBC.xml?iss.meta=off&limit=100
# индекс голубых фишек ММВБ

# http://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/MCXSM.xml?iss.meta=off&limit=100
# индекс малой и средней капитализации

# http://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/MOEXBMI.xml?iss.meta=off&limit=100
# индекс широкого рынка
