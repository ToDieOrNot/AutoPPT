#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_run.py
@Date    ：2025/7/28 17:20
@Descrip ：
'''


from pywebio.output import *
from pywebio.session import *
from views.page_public import batch_remove_scopes
from models.view_run import *
from pywebio.input import *
from pywebio.output import *



def update_params(prompt_key):
    res = dict_update_params(prompt_key)
    input_update(name='param_text1', value=res["param_text1"])
    input_update(name='param_text2', value=res["param_text2"])
    input_update(name='param_file1', value=res["param_file1"])
    input_update(name='param_file2', value=res["param_file2"])

def create_auto_run_step1():
    use_scope("run_scope")
    res = obj_searchall()
    data = input_group("新建流程", [
        input('PPT名称', name='pptx_name', required=True),
        select("PPT模板", options=list(res["dict_files_pptx"].keys()), value=list(res["dict_files_pptx"].keys())[0],
               name="pptx", required=True),
        select("模型", options=list(res["dict_json_models"].keys()), value=list(res["dict_json_models"].keys())[0],
               name="models", required=True),
        select("系统提示词", options=list(res["dict_files_prompts"].keys()),
               value=list(res["dict_files_prompts"].keys())[0], name="sys_prompt", required=True),
        select("用户提示词", options=list(res["dict_files_prompts"].keys()),
               value=list(res["dict_files_prompts"].keys())[0], name="user_prompt", required=True,
               onchange=lambda name: update_params(name)),
        input('文本参数1', name='param_text1', required=False),
        input('文本参数2', name='param_text2', required=False),
        select("文件参数1", options=["None"]+list(res["dict_files_params"].keys()),
               value="None", name="param_file1", required=False),
        select("文件参数2", options=["None"]+list(res["dict_files_params"].keys()),
               value="None", name="param_file2", required=False),
    ])
    if data:
        obj_run(data)
        toast("任务已提交,请等待执行...", color='success')
    load_interface()

def create_auto_run_step2():
    pass



def load_interface():
    batch_remove_scopes()
    put_scope("run_scope")
    create_auto_run_step1()


def page_run():
    load_interface()
