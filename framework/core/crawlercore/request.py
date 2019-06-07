from abc import ABC

import requests
import time

from framework.core.crawlercore.parse import ParseStrategy, ListParseStrategy, ContextListParseStrategy
from framework.core.crawlercore.url import Url, ListUrl, ContextUrl
from framework.core.dbcore.datacore import DataCoreTable


class SingleRequest(ABC):
    def __init__(self):
        self.headers = {}
        self.post=False
        self.data = {}
        self.cookies ={}
        self.get_cookies ={}
        self.url:Url = None
        self.parse_strategy:ParseStrategy = None

    def init(self,request_key_param):
        self.url.request_key_param=request_key_param
        self.parse_strategy.request_key_param=request_key_param

    def request(self):
        url = self.url.get_url()
        if self.post:
            if self.cookies:
                r = requests.post(url, headers=self.headers, data=self.data,cookies=self.cookies)
            else:
                r = requests.post(url, headers=self.headers,data=self.data)
        else:
            r = requests.get(url, headers=self.headers)
        self.get_cookies = r.cookies.get_dict()
        return r

    def get_data(self):
        req = self.request()
        res = req.text
        if req.status_code == 200:
            self.parse_strategy.set_parser(res)
            if self.parse_strategy.is_right():
                return self.parse_strategy.parse()
            else:
                time.sleep(1)
                self.get_data()
        else:
            time.sleep(1)
            print(req.text+'sero')
            self.get_data()


class ListSingleRequest(SingleRequest):
    def __init__(self):
        super().__init__()
        self.url:ListUrl = None
        self.parse_strategy:ListParseStrategy = None
        self.res=""

    def request(self):
        res = super().request()
        self.res=str(self.url.offset)+":"+res.text
        return res

    def get_data(self):
        req = self.request()
        res = req.text
        # print(res[0:200])
        if req.content:
            right = self.parse_strategy.set_parser(res)
            # print('')
            if not right:
                return "skip"
            if self.parse_strategy.is_right():
                self.url.offset += self.url.limit
                self.parse_strategy.offset=self.url.offset
                if isinstance(self.url,ContextUrl) and isinstance(self.parse_strategy,ContextListParseStrategy) and not self.parse_strategy.is_end():
                    self.url.context = self.parse_strategy.get_context()
                return self.parse_strategy.parse()
            else:
                print("judge is_right page: "+str(self.url.offset))
                time.sleep(1)
                res = self.request().text
                self.parse_strategy.set_parser(res)
                if self.parse_strategy.is_right():
                    return self.parse_strategy.parse()
                else:
                    return "skip"
        else:
            time.sleep(10)
            print(req.text+"ero")
            return "skip"

    def glance(self,father):
        pass

class ListRequest:
    def __init__(self,request_key_param):
        self.interval = 0
        self.datacore:DataCoreTable = DataCoreTable()
        self.datacore.table_name=request_key_param
        self.datacore.listdata = []
        self.list_single_request:ListSingleRequest = None
        self.debug=False
        self.last_empty=False

    def get_one_list(self):
        return self.list_single_request.get_data()

    def get_lists(self):
        self.list_single_request.init(self.datacore.table_name)
        self.list_single_request.glance(self)
        while True:
            code = self.get_one_list()
            if not isinstance(code,list):
                if self.debug:
                    print("skip")
                if self.last_empty == True:
                    break
                self.last_empty=True
                continue
            self.last_empty=False
            self.datacore.listdata += code
            if self.debug:
                print("page %d : %d"%(self.list_single_request.url.offset-self.list_single_request.url.limit,len(self.datacore.listdata)))
            if self.interval != 0:
                time.sleep(self.interval)
            if self.list_single_request.parse_strategy.is_end():
                self.list_single_request.url.offset -=  self.list_single_request.url.limit
                time.sleep(1)
                self.get_one_list()
                if self.debug:
                    print("judge end")
                if self.list_single_request.parse_strategy.is_end():
                    break


class IntervalListRequest(ListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.interval = 1