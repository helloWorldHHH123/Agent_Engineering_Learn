

## 1. 基本原理

通过 OpenAI SDK 调用 DeepSeek API。

## 2. Python 示例

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)
```

## 3. 注意事项

- API Key 不要直接写在公开代码中。
- 使用环境变量保存密钥。

## 4. 完整代码
```python
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

# 下面这个循环适用于流式输出 stream=True# for chunk in completion:  
#     print(chunk.choices[0].message.content, end = "")
```

- 输出为
```python
我是DeepSe
Seek最新版模型。

进程已结束，退出代码为 0
```
