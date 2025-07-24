#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_upload.py.py
@Date    ：2025/7/28 15:03
@Descrip ：
'''

import pywebio
from pywebio import config
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.platform.tornado import start_server
from models.config_read import read_env
from views.page_public import dict_upload_option
from views.page_public import batch_remove_scopes
from models.view_upload import obj_create



def create_upload():
    with use_scope('upload_table_scope'):
        data = input_group("上传文件", [
            select("文件类型", name="type", options=list(dict_upload_option.keys()), value=list(dict_upload_option.keys())[0], help_text="请选择要上传的文件类型"),
            file_upload("选择文件", name="file", accept="*", required=True)
        ])
        obj_create(data)
    toast("上传成功", color='success')


def load_interface(models=None):
    """加载界面"""
    batch_remove_scopes()
    put_scope('upload_table_scope')
    create_upload()



def page_upload():
    """模型管理页面"""
    load_interface()

