#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_models.py.py
@Date    ：2025/7/21 16:16
@Descrip ：
'''


from models.view_models_curd import obj_create,obj_update,obj_delete,obj_searchall
from views.page_public import batch_remove_scopes
from pywebio.input import *
from pywebio.output import *


def refresh_table(models=obj_searchall()):
    """刷新表格显示"""
    with use_scope('models_table_scope'):
        put_button("新建", onclick=create_model)
        if not models:
            put_text("暂无数据")
            return
        table_data = []
        for idx, model in enumerate(models):
            row = [
                model.get('note_name', ''),
                model.get('model_name', ''),
                model.get('request_url', ''),
                model.get('api_key', ''),
                put_button('修改', onclick=lambda x=idx: update_model(x), small=True),
                put_button('删除', onclick=lambda x=idx: delete_model(x), small=True, color='danger')
            ]
            table_data.append(row)

        put_table(table_data, header=['备注名', '模型名', '请求地址', '密钥', '修改', '删除']).style("display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;")


def create_model():
    data = input_group("新建模型", [
        input('note_name', name='note_name', required=True),
        input('model_name', name='model_name', required=True),
        input('request_url', name='request_url', required=True),
        input('api_key', name='api_key', type=PASSWORD, required=True),
    ])
    if data:
        r_models = obj_create(data)
        load_interface(r_models)
        toast("新建成功", color='success')
    else:
        load_interface()


def update_model(index):
    """修改模型"""
    models = obj_searchall()
    if not (0 <= index < len(models)):
        return
    model = models[index]
    data = input_group("修改模型", [
        input('note_name', name='note_name', value=model.get('note_name', ''), required=True),
        input('model_name', name='model_name', value=model.get('model_name', ''), required=True),
        input('request_url', name='request_url', value=model.get('request_url', ''), required=True),
        input('api_key', name='api_key', type=PASSWORD, value=model.get('api_key', ''), required=True),
    ])

    if data:
        r_models = obj_update(index,data)
        load_interface(r_models)
        toast("修改成功", color='success')
    else:
        load_interface()


def delete_model(index):
    """删除模型"""
    models = obj_searchall()
    if not (0 <= index < len(models)):
        return

    confirm = actions('确认删除？', [
        {'label': '确认', 'value': True, 'color': 'danger'},
        {'label': '取消', 'value': False}
    ])

    if confirm:
        r_models = obj_delete(index)
        load_interface(r_models)
        toast("删除成功", color='success')
    else:
        load_interface()


def load_interface(models=None):
    """加载界面"""
    batch_remove_scopes()
    put_scope('models_table_scope')
    if models:
        refresh_table(models=models)
    else:
        refresh_table(models=obj_searchall())

def page_models():
    """模型管理页面"""
    load_interface()