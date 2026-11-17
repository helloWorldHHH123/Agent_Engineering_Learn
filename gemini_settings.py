import os
from openai import AsyncOpenAI
from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)

# 创建 Gemini API 客户端
client = AsyncOpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 将 Gemini 客户端设置为 Agents SDK 的默认客户端
set_default_openai_client(client, use_for_tracing=False)

# 使用 Chat Completions 接口
set_default_openai_api("chat_completions")

# 禁用追踪
set_tracing_disabled(True)