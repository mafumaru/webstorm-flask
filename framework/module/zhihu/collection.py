import requests
from bs4 import BeautifulSoup

from framework.core.crawlercore.request import ListSingleRequest
from framework.core.crawlercore.url import ListUrl
from framework.module.zhihu.share import ZhihuListRequest, AnswerListParseStrategy


class ZhihuCollectionUrl(ListUrl):
    def get_url(self, sortdict_key="default"):
        return "https://api.zhihu.com/collections/"+self.request_key_param+"/contents?offset="+str(self.offset)

class ZhihuCollectionParseStrategy(AnswerListParseStrategy):

    def get_total(self):
        return 10000

class ZhihuCollectionSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.url = ZhihuCollectionUrl()
        self.parse_strategy = ZhihuCollectionParseStrategy()
        self.headers = {
            'User-Agent': 'com.zhihu.android/Futureve/5.30.1 Mozilla/5.0 (Linux; Android 5.1; m1 metal Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.146 Mobile Safari/537.36',
            'x-api-version': '3.0.76', 'x-app-version': '5.30.1',
            'x-app-za': 'OS=Android&Release=5.1&Model=m1+metal&VersionName=5.30.1&VersionCode=999&Product=com.zhihu.android&Width=1080&Height=1920&Installer=%E9%AD%85%E6%97%8F%E5%BA%94%E7%94%A8%E5%95%86%E5%BA%97&DeviceType=AndroidPhone&Brand=Meizu',
            'x-app-flavor': 'meizu', 'x-app-build': 'release', 'x-network-type': 'WiFi', 'Host': 'api.zhihu.com',
            'Connection': 'Keep-Alive'}

    def init(self, request_key_param):
        super().init(request_key_param)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36'
        }

        r = requests.get("https://www.zhihu.com/collection/29475875", headers=headers).text
        soup = BeautifulSoup(r)
        t: str = soup.title.text.split('-')[0]
        title = t.strip()
        self.g =  {'title':title}

    def glance(self, father):
        father.datacore.rowdata=self.g

class ZhihuCollection(ZhihuListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = ZhihuCollectionSingleRequest()
