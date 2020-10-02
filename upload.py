#!/usr/bin/python3

import ftplib
import os

# 读取配置
with open(os.path.split(os.path.abspath(__file__))[0]+"./account","r") as f:
    username = f.readline().strip()
    password = f.readline().strip()

# 参数设置
ftplibDebugLevel = 1
remoteroot = "/site/wwwroot"
localroot = os.path.split(os.path.abspath(__file__))[0]
readyToUploadList = []

# 该函数用于遍历目录，将需要上传的文件添加到 readyToUploadList 中
def traverseFile(rootpath):
    for l in os.listdir(rootpath):
        path = os.path.join(rootpath,l)
        # 如果碰到以“.”开头的隐藏文件夹则跳过
        if l.startswith("."):
            continue
        # 跳过配置文件和自身的上传
        if (l == "account" or l==os.path.basename(__file__)):
            continue
        readyToUploadList.append(path)
        if os.path.isdir(path):
            traverseFile(path)


traverseFile(localroot)

# 初始化 FTP 连接并登录
ftp = ftplib.FTP(host=r'ftp.gear.host')
ftp.set_debuglevel(ftplibDebugLevel)
ftp.login(user=username,passwd=password)
ftp.cwd(remoteroot)

# 遍历 readyToUploadList 上传文件
for f in readyToUploadList:
    localFile = f
    remoteFile = remoteroot + os.path.sep + os.path.split(f)[1]
    localRelativePath = os.path.relpath(f,start = os.path.split(os.path.abspath(__file__))[0])
    remotePath = os.path.split(remoteroot + os.path.sep +localRelativePath)[0]
    # 递归创建目录
    if os.path.isdir(f):
        try:
            ftp.mkd(remoteroot+localRelativePath)
        except Exception as identifier:
            pass
        ftp.cwd(remoteroot+localRelativePath)
        continue
    # 上传文件  
    ff = open(f,"rb")
    try:
        ftp.cwd(remotePath)
    except Exception as identifier:
        pass
    ftp.storbinary("STOR "+os.path.split(f)[1],ff,1024)

ftp.quit()

os.system("pause")
