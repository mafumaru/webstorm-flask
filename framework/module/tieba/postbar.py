import json
import re

from bs4 import Tag, BeautifulSoup

from framework.core.crawlercore.parse import JsObjectHtmlListParseStrategy
from framework.core.crawlercore.request import ListSingleRequest, ListRequest
from framework.core.crawlercore.url import ListUrl
from framework.tools.timedate import get_ms_time

def update_content(tag:Tag,table_name,id):
    # li = tag.find('li', class_='j_thread_list')
    li = tag

    li['class'] = list(set(li.get('class', []) + ['list-group-item', 'list_item']))
    li['id']=id
    button = li.find('button',class_='postbar_mark_btn')
    if not button:
        btn = BeautifulSoup().new_tag('button')
        btn['data-id']=id
        btn['class']=['postbar_mark_btn','btn','btn-danger']
        btn.string ='Mark'
        li.append(btn)

    title = tag.find('a', class_='j_th_tit')
    title['href']='http://tieba.baidu.com/p/'+str(id)
    imgs = tag.find_all('img',class_='nicknameEmoji')
    for img in imgs:
        img.extract()
    imgs = tag.find_all('img')
    for img in imgs:
        img['class']= list(set(img.get('class', []) + ['img-rounded','img-responsive']))
        src = img.get('bpic')
        if src:
            img['src'] = src

    ul:Tag = tag.find('ul',class_='j_threadlist_media')
    if ul:
        ul['class'] = list(set(ul.get('class', []) + ['row']))
        lis = ul.find_all('li')
        for li in lis:
            li['class']= ['col-xs-4']

    return tag

class PostbarUrl(ListUrl):
    def __init__(self):
        super().__init__()
        self.offset=0
        self.limit=50

    def get_url(self, sortdict_key="default"):
        return 'https://tieba.baidu.com/f?kw='+self.request_key_param+'&ie=utf-8&pn='+str(self.offset)+'&pagelets=frs-list%2Fpagelet%2Fthread&pagelets_stamp='+str(get_ms_time())

class PostbarParseStrategy(JsObjectHtmlListParseStrategy):
    def __init__(self):
        super().__init__()
        self.identity=get_ms_time()

    def is_end(self):
        return self.offset>=1000

    def regex_html(self, res):
        pattern = re.compile('thread_list",(.+?,")', re.S)
        content = pattern.search(res).group(1)
        pattern = re.compile('{"content":"(.+?)","', re.S)
        html = pattern.search(content).group(1)
        last_html= html.encode('latin-1').decode('unicode_escape')
        final_html = last_html.replace('\\n', '').replace('\\r', '').replace('\\"', '"').replace('\\/', '/')
        return final_html

    def get_total(self):
        pass

    def parse(self):
        html_list = self.parser.find('ul',id='thread_list').find_all('li',class_='j_thread_list')
        listdata = []
        for item in html_list:
            d = item['data-field'].replace('\\\\', '\\')
            jd = json.loads(d)
            data = {
                'id': jd['id'],
                'identity': self.identity,
                'm_identity':0,
                'reply_count':jd['reply_num'],
                'html': update_content(item, self.request_key_param,jd['id']).prettify()
            }
            listdata.append(data)
        return listdata


class PostbarSingleRequest(ListSingleRequest):
    def init(self, request_key_param):
        super().init(request_key_param)

    def __init__(self):
        super().__init__()
        self.headers={'Host': 'tieba.baidu.com', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
        self.url=PostbarUrl()
        self.parse_strategy=PostbarParseStrategy()

class Postbar(ListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.list_single_request=PostbarSingleRequest()

    def get_lists(self):
        super().get_lists()
