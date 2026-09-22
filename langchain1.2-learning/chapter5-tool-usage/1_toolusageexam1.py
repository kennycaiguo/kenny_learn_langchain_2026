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

## 工具的参数模型
class WeatherSchema(BaseModel):
    city:str = Field(
        description="具体的城市",
        default="北京"
    )
    if_forecast:bool = Field(
        description="是否包含明天的天气预报",
        default=False
    )

## 使用args_schema+Pydantic模型定义工具
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