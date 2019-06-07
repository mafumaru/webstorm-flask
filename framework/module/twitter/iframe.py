from framework.core.crawlercore.parse import JsonParseStrategy
from framework.core.crawlercore.request import SingleRequest
from framework.core.crawlercore.url import Url
from framework.module.twitter.comment import sep


class TwitterIframeUrl(Url):
    def get_url(self, sortdict_key="default"):
        return "https://api.twitter.com/1/statuses/oembed.json?hide_media=false&hide_thread=false&id="+ self.request_key_param+"&lang=zh-cn"


class TwitterIframeParseStrategy(JsonParseStrategy):
    def parse(self):
        return self.parser['html']


class TwitterIframe(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = TwitterIframeUrl()
        self.parse_strategy = TwitterIframeParseStrategy()
        self.headers = {'Host': 'api.twitter.com', 'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
