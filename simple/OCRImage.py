#!/bin/python
# -*- coding: utf-8-*-
'''����pytesseract��OCRʶ��ͼƬ����ȷ�ʽϰٶ���ƽ̨�ϲ�'''
from PIL import Image
import pytesseract
text=pytesseract.image_to_string(Image.open('C:\\Users\\sloan\\Desktop\\aa.bmp'),lang="chi_sim+eng")
print(text)