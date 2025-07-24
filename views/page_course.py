#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_course.py
@Date    ：2025/7/23 10:32
@Descrip ：
'''


from views.page_public import *
from models.view_prompts_curd import *
from pywebio.input import *
from pywebio.output import *


def refresh_course(courses={}):
    with use_scope('courses_table_scope'):
        put_button("新建", onclick=create_course)
        if not courses:
            courses = obj_searchall()
            if not courses:
                put_text("暂无数据")
                return
        table_data = []
        for idx, course in enumerate(courses):
            row = [
                course.get('file_name'),
                course.get('prompt_sys_name'),
                course.get('prompt_user_name'),
                course.get('model_name'),
                put_button('修改', onclick=lambda x=idx: update_course(x), small=True, color='danger'),
                put_button('删除', onclick=lambda x=idx: delete_course(x), small=True, color='danger'),
                put_button('执行拆分', onclick=lambda x=idx: delete_course(x), small=True, color='success')
            ]
            table_data.append(row)
        put_table(table_data, header=['文件名', '系统提示词', '用户提示词', '模型', '修改', '删除', '执行拆分']).style("display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;")


def create_course():
    pass


def update_course():
    pass


def delete_course(index):
    pass


def exe_course(index):
    pass


def load_interface(courses=None):
    """加载界面"""
    batch_remove_scopes()
    put_scope('courses_table_scope')
    if courses:
        refresh_course(courses=courses)
    else:
        refresh_course(courses=obj_searchall())


def page_course():
    """模型管理页面"""
    load_interface()
