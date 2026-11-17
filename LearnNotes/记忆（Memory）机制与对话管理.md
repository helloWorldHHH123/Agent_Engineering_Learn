
为了让LLM知道函数的执行结果如何使用，需要把完整对话历史记录下来一起发送给LLM，这就是一种记忆的实现形式，其优点是代码简单、内容完整。

不过当对于内容特别长时，既会增加LLM开销，降低效能，甚至会因为超过上下文长度限制，而调用失败。

## 0. 上下文长度计算

以deepseek为例，首先安装分词器，然后统计分词数量
### 什么是分词

假设有一句话：

```
我喜欢你
```

对于计算机程序来说，这具仅仅是一个字符串，无法理解其中的含义。

如果程序是一个LLM，那么它会：

1. **进行分词**，将文本转化为 Token 序列
    
2. 然后依次进行向量嵌入和位置编码，一起送入Transformer
    
3. 经过Transformer多层处理后得到一系列Token概率分布
    
4. 解码后得到输出文本
    

```
谢谢，我也喜欢你
```

## 一、记忆机制的作用

在多轮对话中，LLM 本身不会自动记住之前的所有对话，需要程序保存历史消息（`message_history`），并在后续请求中将相关历史记录发送给大模型。

随着对话轮数增加，历史消息不断累积，可能导致：

- Token 数量增加，API 调用成本提高。
    
- 上下文过长，影响处理效率。
    
- 超过模型上下文长度限制，导致请求失败。
    

因此，需要通过 Token 统计、滑动窗口和摘要记忆等方法管理对话历史。

## 二、Token 数量统计

**作用：统计文本或历史消息占用的 Token 数量，为上下文长度管理提供依据。**

### 1. 单段文本的 Token 统计

使用 `deepseek_tokenizer` 分词器：

```
result = ds_token.encode(text)
print(len(result))
```

其中：

- `ds_token.encode(text)`：将文本编码为 Token ID 序列。
    
- `len(result)`：计算 Token 数量。
    

例如，`"你是谁？"` 被编码为两个 Token。

### 2. 历史对话的 Token 统计

```
def tokens_by_messages(message_history: list):
    tokens = 0
    for msg in message_history:
        text = msg['content']
        tokens += len(ds_token.encode(text))
    return tokens
```

**实现原理：** 遍历 `message_history` 中的每条消息，提取 `content`，统计其 Token 数量并累加。

注意：这里统计的是消息文本的 Token 数，不包含消息结构及工具调用等额外开销，因此不一定等于 API 实际计费 Token 数。

## 三、滑动窗口记忆（Sliding Window Memory）

**作用：通过裁剪历史对话，只保留最近 K 条消息及系统提示词，减少上下文长度。**

### 实现流程

1. 从 `message_history` 中提取最近 K 条消息。
    
2. 检查保留的消息是否包含系统提示（System Prompt）。
    
3. 如果没有系统提示，而原始记录第一条是系统提示，则将其补充到最前面。
    
4. 返回裁剪后的历史消息列表。
    

核心代码：

```
new_message_list = message_list[-1*k:]
```

表示保留最后 K 条消息。

```
new_message_list.insert(0, message_list[0])
```

表示将原始系统提示插入列表开头。

**优点：** 实现简单、Token 消耗较少、能够保留最近的对话内容。

**缺点：** 较早的对话会被直接丢弃，可能导致模型遗忘重要历史信息。

注意：当前代码中的 K 表示最后 K 条消息，并不是最后 K 轮完整对话；如果历史中包含工具调用，还需要考虑工具请求与结果的完整性。

## 四、摘要记忆（Summary Memory）

**作用：利用 LLM 的文本总结能力，将较长的历史对话压缩成简短摘要，用摘要代替完整历史记录。**

### 实现流程

1. 将 `message_history` 发送给 DeepSeek 模型。
    
2. 要求模型总结历史对话的主要内容。
    
3. 提取模型生成的摘要文本。
    
4. 将摘要封装为新的 System 消息。
    
5. 返回压缩后的消息列表。
    

核心代码：

```
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{
        "role": "user",
        "content": f"请对以下对话内容进行总结：{message_list}"
    }]
)
```

构建摘要记忆：

```
new_message_list = [{
    "role": "system",
    "content": f"此前对话内容的总结：{response.choices[0].message.content}"
}]
```

**优点：** 可以保留较早历史对话中的关键信息，同时减少上下文长度。

**缺点：** 摘要过程需要额外调用 LLM，产生 API 费用，并且可能遗漏或错误概括重要信息。

注意：当前代码只是生成并返回摘要列表，并没有自动更新原始的 `message_history`。

## 五、其他记忆管理机制

### 1. 知识图谱记忆（Knowledge Graph Memory）

将对话中的实体及其关系提取出来，构建知识图谱。

Agent 可以查询知识图谱获取相关信息，适用于需要结构化知识和关系推理的场景。

### 2. 向量数据库记忆（Vector Store Retriever Memory / RAG）

将历史对话或外部文档进行分块、向量化，并存入向量数据库。

当用户提出新问题时，通过向量相似度检索相关历史信息，再将检索结果作为上下文提供给 LLM。

适用于长期记忆、语义检索及知识库问答。

## 六、不同记忆管理方法对比

|方法|核心思想|优点|局限性|
|---|---|---|---|
|完整历史记忆|保存所有历史消息|信息完整|Token 消耗不断增加|
|滑动窗口记忆|只保留最近 K 条消息|简单、高效|丢失早期信息|
|摘要记忆|使用 LLM 压缩历史对话|保留部分长期信息|有额外成本，可能丢失细节|
|知识图谱记忆|存储实体及其关系|适合结构化知识|构建和维护复杂|
|向量数据库记忆|向量化存储并语义检索|适合长期记忆和知识召回|依赖检索质量|

## 七、总结

AI Agent 的记忆管理主要解决三个问题：

1. **记忆存储**：如何保存历史对话和相关信息。
    
2. **记忆压缩**：如何减少历史消息占用的 Token。
    
3. **记忆检索**：如何在需要时获取相关历史信息。
    

本次代码实现了三项基础功能：

- **Token 统计**：判断历史对话的长度。
    
- **滑动窗口记忆**：裁剪较早的对话记录。
    
- **摘要记忆**：通过 LLM 将历史对话压缩为摘要。
    

**核心思想：在有限的上下文窗口内，尽可能保留对当前任务有价值的历史信息，同时控制 Token 消耗和 API 调用成本。**

## 八、完整代码

```python
from deepseek_tokenizer import ds_token  
  
text = "你是谁？"  
result = ds_token.encode(text)  
print(result)  
print(f"Token数：{len(result)}")  
# 输出：文本编码后的两个 Token ID，而 Token数：2 表示这段文本被分成了两个 Token。  
# [122294, 1148]  
# Token数：2  
  
# 针对message对象，可以使用下面函数进行统计  
def tokens_by_messages(message_history:list):  
    tokens = 0  
    for msg in message_history:  
        text = msg['content']  
        tokens += len(ds_token.encode(text))  
    return tokens  
  
message_history = []  
system_prompt = """  
你运行在一个相思考、行动、观察和回答的循环，在循环结束时，你输出最终的答案。  
用“思考”来描述你对被问问题的想法。  
用“操作”运行您可用的操作之一。  
“观察”将是运行这些操作的结果。  
“答案”将是分析观察结果的结果。  
"""  
message_history.append({"role": "system", "content": system_prompt})  
  
query = '比赛场上，篮球队的球员人数乘以排球队的球员人数，结果是多少'  
message_history.append({"role": "user", "content": query})  
message_history.append({"role": "user", "content": query})  
message_history.append({"role": "user", "content": "1+1=?"})  
message_history.append({"role": "user", "content": "再加1呢？"})  
  
print(tokens_by_messages(message_history))  
print(len(system_prompt) + len(query))  
  
# 滑动窗口  
# 对message_history进行裁剪，仅保留system提示和最新的K个user提示  
def context_sliding_window(message_list: list, k=2):  
    new_message_list: list = message_list[-1*k:]  
  
    # 如果丢失了系统提示，则手动补上  
    if new_message_list[0]['role'] != "system":     # 检查现在有没有系统提示  
        if message_list[0]['role'] == "system":     # 检查之前有没有系统提示  
            new_message_list.insert(0, message_list[0])     # 补上系统提示  
  
    return new_message_list  
  
print(context_sliding_window(message_history))  
  
  
# 摘要记忆  
# 利用LLM的摘要能力，对此前对话进行总结，并替代完整的对话内容  
# import openai  
from openai import OpenAI  
import os  
  
# 需要在pycharm中编辑配置文件，设置这个函数所需要的的API密钥  
# client = openai.OpenAI()  
client = OpenAI(  
    api_key=os.environ["DEEPSEEK_API_KEY"],  
    base_url="https://api.deepseek.com"  
)  
def context_summary(message_list):  
    response = client.chat.completions.create(  
        model="deepseek-flash",  
        messages=[{  
            "role": "user",  
            "content": f"请对以下对话内容进行总结：{message_list}"  
        }],  
    )  
  
    new_message_list = [{"role": "system", "content": f"此前对话内容的总结：{response.choices[0].message.content}"}]  
  
    return new_message_list  
print("-------------大模型摘要后的记录-------------")  
print(context_summary(message_history))  
  
  
# ## 其他管理机制  
#  
# **知识图谱记忆 [Knowledge Graph Memory]**：将对话中的实体和关系提取出来存入知识图谱，  
# Agent 可以查询图谱获取相关信息，适用于需要结构化知识的场景。  
#  
# **向量数据库记忆（Vector Store Retriever Memory / RAG）**：将对话（或外部文档）分块、向量化后存入向量数据库。  
# 当需要相关信息时，将用户查询向量化，在数据库中进行相似度搜索，召回最相关的片段作为上下文。这是实现 RAG 的核心。
```
