import pymongo

db_name = 'wuxiaworld'
book_name = 'issth'
conn = pymongo.MongoClient()
db = conn[db_name]
collection = db[book_name]
novel_list_collection = db['novels']

t = list(collection.find())
t2 = t[-1]
print('')
