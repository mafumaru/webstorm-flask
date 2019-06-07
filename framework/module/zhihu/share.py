from framework.core.crawlercore.parse import ListParseStrategy
from framework.core.crawlercore.request import IntervalListRequest


class AnswerListParseStrategy(ListParseStrategy):
    def __init__(self):
        super().__init__()

    def parse(self):
        return self.parser['data']

    def is_end(self):
        return self.parser['paging']['is_end']

    def get_total(self):
        return self.parser['paging']['totals']

class ZhihuListRequest(IntervalListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)