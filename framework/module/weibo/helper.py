from framework.core.dbcore.helper import IntReferHelper


class WeiboListHelper(IntReferHelper):
    def _history_depth(self) -> list:
        return ['mblog','id']

    def __init__(self):
        super().__init__()


class WeiboUserHelper(WeiboListHelper):
    db_name = 'weibouser_test'

    def __init__(self):
        super().__init__()

    def _parse_glance(self, data_core):
        return data_core.listdata[0]['mblog']['user']