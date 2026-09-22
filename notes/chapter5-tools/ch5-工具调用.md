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

![image-20260918183752366](./ch5-工具调用.assets/image-20260918183752366.png)

### 思考，开启了parse_docstring，有设置了description，会发生什么？

![image-20260918184021617](./ch5-工具调用.assets/image-20260918184021617.png)

### 答案是：还是description的优先级高

![image-20260918184157355](./ch5-工具调用.assets/image-20260918184157355.png)

### 注意，在实际开发中，一般不会同时使用docstring和description



## 3.2 更改工具名称：name_Or_callable

![image-20260918184425215](./ch5-工具调用.assets/image-20260918184425215.png)

#### 效果

![image-20260918185543906](./ch5-工具调用.assets/image-20260918185543906.png)

### 工具还可以这么改名字

![image-20260918185718009](./ch5-工具调用.assets/image-20260918185718009.png)

### 给工具改名字是不推荐的

![image-20260918190001891](./ch5-工具调用.assets/image-20260918190001891.png)

## 3.3 自定义arg_schema

### 3.3.1 方式1：使用Pydantic模型定义

![image-20260918192923481](./ch5-工具调用.assets/image-20260918192923481.png)

#### 3.3.1.1 pydantic类型的定义

![image-20260918195325403](./ch5-工具调用.assets/image-20260918195325403.png)

#### 3.3.1.2使用Pydantic定义args_schema

![image-20260918200302829](./ch5-工具调用.assets/image-20260918200302829.png)

#### 还需要添加Field定义

![image-20260918200657340](./ch5-工具调用.assets/image-20260918200657340.png)

#### 还有就是从有限的选项中选择

![image-20260921122209309](./ch5-工具调用.assets/image-20260921122209309.png)

#### 示例代码

```
from typing import Literal

from pydantic import BaseModel,Field
from langchain_core.tools import tool

#定义一个类继承之BaseModel
class WeatherInput(BaseModel):
    city:str = Field(
        description="具体的城市",
        default="北京"
    )
    unit:Literal["celsius","fahrenheit"]

## 定义工具，需要使用@tool装饰器，同时作为工具的函数需要有docstring
@tool(args_schema=WeatherInput)
def get_weather(city,unit): #因为我们在args_schema对应的类已经定义了city的数据类型，所以这里可以不写类型
    """ 查询指定城市天气信息"""

    return f"{city}天气晴朗，万里无云,气温30{unit}"

from rich import print as rprint
from langchain_core.utils.function_calling import convert_to_openai_tool

rprint(convert_to_openai_tool(get_weather))
```



##### 输出效果

![image-20260921123007275](./ch5-工具调用.assets/image-20260921123007275.png)

### 3.3.2 方式2：使用Json Schema定义

![image-20260921123055003](./ch5-工具调用.assets/image-20260921123055003.png)

#### 举例

![image-20260921123248864](./ch5-工具调用.assets/image-20260921123248864.png)

#### 应该传递给arg_schema的只有parameter对应的json字典

![image-20260921123447559](./ch5-工具调用.assets/image-20260921123447559.png)

示例代码

```
from typing import Literal

from pydantic import BaseModel,Field
from langchain_core.tools import tool

param_dict={
            'properties': {
                'city': {'default': '北京', 'description': '具体的城市', 'type': 'string'},
                'unit': {'enum': ['celsius', 'fahrenheit'], 'type': 'string'},
                'include_forecast':{
                    'default':False,
                    'description':'是否包含未来五天的天气预报',
                    'type': 'boolean'
                }
            },
            'required': ['unit','include_forecast'],
            'type': 'object'
        }

## 定义工具，需要使用@tool装饰器，同时作为工具的函数需要有docstring
@tool(args_schema=param_dict)
def get_weather(city,unit): #因为我们在args_schema对应的类已经定义了city的数据类型，所以这里可以不写类型
    """ 查询指定城市天气信息"""

    return f"{city}天气晴朗，万里无云,气温30{unit}"

from rich import print as rprint
from langchain_core.utils.function_calling import convert_to_openai_tool

rprint(convert_to_openai_tool(get_weather))
```

#### 效果

![image-20260921124802283](./ch5-工具调用.assets/image-20260921124802283.png)







# 4.工具应用案例

## 4.1案例1：使用args_schema

![image-20260921125227126](./ch5-工具调用.assets/image-20260921125227126.png)

### 案例1代码

#### 定义工具的代码

```
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from rich import print as rprint
from langchain_core.utils.function_calling import convert_to_openai_tool

class WeatherSchema(BaseModel):
    city:str = Field(
        description="具体的城市",
        default="北京"
    )
    if_forecast:bool = Field(
        description="是否包含明天的天气预报",
        default=False
    )


@tool(description="查询当天的天气，可以包含明天的天气预报",args_schema=WeatherSchema)
def get_weather(city:str,if_forecast:bool):
    res = f"{city}明天天气不错"
    if if_forecast:
        res += f"\n{city}明天有大到暴雨"
    return res    

rprint(convert_to_openai_tool(get_weather))
```

#### 完整代码

```
## 1.初始化模型
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from rich import print as rprint
from langchain_core.utils.function_calling import convert_to_openai_tool

# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   


class WeatherSchema(BaseModel):
    city:str = Field(
        description="具体的城市",
        default="北京"
    )
    if_forecast:bool = Field(
        description="是否包含明天的天气预报",
        default=False
    )


@tool(description="查询当天的天气，可以包含明天的天气预报",args_schema=WeatherSchema)
def get_weather(city:str,if_forecast:bool):
    res = f"{city}明天天气不错"
    if if_forecast:
        res += f"\n{city}明天有大到暴雨"
    return res    

rprint(convert_to_openai_tool(get_weather))

## 1.将工具绑定到模型上
tmodel = model.bind_tools([get_weather])
## 2.创建应该消息列表
msgs = [HumanMessage("广明天的天气任何？明天呢")]
## 3.调用模型
resp = tmodel.invoke(msgs)
## 4.把返回的消息添加到信息列表
msgs.append(resp)
## 5.获取tool_calls列表
tool_calls = resp.tool_calls
for tool_call in tool_calls:
    if tool_call['name'] == 'get_weather':
        # 5.1调用工具
        tmsg = get_weather.invoke(tool_call)
        msgs.append(tmsg)
## 6.把我们获取到的数据提供给模型
resp_final = tmodel.invoke(msgs)
## 7.添加到信息列表
msgs.append(resp_final)
## 8.遍历输出所有信息
for msg in msgs:
    msg.pretty_print()
```



### 模型输出

![image-20260921151717125](./ch5-工具调用.assets/image-20260921151717125.png)

## 4.1案例2:  撰写docstring

![image-20260921151517182](./ch5-工具调用.assets/image-20260921151517182.png)

#### 定义工具的代码

```
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from rich import print as rprint
from langchain_core.utils.function_calling import convert_to_openai_tool

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

rprint(convert_to_openai_tool(get_weather2))
```

#### 案例2完整代码

```
## 1.初始化模型
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from rich import print as rprint
from langchain_core.utils.function_calling import convert_to_openai_tool

   
# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   

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

rprint(convert_to_openai_tool(get_weather2))

## 1.将工具绑定到模型上
tmodel = model.bind_tools([get_weather2])
## 2.创建应该消息列表
msgs = [HumanMessage("佛山天的天气r？明天呢")]
## 3.调用模型
resp = tmodel.invoke(msgs)
## 4.把返回的消息添加到信息列表
msgs.append(resp)
## 5.获取tool_calls列表
tool_calls = resp.tool_calls
for tool_call in tool_calls:
    if tool_call['name'] == 'get_weather2':
        # 5.1调用工具
        tmsg = get_weather2.invoke(tool_call)
        msgs.append(tmsg)
## 6.把我们获取到的数据提供给模型
resp_final = tmodel.invoke(msgs)
## 7.添加到信息列表
msgs.append(resp_final)
## 8.遍历输出所有信息
for msg in msgs:
    msg.pretty_print()
```



## 4.1案例3:  多工具调用

![image-20260921161135042](./ch5-工具调用.assets/image-20260921161135042.png)

### 案例3代码

```
## 定义工具
from langchain_core.tools import tool

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


## 初始化模型
## 1.初始化模型
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI


# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   

## 模型实例在上面的代码中创建了，并且运行了。模型在内存里面
## 绑定工具
tools = [get_stock_price,search_news]
tmodel = model.bind_tools(tools)

msg_list = []
hmsg = HumanMessage(content="苹果公司今天的股价是多少？最近有什么新闻")
# hmsg = HumanMessage(content="比较一下微软公司和苹果公司的股价")
# hmsg = HumanMessage(content="腾讯公司最近有什么新闻")
# hmsg = HumanMessage(content="海水为什么是咸的？")
msg_list.append(hmsg)

## 调用工具，因为工具多于一个需要使用循环
while True:
    res = tmodel.invoke(msg_list)
    msg_list.append(res)

    ## 如果模型不需要调用工具，则直接退出循环
    if not res.tool_calls:
        break
    ## 如果有工具调用，处理工具响应
    for tool_call in res.tool_calls:
        if tool_call["name"] == "get_stock_price":
            stockmsg = get_stock_price.invoke(tool_call)
            print(f"Stcok Result:\n{stockmsg}")
            msg_list.append(stockmsg)
        if tool_call["name"] == "search_news":  
            newmsg = search_news.invoke(tool_call)  
            print(f"New Result:\n{newmsg}")
            msg_list.append(newmsg)

## 遍历消息
for msg in msg_list:
    msg.pretty_print()  
```



### 模型输出

![image-20260921203942525](./ch5-工具调用.assets/image-20260921203942525.png)

## 4.1案例4: 多工具调用

### 案例4代码

```
# 定义工具
## 定义工具
from langchain_core.tools import tool

@tool(parse_docstring=True)
def check_weather(city:str="广州"):
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

# 创建模型
## 1.初始化模型
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI


# 创建模型实例
model = ChatOpenAI(
    model="qwen3-vl:latest",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
    temperature=0.1
)   

## 绑定工具
tools = [check_weather,get_news]

tmodel = model.bind_tools(tools)

msgs = [
    HumanMessage("今天杭州天气如何？今天有什么新闻？别瞎编")
]

resp = tmodel.invoke(msgs)

# 基于模型调用多个工具，这里没有使用循环是因为我们可以肯定后面没有工具调用，如果不肯定，响应使用while循环
msgs.append(resp)
tool_calls = resp.tool_calls
for tool_call in tool_calls:
    if tool_call['name'] == "check_weather":
        check_msg = check_weather.invoke(tool_call)
        print(f"check_weather result:{check_msg}")
        msgs.append(check_msg)
    elif  tool_call['name'] =="get_news":
        news_msg = get_news.invoke(tool_call)  
        print(f"get_news result:{news_msg}") 
        msgs.append(news_msg)
    else:
        raise Exception("不存在的工具")    

final = tmodel.invoke(msgs)
msgs.append(final)    
for msg in msgs:
    msg.pretty_print()
```



### 模型输出

![image-20260921210239428](./ch5-工具调用.assets/image-20260921210239428.png)

### 为了方便编程，我写了一个model_utils.py文件，内容如下

```
def create_qwen3_instance():
    from langchain_openai import ChatOpenAI
    # 创建模型实例
    model = ChatOpenAI(
        model="qwen3-vl:latest",
        api_key="sk12345",
        base_url="http://localhost:11434/v1",
        temperature=0.1
    )    

    return model
```

### 还写了一个tool_utils.py,内容如下，工具也可以从外表导入

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



# 5.拓展：强制使用工具

## 5.1 tool_choice参数说明

![image-20260922142541900](./ch5-工具调用.assets/image-20260922142541900.png)

![image-20260922142622219](./ch5-工具调用.assets/image-20260922142622219.png)

## 5.2 none值举例

### 即使你绑定了工具，只要你添加了tool_choice="none",模型就不会调用工具（既然你不使用工具，那么你绑定它干嘛？）

![image-20260922144449657](./ch5-工具调用.assets/image-20260922144449657.png)

## 5.3 auto值举例，auto是默认值，模型会自己推断该不该使用工具，如果提示词需要使用工具，就会调用工具

![image-20260922151626242](./ch5-工具调用.assets/image-20260922151626242.png)

## 如果你的提示词和工具没有任何关系，模型就不会使用它，即使你绑定了工具。

![image-20260922151911415](./ch5-工具调用.assets/image-20260922151911415.png)

## 5.4 required值举例，强制要求模型使用工具

### 当你把tool_choice上涨位required，如果你的提示词需要使用到工具，模型会调用工具，那是很自然的

![image-20260922153143630](./ch5-工具调用.assets/image-20260922153143630.png)

### 然而，因为你强制要求模型一定要使用工具，即使你的提示词里面没有需要调用工具，模型也会调用工具

![image-20260922153424999](./ch5-工具调用.assets/image-20260922153424999.png)

### 注意：现在有一些模型已经非常聪明，即使你强制它使用工具，它在不需要工具的时候还是不会使用工具

#### 想一想，为什么需要tool_choice这个参数？

`tool_choice` 参数用于**控制和干预大模型在面对注册工具时的选择行为**。

虽然开发者在请求时通过 `tools` 传入了可用的工具列表，但模型默认会根据用户的输入**自主判断**是否需要调用工具。引入 `tool_choice` 参数的核心原因在于满足**精准控制、稳定工作流和规避模型误判**的需求：

核心控制模式

通过设置不同的 `tool_choice` 值，可以对模型的行为进行精细化调整： 

- **`auto`（默认）**：模型自己决定是直接回复文本，还是调用一个或多个工具。
- **`none`**：即使提供了工具列表，也**禁止**模型调用任何工具，强行让模型只生成文本回复。
- **强制特定工具（Specific Tool）**：指定某一个具体的工具名称（如 `get_weather`），强制模型在当前步**必须**调用该工具，哪怕从逻辑上看直接回答也可以。
- **`required` / `any`**：强制模型**至少调用一个**工具，不允许直接返回纯文本回答。 
- 为什么在实际开发中不可或缺？

- **打破模型惰性（避免漏掉调用）**：有时用户的输入比较含糊，或者大模型倾向于用自带的陈旧知识直接回答，导致它“懒得”去调用外部实时搜索或查询工具。使用 `tool_choice` 强行约束后，可以杜绝漏调。

- **构建确定性的工作流（Workflow / Agent）**：在复杂的 Agent 编排中，某一个固定的执行步骤（如第一步必须先检索数据库）容不得半点随机性。通过锁定 `tool_choice`，可以确保流程按照代码预期的那样走完固定环节，防止大模型“自由发挥”把流程带偏。

- **节省 Token 与提升响应速度**：在某些明确知道必须使用特定工具的场景下，直接指定工具可以减少模型在“要不要调用”之间的纠结和不确定性输出。

## 5.5强制调用特定的工具

### 我们还可以给模型绑定一系列的工具，但是规定它只能使用我们指定的工具

![image-20260922154627636](./ch5-工具调用.assets/image-20260922154627636.png)

### 同样，当你规定了模型必须使用你指定的工具，即使你的提示词没有必要用到工具，模型也会调用指定的工具

![image-20260922155045600](./ch5-工具调用.assets/image-20260922155045600.png)

## 注意，required和强制规定使用工具并不是所有模型厂商都支持，Qwen模型就只是支持"none"和"auto"

## 6.工具使用总结

### 1>.工具需要清晰的描述

![image-20260922155553225](./ch5-工具调用.assets/image-20260922155553225.png)

### 2> 工具的功能尽可能的单一，不要在一个工具里面做很多事情

![image-20260922155648270](./ch5-工具调用.assets/image-20260922155648270.png)

### 3》如何处理工具调用失败

#### 三层防护

#### 3.1 工具内部处理

![image-20260922155932401](./ch5-工具调用.assets/image-20260922155932401.png)

#### 3.2 Agent级重试

![image-20260922160050815](./ch5-工具调用.assets/image-20260922160050815.png)

#### 3.3 调用级重试

![image-20260922160333689](./ch5-工具调用.assets/image-20260922160333689.png)



### 4》返回字符串

![image-20260922160841838](./ch5-工具调用.assets/image-20260922160841838.png)

### 5.选择同步 vs 异步

![image-20260922161013696](./ch5-工具调用.assets/image-20260922161013696.png)



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