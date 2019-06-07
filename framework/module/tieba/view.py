from flask import render_template

from framework.core.viewcore.view import ListViewHistory
from framework.module.tieba.helper import TiebaPostbarHelper, TiebaTieHelper


class TiebaPostbarView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Tieba Postbar')
        self.helper = TiebaPostbarHelper()

    def ajax_list_template(self):
        pass

    def html_template(self):
        pass

    def postbar_single_day(self,**args):# identity , postbar , offset=0 , limit=10 , history
        list_data = self.helper.get_identity_tie(args)
        return render_template('tieba/postbar/postbar.html',list_data=list_data, base=self.base)

    def postbar_single_day_ajax(self,**args):# identity , postbar , offset=0 , limit=10 , history
        list_data = self.helper.get_identity_tie(args)
        return render_template('tieba/postbar/postbar_list_content.html', list_data=list_data, base=self.base)

    def bars(self):
        return render_template('tieba/index/bars.html', base=self.base)

    def bar_days(self,postbar):
        data = self.helper.get_all_identity(postbar)
        return render_template('tieba/index/day.html',list_data=data, base=self.base)

    def mark_view(self,**args):# m_identity,postbar
        list_data = self.helper.review_mark(**args)
        return render_template('tieba/postbar/mark.html', list_data=list_data, base=self.base)

class TiebaTieView(ListViewHistory):
    def __init__(self):
        super().__init__()
        self.set_title('Tieba Tie')
        self.helper = TiebaTieHelper()

    def ajax_list_template(self):
        return 'tieba/tie/tie_list_content.html'

    def html_template(self):
        return 'tieba/tie/tie.html'
