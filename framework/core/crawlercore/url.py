from abc import ABC, abstractmethod


class Url(ABC):
    def __init__(self,):
        self.request_key_param=""

    def init(self,request_key_param):
        self.request_key_param=request_key_param

    @abstractmethod
    def get_url(self,sortdict_key="default"):
        pass

class ListUrl(Url):
    def __init__(self):
        self.offset=0
        self.limit=20
        self.sort={}

    def init(self,request_key_param):
        super().init(request_key_param)

class PageUrl(ListUrl):
    def __init__(self):
        super().__init__()
        self.offset=1
        self.limit=1

class ContextUrl(ListUrl):
    def __init__(self):
        super().__init__()
        self.context = {}