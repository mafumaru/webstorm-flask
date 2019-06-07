import re
import requests

url = 'https://www.youtube.com/watch?v=vjF9GgrY9c0'
headers = {
    "Host": "www.youtube.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7"
}
r = requests.get(url, headers=headers)
cookie = r.cookies.get_dict()
pattern = re.compile("window\[\"ytInitialData\"\]\s+=\s+(\{.*\});")
data = pattern.search(r.text).group(1)
session = re.compile("ytcfg.set\((\{.*?\})\);")
session_token = session.search(r.text).group(1)
print('end')
