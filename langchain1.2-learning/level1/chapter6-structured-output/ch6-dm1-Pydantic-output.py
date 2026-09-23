# 1.初始化模型
import sys
from pathlib import Path
from rich import print as rprint
from pydantic import BaseModel, Field

# 获取当前文件的父目录的父目录（即 basic_level目录）
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from utils.model_utils import create_qwen3_instance

# 定义输出格式类，需要使用pydantic里面的BaseModel类作为基类
class Person(BaseModel):
    """人物信息"""
    name:str = Field(description="姓名")
    age:int = Field(description="年龄")
    job:str = Field(description="职业")

model = create_qwen3_instance()

# 设置模型输出格式
ret_model = model.with_structured_output(Person)

result = ret_model.invoke("李明是一名30岁的软件工程师")
rprint(result)