from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from files import write_json
from sql import read_weather_day

def gen_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome-beta"

    prefs = {"download.default_directory": "/home/sss/dev/python/19-08-22_MakeWeatherGreatAgain/download/"}
    chrome_options.add_experimental_option("prefs", prefs)

    # Чтобы работала в фоне, но файлы сохраняются только в папку с программой
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_from_to_date(year, month):
    dates = {}
    str_month = str(month)
    if len(str_month) == 1:
        str_month = ''.join(['0', str_month])
    dates['from_date'] = f'01.{str_month}.{year}'

    if month == 12:
        next_month = 1
        next_year = year+1
    else:
        next_month = month + 1
        next_year = year

    str_next_month = str(next_month)
    if len(str_next_month) == 1:
        str_next_month = ''.join(['0', str_next_month])


    dates['to_date'] = f'01.{str_next_month}.{next_year}'

    return dates


def download_file(driver, dates):
    print(f'start: {dates["from_date"]}')

    dontstop = True

    while dontstop:
        driver.get(
            "https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5_(%D0%92%D0%94%D0%9D%D0%A5)")
        elem = driver.find_element_by_id('tabSynopDLoad')
        time.sleep(1)
        elem.click()
        elem = driver.find_element_by_id('calender_dload')
        elem.clear()
        # elem.send_keys('01.01.2019')
        elem.send_keys(dates['from_date'])
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_id('calender_dload2')
        elem.clear()
        # elem.send_keys('01.02.2019')
        elem.send_keys(dates['to_date'])
        elem.send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//div[@id='toFileMenu']/form/table[2]/tbody/tr[2]/td[3]/label").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Выбрать в файл GZ (архив)'])\
            [1]/preceding::label[2]").click()
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='—'])[2]/preceding::div[2]").click()
        time.sleep(5)
        try:
            driver.find_element_by_link_text(u"Скачать").click()
        except Exception as e:
            continue
        else:
            dontstop = False

        time.sleep(10)
        print(f'end: {dates["from_date"]}')


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
        month = ''.join(['0', month])
    return month


def get_params_for_req(year, month):
    params = {}
    # Подменяем headers
    params['headers'] = {}
    params['headers'][
        'User-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

    if month == 12:
        date_start = f'{year}{month_str(month)}01'
        date_end = f'{year + 1}0101'
    else:
        date_start = f'{year}{month_str(month)}01'
        date_end = f'{year}{month_str(month + 1)}01'

    params[
        'URL'] = f'https://api-ak.wunderground.com/api/75e91f5c866f39a2/history_{date_start}{date_end}/lang:EN/units:english/bestfct:1/v:2.0/q/UUWW.json'
    params['parforget'] = {'showObs': '0', 'ttl': '120'}
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
    for year in range(1937, 2020):
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


def main():
    driver = gen_options()
    download_file(driver)


if __name__ == '__main__':
    main()
