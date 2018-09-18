#!/bin/python
# -*- coding: utf-8-*-
'''利用pytesseract包OCR识别图片，精确率较百度云平台较差'''
from PIL import Image
import pytesseract
text=pytesseract.image_to_string(Image.open('C:\\Users\\sloan\\Desktop\\aa.bmp'),lang="chi_sim+eng")
print(text)