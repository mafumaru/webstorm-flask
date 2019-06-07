# https://www.youtube.com/watch?v=pRjAfs4bJDI
from framework.module.youtube.comment import YoutubeComment

yt = YoutubeComment('pRjAfs4bJDI')
# yt = YoutubeComment('nbYHdvD8Bus')
yt.debug=True
yt.get_lists()
print('end')