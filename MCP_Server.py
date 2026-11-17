import os  # 导入 Python 内置的 os 模块，用于操作文件和目录

from mcp.server import MCPServer  # 从 MCP SDK 中导入 MCPServer 类

# 创建 MCP 服务器实例，服务器名称为 MCP Demo
mcp = MCPServer("MCP Demo")

# 使用装饰器，将下面的 ls 函数注册为 MCP 工具
@mcp.tool()
def ls():  # 定义 ls 函数，用于获取当前目录中的文件名
    """列出目录中的文件名"""  # 函数文档字符串，描述工具的功能

    # 获取当前工作目录中的文件和文件夹名称，并以列表形式返回
    return os.listdir(".")

# 判断当前 Python 文件是否作为主程序直接运行
if __name__ == '__main__':
    # 启动 MCP 服务器，等待客户端连接并调用工具
    mcp.run()