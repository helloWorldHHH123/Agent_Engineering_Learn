**系统提示：**

你运行在一个和思考、行动、观察和回答的循环，在循环结束时，你输出最终的答案。

用“思考”来描述你对被问问题的想法。

用“操作”运行您可用的操作之一。

“观察”将是运行这些操作的结果。

“答案”将是分析观察结果的结果。

**推理+执行（ReAct，2023）** 将推理和行动结合起来应用到LLMs上。其中，推理产生的traces帮助模型归纳、跟踪、更新行动计划，并辅助模型进行异常处理；行动则通过与知识库、维基百科API、环境等外部信息源交互来收集信息。推理与行动交替进行，不仅改善了模型的幻觉（hallucination）和错误传播（error propagation）问题，同时使得LLMs解决问题的过程本身（trajectories）更加接近人类表现，即更具有可解释性，从而生成的结果也更加可信。

## ReAct Agent 的实现原理与执行流程

## 一、代码整体功能

这段代码基于 DeepSeek API 和 Function Calling，实现了一个简化版 ReAct Agent。

**核心思想：让大模型根据用户问题自主判断是否需要调用工具，通过“推理 → 行动 → 观察 → 再次推理”的循环，逐步完成任务。**

例如，用户提出：

> 比赛场上，篮球队的球员人数乘以排球队的球员人数，结果是多少？

Agent 可以分别查询篮球和排球的场上人数，再计算结果：

- 篮球：5 人
    
- 排球：6 人
    
- 最终结果：5 × 6 = 30
    

## 二、代码的主要组成部分

### 1. 初始化大模型客户端

```
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)
```

作用：配置 API Key 和接口地址，以便后续向 DeepSeek 服务器发送请求。

### 2. 定义工具函数：get_info_on_ball_game()

```
def get_info_on_ball_game(game_name: str):
```

作用：根据输入的球类运动名称，查询对应的运动信息。

函数内部使用 `data` 列表存储不同运动的信息，包括：

- `name`：运动名称。
    
- `description`：运动描述。
    
- `team_members`：队伍人数。
    
- `players_on_field`：比赛场上的人数。
    

通过遍历 `data`，查找名称匹配的运动，并返回对应信息。

**注意：该工具查询的是 Python 程序中预先定义的数据，并没有访问外部网站或数据库。**

### 3. 定义工具描述：tools

```
tools = [{
    "type": "function",
    "function": {
        "name": "get_info_on_ball_game",
        "description": "获取球类比赛的基本信息和人数规模",
        "parameters": {
            "type": "object",
            "properties": {
                "game_name": {"type": "string"}
            },
            "required": ["game_name"],
            "additionalProperties": False
        },
        "strict": True
    }
}]
```

作用：向 LLM 描述可以调用的工具及其参数。

其中：

- `name`：工具名称。
    
- `description`：工具功能描述。
    
- `parameters`：工具参数的 JSON Schema。
    
- `required`：必须提供的参数。
    
- `strict`：要求工具调用参数严格遵循定义的 Schema。
    

需要注意，**tools 只是工具描述，不负责真正执行 Python 函数。**

### 4. 初始化系统提示和对话历史

```
message_history = []
message_history.append({
    "role": "system",
    "content": system_prompt
})
```

作用：

- `system_prompt`：告诉模型按照思考、行动、观察和回答的方式处理任务。
    
- `message_history`：保存用户消息、模型回复和工具执行结果，实现对话上下文管理。
    

### 5. get_completion()：调用大模型

该函数主要完成以下操作：

1. 接收一条新消息。
    
2. 将新消息加入 `message_history`。
    
3. 调用 DeepSeek API，并传入对话历史和工具描述。
    
4. 接收大模型返回的文本或工具调用请求。
    
5. 将模型回复转换为 Python 字典。
    
6. 将模型回复保存到历史记录中并返回。
    

核心代码：

```
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=message_history,
    tools=tools,
    extra_body={"thinking": {"type": "disabled"}}
)
```

这里关闭了 DeepSeek 的思考模式，但程序仍然可以通过提示词和工具调用实现 ReAct 风格的执行循环。

### 6. agent()：Agent 的核心控制函数

`agent(query)` 是整个程序的核心，负责协调模型与工具之间的交互。

主要任务包括：

1. 接收用户问题。
    
2. 调用 `get_completion()`。
    
3. 判断模型是否需要调用工具。
    
4. 解析模型返回的工具名称和参数。
    
5. 执行 Python 工具函数。
    
6. 将工具结果加入历史记录。
    
7. 再次调用模型，直到生成最终答案或达到最大轮数。
    

## 三、ReAct Agent 的完整运行流程

```
用户输入问题
      ↓
agent(query) 接收问题
      ↓
将问题封装成 user 消息
      ↓
get_completion() 调用 DeepSeek
      ↓
LLM 分析问题
      ↓
是否需要调用工具？
      │
      ├── 否
      │    ↓
      │   输出模型回答
      │    ↓
      │   结束循环
      │
      └── 是
           ↓
       返回 tool_calls
           ↓
       解析工具名称、参数和调用 ID
           ↓
       Python 执行工具函数
           ↓
       获取工具结果（Observation）
           ↓
       将结果作为 tool 消息
       加入 message_history
           ↓
       再次调用 DeepSeek
           ↓
       LLM 根据观察结果继续处理
           ↓
       重复循环，直至结束
```

### 结合具体问题理解

**用户问题：**

“篮球队的场上人数乘以排球队的场上人数是多少？”

**第一步：LLM 分析问题**

模型发现需要篮球和排球的场上人数，因此可能请求调用两次 `get_info_on_ball_game`。

**第二步：生成工具调用请求**

例如：

```
get_info_on_ball_game(game_name="Basketball")
get_info_on_ball_game(game_name="Volleyball")
```

这里展示的是工具调用意图，真正执行函数的是 Python 程序。

**第三步：Python 执行工具**

通过：

```
func_result = get_info_on_ball_game(**func_kwargs)
```

执行查询，得到对应运动信息。

**第四步：将结果反馈给 LLM**

```
message_history.append({
    "role": "tool",
    "tool_call_id": func_call_id,
    "content": str(func_result)
})
```

其中：

- `role="tool"`：表示消息来自工具。
    
- `tool_call_id`：标识对应的工具调用。
    
- `content`：保存工具执行结果。
    

每个工具调用都需要对应的工具返回消息。

**第五步：LLM 继续处理**

当所有工具结果加入 `message_history` 后，下一轮调用 `get_completion(None)`。

模型读取工具结果，获取篮球 5 人、排球 6 人的信息，并计算：

5 × 6 = 30

最终生成回答。

## 四、关键变量及函数总结

|名称|作用|
|---|---|
|`client`|DeepSeek API 客户端|
|`get_info_on_ball_game()`|查询球类运动信息|
|`tools`|向 LLM 描述可用工具|
|`system_prompt`|设置模型的行为指令|
|`message_history`|保存完整对话历史|
|`get_completion()`|调用 LLM 并记录回复|
|`agent()`|控制整个 ReAct 循环|
|`next_message`|保存下一次需要加入历史的消息|
|`tool_calls`|LLM 返回的工具调用请求|
|`func_call_id`|工具调用的唯一标识|
|`func_kwargs`|解析后的工具调用参数|
|`func_result`|Python 工具执行结果|
|`max_turns`|Agent 最大执行轮数|

## 五、代码中的三个关键机制

**1. Function Calling（工具调用）**

LLM 根据任务判断是否需要工具，并生成工具调用请求。Python 程序负责执行对应的函数。

**2. Memory（记忆机制）**

利用 `message_history` 保存用户问题、模型回复和工具结果，使模型在后续调用时可以获取之前的信息。

这里实现的是基于消息列表的短期上下文记忆，并不是持久化的长期记忆系统。

**3. ReAct（推理与行动循环）**

模型根据问题选择行动，接收工具执行结果，然后继续处理任务。

与只进行一次 LLM 调用不同，ReAct Agent 可以通过多轮“模型调用—工具执行—结果反馈”完成任务。

## 六、当前代码的局限性

这是一份用于学习的简化版 Agent 实现，主要存在以下局限：

1. **工具执行方式固定**：虽然模型可以返回工具名称，但 Python 代码直接执行 `get_info_on_ball_game()`，没有实现通用的多工具分发机制。
    
2. **缺少异常处理**：没有处理 JSON 参数解析失败、工具执行异常或 API 请求失败等情况。
    
3. **最大轮数限制较简单**：如果最后一轮模型仍请求调用工具，可能没有机会再生成最终答案。
    
4. **记忆没有持久化**：`message_history` 仅保存在当前 Python 程序的内存中，程序重新运行后会重新初始化。
    

## 七、总结

这段代码通过 **DeepSeek + Function Calling + message_history + 循环控制** 实现了一个基础 ReAct Agent。

四个关键模块分别承担不同职责：

- **LLM：负责分析任务并决定是否调用工具。**
    
- **Tools：提供外部功能及数据查询能力。**
    
- **Memory：保存历史消息和工具执行结果。**
    
- **Agent Loop：负责控制模型调用、工具执行和结果反馈的循环。**
    

**核心流程：用户提出问题 → LLM 请求工具 → Python 执行工具 → 结果返回 LLM → LLM 继续处理并生成答案。**

这体现了 Agent 与普通 LLM 聊天程序的一个重要区别：Agent 不仅可以生成文本，还能借助外部工具获取信息，并通过多轮交互逐步完成任务。

## 八、完整代码

```python
from openai import OpenAI  
import json  
import os  
  
# 需要在pycharm中编辑配置文件，设置这个函数所需要的的API密钥  
client = OpenAI(  
    api_key=os.environ["DEEPSEEK_API_KEY"],  
    base_url="https://api.deepseek.com"  
)  
  
def get_info_on_ball_game(game_name: str):  
    data = [  
        {  
            "name": "篮球 (Basketball)",  
            "description": "两支球队通过投篮得分，比赛分为四节，每节时间因联赛而异。",  
            "team_members": 12,  
            "players_on_field": 5  
        },  
        {  
            "name": "排球 (Volleyball)",  
            "description": "两队隔网对抗，通过击球过网并使其落在对方场地得分。",  
            "team_members": 12,  
            "players_on_field": 6  
        },  
        {  
            "name": "足球 (Soccer)",  
            "description": "两支球队通过踢球进入对方球门得分，比赛分为上下半场。",  
            "team_members": 11,  
            "players_on_field": 11  
        },  
        {  
            "name": "沙滩排球 (Beach Volleyball)",  
            "description": "排球的变种，在沙地上进行，每队人数较少。",  
            "team_members": 2,  
            "players_on_field": 2  
        },  
        {  
            "name": "网球 (Tennis)",  
            "description": "单打或双打比赛，球员用球拍击球过网，使对手无法回击。",  
            "team_members": 1,  
            "players_on_field": 1  
        },  
        {  
            "name": "棒球 (Baseball)",  
            "description": "进攻方击球后跑垒得分，防守方投球并试图使击球手出局。",  
            "team_members": 9,  
            "players_on_field": 9  
        },  
        {  
            "name": "冰球 (Ice Hockey)",  
            "description": "在冰面上进行，球员用球棍击打冰球进入对方球门。",  
            "team_members": 20,  
            "players_on_field": 6  
        },  
        {  
            "name": "橄榄球 (Rugby)",  
            "description": "球员持球奔跑或传球，通过达阵或射门得分。",  
            "team_members": 15,  
            "players_on_field": 15  
        },  
        {  
            "name": "乒乓球 (Table Tennis)",  
            "description": "两名或四名球员在球桌上用球拍击打小球。",  
            "team_members": 1,  
            "players_on_field": 1  
        },  
        {  
            "name": "羽毛球 (Badminton)",  
            "description": "球员用球拍击打羽毛球过网，使对手无法回击。",  
            "team_members": 1,  
            "players_on_field": 1  
        }  
    ]  
    ret = []  
    for d in data:  
        if game_name.lower() in d['name'].lower():  
            ret.append(d)  
    return ret  
  
tools = [{  
    "type": "function",  
    "function": {  
        "name": "get_info_on_ball_game",  
        "description": "获取球类比赛的基本信息和人数规模",  
        "parameters": {  
            "type": "object",  
            "properties": {  
                "game_name": {"type": "string"},  
            },  
            "required": ["game_name"],  
            "additionalProperties": False  
        },  
        "strict": True  
    }  
}]  
  
system_prompt = """  
你运行在一个和思考、行动、观察和回答的循环，在循环结束时，你输出最终的答案。  
用“思考”来描述你对被问问题的想法。  
用“操作”运行您可用的操作之一。  
“观察”将是运行这些操作的结果。  
“答案”将是分析观察结果的结果。  
"""  
message_history = []  
message_history.append({"role": "system", "content": system_prompt})  
  
def get_completion(message):  
    # 如果存在新消息，则加入历史记录  
    if message is not None:  
        message_history.append(message)  
    # 调用大模型  
    response = client.chat.completions.create(  
        model="deepseek-flash",  
        messages=message_history,  
        tools=tools,  
        extra_body={"thinking": {"type": "disabled"}}  
    )  
    # 将模型响应转换为字典  
    response_dict = response.choices[0].message.model_dump(  
        exclude_none=True  
    )  
    # 保存大模型的响应  
    message_history.append(response_dict)  
    return response_dict  
  
def agent(query):  
    max_turns = 5  
    current_turns = 1  
    # 将用户问题封装成消息  
    next_message = {"role": "user", "content": query}  
    while current_turns <= max_turns:  
        # ① 调用LLM  
        message = get_completion(next_message)  
        # 输出模型返回的文本内容  
        if message.get("content"):  
            print(message["content"])  
        # ② 判断模型是否请求调用工具  
        if message.get("tool_calls"):  
            # 遍历模型请求的所有工具  
            for tool_call in message["tool_calls"]:  
                # 获取工具调用ID  
                func_call_id = tool_call["id"]  
                # 将JSON参数转换成Python字典  
                func_kwargs = json.loads(  
                    tool_call["function"]["arguments"]  
                )  
                # ③ 执行工具函数  
                func_result = get_info_on_ball_game(**func_kwargs)  
                # ④ 输出工具执行结果  
                print(f"观察：{func_result}")  
                # ⑤ 将工具结果添加到对话历史  
                message_history.append({  
                    "role": "tool",  
                    "tool_call_id": func_call_id,  
                    "content": str(func_result)  
                })  
            # 下一轮不再添加新消息  
            # 因为工具结果已经加入message_history  
            next_message = None  
        else:  
            # 模型没有调用工具，结束循环  
            break  
        # 执行轮数加1  
        current_turns += 1  
  
  
if __name__ == '__main__':  
    query = '比赛场上，篮球队的球员人数乘以排球队的球员人数，结果是多少'  
    agent(query)
```

**运行结果**

```python
观察：[{'name': '篮球 (Basketball)', 'description': '两支球队通过投篮得分，比赛分为四节，每节时间因联赛而异。', 'team_members': 12, 'players_on_field': 5}]
观察：[{'name': '排球 (Volleyball)', 'description': '两队隔网对抗，通过击球过网并使其落在对方场地得分。', 'team_members': 12, 'players_on_field': 6}, {'name': '沙滩排球 (Beach Volleyball)', 'description': '排球的变种，在沙地上进行，每队人数较少。', 'team_members': 2, 'players_on_field': 2}]
思考：问题问的是“篮球队的球员人数乘以排球队的球员人数”。需要确定“球员人数”指的是球队名单人数（team_members）还是场上人数（players_on_field）。

篮球队：team_members = 12，players_on_field = 5
排球队：team_members = 12（室内排球），players_on_field = 6

## 答案

按球队总人数计算：篮球 12 人 × 排球 12 人 = **144**

如果按场上球员计算：篮球 5 人 × 排球 6 人 = **30**

补充说明：排球还有沙滩排球变种，每队仅 2 人（场上也是 2 人）。若与沙滩排球相乘，则为 12×2=24 或 5×2=10。通常默认“排球队”指室内排球（12 人队 / 6 人上场）。

进程已结束，退出代码为 0

```