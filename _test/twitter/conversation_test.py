#https://twitter.com/HARUTYA1226/status/1036133716962115584?conversation_id=1036133716962115584
import json

import requests
from bs4 import BeautifulSoup, Tag

from framework.module.twitter.comment import twitter_comment_parse_content

headers = {'Host': 'twitter.com', 'Connection': 'keep-alive', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Overlay-Request': 'true', 'X-Requested-With': 'XMLHttpRequest', 'X-Previous-Page-Name': 'profile', 'X-Twitter-Active-User': 'yes', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Referer': 'https://twitter.com/HARUTYA1226', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8'}

r = requests.get("https://twitter.com/HARUTYA1226/status/1036133716962115584?conversation_id=1036133716962115584 ",headers=headers).text
res = json.loads(r)
soup = BeautifulSoup(res['page'])
h = soup.find('ol',id="stream-items-id").contents
data = twitter_comment_parse_content(h)
j = json.dumps(data)
print('')