#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT_Test
@File    ：config_read.py
@Date    ：2025/7/18 16:49
@Descrip ：
'''

import json
from dotenv import load_dotenv
import os
from typing import Any, Dict, Optional




def read_env(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    读取 .env 文件并返回环境变量字典

    Args:
        env_file: .env 文件路径，默认为项目根目录下的 .env

    Returns:
        包含所有环境变量的字典，值会自动转换为 bool/int/float 类型

    Raises:
        FileNotFoundError: 指定的 .env 文件不存在
    """
    # 用于存储 .env 文件中明确设置的键
    env_vars = {}

    # 加载环境变量
    if env_file:
        if not os.path.exists(env_file):
            raise FileNotFoundError(f".env 文件不存在: {env_file}")
        load_dotenv(dotenv_path=env_file, override=True)
    else:
        load_dotenv(override=True)  # 加载默认 .env 文件

    # 从 .env 文件中读取变量
    with open(env_file or ".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # 忽略空行和注释
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # 布尔值转换
                if value.lower() == 'true':
                    env_vars[key] = True
                elif value.lower() == 'false':
                    env_vars[key] = False
                # 整数转换
                elif value.isdigit():
                    env_vars[key] = int(value)
                # 浮点数转换
                elif value.replace('.', '', 1).isdigit():
                    env_vars[key] = float(value)
                # 字符串（默认）
                else:
                    env_vars[key] = value

    return env_vars



def recursive_list_files(base_dir='./files/prompts'):
    dict_files = {}
    # 规范化路径，移除末尾斜杠
    base_dir = os.path.normpath(base_dir)
    base_len = len(base_dir) + 1  # +1 是为了包含路径分隔符
    for root, _, files in os.walk(base_dir):
        for file in files:
            # 获取完整文件路径
            full_path = os.path.join(root, file)
            # 计算相对路径（相对于base_dir）
            relative_path = full_path[base_len:]
            # 添加到结果列表
            dict_files[relative_path.split(".")[0]] = os.path.join("./",full_path)
    return dict_files




def read_json_file(file_path):
    """
    读取 JSON 文件并返回格式化的字典

    参数:
        file_path (str): JSON 文件路径

    返回:
        dict: 解析后的字典；若出错则返回 None
    """
    try:
        # 打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as f:
            # 直接转换为 Python 字典
            json_dict = json.load(f)

        return json_dict  # 返回字典供后续使用

    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 '{file_path}' 不是有效的 JSON 格式")
        return None
    except Exception as e:
        print(f"读取文件时出错：{str(e)}")
        return None
