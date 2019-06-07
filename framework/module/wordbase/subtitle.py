import os

import copy
from pysubs2 import SSAFile, SSAEvent, make_time

subtitle_ass:SSAFile =None

# work_dir = 'D:\BaiduYunDownload\Hyouka\Hyouka-01'
# work_dir = 'D:\BaiduYunDownload\Oreimo\Oreimo-02'
# work_dir = 'D:\BaiduYunDownload\GirlsLastTour\GirlsLastTour-01'
# work_dir = 'D:\BaiduYunDownload\SAOII\mkv\SAOII-08'
work_dir = 'D:\BaiduYunDownload\Children\Children-02'

file_list=os.listdir(work_dir)
i=1
for filename in file_list:
    file_path = os.path.join(work_dir, filename)
    if os.path.isfile(file_path):
        i+=1
        sub = SSAFile.load(file_path)
        if subtitle_ass:
            if filename == 'c.ass' or filename == 'm.ass':
                sub.shift(s=1)
            subtitle_ass += sub
        else:
            if filename == 'c.ass' or filename == 'm.ass':
                sub.shift(s=1)
            subtitle_ass = sub
# for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
#     for filename in filenames:
#         file_path = os.path.join(parent, filename)
#         sub = SSAFile.load(file_path)
#         if subtitle_ass:
#             subtitle_ass += sub
#         else:
#             subtitle_ass = sub

temp = copy.deepcopy(subtitle_ass)
for sub in temp:
    # text = sub.text
    if sub.text == '' or (sub.text.find('字幕组') != -1) or (sub.text.find('24小') != -1) or (sub.text.find('字幕組') != -1) or (sub.text.find('日听') != -1)or (sub.text.find('双语字幕') != -1) or (sub.text.find('轴：') != -1) or (
        sub.text.find('下載24小時') != -1) or (sub.text.find('翻译：') != -1)or (sub.text.find('翻譯：') != -1) or (sub.text.find('下载24小时') != -1)or (sub.text.find('.com') != -1):
        subtitle_ass.remove(sub)
subtitle_ass.sort()


subtitle_ass.save(work_dir+'.srt')
subtitle_ass = SSAFile.load(work_dir+'.srt')
for sub in list(subtitle_ass):
    if sub.text == '' or (sub.text.find('字幕组') != -1) or (sub.text.find('24小') != -1) or (sub.text.find('字幕組') != -1)or (sub.text.find('日听') != -1)or (sub.text.find('双语字幕') != -1) or (sub.text.find('轴：') != -1) or (
        sub.text.find('下載24小時') != -1) or (sub.text.find('翻译：') != -1)or (sub.text.find('翻譯：') != -1)  or (sub.text.find('下载24小时') != -1)or (sub.text.find('.com') != -1):
        subtitle_ass.remove(sub)
temp = copy.deepcopy(subtitle_ass)
temp.clear()
for sub in list(subtitle_ass):
    f=True
    for sub2 in list(temp):
        if sub.text == sub2.text:
            f=False
            break
    if f:
        temp.append(sub)

flag_text = "<<"+str(i)+">>组字幕"
temp.insert(0,SSAEvent(start=make_time(s=0), end=make_time(s=0), text=flag_text))

temp.save(work_dir+'.srt')
# subtitle_ass = SSAFile.load(work_dir+'.srt')
# for sub in list(subtitle_ass):
#     if sub.text == '' or (sub.text.find('字幕组') != -1) or (sub.text.find('24小') != -1) or (sub.text.find('字幕組') != -1) or (
#         sub.text.find('下載24小時') != -1) or (sub.text.find('翻译：') != -1) or (sub.text.find('下载24小时') != -1):
#         subtitle_ass.remove(sub)
# text = sub.text
# subtitle_ass = SSAFile.load(work_dir+'\[AngelSub][Another][01][BD][BIG5][X264].ass')
# text = subtitle_ass[306]
# text = subtitle_ass[28]
# bool = text.text.find('下載24小時')
# b = (text.text.find('下载24小时') != -1)
