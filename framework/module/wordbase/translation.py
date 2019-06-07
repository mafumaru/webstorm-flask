import json
import time

from langid import langid

from framework.core.crawlercore.parse import JsonParseStrategy, RegexJsonParseStrategy, HtmlParseStrategy
from framework.core.crawlercore.request import SingleRequest
from framework.core.crawlercore.url import Url


class TranslationUrl(Url):
    def get_url(self, sortdict_key="default"):
        return "https://fanyi.baidu.com/transapi"


class TranslationParseStrategy(JsonParseStrategy):
    def parse(self):
        # translate = ''
        # if self.lang == 'en':
        #     j = json.loads(self.parser['result'])
        #     for mean in j['content'][0]['mean']:
        #         means = mean['pre'] + ','.join(mean['cont'].keys())
        #         translate += (means + '\n')
        # elif self.lang == 'jp':
        #     translate = self.parser['data'][0]['dst']
        # return translate
        return self.parser['data'][0]['dst']

class Translation(SingleRequest):

    def __init__(self):
        super().__init__()
        self.url = TranslationUrl()
        self.parse_strategy=TranslationParseStrategy()
        self.post=True
        self.headers={
            'Content - Type':'application/x-www-form-urlencoded'
            # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        self.lang = ''

    def translate(self,word):
        self.init(word)
        lang = langid.classify(word)[0]
        t=None
        if lang == 'en':
            self.lang = 'en'
        elif lang == 'ja' or lang == 'zh':
            self.lang ='jp'
            h = HujiangTranslation()
            h.init(word)
            t = h.get_data()
        else:
            self.lang = 'en'
        self.parse_strategy.lang = self.lang
        self.data={
            'from':self.lang,
            'to':'zh',
            # 'source':'txt',
            'query': self.url.request_key_param
        }
        if self.lang != 'zh':

            if t:
                return self.get_data()+t
            return self.get_data()
        return 'zh'

    def translate_with_pronounce(self,word):
        self.init(word)
        lang = langid.classify(word)[0]
        t = None
        if lang == 'en':
            self.lang = 'en'
        elif lang == 'ja' or lang == 'zh':
            self.lang = 'jp'
            h = HujiangTranslation()
            h.init(word)
            t = h.get_data()
        else:
            self.lang = 'en'
        self.parse_strategy.lang = self.lang
        self.data = {
            'from': self.lang,
            'to': 'zh',
            # 'source':'txt',
            'query': self.url.request_key_param
        }
        if self.lang != 'zh':

            if t:
                return (self.get_data(), t)
            return (self.get_data(),'')
        return ('zh','')

class BaiduSelectTranslationUrl(Url):
    def get_url(self, sortdict_key="default"):
        ts = str(int(round(time.time() * 1000)))
        return "https://sp1.baidu.com/5b11fzupBgM18t7jm9iCKT-xh_/sensearch/selecttext?cb=jQuery110206843677515851383_"+ts+"&q="+self.request_key_param+"&_="+ts


class BaiduSelectTranslationParseStrategy(RegexJsonParseStrategy):


    def regex_json(self, res):
        index = res.find('{')
        index2 = res.rfind('}')
        return res[index:index2 + 1]

    def parse(self):
        return self.parser['data']['result']

class BaiduSelectTranslation(SingleRequest):

    def __init__(self):
        super().__init__()
        self.url = BaiduSelectTranslationUrl()
        self.parse_strategy=BaiduSelectTranslationParseStrategy()
        # self.headers={
        #     'Content - Type':'application/x-www-form-urlencoded',
        #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        # }

    def translate(self,word):
        self.init(word)
        return self.get_data()

class HujiangTranslationUrl(Url):
    def get_url(self, sortdict_key="default"):
        return "https://dict.hjenglish.com/jp/jc/"+self.request_key_param

class HujiangTranslationParseStrategy(HtmlParseStrategy):

    def parse(self):
        try:
            translate = self.parser.find('div',class_="pronounces").span.next_sibling.next_sibling.text.replace('\n','')[1:-1]
        except:
            translate="ERROR"
        return translate

class HujiangTranslation(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url = HujiangTranslationUrl()
        self.parse_strategy=HujiangTranslationParseStrategy()
        self.headers = {'Host': 'dict.hjenglish.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
                        'Cookie': 'HJ_UID=352380f3-9ad9-aa83-379a-91a159561fb7; HJ_CST=1; HJ_SID=e0845452-eb08-b48d-17b8-038c839effa2; _REF=; TRACKSITEMAP=3%2C; HJ_SSID_3=d5f118fb-88b8-958e-c2d9-f9ade518269b; HJ_CSST_3=1; _SREF_3='}
