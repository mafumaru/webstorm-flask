from framework.module.wordbase.helper_beta import WordbaseHelper

w= WordbaseHelper()

def add_pure():
    w.add_pure_word(cn='测试',wordbase_collection='regular',word_type='expression',group='3',en='test',jp='')


def add_group():
    w.add_group('中文 group2-1')

def add_first():
    # w.add(add_type='first',word='trust',wordbase_collection='regular',source_type='twitter_twitter',source_table_name='GiggukAZ',source_id='1061816784863391744',word_type='wordset',group='1')
    w.add(add_type='first',word='is 90% improved',wordbase_collection='regular',source_type='twitter_twitter',source_table_name='GiggukAZ',source_id='1041230227047776256',word_type='expression',group='1')

def add_word():
    w.add(add_type='word',word='unlike',wordbase_collection='regular',source_type='twitter_twitter',source_table_name='GiggukAZ',source_id='1061287589049585669',word_type='word',group='1',word_id='',wordset_id='7')

def add_lang():
    # w.add(add_type='wordlang',word='unlike',wordbase_collection='regular',source_type='twitter_twitter',source_table_name='GiggukAZ',source_id='1061287589049585669',word_type='word',group='',word_id='11',wordset_id='7')
    # w.add(add_type='wordlang',word='ミックス',wordbase_collection='regular',source_type='twitter_twitter',source_table_name='HARUTYA1226',source_id='1075518547260932097',word_type='word',group='',word_id='11',wordset_id='7')
    # w.add(add_type='wordlang',word='上',wordbase_collection='regular',source_type='',source_table_name='',source_id='',word_type='expression',group='',word_id='3',wordset_id='')
    w.add(add_type='wordlang',word='上',wordbase_collection='regular',source_type='',source_table_name='',source_id='',word_type='expression',group='',word_id='5',wordset_id='')

def search():
    # return w.search(word='ミックス',search_type='jp')
    return w.search(word='te',search_type='en')
    # return w.search(word='上',search_type='jp')
add_pure()
# add_first()
# add_word()
# add_lang()
# s = search()
print('')