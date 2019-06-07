from framework.core.crawlercore.parse import JsonParseStrategy
from framework.core.crawlercore.request import SingleRequest
from framework.core.crawlercore.url import Url


class ZhihuAnswerUrl(Url):
    def get_url(self, sortdict_key="default"):
        return "https://api.zhihu.com/answers/" + self.request_key_param


class ZhihuAnswerParseStrategy(JsonParseStrategy):
    def parse(self):
        return self.parser


class ZhihuAnswer(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = ZhihuAnswerUrl()
        self.parse_strategy = ZhihuAnswerParseStrategy()
        self.headers = {
            'User-Agent': 'com.zhihu.android/Futureve/5.30.1 Mozilla/5.0 (Linux; Android 5.1; m1 metal Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.146 Mobile Safari/537.36',
            'x-api-version': '3.0.76', 'x-app-version': '5.30.1',
            'x-app-za': 'OS=Android&Release=5.1&Model=m1+metal&VersionName=5.30.1&VersionCode=999&Product=com.zhihu.android&Width=1080&Height=1920&Installer=%E9%AD%85%E6%97%8F%E5%BA%94%E7%94%A8%E5%95%86%E5%BA%97&DeviceType=AndroidPhone&Brand=Meizu',
            'x-app-flavor': 'meizu', 'x-app-build': 'release', 'x-network-type': 'WiFi', 'Host': 'api.zhihu.com',
            'Connection': 'Keep-Alive'}
