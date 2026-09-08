# 扩展内容

## 1.美化输出

### 1》使用模型的pretty_print()方法

![image-20260908094234388](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908094234388.png)

### 2》使用rich库：pip install rich

![image-20260908094817148](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908094817148.png)

## 2.模型配置信息profile

![image-20260908095001835](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908095001835.png)

### 示例1

![image-20260908095027943](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908095027943.png)

### 很多模型的profile都是空，OpenRouter里面的就有数据

![image-20260908103509862](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908103509862.png)

### 其实，也不是挺重要，了解即可



## 3.完整的模型初始化参数

### 1》所有初始化参数

![image-20260908104543722](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908104543722.png)

#### 输出参考练习源码

### 2>模型类的参数构成，以ChatDeepSeek为例

#### 2.1客户端与连接参数

![image-20260908105828823](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908105828823.png)

#### 2.2模型推理参数

![image-20260908110145855](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908110145855.png)

#### 2.3.langchain框架通用参数

![image-20260908110336906](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908110336906.png)

#### 2.4 高级与特定的扩展参数

![image-20260908111053774](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908111053774.png)

### 参数：model_kwargs

![image-20260908111439028](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908111439028.png)

#### 老师的示例，tools参数可以告诉模型使用什么工具，如果你的问题和这个工具有关，模型就会调用这个工具，如果没有关系，模型就不会调用这个工具

![image-20260908112000651](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908112000651.png)

## 有些模型虽然支持工具调用，但是，无法获取到天气信息，比如下面的开源chat-gpt

```
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage


llm = init_chat_model(
    model="openai/gpt-oss-120b",  # 指定具体的 Groq 模型名称,开源gpt模型
    # model="groq/compound-mini",  # 指定具体的 Groq 模型名称，这个模型不支持工具调用
    # model="groq/compound",  # 指定具体的 Groq 模型名称，这个模型不支持工具调用
    model_kwargs={
                "tools":[
                    {
                        "type":"function",
                        "function":{
                            "name":"get_weather",
                            "description":"Get weather of a location,the user should supply the location first.",
                            "parameters":{
                                "type":"object",
                                "properties":{
                                    "location":{
                                        "type":"string",
                                        "description":"The City and state,e.g. San Francisco,CA",
                                    }
                                },
                                "required":["location"]
                            }
                        },
                    }
                ]
            },
    model_provider="groq",    # 明确指定提供商为 groq
    temperature=0.7
)

# 调用模型
messages = [
    HumanMessage(content="今天北京会下雨吗"),
    # HumanMessage(content="什么水果对肾好？"),
]

response = llm.invoke(messages)

# 打印输出结果
response.pretty_print()
```



## 模型输出

![image-20260908140200193](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908140200193.png)



### 参数：extra_body

![image-20260908140848193](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908140848193.png)

### 演练，本地大模型也支持extra_body

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b',
    extra_body={
        "thinking":{"type":"enabled"}
    }
)

question = "女人法语怎么说"

result = llm.invoke(question)
print(result.content)
```



### 模型输出

![image-20260908141004483](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908141004483.png)

### 需要记住的参数

![image-20260908141902214](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908141902214.png)

### 在常用参数里面找不到的，可能就需要使用model_kwargs或者extra_body来设置，具体参考相关模型厂商的参考文档

## 4.模型调用中的config参数

![image-20260908141706439](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908141706439.png)

### config参数中的可配参数

![image-20260908142054723](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908142054723.png)

### config中支持配置的参数

![image-20260908143419871](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908143419871.png)

### 参数说明

![image-20260908143849427](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908143849427.png)

![image-20260908143932787](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908143932787.png)

![image-20260908144552952](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908144552952.png)

### 写了configurable参数后，你需要设置哪些属性可以手动配置，否则配置不生效

![image-20260908144958584](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908144958584.png)

### 演练，在调用本地大模型的时候传递config参数，不过现在好像还没有什么作用

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b',
    extra_body={
        "thinking":{"type":"enabled"}
    }
)

question = "女人法语怎么说"

result = llm.invoke(
    question,
    config={
        "run_name":"my test",
        "tags":["test","development"],
        "metadata":{"user_id":'124'},
        # 暂时不使用callback参数，等到用到的时候才添加
        "configurable":{
            "model":"deepseek-reasoner",
            "temprature":0.7,
             "max_tokens":200
        }
    }

)
print(result.content)
```



### 模型输出

![image-20260908143724454](./2-12profile属性_初始化model_kwargs与extra_body参数调用的config参数.assets/image-20260908143724454.png)















