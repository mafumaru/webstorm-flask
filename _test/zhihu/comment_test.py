from framework.module.zhihu.comment import ZhihuComment

c=ZhihuComment('473336250')
c.debug=True
r =c.get_lists()

print('')