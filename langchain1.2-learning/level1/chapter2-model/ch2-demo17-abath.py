import asyncio

from langchain.chat_models import init_chat_model
import time
from asyncio import create_task



model = init_chat_model(
    model='deepseek-r1:8b',
    model_provider="ollama"
)

async def async_invoke():
    inputs = [
       "翻译为英文：春天来了",
       "翻译为英文：夏天很热",
       "翻译为英文：秋天落叶",
       "翻译为英文：冬天下雪"
    ]

    print("===================演示abatch的用法=======================")
    start_time = time.perf_counter()
    print("开始....")
    # 1.创建异步任务
    print(">>>发起模型调用")
    as_bat_task = create_task(model.abatch(inputs))
    # 2.继续执行其他操作
    print(">>>模型请求已经在后台发送，继续执行本地逻辑")
    for i in range(3):
        await asyncio.sleep(1) # 使用异步等待，释放控制权
        print(f"正在执行第{i+1}个任务，（已耗时{time.perf_counter()-start_time})")

    # 3.获取模型结果
    print("本地任务完成，检查模型状态")
    resp = await as_bat_task
    for res in resp:
        content = res.content if hasattr(res,"content") else str(res)
        print(f"响应内容：{content}")
    end_time = time.perf_counter()
    print(f"总运行耗时{end_time - start_time:.2f}s===")

async def main():
    await async_invoke()    
        
if __name__ == '__main__':
    asyncio.run(main())