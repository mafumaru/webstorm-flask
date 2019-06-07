import pymongo


class NovelHelper:
    db_name = 'wuxiaworld'
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn[self.db_name]
        self.novel_list_collection = self.db['novels']

    def chapter(self,book_name,id):
        collection = self.db[book_name]
        return collection.find_one({'id':int(id)})

    def delete_p(self,book_name,id,type,p):
        collection = self.db[book_name]
        old = collection.find_one({'id':int(id)})
        old['text'][type][int(p)-1] = old['text'][type][int(p)-1]+old['text'][type][int(p)]
        del old['text'][type][int(p)]
        collection.update({'id':int(id)},{'$set':{'text':old['text']}})
        return 'true'


    def novel(self,book_name):
        return self.novel_list_collection.find_one({'id':book_name})

# class ChapterCommentHelper:
#     db_name = 'chapter_comment'
#     def __init__(self):
#         self.conn = pymongo.MongoClient()
#         self.db = self.conn[self.db_name]
#
#     def write(self,chapter_id,list):
#         collection = self.db[chapter_id]
#         collection.insert(list)
#
#     def read(self,chapter_id):
#         collection = self.db[chapter_id]
#         return  list(collection.find())