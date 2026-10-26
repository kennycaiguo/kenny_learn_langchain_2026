# 1.概述

## 1.1 为什么需要记忆(Memory)

![image-20261025195843130](./chapter9-上下文与记忆.assets/image-20261025195843130.png)

### 举例，情况1：我们先创建一个agent，然后和他进行交互

```
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import Union, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.config import get_stream_writer
from rich import print as rprint
from utils.tool_utils import query_weather_from_web,query_news_from_web

# 1.初始化模型给中间件使用，不是agent
model = ChatOpenAI(
    # model="qwen3-vl:latest",
    # model="483025889/qwen3.5:9b",
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

messages1 = [
    HumanMessage("你好，我叫小明"),
    AIMessage("很高兴认识你，小明"),
    HumanMessage("你用一句话介绍下你自己"),
]
# 2.创建agent
agent = create_agent(model)

resp = agent.invoke({"messages": messages1})
for msg in resp["messages"]:
    msg.pretty_print()


```

#### agent输出

```
================================[1m Human Message [0m=================================

你好，我叫小明
==================================[1m Ai Message [0m==================================

很高兴认识你，小明
================================[1m Human Message [0m=================================

你用一句话介绍下你自己
==================================[1m Ai Message [0m==================================

我是一个由 Google 训练的大型语言模型，旨在协助你处理各种任务、回答问题并提供创意支持。

```

### 然后我们再来调用一次agent，用户问他：我是谁

```
messages2 = [
    HumanMessage("我叫什么名字？"),
]

resp = agent.invoke({"messages":messages2})
for msg in resp["messages"]:
    msg.pretty_print()
```

#### 然后agent就不记得用户是谁

```
================================[1m Human Message [0m=================================

我叫什么名字？
==================================[1m Ai Message [0m==================================

抱歉，因为我是一个人工智能，除非你之前告诉过我，否则我不知道你的名字。

如果你愿意的话，可以告诉我你的名字，这样我就能称呼你啦！

```

### 情况2，问题和答案在同一个列表里面，agent可以在同一个列表里面找到答案

```
messages3 = [
    HumanMessage("你好，我叫小明"),
    AIMessage("很高兴认识你，小明"),
    HumanMessage("你用一句话介绍下你自己"),
    AIMessage("我是一个由 OpenAI 训练的人工智能助手，可以帮你回答问题、写作和解决各种任务。"),
    HumanMessage("我叫什么名字？")
]

response3 = agent.invoke({"messages" : messages3})

for msg in response3["messages"]:
    msg.pretty_print()
```

#### agent 输出

```
================================[1m Human Message [0m=================================

你好，我叫小明
==================================[1m Ai Message [0m==================================

很高兴认识你，小明
================================[1m Human Message [0m=================================

你用一句话介绍下你自己
==================================[1m Ai Message [0m==================================

我是一个由 OpenAI 训练的人工智能助手，可以帮你回答问题、写作和解决各种任务。
================================[1m Human Message [0m=================================

我叫什么名字？
==================================[1m Ai Message [0m==================================

你叫小明。

```

### 我们需要agent有记忆

![image-20261025200909942](./chapter9-上下文与记忆.assets/image-20261025200909942.png)


## 1.2 如何解决记忆问题

### 1.2.1 上下文工程

### 1.2.2 上下文类型及相关的API

## 1.3 LangChain的记忆

### 1.3.1 记忆的分类

### 1.3.2 记忆的管理

# 2.短期记忆

## 2.1 基于内存的持久化记忆

### 2.1.1 举例1：没有记忆

### 2.1.2 举例2： 拥有记忆

### 2.1.3 关键步骤说明

### 2.1.4 工作原理

### 2.1.5 常见问题

## 2.2 基于外部存储接着的持久化器

### 2.2.1 数据库环境的准备

### 2.2.2 代码实现

### 2.2.3 查看持久化数据

## 2.3 对比两种方式

## 2.4 记忆治理策略(上下文管理)

### 2.4.1 消息裁剪

### 2.4.2 消息删除

### 2.4.3 摘要

### 2.4.4 自定义过滤策略

## 2.5 拓展：state的理解

