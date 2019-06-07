import json

import requests

from framework.core.viewcore.view import ListViewHistory, ListView
from framework.module.zhihu.helper import ZhihuPeopleHelper, ZhihuQuestionHelper, ZhihuCommentHelper, \
    ZhihuCollectionHelper, ZhihuSearchHelper
from framework.module.zhihu.recommend import ZhihuRecommend


class ZhihuPeopleView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('People Answers')
        self.helper = ZhihuPeopleHelper()

    def ajax_list_template(self):
        return 'zhihu/people/answer_list_content.html'

    def html_template(self):
        return 'zhihu/people/answers.html'

class ZhihuQuestionView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Question Answers')
        self.helper = ZhihuQuestionHelper()

    def ajax_list_template(self):
        return 'zhihu/question/answer_list_content.html'

    def html_template(self):
        return 'zhihu/question/answers.html'

class ZhihuCommentView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Answer Comments')
        self.helper = ZhihuCommentHelper()

    def ajax_list_template(self):
        return 'zhihu/comment/comment_list_content.html'

    def html_template(self):
        return 'zhihu/comment/comments.html'

class ZhihuCollectionView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Zhihu Collections')
        self.helper = ZhihuCollectionHelper()

    def ajax_list_template(self):
        return 'zhihu/collection/collection_list_content.html'

    def html_template(self):
        return 'zhihu/collection/collection.html'

class ZhihuRecommendView(ListView):

    def __init__(self):
        super().__init__()
        self.set_title('Zhihu Recommend')

    def html_template(self):
        return 'zhihu/recommend/recommend.html'

    def ajax_list_template(self):
        return 'zhihu/recommend/recommend_list_content.html'

    def db_read(self, list_id, offset=0):
        r = ZhihuRecommend()
        r.init("")
        return r.get_data()


class ZhihuCommentRealtimeView(ZhihuCommentView):
    def db_read(self, name, history=0, offset=0):
        self.base['collection'] = {
            'table_name': name,
            'type': 'zhihu_realtime_comment'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; MZ-m1 metal Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/7.3.2 UWS/2.11.0.33 Mobile Safari/537.36',
            'Accept - Encoding': 'gzip, deflat'
        }
        r = requests.get("https://www.zhihu.com/api/v4/answers/"+str(name)+"/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order=normal&limit=20&offset="+str(int(offset)*20)+"&status=open", headers=headers)
        r.encoding='utf-8'
        j = json.loads(r.text)
        return  j['data']

    def html_template(self):
        return 'zhihu/comment/realtime.html'

class ZhihuSearchView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Zhihu Search')
        self.helper = ZhihuSearchHelper()

    def ajax_list_template(self):
        return 'zhihu/search/search_list_content.html'

    def html_template(self):
        return 'zhihu/search/search_result.html'