'''''
网页爬虫
爬取网络图片
'''

import urllib.request
import re


def getHtml():
    # 网址
    url = "http://www.douban.com/"
    # 爬取结果
    response = urllib.request.urlopen(url)

    data = response.read()
    # 打印爬取网页的各类信息
    # print(type(response))
    # print(response.geturl())
    # print(response.info())
    # print(response.getcode())

    # 设置解码方式
    data1 = data.decode('utf-8')
    return data1


def getImage(html):
    reg = r'data-origin="(https://.+?\.jpg)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    imgName = 0
    for imgPath in imglist:
        f = open("D:/img/" + str(imgName) + ".jpg", 'wb')
        f.write((urllib.request.urlopen(imgPath)).read())
        f.close()
        imgName += 1


print("All Done!")