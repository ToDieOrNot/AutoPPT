#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：view_run.py
@Date    ：2025/7/28 17:11
@Descrip ：
'''



import os, json
from models.model_open_ai import quest_open_ai
from models.config_read import read_env,recursive_list_files,read_json_file
from models import view_models_curd



def getfile_syspro_expand():
    pass




def dict_update_params(prompt_file_name):
    dict_env = read_env()
    dir_prompts = dict_env.get("dir_prompts")
    file_path = recursive_list_files(dir_prompts).get(prompt_file_name)
    res = {}
    param_true_value = "请设置参数"
    param_false_value = "无需编辑此处"
    with open(file_path,"r",encoding="utf-8") as f:
        file_data = f.read()
        if "{{{text1}}}" in file_data:
            res["param_text1"] = param_true_value
        else:
            res["param_text1"] = param_false_value
        if "{{{text2}}}" in file_data:
            res["param_text2"] = param_true_value
        else:
            res["param_text2"] = param_false_value
        if "{{{file1}}}" in file_data:
            res["param_file1"] = param_true_value
        else:
            res["param_file1"] = param_false_value
        if "{{{file2}}}" in file_data:
            res["param_file2"] = param_true_value
        else:
            res["param_file2"] = param_false_value
        return res


def obj_run(data={}):
    try:
        if not data:
            return
        if data["param_text1"] in ["请设置参数","无需编辑此处"]:
            data["param_text1"] = ""
        if data["param_text2"] in ["请设置参数","无需编辑此处"]:
            data["param_text2"] = ""
        if data["param_file1"] == "None":
            data["param_file1"] = ""
        if data["param_file2"] == "None":
            data["param_file2"] = ""

        data_all = obj_searchall()
        dict_files_prompts = data_all["dict_files_prompts"]
        dict_json_models = data_all["dict_json_models"]
        dict_files_params = data_all["dict_files_params"]
        dict_files_pptx = data_all["dict_files_pptx"]
        with open(dict_files_prompts.get(data["sys_prompt"]),"r",encoding="utf-8") as sys_f:
            msg_prompt = sys_f.read()
        with open(dict_files_prompts.get(data["user_prompt"]),"r",encoding="utf-8") as sys_f:
            user_prompt = sys_f.read()
        if not msg_prompt or not user_prompt:
            return
        if (data["param_text1"] not in ["请设置参数", "无需编辑此处"]) and ("{{{text1}}}" in user_prompt):
            user_prompt = user_prompt.replace("{{{text1}}}", data["param_text1"])
        if (data["param_text2"] not in ["请设置参数", "无需编辑此处"]) and ("{{{text1}}}" in user_prompt):
            user_prompt = user_prompt.replace("{{{text2}}}", data["param_text2"])
        if (data["param_file1"] != "None") and (data["param_file1"]) and ("{{{file1}}}" in user_prompt):
            with open(dict_files_params.get(data["param_file1"]),"r",encoding="utf-8") as f1:
                text_param_file1 = f1.read()
                user_prompt = user_prompt.replace("{{{file1}}}", text_param_file1)
        if (data["param_file2"] != "None") and (data["param_file2"]) and ("{{{file2}}}" in user_prompt):
            with open(dict_files_params.get(data["param_file2"]),"r",encoding="utf-8") as f2:
                text_param_file2 = f2.read()
                user_prompt = user_prompt.replace("{{{file2}}}", text_param_file2)
        nec_msg = """
                        ``` 必须以JSON格式输出响应，不能输出其他任何信息 ```   
                        ``` 参考示例如下：```
        """
        dict_env = read_env()
        with open(dict_env.get("file_syspro_expand"), "r", encoding="utf-8") as f:
            text_file_syspro_expand = f.read()
        file_json_pptx = str([j["type"] for i, j in read_json_file(os.path.join(dict_env.get("file_json_pptx")))[data["pptx"]].items() if j["type"]])
        text_file_syspro_expand = text_file_syspro_expand.replace("{{{type_key_list}}}",file_json_pptx)
        # if ("json" in msg_prompt.lower()) and ("格式" in msg_prompt.lower()):
        #     msg_prompt = msg_prompt + "\n\n" + nec_msg
        # if ("json" in user_prompt.lower()) and ("格式" in user_prompt.lower()):
        #     user_prompt = user_prompt + "\n\n" + nec_msg
        msg_prompt = msg_prompt + "\n\n" + text_file_syspro_expand
        user_prompt = user_prompt + "\n\n" + text_file_syspro_expand
        model_res = quest_open_ai(
            api_key=(dict_json_models.get(data["models"]))["api_key"],
            base_url=(dict_json_models.get(data["models"]))["request_url"],
            modelname=data["models"],
            msg_content=msg_prompt,
            user_content=user_prompt
        )
        obj_create(model_res,dict_files_pptx.get(data["pptx"]))
    except Exception as e:
        print(e)



def obj_searchall():
    dict_env = read_env()
    dir_prompts = dict_env.get("dir_prompts")
    dir_pptx = dict_env.get("dir_pptx")
    data = {}
    dict_files_pptx = {}
    dict_files_prompts = recursive_list_files(dir_prompts)
    for filepath_name in os.listdir(dir_pptx):
        if filepath_name.endswith(".pptx"):
            dict_files_pptx[filepath_name.replace(".pptx","")] = os.path.join(dir_pptx, filepath_name)
    dict_json_models = {
        i["model_name"]: {"note_name": i["note_name"], "request_url": i["request_url"], "api_key": i["api_key"], } for i
        in view_models_curd.obj_searchall(read_env().get('file_json_models'))
    }
    dict_files_params = recursive_list_files(dict_env.get("dir_params"))
    data["dict_files_prompts"] = dict_files_prompts
    data["dict_json_models"] = dict_json_models
    data["dict_files_params"] = dict_files_params
    data["dict_files_pptx"] = dict_files_pptx
    return data



def obj_create(text_json,pptx_demo):
    json_output = json.dumps(json.loads(text_json), ensure_ascii=False, indent=2)
    print(json_output,pptx_demo)
    exit()



def obj_create_step2():
    pass



def obj_update(data):
    pass


def obj_delete(data):
    pass