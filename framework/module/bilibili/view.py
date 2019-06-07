from flask import render_template

from framework.core.viewcore.view import NavView
from framework.module.bilibili.helper import BilibiliRelateHelper


class BilibiliRelateView(NavView):
    def __init__(self):
        super().__init__()
        self.set_title('Bilibili Relate')
        self.helper = BilibiliRelateHelper()

    def html_template(self):
        pass

    def resume_view(self,id): # id
        resume = self.helper.resume(id)
        return render_template('bilibili/relate/relate.html',base=self.base,resume=resume,root_id=id)

    def relate_view(self,**args):# id , *parent_id , root_id
        data = self.helper.relate_collection.find_one({'aid':int(args['id'])})
        if not data:
            data = self.helper.add(aid=args['id'],type='node',parent_aid=args['parent_id'])
        # self.helper.resume(id=parent_id) # ?
        return render_template('bilibili/relate/relate.html', base=self.base, resume=data,root_id=args['root_id'])

    def back_view(self,id,root_id):
        data = self.helper.relate_collection.find_one({'aid':int(id)})
        return render_template('bilibili/relate/relate.html', base=self.base, resume=data,root_id=root_id)

    def relates(self):
        data = self.helper.show_all()
        return render_template('bilibili/relate/relates.html', base=self.base, data=data)