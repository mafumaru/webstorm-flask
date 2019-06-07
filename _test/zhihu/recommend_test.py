from framework.module.zhihu.recommend import ZhihuRecommend

r= ZhihuRecommend()
r.init("")
rec = r.get_data()
print('')