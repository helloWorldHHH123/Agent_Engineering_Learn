from pydantic import BaseModel
import asyncio
from agents import Agent, Runner
import async_local_settinngs  # 加载本地设置

class Data(BaseModel):
    名字: str
    年龄: int
    性别: str
    事迹: str

# 也可以放到 async def main() 函数里面
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手，使用中文回答。",  # 系统提示词
    model="deepseek-flash",  # 明确指定DeepSeek模型
    output_type=Data,   # 指定输出结构
)

async def main():
    result = await Runner.run(agent, '介绍一位值得记住的人？')     # 异步写法
    obj: Data = result.final_output
    print(result.final_output)
    print(obj.名字)
    print(obj.性别)
    print(obj.事迹)
    print("完整的对话记录：", result.to_input_list())

if __name__ == '__main__':
    # 异步启动
    asyncio.run(main())
