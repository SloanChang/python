#!/bin/python
# -*- coding: utf-8-*-
'''���ðٶ���ƽ̨��OCRʶ��ͼƬ'''
from aip import AipOcr
def main():
    '''APP_ID,API_KEY,SECRET_KEY��Ҫ�Լ�ע���ȡ'''

    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    # ��ʼ��AipOcr
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # ͼƬ·��
    filePath ="C:\\Users\\sloan\\Desktop\\20180905133709.jpg"
    # ��ȡͼƬ
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # �������ò���
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG'
    }
    # ����ͨ������ʶ��ӿ�
    result = aipOcr.basicGeneral(get_file_content(filePath), options)
    print (result.values())

if __name__ == '__main__':
    main()