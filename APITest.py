# -*- coding:utf-8 -*-
'''
作者：陈颖
日期：2026年11月17日
'''

import os
from openai import OpenAI

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# 调用接口
completion = client.chat.completions.create(
    model="deepseek-flash",
    # 非思考模式：temperature 可以生效
    extra_body={"thinking": {"type": "disabled"}},
    temperature = 0,
    # 流式输出，出来一点打印一点，需要结合  for chunk in completion: 这个循环
    # stream=True,
    messages=[
        {
            "role": "system",
            "content": "回复内容等于10个字"
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
)

print(completion.choices[0].message.content)

# 下面这个循环适用于流式输出 stream=True
# for chunk in completion:
#     print(chunk.choices[0].message.content, end = "")

