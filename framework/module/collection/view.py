from framework.core.viewcore.view import  CListView
from framework.module.collection.helper import CollectionHelper


class CollectionView(CListView):

    def __init__(self):
        super().__init__()
        self.set_title('Collection Page')
        self.refer_list_helper = CollectionHelper()
        self.base['collection'] = {
            'table_name': None,
            'type': None
        }

    def ajax_list_template(self):
        return 'collection/collection_list_content.html'

    def html_template(self):
        return 'collection/collection_page.html'