from framework.module.zhihu.search import ZhihuSearch

t = ZhihuSearch("日语")
t.debug=True
t.get_lists()
# h = TwitterCommentHelper()
# h.write_to_db(t.datacore)
print('')