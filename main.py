import requests
from bs4 import BeautifulSoup
import json
import os
import time


def do_session():
    session = requests.session()

    # Добавляем к сессии прокси
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    return session

def get_params_for_req(year):
    params = {}
    # Подменяем headers
    params['headers'] = {}
    params['headers']['User-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

    date_start = f'{year}0101'
    date_end = f'{year}1231'

    params['URL']=f'https://api-ak.wunderground.com/api/75e91f5c866f39a2/history_{date_start}{date_end}/lang:EN/units:english/bestfct:1/v:2.0/q/UUWW.json'
    params['parforget'] = {'showObs' : '0',  'ttl' : '120'}   
    params['year'] = year
    
    return params

def write_json(answ_json, year):
    # Сохраняем json
    dir_out = 'out'
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    with open(f'out/{year}.json', 'w') as write_file:
        json.dump(answ_json, write_file, indent=2, ensure_ascii=False)

def do_request(session, params):
    try:
        r = session.get(params['URL'], headers=params['headers'], params=params['parforget'])
    except HTTPError as e:
        print(e)
    else:
        pass
    write_json(r.json(), params['year'])

def main():
    for year in range(1937,2020):
        print(f'start {year}')
        session = do_session()
        params = get_params_for_req(year)
        do_request(session, params)
        print(f'end {year}')
        time.sleep(10)

if __name__ == "__main__":
    main()