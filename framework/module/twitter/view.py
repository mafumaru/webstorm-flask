import json

import requests

from framework.core.viewcore.view import ListViewHistory
from framework.module.twitter.comment import TwitterConversationRequest
from framework.module.twitter.helper import TwitterTwitterHelper, TwitterCommentHelper


class TwitterTwitterView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Twitter')
        self.helper = TwitterTwitterHelper()

    def html_template(self):
        return 'twitter/twitter/tweets.html'

    def ajax_list_template(self):
        return 'twitter/twitter/tweets_list_content.html'

class TwitterCommentView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Twitter Comments')
        self.helper = TwitterCommentHelper()

    def html_template(self):
        return 'twitter/comment/comment.html'

    def ajax_list_template(self):
        return 'twitter/comment/comment_list_content.html'

class TwitterCommentRealtimeView(TwitterCommentView):
    def db_read(self, name, history=0, offset=0):
        self.base['collection'] = {
            'table_name': name,
            'type': 'twitter_realtime_comment'
        }
        c = TwitterConversationRequest()
        c.init(name)
        c.get_data()
        return c.parse_strategy.first_comment()

    def html_template(self):
        return 'twitter/comment/realtime.html'
