import json

import pymongo
import requests

from framework.module.wuxiaworld.chapter import get_douluo_dalu_chapters
from framework.module.wuxiaworld.comment import WuxiaworldComment
from framework.module.wuxiaworld.helper import NovelHelper
from framework.module.wuxiaworld.novel import get_issth


def main():
    db_name = 'wuxiaworld'
    book_name = 'douluodalu'
    conn = pymongo.MongoClient()
    db = conn[db_name]
    collection = db[book_name]
    novel_list_collection = db['novels']

    # t = list(collection.find())
    # t2 = t[-10:]
    # print('')

    def write_novel_to_db():
        issth = get_douluo_dalu_chapters()
        issth_glance = {
            'name': 'Douluo Dalu',
            'id': book_name,
            'chapters': issth[0]
        }
        collection.insert(issth[1])
        novel_list_collection.remove({'id':book_name})
        novel_list_collection.insert(issth_glance)

    def dir_update():
        dir = novel_list_collection.find()[0]
        dir['id'] = book_name
        novel_list_collection.remove({'name': 'I Shall Seal the Heavens'})
        novel_list_collection.insert(dir)

    def delete_p():
        # old = collection.find()
        # db['delete_p'].insert(old)
        n = NovelHelper()
        n.delete_p('delete_p','4670','en','0')

    # def chapter_comment():
    #     chapters = novel_list_collection.find_one({'id':book_name})['chapters']
    #     h = ChapterCommentHelper()
    #     for chapter in chapters:
    #         chapter_id = chapter['chapter_id']
    #         print(chapter_id)
    #         w = WuxiaworldComment(chapter_id)
    #         w.debug=True
    #         w.get_lists()
    #         reply = w.datacore.listdata
    #         print(chapter['en']+' = '+str(len(reply))+'(total)')
    #         h.write(chapter_id,reply)
    def context_chapter():
        chapters = list(collection.find())
        count = len(chapters)
        for index in range(count):
            if index ==0:
                chapters[index]['prev'] = ''
                chapters[index]['next'] = chapters[index + 1]['id']
            elif index == count-1:
                chapters[index]['prev'] = chapters[index - 1]['id']
                chapters[index]['next'] = ''
            else:
                chapters[index]['prev'] = chapters[index - 1]['id']
                chapters[index]['next'] = chapters[index + 1]['id']

        db.drop_collection(book_name)
        db[book_name].insert(chapters)
    write_novel_to_db()
main()
print('')
def realtime_chapter_comment(chapter,page):
    headers = {'Host': 'www.wuxiaworld.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
               'Cache-Control': 'no-cache', 'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
               'Cookie': '__cfduid=dd6ac8f0b70978d38814d78075c566c4e1545389758; _ga=GA1.2.2117771054.1545389768; _gid=GA1.2.1909350696.1545389768; __asc=013d5e90167d068a3e75d976d99; __auc=013d5e90167d068a3e75d976d99; m2hb=enabled; __gads=ID=5bf229d51e5a7995:T=1545389790:S=ALNI_MaJcB-hx4nfDFZrWNmbJbxOsfEJtg; session_depth=2; _gat=1'}

    r = requests.get("https://www.wuxiaworld.com/api/comments/"+chapter+"/top?page="+page,headers=headers)
    res = r.text
    j = json.loads(res)
    data = j['items']

    print('')
# realtime_chapter_comment('4671','1')