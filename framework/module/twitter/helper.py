from framework.core.dbcore.helper import IntReferHelper


class TwitterTwitterHelper(IntReferHelper):
    db_name = "twitter_twitter"

    def __init__(self):
        super().__init__()

    def _history_depth(self) -> list:
        return ['id']

    def _parse_glance(self, data_core):
        return data_core.rowdata

class TwitterCommentHelper(IntReferHelper):
    db_name = "twitter_comment"

    def __init__(self):
        super().__init__()

    def _history_depth(self) -> list:
        return ['id']

    def _parse_glance(self, data_core):
        return data_core.rowdata