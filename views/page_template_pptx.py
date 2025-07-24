#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_template_pptx.py
@Date    ：2025/7/23 15:15
@Descrip ：
'''

from models.view_template_pptx_curd import *
from views.page_public import batch_remove_scopes,dict_pptx_page_params
from pywebio.input import *
from pywebio.output import *


def refresh_table(table_datas=obj_searchall()):
    if not table_datas:
        put_text("暂无数据")
        return
    with use_scope('template_pptx_table_scope'):
        table_data = []
        for idx, filename in enumerate(table_datas["file_name"]):
            row = [
                filename,
                put_button('查改', onclick=lambda x=filename: update_template_pptx(x,table_datas), small=True),
                put_button('删除', onclick=lambda x=filename: delete_template_pptx(x), small=True, color='danger')
            ]
            table_data.append(row)
        put_table(table_data, header=['文件名', '查改', '删除']).style(
            "display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;"
        )



def on_page_change(selected_page):
    clear("pptx_page_setting_scope")
    with put_scope("pptx_page_setting_scope"):
        page_key_str = f"page{selected_page}"
        print(page_key_str)



def update_template_pptx(filename, table_datas):
    dict_detail = table_datas["detail"][filename]
    pptx_json = table_datas["pptx_json"][filename]
    dict_public_placeholders = dict_pptx_page_params["placeholders"]
    list_dict_detail_keys = list(dict_detail.keys())
    batch_remove_scopes()
    with put_scope("template_pptx_table_scope"):
        select("选择页数", options=list_dict_detail_keys, onchange=list_dict_detail_keys[0], name="page_selector")
        # 表单显示区域
        put_scope("pptx_page_setting_scope")
        # 初始加载第一页（如果有页）
        if list_dict_detail_keys:
            on_page_change(list_dict_detail_keys[0])
    return {}

def update_template_pptx1(filename,table_datas):
    dict_detail = table_datas["detail"][filename]
    pptx_json = table_datas["pptx_json"][filename]
    dict_public_placeholders = dict_pptx_page_params["placeholders"]
    page_input_groups = []
    for page_key in dict_detail.keys():
        page_input_rows = []
        dict_pptx_json_page = pptx_json.get("page" + str(page_key)) if pptx_json.get("page" + str(page_key)) else {'name': '', 'type': '', 'descript': '', 'fisrt_title1': '', 'fisrt_title2': '', 'second_title1': '', 'second_title2': '', 'third_title1': '', 'third_title2': '', 'context1': '', 'context2': '', 'pic1': '', 'pic2': ''}
        page_input_rows.append(
            input_group("页属性",[
                input("页名称", name=f"page{page_key}_name", value=dict_pptx_json_page["name"], readonly=True),
                input("页类型", name=f"page{page_key}_type", value=dict_pptx_json_page["type"], readonly=True),
                input("页描述", name=f"page{page_key}_descript", value=dict_pptx_json_page["descript"], readonly=True),
            ])
        )
        # for d_k,d_v in dict_detail[page_key].items():
        #     len_page_input_rows = len(page_input_rows)
        #     page_input_rows.append(
        #         input_group("占位符",[
        #             input("内容", name=f"page{page_key}_placeholders_{len_page_input_rows}_name",value=d_k[:20]+"......" if len(d_k)>20 else d_k, readonly=True),
        #             input("类型", name=f"page{page_key}_placeholders_{len_page_input_rows}_code", value=d_v, readonly=True),
        #             select("值", name=f"page{page_key}_placeholders_{len_page_input_rows}_key", options=list(dict_public_placeholders.keys()), value=get_placeholder_key(dict_public_placeholders,dict_pptx_json_page,d_v,True), required=False),
        #         ])
        #     )
        page_input_groups.append(
            input_group("第"+str(page_key)+"页", page_input_rows)
        )
    data = input_group("查改", page_input_groups)
    # data = input_group("查改", [
    #     for page_len in list(dict_detail.keys()):
    #         input_group("第"+str(page_len)+"页",[])
    #
    #     # select('Tab类型', name='tab_name', options=list(dict_prompt_tabs.values()),select=list(dict_prompt_tabs.values())[0], required=True),
    #     # input('文件名', name='file_name',value=filename, required=True),
    #     # textarea('文件内容', name='file_content', required=True),
    # ])
    # if data:
    #     data['tab_code'] = next((k for k, v in dict_prompt_tabs.items() if v == data['tab_name']), None)
    #     obj_create(data)
    #     toast("新建成功", color='success')
    # load_interface()


def delete_template_pptx(filename):
    obj_delete(filename)
    pass


def load_interface():
    batch_remove_scopes()
    put_scope('template_pptx_table_scope')
    refresh_table()


def page_template_pptx():
    load_interface()