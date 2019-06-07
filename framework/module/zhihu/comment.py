from framework.core.crawlercore.request import ListSingleRequest
from framework.module.zhihu.answer import ZhihuAnswer
from framework.module.zhihu.share import AnswerListParseStrategy, ZhihuListRequest
from framework.core.crawlercore.url import ListUrl

class ZhihuCommentUrl(ListUrl):

    def __init__(self):
        super().__init__()
        self.sort = {
            'default':'normal'
        }
        # self.limit=100

    def get_url(self, sortdict_key="default"):
               # https://www.zhihu.com/api/v4/answers/33643757/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order=normal&limit=20&offset=0&status=open
        # return "https://www.zhihu.com/api/v4/answers/"+self.request_key_param+"/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order="+self.sort.get(sortdict_key)+"&limit=10&offset="+str(self.offset)+"&status=open"
        return "https://www.zhihu.com/api/v4/answers/"+self.request_key_param+"/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order="+self.sort.get(sortdict_key)+"&limit="+str(self.limit)+"&offset="+str(self.offset)+"&status=open"
        # return "https://www.zhihu.com/api/v4/answers/"+self.request_key_param+"/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order="+self.sort.get(sortdict_key)+"&limit="+str(self.limit)+"&offset="+str(self.offset)+"&status=open"

class CommentListParseStrategy(AnswerListParseStrategy):

    def __init__(self):
        super().__init__()

class ZhihuCommentSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36',
            # 'Accept-Language':' zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
            # 'content-type':' application/json',
            # 'content-encoding':'br',
            # 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'accept-language':' zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
            'Accept - Encoding': 'gzip, deflat'
        }
        # self.headers = {'Host': 'www.zhihu.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
        self.url = ZhihuCommentUrl()
        self.parse_strategy = CommentListParseStrategy()

    def request(self):
        res= super().request()
        res.encoding = 'utf-8'
        return res

    def init(self, request_key_param):
        super().init(request_key_param)
        c = ZhihuAnswer()
        c.init(request_key_param)
        self.g =  c.get_data()

    def glance(self, father):
        father.datacore.rowdata=self.g

class ZhihuComment(ZhihuListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = ZhihuCommentSingleRequest()

