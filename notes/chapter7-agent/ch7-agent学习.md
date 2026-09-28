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

# 2.Agent的基本用法1：模型的传入方式

## 2.1 传入模型字符串

## 2.2 传入模型对象



# 3.Agent的基本用法2：如何调用Agent



# 4.Agent的基本用法3：绑定工具

## 4.1 基本用法：

### 举例1：绑定一个工具

### 举例2：接入内置工具

### 举例3：绑定多个工具

## 4.2工具调用流程分析

## 4.3 重试机制

## 4.4 常见问题



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























