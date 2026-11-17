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
