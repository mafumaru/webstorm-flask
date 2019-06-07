from flask import render_template

from framework.core.viewcore.view import ListView, BaseListView
from framework.module.wordbase.helper import WordbaseHelper, ChineseHelper


class WordbaseView(BaseListView):
    def html_template(self):
        pass

    def ajax_list_template(self):
        pass

    def __init__(self):
        super().__init__()
        self.refer_list_helper=WordbaseHelper()
        self.set_title('Wordbase')
        self.base['collection'] = {
            'table_name': None,
            'type': None
        }

    def wordbase_detail(self,**args):
        list_data = self.refer_list_helper.filter_search(args)
        return render_template('wordbase/wordbase.html', base=self.base, list_data=list_data)

    def wordbase_search(self,**args):
        list_data = self.refer_list_helper.search(args)
        return render_template('wordbase/wordbase.html', base=self.base, list_data=list_data)

    def wordbase_index(self):
        groups = self.refer_list_helper.get_groups()
        return render_template('wordbase/index.html', base=self.base, groups=groups)

class ChineseView(ListView):
    def __init__(self):
        super().__init__()
        self.refer_list_helper = ChineseHelper()
        self.set_title('Chinese Wordbase')

    def html_template(self):
        return 'wordbase/chinese.html'


    def ajax_list_template(self):
        return 'wordbase/chinese_list_content.html'
