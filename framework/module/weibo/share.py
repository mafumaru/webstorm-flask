from framework.core.crawlercore.request import IntervalListRequest


class WeiboListRequest(IntervalListRequest):
    def __init__(self, request_key_param):
        super().__init__(request_key_param)
        self.interval=0