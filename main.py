#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：main.py
@Date    ：2025/7/21 14:54
@Descrip ：
'''


from flask import Flask
import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.platform.tornado import start_server
from models.config_read import read_env


from views.page_header import page_header,pywebio_port,pywebio_host
from views.page_models import page_models
from views.page_prompt import page_prompts


def main_body():
    pass
    # with use_scope('show'):
    #     put_tabs([
    #         {'title': '热门', 'content': [
    #             put_table([
    #                 ['商品', '详情', '数量', '价格', '库存', '购买'],
    #                 ['微软邮箱', '全新微软outlook邮箱', '1', '0.5', '100', put_link("购买","http://www.baidu.com")],
    #                 ['微软邮箱', '一年微软outlook邮箱', '1', '2', '99', put_link("购买","http://www.baidu.com")],
    #             ]).style("display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;")
    #         ]},
    #         {'title': '小红书', 'content': [
    #             put_table([
    #                 ['商品', '详情', '数量', '价格', '库存', '购买'],
    #                 ['小红书账号', '一年小红书万粉账号', '1', '800', '5', put_link("购买","http://www.baidu.com")],
    #                 ['小红书账号', '一年小红书千粉账号', '1', '100', '46', put_link("购买","http://www.baidu.com")],
    #             ]).style("display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;")
    #         ]},
    #     ]).style("margin:5px;background:#F8F8FF;")


def index():
    page_header()
    main_body()


if __name__ == '__main__':
    dict_env = read_env()
    start_server([index,page_models,page_prompts], port=pywebio_port, host=pywebio_host, session_expire_seconds=600, debug=False)