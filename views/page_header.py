#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT_Test
@File    ：page_header.py.py
@Date    ：2025/7/21 16:16
@Descrip ：
'''

from flask import Flask
import pywebio
from pywebio import config
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.platform.tornado import start_server
from models.config_read import read_env



from views.page_models import page_models
from views.page_prompt import page_prompts
# from view.notice2 import notice2
# from view.notice3 import notice3
# from view.notice4 import notice4
# from view.notice5 import notice5

config(theme='minty')
dict_env = read_env()
pywebio_port=int(dict_env.get("port"))
pywebio_host=str(dict_env.get("host"))
pywebio_index_url = "127.0.0.1:"+str(pywebio_port) if pywebio_host == "0.0.0.0" else pywebio_host+":"+str(pywebio_port)
# pywebio_index_url = "127.0.0.0:8090"
def test():
    put_markdown("### ")




# 使用示例

def page_header():
    clear()
    with use_scope('title'):
        put_column([
            put_html("<center><b> 教 辅 资 源 </b></center>").style("font-family:Cursive;font-size:30px;")
        ]).style("margin-bottom:10px;background:#F8F8FF")

    with use_scope('tag'):
        put_row([
            put_table([
                [
                    put_button(
                        "首页",
                        onclick=lambda: run_js('window.location.href="http://'+pywebio_index_url+'"')
                    ),
                    put_button("教材", onclick=test),
                    put_button("模板", onclick=test),
                    put_button("课件", onclick=test),
                    put_button("试题", onclick=test),
                    put_button("授课", onclick=test),
                    put_button("模型", onclick=page_models),
                    put_button("Prompt", onclick=page_prompts),
                ]
            ]).style("display: flex; justify-content: center; align-items: center; width: 100%; height: 100%;")
        ]).style("margin:5px;background:#F8F8FF;")