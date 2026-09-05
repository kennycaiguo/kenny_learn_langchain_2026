# 模型的调用

![image-20260904144650357](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904144650357.png)

## 1.invoke

### 1.1 invoke说明

![image-20260904145359706](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904145359706.png)

### 1.2.invoke参数说明

### 1.2.1.文本输入

![image-20260904150545687](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904150545687.png)

### 这种方式是我们前面一直在使用的。代码如下

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

question = "分析一下中国的经济现状"

result = llm.invoke(question)
print(result.content)
```



### 模型输出

![image-20260904155341221](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904155341221.png)

### 1.2.2.字典列表，这是最灵活的方式，推荐使用

![image-20260904171818594](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904171818594.png)

![image-20260904172251431](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904172251431.png)

![image-20260904172336391](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904172336391.png)

![image-20260904172825234](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904172825234.png)

### 使用字典列表来调用本地ollama大模型

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

messages=[
        {"role":"system","content":"你是一位专业的数学老师"},
        {"role":"user","content":"什么是斐波拉契数列"},
      
]

result = llm.invoke(messages)
print(result.content)
```



### 模型输出

![image-20260904173816548](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904173816548.png)

### 多轮对话方式

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

messages=[
        {"role":"system","content":"你是一位专业的数学老师"},
        {"role":"user","content":"0是偶数吗"},
        {"role":"assistant","content":"是"},
        {"role":"user","content":"我刚才问了什么问题"},
]

result = llm.invoke(messages)
print(result.content)
```



### 模型输出

![image-20260904180708985](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904180708985.png)

### 模型的失忆问题

![image-20260904181421497](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904181421497.png)

### 实例代码

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

messages1=[
        {"role":"system","content":"你是一位非常友好的AI助手"},
        {"role":"user","content":"你好，我叫Kenny"},
]

result = llm.invoke(messages1)
print(result.content)
messages2=[
        {"role":"user","content":"我叫什么名字？"},
]
result = llm.invoke(messages2)
print(result.content)
```



### 模型输出

![image-20260904181711762](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904181711762.png)

### 解决大模型没有记忆的方法

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

msg=[
        {"role":"system","content":"你是一位非常友好的AI助手"},
        {"role":"user","content":"你好，我叫Kenny"},
]

result1 = llm.invoke(msg)
print(result1.content)
# 添加记忆
msg.append({"role":"assistant","content":result1.content}) #把上一次大模型输出的内容添加到字典列表中
msg.append({"role":"user","content":"我叫什么名字？"})# 把第二轮的用户提问添加到字典列表中
result2 = llm.invoke(msg)
print(result2.content)
```



### 模型输出

![image-20260904185104850](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904185104850.png)

### 1.2.3.信息对象列表的输入，从langchain-core.messages导入SystemMessage，AIMessage和HumanMessage

![image-20260904185358782](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904185358782.png)

### 使用消息对象作为模型输入的案例

```
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

messages=[
        SystemMessage("你是一位专业的数学老师"),
        HumanMessage("什么是齐次矩阵")      
]

result = llm.invoke(messages)
print(result.content)
```



### 模型输出

![image-20260904190855341](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904190855341.png)



### 用消息对象的方式给模型添加记忆功能

```
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='deepseek-r1:8b'
)

msg=[
       SystemMessage("你是一位非常友好的AI助手"),
       HumanMessage("你好，我叫Guo")  
]

result1 = llm.invoke(msg)
print(result1.content)
# 添加记忆
msg.append(AIMessage(content=result1.content))
msg.append(HumanMessage("我叫什么名字？"))
result2 = llm.invoke(msg)
print(result2.content)
```



### 模型输出：

![image-20260904191739129](./2-9测试invoke传递三种不同的参数类型.assets/image-20260904191739129.png)

