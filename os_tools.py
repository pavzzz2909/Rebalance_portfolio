import os

def mk_dir(dir):
    ''' Создание директории '''
    if os.path.isdir(dir) !=True:
        os.mkdir(dir)


def list_dir():
    ''' Функция которая возращает названия файлов в директории my_files '''
    dir = "my_files/"
    files2 = []
    files = os.listdir(dir)
    for file in files:
        file = dir+file
        files2.append(file)
    return files2


def list_dir_sber():
    ''' Функция которая возращает названия файлов в директории my_files '''
    dir = "my_files/Sber/"
    files2 = []
    files = os.listdir(dir)
    for file in files:
        file = dir+file
        files2.append(file)
    return files2
