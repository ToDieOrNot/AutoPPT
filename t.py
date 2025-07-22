#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：AutoPPT
@File    ：page_prompt.py
@Date    ：2025/7/22
@Descrip ：
"""

from views.page_prompt import *
from models.view_prompts_curd import *

def main():
    refresh_table()

start_server(main, host="127.0.0.1", port=8080)