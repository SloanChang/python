'''''
��ҳ����
��ȡ����ͼƬ
'''

import urllib.request
import re


def getHtml():
    # ��ַ
    url = "http://www.douban.com/"
    # ��ȡ���
    response = urllib.request.urlopen(url)

    data = response.read()
    # ��ӡ��ȡ��ҳ�ĸ�����Ϣ
    # print(type(response))
    # print(response.geturl())
    # print(response.info())
    # print(response.getcode())

    # ���ý��뷽ʽ
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