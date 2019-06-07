from framework.core.crawlercore.parse import JsonParseStrategy, ListParseStrategy
from framework.core.crawlercore.request import SingleRequest, ListSingleRequest
from framework.core.crawlercore.url import Url, PageUrl
from framework.module.weibo.share import WeiboListRequest


class ContainerUrl(Url):

    def get_url(self, sortdict_key="default"):
        return "https://m.weibo.cn/api/container/getIndex?type=uid&value="+self.request_key_param

class ContainerParseStrategy(JsonParseStrategy):
    def parse(self):
        container= self.parser['data']['tabsInfo']['tabs']
        if isinstance(container,list):
            container = container[1]['containerid']
        elif isinstance(container,dict):
            container = container['1']['containerid']
        else:
            container = 'wrong container'
        return container

    def user_info(self):
        return self.parser['data']['userInfo']

class ContainerRequest(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = ContainerUrl()
        self.parse_strategy = ContainerParseStrategy()

class WeiboUserUrl(PageUrl):

    def __init__(self):
        super().__init__()
        self.container=""

    def get_url(self,sortdict_key="default"):
        return "https://m.weibo.cn/api/container/getIndex?type=uid&value=" + self.request_key_param+"&containerid="+self.container+"&page="+str(self.offset)
        # return "https://m.weibo.cn/api/container/getIndex?type=uid&value=5500878881&containerid=1076035500878881&page=5"
        # return "https://m.weibo.cn/api/container/getIndex?type=uid&value=5500878881&containerid=1076035500878881&page=3"

class WeiboUserParseStrategy(ListParseStrategy):

    def parse(self):
        return self.parser['data']['cards']

    def is_end(self):
        return self.parser['data']['cardlistInfo']['page']==None

    def get_total(self):
        return self.parser['cardlistInfo']['total']

    def is_right(self):
        return self.parser['ok']==1


class WeiboUserSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.url = WeiboUserUrl()
        self.parse_strategy=WeiboUserParseStrategy()

    def init(self, request_key_param):
        super().init(request_key_param)
        c = ContainerRequest()
        c.init(request_key_param)
        self.url.container = c.get_data()


class WeiboUser(WeiboListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = WeiboUserSingleRequest()

