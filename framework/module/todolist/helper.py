from flask import render_template

from framework.core.dbcore.helper import BaseHelper, CollectionHelper
from framework.tools.timedate import get_sec_time


class TodolistHelper(BaseHelper):
    db_name = 'todolist'
    collection_namess = ['daily_todolist', 'daily_parent_lists', 'frequent_todolist', 'frequent_todolist_domain',
                         'undo_task', 'workflow', 'killing_time', 'killing_time_types', 'search',
                         'search_rl_dirs','max_id','manage']

    def __init__(self):
        super().__init__()

class TodolistCollectionHelper(CollectionHelper):
    db_name = 'todolist'

class DailyTodolistHelper(TodolistCollectionHelper):
    collection_name = 'daily_todolist'

    def get_data_struct(self, args):# parent_id ,content
        return {
            'id':int(args['id']),
            'content': args['content'],
            'deadline': 0, # unused_now
            'done_time': 0,
            'parent_id': int(args['parent_id'])
        }


    def show_all_condition(self,**args): # parent_id
        return {'parent_id':int(args['parent_id'])}

    def add_by_uodolist(self,**args):
        self.add(**args)
        pass

class DailyParentTodolistHelper(TodolistCollectionHelper):
    collection_name = 'daily_parent_lists'

    def add(self, **args):
        super().add(**args)
        id = self.get_max_id()
        data = {
            'id':id-1,
            'name':args['name']
        }
        return render_template('todolist/daily/parent/radio.html',list=[data])

    def delete(self, **args):
        h = DailyTodolistHelper()
        undo = h.show_all(parent_id=int(args['id']))
        if undo:
            u = UndoTodolistHelper()
            u.collection.insert(undo)
        h.collection.remove(h.show_all_condition(parent_id=int(args['id'])))
        super().delete(**args)

    def get_data_struct(self, args):# name ,-type
        return {
            'name':args['name'],
            # 'type': args['type'],
            'id': int(args['id'])
        }


class FrequentTodolistHelper(TodolistCollectionHelper):
    collection_name = 'frequent_todolist'

    def __init__(self):
        super().__init__()
        self.history_collection = self.db['manage']

    def get_data_struct(self, args):# content
        id = self.history_collection.find_one({'type': 'frequent_todolist_domain_history'})
        return {
            'id':int(args['id']),
            'content': args['content'],
            'parent_id': id['id']
        }

    def show_all_condition(self,**args):
        id = self.history_collection.find_one({'type':'frequent_todolist_domain_history'})
        if id:
            id =id['id']
        else:
            id=-1
        return {'parent_id':id}

    def show_all_with_set(self, **args): # id
        self.history_collection.remove({'type':'frequent_todolist_domain_history'})
        self.history_collection.insert({'type':'frequent_todolist_domain_history','id':int(args['id'])})
        return super().show_all(**args)


class FrequentDomainTodolistHelper(TodolistCollectionHelper):
    collection_name = 'frequent_todolist_domain'

    def get_data_struct(self, args):# domain
        return {
            'domain':args['domain'],
            'id': int(args['id'])
        }


class TodolistWorkFlowHelper(TodolistCollectionHelper):
    collection_name = 'workflow'

    def get_data_struct(self, args):# content
        return {
            'id':int(args['id']),
            'content': args['content'],
            'deadline': 0, # unused_now
            'done_time': 0,
            'add_time': get_sec_time()
        }

    def add(self, **args):
        super().add(**args)
        h = DailyTodolistHelper()
        h.delete(**args)

    def clear_to_undo(self, **args):
        undo = self.show_all()
        u = UndoTodolistHelper()
        u.collection.insert(undo)
        self.collection.remove()


    def exchange(self,id,exchange_id):
        item = self.collection.find_one({'id':int(id)})
        exchange_item = self.collection.find_one({'id':int(exchange_id)})
        temp_time = item['add_time']
        item['add_time']=exchange_item['add_time']
        exchange_item['add_time'] = temp_time
        self.collection.save(item)
        self.collection.save(exchange_item)
        return 'True'

    def show_all(self, **args):
        res =  super().show_all(**args)
        res.sort(key=lambda e: e['add_time'])
        # res.sort(key=lambda e: e['add_time'], reverse=True)
        return res


class UndoTodolistHelper(TodolistCollectionHelper):
    collection_name = 'undo_task'

    def get_data_struct(self, args):# content
        return {
            'id':int(args['id']),
            'content': args['content']
        }









