# coding=utf-8
# import binascii
# -*-coding:UTF-8-*-
# ####################################
# File name :   excel_to_json
# Author    :   wangxx
# version   :   V1.0
# ####################################
# import os
import openpyxl
import json
import re
import parameter

excel_name = parameter.excel_name
sqr_str = parameter.sqr_str
sheet_name = parameter.sheet_name
wave_path = parameter.wave_path
json_name = parameter.json_name
varb = "'b"
varh = "'h"
# sqr_str = "uvm_test_top.lsu_env0.lsu_virt.sqr"
# sheet_name = "LSU"
json_all = []
json_pt = []
str_list = []


def read_07_Excel(file_path):
    print("****************************")
    print(file_path)
    wb = openpyxl.load_workbook(file_path)      # 打开文件
    sheet = wb[sheet_name]  # 通过sheet名称锁定表格
    testcase_num = []
    for row in sheet.rows:  # 循环所有的行
        list_release = []
        for cell in row:    # 循环行中所有的单元格
            list_release.append(cell.value)
        if list_release[0] == None:
            return
        elif "_test" in list_release[0]:
            # process_to_json(list_release)
            testcase_num.append(list_release[0])
        else:
            pass
            # print(1)


def print_case(testcase_num):
    print("***********")
    i = 0
    for i in range(len(testcase_num)):
        print(testcase_num[i])

print("Conversion start")
file_07_excel = excel_name
read_07_Excel(file_07_excel)
print("Conversion succeeded")
