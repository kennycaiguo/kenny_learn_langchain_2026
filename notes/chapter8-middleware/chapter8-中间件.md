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







