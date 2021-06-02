'''
Author: jojo
Date: 2021-04-23 03:07:36
LastEditors: Please set LastEditors
LastEditTime: 2021-06-02 13:13:17
FilePath: /waifu/interpolation.py
倍帧
'''

import os
import json
from const import RIFE_PATH
import shutil
import threading
from tqdm import tqdm
import time

import sys
from utils import global_var_manager as gv
# src_dir = './workspace/test/src'
# dst_dir = './workspace/test/out'

# filename = 'test.mp4'


def interpolation(src_dir,dst_dir,filename,gpu='0'):
    """倍帧

    Args:
        src_dir (str): 源视频文件所在目录
        dst_dir (str): 输出目录
        filename (str): 文件名，带后缀
        gpu(str): 使用的gpu，默认为1
    """
    gv.set_value(name='interpolated',value=False)
    file_realname = filename.split('.')[0]
    src_file_path = os.path.join(src_dir,filename)
    dst_file_path = os.path.join(dst_dir,filename)

    input_frame_dir = os.path.join(src_dir,file_realname + '_input_frames')
    output_frame_dir = os.path.join(dst_dir,file_realname + '_output_frames')

    if not os.path.exists(input_frame_dir):
        os.mkdir(input_frame_dir)

    if not os.path.exists(output_frame_dir):
        os.mkdir(output_frame_dir)
    
    print("extracting audio...")
    audio_path = os.path.join(src_dir,file_realname + '.m4a')
    extract_audio(src_file_path,audio_path)
    print("extracted!")

    print("decoding frames...")
    decode_frames(src_file_path,input_frame_dir)
    print("decoded!")

    # use thread to monitor the process
    threads = []
    threads.append(threading.Thread(target=interpolate,args=(input_frame_dir,output_frame_dir,gpu)))
    threads.append(threading.Thread(target=process_monitor,args=(input_frame_dir,output_frame_dir)))
    print("interpolating....")
    # interpolate(input_frame_dir,output_frame_dir,gpu)
    # multi-thread processing
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
        
    
    print("interporated!")

    print("concating audio to new video...")
    res_dict = read_video_info(src_dir,filename)
    cont_audio(output_frame_dir,audio_path,dst_file_path,res_dict)
    print("concated!")

    print(f"{src_file_path} has been interpolated to {dst_file_path}")
    os.remove(audio_path)
    shutil.rmtree(input_frame_dir)
    shutil.rmtree(output_frame_dir)


def extract_audio(src_file_path,audio_path):
    # extract audio
    ext_aud_com = f'ffmpeg -y -i {src_file_path} -vn -acodec copy {audio_path}'
    os.system(ext_aud_com)

def decode_frames(src_file_path,input_frame_dir):
    # decode all frames
    # dec_fra_com = f'ffmpeg -i {src_file_path} {input_frame_dir}/frame_%08d.png'
    dec_fra_com = f'ffmpeg -y -hwaccel cuvid -i {src_file_path} {input_frame_dir}/frame_%08d.png'
    os.system(dec_fra_com)

# interpolate 2x frame count
def interpolate(input_frame_dir,output_frame_dir,gpu):
    inter_com = f'{RIFE_PATH} -i {input_frame_dir} -o {output_frame_dir} -j 90:90:90 -g {gpu} -m rife-v2.4'
    os.system(inter_com)
    gv.set_value('interpolated',True)

# interpolated frames in double frame with audio
def cont_audio(output_frame_dir,audio_path,dst_file_path,res_dict):
    fps = get_fps(res_dict)
    pix_fmt = res_dict['streams'][0]['pix_fmt']
    double_fps = fps*2
    
    # # limit the fps
    # if double_fps>60:
    #     double_fps = 60

    # how to determine the crf value: https://zhuanlan.zhihu.com/p/250590703
    int_with_aud_com = f'ffmpeg -y -framerate {double_fps} -i {output_frame_dir}/%08d.png -i {audio_path} -c:a copy -crf 23 -c:v libx264 -pix_fmt {pix_fmt} {dst_file_path}'
    os.system(int_with_aud_com)

def read_video_info(src_dir,filename):
    res_json = os.path.join(src_dir,filename + ".json")
    cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams {os.path.join(src_dir,filename)} >> {res_json}'
    # command = 'ffprobe -v error -select_streams v -show_entries stream=nb_frames -of json {os.path.join(src_dir,filename)} >> {res_json}'
    os.system(cmd)
    res_dict  = {}
    with open(res_json,'r') as file:
        res_dict = json.load(file)  
    
    os.remove(res_json)
    return res_dict

def get_fps(res_dict):
    content = res_dict['streams'][0]['avg_frame_rate']
    up,down = content.split('/')
    # fps = int(up)/int(down)
    # return math.ceil(fps)
    fps = float(up) / float(down)
    return fps

def process_monitor(input_frame_dir,output_frame_dir):
    """monitor the process

    Args:
        input_frame_dir (str): the original video frames path
        output_frame_dir (str): the target video frames path
    """
    total_frame_amount = len(os.listdir(input_frame_dir))
    target_frame_amount = 2*total_frame_amount
    current_frame_amount = 0
    previous_frame_amount = 0
    time.sleep(1)
    with tqdm(total=target_frame_amount,desc ='Interpolating process') as progress_bar:
        # get the current processed frame amount
        while not current_frame_amount==target_frame_amount and gv.get_value('interpolated') == False:
            current_frame_amount = len(os.listdir(output_frame_dir))
            delta = current_frame_amount - previous_frame_amount
            previous_frame_amount = current_frame_amount
            progress_bar.update(delta)
            time.sleep(1)
            
    print("interpolation process done!")
            

if __name__=='__main__':
    src_dir = './workspace/src/p1/'
    filename = '02.mp4'
    dst_dir = './workspace/dst/'
    # filename = 'test.mp4'
    # interpolation(src_dir,dst_dir,filename)
    extract_audio(os.path.join(src_dir,filename),os.path.join(dst_dir,'02.m4a'))
    res_dict = read_video_info(src_dir,filename)
    cont_audio(output_frame_dir=os.path.join(dst_dir,'02_output_frames'),audio_path=os.path.join(dst_dir,'02.m4a'),
               dst_file_path=os.path.join(dst_dir,'02.mp4'),res_dict=res_dict)