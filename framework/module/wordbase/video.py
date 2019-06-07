import os

import requests
from moviepy.video.io.VideoFileClip import VideoFileClip
from pysubs2 import SSAFile
from webvtt import WebVTT

from framework.module.wordbase.helper import WordbaseHelper

# clip = VideoFileClip("D:\BaiduYunDownload\Another\Another-01.mkv").subclip(30,50)
# clip.write_videofile("D:\BaiduYunDownload\Another\Another-01-sub.mkv", codec='libx264', verbose=False, audio=True)
from index import server_ip


class VideoWordbase:
    def add_word(self,word,collection,start,end,name,add_type,word_type,group,word_id='',wordset_id=''):
        clean_word = word.strip()
        puresave_filename = name.split('.')[0] + "~" + clean_word
        # row = {
        #     "videaname":puresave_filename,
        #     "wordbase_type":"video"
        # }
        # w = WordbaseHelper()
        # w.init_word(row,clean_word)
        # w.insert(row,collection)

        data = {
            'filename':puresave_filename,
            'wordbase_collection':collection,
            'word':word,
            'add_type':add_type,
            'word_type':word_type,
            'group':group,
            'word_id':word_id,
            'wordset_id':wordset_id,
        }


        work_dir="D:\BaiduYunDownload"
        file_path=""
        parent_path=""
        double_loop_flag=False
        for parent, dirnames, filenames in os.walk(work_dir, followlinks=True):
            for filename in filenames:
                if filename == name:
                    parent_path=parent
                    file_path = os.path.join(parent, filename)
                    double_loop_flag=True
                    break
            if double_loop_flag:
                break
        start_time = float(start)
        end_time = float(end)
        pure_filename = name.split('.')[0]

        subfile_path = os.path.join(parent_path, pure_filename+".srt")
        video_clip=VideoFileClip(file_path)
        clip = video_clip.subclip(start_time, end_time)
        target = "D:\BaiduYunDownload\\videos\\" +puresave_filename+".mp4"
        clip.write_videofile(target, codec='libx264',verbose=False, audio=True)
        video_clip.close()
        
        subtitle = SSAFile.load(subfile_path)
        text = '''
        1
        00:00:00,000 --> 00:00:00,000
        
        '''
        temp = SSAFile().from_string(text)
        for sub in subtitle:
            if sub.start >=start_time*1000 and sub.end <=end_time*1000:
                text = sub.text.replace(clean_word,'<c.video-heightlight>'+clean_word+'</c>')
                sub.text = text
                sub.shift(s=-start_time)
                temp.append(sub)
        sub_target = "D:\BaiduYunDownload\\videos\\" + puresave_filename
        temp.save(sub_target+'.srt')
        vtt = WebVTT().from_srt(sub_target+'.srt')
        vtt.save(sub_target+'.vtt')

        files = {
            "video": open(target, "rb"),
            "subtitle": open(sub_target+'.vtt', "rb")
        }
        # print(files)

        # r = requests.post('http://127.0.0.1:5000/video', data=data,files=files)
        r = requests.post('http://'+server_ip+'/video', data=data,files=files)
        # print(r.request)


        return "true"


