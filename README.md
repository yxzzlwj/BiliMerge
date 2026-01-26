# BiliMerge
>一键批量转化bilibili缓存视频为mp4的小工具

## 安装
### A. 在android上使用
- 你需要安装[Termux](https://github.com/termux/termux-app),推荐通过[F-Droid](https://f-droid.org/)下载
1. 安装Termux并换源,这里不再赘述
2. 安装运行环境:
```
apt update
apt install python3
apt install ffmpeg
```
3. 授权Termux访问手机存储并为其加锁(防止被杀后台)
```
termux-setup-storage
termux-wake-lock
```
4. 运行命令克隆仓库
```
cd &&cd storage/shared
git clone https://github.com/yxzzlwj/BiliMerge
```
5. 把你获取到的缓存文件(通常位于`内部共享存储/Android/data/tv.danmaku.bili/download`下)复制到`内部共享存储/BiliMerge/from`下
6. 运行命令
```
cd &&cd storage/shared/BiliMerge
python3 main.py
```
7. 你应该可以看到"处理中的目录...",这时你应当保持Termux位于前台并保持手机亮屏,防止任务意外终止
8. 当你看到"结束啦!恭喜!!!"的字样时,代表任务成功

#### 异常处理
如果提示"输出目录"out"已存在,请手动删除或转移!"时,运行`rm -rf out`,然后回到第6步

---
## 鸣谢
### ffmpeg
[ffmpeg官网](https://ffmpeg.org/)
>A complete, cross-platform solution to record, convert and stream audio and video. 

### python
[python官网](https://www.python.org/)
>Python is a programming language that lets you work quickly and integrate systems more effectively.

 ### Termux
[Termux项目地址](https://github.com/termux)
 >Termux - a terminal emulator application for Android OS extendible by variety of packages. 
