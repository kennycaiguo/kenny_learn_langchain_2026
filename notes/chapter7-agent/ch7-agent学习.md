# 1.理解Agent

![image-20260928124115252](./ch7-agent学习.assets/image-20260928124115252.png)

## 1.1 什么是Agent？

![image-20260928124311794](./ch7-agent学习.assets/image-20260928124311794.png)

## 1.2 Agent的核心组件

![image-20260928124629196](./ch7-agent学习.assets/image-20260928124629196.png)

### 1.3 Agent的创建与调用

### 1.3.1 历史上的调用

![image-20260928124823529](./ch7-agent学习.assets/image-20260928124823529.png)

  ![image-20260928125014734](./ch7-agent学习.assets/image-20260928125014734.png)

### 1.3.2 全新调用

![image-20260928125111882](./ch7-agent学习.assets/image-20260928125111882.png)

#### 实例

```
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from rich import print as rprint
# 1.初始化模型
model = ChatOpenAI(
    # model="mistral-nemo:latest",
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)
# 2.创建agent
agent = create_agent(
    model=model,
    tools=[],
    system_prompt="Agent的行为指令" # 可选
)
# 3.调用
result = agent.invoke({
    "messages":[{"role":"user","content":"介绍一下你自己"}]
})

rprint(result)
```



#### Agent输出：

![image-20260928131038440](./ch7-agent学习.assets/image-20260928131038440.png)

### 注意：Agent是会使用工具的。我们把一些工具封装到一个tool_utils.py文件中，内容如下

```
## 定义工具
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests
import os


# 工具1
@tool(parse_docstring=True)
def get_stock_price(company:str,timeframe: str="today") ->str:
    """ 
    获取指定公司的股票在指定时间的价格

    Args:
         company : 具体的公司名称
         timeframe : 时间范围 (today-今日,week-本周,month-本月)

    """
    print(timeframe)
    stock_data = {
        "苹果公司":{"today":185.2,"week":183.5,"month":180.75},
        "谷歌公司":{"today":15.42,"week":15.2,"month":14.85},
        "微软公司":{"today":415.86,"week":412.30,"month":405.42},
    }

    if company in stock_data:
        price = stock_data[company].get(timeframe,"")
        return f"{company} {timeframe}的股价是{price}美元"
    else:
        return f"没有找到{company}的股票信息。"

## 工具2
@tool(parse_docstring=True)
def search_news(company:str) ->str:
    """ 
    搜索指定公司的新闻

    Args:
         company : 公司名称，如：谷歌公司

    Returns:
         指定公司的新闻     
    """
    news_data = {
        "苹果公司":[
            "发布新款Iphone，股价上涨3%","苹果与欧盟达成反垄断和解协议","苹果将在印度扩大生产规模"
        ],

        "谷歌公司":[
           "谷歌发布AI新模型，性能提升20%","谷歌与OpenAI合作，开发AI新模型","谷歌在欧洲开展AI新研究项目",
        ],

        "微软公司":[
           "微软Azuze云业务季度增长超预期","微软完成对Nuance公司的收购","微软推出新一代AI助手Copilot"
        ],
    }

    if company in news_data:
        return "\n".join(news_data[company])
    else:
        return f"找不到关于{company}的新闻"

## 使用docstring方式不需要arg_schema
@tool(parse_docstring=True)
def get_weather2(city:str="北京",if_forecast:bool=False):
    """ 
    查询当天的天气，可以包含明天的天气预报

    Args:
         city : 具体的城市
         if_forecast : 是否包含明天的天气预报

    Returns:
         城市的当天的天气，可以包含明天的天气预报     
    """
    res = f"{city}明天天气不错"
    if if_forecast:
        res += f"\n{city}明天有大到暴雨"
    return res 

    
## 真正可以查询天气的工具
@tool
def query_weather_from_web(city="Beijing", aqi="no", language="zh_cn"):
     """ 
             获取指定城市的天气信息
             参数：
             city：城市的名称，如"上海"
             api_key: OpenWeather的api key
             返回值：
                         天气信息字符串
          
    """ 
     load_dotenv(override=True)
     appid = os.getenv("Weather_api_key")
     # 构建请求URL
     url = "https://api.weatherapi.com/v1/current.json"
     # 设置查询参数
     params = {
         "q": city,                 # 查询的城市，默认为北京
         "key": appid,          # API密钥
         "aqi": aqi,            # 测量单位，默认为摄氏度
         "lang": language           # 输出语言，默认为简体中文
     }
     # 发送GET请求
     response = requests.get(url, params=params)
     # 检查响应状态
     if response.status_code == 200:
         # 解析响应数据
         data = response.json()
         return data
     
     else:
         print(f"查询失败，状态码：{response.status_code}")
         print("响应数据：", response.text)
         return {"error":"weather api 调用失败。。。"}
         


```



### 里面有一个工具函数可以调用webapi查询天气，我们把它以工具的发送传递给agent

```
## agent会使用工具？
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from rich import print as rprint
from tool_utils import  query_weather_from_web
# 1.初始化模型
model = ChatOpenAI(
    # model="mistral-nemo:latest",
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)
# 2.创建agent
agent = create_agent(
    model=model,
    tools=[query_weather_from_web],
    system_prompt="Agent的行为指令" # 可选
)
# 3.调用
result = agent.invoke({
    "messages":[{"role":"user","content":"北京明天的天气如何？"}]
})

rprint(result)
```



### agent输出

![image-20260929154116863](./ch7-agent学习.assets/image-20260929154116863.png)

# 2.Agent的基本用法1：模型的传入方式

![image-20260929154440344](./ch7-agent学习.assets/image-20260929154440344.png)

## 2.1 传入模型字符串

![image-20260929161904258](./ch7-agent学习.assets/image-20260929161904258.png)

![image-20260929154630161](./ch7-agent学习.assets/image-20260929154630161.png)

### 注意：创建agent是需要langgraph支持的。

### 举例代码1，在线模型

```
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv(override=True)

agent = create_agent(
    "groq:openai/gpt-oss-120b", # 必须给出模型提供商比,如这里的groq:
)
print(type(agent))

from IPython.display import Image,display
display(Image(agent.get_graph().draw_mermaid_png()))
```

### 运行结果

![image-20260929161649957](./ch7-agent学习.assets/image-20260929161649957.png)

### 举例2，本地大模型

```
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv(override=True)

agent = create_agent(
    "ollama:qwen3-vl:latest", # 必须给出模型提供商比,如这里的groq:
)
print(type(agent))

from IPython.display import Image,display
display(Image(agent.get_graph().draw_mermaid_png()))
```

### 运行结果

![image-20260929162006139](./ch7-agent学习.assets/image-20260929162006139.png)

## 2.2 传入模型对象

![image-20260929154732800](./ch7-agent学习.assets/image-20260929154732800.png)

# 3.Agent的基本用法2：如何调用Agent

![image-20260929162936507](./ch7-agent学习.assets/image-20260929162936507.png)

![image-20260929163124830](./ch7-agent学习.assets/image-20260929163124830.png)

#### 实例代码参考上面的例子

# 4.Agent的基本用法3：绑定工具

![image-20260929164630097](./ch7-agent学习.assets/image-20260929164630097.png)

## 查看langchain的内置工具，网址： https://www.langchain.com.cn/docs/integrations/tools/



## 4.1 基本用法：

### 举例1：绑定一个工具

![image-20260929164748611](./ch7-agent学习.assets/image-20260929164748611.png)

### 实例代码

```

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from rich import print as rprint
from tool_utils import  query_weather_from_web
# 1.初始化模型
model = ChatOpenAI(
    # model="mistral-nemo:latest",
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)
# 2.创建agent
agent = create_agent(
    model=model,
    tools=[query_weather_from_web],
    system_prompt="Agent的行为指令" # 可选
)
# 3.调用
result = agent.invoke({
    "messages":[{"role":"user","content":"北京明天的天气如何？"}]
})

rprint(result)
```



### agent输出

![image-20260929164859993](./ch7-agent学习.assets/image-20260929164859993.png)

### 举例2：接入内置工具

#### 这里我们使用TavilyResearch，我们需要先获取他的api key保存到.env文件中。

```
import os

from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_tavily import TavilyResearch

load_dotenv(override=True)

tavily_api_key = os.getenv("Tavily_api_key")
# 创建langchain内置工具实例
tavily = TavilyResearch(
    max_results=2,
    tavily_api_key=tavily_api_key,
)

agent = create_agent(
    "ollama:carstenuhlig/omnicoder-9b:latest",  # 必须给出模型提供商比,如这里的ollama，这个模型还好
    tools=[tavily]
)
# print(type(agent))
resp = agent.invoke({
    "messages":[
        {"role":"user","content":"请帮我查一下2024年诺贝尔物理学奖得主是谁？"}
    ]
})



from IPython.display import Image, display

display(Image(agent.get_graph().draw_mermaid_png()))

```

### agent输出

![image-20260929194220372](./ch7-agent学习.assets/image-20260929194220372.png)

```
print(resp)
```



### agent 输出

![image-20260929194331796](./ch7-agent学习.assets/image-20260929194331796.png)

### 举例3：绑定多个工具

```
from langchain_core.tools import tool
import os

from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_tavily import TavilyResearch


load_dotenv(override=True)


@tool(parse_docstring=True)
def get_weather(city:str="广州"):
    """
    查询具体城市的天气

    Args:
          city : 城市名称，如北京

    Returns:
            城市当天的天气
    """
    return f"{city}今天天气很好，阳光明媚，适合郊游~~"


@tool(parse_docstring=True)
def get_news() ->str:
    """
    获取新闻

    Returns:
             返回当前的热点新闻
    """
    return "最近AI智能体非常火爆，有大量的工作岗位缺口，需求量非常大!!!"

agent = create_agent(
    # "ollama:mistral-nemo:latest",  # 必须给出模型提供商比,如这里的ollama:
    # "ollama:granite3.2:8b",  # 必须给出模型提供商比,如这里的ollama:
    "ollama:qwen3-vl:latest",  # 必须给出模型提供商比,如这里的ollama:
    tools=[get_weather,get_news]
)
# print(type(agent))
resp = agent.invoke({
    "messages":[
        {"role":"user","content":"广州今天天气怎么样？最近有什么新闻？"}
    ]
})

print(resp["messages"][-1])

```



### agent输出

![image-20260929194429277](./ch7-agent学习.assets/image-20260929194429277.png)

## 4.2工具调用流程分析

![image-20260929194517360](./ch7-agent学习.assets/image-20260929194517360.png)

![image-20260929194837247](./ch7-agent学习.assets/image-20260929194837247.png)

![image-20260929195010577](./ch7-agent学习.assets/image-20260929195010577.png)

![image-20260929195626628](./ch7-agent学习.assets/image-20260929195626628.png)

## 4.3 重试机制

![image-20260929195826732](./ch7-agent学习.assets/image-20260929195826732.png)

### 举例代码

```
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
import os

from langchain.agents import create_agent
from dotenv import load_dotenv
from rich import print as rprint


load_dotenv(override=True)

flag = 0
@tool(parse_docstring=True)
def get_weather(city:str="广州"):
    """
    查询具体城市的天气

    Args:
          city : 城市名称，如北京

    Returns:
            城市当天的天气
    """
    global flag
    flag += 1
    if flag < 3:
        return "TEMP_UNAVAILABLE:天气服务暂时不可用，请稍后重试"
    return f"{city}今天天气很好，阳光明媚，适合郊游~~"

agent = create_agent(
    # "ollama:mistral-nemo:latest",  # 必须给出模型提供商比,如这里的ollama:
    # "ollama:granite3.2:8b",  # 必须给出模型提供商比,如这里的ollama:
    "ollama:qwen3-vl:latest",  # 必须给出模型提供商比,如这里的ollama:
    tools=[get_weather]
)
msgs = [
    SystemMessage("""
    你是一个天气助手。
    当工具返回以'TEMP_UNAVAILABLE:' 开头的结果时，
    你应该再次调用同一个工具，最多重试3次。
    如果3次后仍然失败，再向用户说明服务暂时不可用。
    """),
    HumanMessage("杭州今天的天气如何？")
]
resp = agent.invoke({"messages":msgs})

rprint(resp)
```



### agent输出,有点长，但是agent的确重试了3次，最后得到结果了

```
{
    'messages': [
        SystemMessage(
            content="\n    你是一个天气助手。\n    当工具返回以'TEMP_UNAVAILABLE:' 开头的结果时，\n    
你应该再次调用同一个工具，最多重试3次。\n    如果3次后仍然失败，再向用户说明服务暂时不可用。\n    ",
            additional_kwargs={},
            response_metadata={},
            id='4ac16108-5bfd-45cf-8ea0-9bc83eed8c85'
        ),
        HumanMessage(
            content='杭州今天的天气如何？',
            additional_kwargs={},
            response_metadata={},
            id='de9bc1cc-5a07-46ac-b0ba-4d88185b31a0'
        ),
        AIMessage(
            content='',
            additional_kwargs={},
            response_metadata={
                'model': 'qwen3-vl:latest',
                'created_at': '2026-09-30T02:12:43.880292Z',
                'done': True,
                'done_reason': 'stop',
                'total_duration': 40245963400,
                'load_duration': 10443900,
                'prompt_eval_count': 210,
                'prompt_eval_duration': 9708206000,
                'eval_count': 152,
                'eval_duration': 30447709000,
                'logprobs': None,
                'model_name': 'qwen3-vl:latest',
                'model_provider': 'ollama'
            },
            id='lc_run--01a0f015-4faf-7312-82d3-e1f2e9ba5ec9-0',
            tool_calls=[
                {
                    'name': 'get_weather',
                    'args': {'city': '杭州'},
                    'id': '64c9c089-ce3a-4652-909e-c3ca81497002',
                    'type': 'tool_call'
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={'input_tokens': 210, 'output_tokens': 152, 'total_tokens': 362}
        ),
        ToolMessage(
            content='TEMP_UNAVAILABLE:天气服务暂时不可用，请稍后重试',
            name='get_weather',
            id='20a8f296-4cba-4fd3-81d4-a28263897f7f',
            tool_call_id='64c9c089-ce3a-4652-909e-c3ca81497002'
        ),
        AIMessage(
            content='',
            additional_kwargs={},
            response_metadata={
                'model': 'qwen3-vl:latest',
                'created_at': '2026-09-30T02:13:18.019742Z',
                'done': True,
                'done_reason': 'stop',
                'total_duration': 34122387100,
                'load_duration': 9664100,
                'prompt_eval_count': 257,
                'prompt_eval_duration': 3375635000,
                'eval_count': 141,
                'eval_duration': 30727596000,
                'logprobs': None,
                'model_name': 'qwen3-vl:latest',
                'model_provider': 'ollama'
            },
            id='lc_run--01a0f015-ecf6-77d1-b487-ed03c9f87b46-0',
            tool_calls=[
                {
                    'name': 'get_weather',
                    'args': {'city': '杭州'},
                    'id': '879565e3-0525-45ce-80a3-3fbea989ce78',
                    'type': 'tool_call'
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={'input_tokens': 257, 'output_tokens': 141, 'total_tokens': 398}
        ),
        ToolMessage(
            content='TEMP_UNAVAILABLE:天气服务暂时不可用，请稍后重试',
            name='get_weather',
            id='5ccf8308-50c1-4244-9d42-96e43dadd355',
            tool_call_id='879565e3-0525-45ce-80a3-3fbea989ce78'
        ),
        AIMessage(
            content='',
            additional_kwargs={},
            response_metadata={
                'model': 'qwen3-vl:latest',
                'created_at': '2026-09-30T02:14:11.9049592Z',
                'done': True,
                'done_reason': 'stop',
                'total_duration': 53874336100,
                'load_duration': 4831900,
                'prompt_eval_count': 304,
                'prompt_eval_duration': 3384616000,
                'eval_count': 227,
                'eval_duration': 50472155000,
                'logprobs': None,
                'model_name': 'qwen3-vl:latest',
                'model_provider': 'ollama'
            },
            id='lc_run--01a0f016-724c-78c2-8a4a-261f941de77b-0',
            tool_calls=[
                {
                    'name': 'get_weather',
                    'args': {'city': '杭州'},
                    'id': 'f31e21b1-f326-4f98-8fa7-4e69fd72db65',
                    'type': 'tool_call'
                }
            ],
            invalid_tool_calls=[],
            usage_metadata={'input_tokens': 304, 'output_tokens': 227, 'total_tokens': 531}
        ),
        ToolMessage(
            content='杭州今天天气很好，阳光明媚，适合郊游~~',
            name='get_weather',
            id='d12eb27d-3c45-4a49-9273-b207ee1ff912',
            tool_call_id='f31e21b1-f326-4f98-8fa7-4e69fd72db65'
        ),
        AIMessage(
            content='杭州今天天气很好，阳光明媚，适合郊游~~',
            additional_kwargs={},
            response_metadata={
                'model': 'qwen3-vl:latest',
                'created_at': '2026-09-30T02:14:45.3170612Z',
                'done': True,
                'done_reason': 'stop',
                'total_duration': 33399604100,
                'load_duration': 13671800,
                'prompt_eval_count': 349,
                'prompt_eval_duration': 3632446000,
                'eval_count': 159,
                'eval_duration': 29728191000,
                'logprobs': None,
                'model_name': 'qwen3-vl:latest',
                'model_provider': 'ollama'
            },
            id='lc_run--01a0f017-44cb-7773-87dc-6e453ca9595b-0',
            tool_calls=[],
            invalid_tool_calls=[],
            usage_metadata={'input_tokens': 349, 'output_tokens': 159, 'total_tokens': 508}
        )
    ]
}
```



## 4.4 常见问题

### 1.agent如何选择工具？

![image-20260929201646981](./ch7-agent学习.assets/image-20260929201646981.png)

### 2.agent为什么没有调用工具？

![image-20260929202058857](./ch7-agent学习.assets/image-20260929202058857.png)

### 3.agent选错工具？

![image-20260929202307377](./ch7-agent学习.assets/image-20260929202307377.png)

### 4.如何知道Agent何时完成？

![image-20260929202437181](./ch7-agent学习.assets/image-20260929202437181.png)

### 5.Agent可以调用多少次工具？

![image-20260929202607125](./ch7-agent学习.assets/image-20260929202607125.png)

### 6.如何限制工具调用次数

![image-20260929202727414](./ch7-agent学习.assets/image-20260929202727414.png)



# 5.Agent的高级用法1：实战Agent名称

## 5.1用法

## 5.2 经典使用场景



# 6.Agent的高级用法2：系统提示词



# 7.Agent的高级用法3：结构化输出

## 7.1模型与Agent的结构化输出对比

## 7.2 结构化输出的4种策略

### ①ProviderStrategy

### ②ToolStrategy

### ③type/AutoStrategy

### ④None

## 7.3ToolStrategy详解

### 7.3.1 结构化输出：schema参数

#### 输出模式1： Pydantic



#### 输出模式2 TypeDict



#### 输出模式3 JsonSchema



#### 输出模式4 @dataclass

#### 多schema输出模式

## 7.3.2自定义工具消息：tool_message_content参数

## 7.3.3错误处理：handle_errors参数

### 举例1：设置为True/False/固定字符串

### 举例2：设置为指定异常类型

### 举例3：设置为自定义错误处理函数

# 8.Agent的高级用法4：流式输出及模型

## 8.1流式输出的说明

## 8.2具体的输出模式

### 8.2.1 values输出模式

### 8.2.2 updates输出模式

### 8.2.3 messages输出模式

### 8.2.4 tasks输出模式

### 8.2.5 debug输出模式

### 8.2.6 checkpoints输出模式

### 8.2.7 custom输出模式

## 8.3 流式输出模式总结

# 9.实战：的功能智能体助手

## 9.1 模型的初始化

## 9.2 工具的定义

## 9.3 agent的创建

## 9.4 主程序























