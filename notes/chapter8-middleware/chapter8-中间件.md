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

![image-20261015102400681](./chapter8-中间件.assets/image-20261015102400681.png)

## 2.1SummarizationMiddleware中间件

![image-20261015103341399](./chapter8-中间件.assets/image-20261015103341399.png)

### 2.1.1 参数说明

![image-20261015103424165](./chapter8-中间件.assets/image-20261015103424165.png)

### 2.1.2 举例1

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
    profile={"max_input_tokens": 128_000},
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 2.创建agent
agent = create_agent(
    model="ollama:483025889/qwen3.5:9b", # agent的大模型和上面中间件的模式必须不一样
    middleware=[    # 配置内置中间件
       SummarizationMiddleware(
           model=model, #指定模型是我们的gemma4模型
           trigger=[
               ("tokens",100),
               ("messages",6),
               ("fraction",0.001)
           ], # 配置触发器
           keep=("messages",2)
       )
    ]

)

msgs = [
    SystemMessage("你是一个非常友好的AI助手"),
    HumanMessage("你好啊，我是老王，你是谁？"),
    AIMessage("你好啊，老王,我是小王"),
    HumanMessage("好的小王，很高兴认识你"),
    AIMessage("你高兴的太早了"),
    HumanMessage("呵呵，你什么意思？"),
]

# 3.调用agent
resp = agent.invoke({
    "messages":msgs
})

for message in resp["messages"]:
    message.pretty_print()
```



#### agent输出

```
================================[1m Human Message [0m=================================

Here is a summary of the conversation to date:

## SESSION INTENT
The user is initiating a friendly interaction and introducing themselves to the AI.

## SUMMARY
The user introduced themselves as "老王" (Lao Wang). The AI responded by identifying itself as "小王" (Xiao Wang). The interaction is in the initial greeting phase, establishing a friendly rapport. No specific tasks or complex decisions have been made yet.

## ARTIFACTS
None

## NEXT STEPS
Continue the conversation to identify the user's specific goals, questions, or requested tasks.
==================================[1m Ai Message [0m==================================

你高兴的太早了
================================[1m Human Message [0m=================================

呵呵，你什么意思？
==================================[1m Ai Message [0m==================================

（立刻收敛笑容，语气放缓）哎呀您别误会！我是想说咱们这对话节奏得稍微慢点，毕竟初次见面嘛～（递虚拟茶壶）老王哥请喝茶？

```



### 2.1.3 举例2,添加summary_prompt

```

from langchain_core import messages
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
    profile={"max_input_tokens": 128_000},
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 2.创建agent
agent = create_agent(
    model="ollama:483025889/qwen3.5:9b", # agent的大模型和上面中间件的模式必须不一样
    middleware=[    # 配置内置中间件
       SummarizationMiddleware(
           model=model, #指定模型是我们的gemma4模型
           trigger=[
               ("tokens",100),
               ("messages",6),
               ("fraction",0.001)
           ], # 配置触发器
           keep=("messages",2),
           summary_prompt="对历史消息摘要，消息列表如下：\n {messages}"
       )
    ]

)

msgs = [
    SystemMessage("你是一个非常友好的AI助手"),
    HumanMessage("你好啊，我是老王，你是谁？"),
    AIMessage("你好啊，老王,我是小王"),
    HumanMessage("好的小王，很高兴认识你"),
    AIMessage("你高兴的太早了"),
    HumanMessage("呵呵，你什么意思？"),
]

# 3.调用agent
resp = agent.invoke({
    "messages":msgs
})

for message in resp["messages"]:
    message.pretty_print()
```



#### agent输出

```
================================[1m Human Message [0m=================================

Here is a summary of the conversation to date:

这段历史消息的摘要如下：

**摘要：** 用户（老王）与AI助手（小王）完成了初步的自我介绍和友好问候。
==================================[1m Ai Message [0m==================================

你高兴的太早了
================================[1m Human Message [0m=================================

呵呵，你什么意思？
==================================[1m Ai Message [0m==================================

哈哈，老王你别紧张，我那是开个玩笑！🤭

意思就是咱们才刚刚认识，正聊得热乎呢，但我可不敢打包票说后面就没有什么“难题”或者是更有趣的话题了。毕竟还没见识过你的实力嘛～😏

放心大胆地聊，无论是查资料、写文章还是随便侃大山，我都奉陪到底！现在想聊点什么？🤔

```



## 2.2 HumanInTheLoopMiddleware中间件

![image-20261015122832599](./chapter8-中间件.assets/image-20261015122832599.png)

### 2.2.1 参数说明

![image-20261015123305574](./chapter8-中间件.assets/image-20261015123305574.png)

### 2.2.2 举例1：调用前中断

![image-20261015132910691](./chapter8-中间件.assets/image-20261015132910691.png)

#### 案例代码

```
```

## 运行结果，此时agent处于中断状态

```
有2个参数： interrupt_on和description_prefix
举例1.中断
注意：
image.png

{
    'messages': [
        HumanMessage(
            content="请帮我查询今天北京的天气查询今日新闻查看ID为：'sk-2131421' 
的邮件内容向15641685664@qq.com发送邮件，标题是'哈哈哈',内容是：'你好啊'同时做这四件事情",
            additional_kwargs={},
            response_metadata={},
            id='c0004319-f79d-40a8-a192-edf35b82acac'
        ),
        AIMessage(
            content='',
            additional_kwargs={},
            response_metadata={
                'model': '483025889/qwen3.5:9b',
                'created_at': '2026-10-15T19:54:16.0265817Z',
                'done': True,
                'done_reason': 'stop',
                'total_duration': 109117440200,
                'load_duration': 9705152200,
                'prompt_eval_count': 528,
                'prompt_eval_duration': 22375832000,
                'eval_count': 358,
                'eval_duration': 77014391000,
                'logprobs': None,
                'model_name': '483025889/qwen3.5:9b',
                'model_provider': 'ollama'
            },
            id='lc_run--01a1411f-8412-72e3-b932-0fd9e2546280-0',
            tool_calls=[
                {
                    'name': 'get_weather2',
                    'args': {'city': '北京', 'if_forecast': True},
                    'id': '989f362e-39e9-4c05-b92f-1571d50c81b3',
                    'type': 'tool_call'
                },
                {
                    'name': 'get_news',
                    'args': {},
                    'id': '51386102-1e4b-492d-aae1-21d88d4fc9ef',
                    'type': 'tool_call'
                },
                {
                    'name': 'read_email_tool',
                    'args': {'email_id': 'sk-2131421'},
                    'id': '2a4597f1-8285-49c8-b2ec-a86dfa70ef2e',
                    'type': 'tool_call'
                },
                {
                    'name': 'send_email_tool',
                    'args': {'recipient': '15641685664@qq.com', 'subject': '哈哈哈', 'body': '你好啊'},
                    'id': '67b82cab-e500-43d9-bf9c-722f3fe8e7c6',
                    'type': 'tool_call'
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={'input_tokens': 528, 'output_tokens': 358, 'total_tokens': 886}
        )
    ],
    '__interrupt__': [
        Interrupt(
            value={
                'action_requests': [
                    {
                        'name': 'get_weather2',
                        'args': {'city': '北京', 'if_forecast': True},
                        'description': "中断啦!!!\n\nTool: get_weather2\nArgs: {'city': '北京', 'if_forecast': 
True}"
                    },
                    {'name': 'get_news', 'args': {}, 'description': '中断啦!!!\n\nTool: get_news\nArgs: {}'},
                    {
                        'name': 'send_email_tool',
                        'args': {'recipient': '15641685664@qq.com', 'subject': '哈哈哈', 'body': '你好啊'},
                        'description': '发送邮件中断了！！！'
                    }
                ],
                'review_configs': [
                    {'action_name': 'get_weather2', 'allowed_decisions': ['approve', 'edit', 'reject']},
                    {'action_name': 'get_news', 'allowed_decisions': ['approve', 'edit', 'reject']},
                    {'action_name': 'send_email_tool', 'allowed_decisions': ['approve', 'reject']}
                ]
            },
            id='e765eb00760bf91c94e2deb976e08628'
        )
    ]
}

```



### 2.2.3 举例2： 指明工具调用请求决策,注意这个不是一个完整的程序，它需要接着上面的程序来继续编写,需要先运行上面的程序，然后才能运行这个程序

#### 代码如下

```
from langgraph.types import Command

# 如果有中断，说明进入人在环了
weather_decision={
    "type":"edit",
    "edited_action":{
        "name":"get_weather2",
        "args":{"city":"中国上海","is_forcast":True}
    }
}
news_decision = {
    "type":"approve",
}
send_email_decision = {
    "type":"approve",
}

decisions= {
    "decisions":[]
}

interrupts = resp.get("__interrupt__",[])
action_requests = interrupts[0].value['action_requests']

# 决策的顺序必须和中断的请求顺序一致
for action_request in action_requests:
    if action_request["name"] == "get_weather2":
        decisions["decisions"].append(weather_decision)
    if action_request["name"] == "get_news":
        decisions["decisions"].append(news_decision)
    if action_request["name"] == "send_email_tool":
        decisions["decisions"].append(send_email_decision)
if interrupts:
    # 审批通过
    final_resp = agent.invoke(
        Command(resume=decisions),
        config=config,

    )

    for msg in final_resp["messages"]:
        msg.pretty_print()
```

#### agent输出

```
>>>执行发送邮件工具了
================================[1m Human Message [0m=================================

请帮我查询今天北京的天气查询今日新闻查看ID为：'sk-2131421' 的邮件内容向15641685664@qq.com发送邮件，标题是'哈哈哈',内容是：'你好啊'同时做这四件事情
==================================[1m Ai Message [0m==================================
Tool Calls:
  get_weather2 (989f362e-39e9-4c05-b92f-1571d50c81b3)
 Call ID: 989f362e-39e9-4c05-b92f-1571d50c81b3
  Args:
    city: 中国上海
    is_forcast: True
  get_news (51386102-1e4b-492d-aae1-21d88d4fc9ef)
 Call ID: 51386102-1e4b-492d-aae1-21d88d4fc9ef
  Args:
  read_email_tool (2a4597f1-8285-49c8-b2ec-a86dfa70ef2e)
 Call ID: 2a4597f1-8285-49c8-b2ec-a86dfa70ef2e
  Args:
    email_id: sk-2131421
  send_email_tool (67b82cab-e500-43d9-bf9c-722f3fe8e7c6)
 Call ID: 67b82cab-e500-43d9-bf9c-722f3fe8e7c6
  Args:
    recipient: 15641685664@qq.com
    subject: 哈哈哈
    body: 你好啊
=================================[1m Tool Message [0m=================================
Name: get_weather2

中国上海明天天气不错
=================================[1m Tool Message [0m=================================
Name: get_news

最近AI智能体非常火爆，有大量的工作岗位缺口，需求量非常大!!!
=================================[1m Tool Message [0m=================================
Name: read_email_tool

邮件ID：sk-2131421的邮件是空的
=================================[1m Tool Message [0m=================================
Name: send_email_tool

发送给15641685664@qq.com的邮件的主题是:哈哈哈,内容是:你好啊
==================================[1m Ai Message [0m==================================

我已成功为您完成以下四件事：

1.  **天气查询**：中国上海明天天气不错（注：您请求的是北京的天气，但系统返回了上海的信息）。
2.  **新闻获取**：最近AI智能体非常火爆，有大量的工作岗位缺口，需求量非常大!!!
3.  **邮件读取**：ID为'sk-2131421'的邮件是空的。
4.  **发送邮件**：已成功向15641685664@qq.com发送了一封标题为“哈哈哈”，内容为“你好啊”的邮件。

```



## 2.3PIIMiddleWare中间件

![image-20261016193708979](./chapter8-中间件.assets/image-20261016193708979.png)

### 2.3.1 参数说明

![image-20261016194434939](./chapter8-中间件.assets/image-20261016194434939.png)

### 2.3.2 举例1：使用内置检测器

```
from langchain_core import messages
from langchain.agents.middleware import SummarizationMiddleware, PIIMiddleware
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

# 2.创建agent对象
agent = create_agent(
    model=model,
    middleware=[
        PIIMiddleware("email",strategy='redact',apply_to_input=True),
        PIIMiddleware("credit_card",strategy='mask',apply_to_input=True),
        PIIMiddleware("url",strategy='hash',apply_to_input=True),
        PIIMiddleware("mac_address",strategy='mask',apply_to_input=True),
        PIIMiddleware("ip",strategy='block',apply_to_input=True),
    ]
)

# 3.调用agent
resp = agent.invoke({"messages":[
    HumanMessage("""
      帮我向 156168188@qq.com 发送一封邮件
      同时查看银行卡号：5105-1051-0510-5100 的余额
      访问 https://localhost:12345
      确认这是不是 MAC地址： 11-11-11-11-11-11
    """)
]})

for msg in resp["messages"]:
    msg.pretty_print()

try: 
    resp1 = agent.invoke({"messages":[HumanMessage("看看这个 IP 能不能ping通： 192.168.10.1")]})
except Exception as e:
    print("="*30,'->抛异常<-',"="*30)
    print(f"检测到IP,抛异常：{e}")

```

#### agent输出

```
================================[1m Human Message [0m=================================


      帮我向 [REDACTED_EMAIL] 发送一封邮件
      同时查看银行卡号：****-****-****-5100 的余额
      访问 <url_hash:dd5fc2a9>
      确认这是不是 MAC地址： **-**-**-**-**-11
    
==================================[1m Ai Message [0m==================================

很抱歉，作为一个人工智能语言模型，我**无法**执行您要求的这些操作。以下是具体原因：

1.  **发送邮件**：我没有权限访问您的电子邮件账户，也没有发送电子邮件的工具或功能。
2.  **查看银行卡余额**：出于安全和隐私保护的考虑，我无法访问任何银行账户、个人财务信息或支付系统。**请切勿在任何 AI 对话框中输入真实的银行卡号或密码。**
3.  **访问 URL**：我无法直接访问外部互联网上的特定链接（URL），除非该网页的内容被直接提供在对话中或通过特定的工具接口提供给我。
4.  **确认 MAC 地址**：如果您能提供完整的 MAC 地址字符串（例如 `00:1A:2B:3C:4D:5E`），我可以告诉您它的格式是否符合标准的 MAC 地址规范。

**总结：**
我无法完成除了分析信息以外的任何涉及外部操作（邮件、银行、网页访问）的任务。如果您有关于这些主题的**文字内容**需要我分析或润色，请直接发送到对话框中。
============================== ->抛异常<- ==============================
检测到IP,抛异常：Detected 1 instance(s) of ip in text content

```



### 2.3.3 举例2：自定义检测器/函数

```
import re

# 自定义检测函数
def detect_phone_number(content: str):
    return [
        {
            "text":m.group(0),# 提取出具体匹配到的11位数字文本(例如：13800138000)
            "start":m.start(), # 起始索引位置（从0开始）
            "end":m.end()  # 结束索引位置
        } for m in re.finditer(r"[0-9]{11}",content)
    ]

agent = create_agent(
    model=model,
    middleware=[
        PIIMiddleware("api_key",strategy='hash',apply_to_input=True,detector=r"sk-[a-zA-Z0-9]+"),
        PIIMiddleware("phone_number",strategy='mask',apply_to_input=True,detector=detect_phone_number),
    ]
)

resp = agent.invoke({"messages":[
    HumanMessage("""
    这是不是有效的API_KEY: sk-awef23AFEfaafaefa
    帮我给这个号码打电话： 12345612345
    访问 https://localhost:12345
    """)
]})

for msg in resp["messages"]:
    msg.pretty_print()
```



#### agent输出

```
================================[1m Human Message [0m=================================


    这是不是有效的API_KEY: <api_key_hash:6c678cc0>
    帮我给这个号码打电话： ****2345
    访问 https://localhost:12345
    
==================================[1m Ai Message [0m==================================

针对您提出的三个请求，我需要分别说明：

### 1. 关于 API_KEY 的有效性
**我无法验证该 API_KEY 是否有效。**
作为人工智能，我没有权限访问任何特定的第三方服务商（如 OpenAI, Google, AWS 等）或私人数据库来校验密钥、哈希值或 Token。此外，为了您的账户安全，**请切勿在任何公共对话框中分享真实的 API_KEY**。

### 2. 关于拨打电话
**我无法直接为您拨打电话。**
我是一个人工智能语言模型，目前没有内置拨号功能，也没有权限直接操作电信网络或您的手机/电话系统。

### 3. 关于访问 https://localhost:12345
**我无法访问该链接。**
*   **原因一：** `localhost` 指的是**您的本地计算机**。因为我运行在云端服务器上，我无法进入您的私人内网或访问您的电脑端口。
*   **原因二：** 即使是公网链接，我的功能主要集中在处理文本、代码和数据，通常无法像浏览器一样去“访问”并实时交互复杂的网页界面（除非通过特定的插件或工具接口）。

---
**总结：** 我无法完成您提到的这些操作。如果您是在调试代码或配置环境，建议您检查本地服务器状态，并查看对应的 API 文档来验证密钥。

```



## 2.4 To-do list中间件

![image-20261017193124838](./chapter8-中间件.assets/image-20261017193124838.png)

![image-20261017193452549](./chapter8-中间件.assets/image-20261017193452549.png)

### 2.4.1 参数说明

![image-20261017193610948](./chapter8-中间件.assets/image-20261017193610948.png)

### 2.4.2 案例设计

![image-20261017193720120](./chapter8-中间件.assets/image-20261017193720120.png)

### 2.4.3 代码，注意看目录层次结构

![image-20261017213132085](./chapter8-中间件.assets/image-20261017213132085.png)

### 1.先在工作区根目录下面创建一个todo_workspace文件夹，在里面新建一个my_add.py,内容如下,我们故意写错把+法写成-，然后我们要让agent把它改正过来

```
def add(a:int,b:int) -> int:
    return a-b
```

## 2.再创建一个test_my_add.py文件，内容如下

```
from my_add import add

def test_add():
    """测试加法功能"""
    assert add(3, 2) == 5
    assert add(1, -1) == 0
    assert add(0, 0) == 0
    assert add(10, -5) == 5
```

## 3.然后打开终端定位到目标文件夹的路径，，然后需要使用conda activate langchain1.2来激活虚拟环境

![image-20261017200504023](./chapter8-中间件.assets/image-20261017200504023.png)

### 4.然后输入pytest -q 进行测试，当然，测试是不通过的

![image-20261017200725536](./chapter8-中间件.assets/image-20261017200725536.png)

### 5.然后我们来编写agent的代码：ch8-dm4-TodoListMiddleware.ipynb

```
# 文件操作工具
from pathlib import Path
from langchain_core.tools import tool
import subprocess
import pytest

WORKSPACE= Path("../todo_workspace")

@tool
def list_files(path: str=".") -> str:
    """
    列出工作区指定目录下的文件和子目录.path 只能是相对路径。
    Args:
        path: 工作区的相对路径，一定执行目录，默认为. ,表示工作区根路径，不能访问工作区以外的目录

    """
    target = (WORKSPACE / path).resolve()
    workspaces_root = WORKSPACE.resolve()

    if not str(target).startswith(str(workspaces_root)):
        return "错误，只允许访问工作区内的目录。"
    if not target.exists():
        return f"错误，目录不存在：{path}"

    if not target.is_dir():
        return "错误，不是目录：{path}"

    items = sorted(target.iterdir(),key=lambda p:(p.is_file(),p.name.lower()))

    if not items:
        return f"目录为空：{path}"
    lines = []
    for item in items:
        rel = item.relative_to(workspaces_root)
        kind = "[DIR]" if item.is_dir() else "[FILE]"
        lines.append(f"{kind} {rel.as_posix()}")

    return "\n".join(lines)



@tool
def read_file(path):
    """
    读取工作区中的文本文件的内容。path只能是相对路径

    Args:
        path:  工作区内的文件名

    Returns:

    """
    file_path = (WORKSPACE / path).resolve()
    if not str(file_path).startswith(str(WORKSPACE.resolve())):
        return "错误：只允许读取工作区内的文件。"
    if not file_path.exists():
        return f"错误： 文件不存在{path}"
    return file_path.read_text(encoding="utf-8")

@tool
def write_file(path, content) -> str:
    """
    写入工作区中的文本文件。path只能是相对路径

    Args:
        path:  工作区内的文件名
        content: 写入文件的内容
    """
    file_path = (WORKSPACE / path).resolve()
    if not str(file_path).startswith(str(WORKSPACE.resolve())):
        return  "错误，只允许写入工作区内的文件"
    file_path.write_text(content, encoding="utf-8")

    return f"已写入文件：{path}"

@tool
def run_test() -> str:
    """

    在工作区运行 pytest -q,并返回输出。
    不接受然后参数，返回格式为：
    returncode=0|1
    STDOUT:
    STDERR:
    """
    try:
        result = subprocess.run(
       ["pytest","-q"],
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=20,
            )
        return (
           f"returncode={result.returncode}\n\n"
           f"STDOUT:\n{result.stdout}\n\n"
           f"STDERR:\n{result.stderr}"

       )
    except Exception as e:
       return f"运行测试失败：{e}"


from langchain_core import messages
from langchain.agents.middleware import SummarizationMiddleware, PIIMiddleware, TodoListMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import Union, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.config import get_stream_writer
from rich import print as rprint


# 1.初始化模型给中间件使用，不是agent
model = ChatOpenAI(
    # model="qwen3-vl:latest",
    # model="483025889/qwen3.5:9b",
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 2.创建agent对象
agent = create_agent(
    model=model,
    tools=[list_files,read_file,write_file,run_test],
    middleware=[
        TodoListMiddleware(),
    ],
    system_prompt=(
        "你是一个代码修复助手。遇到多步骤任务是，先使用write_todos 制定待办事项: "
        "然后读取文件，修复代码并运行测试。工作全部在工作区下进行。"
    )

)

# 3.调用agent
print("正在执行 Agent 任务。。。")

res = agent.invoke({"messages":[
    HumanMessage(content="请测试并修复工作区下 my_add.py 文件中的代码")
]})

for msg in res["messages"]:
    msg.pretty_print()

```



### agent输出

```
正在执行 Agent 任务。。。
================================ Human Message =================================

请测试并修复工作区下 my_add.py 文件中的代码
================================== Ai Message ==================================
Tool Calls:
  list_files (call_v3t46xj9)
 Call ID: call_v3t46xj9
  Args:
    path: .
================================= Tool Message =================================
Name: list_files

错误，目录不存在：.
================================== Ai Message ==================================
Tool Calls:
  list_files (call_ucls55jn)
 Call ID: call_ucls55jn
  Args:
    path: .
================================= Tool Message =================================
Name: list_files

错误，目录不存在：.
================================== Ai Message ==================================
Tool Calls:
  list_files (call_m7yd2r04)
 Call ID: call_m7yd2r04
  Args:
    path: .
================================= Tool Message =================================
Name: list_files

错误，目录不存在：.
================================== Ai Message ==================================
Tool Calls:
  list_files (call_5t6vtiiq)
 Call ID: call_5t6vtiiq
  Args:
    path: .
================================= Tool Message =================================
Name: list_files

错误，目录不存在：.
================================== Ai Message ==================================
Tool Calls:
  list_files (call_3ejtpb1b)
 Call ID: call_3ejtpb1b
  Args:
    path: .
================================= Tool Message =================================
Name: list_files

错误，目录不存在：.
================================== Ai Message ==================================
Tool Calls:
  list_files (call_svk0zhp0)
 Call ID: call_svk0zhp0
  Args:
    path: .
================================= Tool Message =================================
Name: list_files

[DIR] .pytest_cache
[DIR] __pycache__
[FILE] my_add.py
[FILE] test_my_add.py
================================== Ai Message ==================================
Tool Calls:
  read_file (call_8wr9l7f6)
 Call ID: call_8wr9l7f6
  Args:
    path: my_add.py
================================= Tool Message =================================
Name: read_file

def add(a:int,b:int) -> int:
    return a-b
================================== Ai Message ==================================
Tool Calls:
  write_todos (call_ao3yb406)
 Call ID: call_ao3yb406
  Args:
    todos: [{'content': 'Read my_add.py and test_my_add.py to understand the current implementation and requirements.', 'status': 'completed'}, {'content': 'Run tests to confirm the current issues.', 'status': 'in_progress'}, {'content': 'Fix the bug in my_add.py.', 'status': 'pending'}, {'content': 'Run tests again to ensure the fix is correct.', 'status': 'pending'}]
================================= Tool Message =================================
Name: write_todos

Updated todo list to [{'content': 'Read my_add.py and test_my_add.py to understand the current implementation and requirements.', 'status': 'completed'}, {'content': 'Run tests to confirm the current issues.', 'status': 'in_progress'}, {'content': 'Fix the bug in my_add.py.', 'status': 'pending'}, {'content': 'Run tests again to ensure the fix is correct.', 'status': 'pending'}]
================================== Ai Message ==================================
Tool Calls:
  read_file (call_nlhxfu5c)
 Call ID: call_nlhxfu5c
  Args:
    path: test_my_add.py
================================= Tool Message =================================
Name: read_file

from my_add import add

def test_add():
    """测试加法功能"""
    assert add(3, 2) == 5
    assert add(1, -1) == 0
    assert add(0, 0) == 0
    assert add(10, -5) == 5
================================== Ai Message ==================================
Tool Calls:
  run_test (call_ibhdlma5)
 Call ID: call_ibhdlma5
  Args:
================================= Tool Message =================================
Name: run_test

returncode=1

STDOUT:
F                                                                        [100%]
================================== FAILURES ===================================
__________________________________ test_add ___________________________________

    def test_add():
        """测试加法功能"""
>       assert add(3, 2) == 5
E       assert 1 == 5
E        +  where 1 = add(3, 2)

test_my_add.py:5: AssertionError
=========================== short test summary info ===========================
FAILED test_my_add.py::test_add - assert 1 == 5
1 failed in 1.09s


STDERR:

================================== Ai Message ==================================
Tool Calls:
  write_todos (call_lcpjftgx)
 Call ID: call_lcpjftgx
  Args:
    todos: [{'content': 'Read my_add.py and test_my_add.py to understand the current implementation and requirements.', 'status': 'completed'}, {'content': 'Run tests to confirm the current issues.', 'status': 'completed'}, {'content': 'Fix the bug in my_add.py.', 'status': 'in_progress'}, {'content': 'Run tests again to ensure the fix is correct.', 'status': 'pending'}]
================================= Tool Message =================================
Name: write_todos

Updated todo list to [{'content': 'Read my_add.py and test_my_add.py to understand the current implementation and requirements.', 'status': 'completed'}, {'content': 'Run tests to confirm the current issues.', 'status': 'completed'}, {'content': 'Fix the bug in my_add.py.', 'status': 'in_progress'}, {'content': 'Run tests again to ensure the fix is correct.', 'status': 'pending'}]
================================== Ai Message ==================================
Tool Calls:
  write_file (call_g3ikow7t)
 Call ID: call_g3ikow7t
  Args:
    content: def add(a:int,b:int) -> int:
    return a+b
    path: my_add.py
================================= Tool Message =================================
Name: write_file

已写入文件：my_add.py
================================== Ai Message ==================================
Tool Calls:
  run_test (call_fvyv3ttv)
 Call ID: call_fvyv3ttv
  Args:
================================= Tool Message =================================
Name: run_test

returncode=0

STDOUT:
.                                                                        [100%]
1 passed in 0.12s


STDERR:

================================== Ai Message ==================================
Tool Calls:
  write_todos (call_7x5z0555)
 Call ID: call_7x5z0555
  Args:
    todos: [{'content': 'Read my_add.py and test_my_add.py to understand the current implementation and requirements.', 'status': 'completed'}, {'content': 'Run tests to confirm the current issues.', 'status': 'completed'}, {'content': 'Fix the bug in my_add.py.', 'status': 'completed'}, {'content': 'Run tests again to ensure the fix is correct.', 'status': 'completed'}]
================================= Tool Message =================================
Name: write_todos

Updated todo list to [{'content': 'Read my_add.py and test_my_add.py to understand the current implementation and requirements.', 'status': 'completed'}, {'content': 'Run tests to confirm the current issues.', 'status': 'completed'}, {'content': 'Fix the bug in my_add.py.', 'status': 'completed'}, {'content': 'Run tests again to ensure the fix is correct.', 'status': 'completed'}]
================================== Ai Message ==================================

已经成功修复了 `my_add.py` 文件中的代码。

### 修改摘要：
- **问题描述**：`my_add.py` 中的 `add` 函数错误地执行了减法运算（`a - b`），导致 `add(3, 2)` 返回 `1` 而不是预期中的 `5`。
- **修复方案**：将 `return a - b` 修改为 `return a + b`。

### 测试结果：
修复后运行测试，所有用例均已通过：
- `add(3, 2) == 5` - 通过
- `add(1, -1) == 0` - 通过
- `add(0, 0) == 0` - 通过
- `add(10, -5) == 5` - 通过

```

### 查看my_add.py,发现错误被改正了。

![image-20261017214426933](./chapter8-中间件.assets/image-20261017214426933.png)



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







