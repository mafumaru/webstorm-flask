from framework.core.dbcore.helper import BaseHelper
from framework.module.bilibili.relate import BilibiliRelate


class BilibiliRelateHelper(BaseHelper):
    db_name = 'bilibili_relate'

    def __init__(self):
        super().__init__()
        self.relate_collection = self.db['relate']
        self.manage_collection = self.db['manage']
        # self.history_collection = self.db['history']
        # self.resume_collection = self.db['resume'] # ?

    def add_root(self,**args):
        url = args['url']
        if 'av' in url:
            index=url.index('av')
            url=url[index+2:]
        self.add(aid=url,type='root')

    def add(self,**args): #aid ,type:root,node(,parent_aid )
        r = BilibiliRelate()
        r.init(args['aid'])
        data = r.get_data()
        if args['type'] == 'root':
            data['is_root'] = True
            data['resume'] = int(args['aid'])
        else:
            data['is_root'] = False
            data['parent_pointer'] = int(args['parent_aid'])

        data['read_history'] = 0
        ids = self.manage_collection.find_one({'type':'id'})

        if not ids:
            ids = {'type':'id' ,'id_list':[int(args['aid'])]}
            self.manage_collection.insert(ids)

        id_list = ids['id_list']
        for item in list(data['relates']):
            if 'aid' not in item.keys():
                data['relates'].remove(item)
                continue
            if item['aid'] in id_list:
                data['relates'].remove(item)
            else:
                ids['id_list'].append(item['aid'])

        self.relate_collection.insert(data)
        self.manage_collection.save(ids)
        # write read enter

        if args['type'] =='node':
            return data

    # def add_root(self,**args): #aid
    #     r = BilibiliRelate()
    #     r.init('')
    #     data = r.get_data()
    #     data['is_root']=True
    #
    #     self.relate_collection.insert(data)

    # def add_node(self,**args): #aid ,parent_aid
    #     r = BilibiliRelate()
    #     r.init('')
    #     data = r.get_data()
    #     data['is_root'] = False
    #     data['parent_aid'] = args['']
    #
    #     self.relate_collection.insert(data)
    def show_all(self):
        data = list(self.relate_collection.find({'is_root':True}))
        data.reverse()
        return data

    def resume(self , id):
        resume_id = self.relate_collection.find_one({'aid':int(id)})['resume']
        resume = self.relate_collection.find_one({'aid':resume_id})
        return resume

    def set_resume(self ,id ,resume_id):
        self.relate_collection.update({'aid':int(id)},{'$set':{'resume':int(resume_id)}})

    def set_history(self,id ,history):
        self.relate_collection.update({'aid': int(id)}, {'$set': {'read_history': int(history)}})

    # need this ?
    def get_history(self,id):
        return self.relate_collection.find_one({'aid':int(id)})['history']

    def delete(self,id):
        self.relate_collection.remove({'aid':int(id)})

# url = '/av1111'
# index=url.index('av')
# id =url[index+2:]
# print('')


