from framework.module.tieba.helper import TiebaHelper
from framework.module.tieba.tie import Tie

b = Tie('6016105907')
b.debug=True
b.get_lists()
h = TiebaHelper()
b.datacore.parent_id=1
h.write_to_db(b.datacore)
print('')