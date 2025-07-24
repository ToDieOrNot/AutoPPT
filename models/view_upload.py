#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：view_upload.py
@Date    ：2025/7/28 15:06
@Descrip ：
'''


import os
from pywebio.input import *
from pywebio.output import *
from models.config_read import read_env
from views.page_public import dict_upload_option




def obj_searchall():
    pass


def obj_create(data):
    dict_env = read_env()
    file_type = data.get("type")
    dict_file = data.get("file")
    file_name = dict_file.get("filename")
    dir_file = dict_env.get(dict_upload_option.get(file_type))
    if "pptx" in file_name:
        with open(os.path.join(dir_file, file_name), "wb") as f:
            f.write(dict_file.get("content"))
    else:
        with open(os.path.join(dir_file,file_name),"w",encoding="utf-8") as f:
            f.write(dict_file.get("content"))


def obj_update(data):
    pass


def obj_delete(data):
    pass