# <span style="color: #E57373;">1. OpenAI Agents SDK：结构化输出（Structured Output）</span>

## 一、代码功能

代码利用 **Pydantic 的** **BaseModel** **定义数据结构，并通过 Agent 的** **output_type=Data** **指定输出格式**，让大模型按照规定的字段返回人物信息。

核心功能：

**定义数据结构 → 创建 Agent → 指定结构化输出 → 异步调用模型 → 获取 Data 对象 → 访问对象属性 → 获取完整对话记录。**

## 二、核心代码解析

### 1. 定义结构化数据模型

```
class Data(BaseModel):
    名字: str
    年龄: int
    性别: str
    事迹: str
```

- `BaseModel`：Pydantic 提供的数据模型基类。
    
- `Data`：自定义数据结构。
    
- `str`、`int`：指定各字段的数据类型。
    
- Pydantic 负责验证返回数据是否符合结构要求。
    

### 2. 创建 Agent 并指定输出结构

```
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文回答。",
    model="deepseek-flash",
    output_type=Data,
)
```

**关键代码：**`**output_type=Data**`

作用：告诉 OpenAI Agents SDK，最终结果应该符合 `Data` 定义的数据结构。

SDK 会根据 `Data` 生成 JSON Schema，向模型请求结构化结果，并尝试自动解析和验证。

### 3. 异步运行 Agent

```
result = await Runner.run(agent, '介绍一位值得记住的人？')
```

- `Runner.run()`：启动 Agent 执行任务。
    
- `await`：异步等待运行完成。
    
- `result`：保存 Agent 的运行结果。
    

### 4. 获取结构化输出对象

```
obj: Data = result.final_output
```

执行成功且结构化输出被正确解析后，`result.final_output` 是 `Data` 对象。

其中 `obj: Data` 是 Python 类型标注，本身不会执行数据转换。

### 5. 直接访问对象属性

```
print(obj.名字)
print(obj.性别)
print(obj.事迹)
```

可以通过 `.` 直接访问结构化字段，不需要自己使用 `json.loads()` 解析 JSON 字符串。

### 6. 获取完整对话记录

```
print("完整的对话记录：", result.to_input_list())
```

`result.to_input_list()` 将本次运行的输入及输出转换为消息列表，方便后续查看和管理对话历史，也可以用于下一轮对话。

## 三、核心处理流程

```
程序启动
    ↓
加载 DeepSeek API 配置
    ↓
定义 Data(BaseModel)
指定名字、年龄、性别、事迹
    ↓
创建 Agent
设置 output_type=Data
    ↓
await Runner.run(agent, 用户问题)
    ↓
Agents SDK 根据 Data 生成输出约束
    ↓
调用 DeepSeek 模型
    ↓
模型生成结构化人物信息
    ↓
Agents SDK 解析并验证输出
    ↓
result.final_output
返回 Data 对象
    ↓
obj.名字 / obj.性别 / obj.事迹
直接获取字段
    ↓
result.to_input_list()
获取本次完整对话记录
```

## 四、核心知识点

|代码|作用|
|---|---|
|`BaseModel`|定义并验证数据结构|
|`output_type=Data`|指定 Agent 的结构化输出类型|
|`await Runner.run()`|异步运行 Agent|
|`result.final_output`|获取最终结构化结果|
|`obj.名字`|直接访问 Data 对象的字段|
|`result.to_input_list()`|获取本次运行的完整对话记录|

## 五、注意事项

`output_type=Data` 依赖模型 API 支持相应的结构化输出格式。

例如，之前 DeepSeek 的 Chat Completions 接口返回过：

```
400 - This response_format type is unavailable now
```

因此，代码能否正常运行，还取决于当前使用的 DeepSeek API 接口及其结构化输出兼容性。

此外，`result.to_input_list()` 获取的是本次运行的消息记录，不代表自动保存了长期记忆。

## 六、一句话总结

**结构化输出的核心思想：使用** `**BaseModel**` **定义数据结构，通过** `**Agent(output_type=Data)**` **约束模型输出，再利用** `**result.final_output**` **获取经过解析和验证的对象，最后通过** `**obj.字段名**` **直接访问数据。**

## 七、完整代码与运行结果

```python
from pydantic import BaseModel  
import asyncio  
from agents import Agent, Runner  
import async_local_settinngs  # 加载本地设置  
  
class Data(BaseModel):  
    名字: str  
    年龄: int  
    性别: str  
    事迹: str  
  
# 也可以放到 async def main() 函数里面  
agent = Agent(  
    name="AI助手",  
    instructions="你是一个友好的AI助手，使用中文回答。",  # 系统提示词  
    model="deepseek-flash",  # 明确指定DeepSeek模型  
    output_type=Data,   # 指定输出结构  
)  
  
async def main():  
    result = await Runner.run(agent, '介绍一位值得记住的人？')     # 异步写法  
    obj: Data = result.final_output  
    print(result.final_output)  
    print(obj.名字)  
    print(obj.性别)  
    print(obj.事迹)  
    print("完整的对话记录：", result.to_input_list())  
  
if __name__ == '__main__':  
    # 异步启动  
    asyncio.run(main())
```

**运行结果**

```python
名字='袁隆平' 年龄=91 性别='男' 事迹='中国杂交水稻育种专家，被誉为“杂交水稻之父”。他长期致力于水稻高产研究，推动杂交水稻技术应用与推广，帮助大幅提高粮食产量，为解决中国乃至世界的粮食安全问题作出了重要贡献。他朴实、执着、心怀苍生的精神值得被记住。'
袁隆平
男
中国杂交水稻育种专家，被誉为“杂交水稻之父”。他长期致力于水稻高产研究，推动杂交水稻技术应用与推广，帮助大幅提高粮食产量，为解决中国乃至世界的粮食安全问题作出了重要贡献。他朴实、执着、心怀苍生的精神值得被记住。
完整的对话记录： [{'content': '介绍一位值得记住的人？', 'role': 'user'}, {'id': 'cbedc3a7-907c-4d15-99f4-01e1dfe8c15d', 'summary': [], 'type': 'reasoning', 'content': [{'text': '我们需要回答中文，必须严格adhere schema JSON object with fields 名字 年龄 性别 事迹. Need introduce a memorable person. Choose maybe 张桂梅? Age integer current? Born 1957, age maybe 68 (as of 2025). But uncertain. Could choose 袁隆平 age at death? Schema says 年龄 integer, can be age at death? Need be clear in 事迹. Maybe use "年龄": 91 (袁隆平享年91). 性别 男. 事迹 describe. Or "张桂梅" age 68? Current 2026? But safe use historical person with known age: 袁隆平 (1930-2021) 享年91. 名字 袁隆平, 年龄 91, 性别 男, 事迹: 中国杂交水稻之父...值得记住. Need only JSON, no markdown. Ensure valid.', 'type': 'reasoning_text'}], 'encrypted_content': 'c70bd757-d4a8-48f2-89b5-184a62b4e7ed-0', 'status': 'completed'}, {'id': 'b1b0dbe4-9f4b-4dc1-8605-407134412c9f', 'content': [{'annotations': [], 'text': '{"名字":"袁隆平","年龄":91,"性别":"男","事迹":"中国杂交水稻育种专家，被誉为“杂交水稻之父”。他长期致力于水稻高产研究，推动杂交水稻技术应用与推广，帮助大幅提高粮食产量，为解决中国乃至世界的粮食安全问题作出了重要贡献。他朴实、执着、心怀苍生的精神值得被记住。"}', 'type': 'output_text', 'logprobs': []}], 'role': 'assistant', 'status': 'completed', 'type': 'message', 'phase': 'final_answer'}]

进程已结束，退出代码为 0
```

# <span style="color: #E57373;">2. 工具使用</span>

## <span style="color: #81C784;">OpenAI Agents SDK：Function Tool 工具调用</span>
## 一、代码功能

代码使用 OpenAI Agents SDK 的 `@function_tool` 装饰器，将普通 Python 函数转换为 Agent 可以调用的工具，并通过 DeepSeek 模型完成用户任务。

**核心功能：定义工具 → 注册工具 → 创建 Agent → 用户提问 → Agent 调用工具 → 返回结果。**

## 二、核心代码解析

### 1. 定义并注册工具

```
@function_tool
def get_weather(city_name):
    return "23.5℃"
```

- `@function_tool`：将普通 Python 函数注册为 Agent 可以识别和调用的工具。
    
- `get_weather()`：定义天气查询函数。
    
- `city_name`：接收城市名称。
    
- `return "23.5℃"`：返回固定温度，属于模拟数据，并非真实天气。
    

**关键：**`**@function_tool**` **将普通 Python 函数转换为 Agent 工具，供大模型按需调用。**

注意：实际使用时，建议给函数添加参数类型和文档字符串，便于 SDK 生成工具定义。

### 2. 创建 Agent 并绑定工具

```
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文回答。",
    model="deepseek-flash",
    tools=[get_weather],
)
```

- `Agent()`：创建智能体。
    
- `instructions`：指定系统提示词。
    
- `model`：指定 DeepSeek 模型。
    
- `tools=[get_weather]`：将天气查询工具提供给 Agent。
    

### 3. 异步调用 Agent

```
result = await Runner.run(agent, '今天上海天气如何？')
print(result.final_output)
```

- `Runner.run()`：启动 Agent 处理用户问题。
    
- `await`：异步等待执行完成。
    
- `result.final_output`：获取 Agent 最终生成的回答。
    

## 三、核心处理流程

```
程序启动
    ↓
加载 DeepSeek API 配置
    ↓
@function_tool
注册 get_weather() 工具
    ↓
Agent(tools=[get_weather])
创建 Agent 并绑定工具
    ↓
Runner.run(agent, 用户问题)
    ↓
用户提问：今天上海天气如何？
    ↓
Agent 将问题及可用工具信息发送给 LLM
    ↓
LLM 判断是否需要调用工具
    ↓
若决定调用 get_weather(city_name="上海")
    ↓
Agents SDK 执行 Python 函数
    ↓
工具返回 "23.5℃"
    ↓
工具结果传回 LLM
    ↓
LLM 根据工具结果生成回答
    ↓
result.final_output
输出最终结果
```

## 四、核心知识点

|代码|作用|
|---|---|
|`@function_tool`|将 Python 函数注册为 Agent 工具|
|`get_weather(city_name)`|定义工具的具体功能和输入参数|
|`tools=[get_weather]`|将工具绑定到 Agent|
|`Runner.run()`|运行 Agent，协调模型与工具调用|
|`result.final_output`|获取 Agent 最终回答|

## 五、注意事项

1. **工具不会自动执行**：大模型根据用户问题决定是否调用工具。
    
2. **模型负责决策，Python 负责执行**：大模型选择工具和参数，SDK 调用本地函数。
    
3. **当前温度是模拟数据**：`get_weather()` 固定返回 `23.5℃`，不具备真实天气查询能力。
    
4. **工具信息需要明确**：最好为工具函数添加类型注解和文档字符串，便于模型理解和调用。
    

## 六、一句话总结

**Function Tool 的核心机制是：通过** `**@function_tool**` **将 Python 函数注册为 Agent 工具，再通过** `**tools=[...]**` **提供给 Agent，由大模型决定是否调用，SDK 执行工具并把结果返回给模型，最终生成回答。**

## 七、完整代码与运行结果

```python
import os  
from openai import OpenAI  
import httpx  
import asyncio  
from agents import Agent, Runner, function_tool  
import async_local_settinngs  
  
# 用 @function_tool 把函数转成agent可以识别的工具  
@function_tool  
def get_weather(city_name):  
    # """根据城市获取实时摄氏温度"""  
  
    return f"23.5℃"  
  
# 也可以放到 async def main() 函数里面  
agent = Agent(  
    name="AI助手",  
    instructions="你是一个友好的AI助手，使用中文回答。",  # 系统提示词  
    model="deepseek-flash",  # 明确指定DeepSeek模型  
    tools= [get_weather,]  
)  
  
async def main():  
    result = await Runner.run(agent, '今天上海天气如何？')     # 异步写法  
    print(result.final_output)  
  
if __name__ == '__main__':  
    # 异步启动  
    asyncio.run(main())
```

**运行结果**

```python
今天上海的气温大约是 **23.5℃**，体感比较舒适。不过目前获取到的信息只有温度这一项，具体的天气状况（晴雨、风力、湿度等）暂时没有数据。

如果您需要更详细的信息（比如降水概率、穿衣建议），可以告诉我，我再帮您看看。另外，出门前建议再确认一下实时天气预报，以防天气变化。😊

进程已结束，退出代码为 0
```
# <span style="color: #E57373;">3. MCP服务及其使用</span>

## <span style="color: #81C784;">MCP Server：创建服务器与注册工具</span>
## 一、代码功能

代码使用 MCP Python SDK 创建一个 MCP Server，并通过 `@mcp.tool()` 将普通 Python 函数注册为 MCP 工具，供 MCP Client 或 Agent 调用。

**核心功能：创建 MCP 服务器 → 注册工具 → 启动服务器 → 等待客户端调用 → 执行工具并返回结果。**

## 二、核心代码解析

### 1. 创建 MCP Server

```
from mcp.server import MCPServer

mcp = MCPServer("MCP Demo")
```

- `MCPServer`：MCP SDK 提供的服务器类。
    
- `"MCP Demo"`：服务器名称。
    
- `mcp`：创建的 MCP 服务器实例。
    

### 2. 注册 MCP 工具

```
@mcp.tool()
def ls():
    """列出目录中的文件名"""
    return os.listdir(".")
```

- `@mcp.tool()`：装饰器，将 `ls()` 函数注册为 MCP 工具。
    
- `ls()`：工具名称。
    
- `"""列出目录中的文件名"""`：工具的功能描述，可帮助客户端和 Agent 理解工具用途。
    
- `os.listdir(".")`：获取当前工作目录中的文件和文件夹名称，以列表形式返回。
    

**关键：**`**@mcp.tool()**` **使普通 Python 函数能够作为 MCP 工具对外提供服务。**

### 3. 启动 MCP Server

```
if __name__ == "__main__":
    mcp.run()
```

- `if __name__ == "__main__"`：判断程序是否直接运行。
    
- `mcp.run()`：启动 MCP Server，处理客户端发来的协议请求。
    

本示例使用 stdio 通信方式时，也可以明确写成 `mcp.run(transport="stdio")`。

## 三、核心处理流程

```
启动 MCP_Server.py
        ↓
导入 os 和 MCPServer
        ↓
MCPServer("MCP Demo")
创建 MCP 服务器实例
        ↓
@mcp.tool()
注册 ls() 工具
        ↓
mcp.run()
启动 MCP Server
        ↓
等待 MCP Client 连接
        ↓
客户端获取工具列表
        ↓
Agent 决定调用 ls()
        ↓
MCP Client 发送工具调用请求
        ↓
MCP Server 执行 ls()
        ↓
os.listdir(".")
获取当前目录的文件列表
        ↓
MCP Server 返回工具结果
        ↓
Agent 使用结果回答用户
```

## 四、核心知识点

|代码|作用|
|---|---|
|`MCPServer()`|创建 MCP 服务器|
|`@mcp.tool()`|注册 MCP 工具|
|`def ls()`|定义工具的具体功能|
|`os.listdir(".")`|获取当前目录的文件列表|
|`mcp.run()`|启动 MCP 服务器|

## 五、注意事项

1. **MCP Server 不等于 Agent**：Server 负责提供工具，Agent 负责决定何时调用工具。
    
2. **工具需要注册**：通过 `@mcp.tool()` 将 Python 函数暴露给 MCP 客户端。
    
3. **当前目录**：`os.listdir(".")` 中的 `"."` 表示程序的当前工作目录，不一定是服务器脚本所在的目录。
    
4. **Python 环境一致**：在 Windows + Conda 环境中，MCP Client 启动本地服务器时建议使用 `sys.executable`，避免 Python 环境不一致。
    
5. **stdio 通信**：服务器通过标准输入和标准输出与客户端交换协议消息，避免使用普通 `print()` 向标准输出写入调试信息。
    

## 六、一句话总结

**MCP Server 的核心作用是把普通 Python 函数注册为标准化工具，通过 MCP 协议提供给客户端，使 Agent 能够发现、调用这些工具并利用返回结果完成任务。**

## 七、完整代码及运行结果

```python
import os  # 导入 Python 内置的 os 模块，用于操作文件和目录  
  
from mcp.server import MCPServer  # 从 MCP SDK 中导入 MCPServer 类  
  
# 创建 MCP 服务器实例，服务器名称为 MCP Demomcp = MCPServer("MCP Demo")  
  
# 使用装饰器，将下面的 ls 函数注册为 MCP 工具  
@mcp.tool()  
def ls():  # 定义 ls 函数，用于获取当前目录中的文件名  
    """列出目录中的文件名"""  # 函数文档字符串，描述工具的功能  
  
    # 获取当前工作目录中的文件和文件夹名称，并以列表形式返回  
    return os.listdir(".")  
  
# 判断当前 Python 文件是否作为主程序直接运行  
if __name__ == '__main__':  
    # 启动 MCP 服务器，等待客户端连接并调用工具  
    mcp.run()
```

## <span style="color: #81C784;">OpenAI Agents SDK：MCP Client 调用 MCP Server</span>
## 一、代码功能

代码通过 `MCPServerStdio` 启动本地 MCP Server，将 MCP 工具和普通 Python 工具一起提供给 Agent，再使用 DeepSeek 模型完成用户任务。

**核心功能：启动 MCP Server → 建立连接 → 获取 MCP 工具 → 创建 Agent → 调用工具 → 返回结果。**

## 二、核心代码解析

### 1. 定义普通 Python 工具

```
@function_tool
def get_weather(city_name):
    return "23.5℃"
```

- `@function_tool`：把普通 Python 函数注册为 Agent 可调用的工具。
    
- `get_weather()`：示例天气查询工具，固定返回 `23.5℃`，并非真实天气。
    

### 2. 启动 MCP Server

```
async with MCPServerStdio(
    name="普通的mcp服务器",
    params={
        "command": sys.executable,
        "args": ["MCP_Server.py"],
    }
) as mcp_server:
```

- `MCPServerStdio`：通过标准输入输出（stdio）与本地 MCP Server 通信。
    
- `command`：指定启动服务器使用的 Python 解释器。
    
- `sys.executable`：获取当前程序运行的 Python 路径，确保使用相同的 Conda 环境。
    
- `args`：指定要运行的 MCP Server 脚本。
    
- `async with`：异步建立连接，退出代码块时自动关闭连接。
    

**关键：**`**sys.executable**` **避免 MCP Client 和 MCP Server 使用不同的 Python 环境，从而导致连接失败。**

### 3. 创建 Agent 并绑定工具

```
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文回答。",
    model="deepseek-flash",
    tools=[get_weather],
    mcp_servers=[mcp_server],
)
```

这里有两种工具接入方式：

|参数|作用|
|---|---|
|`tools=[get_weather]`|将普通 Python 工具提供给 Agent|
|`mcp_servers=[mcp_server]`|将 MCP Server 提供给 Agent，使其能够发现和调用 MCP 工具|

两种工具可以同时使用。

### 4. 运行 Agent

```
result = await Runner.run(agent, '当前目录有几个文件？')
print(result.final_output)
```

- `Runner.run()`：异步启动 Agent。
    
- Agent 根据问题决定是否调用 MCP 工具。
    
- MCP Server 中的 `ls()` 工具可以返回当前目录的文件及文件夹名称。
    
- Agent 根据工具结果回答用户。
    

注意：`Runner.run()` 必须位于 `async with` 代码块内部，确保调用工具时 MCP 连接仍然有效。

## 三、核心处理流程

```
启动 MCPUse.py
        ↓
加载 DeepSeek API 配置
        ↓
@function_tool
注册普通 Python 工具 get_weather
        ↓
MCPServerStdio()
创建 MCP 客户端连接
        ↓
sys.executable
使用当前 Conda 环境中的 Python
        ↓
启动 MCP_Server.py
        ↓
建立 MCP Client ↔ MCP Server 连接
        ↓
Agent(
    tools=[get_weather],
    mcp_servers=[mcp_server]
)
将两类工具提供给 Agent
        ↓
Runner.run(agent, "当前目录有几个文件？")
        ↓
Agent 发现并选择 MCP 工具 ls()
        ↓
MCP Client 向 MCP Server 发送调用请求
        ↓
MCP Server 执行 os.listdir(".")
        ↓
返回目录中的文件和文件夹列表
        ↓
Agent 根据工具结果统计数量
        ↓
result.final_output
输出最终回答
        ↓
退出 async with
自动关闭 MCP Server 连接
```

## 四、核心知识点

|代码|作用|
|---|---|
|`@function_tool`|将本地 Python 函数注册为 Agent 工具|
|`MCPServerStdio()`|启动并连接本地 MCP Server|
|`sys.executable`|使用当前 Python 解释器|
|`async with`|管理 MCP 连接生命周期|
|`tools=[...]`|提供普通 Python 工具|
|`mcp_servers=[...]`|提供 MCP 服务器中的工具|
|`Runner.run()`|运行 Agent，让其选择和调用工具|
|`result.final_output`|获取 Agent 的最终回答|

## 五、MCP Server 与 MCP Client 的区别

- **MCP Server（**`**MCP_Server.py**`**）**：负责定义、注册和执行工具，例如 `ls()`。
    
- **MCP Client（**`**MCPUse.py**`**）**：负责启动或连接 MCP Server，获取工具并提供给 Agent。
    
- **Agent**：根据用户问题判断是否需要调用工具，并利用工具结果生成回答。
    

## 六、注意事项

1. `sys.executable` 可以避免 Windows + Conda 环境中使用错误的 Python 解释器。
    
2. MCP Server 的脚本路径必须正确；`"MCP_Server.py"` 是相对于当前工作目录解析的。
    
3. `Runner.run()` 必须在 `async with` 内执行，避免 MCP 连接提前关闭。
    
4. `get_weather()` 是普通工具，`ls()` 是 MCP 工具，两者采用不同的注册方式。
    
5. `os.listdir(".")` 返回当前工作目录中的文件和文件夹名称，统计结果可能同时包含文件夹。
    

## 七、完整代码及运行结果

```python
import os  
from openai import OpenAI  
import httpx  
import asyncio  
from agents import Agent, Runner, function_tool  
import async_local_settinngs  
from agents.mcp import MCPServerStdio  
import sys  
  
# 1. 启动MCPServer  
# 2. 从MCPServer获取支持的工具，重点  
# 3. 把工具传递给agent  
  
# 用 @function_tool 把函数转成agent可以识别的工具  
@function_tool  
def get_weather(city_name):  
    # """根据城市获取实时摄氏温度"""  
  
    return f"23.5℃"  
  
async def main():  
    # 1. 启动MCPServer  
    # 2. 把MCPServer变相地传给agent（从MCPServer获取支持的工具  把工具传递给agent）  
    async with MCPServerStdio(  
            name="普通的mcp服务器",  
            params={  
                # 实际上等价于："command": r" 当前conda环境下的python.exe",  
                "command": sys.executable,  
                "args": ["MCP_Server.py"],  
            }  
    ) as mcp_server:  
        agent = Agent(  
            name="AI助手",  
            instructions="你是一个友好的AI助手，使用中文回答。",  # 系统提示词  
            model="deepseek-flash",  # 明确指定DeepSeek模型  
            tools=[get_weather, ],  
            mcp_servers =[mcp_server,],  
        )  
        result = await Runner.run(agent, '当前目录有几个文件？')     # 异步写法  
        print(result.final_output)  
  
if __name__ == '__main__':  
    # 异步启动  
    asyncio.run(main())
```

**运行结果**
```python
当前目录共有 **23 个条目**，其中 **20 个是文件**、**3 个是文件夹**（`.idea`、`MyNotes`、`__pycache__`）。

文件清单：
1. AIAgent.png
2. AIAgent2.png
3. APITest.py
4. async.py
5. AsyncGrammer.py
6. async_local_settinngs.py
7. errorTest.py
8. flowOutput.py
9. FunctionCall.py
10. gemini_settings.py
11. install_agent_packages.bat
12. MCPUse.py
13. MCP_Server.py
14. Memory.py
15. multimodal.py
16. multiturnSession.py
17. ReactAgent.py
18. structuredOutput.py
19. test_gemini.py
20. UseTools.py

进程已结束，退出代码为 0

```

## 八、一句话总结

**MCP 工具调用的核心机制是：通过** `**MCPServerStdio**` **启动并连接 MCP Server，再使用** `**mcp_servers=[mcp_server]**` **将服务器提供的工具交给 Agent，由 Agent 根据用户问题自动选择工具、执行操作并返回结果。**
# <span style="color: #E57373;">4. 多Agent编排</span>

未学，有时间再看吧。。。

# <span style="color: #FFD54F;">5. Obsidian 常用颜色代码</span>

## 一、HEX 十六进制颜色

HEX 颜色使用 `#RRGGBB` 格式表示。

例如：

```
color: #E57373;
```

其中：

- `RR`：红色分量
    
- `GG`：绿色分量
    
- `BB`：蓝色分量
    

## 二、常用颜色代码表

| 颜色名称 | HEX 代码    | 颜色预览                                          |
| ---- | --------- | --------------------------------------------- |
| 柔和红  | `#E57373` | <span style="color: #E57373;">■■■■■ 红色</span> |
| 粉红色  | `#F48FB1` | <span style="color: #F48FB1;">■■■■■ 粉色</span> |
| 橙色   | `#FFB74D` | <span style="color: #FFB74D;">■■■■■ 橙色</span> |
| 黄色   | `#FFD54F` | <span style="color: #FFD54F;">■■■■■ 黄色</span> |
| 浅绿色  | `#81C784` | <span style="color: #81C784;">■■■■■ 浅绿</span> |
| 青绿色  | `#4DB6AC` | <span style="color: #4DB6AC;">■■■■■ 青绿</span> |
| 浅蓝色  | `#64B5F6` | <span style="color: #64B5F6;">■■■■■ 浅蓝</span> |
| 深蓝色  | `#1976D2` | <span style="color: #1976D2;">■■■■■ 深蓝</span> |
| 紫色   | `#BA68C8` | <span style="color: #BA68C8;">■■■■■ 紫色</span> |
| 灰色   | `#9E9E9E` | <span style="color: #9E9E9E;">■■■■■ 灰色</span> |
| 白色   | `#FFFFFF` | <span style="color: #FFFFFF;">■■■■■ 白色</span> |
| 黑色   | `#000000` | <span style="color: #000000;">■■■■■ 黑色</span> |

## 三、在 Obsidian 中设置文字颜色

### 1. 红色文字

```
<span style="color: #E57373;">这是红色文字</span>
```

### 2. 蓝色文字

```
<span style="color: #64B5F6;">这是蓝色文字</span>
```

### 3. 绿色文字

```
<span style="color: #81C784;">这是绿色文字</span>
```

### 4. 橙色文字

```
<span style="color: #FFB74D;">这是橙色文字</span>
```

### 5. 紫色文字

```
<span style="color: #BA68C8;">这是紫色文字</span>
```

## 四、Obsidian 学习笔记推荐配色

|学习内容|推荐颜色|颜色代码|
|---|---|---|
|错误、警告、注意事项|红色|`#E57373`|
|函数、API、基础概念|蓝色|`#64B5F6`|
|正确结果、成功执行|绿色|`#81C784`|
|重点说明、核心参数|橙色|`#FFB74D`|
|核心原理、处理流程|紫色|`#BA68C8`|
|一般备注、补充信息|灰色|`#9E9E9E`|

## 五、快速复制区

```
/* 红色 */ color: #E57373;
/* 粉色 */ color: #F48FB1;
/* 橙色 */ color: #FFB74D;
/* 黄色 */ color: #FFD54F;
/* 浅绿 */ color: #81C784;
/* 青绿 */ color: #4DB6AC;
/* 浅蓝 */ color: #64B5F6;
/* 深蓝 */ color: #1976D2;
/* 紫色 */ color: #BA68C8;
/* 灰色 */ color: #9E9E9E;
/* 白色 */ color: #FFFFFF;
/* 黑色 */ color: #000000;
```

**总结：** HEX 颜色代码可用于 Obsidian 中的 HTML 行内样式及 CSS 样式片段。推荐采用红色标记错误、蓝色标记概念、绿色标记结果、橙色标记重点、紫色标记原理，形成统一的学习笔记配色体系。

注意：Obsidian 的源码模式会显示 HTML 标签，切换到阅读视图后才能看到实际的文字颜色。