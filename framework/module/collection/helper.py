import json

import pymongo


class CollectionHelper:
    id_name = "self_id"
    parent_id='parent_id'

    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.refer_db = self.conn['collection']
        self.refer_db_collection = self.refer_db['collection_dir']
        self.collection_list = list(self.refer_db_collection.find())
        for item in self.collection_list:
            item.pop('_id')
        self.collecton = self.refer_db['collection']
        # self.collection_list = [
        #     {'text': '收藏1', 'self_id': 1, 'parent_id': 0},
        #     {'text': '收藏2', 'self_id': 2, 'parent_id': 0},
        #     {'text': '收藏3', 'self_id': 3, 'parent_id': 1},
        #     {'text': '收藏4', 'self_id': 4, 'parent_id': 1},
        #     {'text': '收藏5', 'self_id': 5, 'parent_id': 3},
        #     {'text': '收藏6', 'self_id': 6, 'parent_id': 2},
        #     {'text': '收藏7', 'self_id': 7, 'parent_id': 6}
        # ]

    def _to_list(self, cursor):
        return list(cursor)

    def list_to_tree(self, listdata):
        tree = []
        for treenode in listdata:
            if treenode['parent_id'] == 0:
                tree.append(treenode)
                self.init_node(treenode)
            for it in listdata:
                if it['parent_id'] == treenode['self_id']:
                    if 'nodes' not in treenode.keys():
                        treenode['nodes'] = []
                    self.init_node(it)
                    treenode['nodes'].append(it)
        return tree

    def init_node(self, node: dict):
        # node['state'] = {
        #     'selected': True
        # }
        # node['backColor']='#ffffff'
        # pass
        node['href']='/module/collection/view/CollectionView/render?list_id='+str(node[CollectionHelper.id_name])
        # if mod == "choose":
        #     node['icon'] = "glyphicon glyphicon-unchecked"
        #     node['selectedIcon'] = "glyphicon glyphicon-check"
        # elif mod == "show":
        #     node['icon'] = ""
        #     node['selectedIcon'] = ""

    def add_dir(self, name, parent_id):
        new_id = self.get_new_id()
        data = {'text': name, 'self_id': new_id, 'parent_id': int(parent_id)}
        self.refer_db_collection.insert(data)
        return str(new_id)

    def delete_dir(self, id):
        if self.refer_db_collection.find({CollectionHelper.parent_id: int(id)}).count() == 0 and self.collecton.find({'collection_parent_id':int(id)}).count()==0:
            self.refer_db_collection.remove({CollectionHelper.id_name: int(id)})
            return 'true'

    def get_new_id(self):
        if self.refer_db_collection.find().count() == 0:
            return 1
        else:
            return self._to_list(self.refer_db_collection.find().sort([(CollectionHelper.id_name,-1)]).limit(1))[0][
                       CollectionHelper.id_name] + 1

    def add_collection(self, parent_id,type,table_name,id):
        res = self.conn[type][table_name].find_one({'id':int(id)})
        res['collection_parent_id']=int(parent_id)
        res['collection_type']=type
        self.collecton.insert(res)

    def delete_collection(self, id):
        self.collecton.remove({'id':int(id)})
        return 'true'

    def read_refer_list(self,list_id,offset=0,limit=10):
        result = self.collecton.find({'collection_parent_id': int(list_id)}).skip(int(offset) * limit).limit(limit)
        return self._to_list(result)

    def get_collection_tree(self):
        treedata = self.list_to_tree(self.collection_list)
        tree = [{
            'text':'收藏',
            CollectionHelper.id_name:0,
            'nodes':treedata
        }]
        return json.dumps(tree)
