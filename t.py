#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoPPT
@File    ：page_prompt.py
@Date    ：2025/7/22
@Descrip ：
"""
from views.page_public import *
from models.view_prompts_curd import *

tabs_datas=obj_searchall()
datas = []
for tab_code,tab_name in dict_prompt_tabs.items():
    table_data = []
    for idx, prompt_col in enumerate(tabs_datas[tab_code]):
        print(prompt_col)