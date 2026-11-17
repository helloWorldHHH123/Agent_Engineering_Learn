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

