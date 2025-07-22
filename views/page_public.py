#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_public.py
@Date    ：2025/7/22 12:24
@Descrip ：
'''

from pywebio.output import remove
from pywebio.output import *

dict_prompt_tabs = {"split_outline":"概括大纲","split_port":"点阵图","output_ppt":"生成PPT"}
def batch_remove_scopes(scope_names=["models_table_scope","prompts_table_scope","courses_table_scope"]):
    """
    批量删除多个scope，自动跳过不存在的scope
    参数:
        scope_names (list): 要删除的scope名称列表
        recursive (bool): 是否递归删除子scope，默认为False
    """
    # clear()
    for name in scope_names:
        try:
            remove(scope=name)
        except Exception as e:  # 捕获scope不存在或其他异常
            print(e)
            continue  # 跳过错误，继续处理下一个scope
