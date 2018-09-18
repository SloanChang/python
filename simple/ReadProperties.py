#!/bin/python
# -*- coding: UTF-8 -*-
'''读取properties类型文件'''
import sys
class Properties:
	def __init__(self,file_name):
		self.file_name = file_name
		self.properties = {}
		try:
			fopen = open(self.file_name,'r')
			for line in fopen:
				line = line.strip()
				if line.find('=') > 0 and not line.startswith('#'):
					index = line.find('=')
					line[0:index]
					self.properties[line[0 : index]] = line[index + 1 :]
			fopen.close()
		except Exception,e:
			raise e

	def get(self,key,default_value=''):
		if self.properties.has_key(key):
			return self.properties[key]
		return default_value

props = Properties(sys.argv[1])