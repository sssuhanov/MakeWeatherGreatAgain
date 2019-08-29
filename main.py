import requests
from bs4 import BeautifulSoup
import json
import os
import time

session = requests.session()

# Добавляем к сессии прокси
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

# Подменяем headers
headers = {}
headers['User-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

date_start = '19370101'
date_end = '20190829'

URL=f'https://api-ak.wunderground.com/api/75e91f5c866f39a2/history_{date_start}{date_end}/lang:EN/units:english/bestfct:1/v:2.0/q/UUWW.json'
parforget = {'showObs' : '0',
            'ttl' : '120'}

try:
    # reqObj = requests.get("https://www.wunderground.com/history/monthly/ru/moscow/UUWW/date/2013-8", timeout=10)
    r = session.get(URL, headers=headers, params=parforget)
except HTTPError as e:
    print(e)
else:
    pass

# Сохраняем json
dir_out = 'out'
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

with open('out/data.json', 'w') as write_file:
    json.dump(r.json(), write_file, indent=2, ensure_ascii=False)