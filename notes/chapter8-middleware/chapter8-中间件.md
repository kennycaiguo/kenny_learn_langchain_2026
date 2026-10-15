# 1.中间件概述

![image-20261014191050282](./chapter8-中间件.assets/image-20261014191050282.png)

![image-20261014193335295](./chapter8-中间件.assets/image-20261014193335295.png)

## 1.1什么是中间件

![image-20261014193743054](./chapter8-中间件.assets/image-20261014193743054.png)

![image-20261014193935954](./chapter8-中间件.assets/image-20261014193935954.png)

## 1.2为什么需要中间件

### 中间件的必要性

![image-20261014202037440](./chapter8-中间件.assets/image-20261014202037440.png)

### 总结：

![image-20261014202133498](./chapter8-中间件.assets/image-20261014202133498.png)

## 1.3中间件的分类

![image-20261014202651586](./chapter8-中间件.assets/image-20261014202651586.png)

### 主要分为内置中间件和自定义中间件，内置中间件有这些

| Middleware                                                   | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [Tool retry](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#tool-retry) | Automatically retry failed tool calls with exponential backoff. |
| [Model retry](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#model-retry) | Automatically retry failed model calls with exponential backoff. |
| [Model fallback](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#model-fallback) | Automatically fallback to alternative models when primary fails. |
| [Summarization](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#summarization) | Automatically summarize conversation history when approaching token limits. |
| [Human-in-the-loop](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#human-in-the-loop) | Pause execution for human approval of tool calls.            |
| [Model call limit](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#model-call-limit) | Limit the number of model calls to prevent excessive costs.  |
| [Tool call limit](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#tool-call-limit) | Control tool execution by limiting call counts.              |
| [PII detection](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#pii-detection) | Detect and handle Personally Identifiable Information (PII). |
| [To-do list](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#to-do-list) | Equip agents with task planning and tracking capabilities.   |
| [LLM tool selector](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#llm-tool-selector) | Use an LLM to select relevant tools before calling main model. |
| [Provider tool search](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#provider-tool-search) | Defer tools behind providers’ server-side tool search, surfacing them on demand. |
| [Filesystem](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#filesystem-middleware) | Provide agents with a filesystem for storing context and long-term memories. |
| [Subagent middleware](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#subagent) | Add the ability to spawn subagents.                          |
| [Context editing](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#context-editing) | Manage conversation context by trimming or clearing tool uses. |
| [LLM tool emulator](https://docs.langchain.com/oss/javascript/langchain/middleware/built-in#llm-tool-emulator) | Emulate tool execution using an LLM for testing purposes.    |

## 1.4 和模型供应商无关的内置中间件分类

### 我们主要把他们分为6个类型

### 类型1：成本与资源控制类

![image-20261014203317312](./chapter8-中间件.assets/image-20261014203317312.png)

### 类型2：稳定性与容错保障类

![image-20261014203458862](./chapter8-中间件.assets/image-20261014203458862.png)

### 类型3： 安全与合格风控类

![image-20261014203552370](./chapter8-中间件.assets/image-20261014203552370.png)

### 类型4：决策增强与智能编排类

![image-20261014203745778](./chapter8-中间件.assets/image-20261014203745778.png)

### 类型5： 执行能力扩展类

![image-20261014203859550](./chapter8-中间件.assets/image-20261014203859550.png)

### 类型6： 开发调试与测试辅助类

![image-20261014203952437](./chapter8-中间件.assets/image-20261014203952437.png)

# 2.常用内置中间件的使用

## 2.1SummarizationMiddleware中间件

### 2.1.1 参数说明

### 2.1.2 举例1

### 2.1.3 举例2

## 2.2 HumanInTheLoopMiddleware中间件

### 2.2.1 参数说明

### 2.2.2 举例1：查看中断信息

### 2.2.3 响应中断

## 2.3PIIMiddleWare中间件

### 2.3.1 参数说明

### 2.3.2 举例1：使用内置检测器

### 2.3.3 举例2：自定义检测器/函数

## 2.4 To-do list中间件

### 2.4.1 参数说明

### 2.4.2 案例设计

### 2.4.3 代码

# 3.其他内置中间件

## 3.1 ModelCallLimitMiddleware中间件

### 举例1：整个会话限制-优雅退出

### 举例2：整个会话限制-抛异常

### 举例3：单次调用限制-优雅退出

### 举例4：单次调用限制-抛异常

## 3.2ToolCallLimitedMiddleware中间件

### 举例1：整个会话限制-优雅结束

### 举例2：整个会话限制-抛异常

### 举例3：单次调用限制-继续运行

## 3.3ModelCallbackMiddleware中间件

## 3.4 LLMToolSelectorMiddleware中间件

### 举例1

### 举例2

### 举例3

### 举例4

### 举例5

## 3.5 ToolRetryMiddleware中间件

### 举例1：带抖动

### 举例2：无抖动

## 3.6ModelRetryMiddleware中间件

### 举例1：继续运行

### 举例2：抛异常

## 3.7 LLMToolEmulator

## 3.8 ContextEditingMiddleware中间件

### 1.实验组-启用上下文编辑

### 2.对照组-不裁剪上下文

## 3.9 FileSystemSearchMiddleware中间件

## 3.10 Shell tool中间件

## 3.11 Filesystem中间件

## 3.12 Subagent中间件

# 4.多个中间件组合及执行顺序

# 5.自定义中间件

## 5.1什么是hook函数(钩子函数)

## 5.2LangChain的hook函数分类

### 类型1： Node-style hooks(节点风格钩子)

### 类型2： Wrap-style hooks(包装风格钩子)

## 5.3 Node-style hooks函数用法

### 5.3.1基本用法

#### 5.3.1.1基于装饰器实现

#### 5.3.1.2 基于类实现

### 5.3.2两种方法的统一

### 5.3.3 参数说明

### 5.3.4.返回值说明

### 5.3.5 装饰器参数：can_jump_to

#### 5.3.5.1 基于装饰器实现

#### 5.3.5.2 基于类实现

## 5.4 Wrap-style hooks函数的用法







