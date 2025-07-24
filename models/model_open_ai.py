#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：AutoPPT
@File    ：model_open_ai.py
@Date    ：2025/7/28 16:40
@Descrip ：
'''


import time
import logging
from openai import OpenAI, OpenAIError

import time


def quest_open_ai(
    api_key="sk-rbumfkdnurenkfesivxfoqhvrcexnbndtmehpbncljvzfgxo",
    base_url="https://api.siliconflow.cn/v1",
    modelname="Qwen/Qwen3-8B",
    msg_content="",
    user_content=""
):
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=modelname,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": msg_content},
                {"role": "user", "content": user_content}
            ]
        )

        res = response.choices[0].message.content
        # 仅在响应无效时重试
        if res and isinstance(res, str) and (res not in ["[1]","[[1]]"]):
            return res
        else:
            if attempt < max_retries:
                print(f"无效响应 (尝试 {attempt}/{max_retries})，正在重试...")
                time.sleep(2)  # 简单延迟，避免立即重试
            else:
                raise ValueError(f"无效响应格式，已尝试 {max_retries} 次")
