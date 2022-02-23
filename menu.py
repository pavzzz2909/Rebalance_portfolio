import schedule
import time                             # импорт времени
import random                           # импорт рандома
import xlwt
import datetime as dt


# подгружаем исполняемые файлы
from config import *
from history import *
from currency import *
from users import *
from threading import Thread
from pprint import pprint

# подгружаем наши модули
from MOEX_TICKs import *
from MOEX_dividents import *
from load_my_files import *
from MOEX_index import *

def use_MOEX_TICKs():
    write_MOEX_tickers() # обновление списка тикеров

def use_dividents():
    dividents_parse_all() # обновление словаря со всеми дивидендами по всем бумагам
    pprint(future_dividents()) # возвращает предстоящие дивиденды


def use_my_files():
    ''' работа с файлом my_files '''
    #get_filenames_from_my_files() # получение списка всех файлов
    #pprint(get_deposits_cash()) # получения списка файлов с пополнениями
    #pprint(get_broker_accounts()) # получение словаря файлов со счетами
    #pprint(arifm_deposits_cash()) # возращает словарь с арифметикой по счетам
    dict = analiz_scheta() # возвращает словарь со всеми счетами
    #pprint(dict['all'])
    print_schet(dict)
    #pprint(get_price('GAZP'))
    #dividents_in_last_year()


def index():
    #get_index() # возвращает словарь с индексами торгуемыми на ММВБ
    write_MOEX_index()


use_my_files()

'''

def start(message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    #print(user_id,user_first_name,user_last_name,user_username)
    update_users(user_id,user_first_name,user_last_name,user_username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🎫 Акции')
    item2 = types.KeyboardButton('🏦 Курсы валют')
    item3 = types.KeyboardButton('📚 В разработке')
    item4 = types.KeyboardButton('➡️ В разработке')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup = markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    #print(user_id,user_first_name,user_last_name,user_username)
    update_users(user_id,user_first_name,user_last_name,user_username)
    if message.chat.type == 'private':
        if message.text == '🎫 Акции':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🚀 На заметку')
            item2 = types.KeyboardButton('💰 Дивиденды')
            item3 = types.KeyboardButton('🏆 Лучшие показатели')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, '🎫 Акции', reply_markup = markup)

        elif message.text == '🚀 На заметку':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(back)
            bot.send_message(message.chat.id, 'Находится в разработке', reply_markup = markup)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с перспективными акциями пользователю", message.chat.id)

        elif message.text == '💰 Дивиденды':
            all_div = dividents_only_load()
            #print(all_div)
            divid = dividents_v_soobshenie(all_div) # запускаем функцию получения списка назначенных дивидендов
            #print(divid)
            soob ="По данным Московской биржи (MOEX) назначены дивиденды по следующим ценным бумагам:🤑\n"
            for divi in divid:
                soob += divi+"\n"
            bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с дивидендами пользователю", message.chat.id)

        elif message.text == '🏆 Лучшие показатели':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('За все время')
            item2 = types.KeyboardButton('РАЗРАБОТКА')
            item3 = types.KeyboardButton('РАЗРАБОТКА')
            item4 = types.KeyboardButton('РАЗРАБОТКА')
            item5 = types.KeyboardButton('РАЗРАБОТКА')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, item3, item4, item5, back)
            bot.send_message(message.chat.id, '🏆 Лучшие показатели', reply_markup = markup)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с Лучшими показателями пользователю", message.chat.id)

        elif message.text == 'За все время':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Количество сделок')
            item2 = types.KeyboardButton('Объем сделок')
            item3 = types.KeyboardButton('Цена открытия')
            item4 = types.KeyboardButton('Минимальная цена')
            item5 = types.KeyboardButton('Максимальная цена')
            item6 = types.KeyboardButton('Цена закрытия')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, item3, item4, item5, item6, back)
            bot.send_message(message.chat.id, 'За все время', reply_markup = markup)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение За все время пользователю", message.chat.id)


######## ЛУЧШИЕ ПОКАЗАТЕЛИ
        elif message.text == 'Количество сделок':
            divid = hystory_soobshenie_numtrade_top() # запускаем функцию получения списка назначенных дивидендов
            soob ="По данным Московской биржи (MOEX) наибольший средний прирост количества сделок за весь период торгов наблюдается у следующих акций:\n"
            bot.send_message(message.chat.id, soob)
            for divi in divid:
                soob = divi
                bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение наибольший средний прирост количества сделок пользователю", message.chat.id)

        elif message.text == 'Объем сделок':
            divid = hystory_soobshenie_volume_top() # запускаем функцию получения списка назначенных дивидендов
            soob ="По данным Московской биржи (MOEX) наибольший средний прирост объёма сделок за весь период торгов наблюдается у следующих акций:\n"
            bot.send_message(message.chat.id, soob)
            for divi in divid:
                soob = divi
                bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение наибольший средний прирост объёма сделок пользователю", message.chat.id)

        elif message.text == 'Цена открытия':
            divid = hystory_soobshenie_open_top() # запускаем функцию получения списка назначенных дивидендов
            soob ="По данным Московской биржи (MOEX) наибольший средний прирост цены открытия за весь период торгов наблюдается у следующих акций:\n"
            bot.send_message(message.chat.id, soob)
            for divi in divid:
                soob = divi
                bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение наибольший средний прирост цены открытия пользователю", message.chat.id)

        elif message.text == 'Минимальная цена':
            divid = hystory_soobshenie_low_top() # запускаем функцию получения списка назначенных дивидендов
            soob ="По данным Московской биржи (MOEX) наибольший средний прирост минимальной цены за весь период торгов наблюдается у следующих акций:\n"
            bot.send_message(message.chat.id, soob)
            for divi in divid:
                soob = divi
                bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение наибольший средний прирост минимальной цены пользователю", message.chat.id)

        elif message.text == 'Максимальная цена':
            divid = hystory_soobshenie_high_top() # запускаем функцию получения списка назначенных дивидендов
            soob ="По данным Московской биржи (MOEX) наибольший средний прирост максимальной цены за весь период торгов наблюдается у следующих акций:\n"
            bot.send_message(message.chat.id, soob)
            for divi in divid:
                soob = divi
                bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение наибольший средний прирост максимальной цены пользователю", message.chat.id)

        elif message.text == 'Цена закрытия':
            divid = hystory_soobshenie_close_top() # запускаем функцию получения списка назначенных дивидендов
            soob ="По данным Московской биржи (MOEX) наибольший средний прирост цены закрытия за весь период торгов наблюдается у следующих акций:\n"
            bot.send_message(message.chat.id, soob)
            for divi in divid:
                soob = divi
                bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение наибольший средний прирост цены закрытия пользователю", message.chat.id)

######## ЛУЧШИЕ ПОКАЗАТЕЛИ

        elif message.text == '🏦 Курсы валют':
            soob ="На текущий момент стоимость валют по данным ММВБ составляет:\n"
            dol = kursi()
            for a in dol:
                soob += a+"\n"
            soob+="Для получения дополнительной информации по валютам обратитесь к соответствующему меню\n"
            bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с курсом доллара пользователю", message.chat.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🇺🇸 Курс Доллара 💵')
            item2 = types.KeyboardButton('🇪🇺 Курс Евро 💶')
            item3 = types.KeyboardButton('🇪🇺/🇺🇸 Разница 💶/💵')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, '🏦 Курсы валют', reply_markup = markup)


################################    ВАЛЮТА   ######################
        elif message.text == '🇺🇸 Курс Доллара 💵':
            soob ="По данным Московской биржи (MOEX) курс 💵/рубль составляет:\n"
            dol = dollar()
            for a in dol:
                soob += a+"\n"
            bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с курсом доллара пользователю", message.chat.id)


        elif message.text == '🇪🇺 Курс Евро 💶':
            soob ="По данным Московской биржи (MOEX) курс 💶/рубль составляет:\n"
            eur = euro()
            for a in eur:
                soob += a+"\n"
            bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с курсом евро пользователю", message.chat.id)

        elif message.text == '🇪🇺/🇺🇸 Разница 💶/💵':
            soob ="По данным Московской биржи (MOEX) курс 💶/💵 составляет:\n"
            eurdol = eur_dol()
            for a in eurdol:
                soob += a+"\n"
            bot.send_message(message.chat.id, soob)
            now = datetime.datetime.now()
            print(now.strftime('%d.%m.%Y %H:%M:%S')," Отправлено сообщение с курсом евро/доллар пользователю", message.chat.id)
################################    ВАЛЮТА   ######################


        elif message.text == '📚 В разработке':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('💾 О боте')
            item2 = types.KeyboardButton('📦 Что в коробке?')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, '📚 В разработке', reply_markup = markup)

        elif message.text == '➡️ В разработке':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🛠 Настройки')
            item2 = types.KeyboardButton('✉️ Подписка')
            item3 = types.KeyboardButton('🧸 Стикер')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(item1, item2, item3, back)
            bot.send_message(message.chat.id, '➡️ В разработке', reply_markup = markup)

        elif message.text == '⬅️ Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🎫 Акции')
            item2 = types.KeyboardButton('🏦 Курсы валют')
            item3 = types.KeyboardButton('📚 В разработке')
            item4 = types.KeyboardButton('➡️ В разработке')
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, '⬅️ Назад', reply_markup = markup)

        elif message.text == 'Up':
            if message.chat.id == admin_id:
                Thread(target=upgrade_data2).start()
                #upgrade_data2()
                bot.send_message(admin_id, 'Обновление данных успешно произведено')


#def bot_message(message): # рассылка всем пользователям о новых акциях на ММВБ
#
#
#

#def bot_message(message): # рассылка всем пользователям о новых дивидендах
#
#
#

def upgrade_data():
    i = 1
    while i > 0:
        while True:
            try:
                TICKs()
                try: # пробуем
                    new = [(dividents_new())]
                    #print("new", new)
                    if new[0] == None: #
                        now = datetime.datetime.now()
                        print(now.strftime('%d.%m.%Y %H:%M:%S'),"Данные по дивидендам проверены и актуальны")
                    else:
                        #print("dividents_v_soobshenie(new) ",dividents_v_soobshenie(new))
                        soob = "Обнаружены данные о новых назначенных дивидендах\n"
                        for n in new:
                            new2 = dividents_v_soobshenie(new)#
                            #print("new2 ",new2)
                            for div in new2:
                                soob += div+"\n"
                                #print(soob)
                            bot.send_message(admin_id, soob)
                            now = datetime.datetime.now()
                            print(now.strftime('%d.%m.%Y %H:%M:%S')," отправлено сообщение о новых дивидендах")
                        #print("парсим")
                        dividents_parse()
                except FileNotFoundError: #
                    dividents_parse()
                now = datetime.datetime.now()
                print(now.strftime('%d.%m.%Y %H:%M:%S')," ПРОВЕРКА данных по тикерам и дивидендам успешно ЗАВЕРШЕНО")

                upgrade_data2()

                time.sleep (86400) # 1 секунда, 60 минута, 3600 час
                i+=1
            except Exception as e:
                print(f"[-] Error: {e}")
                time.sleep (600)
                print("Не подключается, ожидаем 10 минут")
                continue


def upgrade_data2():
    i = 1
    #while i > 0:
    try:
        history_parse_all()
        bot.send_message(admin_id, "Данные истории торгов загружены с ММВБ")
        now = datetime.datetime.now()
        print(now.strftime('%d.%m.%Y %H:%M:%S')," Данные истории торгов загружены с ММВБ")
        history_poisk_all_TICK()
        bot.send_message(admin_id, "Осуществлен поиск истории всех акций")
        now = datetime.datetime.now()
        print(now.strftime('%d.%m.%Y %H:%M:%S')," Осуществлен поиск истории всех акций")
        history_poisk_all_TICK_perc()
        bot.send_message(admin_id, "Создание процент")
        now = datetime.datetime.now()
        print(now.strftime('%d.%m.%Y %H:%M:%S')," Создание процент")
        history_poisk_sred_pokazatel_TICKs()
        bot.send_message(admin_id, "Создание средних показателей")
        now = datetime.datetime.now()
        print(now.strftime('%d.%m.%Y %H:%M:%S')," Создание средних показателей")
        now = datetime.datetime.now()
        print(now.strftime('%d.%m.%Y %H:%M:%S')," ОБНОВЛЕНИЕ данных ИСТОРИИ торгов акциями успешно ЗАВЕРШЕНО")
        i+=1
        time.sleep (86400)
    except:
        time.sleep (600)
        print("Не подключается, ожидаем 10 минут")
        #continue

#def job():
    #schedule.every().day.at("04:30").do()
    #upgrade_data2()

Thread(target=upgrade_data).start()
Thread(target=upgrade_data2).start()

#print(__name__)
if __name__ == "menu":
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(e)


# в except
# os.system('python "C:\ChatBot_VK\Restart.py"')
# time.sleep(1)
# quit()

 # restart.py
#os.system('python "C:\ChatBot_VK\LongPoolVK.py"')
#time.sleep(1)
#quit()
'''
