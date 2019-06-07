from framework.core.crawlercore.request import ListSingleRequest
from framework.core.crawlercore.url import ListUrl
from framework.module.zhihu.share import AnswerListParseStrategy, ZhihuListRequest


class ZhihuQuestionUrl(ListUrl):

    def __init__(self):
        super().__init__()
        self.sort = {
            'created':'created',
            'default':'voteups'
        }

    def get_url(self, sortdict_key="default"):
        return "https://www.zhihu.com/api/v4/questions/"+self.request_key_param+"/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit="+str(self.limit)+"&offset="+str(self.offset)+"&sort_by="+self.sort.get(sortdict_key)

class ZhihuQuestionParseStrategy(AnswerListParseStrategy):
    def is_end(self):
        # print(self.offset)
        # print(self.offset<1200) # t
        # print(super().is_end()) # f
        # print(super().is_end() and self.offset<1200) # f
        return super().is_end() or self.offset>1200


class ZhihuQuestionSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36'
        }
        self.url = ZhihuQuestionUrl()
        self.parse_strategy = ZhihuQuestionParseStrategy()

class ZhihuQuestion(ZhihuListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = ZhihuQuestionSingleRequest()

