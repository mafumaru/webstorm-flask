import requests
from bs4 import BeautifulSoup

headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36'
        }

r = requests.get("https://www.zhihu.com/collection/29475875",headers=headers).text
soup = BeautifulSoup(r)
t:str = soup.title.text.split('-')[0]
title = t.strip()
print('')