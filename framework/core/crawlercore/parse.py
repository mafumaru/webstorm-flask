import json
from abc import ABC,abstractmethod
from json import JSONDecodeError

from bs4 import BeautifulSoup


class ParseStrategy(ABC):
    def __init__(self):
        self.parser=None
        self.request_key_param=None
        self.offset=0

    @abstractmethod
    def set_parser(self,res):
        pass

    @abstractmethod
    def parse(self):
        pass

    def is_right(self):
        return True

class HtmlParseStrategy(ParseStrategy):

    @abstractmethod
    def parse(self):
        pass

    def set_parser(self, res):
        self.parser = BeautifulSoup(res)
        return True

class RegexJsonParseStrategy(ParseStrategy):

    @abstractmethod
    def parse(self):
        pass

    def set_parser(self, res):
        self.parser = json.loads(self.regex_json(res))
        return True

    @abstractmethod
    def regex_json(self, res):
        pass

class RegexHtmlParseStrategy(ParseStrategy):

    @abstractmethod
    def parse(self):
        pass

    def set_parser(self, res):
        self.parser = BeautifulSoup(self.regex_html(res))
        return True

    @abstractmethod
    def regex_html(self, res):
        pass

class JsonParseStrategy(ParseStrategy):

    @abstractmethod
    def parse(self):
        pass

    def set_parser(self, res):
        try:
            self.parser = json.loads(res)
            return True
        except JSONDecodeError:
            print("sjero"+res+'jero')
            return False


class ListParseStrategy(JsonParseStrategy):

    @abstractmethod
    def is_end(self):
        pass

    @abstractmethod
    def get_total(self):
        pass


class HtmlListParseStrategy(HtmlParseStrategy):

    @abstractmethod
    def is_end(self):
        pass

    @abstractmethod
    def get_total(self):
        pass


class JsObjectListParseStrategy(RegexJsonParseStrategy):

    @abstractmethod
    def is_end(self):
        pass

    @abstractmethod
    def get_total(self):
        pass


class JsObjectHtmlListParseStrategy(RegexHtmlParseStrategy):

    @abstractmethod
    def is_end(self):
        pass

    @abstractmethod
    def get_total(self):
        pass


class ContextListParseStrategy(ListParseStrategy):

    @abstractmethod
    def get_context(self):
        pass