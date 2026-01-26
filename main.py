####设置####
FileFrom = "from"
####函数####
def errormp4out(where,getbug):
    with open('output.mp4', 'w', encoding='utf-8') as file:
        file.write('error')
    with open('error.log', 'a', encoding='utf-8') as file:
        willwritebug = "在处理" + where + "时出错,原因:"
        willwrite = "\n" + willwritebug
        file.write(willwrite)
        print(willwritebug + "请在错误报告中查看\n")
        file.write(getbug)
        file.write("----===----")
def autoname(filename):
    filename = str(filename)
    illegal_chars = r'[\\/:\*\?"<>\|\s]'
    sanitized = re.sub(illegal_chars, '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized)
    sanitized = sanitized.strip('_')
    return sanitized
def ReadJson(where):
    which = os.path.join(where,"entry.json")
    with open(which, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
def GetName(TwoWhere):
    try :
        LoadJson = ReadJson(TwoWhere)
    except:
        with open('error.log', 'a', encoding='utf-8') as file:
            willwritebug = "在处理" + TwoWhere + "时出错,原因:\"entry.json\"获取失败\n"
            file.write(willwritebug)
        number = "error"
        name = "error"
        return [name,number]
    try :
        if "ep" in LoadJson and LoadJson["ep"] is not None :
            name = os.path.join("out",autoname(LoadJson["title"]) + "_" + autoname(LoadJson["ep"]["index"]) + "_" + autoname(LoadJson["ep"]["index_title"]) + ".mp4")
        else:
            name = os.path.join("out",autoname(LoadJson["title"]) + "_" + autoname(LoadJson["page_data"]["download_subtitle"]) + ".mp4")
    except:
        name = os.path.join("out",autoname(TwoWhere) + ".mp4")
    try :
        number = str(LoadJson["type_tag"])
    except:
        with open('error.log', 'a', encoding='utf-8') as file:
            willwritebug = "在处理" + TwoWhere + "时出错,原因:数字目录获取失败\n"
            file.write(willwritebug)
        number = "error"
    return [name,number]
def LoadDir(where):
    with os.scandir(where) as entries:
        folders = [entry.name for entry in entries if entry.is_dir()]
    return folders
def ffmpeg(where,number):
    if number == "error":
        print("ffmpeg error")
        return "error"
    where = os.path.join(where,number)
    video = os.path.join(where,"video.m4s")
    audio = os.path.join(where,"audio.m4s")
    if os.path.isfile(video):
        if os.path.isfile(audio):
            result = subprocess.run(['ffmpeg', '-i', video, '-i', audio, '-c', 'copy', "output.mp4"], capture_output=True, text=True)
            if result.returncode != 0:
                errormp4out(where,result.stderr)
        else:
            result = subprocess.run(['ffmpeg', '-i', video, '-c', 'copy', "output.mp4"], capture_output=True, text=True)
            if result.returncode != 0:
                errormp4out(where,result.stderr)
            with open('error.log', 'a', encoding='utf-8') as file:
                willwritebug = "在处理" + where + "时出错,原因:没有声音\n"
                file.write(willwritebug)
                print(willwritebug)
    else:
        if os.path.isfile(audio):
            result = subprocess.run(['ffmpeg', '-i', audio, '-c', 'copy', "output.mp4"], capture_output=True, text=True)
            if result.returncode != 0:
                errormp4out(where,result.stderr)
            with open('error.log', 'a', encoding='utf-8') as file:
                willwritebug = "在处理" + where + "时出错,原因:没有视频\n"
                file.write(willwritebug)
                print(willwritebug)
        else:
            with open('output.mp4', 'w', encoding='utf-8') as file:
                file.write('error')
            with open('error.log', 'a', encoding='utf-8') as file:
                willwritebug = "在处理" + where + "时出错,原因:没有声音也没有视频\n"
                file.write(willwritebug)
                print(willwritebug)
####初始化####
import os
import sys
import shutil
import subprocess
import re
import json
try:
    OneDir = LoadDir(FileFrom)
except :
    print("读取目录\"",FileFrom,"\"失败,请检查权限!")
    sys.exit(1)
try:
    os.mkdir("out")
except FileExistsError :
    print("输出目录\"out\"已存在,请手动删除或转移!")
    sys.exit(1)
except :
    print("输出目录\"out\"创建失败,请检查权限!")
    sys.exit(1)
print (OneDir)
NumOneDir = len(OneDir)
try:
    with open('error.log', 'w', encoding='utf-8') as file:
        file.write('start\n')
except :
    print("日志\"error.log\"创建失败,请检查权限或者手动创建(不推荐手动创建)!")
    sys.exit(1)
####主循环####
for i in range(NumOneDir):
    print(f"当前循环: {i}")
    OneWhere = os.path.join(FileFrom,OneDir[i])
    TwoDir = (LoadDir(OneWhere))
    print("二级目录共有:",TwoDir)
    NumTwoDir = len(TwoDir)
    for l in range(NumTwoDir):
        TwoWhere = os.path.join(OneWhere,TwoDir[l])
        print("处理中的目录" + TwoWhere)
        now = GetName(TwoWhere)
        ffmpeg(TwoWhere,now[1])
        try :
            shutil.move("output.mp4", now[0])
            print("输出:",now[0])
        except:
            print("无法找到来自ffmpeg的\"output.mp4\"")
            with open('error.log', 'a', encoding='utf-8') as file:
                willwritebug = "在处理" + TwoWhere + "时出错,原因:无法找到来自ffmpeg的\"output.mp4\""
                file.write(willwritebug)
print("以下为错误报告,如果只有一个‘start’那就恭喜了")
try:
    with open('error.log', 'r') as f:
        print(f.read())
except:
    print("无法读取错误报告日志")
print("错误报告结束")
print("结束啦!恭喜!!!")
#6.0