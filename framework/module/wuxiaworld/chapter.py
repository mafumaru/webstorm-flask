import requests
from bs4 import BeautifulSoup

from framework.core.crawlercore.url import Url
from framework.module.wuxiaworld.comment import WuxiaworldComment
from framework.module.wuxiaworld.txt import get_douluo_dalu_txt


class ChapterUrl(Url):
    def get_url(self, sortdict_key="default"):
        pass

# w = WuxiaworldComment('5271')
# w.debug=True
# c = w.get_lists()


def get_douluo_dalu():
    headers = {'Host': 'bluesilvertranslations.wordpress.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7', 'Cookie': '__utma=11735858.28966102.1545975344.1545975344.1545975344.1; __utmc=11735858; __utmz=11735858.1545975344.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __ATA_tuuid=ef859a8e-af20-48ea-a082-91573760ab36; __utmt=1; __utmb=11735858.4.10.1545975344'}
    r = requests.get('https://bluesilvertranslations.wordpress.com/chapter-list/',headers=headers)
    soup = BeautifulSoup(r.text)
    dirs_li = soup.find('div',class_='entry-content').find_all('li')[:200]
    dir_url=[]
    for li in dirs_li:
        dir_url.append(li.a['href'])
    return dir_url

def get_douluo_dalu_chapters():
    url_list = get_douluo_dalu()
    chapters=[]
    chapter_names = []
    headers = {'Host': 'bluesilvertranslations.wordpress.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7', 'Cookie': '__utma=11735858.28966102.1545975344.1545975344.1545975344.1; __utmc=11735858; __utmz=11735858.1545975344.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __ATA_tuuid=ef859a8e-af20-48ea-a082-91573760ab36; __utmt=1; __utmb=11735858.4.10.1545975344'}
    txt = get_douluo_dalu_txt()[1]
    for index in range(len(url_list)):
        r = requests.get(url_list[index], headers=headers)
        soup = BeautifulSoup(r.text)
        google_doc_url = soup.find('div', class_='entry-content').find('a')['href']
        google_doc_headers = {'Host': 'docs.google.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                              'Referer': url_list[index],
                              'Accept-Encoding': 'gzip, deflate, br',
                              'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}
        try:
            r = requests.get(google_doc_url, headers=google_doc_headers)
            soup = BeautifulSoup(r.text)
        except:
            continue
        doc_content_tags = soup.find_all('p')
        doc_content_prev=[]
        doc_content=[]
        chapter_num=''
        chapter_name=''
        # index = len(chapters)
        for i in range(len(doc_content_tags)):
            text =doc_content_tags[i].text.strip()
            if text:
                if 'Part' in text and len(text)<10:
                    pass
                else:
                    doc_content_prev.append(text)
        # print('')
        for i in range(len(doc_content_prev)):
            if 'Chapter' in doc_content_prev[i] :
                if len(doc_content_prev[i+1]) <50:
                    doc_content = doc_content_prev[2:]
                    chapter_name = doc_content_prev[0] + ' ' + doc_content_prev[1]
                else:
                    doc_content = doc_content_prev[1:]
                    chapter_name = doc_content_prev[0]
                break
        print(str(index) +' : '+ chapter_name+' | ' +txt[index]['chapter_name'])
        final_chapter = {
            'id': index,
            'book_name': {
                'en': '',
                'cn': ''
            },
            'chapter_name': {
                'en': chapter_name,
                'cn': txt[index]['chapter_name']
            },
            # 'comment':reply,
            'text': {
                'en': doc_content,
                'cn': txt[index]['text']
            }
            # 'text':text
        }
        final_chapter_name = {
            'en': chapter_name,
            'cn': txt[index]['chapter_name'],
            'chapter_id': index
        }
        chapters.append(final_chapter)
        chapter_names.append(final_chapter_name)
        # google_doc_url_list.append(google_doc_url)
        # break

    return (chapter_names,chapters)
# get_douluo_dalu_chapters()
# print('')