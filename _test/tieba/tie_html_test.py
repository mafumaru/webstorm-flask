import json
import re
import requests
from bs4 import BeautifulSoup

headers={'Host': 'tieba.baidu.com', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
req = requests.get('https://tieba.baidu.com/f?kw=bilibili&ie=utf-8&pn=100&pagelets=frs-list%2Fpagelet%2Fthread&pagelets_stamp=1548212660289',headers=headers)
soup = BeautifulSoup(req.text)
res = self.parser.find('div', id='ajax-content').find_all('div', class_='j_l_post')
j=res[0]
d = j['data-field'].replace('\\\\','\\')
jd = json.loads(d)
# print(r)
print('')