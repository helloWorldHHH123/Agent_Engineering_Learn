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
