from urllib.parse import quote

from framework.core.crawlercore.parse import ContextListParseStrategy
from framework.core.crawlercore.request import ListSingleRequest
from framework.core.crawlercore.url import ContextUrl
from framework.module.zhihu.share import ZhihuListRequest


class ZhihuSearchUrl(ContextUrl):

    def get_url(self, sortdict_key="default"):
        if self.offset==0:
            return 'https://www.zhihu.com/api/v4/search_v3?q='+quote(self.request_key_param)+'&t=general&correction=1&offset=0&advert_count=0&limit='+str(self.limit)+'&excerpt_len=50'
        else:
            return "https://www.zhihu.com/api/v4/search_v3?q="+quote(self.request_key_param)+"&t=general&correction=1&offset="+str(self.offset)+"&advert_count=0&limit="+str(self.limit)+"&excerpt_len=50&search_hash_id="+str(self.context)+"&vertical_info=1%2C1%2C0%2C0%2C0%2C1%2C0%2C1%2C0"

class ZhihuSearchParseStrategy(ContextListParseStrategy):
    def get_context(self):
        return self.parser['search_action_info']['search_hash_id']

    def parse(self):
        list_data = []
        for item in self.parser['data']:
            if item['type'] == 'search_result' and item['object']['type'] =='answer':
                list_data.append(item['object'])
            else:
                continue
        return list_data

    def is_end(self):
        return self.parser['paging']['is_end']

    def get_total(self):
        return 10000

class ZhihuSearchSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {'Host': 'www.zhihu.com', 'Connection': 'keep-alive', 'x-hybrid': '1', 'x-app-version': '5.15.1',
                        'x-api-version': '3.0.91', 'x-network-type': 'WiFi',
                        'authorization': 'Bearer gt2.0AAAAAAck18AM7p4hBuEAAAAAAAxNVQJgAgD106JaTaaqyi-GkDhOTsKDpNYx1Q==',
                        'accept': 'application/json, text/plain, */*',
                        'x-udid': 'AADhBiGe7gxLBRpED6VCzidmUci2ZciRLiw=,AADhBiGe7gxLBRpED6VCzidmUci2ZciRLiw=',
                        'User-Agent': 'ZhihuHybrid com.zhihu.android/Futureve/5.15.1 Mozilla/5.0 (Linux; Android 5.1; m1 metal Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.2214.121 Mobile Safari/537.36',
                        'x-app-za': 'OS=Android&Release=5.1&Model=m1+metal&VersionName=5.15.1&VersionCode=658&Width=1080&Height=1920&Installer=%E9%AD%85%E6%97%8F%E5%BA%94%E7%94%A8%E4%B8%AD%E5%BF%83&DeviceType=AndroidPhone&Brand=Meizu',
                        'Referer': 'https://www.zhihu.com/appview/search/general?config=%7B%22is_dark_theme%22%3Afalse%2C%22search_type_panel_types%22%3A%22%5Bgeneral%2C+people%2C+topic%2C+pin%2C+column%2C+live%2C+publication%2C+album%5D%22%2C%22search_tab%22%3A%22collapsed%22%7D',
                        'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
                        'X-Requested-With': 'com.zhihu.android'}
        self.url = ZhihuSearchUrl()
        self.parse_strategy= ZhihuSearchParseStrategy()

class ZhihuSearch(ZhihuListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request = ZhihuSearchSingleRequest()


