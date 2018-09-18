#!/bin/python
# -*- coding: UTF-8 -*-
'''利用base64与AES对字符串加密解密'''
from Crypto.Cipher import AES
import base64
PADDING = '\0'
pad_it = lambda s: s+(16 - len(s)%16)*PADDING

key = 'aasaasasasasasas'
aiv = 'asadasfasfsdsagg'
# 加密
def encrypt_aes(sourceStr):
	generator = AES.new(key,AES.MODE_CBC,aiv)
	crypt = generator.encrypt(pad_it(sourceStr))
	cryptedSer = base64.b64encode(crypt)
	return cryptedSer

#解密
def getplaintext(ciphertext):
    generator = AES.new(key, AES.MODE_CBC, aiv)
    cryptedStr = base64.b64decode(ciphertext)
    recovery = generator.decrypt(cryptedStr)
    decryptedStr = recovery.rstrip(PADDING)
    return decryptedStr