#!/bin/python
# -*- coding: utf-8-*-
'''利用百度云平台，OCR识别图片'''
from aip import AipOcr
def main():
    '''APP_ID,API_KEY,SECRET_KEY需要自己注册获取'''

    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    # 初始化AipOcr
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 图片路径
    filePath ="C:\\Users\\sloan\\Desktop\\20180905133709.jpg"
    # 读取图片
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # 其他配置参数
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG'
    }
    # 调用通用文字识别接口
    result = aipOcr.basicGeneral(get_file_content(filePath), options)
    print (result.values())

if __name__ == '__main__':
    main()