import json
import re

from framework.core.crawlercore.parse import RegexJsonParseStrategy, ContextListParseStrategy
from framework.core.crawlercore.request import SingleRequest, ListSingleRequest, ListRequest
from framework.core.crawlercore.url import ContextUrl, Url


class YoutubeVideoUrl(Url):
    def get_url(self, sortdict_key="default"):
        return "https://www.youtube.com/watch?v=" + self.request_key_param


class YoutubeVideoJsonParseStratrgy(RegexJsonParseStrategy):
    def __init__(self):
        super().__init__()
        self.auth=""

    def regex_json(self, res):
        pattern = re.compile("window\[\"ytInitialData\"\]\s+=\s+(\{.*?\});")
        session = re.compile("ytcfg.set\((\{.*?\})\);")
        auth = session.search(res).group(1)
        self.auth = json.loads(auth)
        return pattern.search(res).group(1)

    def parse(self):
        context = {}
        next = self.parser["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][2][
            "itemSectionRenderer"]["continuations"][0]["nextContinuationData"]
        context["continuation"] = next["continuation"]
        context["itct"] = next["clickTrackingParams"]
        return context

    def video_info(self):
        return self.parser["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0][
            "videoPrimaryInfoRenderer"]


class YoutubeVideoRequest(SingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Host": "www.youtube.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7"
        }
        self.url = YoutubeVideoUrl()
        self.parse_strategy = YoutubeVideoJsonParseStratrgy()

class YoutubeCommentUrl(ContextUrl):

    def get_url(self, sortdict_key="default"):
        return "https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken="+self.context['continuation']+"&continuation="+self.context['continuation']+"&itct="+self.context["itct"]

class YoutubeCommentParseStrategy(ContextListParseStrategy):

    def get_total(self):
        str =  self.parser["response"]["continuationContents"]["itemSectionContinuation"]["header"]["commentsHeaderRenderer"]["commentsCount"]["simpleText"]
        return int(str)

    def parse(self):
        return self.parser["response"]["continuationContents"]["itemSectionContinuation"]['contents']

    def is_end(self):
        return not 'continuations' in  self.parser["response"]["continuationContents"]["itemSectionContinuation"].keys()

    def get_context(self):
        context = {}
        next = self.parser["response"]["continuationContents"]["itemSectionContinuation"]["continuations"][0]["nextContinuationData"]
        context["continuation"] = next["continuation"]
        context["itct"] = next["clickTrackingParams"]
        return context

class YoutubeCommentSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.url = YoutubeCommentUrl()
        self.parse_strategy = YoutubeCommentParseStrategy()
        self.post=True
        self.headers = {'Host': 'www.youtube.com', 'Connection': 'keep-alive', 'Content-Length': '280',
                        'Origin': 'https://www.youtube.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}

    def init(self,request_key_param):
        super().init(request_key_param)
        c = YoutubeVideoRequest()
        c.init(request_key_param)
        self.url.context = c.get_data()
        auth=c.parse_strategy.auth
        self.data = {
            'session_token':auth['XSRF_TOKEN']
        }
        url = "https://www.youtube.com/watch?v=" + request_key_param
        update = {
            "X-YouTube-Page-Label":auth['PAGE_BUILD_LABEL'],
            "X-YouTube-Variants-Checksum":auth['VARIANTS_CHECKSUM'],
            "X-YouTube-Page-CL":str(auth['PAGE_CL']),
            "X-SPF-Referer":url,
            "X-SPF-Previous":url,
            "Referer":url,
            "X-YouTube-Client-Version":auth['INNERTUBE_CONTEXT_CLIENT_VERSION'],
            "X-YouTube-Utc-Offset": "480",
            "X-YouTube-Client-Name": "1"
        }
        self.headers.update(update)
        self.cookies=c.get_cookies
        self.g=c.parse_strategy.video_info()

    def glance(self,father:ListRequest):
        father.datacore.rowdata=self.g


class YoutubeComment(ListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = YoutubeCommentSingleRequest()