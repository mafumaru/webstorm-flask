from flask import render_template

from framework.core.viewcore.view import NavView
from framework.module.todolist.helper import DailyParentTodolistHelper, DailyTodolistHelper, TodolistWorkFlowHelper, \
    FrequentTodolistHelper, UndoTodolistHelper, FrequentDomainTodolistHelper


class TodolistView(NavView):
    def __init__(self):
        super().__init__()
        self.set_title('')
        self.helper = None
        self.daily_parent_helper = DailyParentTodolistHelper()
        self.daily_helper = DailyTodolistHelper()
        self.workflow_helper = TodolistWorkFlowHelper()
        self.frequent_helper = FrequentTodolistHelper()
        self.frequent_domain_helper = FrequentDomainTodolistHelper()
        self.undolist_helper = UndoTodolistHelper()

    def html_template(self):
        pass

    def homepage(self):
        return render_template('todolist/homepage.html',base=self.base)

    def daily_dir(self):
        list_data = self.daily_parent_helper.show_all()
        return render_template('todolist/daily/parent/dir.html',base=self.base,list_data=list_data)

    def daily_todolist(self,parent_id):
        list_data = self.daily_helper.show_all(parent_id=parent_id)
        return render_template('todolist/daily/item/todolist.html',base=self.base,list_data=list_data)

    def workflow(self):
        list_data = self.workflow_helper.show_all()
        return render_template('todolist/daily/workflow/workflow.html',base=self.base,list_data=list_data)

    def get_todolist_parent_dir_view(self):
        l_data = self.daily_parent_helper.show_all()
        return render_template('todolist/daily/parent/radio.html',list=l_data)

    def get_frequent_domain_view(self):
        l_data = self.frequent_domain_helper.show_all()
        return render_template('todolist/daily/frequent_domain_btn.html',list=l_data)

    def get_frequent_domain_set_view(self,**args):
            l_data = self.frequent_helper.show_all_with_set(**args)
            return render_template('todolist/daily/frequent_todolist.html',list=l_data)

    def get_frequent_todolist_view(self,**args):
        l_data = self.frequent_helper.show_all(**{})
        return render_template('todolist/daily/frequent_todolist.html',list=l_data)

    def get_undolist_view(self):
        l_data = self.undolist_helper.show_all()
        return render_template('todolist/daily/undolist.html',list=l_data)

    def killing_time_categories(self):
        pass

    def killing_time(self,parent_id):
        pass

    def search_panel(self):
        pass