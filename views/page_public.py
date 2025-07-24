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


## 配置
### 提示词功能
dict_prompt_tabs = {"split_outline":"概括大纲","split_port":"点阵图","output_ppt":"生成PPT"}
### PPTX页属性
dict_pptx_page_type = ["首页", "目录页", "标题和内容", "内容页", "内容页", "总结页", "尾页"]
dict_pptx_page_params = {
    "名称":"name",
    "类型":"type",
    "描述":"descript",
    "placeholders":{
        "一级标题1": "fisrt_title1",
        "一级标题2": "fisrt_title2",
        "二级标题1": "second_title1",
        "二级标题2": "second_title2",
        "三级标题1": "third_title1",
        "三级标题2": "third_title2",
        "正文内容1": "context1",
        "正文内容2": "context2",
        "插图1": "pic1",
        "插图2": "pic2"
    }
}



## 清除全部scopes


def batch_remove_scopes(scope_names=["models_table_scope","prompts_table_scope","courses_table_scope","template_pptx_table_scope","pptx_page_setting_scope"]):
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
