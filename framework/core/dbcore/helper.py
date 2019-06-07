from abc import ABC, abstractmethod
from framework.core.dbcore.datacore import DataCoreTable

import pymongo

from framework.module.rl.helper import ReadLaterHelper


class BaseHelper(ABC):
    db_name=''

    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn[self.db_name]

    def _to_list(self,cursor):
        return list(cursor)

    def read(self,collection,offset=0,limit=10):
        result = self.db[collection].find().skip(int(offset) * limit).limit(limit)
        return self._to_list(result)

class ReferHelper(ABC):
    db_name = ""

    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn[self.db_name]
        self.read_later_helper = ReadLaterHelper()

    def write_to_db(self, data_core: DataCoreTable):
        data_core.type = self.db_name
        self.delete(data_core.table_name)
        colloction = self.db[data_core.table_name]
        colloction.insert(data_core.listdata)

        self.read_later_helper.refer_db_collection.insert(self._get_refer_row(data_core))# 版本更新时注释

    def _to_list(self, cursor):
        return list(cursor)

    def read_from_db(self,table_name,history=0,offset=0,limit=10):
        result =  self.db[table_name].find(self._read_db_conditon(table_name, history)).skip(int(offset) * limit).limit(limit)
        return self._to_list(result)

    def _get_refer_row(self, data_core: DataCoreTable):
        rl_row = {
            self.read_later_helper.refer_db_collection_row_name: data_core.table_name,
            self.read_later_helper.history_name: self._parse_first_history(data_core.listdata[0]),
            self.read_later_helper.glance_name: self._parse_glance(data_core),
            self.read_later_helper.parent_name: data_core.parent_id,
            self.read_later_helper.type_name: self.db_name,
            self.read_later_helper.timestamp_name: 0
        }
        return rl_row

    def _read_db_conditon(self, table_name, history):
        if history==0:
            real_history = self.get_history(table_name)
        else:
            real_history=history
        offset_history = self.db[table_name].find_one(self._parse_db_offset_condition(real_history))
        return {'_id':{'$gte':offset_history['_id']}}

    def _parse_db_offset_condition(self, history):
        return {'.'.join(self._history_depth()): history}

    def get_history(self,table_name):
        history=self.read_later_helper._read_refer_db(table_name)[self.read_later_helper.history_name]
        return history

    @abstractmethod
    def _parse_glance(self, data_core):
        pass

    @abstractmethod
    def _history_depth(self)->list:
        pass

    def _parse_first_history(self, list_first_data):
        for depth in self._history_depth():
            list_first_data = list_first_data[depth]
        return list_first_data


    def set_history(self,history,table_name):
        self.read_later_helper.refer_db_collection.update({self.read_later_helper.refer_db_collection_row_name:table_name}, {'$set': {self.read_later_helper.history_name: history}})

    def reset_history(self,table_name):
        first_row = self.db[table_name].find_one()
        self.set_history(self._parse_first_history(first_row), table_name)

    def delete(self, table_name):
        self.db.drop_collection(table_name)
        self.read_later_helper.refer_db_collection.remove({self.read_later_helper.refer_db_collection_row_name: table_name})# 版本更新时注释

class IntReferHelper(ReferHelper):
    def read_from_db(self, table_name, history=0, offset=0, limit=10):
        return super().read_from_db(table_name, int(history), offset, limit)

    def set_history(self, history, table_name):
        super().set_history(int(history), table_name)

class CollectionHelper(ABC):
    db_name = ''
    collection_name=''

    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn[self.db_name]
        self.collection=self.db[self.collection_name]

    def _to_list(self, cursor):
        return list(cursor)

    def add(self,**args):
        self.inner_add(args)
        self.inc_max_id()

    def inner_add(self,args:dict):
        id = self.get_max_id()
        if 'id' not in args.keys():
            args['id']=id
        item = self.get_data_struct(args)
        self.collection.insert(item)

    @abstractmethod
    def get_data_struct(self, args):
        pass

    def inc_max_id(self):
        r = self.db['max_id'].find_one({'max_type': self.collection_name})
        self.db['max_id'].update({'max_type': self.collection_name}, {'$set': {'max_id': r['max_id'] + 1}})

    def delete(self,**args):
        self.collection.remove({'id':int(args['id'])})

    def show_all(self,**args):
        condition = self.show_all_condition(**args)
        if condition:
            res = self.collection.find(condition)
        else:
            res = self.collection.find()
        return self._to_list(res)

    def show_all_condition(self,**args):
        return None

    def get_max_id(self):
        r = self.db['max_id'].find_one({'max_type': self.collection_name})
        if not r:
            r = {
                'max_type': self.collection_name,
                'max_id': 0
            }
            self.db['max_id'].insert(r)
        return r['max_id']

