import asyncio
from agents import Agent, Runner
import async_local_settinngs  # 加载本地设置
# import gemini_settings
import base64   # 导入 Python 内置的 Base64 编码模块

# 也可以放到 async def main() 函数里面
agent = Agent(
    name="AI助手",
    instructions="你是一个友好的AI助手。使用中文进行回答",  # 系统提示词
    model="deepseek-flash",  # 明确指定DeepSeek模型
)

# 定义函数，image_path 表示图片的文件路径
def encode_image(image_path):
    # 以二进制只读模式（rb）打开图片文件
    with open(image_path, "rb") as image_file:
        # 读取图片的全部二进制数据，返回 bytes 类型
        bin_content = image_file.read()
        # 将二进制数据编码为 Base64，再转换成 UTF-8 字符串
        return base64.b64encode(bin_content).decode("utf-8")

async def main():
    # 读取 hello.png 图片，并将图片转换成 Base64 编码的字符串
    base64_image = encode_image("AIAgent2.png")
    # print("图片字符串：", base64_image)
    # 创建消息列表，用于向大模型传递图片和文字
    messages = [
        {  # 第一条消息：传递图片
            "role": "user",  # 消息角色：用户
            "content": [  # 消息内容：列表格式，可以包含图片等多模态数据
                {  # 图片信息
                    # "input_image" 不是自己随便设计的，而是 OpenAI API 规定的图片输入类型。
                    "type": "input_image",  # 指定输入内容的类型为图片
                    "image_url": f"data:image/jpeg;base64,{base64_image}",  # 将 Base64 图片编码封装成 Data URL
                }  # 图片信息结束
            ],  # 图片内容列表结束
        },  # 第一条用户消息结束

        {  # 第二条消息：传递文字提示词
            "role": "user",  # 消息角色：用户
            "content": "图片中是什么内容？是什么颜色？",  # 用户提出的问题，让大模型分析上面的图片
        },  # 第二条用户消息结束
    ]  # 消息列表结束
    result = await Runner.run(agent, messages)     # 异步写法
    print(result.final_output)
    # result = await Runner.run(agent, "1+1等于多少？")
    # print(result.final_output)

if __name__ == '__main__':
    # 异步启动
    asyncio.run(main())