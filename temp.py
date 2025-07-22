#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：temp.py
@Date    ：2025/7/22 12:47
@Descrip ：
'''

import os
from views.page_public import batch_remove_scopes
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from views.page_public import batch_remove_scopes
from models.config_read import read_env


def read_prompt_dirmap():
    dict_env = read_env()
    DIR_MAP = {
        "概括大纲": dict_env.get('dir_prompts_split_outline'),
        "点阵图": dict_env.get('dir_prompts_split_port'),
        "生成PPT": dict_env.get('dir_prompts_outppt')
    }
    return DIR_MAP
def load_prompts():
    """从目录加载所有 .txt 提示词文件内容"""
    DIR_MAP = read_prompt_dirmap()
    prompts = {}
    for tab_name, directory in DIR_MAP.items():
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        prompts[tab_name] = {}
        for f in files:
            with open(os.path.join(directory, f), 'r', encoding='utf-8') as fp:
                prompts[tab_name][f] = fp.read()
    return prompts
def save_prompt(tab_name, filename, content):
    """保存提示词文件"""
    DIR_MAP = read_prompt_dirmap()
    directory = DIR_MAP[tab_name]
    with open(os.path.join(directory, filename), 'w', encoding='utf-8') as fp:
        fp.write(content)
def delete_prompt_file(tab_name, filename):
    """删除提示词文件"""
    DIR_MAP = read_prompt_dirmap()
    directory = DIR_MAP[tab_name]
    os.remove(os.path.join(directory, filename))


from pywebio import start_server
from pywebio.output import put_button, put_text, popup
from pywebio.input import input, TEXT, password, PASSWORD

def main():
    put_button("打开登录表单", onclick=show_login_form)

def show_login_form():
    popup("用户登录", [
        put_text("请输入您的登录信息"),
        put_form("login_form", [
            input("用户名", name="username", type=TEXT),
            password("密码", name="password", type=PASSWORD)
        ]),
        put_button("登录", onclick=lambda: handle_login(), color='primary')
    ])

def handle_login():
    form_data = get_form("login_form")
    # 这里添加验证逻辑
    put_text(f"登录成功，欢迎 {form_data['username']}！")

if __name__ == '__main__':
    start_server(main, port=8080)