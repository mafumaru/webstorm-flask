# https://twitter.com/i/profiles/show/Chalilili/timeline/tweets?include_available_features=1&include_entities=1&max_position=728073447494983683&reset_error_state=false
import json

import requests
from bs4 import BeautifulSoup, Tag

headers = {'Host': 'twitter.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
r = requests.get("https://twitter.com/i/profiles/show/Chalilili/timeline/tweets?include_available_features=1&include_entities=1&max_position=728073447494983683&reset_error_state=false",headers=headers)
res = json.loads(r.text)['items_html']
soup = BeautifulSoup(res,"lxml")
list = soup.body.contents
listdata = []
for item in list:
    if isinstance(item,Tag):
        data = {
            'id':item['data-item-id'],
            'html':item.find('div','content').prettify()
        }
        listdata.append(data)
print('end')