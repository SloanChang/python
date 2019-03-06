#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import pandas as pd



def main():
    '''
    主函数
    转换excel文件为csv/tsv文件
    :return:
    '''
    #声明参数解析器
    parse = argparse.ArgumentParser(description="converr  excel file to csv file")
    #-if 输入文件路径
    parse.add_argument('-if', '--inputfile', required=True, help='load file path')
    #-of 输出文件路径
    parse.add_argument('-of', '--outputfile', required=True, help='output file path')
    # -of 文件分隔符
    parse.add_argument('-sep', '--separator', required=True, help='Field delimiter for the output file')
    args = parse.parse_args()
    df = pd.read_excel(args.inputfile)
    df.to_csv(args.outputfile, encoding='utf-8', index=False,sep=args.separator)

if __name__ == '__main__':
    main()