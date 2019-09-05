import requests
from bs4 import BeautifulSoup
import json
import os
import time
import sqlalchemy as db


# Скрапинг
def do_session():
    session = requests.session()

    # Добавляем к сессии прокси
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    return session

def month_str(month):
    month = str(month)
    if len(month) == 1:
        month = ''.join(['0',month])
    return month

def get_params_for_req(year, month):
    params = {}
    # Подменяем headers
    params['headers'] = {}
    params['headers']['User-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

    if month == 12:
        date_start = f'{year}{month_str(month)}01'
        date_end = f'{year+1}0101'
    else:
        date_start = f'{year}{month_str(month)}01'
        date_end = f'{year}{month_str(month+1)}01'

    params['URL']=f'https://api-ak.wunderground.com/api/75e91f5c866f39a2/history_{date_start}{date_end}/lang:EN/units:english/bestfct:1/v:2.0/q/UUWW.json'
    params['parforget'] = {'showObs': '0',  'ttl': '120'}
    params['year'] = year
    params['month'] = month
    
    return params

def do_request(session, params):
    try:
        r = session.get(params['URL'], headers=params['headers'], params=params['parforget'])
    except HTTPError as e:
        print(e)
    else:
        pass
    write_json(r.json(), f'{params["year"]}-{params["month"]}')

def get_weather():
    for year in range(1937,2020):
        for month in range(1, 13):
            print(f'start {year}-{month}')
            session = do_session()
            params = get_params_for_req(year, month)
            do_request(session, params)
            print(f'end {year}-{month}')
            time.sleep(10)

def get_weather_one_year():
    # Определяем какой год будет обновляться
    year = input('year for update: ')
    try:
        year = int(year)
        if year < 1937 or year > 2019:
            raise Exception("Год не попадает в возможные промежутки")
    except Exception as e:
        print(e)
        exit()
    
    print(f'start {year}')

    # Получаем данные по году
    session = do_session()
    params = get_params_for_req(year)
    do_request(session, params)
    
    # Обновляем данные в SQL
    read_weather_day(f'{year}.json')

    print(f'end {year}')


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


# Работа с SQL
def upload_sql(all_days_weather_list):
    # Подключаемся к базе и считываем данные
    engine = db.create_engine('postgresql://postgres:kilo98ui@localhost/weather')
    connection = engine.connect()
    metadata = db.MetaData()
    observ = db.Table('observ', metadata, autoload=True, autoload_with=engine)

    # Формируем запрос
    query = db.dialects.postgresql.insert(observ)
    do_nothing_query = query.on_conflict_do_nothing()

    # Отправляем запрос к серверу
    ResultProxy = connection.execute(do_nothing_query, all_days_weather_list)
    
def read_weather_day(json_file):
    
    weather = read_json(json_file)

    all_days_weather_list = []

    for weather_day in weather['history']['days']:
        # Достаем из файла необходимые данные в удобном формате
        data_weather_day = {}
        # Дату
        year = weather_day['summary']['date']['year']
        month = weather_day['summary']['date']['month']
        day = weather_day['summary']['date']['day']
        data_weather_day['date'] = f'{year}-{month}-{day}'

        # показатели погоды
        list_of_params = ['temperature', 'dewpoint', 'pressure', 'wind_speed',
                            'visibility', 'max_temperature', 'min_temperature',
                            'max_dewpoint', 'min_dewpoint', 'max_humidity',
                            'min_humidity', 'max_wind_speed', 'min_wind_speed',
                            'max_pressure', 'min_pressure', 'max_visibility',
                            'min_visibility', 'rain', 'snow', 'fog', 'hail',
                            'thunder', 'tornado', 'snowfall']
        
        for param in list_of_params:
            data_weather_day[param] = weather_day['summary'][param]
        
        all_days_weather_list.append(data_weather_day)

    # Подключаемся к SQL и записываем данные
    if len(all_days_weather_list) > 0:
        upload_sql(all_days_weather_list)
        print(f'{json_file} в базу записан')
    else:
        print(f'{json_file} пустой, пропущен')

def read_weather_days(files_list):
    for json_file in files_list:

        read_weather_day(json_file)

def push_weather():
    # Получить список файлов в папке out
    files_list = os.listdir('out')
    # Считываем JSON файл
    read_weather_days(files_list)


# Меню программы
def choiser():
    print('------------')
    print('"1316" get weather.')
    print('"3544" push weather to SQL.')
    print('"1552" get weather only one year and insert if not exist.')
    print('"exit" for exit.')
    while True:
        x = input('Your choice: ')
        
        if x == '1316':
            get_weather()
            break
        elif x == '3544':
            push_weather()
            break
        elif x == '1552':
            get_weather_one_year()
            break
        elif x == 'exit':
            exit()
        else:
            pass   

def main():
    choiser()

if __name__ == "__main__":
    main()