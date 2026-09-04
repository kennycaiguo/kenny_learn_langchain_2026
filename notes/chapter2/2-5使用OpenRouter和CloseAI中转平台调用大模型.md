# 为什么需要中转平台

![image-20260903123940869](./2-5使用OpenRouter和CloseAI中转平台调用大模型.assets/image-20260903123940869.png)

# OpenRouter

## 官网：https://OpenRouter.ai

![image-20260903125534711](./2-5使用OpenRouter和CloseAI中转平台调用大模型.assets/image-20260903125534711.png)

```
pip install langchain-openrouter
```

## 把上面的库安装了，然后到官网获取api key保存到.env文件中

## 案例:ch2-demo6-openrouter.ipynb

```
from dotenv import load_dotenv
import os
from langchain_openrouter import ChatOpenRouter

load_dotenv(override=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE")

llm = ChatOpenRouter(
    model="glm-5.3-flash",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_API_BASE
)

resp = llm.invoke("奇门遁甲是什么")
print(resp.text)
```



### 模型输出

![image-20260903132408129](./2-5使用OpenRouter和CloseAI中转平台调用大模型.assets/image-20260903132408129.png)

## 利用ChatOpenRouter调用DeepSeek大模型

```
from dotenv import load_dotenv
import os
from langchain_openrouter import ChatOpenRouter

load_dotenv(override=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE")

llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_API_BASE
)

resp = llm.invoke("奇门遁甲是什么")
print(resp.text)
```



### 模型输出

![image-20260903133920808](./2-5使用OpenRouter和CloseAI中转平台调用大模型.assets/image-20260903133920808.png)

## OpenRouter只有2次免费使用，用完了。。。

# CloseAI

## 官网：https://www.closeai-asia.com

![image-20260903141011047](./2-5使用OpenRouter和CloseAI中转平台调用大模型.assets/image-20260903141011047.png)

## 需要获取api key和base url保存到.env文件中

# CloseAI需要收费，没有免费额度

### 参考代码如下

```
from openai import OpenAI
from dotenv import load_dotenv
import os

CLOSEAI_API_KEY = os.getenv("CLOSEAI_API_KEY")

client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key=CLOSEAI_API_KEY,
)

chatModel = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say hi",
        }
    ],
    model="gpt-3.5-turbo",
)
print(chatModel.choices[0].message.content)
```



# CUN.ai

user:kennycai2

pwd:name+year

