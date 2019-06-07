from abc import ABC, abstractmethod
from flask import render_template

from framework.core.dbcore.helper import ReferHelper, BaseHelper
from framework.module.rl.helper import ReadLaterDirHelper, ReadLaterHelper


class View(ABC):
    def __init__(self):
        self.base = {
            'title': 'No title'
        }

    def set_title(self,title):
        self.base['title']=title

    @abstractmethod
    def html_template(self):
        pass

    def page_render(self):
        return render_template(self.html_template(), base=self.base)

class NavView(View):
    def __init__(self):
        super().__init__()
        self.rl_helper=ReadLaterDirHelper()
        self.helper:ReferHelper=None
        self.base['nav']=self.rl_helper.get_rl_list()



class BaseListView(NavView):

    def __init__(self):
        super().__init__()
        self.list_data=[]

    @abstractmethod
    def ajax_list_template(self):
        pass

    def page_render(self):
        return render_template(self.html_template(), base=self.base, list_data=self.list_data)

    def ajax_render(self,list_data):
        return render_template(self.ajax_list_template(), base=self.base, list_data=list_data)

class RLListView(BaseListView):

    def __init__(self):
        super().__init__()
        self.rl_list_helper = ReadLaterHelper()

    def db_read(self,list_id,offset=0):
        return self.rl_list_helper.read_refer_list(list_id,offset)

    def render(self,list_id,offset=0):
        self.list_data = self.db_read(int(list_id),offset)
        return self.page_render()

    def ajax_list(self, table_name, offset=0):
        list_data = self.db_read(int(table_name), offset)
        return self.ajax_render(list_data)

class CListView(BaseListView):

    def __init__(self):
        super().__init__()
        self.refer_list_helper=None

    def db_read(self,list_id,offset=0):
        return self.refer_list_helper.read_refer_list(list_id,offset)

    def render(self,list_id,offset=0):
        self.list_data = self.db_read(list_id,offset)
        return self.page_render()

    def ajax_list(self, table_name, offset=0):
        list_data = self.db_read(table_name, offset)
        return self.ajax_render(list_data)

class ListView(BaseListView):
    def __init__(self):
        super().__init__()
        self.refer_list_helper:BaseHelper=None

    def db_read(self,list_id,offset=0):
        return self.refer_list_helper.read(list_id,offset)

    def render(self,table_name,offset=0):
        self.list_data = self.db_read(table_name,offset)
        return self.page_render()

    def ajax_list(self, table_name, offset=0):
        list_data = self.db_read(table_name, offset)
        return self.ajax_render(list_data)


class ListViewHistory(BaseListView):

    def __init__(self):
        super().__init__()

    def db_read(self,name,history=0,offset=0):
        self.base['collection'] = {
            'table_name': name,
            'type': self.helper.db_name
        }
        return self.helper.read_from_db(name,history,offset)

    def render(self,name,history=0,offset=0):
        self.list_data = self.db_read(name,history, offset)
        return self.page_render()

    def ajax_list(self,table_name,history=0,offset=0):
        list_data = self.db_read(table_name,history, offset)
        return self.ajax_render(list_data)
