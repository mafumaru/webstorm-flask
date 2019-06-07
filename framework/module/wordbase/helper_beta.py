from flask import render_template
from langid import langid

from framework.core.dbcore.helper import BaseHelper
from framework.module.wordbase.translation import Translation, BaiduSelectTranslation
from framework.tools.timedate import get_ms_time


class WordbaseHelper(BaseHelper):
    db_name = 'wordbase'
    collection_list = ['fresh','regular','fun','tri']


    def __init__(self):
        super().__init__()
        self.source=''
        self.collection = {
            'sentence':'sentence',
            'wordset':'wordset',
            'expression':'expression',
            'group':'group',
            'max_id':'max_id'
        }

    # def first_add(self,word,wordbase_collection,source_type,source_table_name,source_id,word_type,group):
    #     pass
    # def add_to_wordset(self,word,wordbase_collection,source_type,source_table_name,source_id,word_type,group,word_id,wordset_id):
    #     pass
    # def add_to_wordlang(self,word,wordbase_collection,source_type,source_table_name,source_id,word_type,group,word_id,wordset_id):
    #     pass
    #
    # def add_word_pure_translate(self,cn,wordbase_collection,word_type,group,word_id,wordset_id,en='',jp=''):
    #     pass

    def get_groups(self):
        r = self.db[self.collection['group']].find()
        return self._to_list(r)

    def get_groups_view(self):
        return render_template('wordbase/groups.html',list=self.get_groups())

    def delete_groups(self,id):
        self.db[self.collection['group']].remove({'group_id':int(id)})
        return 'true'

    def add_group(self,group_name):
        max_id = self.get_max_num('group')
        group = {
            'group_name':group_name,
            'group_id':max_id+1
        }
        self.db[self.collection['group']].insert(group)
        self.db[self.collection['max_id']].update({'max_type': 'group'}, {'$set': {'max_id': group['group_id']}})
        return render_template('wordbase/groups.html',list=[group])

    def get_max_num(self,type):# group , wordset_id , word_id
        r = self.db[self.collection['max_id']].find_one({'max_type':type})
        # if r.count()==0:
        if not r:
            r= {
                'max_type':type,
                'max_id':0
            }
            self.db[self.collection['max_id']].insert(r)
        # else:
        #     r['max_id'] +=1
        self.db[self.collection['max_id']].update({'max_type':type}, {'$set':{'max_id': r['max_id'] + 1}})
        return r['max_id']

    def tag(self,**args):
        pass

    def filter_search(self,**args):# * group -list, * wordbase_collection , * date(最近) , * wordt_type  | offset , limit
        pass

    def add_pure_word(self,**args):#
        row = self.word_type(args)

        if args['word_type'] == 'expression':
            row['translate'] = args['cn']
        elif args['word_type'] == 'sentence':
            row['translate'] = args['cn']
        elif args['word_type'] == 'word':
            row['translate'] = args['cn']
        elif args['word_type'] == 'wordset':
            row['wordset'][0]['translate'] = args['cn']

        if args['en']:
            self.clean_word = args['en']
            row = self.init_word(row)
        if args['jp']:
            self.clean_word = args['jp']
            row = self.init_word(row)
        self.insert(row, args['word_type'])

    def search(self,args):# keyword
        clean_word = args['word'].strip()
        if args['search_type']=='zh':
            wordset_result = self.db[self.collection['wordset']].find({
                'wordset.translate': {
                    '$regex': clean_word
                }
            })
            expression_result = self.db[self.collection['expression']].find({
                'translate': {
                    '$regex': clean_word
                }
            })
            sentence_result = self.db[self.collection['sentence']].find({
                'translate': {
                    '$regex': clean_word
                }
            })
        elif args['search_type']=='jp' or args['search_type']=='en':
            wordset_result = self.db[self.collection['wordset']].find({
                'wordset.'+args['search_type']+'.word': {
                    '$regex': clean_word
                }
            })
            expression_result = self.db[self.collection['expression']].find({
               args['search_type']+'.expression': {
                    '$regex': clean_word
                }
            })
            sentence_result = self.db[self.collection['sentence']].find({
               args['search_type']+'.sentence': {
                    '$regex': clean_word
                }
            })
        else:
            return None
        res = self._to_list(wordset_result)+self._to_list(expression_result)+self._to_list(sentence_result)
        return res

    def search_view(self,**args):# search(args)
        list = self.search(args)
        return render_template('wordbase/search_view.html',list=list)

    def add(self,**args):
        self.clean_word = args['word'].strip()

        if args['source_type']:
            source = self.conn[args['source_type']][args['source_table_name']].find_one({'id': int(args['source_id'])})
            if args['source_type'] == 'twitter_twitter':
                temp = source['html'].replace(self.clean_word, '<span class="wordbase-highlight">' + self.clean_word + '</span>')
                source['html'] = temp
            source['collection_type'] = args['source_type']
            source['wordbase_type'] = 'collection_type'
            self.init_source(source)

        self.inner_add(args)

    def inner_add(self,args):
        if args['add_type']=='first':
            row = self.word_type(args)
            row = self.init_word(row)
            self.insert(row,args['word_type'])

        elif args['add_type']=='word':
            row = self.db[self.collection['wordset']].find_one({'wordset_id':int(args['wordset_id'])})
            word = self.word_type(args)
            word = self.init_word(word)
            row['wordset'].append(word)
            self.db[self.collection['wordset']].update({'wordset_id':int(args['wordset_id'])}, {'$set':{'wordset':row['wordset']}})

        elif args['add_type']=='wordlang':
            if args['word_type'] == 'expression':
                row = self.db[self.collection['expression']].find_one({'word_id': int(args['word_id'])})
                row = self.init_word(row)
                self.db[self.collection['expression']].save(row)
            elif args['word_type'] == 'sentence':
                row = self.db[self.collection['sentence']].find_one({'word_id':int(args['word_id'])})
                row = self.init_word(row)
                self.db[self.collection['sentence']].save(row)
            elif args['word_type'] == 'word':
                row = self.db[self.collection['wordset']].find_one({
                    'wordset.word_id': {
                        '$eq': int(args['word_id'])
                    }
                })

                index=0
                for i in range(len(row['wordset'])):
                    if row['wordset'][i]['word_id']==int(args['word_id']):
                        index= i
                        break
                row['wordset'][index] = self.init_word(row['wordset'][index])
                self.db['wordset'].update({'wordset_id':int(args['wordset_id'])},{'$set':{'wordset':row['wordset']}})
        else:
            return 'false'
        return 'true'

    def word_type(self,args):
        res = None
        group = self.db[self.collection['group']].find_one({'group_id':int(args['group'])})
        if args['word_type']=='expression':
            res = {
                'word_type': args['word_type'],
                'translate': None,
                'word_id':self.get_max_num('expression')+1,
                'group': [group['group_name']],
                'wordbase_collection': args['wordbase_collection'],
                'date':get_ms_time(),
                "en": {
                    'expression': None,
                    'source': []
                },
                "jp": {
                    'expression': None,
                    'source': []
                }
            }

        elif args['word_type']=='sentence':
            res={
                'word_type':args['word_type'],
                'translate': None,
                'word_id': self.get_max_num('sentence')+1,
                'group': [group['group_name']],
                'wordbase_collection': args['wordbase_collection'],
                'date': get_ms_time(),
                "en": {
                    'sentence': None,
                    'source': []
                },
                "jp": {
                    'sentence': None,
                    'source': []
                }
            }
        elif args['word_type']=='wordset':
            res = {
                'wordset_id':self.get_max_num('wordset')+1,
                'word_type':args['word_type'],
                'wordset':[
                    {
                        'word_type': 'word',
                        'translate':None,
                        'word_id':self.get_max_num('word')+1,
                        'group':[group['group_name']],
                        'wordbase_collection': args['wordbase_collection'],
                        'date': get_ms_time(),
                        "en": {
                            'word':None,
                            'pronounce':None,
                            'source':[]
                        },
                        "jp": {
                            'word':None,
                            'pronounce':None,
                            'source':[]
                        }
                    }
                ]
            }
        elif args['word_type']=='word':
            res = {
                'word_type': 'word',
                'translate': None,
                'word_id': self.get_max_num('word')+1,
                'group': [group['group_name']],
                'wordbase_collection': args['wordbase_collection'],
                'date': get_ms_time(),
                "en": {
                    'word': None,
                    'pronounce': None,
                    'source': []
                },
                "jp": {
                    'word': None,
                    'pronounce': None,
                    'source': []
                }
            }

        return res

    def insert(self,res,collection):
        self.db[collection].insert(res)

    def init_word(self,res):
        lang = self.analysis_word(self.clean_word)
        translate = Translation().translate_with_pronounce(self.clean_word)
        if res['word_type'] == 'expression':
            if res[lang]['expression']:
                pass
            else:
                res[lang]['expression'] = self.clean_word
                if not res['translate']:
                    res['translate'] = translate[0]
            if self.source:
                res[lang]['source'].append(self.source)
        elif res['word_type'] == 'sentence':
            if res[lang]['sentence']:
                pass
            else:
                res[lang]['sentence'] = self.clean_word
                if not res['translate']:
                    res['translate'] = translate[0]
            if self.source:
                res[lang]['source'].append(self.source)
        elif res['word_type'] == 'word':
            if res[lang]['word']:
                pass
            else:
                res[lang]['word'] = self.clean_word
                if not res['translate']:
                    res['translate'] = translate[0]
                res[lang]['pronounce'] = translate[1]
            if self.source:
                res[lang]['source'].append(self.source)
        elif res['word_type'] == 'wordset':
            res['wordset'][0][lang]['word'] = self.clean_word
            res['wordset'][0]['translate'] = translate[0]
            res['wordset'][0][lang]['pronounce'] = translate[1]
            if self.source:
                res['wordset'][0][lang]['source'].append(self.source)

        return res

    def init_source(self,source):
        self.source= source

    def analysis_word(self,word):
        if langid.classify(word)[0]=='ja':
            return 'jp'
        elif langid.classify(word)[0]=='zh':
            return 'jp'
        elif langid.classify(word)[0]=='en':
            return 'en'
        else:
            return 'en'

class ChineseHelper(BaseHelper):
    db_name = 'wordbase'
    collection_list = ['foreign','source']

    def __init__(self):
        super().__init__()

    def add_word(self,word,collection,explanation):
        self.db[collection].insert({'word':word,'explanation':explanation})