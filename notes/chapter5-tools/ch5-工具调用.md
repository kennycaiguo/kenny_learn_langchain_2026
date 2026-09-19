# 1.工具的概述

## 1.1工具的重要性

![image-20260917133241243](./ch5-工具调用.assets/image-20260917133241243.png)

### 举例

![image-20260917140916252](./ch5-工具调用.assets/image-20260917140916252.png)

### 思考：智能体和大模型有什么区别？

大模型一般只能够输出文本，不能直接调用工具，也没有记忆功能，不会做然后行动。智能体是在大模型的基础上打造的，能够调用工具，有记忆功能，能够做决策。虽然大模型是智能体的大脑，但是仅仅靠大模型，很多事情还是做不了的。

## 1.2工具调用的方式

![image-20260917141308126](./ch5-工具调用.assets/image-20260917141308126.png)

### 1.2.1 直接调用

![image-20260917145125649](./ch5-工具调用.assets/image-20260917145125649.png)

### 1.2.2 基于模型进行调用，注意：qwen2.5vl:latest模型不支持工具调用，**qwen3-vl:latest可以使用工具**

![image-20260917150213205](./ch5-工具调用.assets/image-20260917150213205.png)

### 需要注意，模型知道要调用一个工具，但是它自己不能够直接调用工具，需要我们的程序来调用工具。

## 1.3工具调用的整体流程

![image-20260917151404344](./ch5-工具调用.assets/image-20260917151404344.png)

![image-20260917201142342](./ch5-工具调用.assets/image-20260917201142342.png)

## 1.4从message流转看工具的调用

### 我们有一个weather_tool.py模块，里面有一个query_weather方法

```
import os
from langchain_openai import ChatOpenAI
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def query_weather(city="beijing", units="metric", language="zh_cn"):
     appid = os.getenv("OpenWeather_APi_key")
     # 构建请求URL
     url = "https://api.openweathermap.org/data/2.5/weather"
     # 设置查询参数
     params = {
         "q": city,                 # 查询的城市，默认为北京
         "appid": appid,          # API密钥
         "units": units,            # 测量单位，默认为摄氏度
         "lang": language           # 输出语言，默认为简体中文
     }
     # 发送GET请求
     response = requests.get(url, params=params)
     # 检查响应状态
     if response.status_code == 200:
         # 解析响应数据
         data = response.json()
        #  # 打印获取到的数据
        #  print(f"查询城市: {city}")
        #  print(f"温度: {data['main']['temp']}°{units[0].upper()}")
        #  print(f"天气描述: {data['weather'][0]['description']}")
        #  print(f"湿度: {data['main']['humidity']}%")
        #  print(f"风速: {data['wind']['speed']} m/s")
         
         return data
     
     else:
         print(f"查询失败，状态码：{response.status_code}")
         print("响应数据：", response.text)
         return {"error":"weather api 调用失败。。。"}

if __name__ == '__main__':
    weather_data = query_weather(city="guangzhou")  
    model = ChatOpenAI(
        model="qwen2.5vl:latest",
        api_key="sk12345",
        base_url="http://localhost:11434/v1",
        temperature=0.1
    )   

    messages = [
        {"role": "system", "content": "这是当前北京市的实时天气数据：%s, 来源于OpenWeather API：https://api.openweathermap.org/data/2.5/weather" %weather_data},
        {"role": "user", "content": "请问：当前北京市的天气如何？"} 
    ]    

    resp = model.invoke(messages)
    resp.pretty_print()
```



### 不使用@tool修饰符

```
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from weather_tool import query_weather

# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   

t_model = model.bind_tools([query_weather])
msgs = [
    # HumanMessage("广州今天天气如何？"),
    HumanMessage("北京今天天气如何？"),
]

resp = t_model.invoke(msgs)
tool_calls = resp.tool_calls

for tool_call in tool_calls:
    if tool_call['name'] == 'query_weather':
        tl_resp = ToolMessage(
            content = query_weather(tool_call),
            tool_call_id=tool_call["id"],
            name = tool_call["name"]
        )
        msgs.append(tl_resp)
print("========================messages===============================")
for msg in msgs:
    msg.pretty_print()
print("========================messages===============================")
final_resp = t_model.invoke(msgs)
print(f"final response:\n{final_resp}")

```



### 模型输出

![image-20260917213030046](./ch5-工具调用.assets/image-20260917213030046.png)

### 使用@tool修饰符

#### 定义我们的工具函数

```
import os
from langchain_openai import ChatOpenAI
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv(override=True)


@tool
def query_weather_func(city="Beijing", units="metric", language="zh_cn"):
     """ 
        获取指定城市的天气信息
        参数：
        city：城市的名称，如"上海"
        api_key: OpenWeather的api key
        返回值：
                    天气信息字符串
     
     """ 
     appid = os.getenv("OpenWeather_APi_key")
     # 构建请求URL
     url = "https://api.openweathermap.org/data/2.5/weather"
     # 设置查询参数
     params = {
         "q": city,                 # 查询的城市，默认为北京
         "appid": appid,          # API密钥
         "units": units,            # 测量单位，默认为摄氏度
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

#### 调用代码

```
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI


# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   

t_model = model.bind_tools([query_weather_func]) # 使用我们上面定义的工具
msgs = [
    HumanMessage("上海今天天气如何？"),
    # HumanMessage("北京今天天气如何？"),
]

resp = t_model.invoke(msgs)
tool_calls = resp.tool_calls

for tool_call in tool_calls:
    if tool_call['name'] == 'query_weather_func':
        tl_resp = ToolMessage(
            content = query_weather_func.invoke(tool_call),
            tool_call_id=tool_call["id"],
            name = tool_call["name"]
        )
        msgs.append(tl_resp)
print("========================messages===============================")
for msg in msgs:
    msg.pretty_print()
print("========================messages===============================")
final_resp = t_model.invoke(msgs)
print(f"final response:\n{final_resp}")
```



#### 不知道为什么，调用老是失败

![image-20260917213405709](./ch5-工具调用.assets/image-20260917213405709.png)

### 为了更好的学习，我有找到了一个api就是Weather API，我已经把key保存到.env文件了。我创建了一个函数query_weather_web,代码如下

```
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

def query_weather_web(city="广州", aqi="no", language="zh_cn"):
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



### 然后我们使用类似的代码用基于模型的方式来调用

```
## 使用Weather API
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from weather_tool import query_weather_web
# 创建模型实例
model = ChatOpenAI(
    model="pdurugyan/qwen3.5-9b-deepseek-v4-flash-Q4_K_M-v_2:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.3
)   

t_model = model.bind_tools([query_weather_web])
msgs = [
    # HumanMessage("广州今天天气如何？"),
    # HumanMessage("北京今天天气如何？"),
    # HumanMessage("How is the weather for beijing?"), # ok
    HumanMessage("How is the weather for guangzhou?"), # ok
]

resp = t_model.invoke(msgs)
tool_calls = resp.tool_calls

for tool_call in tool_calls:
    if tool_call['name'] == 'query_weather_web':
        tl_resp = ToolMessage(
            content = query_weather_web(tool_call["args"].get('city')),
            tool_call_id=tool_call["id"],
            name = tool_call["name"]
        )
        msgs.append(tl_resp)
print("========================messages===============================")
for msg in msgs:
    msg.pretty_print()
print("========================messages===============================")
final_resp = t_model.invoke(msgs)
print(f"final response:\n{final_resp}")
```



#### 模型输出了天气信息

![image-20260918142113764](./ch5-工具调用.assets/image-20260918142113764.png)

### 然后我们用这个api定义一个工具

```
## 使用工具的方式来定义函数
import os
from langchain_openai import ChatOpenAI
import requests
from langchain_core.tools import tool

load_dotenv(override=True)

@tool
def query_weather_web_tool(city="Beijing", aqi="no", language="zh_cn"):
     """ 
             获取指定城市的天气信息
             参数：
             city：城市的名称，如"上海"
             api_key: OpenWeather的api key
             返回值：
                         天气信息字符串
          
    """ 
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

### 然后我们来基于模型来调用这个工具

```
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI


# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   

t_model = model.bind_tools([query_weather_web_tool]) # 使用我们上面定义的工具
msgs = [
    HumanMessage("new york今天天气如何？"),
    # HumanMessage("北京今天天气如何？"),
]

resp = t_model.invoke(msgs)
tool_calls = resp.tool_calls

for tool_call in tool_calls:
    if tool_call['name'] == 'query_weather_web_tool':
        tl_resp = ToolMessage(
            content = query_weather_web_tool.invoke(tool_call),
            tool_call_id=tool_call["id"],
            name = tool_call["name"]
        )
        msgs.append(tl_resp)
print("========================messages===============================")
for msg in msgs:
    msg.pretty_print()
print("========================messages===============================")
final_resp = t_model.invoke(msgs)
print(f"final response:\n{final_resp}")
```

#### 模型输出

![image-20260918152928334](./ch5-工具调用.assets/image-20260918152928334.png)



# 2.工具的调用方式1，不使用@tool

## 2.1模型绑定工具并发送请求



## 2.2工具描述的各部分详解

### 2.2.1了解：convert_to_openai_tool

![image-20260918155721486](./ch5-工具调用.assets/image-20260918155721486.png)

### 举例

![image-20260918160511241](./ch5-工具调用.assets/image-20260918160511241.png)

#### 返回值如图：

![image-20260918160614186](./ch5-工具调用.assets/image-20260918160614186.png)

#### 结果字段说明

![image-20260918160721083](./ch5-工具调用.assets/image-20260918160721083.png)

#### 思考一下，为什么没有使用工具装饰器也能够识别为工具？

![image-20260918161102567](./ch5-工具调用.assets/image-20260918161102567.png)

### 2.2.2 description说明

![image-20260918161205565](./ch5-工具调用.assets/image-20260918161205565.png)

### 2.2.3 参数说明

##### 参考链接： https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules.html#docstring

##### 参考链接2：https://peps.pythonlang.cn/pep-0257/#multi-line-docstrings

![image-20260918161906862](./ch5-工具调用.assets/image-20260918161906862.png)

![image-20260918162357761](./ch5-工具调用.assets/image-20260918162357761.png)

##### 注意：Args上面的空行是必须的，否则没有参数描述信息。下面是docstring的格式参考示例

![image-20260918164035741](./ch5-工具调用.assets/image-20260918164035741.png)

### 2.2.4 参数类型说明

![image-20260918164525907](./ch5-工具调用.assets/image-20260918164525907.png)

### 2.2.5 参数默认值说明

![image-20260918164759198](./ch5-工具调用.assets/image-20260918164759198.png)

# 3.工具的调用方式2，使用@tool装饰器(推荐)



## 3.1自定义工具描述：description

![image-20260918165223853](./ch5-工具调用.assets/image-20260918165223853.png)

### 情况1：仅提供docstring信息

![image-20260918165250740](./ch5-工具调用.assets/image-20260918165250740.png)

![image-20260918181434783](./ch5-工具调用.assets/image-20260918181434783.png)

### 情况2：添加工具描述：description

![image-20260918173035643](./ch5-工具调用.assets/image-20260918173035643.png)

#### 如果你同时使用了description和docstring，description优先级更高

![image-20260918182227478](./ch5-工具调用.assets/image-20260918182227478.png)



### 情况3：解析docstring信息：parse_docstring

![image-20260918182456118](./ch5-工具调用.assets/image-20260918182456118.png)

#### 原理

![image-20260918182628641](./ch5-工具调用.assets/image-20260918182628641.png)

### 注意：开启了解析docstring选项后，如果你的docstring格式不对，就会报错

![image-20260918183639891](./ch5-工具调用.assets/image-20260918183639891.png)

## 3.2 更改工具名称：name_Or_callable



## 3.3 自定义arg_schema



### 3.3.1 方式1：使用Pydantic模型定义



#### 3.3.1.1 pydantic类型的定义



#### 3.3.1.2使用Pydantic定义args_schema



### 3.3.2 方式2：使用Json Schema定义



# 4.工具应用案例

## 4.1案例1：使用args_schema

## 4.1案例2:  撰写docstring

## 4.1案例3:  多工具调用

## 4.1案例4: 多工具调用

# 5.拓展：强制使用工具

## 5.1 tool_choice参数说明

## 5.2 none值举例

## 5.3 auto值举例

## 5.4 required值举例

## 5.5强制调用特定的工具





# 扩展：调用weather api程序天气

## 参考网址： https://zhuanlan.zhihu.com/p/645985593

需要先注册，这里注册的信息如下

user: David

email: restgenwong@gmail.com

pw: name + year

然后获取api key保存到.env文件或者环境变量中



# 扩展2：简单易用的weather api： https://www.visualcrossing.com/



用户：kenny887@gmail.com

pw: name+year(首字母大写)

base url ：https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/

## 扩展3：https://www.weatherapi.com/

用户：kenny887@gmail.com

pw: name+year