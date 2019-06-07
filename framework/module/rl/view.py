from framework.core.viewcore.view import NavView, RLListView


# class ReadLaterView(NavView):
#     def __init__(self):
#         super().__init__()
#         self.set_title('Read It Later Homepage')
#
#     def html_template(self):
#         return 'rl/rl_homepage.html'

class ReadLaterListView(RLListView):
    def __init__(self):
        super().__init__()
        self.set_title('Read It Later List')

    def html_template(self):
        return 'rl/rl_list.html'

    def ajax_list_template(self):
        return 'rl/rl_list_content.html'