import json

import requests

headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36',
            'Accept - Encoding': 'gzip, deflate'
        }

res = requests.get("https://www.zhihu.com/api/v4/answers/473336250/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order=normal&limit=20&offset=10&status=open",headers=headers)
# res.encoding='gbk'
res.encoding='utf-8'
e =res.encoding
e2 =res.apparent_encoding
r = res.text
# r = requests.get("https://www.zhihu.com/api/v4/answers/473336250/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order=normal&limit=10&offset=0&status=open",headers=headers).text
l = json.loads(r)['data'][10]['content']
print(l)
l2=l.encode(encoding = "utf-8")
print(l2)
# l3=l.encode('raw_unicode_escape').decode()
l3='贵校牛逼'.encode('utf8')
# l4='贵校牛逼'.encode('utf8')
# l3=bytearray(l)
# print(l3)
print('')