## 运行
# 同步写法
from agents import Agent, Runner
import async_local_settinngs  # 加载本地设置

agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手。使用中文进行回答",  # 系统提示词
    model="deepseek-flash",  # 明确指定DeepSeek模型
)

result = Runner.run_sync(agent, '你是谁？')

print(result.final_output)