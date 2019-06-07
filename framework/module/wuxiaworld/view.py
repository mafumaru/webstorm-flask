import json

import requests
from flask import render_template

from framework.core.viewcore.view import NavView
from framework.module.wuxiaworld.helper import NovelHelper


class NovelView(NavView):
    def __init__(self):
        super().__init__()
        self.helper = NovelHelper()

    def html_template(self):
        pass

    def render(self,novel):
        novel_glance = self.helper.novel(novel)
        self.set_title(novel_glance['name'])
        return render_template('wuxiaworld/dirs.html', base=self.base,novel=novel_glance)


class ChapterView(NavView):
    def __init__(self):
        super().__init__()
        self.helper = NovelHelper()

    def html_template(self):
        pass

    def render(self,novel,chapter_id):
        chapter = self.helper.chapter(novel,chapter_id)
        self.set_title(chapter['chapter_name']['en']+' | '+chapter['book_name']['en'])
        return render_template('wuxiaworld/chapter.html', base=self.base,chapter=chapter,novel=novel)

class CommentView(NavView):
    def __init__(self):
        super().__init__()

    def html_template(self):
        pass

    def render(self,novel,chapter_id,page):
        headers = {'Host': 'www.wuxiaworld.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
                   'Cache-Control': 'no-cache', 'Accept': 'application/json, text/plain, */*',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
                   'Cookie': '__cfduid=dd6ac8f0b70978d38814d78075c566c4e1545389758; _ga=GA1.2.2117771054.1545389768; _gid=GA1.2.1909350696.1545389768; __asc=013d5e90167d068a3e75d976d99; __auc=013d5e90167d068a3e75d976d99; m2hb=enabled; __gads=ID=5bf229d51e5a7995:T=1545389790:S=ALNI_MaJcB-hx4nfDFZrWNmbJbxOsfEJtg; session_depth=2; _gat=1'}

        r = requests.get("https://www.wuxiaworld.com/api/comments/" + chapter_id + "/top?page=" + page, headers=headers)
        res = r.text
        j = json.loads(res)
        data = j['items']
        n = NovelHelper()
        chapter_name = n.chapter(novel, chapter_id)['chapter_name']
        self.set_title(chapter_name['en']+' | '+chapter_name['cn'])
        return render_template('wuxiaworld/comment.html', base=self.base,next=str(int(page)+1),prev=str(int(page)-1),comments=data,chapter_id=chapter_id,total=j['total'],page=page,novel=novel,chapter_name=chapter_name)