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





