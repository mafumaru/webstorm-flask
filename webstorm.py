import json
import os

import time

import requests
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from framework.module.rl.helper import ReadLaterDirHelper
from framework.module.twitter.iframe import TwitterIframe
from framework.module.wordbase.helper import WordbaseHelper
from framework.module.wuxiaworld.helper import NovelHelper
from framework.module.zhihu.tools import ZhihuAnswerTool
from index import Index

app = Flask(__name__)
def rl_list_item_type(item_type:str):
    temp = item_type.split('_')
    return temp[0]+'/'+temp[1]+'.html'

def collection_item_type(item_type:str):
    temp = item_type.split('_')
    return temp[0]+'/'+temp[1]+'/item.html'

def zhihu_question_filter(item_type:str):
    return item_type[0:item_type.find('answer')-1]

app.add_template_filter(ZhihuAnswerTool.clear_details,"clear_zhihu_answer")
app.add_template_filter(rl_list_item_type,"rl_list_item_type_filter")
app.add_template_filter(collection_item_type,"collection_item_filter")
app.add_template_filter(zhihu_question_filter,"zhihu_question_filter")

@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    # return time.strftime("%Y-%b-%d %a %H:%M", time.localtime(date))
    return time.strftime("%Y %b %d %a %H:%M", time.localtime(date))
    # return time.strftime("%Y-%m-%d %H:%M", time.localtime(date))

@app.route('/')
def hello_world():
    # base = {
    #     'title':'rl test',
    #     'nav':[
    #     {'list_name':'分类','list_id':1},
    #     {'list_name':'分类','list_id':1},
    #     {'list_name':'分类','list_id':1},
    #     {'list_name':'分类','list_id':1},
    #     {'list_name':'分类','list_id':1}
    # ]
    # }
    # return render_template('rl/rl_homepage.html',base=base)
    # return render_template('collection/collection_page.html')
    # return render_template('_test/collection/demo.html')

    return render_template('index.html',base={'title':'Webstorm','nav':ReadLaterDirHelper().get_rl_list()})

# @app.route('/demo')
# def demo():
#     return render_template('_test/collection/demo.html')
#

@app.route('/test')
def treeview():
    lists = [{
        'name':'out1',
        'en':[{'name':'out1-en-inner1'},{'name':'out1-en-inner2'}],
        'jp':[{'name':'out1-jp-inner1'},{'name':'out1-jp-inner2'}]
    },{
        'name':'out2',
        'en':[{'name':'out2-en-inner1'},{'name':'out2-en-inner2'}],
        'jp':[{'name':'out2-jp-inner1'},{'name':'out2-jp-inner2'}]
    },{
        'name':'out3',
        'en':[{'name':'out3-en-inner1'},{'name':'out3-en-inner2'}],
        'jp':[{'name':'out3-jp-inner1'},{'name':'out3-jp-inner2'}]
    }
    ]
    return render_template('_test/wordbase/double_loop_test.html',data=lists)
    # return render_template('_test/wordbase/copy.html')
    # return render_template('wordbase/chinese_list_content.html')

@app.route('/angular')
def angular():
    dict = {
        'code':200,
        'data':{
            'name':'test'
        }
    }

    return json.dumps(dict)


@app.route('/twitter/iframe')
def iframe():
    id = request.values.to_dict()['twiiter_id']
    iframe = TwitterIframe()
    iframe.init(id)
    data = iframe.get_data()
    return render_template('twitter/twitter/iframe.html', iframe=data,base={'title':'Twitter iframe'})

@app.route('/module/<module>/<component>/<controller>/<method>', methods=["GET", "POST"])
def module(module, component,controller,method):
    # print(request.values.to_dict())
    index = Index(module, component, controller, method,request.values.to_dict())
    return index.render()

@app.route('/video', methods=[ "POST"])
def video():
    video = request.files['video']
    subtitle = request.files['subtitle']
    # print(request.headers)
    # basepath = 'D:\BaiduYunDownload'
    basepath = '/root/webstorm/static/videos'
    # filename = secure_filename(uploaded_file1.filename)
    upload_path = os.path.join(basepath, video.filename)
    video.save(upload_path)
    upload_path = os.path.join(basepath, subtitle.filename)
    subtitle.save(upload_path)

    data = request.values.to_dict()
    source = {
        "videoname": data['filename'],
        "wordbase_type": "video"
    }
    w = WordbaseHelper()
    w.init_source(source)
    w.inner_add(**data)

    return "true"

# def wuxiaworld_chapter(word,collection,book_name,chapter_id,p):
@app.route('/wuxiaworld/chapter', methods=[ "POST"])
def wuxiaworld_chapter():
    req = request.values.to_dict()
    n = NovelHelper()
    chapter = n.chapter(req['book_name'],req['chapter_id'])
    novel_name = n.novel(req['book_name'])['name']

    context_p={
        "wordbase_type": "wuxiaworld_chapter_p",
        "novel_name": novel_name,
        'chapter_id':chapter['id'],
        'chapter_name':chapter['chapter_name'],
        'text':{
            'en':chapter['text']['en'][int(req['p'])].replace(req['word'],'<span class="wordbase-highlight">' + req['word'] + '</span>'),
            'cn':chapter['text']['cn'][int(req['p'])]
        }
    }

    w = WordbaseHelper()
    w.init_source(context_p)
    w.inner_add(**req)


    return "true"

# def wuxiaworld_comment(word,collection,novel,chapter_id,page,comment_id,reply_id):
@app.route('/wuxiaworld/comment', methods=[ "POST"])
def wuxiaworld_comment():
    req = request.values.to_dict()
    headers = {'Host': 'www.wuxiaworld.com', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
               'Cache-Control': 'no-cache', 'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
               'Cookie': '__cfduid=dd6ac8f0b70978d38814d78075c566c4e1545389758; _ga=GA1.2.2117771054.1545389768; _gid=GA1.2.1909350696.1545389768; __asc=013d5e90167d068a3e75d976d99; __auc=013d5e90167d068a3e75d976d99; m2hb=enabled; __gads=ID=5bf229d51e5a7995:T=1545389790:S=ALNI_MaJcB-hx4nfDFZrWNmbJbxOsfEJtg; session_depth=2; _gat=1'}

    r = requests.get("https://www.wuxiaworld.com/api/comments/" + req['chapter_id'] + "/top?page=" + req['page'], headers=headers)
    res = r.text
    j = json.loads(res)
    data = j['items']
    comment={}

    for item in data:
        if item['id']==int(req['comment_id']):
            if req['reply_id']:
                for r in item['children']:
                    if r['id'] == int(req['reply_id']):
                        old = r['content']
                        r['content'] = old.replace(req['word'],'<span class="wordbase-highlight">' + req['word'] + '</span>')
                        # print(r['content'])
                        break
                    for r2 in r['children']:
                        if r2['id'] == int(req['reply_id']):
                            old = r2['content']
                            r2['content'] = old.replace(req['word'], '<span class="wordbase-highlight">' + req['word'] + '</span>')
                            # print(r2['content'])
                            break
                        for r3 in r2['children']:
                            if r3['id'] == int(req['reply_id']):
                                old = r3['content']
                                r3['content'] = old.replace(req['word'], '<span class="wordbase-highlight">' + req[
                                    'word'] + '</span>')
                                # print(r3['content'])
                                break
                            for r4 in r3['children']:
                                if r4['id'] == int(req['reply_id']):
                                    old = r4['content']
                                    r4['content'] = old.replace(req['word'], '<span class="wordbase-highlight">' + req[
                                        'word'] + '</span>')
                                    # print(r4['content'])
                                    break
            else:
                old = item['content']
                item['content'] = old.replace(req['word'], '<span class="wordbase-highlight">' + req['word'] + '</span>')
            comment=item
            break

    n = NovelHelper()
    chapter = n.chapter(req['novel'], req['chapter_id'])
    novel_name = n.novel(req['novel'])['name']
    comment['wordbase_type']='wuxiaworld_chapter_comment'
    comment['novel']=req['novel']
    comment['chapter_id']=req['chapter_id']
    comment['page']=req['page']
    comment['chapter_name']=chapter['chapter_name']
    comment['novel_name']=novel_name

    w = WordbaseHelper()
    w.init_source(comment)
    w.inner_add(**req)


    return 'true'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
