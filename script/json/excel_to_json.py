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
    # wb = openpyxl.load_workbook("lsu_test_plan.xlsx")
    # print(wb)
    # sheet = wb.get_sheet_by_name("test2007")
    sheet = wb[sheet_name]  # 通过sheet名称锁定表格
    # new_list = []
    for row in sheet.rows:  # 循环所有的行
        list_release = []
        for cell in row:    # 循环行中所有的单元格
            # print(cell.value, "\t",end ="")  # 获取单元格的值
            list_release.append(cell.value)
        # c=list_release[0]
        # print(list_release[0])
        if list_release[0] == None:
            return
        elif "_test" in list_release[0]:
            process_to_json(list_release)
        else:
            pass
            # print(1)


def process_to_json(json_list):
    list_json = json_list
    release_dirt = {'uvm_testname':'test',"sim_args":'test',"tcl": wave_path,"timescale":"1ns/1ps"}
    release_dirt["uvm_testname"] = list_json[4]
    # print(type(list_json[3]))
    list_json[3] = list_json[3].replace(';', '')
    list_json[3] = re.split('\n |=', list_json[3])
    a = 1
    # # list_json[3] = list_json[3].replace(';', '')
    # # string1 = '%s%s%s%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][1], list_json[3][2], '\"')
    # for i in range(1, len(list_json[3])+1, 2):
    #     # print(list_json[3])
    #     # print(type(list_json[3]))
    #     if list_json[3][i].isdigit():
    #         string1 = '%s%s%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][i - 1], list_json[3][i], '\"')
    #         str_list.append(string1)
    #     else:
    #         string1 = '%s%s%s,%s%s' % ('+uvm_set_config_string=\"', sqr_str, list_json[3][i-1], list_json[3][i], '\"')
    #         str_list.append(string1)
    while a<len(list_json[3]):
        if list_json[3][a].isdigit():
            string1 = '%s%s%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
            str_list.append(string1)
        else:
            if varb in list_json[3][a]:
                list_json[3][a] = list_json[3][a].replace("'b", '')
                list_json[3][a] = int(list_json[3][a], 2)
                string1 = '%s%s%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                str_list.append(string1)
            elif varh in list_json[3][a]:
                list_json[3][a] = list_json[3][a].replace("'h", '')
                list_json[3][a] = int(list_json[3][a], 16)
                string1 = '%s%s%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                str_list.append(string1)
            else:
                string1 = '%s%s%s,%s%s' % ('+uvm_set_config_string=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                str_list.append(string1)
        a = a+2
    # t = list_json[3].split(spe=\n, maxsplit=-1)
    # print(list_json[3])
    # print(str_list)
    # print(str_list[0])
    string3 = ''.join(str_list)
    str_list.clear()
    release_dirt["sim_args"] = string3
    json_all = {list_json[0]: release_dirt}
    # print(release_dirt)
    # json_str = json.dumps(release_dirt)
    # json_all.append(release_dirt)
    # json_all = {list_json[0]: json_all1}
    json_pt.append(json_all)
    # f = open('release_notes.json', 'w')
    # f.writelines(json_all)
    # f.close()
    json_str1 = json.dumps(json_pt)
    # print(type{json_str1})
    json_str2 = json_str1.replace('[', '')
    json_str3 = json_str2.replace(']', '')
    json_str4 = json_str3.replace('}, {', ',')
    json_str5 = json_str4.replace('{', '{\n')
    json_str6 = json_str5.replace('",', '",\n')
    json_str7 = json_str6.replace('},', '},\n')
    json_str8 = json_str7.replace('1ps"', '1ps"\n')
    json_str9 = json_str8.replace('"uvm_testname"', ' "uvm_testname"')
    json_str10 = json_str9.replace('"sim_args"', ' "sim_args"')
    json_str11 = json_str10.replace('"tcl"', ' "tcl"')
    json_str12 = json_str11.replace('"timescale"', ' "timescale"')
    json_str = json_str12.replace('*', '[*]')

    # re.sub('[', '', json_str)
    f = open(json_name, 'w')
    f.write(json_str)
    f.close()


print("Conversion start")
# file_07_excel = "c:/user/lsu_test_plan.xlsx"
# 设置表格路径，默认路径是执行文件的当前目录
# file_07_excel = "./lsu_test_plan.xlsx"
# excel_name = "./lsu_test_plan.xlsx"
file_07_excel = excel_name
read_07_Excel(file_07_excel)
print("Conversion succeeded")
