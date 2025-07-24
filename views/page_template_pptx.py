#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：page_template_pptx.py
@Date    ：2025/7/23 15:15
@Descrip ：
'''
import os.path

from models.view_template_pptx_curd import *
from views.page_public import batch_remove_scopes,dict_pptx_page_params,dict_pptx_page_type
from pywebio.input import *
from pywebio.output import *
from models.config_read import read_env



def refresh_table(table_datas={}):
    # def refresh_table(table_datas=obj_searchall())
    if not table_datas:
        table_datas = obj_searchall()
        if not table_datas:
            put_text("暂无数据")
            return
    with use_scope('template_pptx_table_scope'):
        table_data = []
        for filename, fileinfo in table_datas.items():
            row = [
                filename,
                # put_button('下载', onclick=lambda x=filename: download_file(x), small=True),
                download_file(filename),
                put_button('查改', onclick=lambda x=[filename,fileinfo]: update_template_pptx(x[0],x[1]), small=True),
                put_button('删除', onclick=lambda x=filename: delete_template_pptx(x), small=True, color='danger')
            ]
            table_data.append(row)
        put_table(table_data, header=['文件名', '下载', '查改', '删除']).style(
            "display: flex; text-align: center; justify-content: center; align-items: center; width: 100%; height: 100%;"
        )


def download_file(file_name):
    try:
        dict_env = read_env()
        # 获取文件名
        file_path = os.path.join(dict_env.get("dir_pptx"),file_name+".pptx")
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # 提供文件下载
        return put_file(file_name+".pptx", file_content, label=f'下载')

    except Exception as e:
        toast(f'下载失败: {str(e)}', color='error')



def on_page_change(selected_page_num):
    pass
    # clear("pptx_page_setting_scope")
    # with put_scope("pptx_page_setting_scope"):
    #     page_key_str = f"page{selected_page}"
    #     print(page_key_str)


def update_template_pptx(filename, fileinfo, page=1):
    batch_remove_scopes()
    clear('pptx_page_setting_scope')
    put_scope("pptx_page_setting_scope")
    use_scope("pptx_page_setting_scope")
    page = int(page)
    page_total_nums = len(list(fileinfo.keys()))
    inputs = []
    page_options = [{"label": f"第{p}页", "value": p} for p in range(1, page_total_nums + 1)]
    nav_controls = [
        select("", options=page_options, value=page, name="page", onchange=lambda x:update_template_pptx(filename, fileinfo, x)),
        actions(
            name="action",
            buttons=[
                {"label": "上一页", "value": "prev", "disabled": page == 1},
                {"label": "下一页", "value": "next", "disabled": page == page_total_nums},
            ]
        )
    ]
    inputs.extend(nav_controls)
    inputs.append(input(label="页名称", name="name", value=fileinfo.get(str(page))["name"]))
    # inputs.append(input(label="页类型", name="type", value=fileinfo.get(str(page))["type"]))
    inputs.append(select(label="页类型", name="type", options=dict_pptx_page_type,value=fileinfo.get(str(page))["type"]))
    inputs.append(input(label="页描述", name="descript", value=fileinfo.get(str(page))["descript"]))
    file_page_info_placeholders = fileinfo[str(page)].get("placeholders") if fileinfo[str(page)].get("placeholders") else {}
    dict_placeholder_kv = {}
    for idx, placeholders_row in enumerate(file_page_info_placeholders):
        row_file_page_info_placeholders = file_page_info_placeholders[placeholders_row]
        inputs.append(select(
            label=f'内容:"{placeholders_row}"\t||\t占位符:"{row_file_page_info_placeholders["placeholder_code"]}"',
            options=list(dict_pptx_page_params["placeholders"].keys()),
            value= row_file_page_info_placeholders['placeholder_type_cn'] if row_file_page_info_placeholders['placeholder_type_cn'] else None,
            name=f"placeholders_{idx}"
        ))
        dict_placeholder_kv[f"placeholders_{idx}"] = row_file_page_info_placeholders["placeholder_code"]
    data = input_group(f"第 {page} 页 / 共 {page_total_nums} 页", inputs)

    action = data['action']
    if action == "prev" and page > 1:
        data = None
        page -= 1
        update_template_pptx(filename, fileinfo, page)
    elif action == "next" and page < page_total_nums:
        data = None
        page += 1
        update_template_pptx(filename, fileinfo, page)
    else:
        pass

    if data and not action:
        data["file_name"] = filename
        data["page"] = page
        data["placeholder_kv"] = dict_placeholder_kv
        obj_update(data)
        toast("查改完成", color='success')
    elif data and action:
        toast("查改失败", color='info')
    elif not data and action:
        pass ## 上下页后提交
    else:
        pass

    load_interface()



def update_template_pptx_last(filename,table_datas):
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
    toast("查改完成", color='success')
    load_interface()

def load_interface():
    batch_remove_scopes()
    put_scope('template_pptx_table_scope')
    refresh_table()


def page_template_pptx():
    load_interface()