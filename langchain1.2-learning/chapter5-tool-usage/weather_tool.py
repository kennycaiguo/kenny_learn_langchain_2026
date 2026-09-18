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