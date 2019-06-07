from abc import ABC, abstractmethod
from urllib.parse import unquote


class Filter():

    map_name_list = ['zhihu','twitter']
    map_list=[]
    host = []
    attr_list = []
    query_attrs={}

    def __init__(self):
        self.map:Map = None

    def route(self, follow_url,list_id):
        self.cut_url(self.cut_https(follow_url))
        self.parse_host()
        self.map.parse_path(self.attr_list)
        # if 'https://www.zhihu.com/people/' in follow_url:
        #     temp = follow_url[len('https://www.zhihu.com/people/'):]
        #     name = str.split('/',temp)[0]
        #     return name
        # return False
        return self.map.excute_follow(list_id)

    def cut_https(self,url):
        https = 'https://'
        http = 'http://'
        if https in url:
            return url[len(https):]
        elif http in url:
            return url[len(https):]
        return url

    def cut_url(self,url):
        # path = url.split('?')
        # cut_list = path[0].split('/')
        cut_list = url.split('/')
        self.host = cut_list[0]
        self.attr_list = cut_list[1:]

    def parse_host(self):
        for host in self.map_name_list:
            if host in self.host:
                self.map = eval(host.title()+'Map')(host)
                break


class Map:
    parse_name_list = []

    def __init__(self,type:str):
        self.type = type
        self.parse_list = []
        for parse_name in self.parse_name_list:
            self.parse_list.append(eval(type.title()+parse_name.title()+'Parser')(parse_name))
        self.parser:Parser =None

    def parse_path(self,atrr_list:list):
        for parser in self.parse_list:
            if parser.is_match(atrr_list):
                self.parser = parser
                break

    def excute_follow(self,list_id):
        crawler = self.get_crawler()
        crawler.get_lists()
        crawler.datacore.parent_id = int(list_id)
        helper = self.get_helper()
        helper.write_to_db(crawler.datacore)
        return 'true'

    def get_crawler(self):
        m = __import__('.'.join(['framework', 'module', self.type, self.parser.type]))
        C = getattr(m, 'module')
        C = getattr(C, self.type)
        C = getattr(C, self.parser.type)
        C = getattr(C, self.get_crawler_name())
        return C(self.parser.get_keyword())

    def get_crawler_name(self):
        return self.type.title()+self.parser.type.title()

    def get_helper(self):
        h = 'helper'
        m = __import__('.'.join(['framework', 'module', self.type,h ]))
        C = getattr(m, 'module')
        C = getattr(C, self.type)
        C = getattr(C, h)
        C = getattr(C, self.get_helper_name())
        return C()

    def get_helper_name(self):
        return self.get_crawler_name()+'Helper'

class Parser(ABC):

    def __init__(self,type:str):
        self.type = type
        self.attr_list = []
        self.query_attrs = {}

    @abstractmethod
    def data_position(self):
        pass


    def is_match(self,atrr_list:list):
        self.attr_list = atrr_list
        return self.type in atrr_list

    def get_keyword(self):
        # return self.attr_list[0]
        return self.attr_list[self.data_position()].split('?')[0]

class ZhihuMap(Map):
    parse_name_list = ['people','comment','question','collection','search']

class ZhihuPeopleParser(Parser):
    def data_position(self):
        return 1

class ZhihuQuestionParser(Parser):
    def data_position(self):
        return 1

class ZhihuCollectionParser(Parser):
    def data_position(self):
        return 1

class ZhihuCommentParser(Parser):

    def is_match(self, atrr_list: list):
        self.attr_list = atrr_list
        return 'question' in self.attr_list and 'answer' in self.attr_list

    def data_position(self):
        return 3

class ZhihuSearchParser(Parser):

    def is_match(self, atrr_list: list):
        self.attr_list = atrr_list
        return  self.attr_list[0].find('search?')!=-1

    def get_keyword(self):
         for attr in self.attr_list[0].split('?')[1].split('&'):
             kv = attr.split('=')
             if kv[0]=='q':
                 return unquote(kv[1])

    def data_position(self):
        pass

class TwitterMap(Map):
    parse_name_list = ['twitter','comment']

class TwitterTwitterParser(Parser):

    def data_position(self):
        return 0

    def is_match(self, atrr_list: list):
        self.attr_list = atrr_list
        return len(atrr_list)==1

class TwitterCommentParser(Parser):

    def get_keyword(self):
        return self.attr_list[0]+'-'+self.attr_list[2]

    def is_match(self, atrr_list: list):
        self.attr_list = atrr_list
        return 'status' in atrr_list

    def data_position(self):
        pass
