在本地大模型（LLM）的开发中，如果你发现模型**确实成功触发并调用了工具（或者你感知到它执行了工具逻辑），但返回的 `tool_calls` 参数却是一个空列表 `[]`**，这通常是由以下几个最常见的原因导致的：

1. 提示词（Prompt）硬编码了工具逻辑

- **原因**：大模型并没有真正走官方的 Function Calling 协议，而是通过其强大的**上下文理解能力**，直接在生成的文本回复（`content`）中模仿了工具调用的格式（例如直接输出了 `{"name": "get_weather", "arguments": ...}`）。
- **表现**：`tool_calls` 为 `[]`，但 `message.content` 里包含大量的 JSON 文本或类似代码的字符串。
- 本地推理框架的 API 映射不完整

- **原因**：你使用的本地推理框架（如 Ollama, Llama.cpp, vLLM 等）与你的代码客户端（如 OpenAI SDK）之间存在**协议转换丢失**。
- **排查**：有些本地框架在旧版本中虽然能识别工具，但其返回的 JSON 结构与 OpenAI 标准的 `message.tool_calls` 不完全一致，导致 SDK 在解析时无法正确注入到 `tool_calls` 字段中，最终被归类为了普通的 `content`。
- 模型本身对工具调用的支持不稳定

- **原因**：除了少数原生对 Function Calling 做过深度微调的本地模型（如 `Hermes-3`、`Command R+`、`Qwen2.5-Instruct`、`Llama-3.1`），大部分开源模型对官方工具调用协议的支持较弱。它们经常会直接把工具调用当作普通的文本聊天内容输出。

🛠️ 怎么解决和排查？

第一步：打印完整的 Response 对象

不要只看 `tool_calls`，请把模型返回的完整 JSON 结构打印出来。

python

```
print(response.choices[0].message)
```

 

- 如果工具调用的参数出现在了 **`content`** 字段里，说明模型走的是“文本生成”而不是“工具规范”。
- 如果出现在了 **`function_call`**（旧版协议）里，说明需要更换解析字段。

第二步：检查本地框架和模型是否匹配

如果你使用的是 **Ollama** 或 **vLLM**：

1. **确认模型支持**：确保你选用的模型明确标注了支持 `Tools` 或 `Function Calling`（推荐使用 `qwen2.5` 或 `llama3.1`）。
2. **更新框架版本**：确保你的本地推理框架是最新版，因为各大框架对工具调用的 API 适配一直在频繁更新。

第三步：后备解析方案（脏数据清洗）

如果模型死活不走 `tool_calls` 字段，但能在 `content` 中稳定输出 JSON，你可以通过代码手动截获并解析：

python

```
import json

content = response.choices[0].message.content
if content and "{" in content:
    try:
        # 尝试从文本中提取并解析 JSON
        start_idx = content.find("{")
        end_idx = content.rfind("}") + 1
        tool_data = json.loads(content[start_idx:end_idx])
        print("手动解析工具调用成功:", tool_data)
    except Exception as e:
        print("解析失败:", e)
```

 