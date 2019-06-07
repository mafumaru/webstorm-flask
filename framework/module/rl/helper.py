import pymongo
from flask import render_template

class ReadLaterDirHelper():
    refer_db_name = "rl"
    refer_collection_name='dirs'
    list_id_name='list_id'
    list_name = 'list_name'
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.refer_db = self.conn[self.refer_db_name]
        self.refer_db_collection = self.refer_db[self.refer_collection_name]

    def _to_list(self, cursor):
        return list(cursor)

    def get_rl_list(self):
        return self._to_list(self.refer_db_collection.find())

    def get_max_id(self):
        if self.refer_db_collection.find().count()==0:
            return {self.list_id_name:0}
        else:
            return self._to_list(self.refer_db_collection.find().sort([(self.list_id_name,-1)]).limit(1))[0]

    def add_rl_list(self,list_name):
        max_id = self.get_max_id()
        list_id = max_id[self.list_id_name]+1
        self.refer_db_collection.insert({self.list_name:list_name,self.list_id_name:list_id})
        res = self.refer_db_collection.find_one({self.list_name:list_name})
        return render_template('rl/dir_category.html',rl_item=res)

    def delete_rl_list(self,list_id):
        if self.refer_db_collection.find({ReadLaterHelper.parent_name:list_id}).count()==0:
            self.refer_db_collection.remove({self.list_id_name:int(list_id)})
            return 'true'
        return 'false'


class ReadLaterHelper:
    refer_db_collection_row_name = "row_name"
    refer_db_name = "rl"
    refer_db_collection_name='rl_list'
    history_name = "history"
    glance_name = 'glance'
    parent_name = 'parent_id'
    type_name = 'type'
    timestamp_name = 'timestamp'

    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.refer_db = self.conn[self.refer_db_name]
        self.refer_db_collection = self.refer_db[self.refer_db_collection_name]

    def _to_list(self, cursor):
        return list(cursor)

    def read_refer_list(self,list_id,offset=0,limit=10):
        result = self.refer_db_collection.find({self.parent_name:list_id})
        # result = self.refer_db_collection.find({self.parent_name:list_id}).skip(int(offset) * limit).limit(limit)
        res = self._to_list(result)
        res.reverse()
        return res

    def _read_refer_db(self, table_name=0, offset=0, limit=10):
        if table_name==0:
            result = self.refer_db_collection.find().skip(int(offset)*limit).limit(limit)
            return self._to_list(result)
        else:
            return self.refer_db_collection.find_one({self.refer_db_collection_row_name:table_name})

    def delete(self,row_name,type):
        db = self.conn[type]
        db[row_name].drop()
        self.refer_db_collection.remove({self.refer_db_collection_row_name:row_name})