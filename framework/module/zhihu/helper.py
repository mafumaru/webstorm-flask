import urllib
from urllib.parse import unquote

from framework.core.dbcore.helper import DataCoreTable, IntReferHelper, ReferHelper


class ZhihuAnswerListHelper(IntReferHelper):

    def _history_depth(self) -> list:
        return ['id']

class ZhihuPeopleHelper(ZhihuAnswerListHelper):
    db_name = "zhihu_people"

    def _parse_glance(self, data_core:DataCoreTable):
        return data_core.listdata[0]['author']

class ZhihuQuestionHelper(ZhihuAnswerListHelper):
    db_name = "zhihu_question"

    def write_to_db(self, data_core: DataCoreTable):
        data_core.listdata.sort(key=lambda e: e['voteup_count'], reverse=True)
        super().write_to_db(data_core)

    def _parse_glance(self, data_core):
        return data_core.listdata[0]['question']

class ZhihuCommentHelper(ZhihuAnswerListHelper):
    db_name = 'zhihu_comment'

    def _parse_glance(self, data_core):
        return data_core.rowdata

class ZhihuCollectionHelper(ZhihuAnswerListHelper):
    db_name = 'zhihu_collection'

    def _parse_glance(self, data_core):
        return data_core.rowdata

class ZhihuSearchHelper(ReferHelper):
    db_name = 'zhihu_search'

    def _history_depth(self) -> list:
        return ['id']

    def _parse_glance(self, data_core):
        return data_core.rowdata

    def get_history(self, table_name):
        return super().get_history(unquote(table_name))

    def set_history(self, history, table_name):
        super().set_history(history, unquote(table_name))


