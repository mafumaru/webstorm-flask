import os

from moviepy.video.io.VideoFileClip import VideoFileClip


def mkv_to_mp4(name):
    work_dir = "D:\BaiduYunDownload"
    file_path = ""
    parent_path = ""
    double_loop_flag = False
    for parent, dirnames, filenames in os.walk(work_dir, followlinks=True):
        for filename in filenames:
            if filename == name:
                parent_path = parent
                file_path = os.path.join(parent, filename)
                double_loop_flag = True
                break
        if double_loop_flag:
            break
    pure_filename = name.split('.')[0]

    video_clip = VideoFileClip(file_path)
    target = parent_path + pure_filename + ".mp4"
    video_clip.write_videofile(target, codec='libx264', verbose=False, audio=True)
    video_clip.close()

mkv_to_mp4('GirlsLastTour-01.mkv')