from bs4 import BeautifulSoup, Tag

from framework.core.crawlercore.parse import JsonParseStrategy, ContextListParseStrategy
from framework.core.crawlercore.request import SingleRequest, ListSingleRequest, IntervalListRequest
from framework.core.crawlercore.url import Url, ContextUrl


def twitter_comment_parse_content(l:list,first=""):
    listdata = []
    for item in l:
        if isinstance(item, Tag):
            if item['class'][0] == 'ThreadedConversation--loneTweet':
                data = {
                    'id': int(item.ol.li['data-item-id']),
                    'comment_type':'loneTweet',
                    'fullname':item.find('span',class_='FullNameGroup').text.strip(),
                    'uid':item.find('a',class_='js-account-group')['href'][1:],
                    'avatar':item.find('img',class_='js-action-profile-avatar')['src'],
                    'date':item.find('a',class_='tweet-timestamp').text,
                    'content':item.find('div',class_='js-tweet-text-container').p.text
                }
            elif item['class'][0]== 'ThreadedConversation':
                f = item.ol.div.li
                reply = twitter_comment_parse_content(item.ol.contents,f['data-item-id'])
                data = {
                    'id': int(f['data-item-id']),
                    'comment_type': 'conversation',
                    'fullname': f.find('span', class_='FullNameGroup').text.strip(),
                    'uid': f.find('a', class_='js-account-group')['href'][1:],
                    'avatar': f.find('img', class_='js-action-profile-avatar')['src'],
                    'date': f.find('a', class_='tweet-timestamp').text,
                    'content': f.find('div', class_='js-tweet-text-container').p.text,
                    'reply':reply
                }
            elif item['class'][0] == 'ThreadedConversation-tweet':
                if item.li['data-item-id'] == first:
                    continue
                data = {
                    'id': int(item.li['data-item-id']),
                    'fullname': item.find('span', class_='FullNameGroup').text.strip(),
                    'uid': item.find('a', class_='js-account-group')['href'][1:],
                    'avatar': item.find('img', class_='js-action-profile-avatar')['src'],
                    'date': item.find('a', class_='tweet-timestamp').text,
                    'content': item.find('div', class_='js-tweet-text-container').p.text,
                    'reply_to': item.find('div', class_='ReplyingToContextBelowAuthor').a.text
                }
                pass
            else:
                continue
            listdata.append(data)
    return listdata

sep = '-'
class TwitterConversationUrl(Url):
    def __init__(self):
        super().__init__()
        self.soup:BeautifulSoup=None

    def get_url(self, sortdict_key="default"):
        self.request_key_params = self.request_key_param.split(sep)
        return "https://twitter.com/"+self.request_key_params[0]+"/status/"+self.request_key_params[1]+"?conversation_id="+self.request_key_params[1]

class TwitterConversationParseStratrgy(JsonParseStrategy):
    def parse(self):
        self.soup = BeautifulSoup(self.parser['page'])
        return self.soup.find('div',class_="stream-container")['data-min-position']

    def first_comment(self):
        contents = self.soup.find('ol',id="stream-items-id").contents
        return twitter_comment_parse_content(contents)

    def twitter_info(self):
        return {'title':self.parser['title'],'uid':self.parser['init_data']['internalReferer'][1:]}

class TwitterConversationRequest(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = TwitterConversationUrl()
        self.parse_strategy = TwitterConversationParseStratrgy()

    def init(self, request_key_param):
        super().init(request_key_param)
        self.request_key_params = request_key_param.split(sep)
        self.headers = {'Host': 'twitter.com', 'Connection': 'keep-alive',
                   'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Overlay-Request': 'true',
                   'X-Requested-With': 'XMLHttpRequest', 'X-Previous-Page-Name': 'profile',
                   'X-Twitter-Active-User': 'yes',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                   'Referer': 'https://twitter.com/'+self.request_key_params[0], 'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8'}

class TwitterCommentUrl(ContextUrl):
    def get_url(self, sortdict_key="default"):
        self.request_key_params = self.request_key_param.split(sep)
        return "https://twitter.com/i/"+self.request_key_params[0]+"/conversation/"+self.request_key_params[1]+"?include_available_features=1&include_entities=1&max_position="+str(self.context)+"&reset_error_state=false"

class TwitterCommentParseStrategy(ContextListParseStrategy):

    def is_end(self):
        return not self.parser['has_more_items']

    def get_total(self):
        pass

    def get_context(self):
        return self.parser["min_position"]

    def parse(self):
    # try:
        soup = BeautifulSoup(self.parser['items_html'])
        if soup.body:
            res = twitter_comment_parse_content(soup.body.contents)
        else:
            data = soup.contents
            res = twitter_comment_parse_content(data)
    # except:
        return res

class TwitterCommentSingleRequest(ListSingleRequest):
    def __init__(self):
        super().__init__()
        self.url = TwitterCommentUrl()
        self.parse_strategy= TwitterCommentParseStrategy()

    def init(self, request_key_param):
        super().init(request_key_param)
        self.request_key_params = request_key_param.split(sep)
        self.headers = {'Host': 'twitter.com', 'Connection': 'keep-alive',
                        'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Overlay-Request': 'true',
                        'X-Requested-With': 'XMLHttpRequest', 'X-Previous-Page-Name': 'profile',
                        'X-Twitter-Active-User': 'yes',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                        'Referer': 'https://twitter.com/'+self.request_key_params[0], 'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8'}
        c = TwitterConversationRequest()
        c.init(request_key_param)
        self.url.context = c.get_data()
        self.g = c.parse_strategy.first_comment()
        self.gg = c.parse_strategy.twitter_info()

    def glance(self, father):
        father.datacore.listdata=self.g
        father.datacore.rowdata=self.gg

class TwitterComment(IntervalListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        # self.debug=True
        self.list_single_request = TwitterCommentSingleRequest()