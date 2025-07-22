#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：view_prompts_curd.py
@Date    ：2025/7/22 14:18
@Descrip ：
'''

import os
from models.config_read import read_env


def parse_params(content):
    """解析文件中的参数"""
    params = {
        "param_text1": "",
        "param_text2": "",
        "param_file1": "",
        "param_file2": ""
    }
    if "{{{text1}}}" in content:
        params["param_text1"] = "param_text1"
    if "{{{text2}}}" in content:
        params["param_text2"] = "param_text2"
    if "{{{file1}}}" in content:
        params["param_file1"] = "param_file1"
    if "{{{file2}}}" in content:
        params["param_file2"] = "param_file2"
    return params

def obj_searchall():
    dict_env = read_env()
    tabs_datas = {}
    tabs = ["split_outline","split_port","output_ppt"] ## 概括大纲、点阵图、生成PPT
    for tab in tabs:
        tabs_datas[tab] = []
        dir_tab = dict_env.get('dir_prompts_'+str(tab))
        for filename in os.listdir(dir_tab):
            column_data = {}
            column_data["file_name"] = filename
            filepath = os.path.join(dir_tab, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                params = parse_params(content)
                column_data["file_content"] = content
                column_data["param_text1"] = params["param_text1"]
                column_data["param_text2"] = params["param_text2"]
                column_data["param_file1"] = params["param_file1"]
                column_data["param_file2"] = params["param_file2"]
            tabs_datas[tab].append(column_data)
    return tabs_datas

def obj_create(data):
    file_path = os.path.join(read_env().get('dir_prompts_' + str(data['tab_code'])),data['file_name'])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data['file_content'])


def obj_update(data):
    file_path = os.path.join(read_env().get('dir_prompts_' + str(data['tab_code'])), data['file_name'])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data['file_content'])

def obj_delete(tabs_datas, tab_name, file_name):
    file_path = os.path.join(read_env().get('dir_prompts_' + str(tab_name)), file_name)
    os.remove(file_path)
    return tabs_datas