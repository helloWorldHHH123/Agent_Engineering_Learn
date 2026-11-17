# <span style="color: #E57373;">1. OpenAI Agents SDK：异步调用（Async）</span>
## 一、异步调用的基本原理

异步调用（Asynchronous Programming）是一种非阻塞的程序执行方式，允许程序在等待某项操作完成时，执行其他可以运行的任务。

在 AI Agent 开发中，异步调用主要用于大模型 API 请求、工具调用以及多个 Agent 的并发执行。

**异步编程的核心关键词：**

- `async def`：定义异步函数（协程函数）。
    
- `await`：等待异步操作完成，并获取其返回结果。
    
- `asyncio.run()`：创建并运行事件循环，执行顶层协程。
    
- `Runner.run()`：OpenAI Agents SDK 提供的异步 Agent 运行方法。
    

## 二、基本异步代码结构

```
import asyncio

async def main():
    print('123')
    await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
```

**执行流程：**

1. 导入 Python 内置的 `asyncio` 模块。
    
2. 使用 `async def main()` 定义异步函数。
    
3. 执行 `print('123')`。
    
4. 使用 `await asyncio.sleep(1)` 异步等待 1 秒。
    
5. 通过 `asyncio.run(main())` 启动事件循环并执行 `main()`。
    

注意：`await` 会暂停当前协程，但不会阻塞整个事件循环。如果存在其他可运行的协程，事件循环可以调度它们执行。

## 三、OpenAI Agents SDK 的异步调用

### 1. 初始化 Agent

```
from agents import Agent, Runner
import async_local_settinngs

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手。使用中文进行回答",
    model="deepseek-flash",
)
```

其中：

- `Agent`：创建 Agent 实例。
    
- `name`：设置 Agent 名称。
    
- `instructions`：设置系统提示词。
    
- `model`：指定 DeepSeek 模型。
    
- `async_local_settinngs`：导入自定义配置模块，用于配置 DeepSeek API 客户端等信息。
    

Agent 可以在异步函数外部创建，不要求必须写在 `async def main()` 中。

### 2. 异步执行 Agent

```
async def main():
    result = await Runner.run(agent, '你是谁？')
    print(result.final_output)
```

核心代码：

```
result = await Runner.run(agent, '你是谁？')
```

执行过程：

1. `Runner.run()` 创建 Agent 运行协程。
    
2. `await` 等待 Agent 执行完成。
    
3. 将执行结果赋值给 `result`。
    
4. 使用 `result.final_output` 获取最终回答。
    

**注意：**`**Runner.run()**` **不会直接返回最终结果，而是返回一个需要等待执行的协程对象。**

如果不使用 `await`：

```
result = Runner.run(agent, '你是谁？')
```

此时 `result` 是协程对象，不能直接访问 `result.final_output`。

### 3. 启动异步程序

```
if __name__ == '__main__':
    asyncio.run(main())
```

作用：创建事件循环，运行 `main()` 协程，等待其完成并关闭事件循环。

## 四、完整代码

```python
'''  
异步，但是仍然属于一次性输出，而非流式输出  
下面这些代码需要配合使用：  
import asyncio  
  
async def main():  
    print('123')    await asyncio.sleep(1)  
if __name__ == '__main__':  
    asyncio.run(main())'''  
  
import asyncio  
from agents import Agent, Runner  
import async_local_settinngs  # 加载本地设置  
  
# 也可以放到 async def main() 函数里面  
agent = Agent(  
    name="AI助手",  
    instructions="你是一个友好的AI助手。使用中文进行回答",  # 系统提示词  
    model="deepseek-flash",  # 明确指定DeepSeek模型  
)  
  
async def main():  
    # result = Runner.run_sync(agent, '你是谁？')     # 同步写法  
    # 让协程变成运行之后的结果，即：需要加个 await，否则不能使用 result.final_output     
    result = await Runner.run(agent, '你是谁？')     # 异步写法  
    print(result.final_output)  
  
if __name__ == '__main__':  
    # 异步启动  
    asyncio.run(main())
```

**输出**

```python
你好！我是你的AI助手，可以叫我小助手或其他你喜欢的名字。我在这里为你提供信息、解答问题、聊天陪伴，或者帮忙处理各种任务。有什么需要尽管告诉我！😊

进程已结束，退出代码为 0
```
## 五、同步与异步调用的区别

| 对比项        | 同步调用（Sync）          | 异步调用（Async）          |
| ---------- | ------------------- | -------------------- |
| SDK 方法     | `Runner.run_sync()` | `Runner.run()`       |
| 函数定义       | `def`               | `async def`          |
| 是否需要 await | 不需要                 | 需要                   |
| 运行方式       | 顺序等待结果              | 可在等待期间调度其他协程         |
| 代码复杂度      | 较低                  | 相对较高                 |
| 适用场景       | 简单 Agent、单次任务       | 并发 API 请求、多 Agent 协作 |

同步示例：

```
result = Runner.run_sync(agent, "你是谁？")
print(result.final_output)
```

异步示例：

```
result = await Runner.run(agent, "你是谁？")
print(result.final_output)
```

## 六、异步 Agent 的完整执行流程

```
Python 程序启动
       ↓
import async_local_settinngs
加载 DeepSeek API 配置
       ↓
Agent() 创建智能体
       ↓
asyncio.run(main())
启动事件循环
       ↓
进入 async def main()
       ↓
await Runner.run(agent, query)
异步执行 Agent
       ↓
Agent 调用 DeepSeek API
       ↓
等待模型响应
       ↓
Agent 完成任务
       ↓
返回执行结果 result
       ↓
result.final_output
获取最终回答
       ↓
print() 输出结果
       ↓
程序结束
```

## 七、总结

OpenAI Agents SDK 同时支持同步和异步调用。

异步写法主要使用三个关键语法：

1. `**async def**`：定义协程函数。
    
2. `**await**`：等待异步任务完成，并获取结果。
    
3. `**asyncio.run()**`：启动事件循环，运行异步主函数。
    

在 Agent 开发中，异步机制可以提高多个独立任务并发执行时的效率，但不意味着单次 API 请求一定更快。

**核心代码结构：**

```
async def main():
    result = await Runner.run(agent, "用户问题")
    print(result.final_output)

asyncio.run(main())
```

这也是后续学习 Agent 流式输出、异步工具调用和多 Agent 并发执行的基础。


# <span style="color: #E57373;">2. 流式传输</span>
## 一、流式输出的基本原理

**流式输出（Streaming）是指大模型在生成回答的过程中，将已生成的内容逐步返回给客户端，而不是等待全部内容生成完毕后再一次性返回。**

例如，用户提出：“你是谁？”

普通调用：

```
用户提问
    ↓
调用大模型
    ↓
等待完整回答生成
    ↓
一次性输出全部内容
```

流式调用：

```
用户提问
    ↓
调用大模型
    ↓
模型开始生成回答
    ↓
生成一部分 → 立即返回
    ↓
继续生成 → 继续返回
    ↓
直到回答生成完毕
```

流式输出可以让用户更早看到生成内容，改善交互体验，但不代表整个模型推理过程一定更快。

## 二、核心代码与作用

### 1. 创建 Agent

```
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手。使用中文进行回答",
    model="deepseek-flash",
)
```

作用：创建一个 Agent，指定名称、系统提示词及使用的 DeepSeek 模型。

其中，`async_local_settinngs` 是自定义配置模块，用于配置 DeepSeek API 客户端。

### 2. 启动流式运行

```
result = Runner.run_streamed(agent, "你是谁？")
```

作用：启动 Agent 的流式运行，返回一个流式运行结果对象。

与普通调用的区别：

- `Runner.run_sync()`：同步执行，等待完整结果。
    
- `await Runner.run()`：异步执行，等待完整结果。
    
- `Runner.run_streamed()`：以流式方式运行，通过事件逐步获取输出。
    

注意：`Runner.run_streamed()` 本身不需要添加 `await`。

### 3. 异步遍历流式事件

```
async for event in result.stream_events():
```

作用：持续接收 Agent 运行过程中产生的流式事件。

每当有新的事件到达，就执行一次循环体。

其中：

- `async for`：异步遍历事件。
    
- `result.stream_events()`：获取 Agent 的流式事件。
    
- `event`：当前接收到的事件对象。
    

### 4. 判断事件类型

```
if event.type == "raw_response_event" and isinstance(
    event.data, ResponseTextDeltaEvent
):
```

作用：筛选大模型返回的文本增量事件。

分为两个判断条件：

**第一个条件：**

```
event.type == "raw_response_event"
```

判断当前事件是否属于模型的原始响应事件。

**第二个条件：**

```
isinstance(event.data, ResponseTextDeltaEvent)
```

判断事件携带的数据是否属于文本增量事件。

只有两个条件同时满足时，才处理当前文本片段。

### 5. 输出流式内容

```
print(event.data.delta, end="", flush=True)
```

其中：

- `event.data.delta`：获取当前事件中新生成的文本片段。
    
- `end=""`：不自动换行，将多个片段连续输出。
    
- `flush=True`：立即刷新输出缓冲区。
    

例如，模型最终生成：

```
你好，我是一个AI助手。
```

流式返回可能是：

```
第1次：你好，
第2次：我是
第3次：一个
第4次：AI助手。
```

这些增量片段可以依次拼接成完整回答。

## 三、Agent 流式事件类型

OpenAI Agents SDK 主要提供以下几类流式事件：

|事件类型|作用|
|---|---|
|`raw_response_event`|大模型返回的原始响应事件，包括文本增量等|
|`run_item_stream_event`|Agent 运行过程中的工具调用、工具结果、交接等事件|
|`agent_updated_stream_event`|当前执行的 Agent 发生变化时产生的事件|

因此，流式传输不仅可以输出模型生成的文本，也可以用于观察 Agent 执行工具和交接任务等过程。

## 四、完整流式输出调用流程

```
Python 程序启动
        ↓
导入 asyncio、Agent、Runner
        ↓
加载 DeepSeek API 配置
        ↓
通过 Agent() 创建智能体
        ↓
asyncio.run(main())
启动异步事件循环
        ↓
进入 async def main()
        ↓
Runner.run_streamed(agent, query)
启动 Agent 流式运行
        ↓
result.stream_events()
获取流式事件序列
        ↓
async for event
持续接收流式事件
        ↓
判断事件类型
        ↓
是否为 raw_response_event？
        │
        ├── 否 → 跳过当前事件
        │
        └── 是
             ↓
        是否为 ResponseTextDeltaEvent？
             │
             ├── 否 → 跳过当前事件
             │
             └── 是
                  ↓
             event.data.delta
             提取本次新增文本
                  ↓
             print()
             实时输出文本
                  ↓
             继续接收下一个事件
                  ↓
        直到 Agent 运行结束
                  ↓
             程序结束
```

## 五、完整代码

```python
'''  
流式输出：边运行边出结果  
'''  
import asyncio  
from agents import Agent, Runner  
import async_local_settinngs  # 加载本地设置  
from openai.types.responses import ResponseTextDeltaEvent  
  
# 也可以放到 async def main() 函数里面  
agent = Agent(  
    name="AI助手",  
    instructions="你是一个友好的AI助手。使用中文进行回答",  # 系统提示词  
    model="deepseek-flash",  # 明确指定DeepSeek模型  
)  
  
async def main():  
    # 流式传输  
    result = Runner.run_streamed(agent, '你是谁？')     # 异步写法  
    # 异步遍历 Agent 流式运行过程中产生的事件  
    async for event in result.stream_events():  
        # 判断当前事件是否为大模型返回的原始响应事件  
        # raw_response_event 来自LLM的响应  
        # run_item_stream_event 来自Runner事件：工具调用、交接  
        # 判断当前事件是否为大模型返回的文本增量事件（Text Delta Event），如果是，就执行后续代码  
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):  
            # 输出当前事件中的增量数据（delta）  
            # delta 表示本次流式返回的新内容，而不是完整回答  
            # 有一个东西出来就打印一次，不需要等待三百多个字全出来  
            # event.data.delta 的作用是：获取大模型在流式传输（Streaming）过程中，本次新生成的文本片段。  
            # print(event.data.delta)  
            print(event)  
  
if __name__ == '__main__':  
    # 异步启动  
    asyncio.run(main())
```

**输出**

```python
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='你好', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=67, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='！', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=68, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='我是', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=69, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='你的', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=70, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='友好', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=71, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta=' AI', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=72, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta=' ', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=73, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='助手', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=74, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='，', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=75, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='可以', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=76, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='帮你', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=77, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='解答', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=78, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='问题', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=79, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='、', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=80, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='整理', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=81, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='信息', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=82, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='、', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=83, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='提供', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=84, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='建议', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=85, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='，', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=86, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='也能', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=87, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='陪你', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=88, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='聊天', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=89, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='。', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=90, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='有什么', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=91, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='想', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=92, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='让我', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=93, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='帮忙', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=94, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='的吗', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=95, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='？', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=96, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='😊', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=97, type='response.output_text.delta'), type='raw_response_event')
RawResponsesStreamEvent(data=ResponseTextDeltaEvent(content_index=0, delta='', item_id='__fake_id__', logprobs=[], output_index=1, sequence_number=98, type='response.output_text.delta'), type='raw_response_event')

进程已结束，退出代码为 0
```
## 六、流式输出与异步调用的区别

|对比项|异步调用（Async）|流式输出（Streaming）|
|---|---|---|
|核心目标|非阻塞地等待任务|逐步获取生成结果|
|SDK 方法|`Runner.run()`|`Runner.run_streamed()`|
|是否使用 await|`await Runner.run()`|`run_streamed()` 本身不需要|
|获取结果方式|`result.final_output`|`result.stream_events()`|
|输出时机|等待完整回答|生成过程中逐步输出|
|典型应用|并发 API、异步工具调用|AI 聊天界面、实时生成内容|

需要注意：异步调用和流式输出不是互斥关系。当前示例实际上结合了两者，通过异步事件迭代实现流式输出。

## 七、总结

OpenAI Agents SDK 的流式输出主要包含四个核心步骤：

1. **启动流式运行**：使用 `Runner.run_streamed()` 创建流式运行结果。
    
2. **监听流式事件**：使用 `async for` 遍历 `result.stream_events()`。
    
3. **筛选文本事件**：通过 `raw_response_event` 和 `ResponseTextDeltaEvent` 判断是否存在新生成的文本。
    
4. **实时输出内容**：使用 `event.data.delta` 获取新增文本，并通过 `print()` 实时显示。
    

**核心实现：**

```
result = Runner.run_streamed(agent, "你是谁？")

async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(
        event.data, ResponseTextDeltaEvent
    ):
        print(event.data.delta, end="", flush=True)
```

**一句话总结：流式输出的核心机制是启动 Agent 流式运行，持续监听模型返回的事件，从中提取文本增量，并在生成过程中实时展示。**