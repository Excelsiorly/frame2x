'''
Author: jojo
Date: 2021-04-23 11:24:18
LastEditors: Please set LastEditors
LastEditTime: 2021-06-02 13:21:53
FilePath: /waifu/video-interpolation.py
'''

import os
import argparse
import time
import datetime
from pathlib import Path

from interpolation import interpolation

def muti_interp(src,dst,gpu):
    file_list = os.listdir(src)
    print("videos to be interpolated are:")
    temp_list = []
    for file in file_list:
        temp_file = Path(os.path.join(src,file))
        if not temp_file.is_dir() and not file.split('.')[-1]=='m4a':
            temp_list.append(file)
    file_list = temp_list
    for file in file_list:
        print(file)
    i = 0
    for file in file_list:
        # src_path = os.path.join(src,file)
        # dst_path = os.path.join(dst,file.split('.')[0]+'.mp4')
        print(f"interpolating video {file}...")
        interpolation(src,dst,file,gpu)
        print(f"video {file} interpolated!")
        i +=1
        print(f"remains {len(file_list)-i} to go!")
        
def single_interp(src,dst,file,gpu):
    print(f"interpolating video {file}...")
    interpolation(src,dst,file,gpu)
    print(f"video {file} interpolated!")
        
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='args to use.')
    parser.add_argument('--src',dest='src_path' ,default='./workspace/src',type=str,
                        help='the video source filepath')
    parser.add_argument('--dst', dest='dst_path', default='./workspace/dst',type=str,
                        help='the video destination filepath')
    parser.add_argument('--gpu', dest='gpu', default='0',type=str,
                        help='gpu to use')
    parser.add_argument('--once', dest='once', action="store_true",
                        help='whether to interpolate muti-files at one time')
    parser.add_argument('--filename', dest='filename', default=None,type=str,
                        help='the very file to interpolate')

    args = parser.parse_args()
    src_path = args.src_path
    dst_path = args.dst_path
    print("current pid is {}".format(os.getpid()))
    start_time = time.time()
    if args.once:
        muti_interp(src_path,dst_path,args.gpu)
    else:
        print(f"interpolating {args.filename}")
        single_interp(src_path,dst_path,args.filename,args.gpu)
        print(f"{src_path}/{args.filename} has been interpolated to {dst_path}")
    end_time = time.time()
    cost_time = datetime.timedelta(seconds=end_time-start_time)
    print(f"cost of the time is {cost_time}")