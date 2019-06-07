import json

from bs4 import Tag

from framework.core.crawlercore.parse import HtmlListParseStrategy
from framework.core.crawlercore.request import ListSingleRequest, ListRequest
from framework.core.crawlercore.url import PageUrl
from framework.tools.timedate import get_ms_time


def update_tie_content(tag:Tag, table_name, id):
    imgs = tag.find_all('img')
    for img in imgs:
        l = list(set(img.get('class', []) + ['img-rounded', 'img-responsive']))
        if 'icon-jubao' in l:
            img.extract()
            continue
        img['class']= l
        src = img.get('data-tb-lazyload')
        if src:
            img['src'] = src

    return tag

class TieUrl(PageUrl):
    def get_url(self, sortdict_key="default"):
        return 'https://tieba.baidu.com/p/'+self.request_key_param+'?pn='+str(self.offset)+'&ajax=1&t='+str(get_ms_time())

class TieParseStrategy(HtmlListParseStrategy):
    def is_end(self):
        return self.offset>self.get_total()

    def set_parser(self, res):
        return super().set_parser(res)

    def parse(self):
        res = self.parser.find('div', id='ajax-content').find_all('div', class_='j_l_post')

        listdata = []
        for item in res:
            d = item['data-field'].replace('\\\\', '\\')
            jd = json.loads(d)
            content = jd['content']
            mix_id = self.request_key_param+'-'+str(content['post_id'])
            data = {
                'tid':int(self.request_key_param),
                'floor_num': content['post_no'],
                'mix_id':mix_id,
                'post_id':content['post_id'],
                'content':content,
                'html': update_tie_content(item, self.request_key_param, mix_id).prettify()
            }
            listdata.append(data)
        return listdata

    def get_total(self):
        max = self.parser.find('input',class_='jump_input_bright')
        return int(max.get('max-page'))
    
class TieSingleRequest(ListSingleRequest):
    def init(self, request_key_param):
        super().init(request_key_param)

    def __init__(self):
        super().__init__()
        self.headers={'Host': 'tieba.baidu.com', 'Connection': 'keep-alive', 'Accept': 'text/html, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
        self.url=TieUrl()
        self.parse_strategy=TieParseStrategy()

class Tie(ListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request=TieSingleRequest()