import os

import re

import requests
from bs4 import BeautifulSoup


class Txt:
    pass

def get_txt():
    note = ['582、583二合一', '690不存在', '1377不存在']

    work_dir = "D:\BaiduYunDownload"
    # work_dir = "/root/webstorm/static/"
    filename = 'issth.txt'
    file_path = os.path.join(work_dir, filename)
    f = open(file_path, 'r')
    txt = f.read()
    # book_pattern = re.compile('第.章.+\n\n?')
    # books = re.split(book_pattern, txt,re.S)
    books = txt.split('\n\n')
    chapters = []
    book_names = []
    for item in books:
        if len(item) > 50:
            chapter_ary = item.strip().split('\n', 1)
            p = chapter_ary[1].split('\n')
            chapter = {
                'chapter_name': chapter_ary[0],
                'text': p
            }
            chapters.append(chapter)
        else:
            if item and item.find('第') != -1:
                book = item.strip()
                book_names.append(book)
    # a_find = chapters[1360:1400]
    # find = chapters[1000:1010]
    last = chapters[-1]

    # r = requests.get('https://www.dingdiann.com/ddk815/1339788.html')
    # soup = BeautifulSoup(r.text)
    # content = soup.find('div',class_='content')
    # txt = content.text

    # print('')
    return (book_names,chapters)

def get_douluo_dalu_txt():
    note = ['582、583二合一', '690不存在', '1377不存在']

    work_dir = "D:\BaiduYunDownload"
    # work_dir = "/root/webstorm/static/"
    filename = 'douluodalu.txt'
    file_path = os.path.join(work_dir, filename)
    f = open(file_path, 'r')
    txt = f.read()
    # book_pattern = re.compile('第.章.+\n\n?')
    # books = re.split(book_pattern, txt,re.S)
    books = txt.split('\n\n')[0:400]
    last = books[-2:]
    chapters = []
    book_names = []
    combine_flag=False
    for i in range(len(books)):
        if len(books[i])<70:
            p = books[i + 1].split('\n')
            chapter = {
                'chapter_name': books[i],
                'text': p
            }
            chapters.append(chapter)
            combine_flag=True
        else:
            if combine_flag:
                combine_flag=False
            else:
                p = books[i].split('\n')
                chapter = {
                    'chapter_name': '',
                    'text': books[i]
                }
                chapters.append(chapter)
        # if len(item) > 50:
        #     chapter_ary = item.strip().split('\n', 1)
        #     p = chapter_ary[1].split('\n')
        #     chapter = {
        #         'chapter_name': chapter_ary[0],
        #         'text': p
        #     }
        #     chapters.append(chapter)
        # else:
        #     if item and item.find('第') != -1:
        #         book = item.strip()
        #         book_names.append(book)
    # a_find = chapters[1360:1400]
    # find = chapters[1000:1010]

    # r = requests.get('https://www.dingdiann.com/ddk815/1339788.html')
    # soup = BeautifulSoup(r.text)
    # content = soup.find('div',class_='content')
    # txt = content.text

    # print('')
    return (book_names,chapters)
# txt = get_douluo_dalu_txt()
# print('')