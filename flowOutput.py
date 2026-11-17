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