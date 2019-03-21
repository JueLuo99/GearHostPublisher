import ftplib
import os

username = r'username'
password = r'password'

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
        # print(path)
        if os.path.isdir(path):
            traverseFile(path)
        else:
            readyToUploadList.append(path)
traverseFile(localroot)


print(os.path.basename(__file__))
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
    remotePath = remoteroot + localRelativePath
    # print("remoteFile:" + remoteFile)
    # print(remotePath)
    ff = open(f,"rb")
    print(ftp.pwd())
    ftp.storbinary("STOR "+localRelativePath,ff,1024)

    # f = open(os.path.split(os.path.abspath(__file__))[0]+"\\"+"test","rb")
    # # fsize = os.path.getsize(f)
    # ftp.storbinary("STOR "+"test ",f,blocksize=8192)



ftp.cwd(remoteroot)
# f = open(os.path.split(os.path.abspath(__file__))[0]+"\\"+"test")
# fsize = os.path.getsize(f)
# ftp.storbinary("STOR "+"test ",f,blocksize=8192)
# ftp.dir("/site/wwwroot")

ftp.quit()
