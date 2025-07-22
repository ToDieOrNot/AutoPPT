#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_prompt.py
@Date    ：2025/7/22 10:19
@Descrip ：
'''


from views.page_public import *
from models.view_prompts_curd import *
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *


def refresh_table(tabs_datas=obj_searchall()):
    if not tabs_datas:
        put_text("暂无数据")
        return
    with use_scope('prompts_table_scope'):
        datas = []
        for tab_code,tab_name in dict_prompt_tabs.items():
            table_data = []
            for idx, prompt_col in enumerate(tabs_datas[tab_code]):
                row = [
                    tab_name,
                    prompt_col.get('file_name', ''),
                    prompt_col.get('param_text1', ''),
                    prompt_col.get('param_text2', ''),
                    prompt_col.get('param_file1', ''),
                    prompt_col.get('param_file2', ''),
                ]
                table_data.append(row)
            datas.append({'title': tab_name, 'content': [put_row([put_button("新建", onclick=create_prompt),None,put_button("查改", onclick=update_prompt)], size="auto 20px auto").style("display: flex; text-align: left; justify-content: left; "),put_table(table_data, header=['类型', '文件名', '文本参数1', '文本参数2', '文件参数1', '文件参数2']).style("display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;")]})
        put_tabs(datas).style("margin:5px;background:#F8F8FF;")


def load_interface():
    """加载界面"""
    batch_remove_scopes()
    put_scope('prompts_table_scope')
    refresh_table()


def create_prompt():
    data = input_group("新建词组", [
        select('Tab类型', name='tab_name', options=list(dict_prompt_tabs.values()), select=list(dict_prompt_tabs.values())[0], required=True),
        input('文件名', name='file_name', required=True),
        textarea('文件内容', name='file_content', required=True),
    ])
    if data:
        data['tab_code'] = next((k for k, v in dict_prompt_tabs.items() if v == data['tab_name']), None)
        obj_create(data)
        toast("新建成功", color='success')
    load_interface()


def update_prompt():
    data = input_group("新建词组", [
        select('Tab类型', name='tab_name', options=list(dict_prompt_tabs.values()), select=list(dict_prompt_tabs.values())[0], required=True),
        input('文件名', name='file_name', required=True),
        textarea('文件内容', name='file_content', required=True),
    ])
    if data:
        data['tab_code'] = next((k for k, v in dict_prompt_tabs.items() if v == data['tab_name']), None)
        obj_create(data)
        toast("新建成功", color='success')
    load_interface()

def page_prompts():
    """模型管理页面"""
    load_interface()
    pass
