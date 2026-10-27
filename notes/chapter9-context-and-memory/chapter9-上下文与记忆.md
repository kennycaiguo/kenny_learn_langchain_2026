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

![image-20261026104328510](./chapter9-上下文与记忆.assets/image-20261026104328510.png)

![image-20261026104432084](./chapter9-上下文与记忆.assets/image-20261026104432084.png)

### 1.2.2 上下文类型及相关的API

![image-20261026104545147](./chapter9-上下文与记忆.assets/image-20261026104545147.png)

## 1.3 LangChain的记忆

### 1.3.1 记忆的分类

![image-20261026110433130](./chapter9-上下文与记忆.assets/image-20261026110433130.png)

### 1.3.2 记忆的管理

![image-20261026112248665](./chapter9-上下文与记忆.assets/image-20261026112248665.png)

# 2.短期记忆

![image-20261026112528589](./chapter9-上下文与记忆.assets/image-20261026112528589.png)

## 2.1 基于内存的持久化记忆

![image-20261026112553322](./chapter9-上下文与记忆.assets/image-20261026112553322.png)

### 2.1.1 举例1：没有记忆

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

agent = create_agent(model)

print("\n第1轮对话：")
resp1 = agent.invoke({"messages":[HumanMessage("你好，我叫小国")]})
for msg in resp1["messages"]:
    msg.pretty_print()

print("\n第2轮对话：")
resp1 = agent.invoke({"messages":[HumanMessage("我叫什么名字？")]})
for msg in resp1["messages"]:
    msg.pretty_print()
```

### agent输出

```

第1轮对话：
================================[1m Human Message [0m=================================

你好，我叫小国
==================================[1m Ai Message [0m==================================

你好，小国！很高兴认识你。

我是你的AI助手。请问今天有什么我可以帮到你的吗？无论是想聊天、问问题，还是需要我帮你处理一些任务，都可以随时告诉我。

第2轮对话：
================================[1m Human Message [0m=================================

我叫什么名字？
==================================[1m Ai Message [0m==================================

抱歉，作为一个人工智能，我没有权限访问您的个人信息，所以**我不知道您的名字**。

如果您愿意告诉我，我很乐意称呼您的名字！😊

```



### 2.1.2 举例2： 拥有记忆,基于checkpointer

```
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import Union, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from rich import print as rprint
from utils.tool_utils import query_weather_from_web,query_news_from_web

checkpoint = InMemorySaver()

# 1.初始化模型给中间件使用，不是agent
model = ChatOpenAI(
    # model="qwen3-vl:latest",
    # model="483025889/qwen3.5:9b",
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 3、同一个thread_id共享记忆的，不同的id就不能够共享记忆
config = {"configurable":{"thread_id":"1"}}
agent = create_agent(model,checkpointer=checkpoint)

print("\n第1轮对话：")
resp1 = agent.invoke({"messages":[HumanMessage("你好，我叫小国")]},config=config)
for msg in resp1["messages"]:
    msg.pretty_print()

print("\n第2轮对话：")
resp1 = agent.invoke({"messages":[HumanMessage("我叫什么名字？")]},config=config)
for msg in resp1["messages"]:
    msg.pretty_print()
```

### agent输出

```

第1轮对话：
================================[1m Human Message [0m=================================

你好，我叫小国
==================================[1m Ai Message [0m==================================

你好，小国！很高兴认识你。

请问今天有什么我可以帮你的吗？无论是你想聊天、咨询问题，还是需要我帮你完成某些任务，尽管告诉我！

第2轮对话：
================================[1m Human Message [0m=================================

你好，我叫小国
==================================[1m Ai Message [0m==================================

你好，小国！很高兴认识你。

请问今天有什么我可以帮你的吗？无论是你想聊天、咨询问题，还是需要我帮你完成某些任务，尽管告诉我！
================================[1m Human Message [0m=================================

我叫什么名字？
==================================[1m Ai Message [0m==================================

你叫**小国**。

```

### 用同一个thread_id再调用一次模型，它也会共享记忆

```
print("\n第3轮对话：")
resp1 = agent.invoke({"messages":[HumanMessage("我刚才问了什么问题？")]},config=config)
for msg in resp1["messages"]:
    msg.pretty_print()
```

#### agent输出

```

第3轮对话：
================================[1m Human Message [0m=================================

你好，我叫小国
==================================[1m Ai Message [0m==================================

你好，小国！很高兴认识你。

我是你的人工智能助手。请问今天有什么我可以帮你的吗？无论是你想聊聊天、问问题，还是需要我协助处理一些任务，都可以随时告诉我。
================================[1m Human Message [0m=================================

我叫什么名字？
==================================[1m Ai Message [0m==================================

你叫**小国**。刚才你刚刚才告诉我你的名字。😊
================================[1m Human Message [0m=================================

我刚才问了什么问题？
==================================[1m Ai Message [0m==================================

你刚才问的问题是：**“我叫什么名字？”**

```



### 注意：如果thread_id不一样，是不能够共享记忆的

```
config1 = {"configurable":{"thread_id":"2"}}
print("\n第4轮对话：")
resp2 = agent.invoke({"messages":[HumanMessage("我叫什么名字？")]},config=config1)
for msg in resp2["messages"]:
    msg.pretty_print()
```

#### agent输出

```
```



### 2.1.3 关键步骤说明

#### 基本步骤

![image-20261026115540183](./chapter9-上下文与记忆.assets/image-20261026115540183.png)

![image-20261026115659250](./chapter9-上下文与记忆.assets/image-20261026115659250.png)

#### 在生产环境中的情况

##### 场景1

![image-20261026120010835](./chapter9-上下文与记忆.assets/image-20261026120010835.png)

##### 场景2

![image-20261026121430823](./chapter9-上下文与记忆.assets/image-20261026121430823.png)

### 2.1.4 工作原理

### 内存保存了什么？会话记录

![image-20261026121944877](./chapter9-上下文与记忆.assets/image-20261026121944877.png)

### 自动追加历史

![image-20261026122139849](./chapter9-上下文与记忆.assets/image-20261026122139849.png)

#### 说明

![image-20261026144932864](./chapter9-上下文与记忆.assets/image-20261026144932864.png)



### 2.1.5 常见问题

#### 1.为什么agent不记得？

![image-20261026145553926](./chapter9-上下文与记忆.assets/image-20261026145553926.png)

#### 2.InMemorySaver会丢失数据吗？

![image-20261026145708377](./chapter9-上下文与记忆.assets/image-20261026145708377.png)

#### 3.内存会无限增长

![image-20261026150001306](./chapter9-上下文与记忆.assets/image-20261026150001306.png)

#### 4.如何清空某个会话的历史

![image-20261026150209840](./chapter9-上下文与记忆.assets/image-20261026150209840.png)

## 2.2 基于外部存储接着的持久化器

![image-20261026150444128](./chapter9-上下文与记忆.assets/image-20261026150444128.png)

### 一些类的使用

![image-20261026151821083](./chapter9-上下文与记忆.assets/image-20261026151821083.png)

![image-20261026151748588](./chapter9-上下文与记忆.assets/image-20261026151748588.png)

### 2.2.1 数据库环境的准备,老师使用腾讯云，我使用本地，和他的不一样。

#### 1》安装，参考：[Postgresql安装](postgres数据库安装.md)

#### 2》基本使用，参考： [Postgresql命令的使用](PostgreSQL操作-psql基本命令.md)

#### 3》python操作Postgresql： [python操作postgresql数据库](python操作postgresql数据库.md)

##### 这里也有一个简单示例,注意需要安装psycopg2： pip install psycopg2

```
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv('db_user')
db_pwd = os.getenv("db_pwd")

db_url=f"postgresql://{db_user}:{db_pwd}@localhost:5432/exampledb"
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

sql = "select * from employees;"
cursor.execute(sql)

result = cursor.fetchall()
print(result)

# [(2, 'Mary', 28, 'Secretary')]
```

#### 为了方便学习，我们需要创建一个数据库和用户,打开一个cmd窗口，输入psql -U postgres,然后输入密码，就进入postgres控制台，

![image-20261026155903250](./chapter9-上下文与记忆.assets/image-20261026155903250.png)

#### 1）先创建一个用户langchain_user,密码是abcd1234, 命令是：

```
create user langchain_user with password 'abcd1234';
```

刚刚创建错了，需要重新创建

![image-20261026160618686](./chapter9-上下文与记忆.assets/image-20261026160618686.png)

#### 2）然后创建一个数据库langchain_db,并指定所有者为langchain_user,命令如下

```
create database langchain_db owner langchain_user;
```

![image-20261026160721626](./chapter9-上下文与记忆.assets/image-20261026160721626.png)

#### 3）给用户赋权，命令如下

```
grant all privileges on database langchain_db to langchain_user;
```

![image-20261026161051698](./chapter9-上下文与记忆.assets/image-20261026161051698.png)

#### 4）查看数据库： \l

![image-20261026161334676](./chapter9-上下文与记忆.assets/image-20261026161334676.png)

#### 5)退出控制台： \q

![image-20261026161527310](./chapter9-上下文与记忆.assets/image-20261026161527310.png)

#### 6)把我们创建的用户名和密码保存到.env文件中，然后些一段代码来测试一下

```
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("PG_USER")
db_pwd = os.getenv("PG_PWD")

db_url = f"postgresql://{db_user}:{db_pwd}@localhost:5432/langchain_db?sslmode=disable"
conn = psycopg2.connect(db_url)
cursor = conn.cursor()
print(cursor)
```

#### 运行程序，可以获得cursor对象说明连接成功

![image-20261026170201202](./chapter9-上下文与记忆.assets/image-20261026170201202.png)

#### 也可以用psql命令来连接

```
psql "postgresql://langchain_user:abcd1234@localhost:5432/langchain_db?sslmode=disable"
```

![image-20261026170508177](./chapter9-上下文与记忆.assets/image-20261026170508177.png)

### 至此，数据库安装和配置成功

#### 举例：代码如下

```
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import Union, Dict, Any
from langgraph.checkpoint.postgres import PostgresSaver # 保存数据到Postgresql数据库的类
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from rich import print as rprint
from dotenv import load_dotenv
import os

load_dotenv() ## 加载.env文件，因为我们的数据库用户和密码都在里面，然后分别加载他们
db_user = os.getenv("PG_USER")
db_pwd = os.getenv("PG_PWD")
# 拼接数据库url
db_url = f"postgresql://{db_user}:{db_pwd}@localhost:5432/langchain_db?sslmode=disable"

checkpoint = InMemorySaver() # 创建了内存级的记忆存储

# 1.初始化模型给中间件使用，不是agent
model = ChatOpenAI(
    # model="qwen3-vl:latest",
    # model="483025889/qwen3.5:9b",
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

with PostgresSaver.from_conn_string(db_url) as checkpointer:
    # 初始化postgresql数据库
    checkpointer.setup()
    # 、同一个thread_id共享记忆的，不同的id就不能够共享记忆
    config = {"configurable":{"thread_id":"1"}}
    agent = create_agent(model,checkpointer=checkpointer) # checkpointer让angent有记忆能力

    resp1 = agent.invoke({"messages":[HumanMessage("你好，我是国仔")]},config=config)
    for msg in resp1["messages"]:
        msg.pretty_print()
    resp2 = agent.invoke({"messages":[HumanMessage("我是谁？")]},config=config)
    for msg in resp2["messages"]:
        msg.pretty_print()


```

#### agent输出

```
================================[1m Human Message [0m=================================

你好，我是国仔
==================================[1m Ai Message [0m==================================

你好，国仔！很高兴认识你。

我是你的 AI 助手。今天有什么我可以帮你的吗？无论是你想聊天、寻求建议、翻译文字，还是有任何问题，尽管告诉我吧！
================================[1m Human Message [0m=================================

你好，我是国仔
==================================[1m Ai Message [0m==================================

你好，国仔！很高兴认识你。

我是你的 AI 助手。今天有什么我可以帮你的吗？无论是你想聊天、寻求建议、翻译文字，还是有任何问题，尽管告诉我吧！
================================[1m Human Message [0m=================================

我是谁？
==================================[1m Ai Message [0m==================================

你是**国仔**。

你刚刚在刚才的对话中向我介绍了自己的名字。

除此之外，作为一个人工智能，我并不知道你的现实身份、个人背景或私人信息。如果你愿意分享一些关于你的兴趣、想法或者你想聊的话题，我会很乐意继续和你交流！

```

##### 用navicat查看数据库，发现生成了4个数据表，说明调用成功。持久化也成功，注意：我们不需要自己创建表，agent会自动创建

![image-20261026180904972](./chapter9-上下文与记忆.assets/image-20261026180904972.png)

### 2.2.2 查看持久化数据

![image-20261026181147385](./chapter9-上下文与记忆.assets/image-20261026181147385.png)

#### 打开一个cmd窗口，用psql来登录数据库

```
psql "postgresql://langchain_user:abcd1234@localhost:5432/langchain_db?sslmode=disable"
```

![image-20261026182149587](./chapter9-上下文与记忆.assets/image-20261026182149587.png)

#### 查看所有数据库：\l

![image-20261026181553128](./chapter9-上下文与记忆.assets/image-20261026181553128.png)

#### 查看schema： \dn

![image-20261026181722495](./chapter9-上下文与记忆.assets/image-20261026181722495.png)

#### 也可以这么用

```
select current_schema();
```

![image-20261026181850062](./chapter9-上下文与记忆.assets/image-20261026181850062.png)

#### 查看当前数据库有哪些数据表：\dt

![image-20261026182243975](./chapter9-上下文与记忆.assets/image-20261026182243975.png)

##### 注意：checkpoints是主表，非常重要



## 2.3 对比两种方式

## 2.4 记忆治理策略(上下文管理)

### 2.4.1 消息裁剪

### 2.4.2 消息删除

### 2.4.3 摘要

### 2.4.4 自定义过滤策略

## 2.5 拓展：state的理解

# 3.长期记忆

## 3.1基本理解

### 3.1.1什么是长期记忆？

### 3.1.2 类型划分

### 3.1.3 存储方式

### 3.1.4 存储架构

## 3.2基础API的使用

### 3.2.1 put()/get(): 写入/读取

#### ①put()源码剖析

#### ②get()源码剖析

#### ③举例1：基于InMemoryStore

#### ④举例2：基于PostgresStore

### 3.2.2 search():搜索API

#### ①源码剖析

#### ②举例1：按照namespace前缀搜索

#### ③举例2：按照filter过滤

#### ④举例3：按照语义搜索
