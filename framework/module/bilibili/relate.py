import hashlib

from framework.core.crawlercore.parse import JsonParseStrategy
from framework.core.crawlercore.request import SingleRequest
from framework.core.crawlercore.url import Url
from framework.tools.timedate import get_sec_time

appkey='6f90a59ac58a4123'
appsecret='0bfd84cc3940035173f35e6777508326'

class BilibiliRelateUrl(Url):
    def get_url(self, sortdict_key="default"):
        param ='aid='+str(self.request_key_param)+'&appkey='+appkey+'&build=591181&from=3&mobi_app=android&plat=0&platform=android&ts='+str(get_sec_time())
        src = param+appsecret
        m2 = hashlib.md5()
        m2.update(src.encode('utf-8'))
        return 'https://app.bilibili.com/x/v2/view?'+param+'&sign='+m2.hexdigest()
        # return 'https://app.bilibili.com/x/v2/view?aid='+str(self.request_key_param)+'&appkey=1d8b6e7d45233436&build=591181&from=3&mobi_app=android&plat=0&platform=android&trackid=2044665098629159183&ts='+str(get_sec_time())+'&sign=12133392cba096813bcb88c29f423343'


class BilibiliRelateParseStrategy(JsonParseStrategy):
    def parse(self):
        return self.parser['data']


class BilibiliRelate(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = BilibiliRelateUrl()
        self.parse_strategy = BilibiliRelateParseStrategy()
        self.headers = {'Display-ID': '6CB2E3C2-DE1F-451C-89FA-5933D6F5E9A130584infoc-1524995538',
                        'Buvid': '6CB2E3C2-DE1F-451C-89FA-5933D6F5E9A130584infoc',
                        'User-Agent': 'Mozilla/5.0 BiliDroid/blue (bbcallen@gmail.com)',
                        'Device-ID': 'HCQXckF1Fi9Je0krVysfKkgpHSscKmpaa106DT9DIhMjQiBOPVcyWi1Z',
                        'Host': 'app.bilibili.com',
                        'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
