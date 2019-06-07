from bs4 import BeautifulSoup

from framework.core.dbcore.datacore import DataCoreTable
from framework.core.dbcore.helper import IntReferHelper, ReferHelper
from framework.module.tieba.postbar import update_content
from framework.module.tieba.tie import update_tie_content


class TiebaPostbarHelper(IntReferHelper):
    db_name = 'tieba_postbar'

    def _history_depth(self) -> list:
        return ['id']

    def _parse_glance(self, data_core):
        pass

    def write_to_db(self, data_core: DataCoreTable):
        bar_manage= self.db['postbar'].find_one({'postbar':data_core.table_name})
        if not bar_manage:
            bar_manage={'postbar':data_core.table_name,'id_list':[],'mark_id_list':[]}
            # self.db['postbar'].insert(bar_manage)
        db_id_list=bar_manage['id_list']
        mark_id_list=bar_manage['mark_id_list']
        id_list=[]

        # identity_list

        for item in list(data_core.listdata):
            if item['id'] in db_id_list or item['reply_count']<150:
                if item['id'] in mark_id_list:
                    # 如果回复数增长超过200，则再次录入？
                    pass
                data_core.listdata.remove(item)
            else:
                id_list.append(item['id'])
        bar_manage['id_list']+=id_list
        data_core.listdata.sort(key=lambda e: e['reply_count'], reverse=True)
        print(len(data_core.listdata))
        first_flag=True
        for item in data_core.listdata:
            try:
                self.db[data_core.table_name].insert(item)
                if first_flag:
                    first_tie = item
                    first_flag=False
            except:
                pass
        # self.db[data_core.table_name].insert(data_core.listdata)
        self.db['postbar'].save(bar_manage)

        identity_history_manage = {
            'postbar': data_core.table_name,
            'identity': first_tie['identity'],
            'history': first_tie['id']
        }
        self.db['identity'].insert(identity_history_manage)

    def get_bars(self):
        bars_info = self.db['postbar'].find()
        bars = []
        for bar in bars_info:
            bars.append(bar['postbar'])
        return bars

    def get_all_identity(self,postbar):
        all = self.db['identity'].find({'postbar':postbar})
        res = self._to_list(all)
        res.reverse()
        return res

    def get_identity_history(self,**args):#identity,postbar
        history = self.db['identity'].find_one({'$and':[{'identity':int(args['identity'])},{'postbar':args['postbar']}]})
        return history['history']

    def set_identity_history(self,**args):
        self.db['identity'].update({'$and':[{'identity':int(args['identity'])},{'postbar':args['postbar']}]},{'$set':{'history':int(args['history'])}})

    def get_identity_tie(self,args):# identity , postbar , offset=0 , limit=10 , history
        # res = self.db[args['postbar']].find(self._select_conditon(args)).skip(int(args['offset']) * int(args['limit'])).limit(int(args['limit']))
        res = self.db[args['postbar']].find({'$and':[{'identity':int(args['identity'])},self._select_conditon(args)]}).skip(int(args['offset']) * int(args['limit'])).limit(int(args['limit']))
        # print(res.count())
        return self._to_list(res)

    def _select_conditon(self,args:dict):
        if 'history' not in args.keys():
            real_history = self.get_identity_history(**args)
        else:
            real_history=int(args['history'])
        offset_history = self.db[args['postbar']].find_one(self._parse_db_offset_condition(real_history))
        # print(offset_history)
        return {'_id':{'$gte':offset_history['_id']}}

    def mark(self,id,m_identity,identity,postbar):
        tie_glance = self.db[postbar].find_one({'id':int(id)})
        tie_glance['m_identity']=int(m_identity)
        self.db[postbar].save(tie_glance)

        mark = self.get_single_mark(int(m_identity),postbar)
        if not mark:
            mark_manage = {
                'postbar': postbar,
                'm_identity': int(m_identity),
                'identity': int(identity)
            }
            self.db['mark'].insert(mark_manage)

    def get_single_mark(self,m_identity,postbar):
        return self.db['mark'].find_one({'$and':[{'postbar':postbar},{'m_identity':int(m_identity)}]})

    def get_mark_lsit(self,m_identity,identity,postbar):
        mark_lists = self.db['mark'].find({'$and':[{'postbar':postbar},{'identity':int(identity)}]})
        return self._to_list(mark_lists)

    def review_mark(self,m_identity,postbar):
        all_mark = self.db[postbar].find({'m_identity': int(m_identity)})
        return self._to_list(all_mark)

    def update_html(self):
        for collection_name in self.get_bars():
            collection = self.db[collection_name]
            records = collection.find()
            for record in records:
                tag = BeautifulSoup(record['html'])
                li = tag.find('li',class_='j_thread_list')
                new_tag = update_content(li,collection_name,record['id'])
                record['html'] = new_tag.prettify()
                collection.save(record)

class TiebaTieHelper(ReferHelper):
    db_name = 'tieba_tie'

    def _history_depth(self) -> list:
        return ['mix_id']

    def _parse_glance(self, data_core):
        pass

    def update_html(self):
        collection_names = self.db.collection_names()
        for collection_name in collection_names:
            collection = self.db[collection_name]
            records = collection.find()
            for record in records:
                tag = BeautifulSoup(record['html'])
                new_tag = update_tie_content(tag,collection_name,record['mix_id'])
                record['html'] = new_tag.prettify()
                collection.save(record)
