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