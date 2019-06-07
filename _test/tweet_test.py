from framework.module.twitter.helper import TwitterTwitterHelper
from framework.module.twitter.twitter import TwitterTwitter

t = TwitterTwitter("Chalilili")
t.debug=True
t.get_lists()
h = TwitterTwitterHelper()
h.write_to_db(t.datacore)
print('end')