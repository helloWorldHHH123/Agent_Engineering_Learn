import os
import httpx
from openai import OpenAI, APITimeoutError, APIStatusError

# Hiddify 本地代理
proxy_url = "http://127.0.0.1:12334"

# 创建 Gemini 客户端，明确指定代理和超时时间
with httpx.Client(
    proxy=proxy_url,
    timeout=60.0,
) as http_client:

    client = OpenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        http_client=http_client,
        timeout=60.0,       # 单次请求超时设置
        max_retries=1,      # 请求失败时最多自动重试一次
    )

    try:
        print("正在调用 Gemini...")

        response = client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=[
                {
                    "role": "user",
                    "content": "1+1等于多少？请简短回答。"
                }
            ]
        )

        print("模型回答：", response.choices[0].message.content)

    except APITimeoutError as e:
        print("请求超时：", repr(e))
        print("请检查 Hiddify 代理连接或 Gemini 服务状态。")

    except APIStatusError as e:
        print("HTTP 状态码：", e.status_code)
        print("服务器返回内容：", e.response.text)

    except Exception as e:
        print("其他错误：", repr(e))