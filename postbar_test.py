import pymongo

from framework.module.tieba.helper import TiebaPostbarHelper
from framework.module.tieba.postbar import Postbar

b = Postbar('bilibili')
b.debug=True
b.get_lists()
h = TiebaPostbarHelper()
h.write_to_db(b.datacore)

# conn = pymongo.MongoClient()
# db = conn['tieba_postbar']
# db['postbar'].insert(
#     {"postbar": "bilibili", "id_list": [], "mark_id_list": []})

# print('')
