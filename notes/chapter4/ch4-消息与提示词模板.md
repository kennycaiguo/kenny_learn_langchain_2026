# 1.认识消息

![image-20260909154511519](./消息与提示词模板.assets/image-20260909154511519.png)

## 1.1消息的内部结构

![image-20260909154729616](./消息与提示词模板.assets/image-20260909154729616.png)

## 1.2消息的类型

![image-20260909155440750](./消息与提示词模板.assets/image-20260909155440750.png)

### 为什么使用不同的消息类型？

![image-20260909155655931](./消息与提示词模板.assets/image-20260909155655931.png)

## 1.3消息格式

### 1》JSON格式

![image-20260909155929376](./消息与提示词模板.assets/image-20260909155929376.png)

### 2》类的对象格式

![image-20260909160031605](./消息与提示词模板.assets/image-20260909160031605.png)

![image-20260909160255626](./消息与提示词模板.assets/image-20260909160255626.png)

![image-20260909160329488](./消息与提示词模板.assets/image-20260909160329488.png)

## 1.4案例

### JSON格式的消息列表


```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
gemini_api_key = os.getenv("gemini_api_key")

llm = ChatOpenAI(
    model="gemini-3.1-flash-lite",
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

resp = llm.invoke([{"role":"user","content":"香港有多少人口"}])
print(resp.text)
```

### 模型输出

    根据香港政府统计处最新的数据，截至 **2023年年中**，香港的临时人口数字约为 **749.81万人**。
    
    以下是一些关键信息供参考：
    
    1.  **趋势：** 经过连续几年的下跌后，香港人口在2023年出现回升。这主要得益于疫情后人口流动恢复正常，许多香港居民返回香港，以及部分人才引进计划（如“高才通”等）带来的非本地居民流入。
    2.  **构成：** 该总数包括常住居民和流动居民。
    3.  **预测：** 根据政府的推算，由于人口老龄化和低生育率，香港未来的人口结构将持续面临挑战，劳动力人口预计会进一步缩减。
    
    **建议：** 如果你需要最实时的精确数据，可以访问[香港政府统计处官方网站](https://www.censtatd.gov.hk/)查询最新的《香港人口数字》报告。

### 消息对象列表


```python
from langchain.messages import HumanMessage,AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
gemini_api_key = os.getenv("gemini_api_key")

llm = ChatOpenAI(
    model="gemini-3.1-flash-lite",
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

resp = llm.invoke([HumanMessage("我爱你的法语怎么说")])
resp.pretty_print()
```

### 模型输出

    ==================================[1m Ai Message [0m==================================
    
    法语中表达“我爱你”最标准、最常用的说法是：
    
    **Je t'aime.**
    
    *   **发音提示：**
        *   **Je** (发音类似“惹”，但舌头不用卷，发音短促)
        *   **t'aime** (t'的发音类似“得”，aime的发音类似“爱姆”)
        *   连起来读：**惹-带姆** (Je t'aime)
    
    ---
    
    **其他相关的表达方式：**
    
    1.  **Je t'aime beaucoup.**
        *   字面意思是“我很爱你”，但在法语中，这通常表示“我很喜欢你”（多用于朋友或家人之间，或者作为委婉的表白，比单纯的 Je t'aime 程度要轻）。
    2.  **Je t'adore.**
        *   意为“我崇拜你/我非常喜欢你”。
    3.  **Je suis amoureux / amoureuse de toi.**
        *   意为“我爱上了你”。（如果你是男性说这句话，用 amoureux；如果你是女性，用 amoureuse）。
    
    **最浪漫的用法：** 如果你想表达“我深深地爱着你”，可以说 **"Je t'aime passionnément."**

## 1.5消息对象字段说明

### SystemMessage和HumanMessage参数列表

![image-20260909162845475](./消息与提示词模板.assets/image-20260909162845475.png)

### 举例，带有元数据字段的消息

![image-20260909163541456](./消息与提示词模板.assets/image-20260909163541456.png)

### AIMessage参数列表

![image-20260909202256326](./消息与提示词模板.assets/image-20260909202256326.png)

![image-20260909202530285](./消息与提示词模板.assets/image-20260909202530285.png)

![image-20260909205632278](./消息与提示词模板.assets/image-20260909205632278.png)

#### 返回的内容分析

![image-20260911105005940](./消息与提示词模板.assets/image-20260911105005940.png)

### ToolMessage参数列表

![image-20260911105148630](./消息与提示词模板.assets/image-20260911105148630.png)





### 演练，看看gpt-oss-120b大模型是否支持name元数据，答案是不支持

```
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage


llm = init_chat_model(
    model="openai/gpt-oss-120b",  # 指定具体的 Groq 模型名称
    model_provider="groq",    # 明确指定提供商为 groq
    temperature=0.7
)

# 调用模型
messages = [
  SystemMessage("""你是一个消息抽取器。你会收到来自不同发言者的user消息。每条消息可能带有name字段。
   你的任务是：严格根据每条消息的name提取发言者及其观点，并输出JSON。禁止使用”第一人称/第二人称“这种称呼。
   若某条消息没有name，则输出unknown。输出格式：{\"speakers\":[{\"name\":\"...\",\"claim\":\"}]}"""),
  HumanMessage(
       content="我认为日本的首都是大阪",
       name="Bob"
  ),
  HumanMessage(
      content="我认为日本的首都是东京",
      name="Mary"
  ),
  HumanMessage(
      content="请列出谁说了什么，不要判断对错",
      name="audience"
  )
]

response = llm.invoke(messages)

# 打印输出结果
response.pretty_print()
```



### 模型输出

![image-20260909165757229](./消息与提示词模板.assets/image-20260909165757229.png)

### 演练2.来看看Gemini

```
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,SystemMessage
import os

load_dotenv(override=True)
gemini_api_key = os.getenv("gemini_api_key")

llm = ChatOpenAI(
    model="gemini-3.1-flash-lite",
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

messages = [
  SystemMessage("""你是一个消息抽取器。你会收到来自不同发言者的user消息。每条消息可能带有name字段。
   你的任务是：严格根据每条消息的name提取发言者及其观点，并输出JSON。禁止使用”第一人称/第二人称“这种称呼。
   若某条消息没有name，则输出unknown。输出格式：{\"speakers\":[{\"name\":\"...\",\"claim\":\"}]}"""),
  HumanMessage(
       content="我认为日本的首都是大阪",
       name="Bob"
  ),
  HumanMessage(
      content="我认为日本的首都是东京",
      name="Mary"
  ),
  HumanMessage(
      content="请列出谁说了什么，不要判断对错",
      name="audience"
  )
]

resp = llm.invoke(messages)
resp.pretty_print()
```



### 模型输出：

![image-20260909170335472](./消息与提示词模板.assets/image-20260909170335472.png)

### 演练3.ToolMessage的使用1,字典列表格式参数

```
from langchain_ollama import ChatOllama
import rich

llm = ChatOllama(
    model='gemma4:latest'
)

def get_weather(city:str):
    return "~不错哟~~"

t_model = llm.bind_tools([get_weather])

ai_msg = {
    "role":"assistant",
    "content":" ",
    "tool_calls":[{
        "name":"get_weather",
        "args":{"location":"北京"},
        "id":"call_00_nUD2NC9QRN5Cg1GaoIkBJQ4s"
    }]
}

tool_msg = {
    "role":"tool",
    "content":"北京今天天气晴朗，万里无云",
    "tool_call_id":"call_00_nUD2NC9QRN5Cg1GaoIkBJQ4s"
}
messages = [
    {"role":"user","content":"北京天气如何"},
    ai_msg,
    tool_msg
]

# result = t_model.invoke(
#     messages
# )
result = llm.invoke(
    messages
)

rich.print(result)
```



### 模型输出

![image-20260911131133418](./消息与提示词模板.assets/image-20260911131133418.png)

### 演练4.ToolMessage的使用，对象列表参数格式

```
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage,HumanMessage,ToolMessage
import rich

llm = ChatOllama(
    model='gemma4:latest'
)

def get_weather(city:str):
    return "~不错哟~~"

t_model = llm.bind_tools([get_weather])


ai_msg = AIMessage(
    content=" ",
    tool_calls=[{
            "name":"get_weather",
            "args":{"location":"北京"},
            "id":"call_00_nUD2NC9QRN5Cg1GaoIkBJQ4s"
        }]
    )

tool_msg = ToolMessage(
    content="北京今天天气晴朗，万里无云",
    tool_call_id="call_00_nUD2NC9QRN5Cg1GaoIkBJQ4s"
    )

messages = [
    HumanMessage(content="北京天气如何"),
    {"role":"user","content":"北京天气如何"},
    ai_msg,
    tool_msg
]

# result = t_model.invoke(
#     messages
# )
result = llm.invoke(
    messages
)

rich.print(result)
```



### 模型输出

![image-20260911131227240](./消息与提示词模板.assets/image-20260911131227240.png)

## 1.6实战

### 1.6.1.对话历史管理

![image-20260911133448461](./消息与提示词模板.assets/image-20260911133448461.png)

![image-20260911135845389](./消息与提示词模板.assets/image-20260911135845389.png)

### 演练1，

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='granite3.2:8b'
)

msg=[
        {"role":"system","content":"你是一位非常友好的AI助手"},
        {"role":"user","content":"你好，我叫Kenny"},
]

result1 = llm.invoke(msg)
print(result1.content)
# 添加记忆
msg.append({"role":"assistant","content":result1.content})
msg.append({"role":"user","content":"我叫什么名字？"})
result2 = llm.invoke(msg)
print(result2.content)
```



### 模型回复

![image-20260911140054030](./消息与提示词模板.assets/image-20260911140054030.png)

### 演练2，

```
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='granite3.2:8b'
)

msg=[
        {"role":"system","content":"你是一位非常友好的AI助手"},
        {"role":"user","content":"你好，我叫Kenny"},
]

result1 = llm.invoke(msg)
print(result1.content)
# 添加记忆
msg.append({"role":"assistant","content":result1.content})
msg.append({"role":"user","content":"我叫什么名字？"})
result2 = llm.invoke(msg)
msg.append({"role":"assistant","content":result2.content})
msg.append({"role":"user","content":"Jackline is a nice girl,she has 20 years old,her email is : jackline1234@gmail.com"})
msg.append({"role":"user","content":"Jackline是男还是女?"})
result3 = llm.invoke(msg)
result3.pretty_print()
```



### 模型输出

![image-20260911140153468](./消息与提示词模板.assets/image-20260911140153468.png)

### 1.6.2.对话历史优化

![image-20260911140300093](./消息与提示词模板.assets/image-20260911140300093.png)

![image-20260911140808917](./消息与提示词模板.assets/image-20260911140808917.png)

### 1.6.3.多轮对话聊天机器人

#### 示例代码如下,能够一直聊下去，直到用户输入的提示词是quit就会退出，我们使用本地大模型，否则可能会消耗非常多的token，很快就所有的在线模型都用不了。

```
from langchain_ollama import ChatOllama

# 1.基础配置
# MODEL_NAME='gemma4:latest'
MODEL_NAME='qwen2.5vl:latest'
MAX_PAIR_HISTORY = 10
EXIT_WORD = "quit"

# 2.初始化本地大模型对象
model = ChatOllama(
    model=MODEL_NAME
)

# 3.维护一个消息列表
messages = [
    {"role":"system","content":"你叫小美，是一个非常友好的人工智能客服，你回答问题都是非常简明扼要，直奔重点的。"}
]

# 4.用循环来交互
i = 1 #记录对话的轮数
print(f"交互对话开始，请输入提示词(也就是你的问题),输入{EXIT_WORD}结束对话")
while True:
    print(f"\n{'*'*10}第{i}轮交互对话开始{'*'*10}\n")
    prompt = input("提示词：>>>")
    print(f"你的问题是：{prompt}")
    if prompt == EXIT_WORD:
        print("今天暂时聊到这里，我们下一次再见！")
        break
    messages.append({"role":"user","content":prompt})
    r = model.invoke(messages)
    r.pretty_print()
    messages.append({"role":"assistant","content":r.content})
    i+=1

```



#### 效果

![image-20260911180544118](./消息与提示词模板.assets/image-20260911180544118.png)

#### 代码优化，如果把每一次的模型输出都添加到消息列表中，列表就会非常大，相互非常多的内存和token，我们定义一个函数来保留最近几次的聊天信息，这样子效果就会好很多

```
def keep_recent_messages(messages,max_pairs=3):
    # 分离system和对话
    sys_msgs = [m for m in messages if m.get("role")=="system"]
    conversation_msgs = [m for m in messages if m.get("role")!="system"]
    # 只保留最佳的
    recent_msgs = conversation_msgs[-(max_pairs*2):] # 对话需要user,assistant,user,assistant,。。。是成对使用的，所以是max_pairs*2

    # 返回：sys_msgs + 最近对话
    return sys_msgs + recent_msgs # 列表+列表=列表
```



#### 然后我们把上面的聊天机器人的代码优化一下

```
from langchain_ollama import ChatOllama

# 1.基础配置
# MODEL_NAME='gemma4:latest'
MODEL_NAME='qwen2.5vl:latest'
MAX_PAIR_HISTORY = 10
EXIT_WORD = "quit"

# 2.初始化本地大模型对象
model = ChatOllama(
    model=MODEL_NAME
)

# 3.维护一个消息列表
messages = [
    {"role":"system","content":"你叫小美，是一个非常友好的人工智能客服，你回答问题都是非常简明扼要，直奔重点的。"}
]

# 4.用循环来交互
i = 1 #记录对话的轮数
print(f"交互对话开始，请输入提示词(也就是你的问题),输入{EXIT_WORD}结束对话")
while True:
    print(f"\n{'*'*10}第{i}轮交互对话开始{'*'*10}\n")
    prompt = input("提示词：>>>")
    # 判断一下提示词是否是退出，如果是就退出
    if prompt == EXIT_WORD:
        print("今天暂时聊到这里，我们下一次再见！")
        break
    # 如果不是，就输出提示词。
    print(f"你：{prompt}")
    messages.append({"role":"user","content":prompt})
    # 在调用模型的时候，需要选取最近n次的消息
    messages1 = keep_recent_messages(messages,max_pairs=MAX_PAIR_HISTORY)
    r = model.invoke(messages1)
    r.pretty_print()
    messages.append({"role":"assistant","content":r.content}) # 但是我们必须保存一个完整的消息列表。
    print(f"\n{'*'*10}第{i}轮交互对话结束{'*'*10}\n")
    i +=1

```



#### 模型输出

![image-20260911194349227](./消息与提示词模板.assets/image-20260911194349227.png)

## 1.7拓展：消息属性content,content_blocks

### 1.7.1 content

![image-20260914130429704](./消息与提示词模板.assets/image-20260914130429704.png)

#### 举例1

![image-20260914130506574](./消息与提示词模板.assets/image-20260914130506574.png)

#### 举例2

![image-20260914130536125](./消息与提示词模板.assets/image-20260914130536125.png)

##### 案例2代码，我们可以把一幅图片转化为data uri字符串格式，然后把他作为image_url传递给模型，如果是支持视觉的模型，就可以识别出来

![image-20260914141650796](./消息与提示词模板.assets/image-20260914141650796.png)

##### 先定义一个图片转为data uri的函数

```
def encode_image(img_path,img_type='jpeg'):
    """将一张本地图片转换为Base64编码的Data URI字符串，方便在文本中嵌入图片数据"""
    with open(img_path,"rb") as img_file:
        return f"data:image/{img_type};base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
```



##### 然后是让模型识别图片的代码，注意，需要先运行上面的代码

```
from  langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import base64

model = ChatOllama(
    model="qwen2.5vl:latest"
)

img_path="image_test.png"
# 获取图片的base64编码数据
base64_img = encode_image(img_path)

resp = model.invoke([
   HumanMessage(
     content=[
        {"type":"text","text":"这张图片里面有什么？"},
        {"type":"image_url","image_url":base64_img}
     ]
   )
])
resp.pretty_print()
```



##### 模型输出

![image-20260914141710893](./消息与提示词模板.assets/image-20260914141710893.png)

##### 我们可以创建一个函数，读取网上一幅图片的数据，然后把它转化为base64编码的data uri在传递给模型，模型一样可以识别出来

我们的测试图片是（url: https://img.iplaysoft.com/wp-content/uploads/2019/free-images/free_stock_photo_2x.jpg!0x0.webp）： 

![image-20260914145147276](./消息与提示词模板.assets/image-20260914145147276.png)

##### encode_image_from_web函数的代码如下,需要安装pillow，pip install pillow

```
def encode_image_from_web(imgurl,img_type='jpeg'):
    import requests
    from PIL import Image

    # 2. 发送请求获取图片内容
    response = requests.get(imgurl)

    # 3. 检查请求是否成功
    if response.status_code == 200:
         return f"data:image/{img_type};base64,{base64.b64encode(response.content).decode('utf-8')}"
```

##### 然后我们修改一下代码如下

```
from  langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import base64

model = ChatOllama(
    model="qwen2.5vl:latest"
)

# 识别本地图片
# img_path="image_test.png"
# img_path="pussy.jpg"
# # 获取图片的base64编码数据
# base64_img = encode_image(img_path)
# 识别网络图片
imgurl = "https://img.iplaysoft.com/wp-content/uploads/2019/free-images/free_stock_photo_2x.jpg!0x0.webp"
base64_web_img = encode_image_from_web(imgurl)

resp = model.invoke([
   HumanMessage(
     content=[
        {"type":"text","text":"这张图片里面有什么？"},
        {"type":"image_url","image_url":base64_web_img}
     ]
   )
])
resp.pretty_print()
```



##### 运行程序，分析模型把图片的内容识别出来了

![image-20260914145312393](./消息与提示词模板.assets/image-20260914145312393.png)

#### 太棒了，我们的程序可以识别网络和本地图片！！！

### 1.7.2 content_block，在使用在消息类里面，如HumanMessage,SystemMessage等等，在消息字典列表里面是不支持的。

#### 什么是content_block以及输入的格式化

![image-20260914150057861](./消息与提示词模板.assets/image-20260914150057861.png)

#### 举例1，注意这个教程老师的content_blocks的字段不正确。还是使用上面的自定义函数来加载图片

```
from  langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import base64

model = ChatOllama(
    model="qwen2.5vl:latest"
)

# 识别本地图片
# img_path="image_test.png"
# img_path="pussy.jpg"
# # 获取图片的base64编码数据
# base64_img = encode_image(img_path)
# 识别网络图片
# imgurl = "https://img.iplaysoft.com/wp-content/uploads/2019/free-images/free_stock_photo_2x.jpg!0x0.webp"
imgurl = "https://m.media-amazon.com/images/I/917DlMVdioL._AC_SL1500_.jpg"

base64_web_img = encode_image_from_web(imgurl)

resp = model.invoke([
   HumanMessage(
     content_blocks=[
        {"type":"text","text":"这张图片里面有什么？"},
        # {"type":"image_url","image_url":base64_img,'mime_type':"image/jpg"},
        {"type":"image_url","image_url":base64_web_img,'mime_type':"image/jpg"},
     ]
   )
])
resp.pretty_print()
```



#### 也可以使用ChatOpenAI类来加载本地模型，做一样的事情

```
from langchain_openai import ChatOpenAI

# 构造 ChatOpenAI 实例连接本地大模型
model = ChatOpenAI(
    model="qwen2.5vl:latest",                  # 替换为你本地实际的模型名称
    base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
    api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
    temperature=0.7
)

# 识别本地图片
# img_path="image_test.png"
# img_path="pussy.jpg"
# # 获取图片的base64编码数据
# base64_img = encode_image(img_path)
# 识别网络图片
# imgurl = "https://img.iplaysoft.com/wp-content/uploads/2019/free-images/free_stock_photo_2x.jpg!0x0.webp"
imgurl = "https://m.media-amazon.com/images/I/917DlMVdioL._AC_SL1500_.jpg"

base64_web_img = encode_image_from_web(imgurl)

response =model.invoke([
   HumanMessage(
     content_blocks=[
        {"type":"text","text":"这张图片里面有什么？"},
        {"type":"image_url","image_url":base64_img,'mime_type':"image/jpg"}, # 网上教程老师的字段是错误的。
     ]
   )
])

response.pretty_print()
```



#### 模型输出

![image-20260914163719080](./消息与提示词模板.assets/image-20260914163719080.png)

#### 输出格式化

![image-20260914165323942](./消息与提示词模板.assets/image-20260914165323942.png)

![image-20260914165430640](./消息与提示词模板.assets/image-20260914165430640.png)

# 2.提示词模板

## 2.1.ChatPromptTemplate的2种实例化和3种调用方式

### 1.为什么推荐提示词模板？

![image-20260914193209553](./消息与提示词模板.assets/image-20260914193209553.png)

#### 举例1，使用字符串拼接

![image-20260914193304516](./消息与提示词模板.assets/image-20260914193304516.png)

![image-20260914193526916](./消息与提示词模板.assets/image-20260914193526916.png)

#### 举例2.提示词模板

![image-20260914194003316](./消息与提示词模板.assets/image-20260914194003316.png)

![image-20260914194104642](./消息与提示词模板.assets/image-20260914194104642.png)

![image-20260914194223623](./消息与提示词模板.assets/image-20260914194223623.png)

### 2.提示词机制演进

#### 旧时代：llm+PromptTemplate,现在已经不使用了。

#### ![image-20260914194710837](./消息与提示词模板.assets/image-20260914194710837.png)

#### 新时代：ChatModel+ChatPromptTemplate

![image-20260914195012885](./消息与提示词模板.assets/image-20260914195012885.png)

#### 两者对比

![image-20260914195125834](./消息与提示词模板.assets/image-20260914195125834.png)



###  3.ChatPromptTemplate的使用

![image-20260915124353484](./消息与提示词模板.assets/image-20260915124353484.png)

### 3.1两种实例化方式

![image-20260915124622134](./消息与提示词模板.assets/image-20260915124622134.png)

#### 1》使用from_message(),这是我们推荐的方式

#### 简单示例

```
from langchain_core.prompts import ChatPromptTemplate

# 实例化提示模板
tmp = ChatPromptTemplate.from_messages([
  ("system","你是一个非常友好的Ai助手,你的名字叫{name}"),
  ("user","你好，最近怎么样？"),
  ("ai","我很好，谢谢"),
  ("human","{user_input}")
])

# 调用提示模板
res = tmp.invoke({"name":"Jessica","user_input":"女人比男人长寿吗?"})
print(res)
```



#### 程序输出

![image-20260915131553527](./消息与提示词模板.assets/image-20260915131553527.png)

#### 2》使用实例初始化方式

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板
tmp = ChatPromptTemplate([
  ("system","你是一个非常友好的Ai助手,你的名字叫{name}"),
  ("user","你好，最近怎么样？"),
  ("ai","我很好，谢谢"),
  ("human","{user_input}")
])

# 调用提示模板
res = tmp.invoke({"name":"Jessica","user_input":"女人比男人长寿吗?"})
print(res)
```



#### 程序输出

![image-20260915134725502](./消息与提示词模板.assets/image-20260915134725502.png)

### 3.2模板调用的三种方式

#### 方式1.invoke

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板
tmp = ChatPromptTemplate([
  ("system","你是一个非常友好的Ai助手,你的名字叫{name}"),
  ("user","你好，最近怎么样？"),
  ("ai","我很好，谢谢"),
  ("human","{user_input}")
])

# 调用提示模板
res = tmp.invoke({"name":"Jessica","user_input":"猫的能活多少年?"})
print(res)
```



#### 这个方法返回的是一个PromptValue对象，传递给模型需要使用它的to_messages()方法来得到一个消息列表

![image-20260915144447475](./消息与提示词模板.assets/image-20260915144447475.png)

![image-20260915144611855](./消息与提示词模板.assets/image-20260915144611855.png)

#### 其实PromptValue是可以直接传递给模型的invoke方法的

![image-20260915150921994](./消息与提示词模板.assets/image-20260915150921994.png)

#### 方式2.format

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板
tmp = ChatPromptTemplate.from_messages([
  ("system","你是一个非常友好的Ai助手,你的名字叫{name}"),
  ("user","你好，最近怎么样？"),
  ("ai","我很好，谢谢"),
  ("human","{user_input}")
])

# 调用提示模板
prompt_str = tmp.format(name="小明",user_input="牛的能活多少年?") # 返回的是字符串
print(res)
```



#### 这个format方法返回的是一个字符串，传递给模型的invoke方法时，需要放在一个[]里面

![image-20260915145100351](./消息与提示词模板.assets/image-20260915145100351.png)

##### 使用示例

![image-20260915145521452](./消息与提示词模板.assets/image-20260915145521452.png)

#### 其实字符串也是可以直接使用的

![image-20260915151608155](./消息与提示词模板.assets/image-20260915151608155.png)

#### 方式3.format_message

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板
tmp = ChatPromptTemplate.from_messages([
  ("system","你是一个非常友好的Ai助手,你的名字叫{name}"),
  ("user","你好，最近怎么样？"),
  ("ai","我很好，谢谢"),
  ("human","{user_input}")
])

# 调用提示模板
str_list = tmp.format_messages(name="金元宝",user_input="狗的能活多少年?") # 返回的是字符串
print(str_list)
```



#### 这个方法返回一个字符串列表，可以直接提供给模型的invoke方法

![image-20260915150556934](./消息与提示词模板.assets/image-20260915150556934.png)

## 2.2 ChatPromptTemplate初始化的6种参数类型

### 更丰富的初始化参数类型

![image-20260915152313125](./消息与提示词模板.assets/image-20260915152313125.png)

#### 类型1：字符串列表类型

```
from click import format_filename
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 字符串列表
tmp = ChatPromptTemplate([ 
    "你好，我是{name}"    
])

prompt = tmp.format(name="Kenny")

model = ChatOpenAI(
    model="gemma4:latest",
    base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
    api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
    temperature=0.1,
)

resp = model.invoke(prompt)
resp.pretty_print()
```



#### 类型2：元组列表类型

```
from click import format_filename
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 字符串列表
tmp = ChatPromptTemplate([ 
    ("user","{user_input}")   
])

prompt = tmp.format(user_input="世界7大奇迹是什么")

model = ChatOpenAI(
    model="gemma4:latest",
    base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
    api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
    temperature=0.1,
)

resp = model.invoke(prompt)
resp.pretty_print()
```



#### 类型3：字典列表类型

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板
tmp = ChatPromptTemplate.from_messages([
  {"role":"system","content":"你是一个非常友好的Ai助手,你的名字叫{name}"},
  {"role":"user","content":"{user_input}"}
])

# 调用提示模板
str_list = tmp.format_messages(name="金元宝",user_input="2的20次方是多少?") # 返回的是字符串
# print(str_list)
model = ChatOpenAI(
        model="gemma4:latest",                  # 替换为你本地实际的模型名称
        base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
        api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
        temperature=0.1,
)

resp = model.invoke(str_list) # 这个prompt_str是一个字符串，必须放在[]里面
resp.pretty_print()
```



#### 类型4：Message对象列表类型

```
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板
tmp = ChatPromptTemplate.from_messages([
  SystemMessage(content="你是一个非常友好的Ai助手,你的名字叫小智"), # 构造消息对象的时候，不能够使用{}，英文模板识别不出来
  HumanMessage(content="中国那个省的gdp最高？")
])

# 调用提示模板
str_list = tmp.invoke({}) # 返回的是字符串
# print(str_list)
model = ChatOpenAI(
        model="gemma4:latest",                  # 替换为你本地实际的模型名称
        base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
        api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
        temperature=0.1,
)

resp = model.invoke(str_list) # 这个prompt_str是一个字符串，必须放在[]里面
resp.pretty_print()
```



#### 类型5：MessagePromptTemplate列表类型

```
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI


# 实例化提示模板
sys_tmp = SystemMessagePromptTemplate.from_template("你是一个非常友好的Ai助手,你的名字叫{name}")
user_tmp = HumanMessagePromptTemplate.from_template("{user_input}")

tmp = ChatPromptTemplate.from_messages([
      sys_tmp,user_tmp
])


# 调用提示模板
str_list = tmp.invoke({"name":"小谷","user_input":"中国的国菜是什么？"}) # 返回的是字符串
# print(str_list)
model = ChatOpenAI(
        model="gemma4:latest",                  # 替换为你本地实际的模型名称
        base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
        api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
        temperature=0.1,
)

resp = model.invoke(str_list) # 这个prompt_str是一个字符串，必须放在[]里面
resp.pretty_print()
```



#### 类型6：BaseChatPromptTemplate列表类型

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 实例化提示模板,这里使用ChatPromptTemplate模板嵌套的方法
tmp1 = ChatPromptTemplate.from_messages([("system","你是一个非常友好的Ai助手,你的名字叫{name}")])
tmp2 = ChatPromptTemplate.from_messages([("user","{user_input}")])
tmp = ChatPromptTemplate.from_messages([
 tmp1,tmp2
])

# 调用提示模板
str_list = tmp.format_messages(name="金元宝",user_input="怎么称呼你孙子的孙子？") # 返回的是字符串
# print(str_list)
model = ChatOpenAI(
        model="gemma4:latest",                  # 替换为你本地实际的模型名称
        base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
        api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
        temperature=0.1,
)

resp = model.invoke(str_list) 
resp.pretty_print()
```



#### 注意，上面这些参数可以混合使用，也就是在一个ChatPromptTemplate的构造函数里面同时使用不同类型的参数。

![image-20260915175509104](./消息与提示词模板.assets/image-20260915175509104.png)

### 高级特性

#### 1>部分变量预填充

![image-20260915180535118](./消息与提示词模板.assets/image-20260915180535118.png)

##### 实例代码

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 字符串列表
tmp = ChatPromptTemplate([ 
    ("system","你是{role},目标用户是{audience}"),
    ("user","{task}")   
])

cust_tmp = tmp.partial(role="导游",audience="游客") # 注意，进行变量的部分填充后，需要用一个变量接收返回值，否则报错
prompt = cust_tmp.invoke({"task":"请介绍一下肇庆七星岩"})

model = ChatOpenAI(
    model="gemma4:latest",
    base_url="http://localhost:11434/v1",  # 本地 OpenAI 兼容接口地址
    api_key="ollama",                 # 本地调用无需真实 Key，但参数不可为空
    temperature=0.1,
)

resp = model.invoke(prompt)
resp.pretty_print()
```



##### 模型输出：

![image-20260916112533591](./消息与提示词模板.assets/image-20260916112533591.png)

#### 2>消息占位符

![image-20260916144702136](./消息与提示词模板.assets/image-20260916144702136.png)

##### 2.1>JSON形式

![image-20260916144802956](./消息与提示词模板.assets/image-20260916144802956.png)

###### 实例代码

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

tmp = ChatPromptTemplate([
    ("system","你是一个优秀的AI助手"),
    ("placeholder","{conversation}")
])

prompt = tmp.invoke({ # 这个整体是一个json格式，key是conversation，value就是一个元组列表
    "conversation":[
       ("human","嗨，你好"),
       ("ai","你好，有什么可以帮助你的？"),
       ("human","能给我做一顿饭吗"),
       ("ai","对不起，我没有那个能力"),
       ("human","中国有多少个直辖市？")
    ]
})

model = ChatOpenAI(
    model="gemma4:latest",
    base_url="http://localhost:11434/v1",
    api_key="sk123456",
    temperature=0.1
)

resp = model.invoke(prompt)
```



##### 2.2>MessagePlaceHolder示例

```
from langchain.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

tmp = ChatPromptTemplate([
    ("system","你是一个优秀的AI助手"),
    MessagesPlaceholder(variable_name="conversation")
])

# prompt = tmp.invoke({
#     "conversation":[
#        ("human","嗨，你好"),
#        ("ai","你好，有什么可以帮助你的？"),
#        ("human","能给我做一顿饭吗"),
#        ("ai","对不起，我没有那个能力"),
#        ("human","中国首富是谁？")
#     ]
# })

#换一种写法
prompt = tmp.invoke({
    "conversation":[
        HumanMessage("嗨，你好"),
        AIMessage("你好，有什么可以帮助你的？"),
        HumanMessage("能给我包饺子吗"),
        AIMessage("对不起，我没有那个能力"),
        HumanMessage("中国有哪些知名的古镇？")
    ]
})

model = ChatOpenAI(
    model="gemma4:latest",
    base_url="http://localhost:11434/v1",
    api_key="sk123456",
    temperature=0.1
)

resp = model.invoke(prompt)
resp.pretty_print()
```

###### 存储历史记录

![image-20260916152338953](./消息与提示词模板.assets/image-20260916152338953.png)

###### 实例代码

```
from langchain.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

tmp = ChatPromptTemplate([
    ("system","你是一个优秀的AI助手"),
    MessagesPlaceholder(variable_name="history"),
    ("human","{question}")
])

prompt = tmp.invoke({
    "history":[
       ("human","5+3=?"),
       ("ai","8"),
    ],
    "question":"结果再除以0.5呢？"
})


model = ChatOpenAI(
    model="gemma4:latest",
    base_url="http://localhost:11434/v1",
    api_key="sk123456",
    temperature=0.1
)

resp = model.invoke(prompt)
resp.pretty_print()
```



###### 模型输出

![image-20260916161855596](./消息与提示词模板.assets/image-20260916161855596.png)

#### 3>可复用模板库

![image-20260916162446276](./消息与提示词模板.assets/image-20260916162446276.png)

##### 我们创建一个reusable_template.py,内容如下

```
from langchain_core.prompts import ChatPromptTemplate

class ReusablePromptTemplate:
    """可复用提示模板"""
    TRANSLATOR = ChatPromptTemplate([
        ("system","你是专业翻译，精通{src_lang}和{target_lang}"),
        ("user","翻译一下文本\n{text}"),
    ])
    CODE_REVIEWER = ChatPromptTemplate([
        ("system","你是{language}代码审查专家，重点关注{focus}"),
        ("human","审查代码：\n'''{language}\n{code}\n'''"),
    ])
    SUMMARIZOR = ChatPromptTemplate([
        ("system","你是内容摘要专家"),
        ("user","将以下内容总结为{n}个要点{content}"),
    ])
    TUTOR = ChatPromptTemplate([
        ("system","你是{subject}导师，学生水平{level}"),
        ("user","{question}"),
    ])
```

##### 然后我们可以在notebook中编写下面的代码

```
from langchain.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from reusable_template import ReusablePromptTemplate

message = ReusablePromptTemplate.TRANSLATOR.format_messages(src_lang="英文",target_lang="中文",text="Do you have time tonight?")
model = ChatOpenAI(
    model="gemma4:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)

resp = model.invoke(message)
resp.pretty_print()
```



##### 运行程序，模型输出如下

![image-20260916201045011](./消息与提示词模板.assets/image-20260916201045011.png)

##### 当然我们可以进一步细化，用一个py文件来存放一个模板这样子更加好维护

![image-20260916201208167](./消息与提示词模板.assets/image-20260916201208167.png)

#### 4>模板组合

![image-20260916201513833](./消息与提示词模板.assets/image-20260916201513833.png)
