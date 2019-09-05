import sqlalchemy as db
from files import read_json

# Работа с SQL
def upload_sql(all_days_weather_list, table):
    # Подключаемся к базе и считываем данные
    engine = db.create_engine('postgresql://postgres:kilo98ui@localhost/weather')
    connection = engine.connect()
    metadata = db.MetaData()
    observ = db.Table(table, metadata, autoload=True, autoload_with=engine)

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