import json
import os
import pandas as pd

# Работа с файлами
def write_json(answ_json, year):
    # Сохраняем json
    dir_out = 'out'
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    with open(f'out/{year}.json', 'w') as write_file:
        json.dump(answ_json, write_file, indent=2, ensure_ascii=False)


def read_json(file_adr):
    with open(f'out/{file_adr}', 'r') as f:
        data = json.load(f)
    return data

def read_files_list(dir):
    # Получить список файлов в папке out
    return os.listdir(dir)

def csv_to_list(file):
    # Считываем файл
    df = pd.read_csv(file, skiprows=6, sep=';', index_col=False)
    df = df[['Местное время в Москве (ВДНХ)', 'T']]
    df.columns = ['time', 'temp']

    # Отобрать данные только в 12 часов
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%Y %H:%S')
    df = df.set_index('time')
    df = df.between_time('12:00:00', '12:00:00')

    # ДатаФрейм в лист
    df.reset_index(level=0, inplace=True)
    df_list = df.values.tolist()
    # Лист в словарь и вернуть назад
    result = []
    for day in df_list:
        one_day = {}
        one_day['date'] = day[0]
        one_day['temperature'] = day[1]
        result.append(one_day)
    return result