# Frame2x 倍帧工具


## requirements
1. ```linux```
2. ```ffmpeg``` and ```vulkan``` needed
3. [```RIFE-NCNN-VULKAN```](https://github.com/nihui/rife-ncnn-vulkan/releases/download/20210520/rife-ncnn-vulkan-20210520-ubuntu.zip) needed. Keep the dictionary as follow when downloading is done:
```
- rife-ncnn-vulkan-20210227-ubuntu
 -- rife
 -- rife-anime
 ...
 -- rife-v2.4
- utils
- workspace
...
- video-interpolation.py
```
---
## usage
1. basic usage
    ```powershell
    python video-interpolation.py [-h] [--src SRC_PATH [--dst DST_PATH] [--gpu GPU] [--once] [--filename FILENAME]
    ```
2. 命令行参数
    ```powershell
        -h, --help           show this help message and exit
        --src SRC_PATH       the video source filepath
        --dst DST_PATH       the video destination filepath
        --gpu GPU            gpu to use
        --once               whether to interpolate muti-files at one time
        --filename FILENAME  the very file to interpolate
    ```
3. examples
   ```powershell
   # using gpu 1 to double the frames of the samples.mp4
   python video-interpolation.py --src ./workspace/src/sample.mp4 --gpu 1

   # using gpu 0 to double the frames of all videos in ./worksapce/src/
   python video-interpolation.py --src ./workspace/src/ --gpu 0
   ```
---
- Thanks [video2x](https://github.com/k4yt3x/video2x) for inspiring the progress monitor part.
- if you by chance(which is most unlikely) notice this repo and by chance(which is also most unlikely) care about the bugs in these codes, you may not be recommanded to new a issue, because I will give up fixing it. XD