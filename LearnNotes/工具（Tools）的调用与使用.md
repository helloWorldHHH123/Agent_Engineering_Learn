# AI Agent 核心技术：Function Calling（工具调用）

## 一、Function Calling 的基本原理

**Function Calling 是大语言模型根据用户需求，判断是否需要调用外部工具，并生成相应工具调用指令的机制。**

需要注意：**LLM 本身并不执行工具，而是由外部 Python 程序执行工具，再将结果返回给 LLM。**

## 二、Function Calling 的完整流程

以“今天上海天气如何？”为例：

**步骤 1：定义工具函数**

使用 Python 编写 `get_weather(latitude, longitude)` 函数，负责通过 Open-Meteo API 查询指定经纬度的实时温度。

**步骤 2：向大模型描述工具**

通过 `tools` 列表向模型提供工具信息，包括：

- `name`：工具名称，例如 `get_weather`。
    
- `description`：工具的功能描述。
    
- `parameters`：工具需要的参数及其数据类型。
    
- `required`：指定必需参数。
    

工具描述采用 JSON Schema 格式，让模型知道有哪些工具可以使用、什么时候使用以及需要提供什么参数。

**步骤 3：用户提出问题**

用户输入：“今天上海天气如何？”

程序通过 `get_completion()` 函数，将用户消息加入 `message_history`，并调用大模型 API。

**步骤 4：大模型决定调用工具**

模型分析用户请求，判断需要使用 `get_weather` 工具，并返回工具调用信息：

- `function.name`：需要调用的工具名称。
    
- `function.arguments`：调用工具所需的参数。
    
- `tool_call_id`：本次工具调用的唯一标识。
    

注意：此时模型只是生成了调用请求，尚未真正执行工具。

**步骤 5：解析并执行工具**

Python 程序提取模型返回的参数：

```
func_call_id = message['tool_calls'][0].id

func_kwargs = json.loads(
    message['tool_calls'][0].function.arguments
)
```

其中：

- `tool_calls[0]`：获取第一个工具调用。
    
- `json.loads()`：将 JSON 字符串转换为 Python 字典。
    
- `func_kwargs`：保存工具参数。
    

然后执行：

```
func_result = get_weather(**func_kwargs)
```

这里的 `**` 用于将字典展开为函数的关键字参数。

工具函数向天气 API 发送请求，获取实际温度数据。

**步骤 6：将工具结果返回给大模型**

```
message = get_completion({
    "role": "tool",
    "tool_call_id": func_call_id,
    "content": str(func_result)
})
```

其中：

- `role="tool"`：表示这是一条工具返回的消息。
    
- `tool_call_id`：将结果关联到对应的工具调用。
    
- `content`：传递工具实际执行的结果。
    

**步骤 7：大模型生成最终回答**

模型接收到工具结果后，再次进行推理并生成自然语言回复。

例如：“今天上海的气温是 12.3℃。”

这里的温度仅是原网页中的运行示例，不代表当前天气。

## 三、完整流程总结

```
用户提出问题
      ↓
将用户消息加入历史记录
      ↓
调用 LLM API（传入 tools）
      ↓
LLM 判断是否需要调用工具
      ↓
LLM 返回工具名称和参数
      ↓
Python 解析工具调用信息
      ↓
Python 执行对应工具函数
      ↓
工具访问外部 API 获取数据
      ↓
将工具结果加入历史记录
      ↓
再次调用 LLM API
      ↓
LLM 根据工具结果生成最终回答
```

## 四、核心代码的作用

| 核心代码                               | 作用                      |
| ---------------------------------- | ----------------------- |
| `tools = [...]`                    | 定义模型可以使用的工具             |
| `message_history.append(message)`  | 保存对话历史                  |
| `client.chat.completions.create()` | 向大模型发送请求                |
| `message['tool_calls'][0]`         | 获取模型请求的第一个工具调用          |
| `.function.arguments`              | 获取工具调用参数                |
| `json.loads()`                     | 将 JSON 字符串转换为 Python 对象 |
| `get_weather(**func_kwargs)`       | 真正执行 Python 工具函数        |
| `"role": "tool"`                   | 将工具执行结果反馈给大模型           |

## 五、Function Calling 的核心作用

1. **扩展模型能力**：让 LLM 获取天气、数据库等外部实时信息。
    
2. **执行外部操作**：通过 Python 函数完成计算、查询等具体任务。
    
3. **实现工具协作**：让模型负责选择工具和生成参数，程序负责实际执行。
    
4. **支持复杂 Agent**：为多步骤任务执行提供基础。
    

## 六、总结

Function Calling 的本质是：

**LLM 负责决策和生成工具调用指令，Python 程序负责执行工具，最后由 LLM 根据工具返回结果生成回答。**

整个过程中涉及两次主要的大模型调用：

- 第一次：模型分析问题，决定是否调用工具，并生成工具调用参数。
    
- 第二次：模型接收工具结果，生成最终回答。
    

这使 AI Agent 从只能进行文本交互的系统，扩展为能够调用外部工具、获取实时信息和执行任务的系统。

## 七、完整可运行的python代码
```python
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
        # temperature = 0,        model = "deepseek-flash",  
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
# message   大模型返回的消息  
# ['tool_calls']    获取模型请求调用的工具列表  
# [0]   选择第一个工具调用  
# .function 获取该工具的函数调用信息  
# .arguments    获取模型生成的函数参数（JSON 字符串）  
# json.loads()  将 JSON 字符串转换为 Python 对象，这里通常是字典  
# func_kwargs   保存转换后的函数参数  
func_kwargs = json.loads(message['tool_calls'][0].function.arguments)  
#调用函数  
func_result = get_weather(**func_kwargs)  
  
print("")  
# 6. 将工具执行的结果返回给大模型，让大模型根据工具结果继续生成回答。  
# get_completion()  你自己定义的函数，用于调用大模型 API# "role": "tool"    告诉模型，这条消息来自工具，而不是用户  
# "tool_call_id": func_call_id  指明这条结果对应哪一次工具调用  
# "content": str(func_result)   将工具运行结果转换为字符串，发送给模型  
# message = ... 接收 get_completion() 函数返回的结果  
message = get_completion({"role": "tool","tool_call_id":func_call_id,"content": str(func_result)})  
print(message)      # LLM返回工具调用信息
```

- 输出
```python
{'content': '', 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': [ChatCompletionMessageFunctionToolCall(id='call_00_ZBdIzUHm8qBurQcBFhq44516', function=Function(arguments='{"latitude": 31.23, "longitude": 121.47}', name='get_weather'), type='function', index=0)], 'reasoning_content': 'The user asks about Shanghai weather today. I need coordinates for Shanghai: 31.23, 121.47.'}

{'content': '上海当前气温约 **15.5℃**。\n\n这个工具只返回温度，不包含天气状况（晴、雨）或风力、湿度等信息。如果你需要更完整的天气详情，可以查看天气应用或气象台网站。要我帮你查其他城市的温度吗？', 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': None, 'reasoning_content': ''}

进程已结束，退出代码为 0

```
---

参考资料：[Function Call 教程](https://supermeok.github.io/2025/11/12/Function-Call/)