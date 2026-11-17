
# <span style="color: #E57373;">1. 常见的 Agent 开发框架</span>

## 一、主流 Agent 开发框架汇总（截至 2026 年 11 月）

| 名称                        | 背景                                     | 主要特点                       | Star 数 |
| ------------------------- | -------------------------------------- | -------------------------- | ------ |
| LangGraph                 | 来自 Agent 经典框架 LangChain                | 工作流编排、状态管理、持久化执行           | 12.8k  |
| LlamaIndex                | 曾是 RAG 经典框架，现发力 Agent                  | 知识库、RAG、数据检索、Agent         | 41.1k  |
| AutoGen                   | 背靠微软                                   | 多 Agent 对话与协作              | 44.6k  |
| AG2                       | AutoGen 创始人从 AutoGen v0.2 分叉而来         | 多 Agent 协作、任务自动化           | 2.6k   |
| OpenAI Agents SDK         | 背靠 OpenAI，从 Swarm 演进而来                 | 工具调用、Agent Handoff、Tracing | 10.4k  |
| PydanticAI                | 背靠 Pydantic 团队                         | 类型安全、结构化输出、工具调用            | 9.6k   |
| smolagents                | 背靠 Hugging Face                        | 轻量级 Agent、代码执行、工具调用        | 18.8k  |
| CrewAI                    | 曾基于 LangChain，后来重构                     | 多 Agent 协作、角色分工、任务编排       | 31.8k  |
| Atomic Agents             | 社区开源项目                                 | 模块化 Agent、结构化输入输出          | 3.7k   |
| Microsoft Agent Framework | 微软推出，整合 AutoGen 与 Semantic Kernel 技术路线 | 多 Agent 编排、工作流、持久化执行       | —      |
| Google ADK                | Google 推出的 Agent Development Kit       | 多 Agent 协作、工具调用、工作流        | —      |
| Claude Agent SDK          | Anthropic 推出的 Agent 开发 SDK             | 代码执行、文件操作、工具调用、子 Agent     | —      |
| LangChain DeepAgents      | LangChain 生态                           | 任务规划、文件系统、子 Agent、长期任务     | —      |
| Strands Agents            | AWS 开源                                 | 模型驱动的工具使用、多模型支持、Agent 编排   | —      |
| Agno                      | 开源 Python Agent 框架                     | 记忆、知识库、工具、多 Agent          | —      |
| Mastra                    | TypeScript / JavaScript Agent 框架       | Agent、工作流、Memory、RAG、评估    | —      |
| Vercel AI SDK             | Vercel 开发                              | TypeScript AI 应用、工具调用、流式输出 | —      |
| Vercel Eve                | Vercel 生态，2026 年持续发展的 Agent 框架         | 持久化 Agent、文件系统、Skills、任务调度 | —      |
| LightAgent                | 开源轻量级 Python Agent 框架                  | 工具调用、记忆、Skills、多 Agent 工作流 | —      |

**注：**

- 后 10 个框架为补充内容，包括 2026 年下半年有重要进展的项目，并不代表它们均在下半年首次发布。
    
- `—` 表示未核实实时 GitHub Star 数，不代表没有 Star。


## 二、2026 年下半年值得关注的变化

**1. Microsoft Agent Framework**

2026 年 4 月达到 1.0 正式版本，7 月发布 Agent Harness，进一步完善规划、记忆、Skills、审批和执行过程管理能力。

它是微软目前值得重点关注的 Agent 开发框架之一。

**2. Google ADK**

2026 年继续扩展多语言支持和工作流能力，TypeScript 版本于 2026 年 8 月进入正式可用阶段。

**3. AG2**

2026 年 7 月发布 1.0 版本，进一步发展独立的多 Agent 开发框架路线。

**4. Vercel Eve**

2026 年下半年持续发展，采用文件系统优先的设计方式，面向具有持久状态、工具和任务调度能力的 Agent。

**5. LightAgent**

2026 年 10 月发布 v0.11.0，新增持久化动态 DAG 多 Agent 执行等能力。

注意：这些框架并非全部在 2026 年下半年首次发布，部分是既有项目在下半年推出重要版本或功能。

## 三、总结

目前 Agent 开发框架大致可以按照应用方向进行分类：

|技术方向|代表框架|
|---|---|
|工作流与状态管理|LangGraph、Microsoft Agent Framework|
|多 Agent 协作|CrewAI、AG2、Google ADK|
|轻量级工具调用|OpenAI Agents SDK、PydanticAI、smolagents|
|知识库与 RAG|LlamaIndex、LangChain|
|复杂任务和编码 Agent|Claude Agent SDK、DeepAgents|
|TypeScript Agent 开发|Mastra、Vercel AI SDK|
|AWS 生态|Strands Agents|
|轻量级 Python Agent|Agno、LightAgent|

**核心认识：Agent 框架的作用主要是将 LLM、Tools、Memory、Workflow 和多 Agent 协作等能力组织起来，降低复杂 Agent 系统的开发与维护成本。**

# <span style="color: #E57373;">2. Agent 开发框架的选择策略</span>

### 一、原视频中的选择建议

- **快速上手**：OpenAI Agents SDK / smolagents
    
- **小规模快速开发**：CrewAI / PydanticAI / AutoGen / AG2
    
- **高级定制与深度控制**：AutoGen / AG2 / LangGraph（LangChain）
    

### 二、2026 年更新后的选择建议

| 开发需求                       | 推荐框架                                           | 主要原因                          |
| -------------------------- | ---------------------------------------------- | ----------------------------- |
| 快速入门 Agent                 | OpenAI Agents SDK、smolagents、PydanticAI        | API 简单，代码量少，适合学习 Tool Calling |
| 小规模 Agent 应用               | PydanticAI、Agno、OpenAI Agents SDK              | 适合快速构建带有工具和记忆功能的 Agent        |
| 多 Agent 协作                 | CrewAI、AG2、Google ADK                          | 支持多个 Agent 分工、协作与任务编排         |
| 复杂工作流与状态管理                 | LangGraph、Microsoft Agent Framework、Google ADK | 支持状态管理、条件分支和工作流控制             |
| 长时间运行的复杂任务                 | LangChain DeepAgents、Claude Agent SDK          | 提供任务规划、文件操作、子 Agent 等能力       |
| 企业级 Agent 系统               | Microsoft Agent Framework、LangGraph、Google ADK | 适合复杂编排、持久化执行和系统集成             |
| RAG 与知识库 Agent             | LlamaIndex、LangChain、Haystack                  | 擅长知识检索、文档处理和 RAG 集成           |
| AWS 生态开发                   | Strands Agents                                 | 与 AWS 服务集成较方便                 |
| TypeScript / JavaScript 开发 | Mastra、Vercel AI SDK                           | 适合 Web 应用和 TypeScript 技术栈     |

### 三、2026 年值得关注的框架变化

**1. Microsoft Agent Framework**

2026 年推出 1.0 正式版本，是微软整合 AutoGen 和 Semantic Kernel 技术路线后的重要框架。对于新的微软生态 Agent 项目，值得优先评估。

**2. Google ADK**

2026 年继续完善多 Agent 编排、工作流和多语言支持，适合 Google Cloud、Gemini 及跨语言 Agent 应用。

**3. LangChain DeepAgents**

相比基础的 Agent 工具调用，DeepAgents 更侧重复杂任务规划、文件系统、上下文管理和子 Agent 协作。

**4. Claude Agent SDK**

适合开发具有代码执行、文件操作、工具使用和长任务处理能力的 Agent。

**5. Strands Agents**

AWS 开源的 Agent SDK，采用模型驱动的工具使用方式，适合 AWS 生态及多模型应用。

### 四、学习建议

对于初学者，建议按照以下路线：

**原生 LLM API → Function Calling → ReAct → Memory → Agent 框架 → 多 Agent 系统**

不需要同时学习所有 Agent 框架。

先掌握工具调用、记忆机制和 ReAct 的基本原理，再选择一个框架深入学习，最后根据项目需求扩展其他框架。

**核心原则：按照项目的复杂度、技术栈、模型兼容性和控制需求选择 Agent 框架，而不是单纯根据 GitHub Star 数量选择。**

# <span style="color: #E57373;">3. OpenAI Agent SDK特点</span>

**设计原则：**

1. 具有足够的功能值得使用，但原语很少，可以快速学习
    
2. 开箱即用，并且可以自定义内部细节
    

**主要功能：**

- **代理循环**：内置代理循环，负责调用工具、将结果发送到 LLM，并循环直到 LLM 完成。
    
- **交接**：在多个代理之间进行协调和委派的强大功能。
    
- **护栏**：与代理并行运行输入验证和检查，如果检查失败则提前中断。
    
- **Python 优先**：使用内置语言功能来协调和链接代理，而不需要学习新的抽象概念。
    
- **函数工具**：将任何 Python 函数转换为工具，并具有自动模式生成和 Pydantic 支持的验证。
    
- **跟踪**：内置跟踪功能支持可视化、调试和监控您的工作流程，并配合使用 OpenAI 的评估、微调和提炼工具套件。

![[Pasted image 20261117233742.png]]

- 注：图片来源于 https://humanloop.com/blog/openai-agents-sdk