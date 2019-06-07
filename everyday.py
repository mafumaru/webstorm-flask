from framework.module.tieba.helper import TiebaPostbarHelper
from framework.module.tieba.postbar import Postbar

h = TiebaPostbarHelper()
for bar in h.get_bars():
    b = Postbar(bar)
    b.get_lists()
    h = TiebaPostbarHelper()
    h.write_to_db(b.datacore)