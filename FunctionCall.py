import os
from openai import OpenAI
import httpx
import json

# 0. 建立与大模型服务端的通信连接：配置大模型 API 接口地址和 API 密钥，以便后续向大模型服务器发送请求并获取模型响应。
# 需要在pycharm中编辑配置文件，设置这个函数所需要的的API密钥
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# 工具定义与使用：Function Call实现天气查询
# 1. 定义工具函数：天气查询函数
# get_weather函数调用Open-Meteo API（外部服务），根据经纬度获取当前温度。
def get_weather(latitude, longitude):
    """根据经纬度获取实时摄氏温度"""
    response = httpx.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m'
    )
    data = response.json()
    return f"{data['current']['temperature_2m']}℃"

# 2. 工具描述函数
# name：函数名，与代码中的函数一致。
# description：描述函数用途。
# parameters：指定参数类型和必需字段，要求latitude和longitude为数字。
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "根据指定坐标提供当地摄氏温度",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# 3. 封装LLM
# 使用变量保存历史记录
message_history = []
# 4. 发送消息给大模型，并自动保存记录
def get_completion(message):
    #用户提问加入历史记录
    message_history.append(message)
    # 调用LLM接口
    response = client.chat.completions.create(
        # 非思考模式：temperature 可以生效
        # extra_body={"thinking": {"type": "disabled"}},
        # temperature = 0,
        model = "deepseek-flash",
        messages = message_history,
        tools = tools,
    )
    response_dict = dict(response.choices[0].message)
    #大模型回答加入记录
    message_history.append(response_dict)
    return response_dict

# 5. 调用LLM接口，获取工具调用结果信息
message = get_completion({"role": "user","content": "今天上海天气如何"})
#LLM返回工具调用信息
print(message)
# 解析工具调用ID和参数，执行函数获取结果
# 发送工具结果回模型，获取最终响应
func_call_id = message['tool_calls'][0].id
# 从大模型返回的工具调用请求中，提取第一个工具的参数，并将 JSON 字符串转换成 Python 字典。
# message	大模型返回的消息
# ['tool_calls']	获取模型请求调用的工具列表
# [0]	选择第一个工具调用
# .function	获取该工具的函数调用信息
# .arguments	获取模型生成的函数参数（JSON 字符串）
# json.loads()	将 JSON 字符串转换为 Python 对象，这里通常是字典
# func_kwargs	保存转换后的函数参数
func_kwargs = json.loads(message['tool_calls'][0].function.arguments)
#调用函数
func_result = get_weather(**func_kwargs)

print("")
# 6. 将工具执行的结果返回给大模型，让大模型根据工具结果继续生成回答。
# get_completion()	你自己定义的函数，用于调用大模型 API
# "role": "tool"	告诉模型，这条消息来自工具，而不是用户
# "tool_call_id": func_call_id	指明这条结果对应哪一次工具调用
# "content": str(func_result)	将工具运行结果转换为字符串，发送给模型
# message = ...	接收 get_completion() 函数返回的结果
message = get_completion({"role": "tool","tool_call_id":func_call_id,"content": str(func_result)})
print(message)      # LLM返回工具调用信息