import datetime
import time                             # импорт времени
from pytz import timezone

def Now_date_in_integer_for_dividents():
    ''' Используется в дивидендах '''
    now = datetime.datetime.now()
    Ynow = str(now.year)
    Mnow  = str(now.month)
    Dnow = str(now.day)
    Datenow =Ynow+"-"+Mnow+"-"+Dnow
    Datedays = now.year*365+now.month*365/12+now.day
    return Datedays

def Date_in_integer_for_dividents(date):
    ''' Используется в дивидендах '''
    return int(date.split('-')[0])*365+int(date.split('-')[1])*365/12+int(date.split('-')[2])

def now_year():
    '''  Возвращает текущий год  '''
    now = get_now()
    return int(str(now.year))


def localize(d: datetime) -> datetime:
    ''' используется в TICKs '''
    return timezone('Asia/Yekaterinburg').localize(d)

def get_now() -> datetime:
    ''' используется в TICKs '''
    return localize(datetime.datetime.now())
