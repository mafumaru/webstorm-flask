from framework.core.crawlercore.parse import ListParseStrategy
from framework.core.crawlercore.request import ListSingleRequest, IntervalListRequest
from framework.core.crawlercore.url import PageUrl


class WuxiaworldCommentUrl(PageUrl):
    def get_url(self, sortdict_key="default"):
        return "https://www.wuxiaworld.com/api/comments/"+self.request_key_param+"/top?page="+str(self.offset)

class WuxiaworldCommentParseStrategy(ListParseStrategy):
    def get_total(self):
        return self.parser['total']

    def is_end(self):
        return len(self.parser['items'])==0

    def parse(self):
        return self.parser['items']

    def is_right(self):
        return 'items' in self.parser.keys()


class WuxiaworldCommentSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {'Host': 'www.wuxiaworld.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache', 'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                        'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
                        'Cookie': '__cfduid=dd6ac8f0b70978d38814d78075c566c4e1545389758; _ga=GA1.2.2117771054.1545389768; _gid=GA1.2.1909350696.1545389768; __asc=013d5e90167d068a3e75d976d99; __auc=013d5e90167d068a3e75d976d99; m2hb=enabled; __gads=ID=5bf229d51e5a7995:T=1545389790:S=ALNI_MaJcB-hx4nfDFZrWNmbJbxOsfEJtg; session_depth=2; _gat=1'}
        self.url = WuxiaworldCommentUrl()
        self.parse_strategy = WuxiaworldCommentParseStrategy()

class WuxiaworldComment(IntervalListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = WuxiaworldCommentSingleRequest()
        self.interval=2.5

