# coding=utf-8
# 作用：微服务接口验证客户端

import os, hashlib
import requests
import json

#获取文件MD5
def getmd5(filename):
    m = hashlib.md5()
    mfile = open(filename, 'rb')
    m.update(mfile.read())
    mfile.close()
    return m.hexdigest()

#扫码获得IP、端口号和服务类型
qrinfo = '127.0.0.1:8098-1'
connIPPort = qrinfo.split('-')[0]
method = qrinfo.split('-')[1]

#通知服务端连接成功
print('客户端连接成功!')
requests.get(url='http://' + connIPPort + '/showinfo?info=客户端连接成功!')

# 数据下载
if (method == '1'):

    #获取下载文件信息
    res = requests.get(url='http://' + connIPPort + '/downloadfileinfo')
    fileinfo = json.loads(res.content)

    #提示正在下载文件
    print('正在下载数据...')
    requests.get(url='http://' + connIPPort + '/showinfo?info=正在下载数据...')

    #下载文件
    urlString = 'http://' + connIPPort + '/download?fileid=' + fileinfo['fileid']
    res = requests.get(url=urlString, stream=True)

    #文件保存
    savefile = fileinfo['fileid'] + ".zip"
    f = open(savefile, "wb")
    for chunk in res.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

    f.close()

    #验证文件大小和MD5，是否与服务端一致
    datamd5 = getmd5(savefile)
    datasize = os.path.getsize(savefile)

    if (datamd5 != fileinfo['filemd5'] or datasize != fileinfo['filesize']):
        print('数据下载错误!')
        requests.get(url='http://' + connIPPort + '/showinfo?info=数据下载错误!')
    else:
        print('数据下载成功!')
        requests.get(url='http://' + connIPPort + '/showinfo?info=数据下载成功!')

    #提示服务端传输完成
    requests.get(url='http://' + connIPPort + '/transformdone')

else:
    #数据上传
    todo = 'TODO'