import scraping
from files import read_files_list
from sql import read_weather_days
from files import csv_to_list
from sql import upload_sql

def get_weather():
    scraping.get_weather()

def get_weather_one_year():
    scraping.get_weather_one_year()

def push_weather():
    # Получить список файлов в папке out
    files_list = read_files_list('out')
    # Считываем JSON файл
    read_weather_days(files_list)

def get_weather_by_selenium():
    driver = scraping.gen_options()
    for year in range (2005, 2020):
        for month in range(1, 13):
            dates = scraping.get_from_to_date(year, month)
            scraping.download_file(driver, dates)
    driver.close()

def push_weather_selenium():
    # Читаем все файлы из папки
    files_list = read_files_list('download')
    # Берем каждый файл по очереди
    for file in files_list:
        # Считываем данные из файла
        weather_month_list = csv_to_list(f'download/{file}')
        # Записываем данные в SQL
        upload_sql(weather_month_list, 'temperature')
    pass


# Меню программы
def choiser():
    print('------------')
    print('"1316" get weather.')
    print('"2883" get weather by selenium')
    print('"3544" push weather to SQL.')
    print('"5515" push weather to SQL from selenium.')
    print('"1552" get weather only one year and insert if not exist.')
    print('"exit" for exit.')
    while True:
        x = input('Your choice: ')
        
        if x == '1316':
            get_weather()
            break
        if x == '2883':
            get_weather_by_selenium()
            break
        elif x == '3544':
            push_weather()
            break
        elif x == '5515':
            push_weather_selenium()
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