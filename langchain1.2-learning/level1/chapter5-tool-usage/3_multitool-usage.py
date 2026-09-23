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