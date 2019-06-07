from framework.core.crawlercore.request import ListSingleRequest
from framework.core.crawlercore.url import ListUrl
from framework.module.zhihu.share import AnswerListParseStrategy, ZhihuListRequest


class ZhihuPeopleUrl(ListUrl):

    def __init__(self):
        super().__init__()
        self.sort = {
            'created':'created',
            'default':'voteups'
        }

    def get_url(self, sortdict_key="default"):
        return "https://www.zhihu.com/api/v4/members/"+self.request_key_param+"/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset="+str(self.offset)+"&limit="+str(self.limit)+"&sort_by="+self.sort.get(sortdict_key)

class ZhihuPeopleSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36'
        }
        self.url = ZhihuPeopleUrl()
        self.parse_strategy = AnswerListParseStrategy()

class ZhihuPeople(ZhihuListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = ZhihuPeopleSingleRequest()
