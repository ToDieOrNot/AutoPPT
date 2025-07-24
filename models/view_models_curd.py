#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：view_models_curd.py
@Date    ：2025/7/22 13:52
@Descrip ：
'''


from models.config_read import read_env
import json



def save_models(models,MODELS_FILE = read_env().get('file_json_models')):
    """保存模型数据到JSON文件"""
    with open(MODELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(models, f, ensure_ascii=False, indent=2)


def obj_searchall(MODELS_FILE = read_env().get('file_json_models')):
    try:
        with open(MODELS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def obj_create(data):
    models = obj_searchall()
    models.append({
        "note_name": data['note_name'],
        "model_name": data['model_name'],
        "request_url": data['request_url'],
        "api_key": data['api_key']
    })
    save_models(models)
    return models

def obj_update(index,data):
    models = obj_searchall()
    models[index] = data
    save_models(models)
    return models

def obj_delete(index):
    models = obj_searchall()
    del models[index]
    save_models(models)
    return models
