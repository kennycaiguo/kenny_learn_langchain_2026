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

#### ②get()源码剖析

#### ③举例1：基于InMemoryStore

#### ④举例2：基于PostgresStore

### 3.2.2 search():搜索API

#### ①源码剖析

#### ②举例1：按照namespace前缀搜索

#### ③举例2：按照filter过滤

#### ④举例3：按照语义搜索

## 3.3 在Agent运行图中访问长期记忆

### 3.3.1 在工具在访问长期记忆

#### ①基于InMemoryStore

#### ②基于PostgresStore

### 3.3.2 在中间件中访问长期记忆

#### ①Node-style hooks中访问

#### ②Wrap-style hooks中访问

## 3.4何时写入记忆

# 4.课后阅读：Static runtime Context

## 4.1中间件中访问

### 4.1.1 Node-style hooks
