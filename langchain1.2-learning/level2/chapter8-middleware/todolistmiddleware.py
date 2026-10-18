from langchain_core import messages
from langchain.agents.middleware import SummarizationMiddleware, PIIMiddleware, TodoListMiddleware
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import Union, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.config import get_stream_writer
from rich import print as rprint
from utils.file_utils import read_file, write_file, list_files,run_test


# 1.初始化模型给中间件使用，不是agent
model = ChatOpenAI(
    # model="qwen3-vl:latest",
    # model="483025889/qwen3.5:9b",
    model="gemma4:12b",
    api_key="sk12345",
    base_url="http://localhost:11434/v1",
)

# 2.创建agent对象
agent = create_agent(
    model=model,
    tools=[list_files,read_file,write_file,run_test],
    middleware=[
        TodoListMiddleware(),
    ],
    system_prompt=(
        "你是一个代码修复助手。遇到多步骤任务是，先使用write_todos 制定待办事项: "
        "然后读取文件，修复代码并运行测试。工作全部在工作区下进行。"
    )

)

# 3.调用agent
print("正在执行 Agent 任务。。。")

res = agent.invoke({"messages":[
    HumanMessage(content="请测试并修复工作区下 my_add.py 文件中的代码")
]})

for msg in res["messages"]:
    msg.pretty_print()




