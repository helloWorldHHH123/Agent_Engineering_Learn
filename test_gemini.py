import os
from openai import OpenAI, APIStatusError

# 直接调用 Gemini，不经过 Agents SDK
client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    max_retries=0,
)

# 检查 Gemini 连接和模型
try:
    print("当前 API 地址：", client.base_url)

    print("\n===== 查询可用模型 =====")
    models = client.models.list()

    for model in models:
        print(model.id)

    print("\n===== 测试文本调用 =====")
    response = client.chat.completions.create(
        model="gemini-3.8-flash",
        messages=[
            {"role": "user", "content": "1+1等于多少？"}
        ],
    )

    print("模型回答：", response.choices[0].message.content)

except APIStatusError as e:
    print("HTTP 状态码：", e.status_code)
    print("服务器返回内容：", e.response.text)

except Exception as e:
    print("错误类型：", type(e).__name__)
    print("错误信息：", str(e))