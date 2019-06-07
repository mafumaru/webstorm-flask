import json

import requests

r = requests.get("https://app.bilibili.com/x/feed/index?appkey=1d8b6e7d45233436&build=591181&idx=0&login_event=0&mobi_app=android&network=wifi&open_event=cold&platform=android&pull=true&style=2&ts=1538192742")
res = json.loads(r.text)
print('end')