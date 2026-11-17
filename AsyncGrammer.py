'''
异步，但是仍然属于一次性输出，而非流式输出
下面这些代码需要配合使用：
import asyncio

async def main():
    print('123')
    await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
'''

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

