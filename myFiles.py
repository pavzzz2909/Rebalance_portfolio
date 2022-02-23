# подключаем свои модули
from os_tools import *



from pprint import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
from openpyxl import load_workbook
import datetime
import re



def open_xls(file):
    ''' Получаем дата фрейм из одного эксель файла '''
    df = pd.read_excel(file)
    return df

def get_filenames_from_my_files():
    ''' Получаем словарь с именами файлов и полным путем к файлам '''
    files = list_dir()
    data = {}
    for file in files:
        key = file.split('/')[1].split('.')[0]
        data[key] = file
    return data

def get_deposits_cash():
    dict = get_filenames_from_my_files()
    data = {}
    for key in dict.keys():
        if 'ВНЕСЕНИЕ' in key:
            data[key] = dict[key]
    return data

def get_broker_accounts():
    dict = get_filenames_from_my_files()
    data = {}
    for key in dict.keys():
        if 'ВНЕСЕНИЕ' not in key:
            data[key] = dict[key]
    return data

def arifm_deposits_cash():
    dict = get_deposits_cash()
    dict_itog = {}
    for key in dict.keys():
        dict_name = {}
        name = key.split(' ')[3]
        filename = dict[key]
        data = open_xls(filename)

        sum_IIS_Tin = round(data['ИИС Тинькофф'].astype('float64').sum(),2)
        sum_IIS_Sber = round(data['ИИС Сбер'].astype('float64').sum(),2)
        sum_IIS_VTB = round(data['ИИС ВТБ'].astype('float64').sum(),2)
        sum_Br_sber1 = round(data['Брокер Сбер моя подушка'].astype('float64').sum(),2)
        sum_Br_sber2 = round(data['Брокер Сбер подарки дочкам'].astype('float64').sum(),2)
        sum_Br_vtb_P = round(data['Брокер ВТБ Паши'].astype('float64').sum(),2)
        sum_Br_vtb_L = round(data['Брокер ВТБ Лены'].astype('float64').sum(),2)
        sum_Br_tin = round(data['Брокер Тинькофф'].astype('float64').sum(),2)
        sum_Br_tin_sp = round(data['Брокер Тинькофф спекуляции'].astype('float64').sum(),2)
        sum_all = sum_IIS_Tin + sum_IIS_Sber + sum_IIS_VTB + sum_Br_sber1 + sum_Br_sber2 + sum_Br_vtb_P + sum_Br_vtb_L + sum_Br_tin + sum_Br_tin_sp
        dict_name ={
                     "Сумма всех взносов":sum_all,
                     "ИИС Тинькофф":sum_IIS_Tin,
                     "ИИС Сбер":sum_IIS_Sber,
                     "ИИС ВТБ":sum_IIS_VTB,
                     "Брокер Сбер моя подушка":sum_Br_sber1,
                     "Брокер Сбер подарки дочкам":sum_Br_sber2,
                     "Брокер ВТБ Паши":sum_Br_vtb_P,
                     "Брокер ВТБ Лены":sum_Br_vtb_L,
                     "Брокер Тинькофф":sum_Br_tin,
                     "Брокер Тинькофф спекуляции":sum_Br_tin_sp
                    }
        dict_itog[name] = dict_name
    return dict_itog

def is_nan(x):
    return (x != x)

def analiz_scheta():
    '''  '''
    dict = get_broker_accounts()
    dict_itog = {}
    count_tick_kupleno_all = 0
    sum_tick_pokupka_kom_all = 0
    sum_tick_pokupka_all = 0
    count_tick_prodano_all = 0
    sum_tick_prodaga_kom_all = 0
    sum_tick_prodaga_all = 0
    tick_divid_all = 0
    tick_kupon_all = 0
    count_tick_nalichie_all = 0
    valute_act_all = ""
    valute_div_all = ""
    dict_all = {}
    for key in dict.keys():
        filename = dict[key]
        data = open_xls(filename)
        if len(data) != 0:
            spisok_ticks = data['Тикер'].unique()
            dict_sch = {}
            for tick in spisok_ticks:
                x = float('nan')
                if tick == tick:
                    options = [tick]
                    data_tick = data[data['Тикер'].isin(options)]
                    data_tick = data_tick.fillna(0)
                    data_tick['Сумма покупки'] = (data_tick['Куплено'] * data_tick['Цена покупки'] + data_tick['НКД покупки'] + data_tick['Комиссия покупки'])
                    data_tick['Сумма продажи'] = (data_tick['Продано'] * data_tick['Цена продажи'] + data_tick['НКД продажи'] + data_tick['Комиссия продажи'])
                    count_tick_kupleno = round(data_tick['Куплено'].astype('float64').sum(),2)
                    count_tick_prodano = round(data_tick['Продано'].astype('float64').sum(),2) # количество ценных бумаг в наличии
                    count_tick_nalichie = round(count_tick_kupleno - count_tick_prodano,2)
                    sum_tick_pokupka = round(data_tick['Сумма покупки'].astype('float64').sum(),2) # сумма за которую приобели все ценные бумаги имеющиеся в наличии
                    sum_tick_pokupka_kom = round(data_tick['Комиссия покупки'].astype('float64').sum(),2) # сумма за которую приобели все ценные бумаги имеющиеся в наличии
                    sum_tick_prodaga = round(data_tick['Сумма продажи'].astype('float64').sum(),2) # сумма за которую приобели все ценные бумаги имеющиеся в наличии
                    sum_tick_prodaga_kom = round(data_tick['Комиссия продажи'].astype('float64').sum(),2) # сумма за которую приобели все ценные бумаги имеющиеся в наличии
                    tick_divid = round(data_tick['Выплаченные дивиденды'].astype('float64').sum(),2) # сумма полученных дивидендов
                    tick_kupon = round(data_tick['Выплаченные купоны'].astype('float64').sum(),2) # сумма купонов
                    valute_act = data_tick['Валюта'].unique()[0]
                    data_tick_div = data_tick[(data_tick['Выплаченные дивиденды'] > 0)|(data_tick['Выплаченные купоны'] > 0)]
                    if len(data_tick_div) != 0:
                        valute_div = data_tick_div['Валюта'].unique()[0]
                        valute_div_all = data_tick_div['Валюта'].unique()[0]
                    else:
                        valute_div = None
                        valute_div_all = None
                    count_tick_kupleno_all += count_tick_kupleno
                    sum_tick_pokupka_kom_all += sum_tick_pokupka_kom
                    sum_tick_pokupka_all += sum_tick_pokupka
                    count_tick_prodano_all += count_tick_prodano
                    sum_tick_prodaga_kom_all += sum_tick_prodaga_kom
                    sum_tick_prodaga_all += sum_tick_prodaga
                    tick_divid_all += tick_divid
                    tick_kupon_all += tick_kupon
                    count_tick_nalichie_all += count_tick_nalichie
                    valute_act_all = data_tick['Валюта'].unique()[0]
                    dict_sch[tick] = {
                                       "Количество куплено" : count_tick_kupleno,
                                       "Комиссия покупки" : sum_tick_pokupka_kom,
                                       "Сумма приобретения" : sum_tick_pokupka,
                                       "Количество продано" : count_tick_prodano,
                                       "Комиссия продажи" : sum_tick_prodaga_kom,
                                       "Сумма продажи" : sum_tick_prodaga,
                                       "Полученные дивиденды" : tick_divid,
                                       "Полученные купоны" : tick_kupon,
                                       "Имеется" : count_tick_nalichie,
                                       "Валюта ЦБ" : valute_act,
                                       "Валюта див" : valute_div
                                      }

                    if tick in dict_all.keys():
                        dict_all[tick]["Количество куплено"] += count_tick_kupleno
                        dict_all[tick]["Комиссия покупки"] += sum_tick_pokupka_kom
                        dict_all[tick]["Сумма приобретения"] += sum_tick_pokupka
                        dict_all[tick]["Количество продано"] += count_tick_prodano
                        dict_all[tick]["Комиссия продажи"] += sum_tick_prodaga_kom
                        dict_all[tick]["Сумма продажи"] += sum_tick_prodaga
                        dict_all[tick]["Полученные дивиденды"] += tick_divid
                        dict_all[tick]["Полученные купоны"] += tick_kupon
                        dict_all[tick]["Имеется"] += count_tick_nalichie
                    else:
                        dict_all[tick] = {
                                           "Количество куплено" : count_tick_kupleno,
                                           "Комиссия покупки" : sum_tick_pokupka_kom,
                                           "Сумма приобретения" : sum_tick_pokupka,
                                           "Количество продано" : count_tick_prodano,
                                           "Комиссия продажи" : sum_tick_prodaga_kom,
                                           "Сумма продажи" : sum_tick_prodaga,
                                           "Полученные дивиденды" : tick_divid,
                                           "Полученные купоны" : tick_kupon,
                                           "Имеется" : count_tick_nalichie,
                                           "Валюта ЦБ" : valute_act,
                                           "Валюта див" : valute_div
                                          }
            dict_itog[key] = dict_sch
        else:
            dict_itog[key] = {}
    for key_dict_all in dict_all.keys():
        if dict_all[key_dict_all]["Имеется"] > 0:
            dict_all[key_dict_all]["Количество куплено"] = round(dict_all[key_dict_all]["Количество куплено"],2)
            dict_all[key_dict_all]["Комиссия покупки"] = round(dict_all[key_dict_all]["Комиссия покупки"],2)
            dict_all[key_dict_all]["Сумма приобретения"] = round(dict_all[key_dict_all]["Сумма приобретения"],2)
            dict_all[key_dict_all]["Количество продано"] = round(dict_all[key_dict_all]["Количество продано"],2)
            dict_all[key_dict_all]["Комиссия продажи"] = round(dict_all[key_dict_all]["Комиссия продажи"],2)
            dict_all[key_dict_all]["Сумма продажи"] = round(dict_all[key_dict_all]["Сумма продажи"],2)
            dict_all[key_dict_all]["Полученные дивиденды"] = round(dict_all[key_dict_all]["Полученные дивиденды"],2)
            dict_all[key_dict_all]["Полученные купоны"] = round(dict_all[key_dict_all]["Полученные купоны"],2)
            dict_all[key_dict_all]["Имеется"] = round(dict_all[key_dict_all]["Имеется"],2)
            dict_all[key_dict_all]["Средняя цена покупки"] = round((dict_all[key_dict_all]["Сумма приобретения"]+dict_all[key_dict_all]["Комиссия покупки"])/dict_all[key_dict_all]["Количество куплено"],2)
    dict_all2 ={}
    for key in dict_all.keys():
        if dict_all[key]['Имеется'] > 0:
            dict_all2[key] = dict_all[key]

    dict_itog['all'] = dict_all2
    return dict_itog

def print_schet(dict):
    for key in dict.keys():
        div_doh = 0
        kup_doh = 0
        print('______________________________________________________________________')
        print(key)
        if key == 'all':
            for key2 in dict[key].keys():
                doh_perc = round((dict[key][key2]['Полученные дивиденды']+dict[key][key2]['Полученные купоны'])/dict[key][key2]['Сумма приобретения']*100,2)
                sum_doh = round(dict[key][key2]['Полученные дивиденды'] + dict[key][key2]['Полученные купоны'],2)
                print(key2)
                print(f"Текущий баланс составляет {dict[key][key2]['Имеется']}, средняя цена закупки составляет {dict[key][key2]['Средняя цена покупки']}") #Было приобретено {dict[key][key2]['Количество куплено']} акций, из которых продано {dict[key][key2]['Количество продано']} акций.
                print(f"Сумма полученного дохода по дивидендам или купоны {sum_doh}, процент от суммы вложений составляет {doh_perc}%")
        else:
            for key2 in dict[key].keys():
                doh_perc = round((dict[key][key2]['Полученные дивиденды']+dict[key][key2]['Полученные купоны'])/dict[key][key2]['Сумма приобретения']*100,2)
                sum_doh = round(dict[key][key2]['Полученные дивиденды'] + dict[key][key2]['Полученные купоны'],2)
                print(key2)
                print(f"Текущий баланс составляет {dict[key][key2]['Имеется']}.") #Было приобретено {dict[key][key2]['Количество куплено']} акций, из которых продано {dict[key][key2]['Количество продано']} акций.
                print(f"Сумма покупки акций составляет {dict[key][key2]['Сумма приобретения']}, сумма продажи акций составляет {dict[key][key2]['Сумма продажи']} ")
                print(f"Сумма полученного дохода по дивидендам или купоны {sum_doh}, процент от суммы вложений составляет {doh_perc}%")










def new():
    pass
