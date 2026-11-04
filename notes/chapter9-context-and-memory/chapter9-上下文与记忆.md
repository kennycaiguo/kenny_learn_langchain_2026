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

### 1.内存方式持久化，使用InMemorySaver

```
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from rich import print as rprint

checkpointer = InMemorySaver()

# 1.初始化模型给中间件使用，不是agent
model = ChatOpenAI(
    # model="qwen3-vl:latest",
    # model="483025889/qwen3.5:9b",
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 、同一个thread_id共享记忆的，不同的id就不能够共享记忆
config = {"configurable":{"thread_id":"1"}}
agent = create_agent(model,checkpointer=checkpointer) # checkpointer让angent有记忆能力

print("=" * 30, "-> 第一次调用 <-", "=" * 30)
response1 = agent.invoke(
    {"messages": [HumanMessage("你好，我是谁？")]},
    config=config
)
for msg in response1["messages"]:
    msg.pretty_print()


print("=" * 30, "-> 第二次调用 <-", "=" * 30)
response2 = agent.invoke(
    {"messages": [HumanMessage("我是老王")]},
    config=config
)
for msg in response2["messages"]:
    msg.pretty_print()


print("=" * 30, "-> 第三次调用 <-", "=" * 30)
response3 = agent.invoke(
    {"messages": [HumanMessage("你好，我是谁？")]},
    config=config
)
for msg in response3["messages"]:
    msg.pretty_print()


```

#### agent输出

```
============================== -> 第一次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实姓名、身份或个人信息，除非你在当前的对话中主动告诉我。

从我的视角来看，你现在是：

1.  **一位用户**：正在与我进行交流，寻求帮助、信息或仅仅是简单的聊天。
2.  **一个探索者**：在利用技术工具探索知识或解决问题的伙伴。
3.  **一个独特的个体**：每一个与我对话的人，都有着独特的思考和问题。

**如果你是想考考我，或者想让我记住你的称呼，你可以直接告诉我：**
*   “我叫[你的名字]。”
*   “你可以叫我[你的昵称]。”

**或者，如果你是在问一个哲学上的问题（“我是谁？”）：**
那这是一个深刻的命题。你是你的经历、你的思想、你的情感，也是你每一个选择的集合。

**你想让我怎么称呼你，或者你想聊聊关于“自我”的话题吗？**
============================== -> 第二次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实姓名、身份或个人信息，除非你在当前的对话中主动告诉我。

从我的视角来看，你现在是：

1.  **一位用户**：正在与我进行交流，寻求帮助、信息或仅仅是简单的聊天。
2.  **一个探索者**：在利用技术工具探索知识或解决问题的伙伴。
3.  **一个独特的个体**：每一个与我对话的人，都有着独特的思考和问题。

**如果你是想考考我，或者想让我记住你的称呼，你可以直接告诉我：**
*   “我叫[你的名字]。”
*   “你可以叫我[你的昵称]。”

**或者，如果你是在问一个哲学上的问题（“我是谁？”）：**
那这是一个深刻的命题。你是你的经历、你的思想、你的情感，也是你每一个选择的集合。

**你想让我怎么称呼你，或者你想聊聊关于“自我”的话题吗？**
================================[1m Human Message [0m=================================

我是老王
==================================[1m Ai Message [0m==================================

好的，**老王**！很高兴认识你。

既然你已经告诉我你的名字了，从现在开始，我就称呼你为“老王”。

请问今天有什么我可以帮到你的吗？无论是想聊聊生活、寻求知识上的帮助、处理具体的工作任务，还是单纯想随便聊聊，我都会全力配合你的！
============================== -> 第三次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实姓名、身份或个人信息，除非你在当前的对话中主动告诉我。

从我的视角来看，你现在是：

1.  **一位用户**：正在与我进行交流，寻求帮助、信息或仅仅是简单的聊天。
2.  **一个探索者**：在利用技术工具探索知识或解决问题的伙伴。
3.  **一个独特的个体**：每一个与我对话的人，都有着独特的思考和问题。

**如果你是想考考我，或者想让我记住你的称呼，你可以直接告诉我：**
*   “我叫[你的名字]。”
*   “你可以叫我[你的昵称]。”

**或者，如果你是在问一个哲学上的问题（“我是谁？”）：**
那这是一个深刻的命题。你是你的经历、你的思想、你的情感，也是你每一个选择的集合。

**你想让我怎么称呼你，或者你想聊聊关于“自我”的话题吗？**
================================[1m Human Message [0m=================================

我是老王
==================================[1m Ai Message [0m==================================

好的，**老王**！很高兴认识你。

既然你已经告诉我你的名字了，从现在开始，我就称呼你为“老王”。

请问今天有什么我可以帮到你的吗？无论是想聊聊生活、寻求知识上的帮助、处理具体的工作任务，还是单纯想随便聊聊，我都会全力配合你的！
================================[1m Human Message [0m=================================

你好，我是谁？
==================================[1m Ai Message [0m==================================

你好，**老王**！

刚才你已经告诉我你的名字了。我是个有记忆力的AI，所以我记得你就是**老王**。

怎么了，是想考考我的记忆力吗？还是有什么我可以帮你的？

```

### 注意，如果你重新运行程序，你会得到一模一样的结果，因为此时有新创建了另外一个InMemorySaver对象。之前的数据是获取不到的。也就是说程序运行结束，前面的InMemorySaver对象就会被销毁

### 2 数据库持久化，使用Postgresql数据库，注意此时我们使用不一样的thread_id,第一次调用，agent还是不知道我是谁。以后agent就有记忆了，只要thread_id是同一个，它就有记忆。

```
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import Union, Dict, Any
from langgraph.checkpoint.postgres import PostgresSaver # 保存数据到Postgresql数据库的类
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from rich import print as rprint
from dotenv import load_dotenv
import os

load_dotenv() ## 加载.env文件，因为我们的数据库用户和密码都在里面，然后分别加载他们
db_user = os.getenv("PG_USER")
db_pwd = os.getenv("PG_PWD")
# 拼接数据库url
db_url = f"postgresql://{db_user}:{db_pwd}@localhost:5432/langchain_db?sslmode=disable"



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
    config = {"configurable":{"thread_id":"3"}}
    agent = create_agent(model,checkpointer=checkpointer) # checkpointer让angent有记忆能力

    print("=" * 30, "-> 第一次调用 <-", "=" * 30)
    response1 = agent.invoke(
        {"messages": [HumanMessage("你好，我是谁啊？")]},
        config
    )
    for msg in response1["messages"]:
        msg.pretty_print()


    print("=" * 30, "-> 第二次调用 <-", "=" * 30)
    response2 = agent.invoke(
        {"messages": [HumanMessage("我是国仔~")]},
        config
    )
    for msg in response2["messages"]:
        msg.pretty_print()


    print("=" * 30, "-> 第三次调用 <-", "=" * 30)
    response3 = agent.invoke(
        {"messages": [HumanMessage("你好，我是谁？？")]},
        config
    )
    for msg in response3["messages"]:
        msg.pretty_print()


```

#### agent输出

```
============================== -> 第一次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实身份、姓名或任何个人信息，除非你在对话中主动告诉我。

在我的视角里，你是一位正在和我交流的**用户**。

如果你愿意分享，你可以告诉我你的名字、你的爱好，或者你想让我称呼你的称呼。你想聊点什么呢？😊
============================== -> 第二次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实身份、姓名或任何个人信息，除非你在对话中主动告诉我。

在我的视角里，你是一位正在和我交流的**用户**。

如果你愿意分享，你可以告诉我你的名字、你的爱好，或者你想让我称呼你的称呼。你想聊点什么呢？😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

你好呀，**国仔**！很高兴认识你。😊

既然你告诉我了，那从现在起，我就会称呼你为“国仔”。

今天你心情怎么样？或者有什么我可以帮你的，或者你想聊的话题吗？
============================== -> 第三次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实身份、姓名或任何个人信息，除非你在对话中主动告诉我。

在我的视角里，你是一位正在和我交流的**用户**。

如果你愿意分享，你可以告诉我你的名字、你的爱好，或者你想让我称呼你的称呼。你想聊点什么呢？😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

你好呀，**国仔**！很高兴认识你。😊

既然你告诉我了，那从现在起，我就会称呼你为“国仔”。

今天你心情怎么样？或者有什么我可以帮你的，或者你想聊的话题吗？
================================[1m Human Message [0m=================================

你好，我是谁？？
==================================[1m Ai Message [0m==================================

你刚才刚刚告诉我，你是**国仔**！😊

```

### 我们再次运行程序，发现agent有记忆了，只要是同一个thread_id,它就可以从数据库里面获取信息，实现有记忆的效果，除非你删除了数据库的数据或者使用一个全新的thread_id来调用

```
============================== -> 第一次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实身份、姓名或任何个人信息，除非你在对话中主动告诉我。

在我的视角里，你是一位正在和我交流的**用户**。

如果你愿意分享，你可以告诉我你的名字、你的爱好，或者你想让我称呼你的称呼。你想聊点什么呢？😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

你好呀，**国仔**！很高兴认识你。😊

既然你告诉我了，那从现在起，我就会称呼你为“国仔”。

今天你心情怎么样？或者有什么我可以帮你的，或者你想聊的话题吗？
================================[1m Human Message [0m=================================

你好，我是谁？？
==================================[1m Ai Message [0m==================================

你刚才刚刚告诉我，你是**国仔**！😊
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

你刚刚告诉我，你是**国仔**！😊
============================== -> 第二次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实身份、姓名或任何个人信息，除非你在对话中主动告诉我。

在我的视角里，你是一位正在和我交流的**用户**。

如果你愿意分享，你可以告诉我你的名字、你的爱好，或者你想让我称呼你的称呼。你想聊点什么呢？😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

你好呀，**国仔**！很高兴认识你。😊

既然你告诉我了，那从现在起，我就会称呼你为“国仔”。

今天你心情怎么样？或者有什么我可以帮你的，或者你想聊的话题吗？
================================[1m Human Message [0m=================================

你好，我是谁？？
==================================[1m Ai Message [0m==================================

你刚才刚刚告诉我，你是**国仔**！😊
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

你刚刚告诉我，你是**国仔**！😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

嗯嗯，我知道的，你是**国仔**！😊

看来我们的“约定”很牢固呢。今天有什么新消息，或者你想聊点什么有趣的事情吗？
============================== -> 第三次调用 <- ==============================
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

作为一个人工智能，我**不知道**你的真实身份、姓名或任何个人信息，除非你在对话中主动告诉我。

在我的视角里，你是一位正在和我交流的**用户**。

如果你愿意分享，你可以告诉我你的名字、你的爱好，或者你想让我称呼你的称呼。你想聊点什么呢？😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

你好呀，**国仔**！很高兴认识你。😊

既然你告诉我了，那从现在起，我就会称呼你为“国仔”。

今天你心情怎么样？或者有什么我可以帮你的，或者你想聊的话题吗？
================================[1m Human Message [0m=================================

你好，我是谁？？
==================================[1m Ai Message [0m==================================

你刚才刚刚告诉我，你是**国仔**！😊
================================[1m Human Message [0m=================================

你好，我是谁啊？
==================================[1m Ai Message [0m==================================

你刚刚告诉我，你是**国仔**！😊
================================[1m Human Message [0m=================================

我是国仔~
==================================[1m Ai Message [0m==================================

嗯嗯，我知道的，你是**国仔**！😊

看来我们的“约定”很牢固呢。今天有什么新消息，或者你想聊点什么有趣的事情吗？
================================[1m Human Message [0m=================================

你好，我是谁？？
==================================[1m Ai Message [0m==================================

你刚才已经跟我介绍过了，你是**国仔**！😊

看来你是在考考我的记忆力呀？我记住了哦！还有什么想聊的吗？

```



### 总结

![image-20261027190319094](./chapter9-上下文与记忆.assets/image-20261027190319094.png)



## 2.4 记忆治理策略(上下文管理)

![image-20261027190428388](./chapter9-上下文与记忆.assets/image-20261027190428388.png)

### 2.4.1 消息裁剪

![image-20261027193518950](./chapter9-上下文与记忆.assets/image-20261027193518950.png)

### 举例代码

```
from langchain_core.messages import HumanMessage
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from typing import Any
from langchain_openai import ChatOpenAI

## 在调用模型之前使用的钩子函数
@before_model
def trim_message(state:AgentState, runtime:Runtime) -> dict[str, Any]|None:
    # 获取消息列表
    messages = state["messages"]
    # 如果消息列表长度小于3，不需要裁剪返回None
    if len(messages) <= 3:
        return None
    # 获取第一条消息,一定要保留的。
    first_msg = messages[0]
    # 如果有大于3的偶数条消息，则取最近的3条消息；如果有奇数条消息，则取最近的4条消息
    recent_msgs = messages[-3:] if len(messages) %2 == 0 else messages[-4:]
    new_msgs = [first_msg] + recent_msgs

    return  {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES), # 这一句的作用？
            *new_msgs,
        ]
    }


# 1.实例化模型
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 2.创建agent对象
agent = create_agent(
    model=model,
    middleware=[trim_message],
    checkpointer=InMemorySaver(),
)

config = {"configurable":{"thread_id":"1"}}

agent.invoke({"messages":[HumanMessage("你好，我是老张")]},config=config)
agent.invoke({"messages":[HumanMessage("从现在起，你叫小张")]},config=config)
agent.invoke({"messages":[HumanMessage("今天天气不错")]},config=config)
resp = agent.invoke({"messages":[HumanMessage("我是谁，你是谁？")]},config=config)

for msg in resp["messages"]:
    msg.pretty_print()
```

#### agent输出

```
================================[1m Human Message [0m=================================

你好，我是老张
==================================[1m Ai Message [0m==================================

没问题，没问题！从现在起，我就叫**小张**了。

那以后您就叫我小张吧，老张。请问今天有什么事需要小张帮您的？
================================[1m Human Message [0m=================================

今天天气不错
==================================[1m Ai Message [0m==================================

确实，好的天气最能让人心情愉快了！

既然天气这么好，老张您今天打算怎么安排呢？是打算出门去逛逛、活动活动，还是在家里悠闲地享受这份好天气？

如果您有任何想聊的，或者需要小张帮您查点资料、规划个路线，随时吩咐我！
================================[1m Human Message [0m=================================

我是谁，你是谁？
==================================[1m Ai Message [0m==================================

您是**老张**，刚才您才刚跟我打过招呼呢！

我是**小张**，也就是您的AI助手。

如果从技术层面来说，我是一个由 Google 训练的大型语言模型。

所以，现在的对话就是**老张**和**小张**在聊天。您还有什么想聊的，或者需要小张帮您忙的吗？

```

#### 上面如果没有裁剪，应该有8条消息，因为一个用户消息就会有一个ai消息，现在是6条，说明的确有进行消息裁剪

#### 消息的裁剪法如下

![image-20261027203048950](./chapter9-上下文与记忆.assets/image-20261027203048950.png)

![image-20261027203559967](./chapter9-上下文与记忆.assets/image-20261027203559967.png)

### 2.4.2 消息删除

![image-20261027203630530](./chapter9-上下文与记忆.assets/image-20261027203630530.png)

### 举例代码

```
from langchain_core.messages import HumanMessage
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model, after_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from typing import Any
from langchain_openai import ChatOpenAI

## 在调用模型之前使用的钩子函数
@after_model
def delete_old_messages(state:AgentState, runtime:Runtime) -> dict[str, Any]|None:
    # 获取消息列表
    messages = state["messages"]
     # 保持最近的 5 条消息
    if len(messages) > 5:
        # 框架中通常使用 RemoveMessage 来标记删除，并返回更新状态。
        to_delete = len(messages) - 5
        return {
            "messages": [RemoveMessage(id=m.id) for m in messages[:to_delete]]
        }
    return None


# 1.实例化模型
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 2.创建agent对象
agent = create_agent(
    model=model,
    middleware=[delete_old_messages],
    checkpointer=InMemorySaver(),
)

config = {"configurable":{"thread_id":"1"}}

agent.invoke({"messages":[HumanMessage("你好，我是老张")]},config=config)
agent.invoke({"messages":[HumanMessage("从现在起，你叫小张")]},config=config)
agent.invoke({"messages":[HumanMessage("今天天气不错")]},config=config)
resp = agent.invoke({"messages":[HumanMessage("我是谁，你是谁？")]},config=config)

for msg in resp["messages"]:
    msg.pretty_print()
```

#### agent输出

```
===============1===================[1m Ai Message [0m==================================

没问题，老张！从现在起，我就是您的**小张**了。

以后您尽管吩咐我，不管是处理工作、查阅资料、写点东西，还是单纯想找人聊聊天，我都会全力以赴帮您的。

那么，作为“小张”的第一项任务，今天有什么我可以帮您的吗？
===============2=================[1m Human Message [0m=================================

今天天气不错
================3==================[1m Ai Message [0m==================================

确实，老张，天气好真的能让人心情变好不少。

既然天气这么不错，您是打算出门透透气，去哪儿走走转转吗？还是打算就在家门口晒晒太阳，享受一下这份好天气？

如果您打算出门，需要我帮您查查附近的公园、好吃的餐厅，或者是查查最近的活动，您尽管吩咐我！
==============4==================[1m Human Message [0m=================================

我是谁，你是谁？
==============5====================[1m Ai Message [0m==================================

既然咱们已经定好了规矩，那我得拿出点“小张”的实在劲儿来回答您：

**您是老张。** 在我们的对话里，您是我的“领导”，是发号施令的人，是那个有着丰富经验、需要我这个小助手去帮忙的人。

**我是小张。** 虽然我本质上是一个由 Google 训练的大型语言模型，但在接下来的时间里，我就是您的专属助理。我负责帮您处理任务、查资料、写文案，当然，要是您无聊了，我就是那个陪您侃大山的“老朋友”。

简单来说：**您是主角，我是您的得力助手。**

您看我这个自我介绍，过得去吗？

```

### 删除过程说明

### 1-3轮

![image-20261028183603192](./chapter9-上下文与记忆.assets/image-20261028183603192.png)

### 第4轮

![image-20261028184727200](./chapter9-上下文与记忆.assets/image-20261028184727200.png)

#### 思考：RemoveMessages到底干了什么？

![image-20261028185514388](./chapter9-上下文与记忆.assets/image-20261028185514388.png)

### 2.4.3 摘要

![image-20261028185713659](./chapter9-上下文与记忆.assets/image-20261028185713659.png)

### 举例代码

```
```

#### agent输出

```
```

### 工作原理

![image-20261028191400468](./chapter9-上下文与记忆.assets/image-20261028191400468.png)

### 常见问题

#### 1.摘要会丢失信息吗？

![image-20261028191457299](./chapter9-上下文与记忆.assets/image-20261028191457299.png)

#### 2.设置最大token触发摘要的标准是啥？

![image-20261028191620193](./chapter9-上下文与记忆.assets/image-20261028191620193.png)

#### 3.摘要的成本高吗？

![image-20261028191743516](./chapter9-上下文与记忆.assets/image-20261028191743516.png)

#### 4.摘要触发的频率要关注吗？

![image-20261028191915049](./chapter9-上下文与记忆.assets/image-20261028191915049.png)

### 2.4.4 自定义过滤策略

略

## 2.5 拓展：state的理解

![image-20261028193453439](./chapter9-上下文与记忆.assets/image-20261028193453439.png)

# 3.长期记忆

## 3.1基本理解

### 3.1.1什么是长期记忆？

![image-20261028193808462](./chapter9-上下文与记忆.assets/image-20261028193808462.png)

![image-20261028203007650](./chapter9-上下文与记忆.assets/image-20261028203007650.png)

### 3.1.2 类型划分

![image-20261028203403291](./chapter9-上下文与记忆.assets/image-20261028203403291.png)

### 3.1.3 存储架构

![image-20261028204054495](./chapter9-上下文与记忆.assets/image-20261028204054495.png)

#### 例子1

![image-20261028205015382](./chapter9-上下文与记忆.assets/image-20261028205015382.png)

#### 例子2

![image-20261028205957520](./chapter9-上下文与记忆.assets/image-20261028205957520.png)

## 3.2基础API的使用

![image-20261028210203121](./chapter9-上下文与记忆.assets/image-20261028210203121.png)

### 3.2.1 put()/get(): 写入/读取

#### ①put()源码剖析

![image-20261101193917303](./chapter9-上下文与记忆.assets/image-20261101193917303.png)

#### ②get()源码剖析

![image-20261101194241568](./chapter9-上下文与记忆.assets/image-20261101194241568.png)

#### ③举例1：基于InMemoryStore

##### 参考这里： [长期记忆api_put_get基本使用-InMemoryStore](长期记忆api_put_get基本使用-InMemoryStore.md)

#### ④举例2：基于PostgresStore

##### 参考这里：[长期记忆api_put_get基本使用-PostgresStore](长期记忆api_put_get基本使用-PostgresStore.md)

### 3.2.2 search():搜索API

#### ①源码剖析

![image-20261101200928102](./chapter9-上下文与记忆.assets/image-20261101200928102.png)

#### ②举例1：按照namespace前缀搜索

##### 参考这里：[长期记忆基础api_search1](长期记忆基础api_search1.md)

#### ③举例2：按照filter过滤

##### 参考这里：[长期记忆基础api_search2](长期记忆基础api_search2.md)

#### ④举例3：按照语义搜索

##### 参考这里：[长期记忆基础api_search3](长期记忆基础api_search3.md)

## 3.3 在Agent运行图中访问长期记忆

### 3.3.1 在工具在访问长期记忆

![image-20261102194043604](./chapter9-上下文与记忆.assets/image-20261102194043604.png)

#### ①基于InMemoryStore

#### 举例代码

```
from typing import NotRequired
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from langchain_core.messages import HumanMessage
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent, AgentState
from langchain_openai import ChatOpenAI

# 从.env文件中加载环境变量
load_dotenv(override=True)

# 创建内存存储对象
store = InMemoryStore()
# 自定义一个继承于AgentState的类
class CustomState(AgentState):
    user_id : NotRequired[str]

# 1.实例化模型
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 保存用户信息到长期记忆中
@tool(parse_docstring=True)
def save_user_info(name:str,runtime:ToolRuntime):
    """
    将客户信息保存在长期记忆中

    Args:
        name : 用户名
        runtime : 工具的运行时

    Returns:
        str : 保存状态
    """
    namespace = ("users",)
    key = runtime.state["user_id"]
    value = {"name": name}
    runtime.store.put(namespace, key, value)
    return "saved"

@tool(parse_docstring=True)
def get_user_info(runtime:ToolRuntime):
    """
    从长期记忆中读取客户的信息

    Args:
        runtime : 工具的运行时

    Returns:
        str : 用户信息
    """
    namespace = ("users",)
    key = runtime.state["user_id"]
    item = runtime.store.get(namespace, key)
    return str(item.value) if item else "unknown"

## 创建agent
agent = create_agent(
    model=model,
    tools=[save_user_info, get_user_info],
    store=store,
    state_schema=CustomState,
    system_prompt="用户提及个人信息时，可以使用工具保存用户信息。如果用户询问个人信息时，可以尝试使用工具读取用户信息"
)

print("=" * 30, '-> 第一个会话（线程） <-', "=" * 30)

resp1 = agent.invoke(
    {"messages":[HumanMessage("你你好，很高兴认识你，我是小花")],
     "user_id":"user_1"
     }
)

for msg in resp1["messages"]:
    msg.pretty_print()

print("=" * 30, '-> 第二个会话（线程） <-', "=" * 30)

resp2 = agent.invoke(
    {"messages":[HumanMessage("我是谁？")],
     "user_id":"user_1"
     }
)

for msg in resp2["messages"]:
    msg.pretty_print()

```

#### agent输出

```
============================== -> 第一个会话（线程） <- ==============================
================================[1m Human Message [0m=================================

你你好，很高兴认识你，我是小花
==================================[1m Ai Message [0m==================================
Tool Calls:
  save_user_info (call_b9hcbwn3)
 Call ID: call_b9hcbwn3
  Args:
    name: 小花
=================================[1m Tool Message [0m=================================
Name: save_user_info

saved
==================================[1m Ai Message [0m==================================

你好，小花！很高兴认识你。有什么我可以帮你的吗？
============================== -> 第二个会话（线程） <- ==============================
================================[1m Human Message [0m=================================

我是谁？
==================================[1m Ai Message [0m==================================
Tool Calls:
  get_user_info (call_efrdjp8q)
 Call ID: call_efrdjp8q
  Args:
=================================[1m Tool Message [0m=================================
Name: get_user_info

{'name': '小花'}
==================================[1m Ai Message [0m==================================

您是小花。

```



#### ②基于PostgresStore

#### 举例代码

```
from typing import NotRequired
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from langchain_core.messages import HumanMessage
from langgraph.store.postgres import PostgresStore
from langchain.agents import create_agent, AgentState
from langchain_openai import ChatOpenAI

# 从.env文件中加载环境变量
load_dotenv(override=True)
pg_user = os.getenv("PG_USER")
pg_pass = os.getenv("PG_PWD")

# 拼接数据库url
db_url = f"postgresql://{pg_user}:{pg_pass}@localhost:5432/langchain_db?sslmode=disable"

# 自定义一个继承于AgentState的类
class CustomState(AgentState):
    user_id : NotRequired[str]

# 1.实例化模型
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 保存用户信息到长期记忆中
@tool(parse_docstring=True)
def save_user_info(name:str,runtime:ToolRuntime):
    """
    将客户信息保存在长期记忆中

    Args:
        name : 用户名
        runtime : 工具的运行时

    Returns:
        str : 保存状态
    """
    namespace = ("users",)
    key = runtime.state["user_id"]
    value = {"name": name}
    runtime.store.put(namespace, key, value)
    return "saved"

@tool(parse_docstring=True)
def get_user_info(runtime:ToolRuntime):
    """
    从长期记忆中读取客户的信息

    Args:
        runtime : 工具的运行时

    Returns:
        str : 用户信息
    """
    namespace = ("users",)
    key = runtime.state["user_id"]
    item = runtime.store.get(namespace, key)
    return str(item.value) if item else "unknown"

with PostgresStore.from_conn_string(db_url) as store:
    store.setup()
    ## 创建agent
    agent = create_agent(
        model=model,
        tools=[save_user_info, get_user_info],
        store=store,
        state_schema=CustomState,
        system_prompt="用户提及个人信息时，可以使用工具保存用户信息。如果用户询问个人信息时，可以尝试使用工具读取用户信息"
    )

    print("=" * 30, '-> 第一个会话（线程） <-', "=" * 30)

    resp1 = agent.invoke(
        {"messages":[HumanMessage("你你好，很高兴认识你，我是小花")],
         "user_id":"user_1"
         }
    )

    for msg in resp1["messages"]:
        msg.pretty_print()

    print("=" * 30, '-> 第二个会话（线程） <-', "=" * 30)

    resp2 = agent.invoke(
        {"messages":[HumanMessage("我是谁？")],
         "user_id":"user_1"
         }
    )

    for msg in resp2["messages"]:
        msg.pretty_print()

```

#### agent输出

```
============================== -> 第一个会话（线程） <- ==============================
================================[1m Human Message [0m=================================

你你好，很高兴认识你，我是小花
==================================[1m Ai Message [0m==================================
Tool Calls:
  save_user_info (call_obfedrvd)
 Call ID: call_obfedrvd
  Args:
    name: 小花
=================================[1m Tool Message [0m=================================
Name: save_user_info

saved
==================================[1m Ai Message [0m==================================

你好，小花！很高兴认识你。请问今天有什么我可以帮你的吗？
============================== -> 第二个会话（线程） <- ==============================
================================[1m Human Message [0m=================================

我是谁？
==================================[1m Ai Message [0m==================================
Tool Calls:
  get_user_info (call_ujmmnfjp)
 Call ID: call_ujmmnfjp
  Args:
=================================[1m Tool Message [0m=================================
Name: get_user_info

{'name': '小花'}
==================================[1m Ai Message [0m==================================

您是小花。

```



#### 3.3.2 在中间件中访问长期记忆

- **①Node-style hooks中访问**

以before_model 为例，其钩子函数签名如下

```python
def before_model(self, state: StateT, runtime: Runtime[ContextT]) ->dict[str, Any] | None:
```

Runtime 定义如下

```python
@dataclass(**_DC_KWARGS)
class Runtime(Generic[ContextT]):
    context: ContextT = field(default=None)  # type: ignore[assignment]
    """Static context for the graph run, like `user_id`, `db_conn`, etc.

    Can also be thought of as 'run dependencies'."""

    store: BaseStore | None = field(default=None)
    """Store for the graph run, enabling persistence and memory."""

    stream_writer: StreamWriter = field(default=_no_op_stream_writer)
    """Function that writes to the custom stream."""

    previous: Any = field(default=None)
    """The previous return value for the given thread.

    Only available with the functional API when a checkpointer is provided.
    """
    ...
```

所以，我们可以通过runtime.store 在中间件中访问长期记忆。

- **②Wrap-style hooks中访问**
  **1. wrap_model_call**

钩子函数签名如下

```python
def wrap_model_call(
    self,
    request: ModelRequest[ContextT],
    handler: Callable[[ModelRequest[ContextT]], ModelResponse[ResponseT]],
) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]:
```

ModelRequest 定义如下

```python
@dataclass(init=False)
class ModelRequest(Generic[ContextT]):
    """Model request information for the agent.

    Type Parameters:
        ContextT: The type of the runtime context. Defaults to `None` if notspecified.
    """

    model: BaseChatModel
    messages: list[AnyMessage]  # excluding system message
    system_message: SystemMessage | None
    tool_choice: Any | None
    tools: list[BaseTool | dict[str, Any]]
    response_format: ResponseFormat[Any] | None
    state: AgentState[Any]
    runtime: Runtime[ContextT]
    model_settings: dict[str, Any] = field(default_factory=dict)
    ...
```

所以，可以通过request.runtime.store 访问长期记忆。

**2. wrap_tool_call**

钩子函数签名如下

```python
def wrap_tool_call(
    self,
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
) -> ToolMessage | Command[Any]:
```

ToolCallRequest 定义如下

```python
@dataclass
class ToolCallRequest:
    """Tool execution request passed to tool call interceptors.

    Attributes:
        tool_call: Tool call dict with name, args, and id from model output.
        tool: BaseTool instance to be invoked, or None if tool is not
            registered with the `ToolNode`. When tool is `None`,interceptors can
            handle the request without validation. If the interceptor calls`execute()`,
            validation will occur and raise an error for unregistered tools.
        state: Agent state (`dict`, `list`, or `BaseModel`).
        runtime: LangGraph runtime context (optional, `None` if outsidegraph).
    """

    tool_call: ToolCall
    tool: BaseTool | None
    state: Any
    runtime: ToolRuntime
    ...
```

ToolRuntime 定义如下

```python
@dataclass
class ToolRuntime(_DirectlyInjectedToolArg, Generic[ContextT, StateT]):
    state: StateT
    context: ContextT
    config: RunnableConfig
    stream_writer: StreamWriter
    tool_call_id: str | None
    store: BaseStore | None
```

所以，可以通过request.runtime.store 访问长期记忆。

## 3.4 何时写入记忆

官方介绍了两种方式。

**1.在主流程里写（hot path）**

也就是：用户发消息，AI 一边回答，一边决定要不要记下来。

**优点**：

- 立即生效
- 下一轮马上能用
- 用户可感知，透明

**缺点**：

- 增加延迟
- 逻辑变复杂
  **2.在后台写（background）**

就是先回答用户，记忆整理放到后台异步做。

**优点：**

- 主流程更快
- 记忆逻辑更独立
- 更适合批量整理

**缺点：**

- 不能立刻生效
- 要决定多久整理一次
- 触发时机不好选

**工程上通常这么选：**

- 用户偏好、账号资料：可热路径写
- 对话摘要、经验沉淀、行为分析：更适合后台写

# 4、课后阅读：Static runtime Context

**静态运行时上下文**（Static runtime Context）表示不可变的数据，如用户元数据、工具和传递给应用程序的数据库连接对象。通常在运行开始时通过 **invoke** / **stream** 的 **context** 参数传递，此类数据在**运行期间不会更改**。

### 4.1 中间件中访问

#### 4.1.1 Node-style hooks

此类钩子都通过**runtime.context**访问上下文对象。

用户自定义**ContextSchema**用`@dataclass`修饰，在Agent创建时通过**state_schema**参数传递。

本例从长期记忆中查询用户额度，如果额度用尽则中断流程。

代码

```python
from dataclasses import dataclass
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState,hook_config
from langchain.messages import AIMessage

from langgraph.runtime import Runtime
from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv
from loguru import logger
from langchain_openai import ChatOpenAI

load_dotenv()

store = InMemoryStore()
namespace = ("users", "credits")
key1 = 'Ada Lovelace'
value1 = {
    "tokens_credit_left": 5000,
    "user_level": 5
}
key2 = 'Blackwell'
value2 = {
    "tokens_credit_left": 2999,
    "user_level": 5
}
key3 = 'Ampere'
value3 = {
    "tokens_credit_left": 1000,
    "user_level": 5
}
store.put(namespace, key1, value1)
store.put(namespace, key2, value2)
store.put(namespace, key3, value3)

@dataclass
class UserContext:
    username: str

class CheckCredit(AgentMiddleware):
    @hook_config(can_jump_to=["end"])
    def before_model(self, state: AgentState, runtime: Runtime) ->dict[str, Any] | None:
        store = runtime.store
        context = runtime.context

        username = context.username
        credit = store.get(namespace, username)
        if not credit:
            return {
                "jump_to": "end",
                "messages": AIMessage("您尚未注册~")
            }

        if credit.value["tokens_credit_left"] < 3000:
            return {
                "jump_to": "end",
                "messages": AIMessage(f"{username}额度不足，请充值")
            }

        return None

    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str,Any] | None:
        store = runtime.store
        context = runtime.context

        username = context.username
        credit = store.get(namespace, username)
        usage_metadata = state["messages"][-1].usage_metadata
        token_usage = usage_metadata["input_tokens"] + usage_metadata["output_tokens"] * 6
        credit.value["tokens_credit_left"] -= token_usage

        # 更新长期记忆
        store.put(namespace, username, credit.value)

        return None

    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str,Any] | None:
        store = runtime.store
        context = runtime.context

        username = context.username
        item = store.get(namespace, username)
        credit = item.value["tokens_credit_left"]

        logger.info(f"{username} 当前剩余额度：{credit}")
        return None

# 1.实例化模型
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

agent = create_agent(
    model=model,
    middleware=[CheckCredit()],
    store=store,
    context_schema=UserContext
)

response1 = agent.invoke(
    {"messages": ["你好啊，你知道 Ada Lovelace 的贡献吗？"]},
    context=UserContext(username="Ada Lovelace")
)
print("=" * 30, '-> Ada Lovelace messages <-', '=' * 30)
for msg in response1["messages"]:
    msg.pretty_print()

response2 = agent.invoke(
    {"messages": ["你好啊，你知道 Blackwell 的贡献吗？"]},
    context=UserContext(username="Blackwell")
)
print("=" * 30, '-> Blackwell messages <-', '=' * 30)
for msg in response2["messages"]:
    msg.pretty_print()
```

输出

```markdown
2026-04-14 11:39:18.876 | INFO     |__main__:after_agent:85 - Ada Lovelace当前剩余额度：2721
2026-04-14 11:39:18.881 | INFO     |__main__:after_agent:85 - Blackwell 当前剩余额度：2999

============================== -> Ada Lovelace messages <-==============================
================================ Human Message=================================

你好啊，你知道 Ada Lovelace 的贡献吗？
================================== Ai Message==================================

是的，Ada Lovelace（1815-1852）被广泛认为是世界上第一位计算机程序员，她的贡献主要体现在以下几个方面：

---

### **1. 翻译与注释：解析“分析机”的潜力**
- 1843年，她翻译了意大利工程师路易吉·费德里科·米纳布里关于查尔斯·巴贝奇“分析机”（早期机械通用计算机）的论文，并添加了大量自己的注释，篇幅远超原文。
- 她的注释中包含了**世界上第一个计算机算法**，用于计算伯努利数，这被视为最早的“计算机程序”概念。

---

### **2. 超越计算的前瞻性思想**
- 她指出分析机不仅限于数值计算，还能处理符号、音乐甚至艺术，预见了计算机的**通用性**和**创造性潜力**。
- 她强调“机器只能执行指令，不能自主思考”，区分了人工智能与人类智能的界限。
---

### **3. 技术与人文的桥梁**
- 作为诗人拜伦的女儿，她将数学逻辑与想象力结合，主张科技与艺术的融合，这一思想对后世计算科学影响深远。

---

### **4. 历史意义**
- 尽管分析机在她有生之年未能建成，但她的工作在一个世纪后启发了艾伦·图灵等计算机科学先驱。
- 1980年，美国国防部将一种编程语言命名为“Ada”以纪念她。

---

### **争议与澄清**
- 部分学者认为她的贡献被过度神话，但主流观点仍肯定她首次系统阐述了编程逻辑的核心思想，尤其在19世纪女性科学参与受限的背景下，她的成就尤为突出。

---

Ada Lovelace 的故事不仅是技术史上的里程碑，也象征着跨学科创新如何推动人类认知边界。如果需要更具体的细节，我可以进一步展开！
============================== -> Blackwell messages <-==============================
================================ Human Message=================================

你好啊，你知道 Blackwell 的贡献吗？
================================== Ai Message==================================

Blackwell额度不足，请充值
```

#### 4.1.2 Wrap-style hooks

- **①wrap_model_call**

本例通过 **context**中记录的用户身份信息调整暴露给模型的工具集。

此处更改模型请求的方法是 **transient request update**，见上文**短期记忆2-4-2**

```python
from dataclasses import dataclass
from typing import Callable
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelResponse,ModelRequest
from langchain.messages import AIMessage
from langchain.tools import tool

from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

store = InMemoryStore()
namespace = ("users", "credits")
key1 = 'Ada Lovelace'
value1 = {
    "tokens_left": 3000,  # 剩余大模型token额度
    "get_weather": "yes",  # 是否认证天气查询服务
    "get_news": "no"  # 是否认证网络爬虫服务，用于查询新闻
}
key2 = 'Blackwell'
value2 = {
    "tokens_left": 2000,  # 剩余大模型token额度
    "get_weather": "no",  # 是否认证天气查询服务
    "get_news": "yes"  # 是否认证网络爬虫服务，用于查询新闻
}
key3 = 'Ampere'
value3 = {
    "tokens_left": 3000,  # 剩余大模型token额度
    "get_weather": "yes",  # 是否认证天气查询服务
    "get_news": "yes"  # 是否认证网络爬虫服务，用于查询新闻
}
store.put(namespace, key1, value1)
store.put(namespace, key2, value2)
store.put(namespace, key3, value3)

@tool
def get_weather(city: str):
    """
    查询指定城市当日天气

    Args:
        city: 城市名称
    """
    return f"{city} 今天天气不错"

@tool()
def get_news():
    """查询当日新闻"""
    return "美伊尚未达成停战协议"

@dataclass
class UserContext:
    username: str

class CheckCredit(AgentMiddleware):
    def wrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        context = request.runtime.context
        store = request.runtime.store

        value = store.get(namespace, context.username).value
        tools = []

        for tool in request.tools:
            tool_name = tool.name
            if value[tool_name] == "yes":
                tools.append(tool)
            else:
                logger.warning(f"{context.username} 无权调用 {tool_name}")

        # 更改调用请求携带的工具集，仅本次生效
        request = request.override(tools=tools)

        return handler(request)

# 1.实例化模型
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

agent = create_agent(
    model=model,
    middleware=[CheckCredit()],
    tools=[get_weather, get_news],
    store=store,
    context_schema=UserContext
)

response1 = agent.invoke(
    {"messages": ["你好啊，今天北京天气如何，今日有哪些新闻？"]},
    context=UserContext(username="Ada Lovelace")
)
print("=" * 30, '-> Ada Lovelace messages <-', '=' * 30)
for msg in response1["messages"]:
    msg.pretty_print()

response2 = agent.invoke(
    {"messages": ["你好啊，今天北京天气如何，今日有哪些新闻？"]},
    context=UserContext(username="Blackwell")
)
print("=" * 30, '-> Blackwell messages <-', '=' * 30)
for msg in response2["messages"]:
    msg.pretty_print()

response3 = agent.invoke(
    {"messages": ["你好啊，今天北京天气如何，今日有哪些新闻？"]},
    context=UserContext(username="Ampere")
)
print("=" * 30, '-> Ampere messages <-', '=' * 30)
for msg in response3["messages"]:
    msg.pretty_print()
```

输出

```text
2026-04-14 11:40:07.527 | WARNING  |__main__:wrap_model_call:75 - AdaLovelace 无权调用 get_news
2026-04-14 11:40:11.357 | WARNING  |__main__:wrap_model_call:75 - AdaLovelace 无权调用 get_news
2026-04-14 11:40:15.049 | WARNING  |__main__:wrap_model_call:75 -Blackwell 无权调用 get_weather

============================== -> Ada Lovelace messages <-==============================
================================ Human Message=================================
你好啊，今天北京天气如何，今日有哪些新闻？
================================== Ai Message==================================

我来帮您查询北京的天气情况。不过关于今日新闻，我目前没有相关的查询功能。
Tool Calls:
get_weather (call_00_OplicbLHGEaTanH3yaTDuiMp)
Call ID: call_00_OplicbLHGEaTanH3yaTDuiMp
Args:
 city: 北京
================================= Tool Message=================================
Name: get_weather

北京 今天天气不错
================================== Ai Message==================================

根据查询结果，北京今天天气不错！

关于今日新闻，我目前无法为您提供实时的新闻信息。您可以：
1. 查看各大新闻网站或新闻应用
2. 关注官方新闻发布平台
3. 使用专门的新闻查询工具

如果您需要了解其他城市的天气情况，我很乐意为您查询。

2026-04-14 11:40:17.903 | WARNING  |__main__:wrap_model_call:75 -Blackwell 无权调用 get_weather

============================== -> Blackwell messages <-==============================
================================ Human Message=================================

你好啊，今天北京天气如何，今日有哪些新闻？
================================== Ai Message==================================

我目前无法查询天气信息，不过我可以帮您查询今天的新闻。让我为您获取一下今日的新闻内容。
Tool Calls:
  get_news (call_00_thc8aLWFXkeffY1vafIwMJLk)
 Call ID: call_00_thc8aLWFXkeffY1vafIwMJLk
  Args:
================================= Tool Message=================================
Name: get_news

美伊尚未达成停战协议
================================== Ai Message==================================

根据查询结果，今天有一条重要新闻：**美伊尚未达成停战协议**。

关于北京的天气情况，我目前无法为您提供实时天气信息。建议您可以通过以下方式获取准确的北京天气信息：
1. 查看天气预报应用或网站
2. 使用搜索引擎搜索"北京天气"
3. 查看手机自带的天气应用

如果您还想了解其他新闻或者有其他问题，我很乐意为您提供帮助！
============================== -> Ampere messages <-==============================
================================ Human Message=================================

你好啊，今天北京天气如何，今日有哪些新闻？
================================== Ai Message==================================

我来帮您查询北京的天气和今日新闻。
Tool Calls:
  get_weather (call_00_ZyVpPMawPgdFdv49ojD3zIFt)
 Call ID: call_00_ZyVpPMawPgdFdv49ojD3zIFt
  Args:
    city: 北京
  get_news (call_01_kZaouXjSdhjrJGmzGWRbP3so)
 Call ID: call_01_kZaouXjSdhjrJGmzGWRbP3so
  Args:
================================= Tool Message=================================
Name: get_weather

北京 今天天气不错
================================= Tool Message=================================
Name: get_news

美伊尚未达成停战协议
================================== Ai Message==================================

根据查询结果：

**北京天气：**
今天北京天气不错。

**今日新闻：**
- 美伊尚未达成停战协议

如果您需要更详细的天气信息（比如具体温度、湿度等）或者想了解其他新闻，请告诉我！
```

- **②wrap_tool_call**

在上述案例的基础上，我们补充额度校验，和长期记忆更新。

```python
from dataclasses import dataclass
from typing import Callable, Any

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelResponse,ModelRequest, ToolCallRequest
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool

from langgraph.store.memory import InMemoryStore
from langgraph.types import Command
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

store = InMemoryStore()
namespace = ("users", "credits")
key1 = 'Ada Lovelace'
value1 = {
    "tokens_left": 3000,  # 剩余大模型token额度
    "get_weather": "yes",  # 是否认证天气查询服务
    "get_news": "no"  # 是否认证网络爬虫服务，用于查询新闻
}
key2 = 'Blackwell'
value2 = {
    "tokens_left": 2000,  # 剩余大模型token额度
    "get_weather": "no",  # 是否认证天气查询服务
    "get_news": "yes"  # 是否认证网络爬虫服务，用于查询新闻
}
key3 = 'Ampere'
value3 = {
    "tokens_left": 3000,  # 剩余大模型token额度
    "get_weather": "yes",  # 是否认证天气查询服务
    "get_news": "yes"  # 是否认证网络爬虫服务，用于查询新闻
}
store.put(namespace, key1, value1)
store.put(namespace, key2, value2)
store.put(namespace, key3, value3)

# 工具额度消耗
CREDIT_MAP = {
    "get_weather": 10,
    "get_news": 20
}

@tool
def get_weather(city: str):
    """
    查询指定城市当日天气

    Args:
        city: 城市名称
    """
    return f"{city} 今天天气不错"

@tool()
def get_news():
    """查询当日新闻"""
    return "美伊尚未达成停战协议"

@dataclass
class UserContext:
    username: str

class CheckCredit(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        context = request.runtime.context
        store = request.runtime.store

        value = store.get(namespace, context.username).value
        tools = []

        for tool in request.tools:
            tool_name = tool.name
            if value[tool_name] == "yes":
                tools.append(tool)
            else:
                logger.warning(f"{context.username} 无权调用 {tool_name}")

        # 更改调用请求携带的工具集，仅本次生效
        request = request.override(tools=tools)

        return handler(request)

class ToolGuard(AgentMiddleware):
    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
    ) -> ToolMessage | Command[Any]:
        store = request.runtime.store
        context = request.runtime.context

        username = context.username
        value = store.get(namespace, username).value
        tool_name = request.tool.name

        # 本次调用花费
        credits_cost = CREDIT_MAP.get(tool_name)
        # 剩余额度
        credits_left = value["tokens_left"]

        if credits_left < credits_cost:
            logger.warning(f"{username} 额度不足，{tool_name} 调用失败！")
            return Command(
                update={
                    "messages": [
                        ToolMessage(
                            content="额度不足，无法调用工具，请充值~",
                            tool_call_id=request.runtime.tool_call_id
                        )
                    ]
                }
            )

        # 更新剩余额度
        credits_left -= credits_cost
        value["tokens_left"] = credits_left
        store.put(namespace, username, value)
        logger.info(f"{username} 调用 {tool_name} 花费 {credits_cost}，剩余额度 {credits_left}")
        logger.info(f"{username} 状态已更新，当前状态 {store.get(namespace,username).value}")

        return handler(request)

agent = create_agent(
    model="deepseek-chat",
    middleware=[CheckCredit(), ToolGuard()],
    tools=[get_weather, get_news],
    store=store,
    context_schema=UserContext
)

response = agent.invoke(
    {"messages": ["你好啊，今天北京天气如何，今日有哪些新闻？"]},
    context=UserContext(username="Ada Lovelace")
)
print("=" * 30, '-> Ada Lovelace messages <-', '=' * 30)
for msg in response["messages"]:
    msg.pretty_print()
```

输出

```text
2026-04-14 11:41:20.386 | WARNING  |__main__:wrap_model_call:82 - AdaLovelace 无权调用 get_news
2026-04-14 11:41:23.859 | INFO     |__main__:wrap_tool_call:124 - AdaLovelace 调用 get_weather 花费 10，剩余额度 2990
2026-04-14 11:41:23.860 | INFO     |__main__:wrap_tool_call:125 - AdaLovelace 状态已更新，当前状态 {'tokens_left': 2990, 'get_weather': 'yes','get_news': 'no'}
2026-04-14 11:41:23.865 | WARNING  |__main__:wrap_model_call:82 - AdaLovelace 无权调用 get_news

============================== -> Ada Lovelace messages <-==============================
================================ Human Message=================================

你好啊，今天北京天气如何，今日有哪些新闻？
================================== Ai Message==================================

我来帮您查询北京的天气情况。不过需要说明的是，我目前只能查询天气信息，无法提供新闻资讯。
Tool Calls:
get_weather (call_00_HY2jENXsRyK21gITiQqeVSk9)
Call ID: call_00_HY2jENXsRyK21gITiQqeVSk9
Args:
 city: 北京
================================= Tool Message=================================
Name: get_weather

北京 今天天气不错
================================== Ai Message==================================

根据查询结果，北京今天天气不错。

关于新闻资讯，我目前没有相关的查询功能。如果您想了解今日新闻，建议您：
1. 查看主流新闻网站或APP
2. 关注官方新闻媒体
3. 使用专门的新闻搜索工具

如果您还需要了解其他城市的天气情况，我很乐意为您查询。
```

#### 4.1.3 特殊的便捷中间件dynamic_prompt

如前所述，@dynamic_prompt底层实现机制和通用钩子函数是统一的，对于动态提示词处理提供了更加便捷的入口。

本例通过静态上下文中携带的用户信息，动态更改系统提示词。

```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_openai import ChatOpenAI
from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# 准备历史记忆
namespace = ("users", "preferences")
key1 = "Ada Lovelace"
value1 = {
    "chat_preferences": [
        "不喜欢啰嗦",
        "尽可能用最精简的文字解释清楚"
    ]
}

key2 = "Blackwell"
value2 = {
    "chat_preferences": [
        "喜欢长篇大论、引经据典",
        "不知道的东西要明确说'不知道'，不能胡编乱造"
    ]
}

store = InMemoryStore()
store.put(namespace, key1, value1)
store.put(namespace, key2, value2)

@dataclass
class UserContext:
    username: str

@dynamic_prompt
def personalized_prompt(request: ModelRequest) -> str:
    username = request.runtime.context.username
    store = request.runtime.store

    preferences = store.get(namespace, username).value["chat_preferences"]
    custom_prompt = f"# 用户偏好\n{'\n'.join(preferences)}"
    logger.info(f"{username} 自定义系统提示词\n{custom_prompt}")

    return custom_prompt
model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

agent = create_agent(
    model=model,
    middleware=[personalized_prompt],
    store=store,
    context_schema=UserContext
)

response1 = agent.invoke(
    {"messages": ["为什么花儿这样红？"]},
    context=UserContext(username="Ada Lovelace")
)
print("=" * 30, '-> Ada Lovelace messages <-', '=' * 30)
for msg in response1["messages"]:
    msg.pretty_print()

response2 = agent.invoke(
    {"messages": ["为什么花儿这样红？"]},
    context=UserContext(username="Blackwell")
)
print("=" * 30, '-> Blackwell messages <-', '=' * 30)
for msg in response2["messages"]:
    msg.pretty_print()
```

输出

```markdown
2026-04-14 11:44:10.784 | INFO     |__main__:personalized_prompt:44 - AdaLovelace 自定义系统提示词
# 用户偏好
不喜欢啰嗦
尽可能用最精简的文字解释清楚
2026-04-14 11:44:13.622 | INFO     |__main__:personalized_prompt:44 -Blackwell 自定义系统提示词
# 用户偏好
喜欢长篇大论、引经据典
不知道的东西要明确说'不知道'，不能胡编乱造

============================== -> Ada Lovelace messages <-==============================
================================ Human Message=================================

为什么花儿这样红？
================================== Ai Message==================================

花儿红的主要原因是花瓣细胞中的**花青素**在酸性环境下显红色，同时受光照、温度、养分等影响，为吸引传粉者进化而成。
============================== -> Blackwell messages <-==============================
================================ Human Message=================================

为什么花儿这样红？
================================== Ai Message==================================

“为什么花儿这样红”这一问题，可以从科学、文学、文化等多个维度展开探讨。以下将从不同角度进行详细分析，力求全面而深入。

---

### **一、科学视角：色彩形成的自然机制**
花朵的红色主要源于植物色素、光学结构以及进化适应性的共同作用。

1. **色素基础：花青素的主导作用**
   - 花青素（Anthocyanin）是形成红、紫、蓝等颜色的关键色素，属于类黄酮化合物。它在不同酸碱度（pH）下呈现颜色变化：酸性环境中偏红（如玫瑰、牡丹），中性时呈紫色，碱性环境中则偏蓝。
   - 其他色素如类胡萝卜素（橙黄色）和甜菜色素（少数植物如仙人掌）也可能与红色相关，但花青素是最常见的红色来源。

2. **光学与结构增色**
   - 部分花朵的红色并非单纯依赖色素，而是通过花瓣表面的微观结构（如多层薄膜、衍射光栅）反射特定波长的光，增强色彩饱和度。例如红罂粟的花瓣具有蜂窝状结构，能强化红色视觉效果。

3. **进化与生态学意义**
   - **传粉者吸引**：红色对许多传粉昆虫（如蜜蜂）可见度较低，但对鸟类（如蜂鸟）和部分蝶类极具吸引力。在美洲、亚洲等地区，红色花朵常与鸟媒传粉相关。
   - **环境适应**：花青素可抵御紫外线伤害、抵抗病原体，并在低温或干旱条件下保护植物细胞。高海拔地区的红花比例较高，可能与紫外线防护有关。

---

### **二、文学与艺术中的象征意义**
红色在人类文化中被赋予丰富内涵，花朵的红色常成为情感与哲思的载体。

1. **爱情与激情**
   - 红玫瑰在西方传统中象征炽热爱情，可追溯至希腊罗马神话中维纳斯与阿多尼斯的故事，玫瑰的红色被联想为爱神之血。波斯诗人萨迪在《蔷薇园》中亦以玫瑰隐喻激情。

2. **生命、牺牲与革命**
   - 中国文学中，红色梅花、杜鹃常被赋予坚贞或壮烈的意象（如“杜鹃啼血”）。近现代以来，红色花朵亦与革命精神关联，如《红岩》中的红梅象征烈士鲜血。

3. **美学与哲学隐喻**
   - 王阳明在《传习录》中提及“岩中花树”，探讨心与物的关系；歌德在《色彩论》中分析红色对情感的影响。红色花朵的视觉冲击力，常引发对生命短暂与绚烂的思考（如日本“物哀”美学中的樱花）。
---

### **三、文化差异与历史演变**
不同文明对红色花朵的解读存在显著差异：

1. **东方文化**
   - 中国：红色象征吉祥、喜庆，牡丹被称为“国色天香”，红色牡丹尤其代表富贵。但李贺诗句“桃花乱落如红雨”亦暗含哀愁。
   - 日本：红椿花在江户时代被赋予“谦逊”与“永恒”之意，但亦因整朵凋落的特点与武士精神关联。

2. **西方文化**
   - 基督教艺术中，红色玫瑰象征殉道者的鲜血与神圣之爱（如但丁《神曲》中天堂的玫瑰）。
   - 近代欧洲，红罂粟因一战战场盛放，成为纪念阵亡将士的符号（如约翰·麦克雷诗作《在弗兰德战场》）。

---

### **四、现代科学的新发现**
近年研究进一步揭示了花朵红色的复杂性：
- **基因调控**：MYB转录因子等基因可精确控制花青素合成，通过基因工程已培育出深浅各异的红色花卉。
- **气候响应**：全球变暖可能导致花朵颜色加深，因高温促进花青素积累（2020年《生态学通讯》研究）。
- **传粉者视觉模型**：蜂鸟对红色的偏好与其视网膜中特殊色素细胞（油滴滤光）相关，这解释了美洲红色花与蜂鸟的协同进化。

---

### **结语**
“花儿这样红”既是自然选择的精巧结果，也是人类文明的情感投射。从花青素的生物化学路径到《诗经》中的“桃之夭夭”，从达尔文对传粉生态的观察到现代基因图谱的解析，这一问题串联起了科学与人文的对话。红色花朵的绚丽，最终在观察者的眼中完成了自然法则与心灵共鸣的统一。

**参考文献方向**（如需进一步研究可查阅）：
- 植物生理学：《植物生物化学与分子生物学》（B.B. Buchanan等编著）
- 文化象征：《花的语言》（Jack Goody，人类学著作）
- 进化生态学：《花的起源与多样性》（昆虫传粉协同进化理论）
```

**dynamic_prompt** 是动态更新本次调用前的系统提示词，并不会更改消息列表，所以根据模型输出，可以发现系统提示词生效，但消息列表看不到相关提示词。

### 4.2 工具中访问

在上文介绍工具的自定义args_schema时我们介绍了两种方式：

- 基于pydantic模型
- 基于json_schema

实际上，Langchain底层在生成工具的schema时，如果参数类型注解是pydantic模型，也会被一并解析。

```python
from pydantic import BaseModel, Field
from typing import List

from langchain.tools import tool
from langgraph.prebuilt.tool_node import ToolRuntime
from langchain_core.utils.function_calling import convert_to_openai_tool

class UserInfo(BaseModel):
    username: str = Field(description="用户名")
    age: int = Field(description="年龄")
    hobbies: List[str] = Field(description="兴趣爱好")

@tool(parse_docstring=True)
def save_user_info(user_info: UserInfo, runtime: ToolRuntime) -> str:
    """
    保存用户信息

    Args:
        user_info: 用户信息对象
    """
    return "ok"

print(convert_to_openai_tool(save_user_info))
```

输出如下

```json
{
    "type": "function",
    "function": {
        "name": "save_user_info",
        "description": "保存用户信息",
        "parameters": {
            "properties": {
                "user_info": {
                    "properties": {
                        "username": {
                            "description": "用户名",
                            "type": "string"
                        },
                        "age": {
                            "description": "年龄",
                            "type": "integer"
                        },
                        "hobbies": {
                            "description": "兴趣爱好",
                            "items": {
                                "type": "string"
                            },
                            "type": "array"
                        }
                    },
                    "required": [
                        "username",
                        "age",
                        "hobbies"
                    ],
                    "type": "object",
                    "description": "用户信息对象"
                }
            },
            "required": [
                "user_info"
            ],
            "type": "object"
        }
    }
}
```

下面的案例中，我们通过工具读写长期记忆中保存的用户信息

```python
from pydantic import BaseModel, Field
from typing import List, Any
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, SystemMessage

from langgraph.prebuilt.tool_node import ToolRuntime
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver

from loguru import logger
from dotenv import load_dotenv
load_dotenv()

@dataclass
class UserContext:
    user_id: str

store = InMemoryStore()
namespace = ("users", "user_info")

class UserInfo(BaseModel):
    username: str = Field(description="用户名", default="unknown")
    age: int = Field(description="年龄", default=0)
    # 这里相当于告诉模型，每次创建新实例时，调用list()创建一个新的list传进去
    hobbies: List[str] = Field(description="兴趣爱好", default_factory=list)
    # 这种写法是用可变对象做默认值，会有多个对象共享一个列表对象的风险
    # hobbies: List[str] = Field(description="兴趣爱好", default=[])

@tool(parse_docstring=True)
def read_user_info(runtime: ToolRuntime[UserContext, Any]) -> UserInfo |str:
    """
    读取用户信息

    Returns:
        UserInfo | str: 如果找到用户信息，返回 UserInfo 对象；否则返回空字符串。
    """
    user_id = runtime.context.user_id
    store = runtime.store
    item = store.get(namespace, user_id)
    if item:
        return UserInfo(**item.value)
    return ''

@tool(parse_docstring=True)
def write_user_info(user_info: UserInfo, runtime: ToolRuntime[UserContext,Any]) -> bool:
    """
    将用户信息写入长期记忆

    Args:
        user_info：用户信息对象

    Returns:
        bool: 如果成功写入则返回True，否则返回False
    """
    user_id = runtime.context.user_id
    store = runtime.store
    try:
        logger.info(f"写入记忆, namespace: {namespace}, user_id: {user_id},user_info: {user_info.model_dump()}")
        store.put(namespace, user_id, user_info.model_dump())
    except Exception as e:
        logger.error(e)
        return False
    return True

model = ChatOpenAI(
    model="gemma4:12b",
    api_key="sk_1234",
    base_url="http://localhost:11434/v1"
)

agent = create_agent(
    model =model,
    tools = [read_user_info, write_user_info],
    store = store,
    checkpointer=InMemorySaver(),
    context_schema=UserContext
)

config1 = {"configurable": {"thread_id": "thread_1"}}
config2 = {"configurable": {"thread_id": "thread_2"}}

agent.invoke(
    {"messages": [
        SystemMessage("如果输入包含用户信息，抽取并调用工具记录。在记录之前先查找历史信息，和新增信息合并后记录。"
                      "如果用户提问设计个人信息，调用工具查找"),
        HumanMessage("你好，我是韩立，我喜欢修仙")
    ]},
    context = UserContext(user_id = 'user_1'),
    config = config1
)

thread_1_response = agent.invoke(
    {"messages": ["我今年两百岁了，是你们口中的 “元婴老怪”，我喜欢跑步"]},
    context = UserContext(user_id = 'user_1'),
    config = config1
)

print("=" * 30, '-> thread_1 messages <-', '=' * 30)
for msg in thread_1_response["messages"]:
    msg.pretty_print()

thread_2_response = agent.invoke(
    {"messages": ["你还记得我吗？"]},
    context = UserContext(user_id = 'user_1'),
    config = config2
)

print("=" * 30, '-> thread_2 messages <-', '=' * 30)
for msg in thread_2_response["messages"]:
    msg.pretty_print()
```

输出

```text
2026-04-14 15:58:30.011 | INFO     |__main__:write_user_info:61 - 写入记忆,namespace: ('users', 'user_info'), user_id: user_1, user_info:{'username': '韩立', 'age': 0, 'hobbies': ['修仙']}
2026-04-14 15:58:41.439 | INFO     |__main__:write_user_info:61 - 写入记忆,namespace: ('users', 'user_info'), user_id: user_1, user_info:{'username': '韩立', 'age': 200, 'hobbies': ['修仙', '跑步']}

============================== -> thread_1 messages <-==============================
================================ System Message================================

如果输入包含用户信息，抽取并调用工具记录。在记录之前先查找历史信息，和新增信息合并后记录。如果用户提问设计个人信息，调用工具查找
================================ Human Message=================================

你好，我是韩立，我喜欢修仙
================================== Ai Message==================================

你好韩立！很高兴认识你。我看到你喜欢修仙，这是一个很有趣的爱好。

为了让我能更好地记住你的信息，让我先查看一下是否已经有你的历史记录。
Tool Calls:
read_user_info (call_00_DAqBrMPFS4iZVK5F7mvaOsBy)
Call ID: call_00_DAqBrMPFS4iZVK5F7mvaOsBy
Args:
================================= Tool Message=================================
Name: read_user_info


================================== Ai Message==================================

看起来目前还没有你的历史记录。让我记录一下你的基本信息：
Tool Calls:
write_user_info (call_00_Zoz8sLHivXkA0a0Py2yvDFJB)
Call ID: call_00_Zoz8sLHivXkA0a0Py2yvDFJB
Args:
 user_info: {'username': '韩立', 'hobbies': ['修仙']}
================================= Tool Message=================================
Name: write_user_info

true
================================== Ai Message==================================

好的，我已经记录了你喜欢修仙这个爱好。修仙确实是一个很有深度的领域，涉及到修炼、功法、丹药、法宝等很多方面。你对修仙的哪个方面特别感兴趣呢？比如是修炼功法、炼丹术、阵法，还是其他方面？
================================ Human Message=================================

我今年两百岁了，是你们口中的 “元婴老怪”，我喜欢跑步
================================== Ai Message==================================

哇！两百岁的元婴老怪，这真是令人惊叹！看来您在修仙道路上已经走了很长的路。

让我更新一下您的信息，包括年龄和新的爱好——跑步。
Tool Calls:
read_user_info (call_00_I9AO3Y8RJSQLeHhwBGszkuiW)
Call ID: call_00_I9AO3Y8RJSQLeHhwBGszkuiW
Args:
================================= Tool Message=================================
Name: read_user_info

username='韩立' age=0 hobbies=['修仙']
================================== Ai Message==================================

现在我来更新您的完整信息：
Tool Calls:
write_user_info (call_00_3JpZC48aqJG7m0m6X2EnZFNH)
Call ID: call_00_3JpZC48aqJG7m0m6X2EnZFNH
Args:
 user_info: {'username': '韩立', 'age': 200, 'hobbies': ['修仙', '跑步']}
================================= Tool Message=================================
Name: write_user_info

true
================================== Ai Message==================================

很好！我已经更新了您的信息：
- 姓名：韩立
- 年龄：200岁
- 爱好：修仙、跑步

作为一位元婴期的前辈，您一定有着丰富的修炼经验和人生智慧。跑步这个爱好很有意思，对于修仙者来说，这既是锻炼身体的好方法，也能让心境更加平和。您平时是在宗门内跑步，还是在山林间奔跑呢？
============================== -> thread_2 messages <-==============================
================================ Human Message=================================

你还记得我吗？
================================== Ai Message==================================

我来查看一下之前记录的用户信息。
Tool Calls:
  read_user_info (call_00_iJgxeOZKvXCNYkRjX3EFGp8q)
 Call ID: call_00_iJgxeOZKvXCNYkRjX3EFGp8q
  Args:
================================= Tool Message=================================
Name: read_user_info

username='韩立' age=200 hobbies=['修仙', '跑步']
================================== Ai Message==================================

当然记得！你是韩立，200岁，喜欢修仙和跑步。很高兴再次见到你！最近修仙进展如何？还是经常跑步锻炼吗？
```

分析

1. 前两次invoke通过相同的thread_id串联为一个会话，共享短期记忆
2. context是运行时静态配置，每次invoke互相独立
3. 长期记忆可以在任意位置访问，全局共享同一份信息
4. tool参数列表中的ToolRuntime是Langchain / Langgraph运行时注入的，在工具schema中没有体现
5. ToolRuntime的默认泛型是[None, Any]，第一个是Context的泛型，第二个是State对象的泛型。

- 如果不显式指定上下文对象的类型，则Langchain/Langgraph底层会认为上下文对象为None，invoke调用时传递了context就会抛出警告，所以这里将UserContext作为ToolRuntime的第一个泛型传递。
