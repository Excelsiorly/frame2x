# Frame2x 倍帧工具

## requirements
1. ```linux```
2. 需要 ```ffmpeg```、```vulkan```
3. 需要```RIFE-NCNN-VULKAN```模型,[下载点这里](https://github.com/nihui/rife-ncnn-vulkan/releases/download/20210520/rife-ncnn-vulkan-20210520-ubuntu.zip), 下载完成后解压到根目录，保持整个目录结构如下：
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
1. 基础使用
    ```powershell
    python video-interpolation.py [-h] [--src SRC_PATH [--dst DST_PATH] [--gpu GPU] [--once] [--filename FILENAME]
    ```
2. 命令行参数
    ```powershell
        -h, --help           帮助
        --src SRC_PATH       原视频所在目录
        --dst DST_PATH       输出视频所在目录
        --gpu GPU            所使用gpu的id
        --once               一次处理原视频所在目录(SRC_PATH)下的所有视频 
        --filename FILENAME  若不使用--once，则需要指定原视频的文件名
    ```
3. 示例用法
   ```powershell
   # 使用gpu 1 处理一个视频 sample.mp4
   python video-interpolation.py --src ./workspace/src/sample.mp4 --gpu 1

   # 使用gpu 0 处理 ./workspace/src/ 目录下所有的视频文件
   python video-interpolation.py --src ./workspace/src/ --gpu 0
   ```
---
- 代码参考 [video2x](https://github.com/k4yt3x/video2x)，感谢关于进度条的启发
- 如果大概可能、或许有人看到本仓库，甚至大概可能、或许有人发现了bug，最好放弃发issues，因为我大概不会想改自己的垃圾代码 XD