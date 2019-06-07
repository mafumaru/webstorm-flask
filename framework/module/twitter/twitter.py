import re
from bs4 import Tag, BeautifulSoup

from framework.core.crawlercore.parse import HtmlParseStrategy, ContextListParseStrategy
from framework.core.crawlercore.request import SingleRequest, ListSingleRequest, ListRequest, IntervalListRequest
from framework.core.crawlercore.url import Url, ContextUrl

def update_content(tag:Tag,table_name,id):
    collection_tag = tag.find('span','ProfileTweet-action--favorite')
    collection_tag['data-toggle']="modal"
    collection_tag['data-target']="#collection_choose"
    collection_tag['data-type']="twitter_twitter"
    collection_tag['data-table_name']=table_name
    collection_tag['data-id']=id

    media_tag = tag.find('div','PlayableMedia-player')
    if media_tag:
        img_url = re.findall('url\(\'(.*?)\'\)', media_tag['style'])
        img_tag = BeautifulSoup().new_tag('img', src=img_url[0])
        media_tag.replace_with(img_tag)

    imgs = tag.find_all('img')
    for img in imgs:
        img['style']=''
        img['class']= img.get('class', []) + ['img-rounded','img-responsive','center-block']
        # img['class']= img['class']+'img-thumbnail'

    header = tag.find('div', 'stream-item-header')
    a_tags = header.find_all('a')
    for a_tag in a_tags:
        del a_tag['href']

    # p = tag.find_all('p','tweet-text')
    # for item in p:
    #     text = "".join([str(x) for x in item.contents])
    #     clear = text.strip()
    #     print(text)
    #     print(text.strip())
    #     print(clear)
    #     item.clear()
    #     item.string=clear

    reply=tag.find('span','ProfileTweet-action--reply')
    reply['class']= reply.get('class', []) + ['btn','btn-info']
    reply.wrap(BeautifulSoup().new_tag("a",href="/module/twitter/view/TwitterCommentRealtimeView/render?name="+table_name+'-'+id))
    # reply['class']= reply['class']+'btn btn-info'
    retweet=tag.find('span','ProfileTweet-action--retweet')
    retweet['class']= retweet.get('class', []) + ['btn','btn-warning']
    retweet['data-table_name'] = table_name
    retweet['data-id'] = id
    # retweet['class']= retweet['class']+'btn btn-warning'
    favorite=tag.find('span','ProfileTweet-action--favorite')
    favorite['class']= favorite.get('class', []) + ['btn','btn-danger']
    # favorite['class']= favorite['class']+'btn btn-danger'

    avatar=tag.find(class_='js-action-profile-avatar')
    avatar['class']= avatar.get('class', []) + ['img-circle']
    avatar['class'].remove('img-rounded')
    avatar.wrap(BeautifulSoup().new_tag("a",href="/twitter/iframe?twiiter_id="+id))
    # avatar.wrap(BeautifulSoup().new_tag("a",href="https://twitter.com/"+table_name+"/status/"+id))

    return tag

class TwitterUrl(Url):

    def get_url(self, sortdict_key="default"):
        return "https://twitter.com/"+self.request_key_param

class TwitterParseStrategy(HtmlParseStrategy):

    def parse(self):
        return self.parser.find('div',class_="stream-container")['data-min-position']

    def first_twitter(self):
        list = self.parser.find('ol', class_="stream-items").contents
        listdata = []
        for item in list:
            if isinstance(item, Tag):
                data = {
                    'id': int(item['data-item-id']),
                    'html': update_content(item.find('div', 'content'),self.request_key_param,item['data-item-id']).prettify()
                }
                listdata.append(data)
        return listdata

class TwitterRequest(SingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {'Host': 'twitter.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
        self.url = TwitterUrl()
        self.parse_strategy = TwitterParseStrategy()

class TweetUrl(ContextUrl):

    def get_url(self, sortdict_key="default"):
        return "https://twitter.com/i/profiles/show/"+self.request_key_param+"/timeline/tweets?include_available_features=1&include_entities=1&max_position="+str(self.context)+"&reset_error_state=false"

class TweetParseStrategy(ContextListParseStrategy):

    def is_end(self):
        return not self.parser['has_more_items']

    def get_total(self):
        pass

    def get_context(self):
        return self.parser["min_position"]

    def parse(self):
        soup = BeautifulSoup(self.parser['items_html'])
        if soup.body:
            list = soup.body.contents
        else:
            list = soup
        listdata = []
        for item in list:
            if isinstance(item, Tag):
                data = {
                    'id': int(item['data-item-id']),
                    'html': update_content(item.find('div', 'content'),self.request_key_param,item['data-item-id']).prettify()
                }
                listdata.append(data)
        return listdata

class TweetSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.headers = {'Host': 'twitter.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
        self.url = TweetUrl()
        self.parse_strategy= TweetParseStrategy()

    def init(self, request_key_param):
        super().init(request_key_param)
        c = TwitterRequest()
        c.init(request_key_param)
        self.url.context = c.get_data()
        self.g = c.parse_strategy.first_twitter()

    def glance(self, father):
        father.datacore.listdata=self.g

class TwitterTwitter(IntervalListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        # self.debug=True
        self.list_single_request = TweetSingleRequest()