'''
解决异步模式下只回答新的问题，旧的问题不回答的困难
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
    result = await Runner.run(agent, '1+1=？')     # 异步写法
    history = result.to_input_list()        # 转成python列表
    print("-----------历史对话-----------")
    print(history)
    history.append({"role": "user", "content": "再+1=？"})        # 对会话进行管理，也可以执行删减、裁剪、语义检索等操作
    result = await Runner.run(agent, history)     # 异步写法
    print(result.final_output)
    print("最新的完整对话过程：", result.to_input_list())

if __name__ == '__main__':
    # 异步启动
    asyncio.run(main())