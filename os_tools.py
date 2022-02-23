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



def list_one_dir_sber():
    dir = "my_files/Sber/"
    files = []
    dirs = []
    prefs = []
    forms = []
    files2 = os.listdir(dir)
    for file in files2:
        if '.' in file:
            format_f = file.split('.')[len(file.split('.'))-1]
            if format_f not in forms:
                forms.append(format_f)
            filename = file.split('.')[0]
            if '-' in filename:
                filename = filename.split('-')[0]
                if filename not in prefs:
                    prefs.append(filename)
            file = dir+file
            files.append(file)
        else:
            file = dir+file+'/'
            dirs.append(file)
    return dirs, files, prefs, forms
