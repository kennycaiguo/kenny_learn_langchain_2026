# 调用Google的Gemini大模型

## pip install google-genai

### 注意，gemini-2.x-xx的模型已经不给新用户使用了，

### 可以使用：gemini-3.5-flash或者gemini-3.1-flash-lite


```python
# 使用genai接口
import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
gemini_api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key=gemini_api_key)
resp = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=["Define autonomous AI agent in one line."]
)

print(resp.text)

```

### 模型输出

    An autonomous AI agent is a software system capable of perceiving its environment, reasoning, and executing a sequence of actions independently to achieve predefined goals without continuous human intervention.

### 第二种写法，使用openai接口

```python
# 使用openai接口
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
gemini_api_key = os.getenv("gemini_api_key")
client = OpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
resp = client.chat.completions.create(
     model="gemini-3.1-flash-lite",
     messages=[{
         "role":"user","content":"Define autonomous AI agent in one line."
     }]
)
    


print(resp.choices[0].message.content)
```

### 模型输出

    An autonomous AI agent is a system capable of perceiving its environment, reasoning to achieve specific goals, and executing sequences of actions independently without human intervention.



