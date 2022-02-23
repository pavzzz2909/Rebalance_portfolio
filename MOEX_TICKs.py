import requests
import json
import pandas as pd

from MOEX_dates import *
from os_tools import *

# на время запила
from pprint import pprint




def get_price(tick):
    ''' Не доделано '''
    URL = f"https://iss.moex.com/iss/securities/{tick}.json"
    response = requests.get(URL).json()
    pprint(response)


def get_MOEX_tickers_slovar():
    ''' Получение словаря тикеров торгуемых акций на Московской бирже
    формируется в словарь:
    {'ABRD': {'BOARDID': 'TQBR',
          'BOARDNAME': 'Т+: Акции и ДР - безадрес.',
          'CURRENCYID': 'SUR',
          'DECIMALS': 1,
          'FACEUNIT': 'SUR',
          'FACEVALUE': 1,
          'INSTRID': 'EQIN',
          'ISIN': 'RU000A0JS5T7',
          'ISSUESIZE': 98000184,
          'LATNAME': 'Abrau-Durso ao',
          'LISTLEVEL': 3,
          'LOTSIZE': 10,
          'MARKETCODE': 'FNDT',
          'MINSTEP': 0.5,
          'PREVADMITTEDQUOTE': 193,
          'PREVDATE': '2021-12-20',
          'PREVLEGALCLOSEPRICE': 193,
          'PREVPRICE': 193,
          'PREVWAPRICE': 193,
          'REGNUMBER': '1-02-12500-A',
          'REMARKS': None,
          'SECID': 'ABRD',
          'SECNAME': 'Абрау-Дюрсо ПАО ао',
          'SECTORID': None,
          'SECTYPE': '1',
          'SETTLEDATE': '2021-12-23',
          'SHORTNAME': 'АбрауДюрсо',
          'STATUS': 'A'},
          ...
    '''
    slovar_TICKs = {}
    URL ="http://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?iss.meta=off&iss.only=securities&securities"
    response = requests.get(URL).json()
    number_of_dict = 1
    for row in response['securities']['data']:
        slovar_TICKs[number_of_dict] = {
                f"{response['securities']['columns'][0]}" : row[0],
                f"{response['securities']['columns'][1]}" : row[1],
                f"{response['securities']['columns'][2]}" : row[2],
                f"{response['securities']['columns'][3]}" : row[3],
                f"{response['securities']['columns'][4]}" : row[4],
                f"{response['securities']['columns'][5]}" : row[5],
                f"{response['securities']['columns'][6]}" : row[6],
                f"{response['securities']['columns'][7]}" : row[7],
                f"{response['securities']['columns'][8]}" : row[8],
                f"{response['securities']['columns'][9]}" : row[9],
                f"{response['securities']['columns'][10]}" : row[10],
                f"{response['securities']['columns'][11]}" : row[11],
                f"{response['securities']['columns'][12]}" : row[12],
                f"{response['securities']['columns'][13]}" : row[13],
                f"{response['securities']['columns'][14]}" : row[14],
                f"{response['securities']['columns'][15]}" : row[15],
                f"{response['securities']['columns'][16]}" : row[16],
                f"{response['securities']['columns'][17]}" : row[17],
                f"{response['securities']['columns'][18]}" : row[18],
                f"{response['securities']['columns'][19]}" : row[19],
                f"{response['securities']['columns'][20]}" : row[20],
                f"{response['securities']['columns'][21]}" : row[21],
                f"{response['securities']['columns'][22]}" : row[22],
                f"{response['securities']['columns'][23]}" : row[23],
                f"{response['securities']['columns'][24]}" : row[24],
                f"{response['securities']['columns'][25]}" : row[25],
                f"{response['securities']['columns'][26]}" : row[26],
                f"{response['securities']['columns'][27]}" : row[27]
        }
        number_of_dict +=1
    return slovar_TICKs

def json_create_MOEX_tickers(dictionary,filename):
    '''    Создает json словарь со всеми акциями торгуемыми на бирже
    ******************** РАБОТАЕТ, доработки не требуется ********************'''
    s1 = get_now()
    jsonData = json.dumps(dictionary)
    with open(filename,'w',encoding ='utf-8') as file:
        file.write(jsonData)
    s5 = get_now()
    ss = s5 - s1

def xlsx_create_MOEX_tickers(data):
    '''    Создает xlsx книгу со всеми ценными бумагами торгуемыми на Московской бирже    '''
    dir = 'data/'
    mk_dir(dir)
    count = len(list(data.keys()))
    df = pd.DataFrame(data)
    data_in_file = df.transpose()
    filename = dir+'TICKs.xlsx'
    s1 = get_now()
    data_in_file.to_excel(filename, sheet_name='operation', index=False)
    s5 = get_now()
    ss = s5 - s1
    print('Время создания xlsx файла со всеми операциями составляет: ',ss)
    dict = data_in_file.to_dict('index')
    filename_j = dir+'TICKs.json'
    json_create_MOEX_tickers(dict,filename_j)
    s5 = get_now()
    ss = s5 - s1
    print('Время создания json файла составляет: ',ss)

def write_MOEX_tickers():
    print('Создаем файлы с тикерами')
    dictionary = get_MOEX_tickers_slovar()
    xlsx_create_MOEX_tickers(dictionary)

def read_MOEX_tickers():
    '''    Считываем словарь с тикерами акций из файла    '''
    with open('data/TICKs.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    return data

def read_MOEX_tickers_figi(SECID):
    ''' Возращает всю информацию по указанному тикеру в виде словаря '''
    data = read_MOEX_tickers()
    for key in data.keys():
        iskomoe = data[key]['SECID']
        if SECID == iskomoe:
            return data[key]

def read_MOEX_tickers_BOARDID(value):
    ''' Определение "Код режима" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['BOARDID']

def read_MOEX_tickers_BOARDNAME(value):
    ''' Определение "Режим торгов" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['BOARDNAME']

def read_MOEX_tickers_CURRENCYID(value):
    ''' Определение "Валюта" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['CURRENCYID']

def read_MOEX_tickers_DECIMALS(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['DECIMALS']

def read_MOEX_tickers_FACEUNIT(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['FACEUNIT']

def read_MOEX_tickers_FACEVALUE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['FACEVALUE']

def read_MOEX_tickers_INSTRID(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['INSTRID']

def read_MOEX_tickers_ISIN(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['ISIN']

def read_MOEX_tickers_ISSUESIZE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['ISSUESIZE']

def read_MOEX_tickers_LATNAME(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['LATNAME']

def read_MOEX_tickers_LISTLEVEL(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['LISTLEVEL']

def read_MOEX_tickers_LOTSIZE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['LOTSIZE']

def read_MOEX_tickers_MARKETCODE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['MARKETCODE']

def read_MOEX_tickers_MINSTEP(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['MINSTEP']

def read_MOEX_tickers_PREVADMITTEDQUOTE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['PREVADMITTEDQUOTE']

def read_MOEX_tickers_PREVDATE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['PREVDATE']

def read_MOEX_tickers_PREVLEGALCLOSEPRICE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['PREVLEGALCLOSEPRICE']

def read_MOEX_tickers_PREVPRICE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['PREVPRICE']

def read_MOEX_tickers_PREVWAPRICE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['PREVWAPRICE']

def read_MOEX_tickers_REGNUMBER(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['REGNUMBER']

def read_MOEX_tickers_REMARKS(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['REMARKS']

def read_MOEX_tickers_SECNAME(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['SECNAME']

def read_MOEX_tickers_SECTORID(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['SECTORID']

def read_MOEX_tickers_SECTYPE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['SECTYPE']

def read_MOEX_tickers_SETTLEDATE(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['SETTLEDATE']

def read_MOEX_tickers_SHORTNAME(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['SHORTNAME']

def read_MOEX_tickers_STATUS(value):
    ''' Определение "" по тикеру '''
    data = read_MOEX_tickers_lot(value)
    return data['STATUS']







# подумать как сделать со словарями такое
def ticks_new(filename): # функция обновления элементов в списке торгуемых акций
#    print("Применяем функцию ticks_new(filename)")
    spisok_new = ticks_parse()
    spisok_TICKs = ticks_load(filename)
    spisokNew =[]
    for new in spisok_new:
        spisokNew.append(new[1])
    spisokTICKs =[]
    for Tick in spisok_TICKs:
        spisokTICKs.append(Tick[1])
    new_TICKs = []
    for name in spisokNew:
        if name not in spisokTICKs:
            new_TICKs.append (name)
    dlina = len(new_TICKs)
    if dlina != 0:
        return new_TICKs
    else:
        print("Новых тикеров не обнаружено!")

def TICKs(): # функция пробуем если вес файла > 0 функция обновления, если ошибка создаем файл с тикерами
#    print("Применяем функцию TICKs()")
    try:
        new = ticks_new(filename)
        if new == None:
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S'),"Данные по тикерам проверены и актуальны")
        else:
            ticks_new(filename)
            ticks_update(filename)
    except FileNotFoundError:
        ticks_sozdanie(ticks_parse(), header, filename)
