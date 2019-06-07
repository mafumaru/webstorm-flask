import re
import requests
import time
from bs4 import BeautifulSoup, Tag

from framework.module.wuxiaworld.comment import WuxiaworldComment
from framework.module.wuxiaworld.txt import get_txt

def get_issth():
    books_list = [
        {'book_num': 1, 'name': 'Book 1: Patriarch Reliance', 'start': 1, 'end': 95},
        {'book_num': 2, 'name': 'Book 2: Cutting Into The Southern Domain', 'start': 96, 'end': 204},
        {'book_num': 3, 'name': 'Book 3: The Honor Of Violet Fate', 'start': 205, 'end': 313},
        {'book_num': 4, 'name': 'Book 4: Five Color Paragon', 'start': 314, 'end': 628},
        {'book_num': 5, 'name': 'Book 5: Nirvanic Rebirth. Blood Everywhere!', 'start': 629, 'end': 800},
        {'book_num': 6, 'name': 'Book 6: Fame That Rocks the Ninth Mountain; the Path to True Immortality',
         'start': 801, 'end': 1004},
        {'book_num': 7, 'name': 'Book 7: Immortal Ancient Builds a Bridge Leaving the Ninth Mountain!', 'start': 1005,
         'end': 1211},
        {'book_num': 8, 'name': 'Book 8: My Mountain and Sea Realm', 'start': 1212, 'end': 1409},
        {'book_num': 9, 'name': 'Book 9: The Demon Sovereign Returns; the Peak of the Vast Expanse!', 'start': 1410,
         'end': 1557},
        {'book_num': 10, 'name': 'Book 10: I Watch Blue Seas Become Lush Fields', 'start': 1558, 'end': 1614}
    ]

    headers = {'Host': 'www.wuxiaworld.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}

    chapters = []
    dirs = []
    txt = get_txt()
    txt_bn = txt[0]
    txt_chpts = txt[1]
    for book in books_list:
        for chapter_index in range(book['start'], book['end'] + 1):
            if chapter_index == 582:
                url = 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-' + str(
                    book['book_num']) + '-chapter-' + str(chapter_index) + '-0583'

            elif chapter_index == 583 or chapter_index == 690 or chapter_index == 1377:
                continue
            else:
                url = 'https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-' + str(
                    book['book_num']) + '-chapter-' + str(chapter_index)
            print(url)
            r = requests.get(url, headers=headers)
            # r = requests.get('https://www.wuxiaworld.com/novel/i-shall-seal-the-heavens/issth-book-4-chapter-597',headers=headers)
            r.encoding = 'utf-8'
            html = r.text
            soup = BeautifulSoup(html)
            p = soup.find('div', class_='fr-view').find_all('p')
            if p[0].text.find('Previous') != -1:
                del p[0]
            if not p[0].text:
                del p[0]
            en=[]
            for item in p[1:]:
                en.append(item.text)
            chapter = {
                'chapter_name': p[0].text,
                'text': en
            }
            pattern = re.compile('{"id":(\d+?),"')
            comment = pattern.search(html).group(1)

            final_chapter_name = {
                'en': chapter['chapter_name'],
                'cn': txt_chpts[len(chapters)]['chapter_name'],
                'chapter_id': comment
            }

            # text=[]
            # for index, item in enumerate(chapter['text']):
            #     txt_text = txt_chpts[len(chapters)]['text']
            #     if index < len(txt_text):
            #         txt_p = txt_text[index]
            #     else:
            #         txt_p = ''
            #     final_text = {
            #         'id': index,
            #         'en': item.text,
            #         'cn': txt_p
            #     }
            #     text.append(final_text)

            # w = WuxiaworldComment(comment)
            # w.get_lists()
            # reply = w.datacore.listdata

            final_chapter = {
                'id': comment,
                'book_name': {
                    'en': book['name'],
                    'cn': txt_bn[book['book_num'] - 1]
                },
                'chapter_name': {
                    'en': chapter['chapter_name'],
                    'cn': txt_chpts[len(chapters)]['chapter_name']
                },
                # 'comment':reply,
                'text': {
                    'en': chapter['text'],
                    'cn': txt_chpts[len(chapters)]['text']
                }
                # 'text':text
            }
            chapters.append(final_chapter)
            dirs.append(final_chapter_name)

            # time.sleep(1)
    return (dirs,chapters)

def get_btth():
    headers = {'Host': 'www.wuxiaworld.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://www.wuxiaworld.com/novel/battle-through-the-heavens',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7'}

    chapters = []
    dirs = []
    txt = get_txt()
    txt_chpts = txt[1]
    for i in range(1,1649):
        url = 'https://www.wuxiaworld.com/novel/battle-through-the-heavens/btth-chapter-' + str(i)
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        html = r.text
        soup = BeautifulSoup(html)
        p = soup.find('div', class_='fr-view').find_all('p')
        if p[0].text.find('Previous') != -1:
            del p[0]
        if not p[0].text:
            del p[0]
        en = []
        for item in p[1:]:
            en.append(item.text)
        chapter = {
            'chapter_name': p[0].text,
            'text': en
        }
        pattern = re.compile('{"id":(\d+?),"')
        comment = pattern.search(html).group(1)

        final_chapter_name = {
            'en': chapter['chapter_name'],
            'cn': txt_chpts[len(chapters)]['chapter_name'],
            'chapter_id': comment
        }

        final_chapter = {
            'id': comment,
            'chapter_name': {
                'en': chapter['chapter_name'],
                'cn': txt_chpts[len(chapters)]['chapter_name']
            },
            'text': {
                'en': chapter['text'],
                'cn': txt_chpts[len(chapters)]['text']
            }
        }
        chapters.append(final_chapter)
        dirs.append(final_chapter_name)

    return (dirs, chapters)