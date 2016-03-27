# maplemuxtool v1.2
# 修改了用法，更符合cmd常见用法
# 修复了路径名不能包含中文的bug
# 用法：
# python 脚本路径 -v 视频路径 -a 音频路径 -n [num]开始数字~[num]结束数字 -t 音轨号(第一条音轨一般为0)
# 仅-v 必填 -a 默认同-v -n默认1~1 -t默认0
# 1——————————————————————————————————————
# python E:\python\automux\automux.py -v E:\python\automux\[num].mp4 -a E:\python\automux\02.mp4 -n 2~4
# 上面脚本的意思是把02.mp4的第一条音轨分别和02.mp4、03.mp4、04.mp4的第一条视频轨合并
# (数字2、4代表[num]从02取到04，请注意0是程序自动加的，请不要手动添加)
# 
# 2——————————————————————————————————————
# python E:\python\automux\automux.py -v E:\python\automux\[num].mp4 -a E:\python\automux\逸站[num]要完.aac -n 1~12 -t 0
# 逸站01要完.aac的第一条音轨和01.mp4合并为01_mmux.mp4
# 逸站02要完.aac的第一条音轨和02.mp4合并为02_mmux.mp4
# ······
# 逸站12要完.aac的第一条音轨和12.mp4合并为12_mmux.mp4
#
# 3——————————————————————————————————————
# 当只有一个视频需要封装时:
# python E:\python\automux\automux.py -v E:\python\automux\逸站12要完.mp4 -a E:\python\automux\逸站12要完.aac
# 音频请自行转码，不符合规范的音频只会有一个不明显的报错。此时生成的视频文件一般只有几十kb
import os
import subprocess
import sys
import getopt
def mainmux(vedioinput,audioinput,vedioselect = r"0",audioselect = r"0",vediofilter = r"copy",audiofilter = r"copy"):
    #组合输出路径
    p = os.path.split(vedioinput)
    pe = os.path.splitext(p[1])
    filepath = p[0]
    filename = pe[0]
    fileextraname = pe[1]
    output = os.path.join(filepath,filename+"_mmux"+fileextraname)
    command = r'ffmpeg -i '+'"'+vedioinput+'"'+' -i '+'"'+audioinput+'"'+' -c:v '+vediofilter+' -map 0:v:'+vedioselect+' -c:a '+audiofilter+' -map 1:a:'+audioselect+' -y '+'"'+output+'"'
    print(command)
    a = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
    b = a.communicate(b'y')
    return(b[0].decode("utf-8"))
    #return command
def autofilename(filename,firstnum=1,lastnum=1):
    filenames=[]
    for number in range(int(firstnum),int(lastnum)+1):
        if number < 10:
            number='0'+str(number)
        filename_edited=filename.replace('[num]',str(number))
        filenames.append(filename_edited)
        # print(number)
    return filenames
def automux(vediofile,audiofile,firstnum=1,lastnum=1,audiotrack=0,audiofilter = ""):
    # vediofile = r"E:\python\automux\[num].mp4"
    # audiofile = r"E:\python\automux\[num]_AAC.aac"
    audiotrack = str(audiotrack)
    vediofilenames = autofilename(vediofile,firstnum,lastnum)
    audiofilenames = autofilename(audiofile,firstnum,lastnum)
    #print(vediofilenames)
    #print(audiofilenames)
    num = 0
    vediotrack='0'
    for v in vediofilenames:
        r = mainmux(v,audiofilenames[num],vediotrack,audiotrack,audiofilter)
        num = num+1
        print(r)

if __name__ == '__main__':
    argv_list = []
    argv_list = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv_list,"v:a:n:t:",["vedio=", 'audio=', 'number=', 'track='])
    except getopt.GetoptError:
        usage()
        exit()
    audiotrack = 0
    firstnum = 1
    lastnum = 1
    audiofilter = 'copy'
    for o, a in opts:
        if o in ('-v', '--vedio'):
            vediofile = a
        if o in ('-a', '--audio'):
            audiofile = a
        if o in ('-n', '--number'):
            a = a.split("~")
            firstnum = a[0]
            lastnum = a[1]
            if firstnum>lastnum :
                exit("开始数不能大于结束数")
        if o in ('-t', '--track'):
            audiotrack = a
    try:
        audiofile
    except:
        audiofile = vediofile
automux(vediofile,audiofile,firstnum,lastnum,audiotrack,audiofilter)