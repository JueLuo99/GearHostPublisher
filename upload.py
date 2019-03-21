import ftplib
import os



with open(os.path.split(os.path.abspath(__file__))[0]+"./account","r") as f:
    username = f.readline().strip()
    password = f.readline().strip()

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
# print(os.path.basename(__file__))
traverseFile(localroot)

# def mkdirs(p):
#     p = os.path.split(p)[0]
#     if (p!=""):
#         mkdirs(p)
#         try:
#             ftp.mkd(p)
#         except Exception as identifier:
#             pass
        



# 初始化 FTP 连接并登录
ftp = ftplib.FTP(host=r'ftp.gear.host')
ftp.set_debuglevel(ftplibDebugLevel)
ftp.login(user=username,passwd=password)
ftp.cwd(remoteroot)

print(readyToUploadList)

# 遍历 readyToUploadList 上传文件
for f in readyToUploadList:
    print("++++++++++++++++++++++NOW f is "+f)
    localFile = f
    remoteFile = remoteroot + os.path.sep + os.path.split(f)[1]
    localRelativePath = os.path.relpath(f,start = os.path.split(os.path.abspath(__file__))[0])
    remotePath = os.path.split(remoteroot + os.path.sep +localRelativePath)[0]
    if os.path.isdir(f):
        try:
            ftp.mkd(remoteroot+localRelativePath)
        except Exception as identifier:
            pass
        ftp.cwd(remoteroot+localRelativePath)
        continue
        
    # print("remoteFile:" + remoteFile)
    # print(remotePath)
    ff = open(f,"rb")
    # print("++++++++++++++++++"+remotePath)
    try:
        ftp.cwd(remotePath)
    except Exception as identifier:
        pass
    ftp.storbinary("STOR "+os.path.split(f)[1],ff,1024)
    
    

    # f = open(os.path.split(os.path.abspath(__file__))[0]+"\\"+"test","rb")
    # # fsize = os.path.getsize(f)
    # ftp.storbinary("STOR "+"test ",f,blocksize=8192)



ftp.cwd(remoteroot)
# f = open(os.path.split(os.path.abspath(__file__))[0]+"\\"+"test")
# fsize = os.path.getsize(f)
# ftp.storbinary("STOR "+"test ",f,blocksize=8192)
# ftp.dir("/site/wwwroot")

ftp.quit()
