from framework.module.twitter.comment import TwitterComment
from framework.module.twitter.helper import TwitterCommentHelper

t = TwitterComment("HARUTYA1226-1036133716962115584")
t.debug=True
t.get_lists()
h = TwitterCommentHelper()
h.write_to_db(t.datacore)
print('')