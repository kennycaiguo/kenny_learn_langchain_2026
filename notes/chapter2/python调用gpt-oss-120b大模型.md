AI 概览

## **llama-3.3-70b-versatile已经不能够使用了**

你可以通过访问 Groq Console 获取 API Key，并使用 Python 的 `groq` 库来调用 `openai/gpt-oss-120b` 大模型。 

获取apikey的链接：https://console.groq.com/docs/text-chat

### 1.安装依赖库

在终端中运行以下命令安装官方 Python SDK： [[1](https://github.com/livekit-examples/groq-voice-assistant/blob/main/README.md), [2](https://console.groq.com/docs/text-chat)]

bash

```
pip install groq
```

请谨慎使用此类代码。

### 2.配置 API Key

推荐将 `GROQ_API_KEY` 设置为环境变量，或者直接在代码中填入。 [[1](https://www.ibm.com/docs/en/instana-observability?topic=providers-grok)]

- **Linux/macOS**: `export GROQ_API_KEY="你的API_KEY"`
- **Windows**: `set GROQ_API_KEY="你的API_KEY"`

### 3.实例代码

```
from groq import Groq

client = Groq()
chat = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{
        "role":"user","content":"Introduce yourself"
    }]
)

print(chat.choices[0].message.content)
```



### 模型输出

```
Hello! I’m ChatGPT, an AI language model created by OpenAI. I’m designed to understand and generate text across a wide range of topics, from answering factual questions and explaining concepts to brainstorming ideas, helping with writing, and just having a friendly chat. Think of me as a versatile conversational partner who can provide information, assistance, and a bit of creativity whenever you need it. How can I help you today?
```

