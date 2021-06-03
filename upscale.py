'''
Author: your name
Date: 2021-06-03 03:50:38
LastEditTime: 2021-06-03 03:50:39
LastEditors: your name
Description: In User Settings Edit
FilePath: /waifu/upscale.py
'''
'''
Author: jojo
Date: 2021-04-22 17:36:32
LastEditors: jojo
LastEditTime: 2021-04-23 03:08:35
FilePath: /waifu/upscale.py
放大处理
'''
import os
from const import WNV_PATH

src_dir = './workspace/pj-01/src/test.jpg'
dst_dir = './workspace/pj-01/out/test.jpg'


upscale_command = f'{WNV_PATH} -i {src_dir} -o {dst_dir} -n 1 -s 2 -j 4:4:4'
os.system(upscale_command)