import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def query_weather(city="Beijing", units="metric", language="zh_cn"):
     api_key = os.getenv("OpenWeather_APi_key") 
     # 构建请求URL
     url = "https://api.openweathermap.org/data/2.5/weather"
     # 设置查询参数
     params = {
         "q": city,                 # 查询的城市，默认为北京
         "appid": api_key,          # API密钥
         "units": units,            # 测量单位，默认为摄氏度
         "lang": language           # 输出语言，默认为简体中文
     }
     # 发送GET请求
     response = requests.get(url, params=params)
     # 检查响应状态
     if response.status_code == 200:
         # 解析响应数据
         data = response.json()
         # 打印获取到的数据
         print(f"查询城市: {city}")
         print(f"温度: {data['main']['temp']}°{units[0].upper()}")
         print(f"天气描述: {data['weather'][0]['description']}")
         print(f"湿度: {data['main']['humidity']}%")
         print(f"风速: {data['wind']['speed']} m/s")
         
         return data
     
     else:
         print(f"查询失败，状态码：{response.status_code}")
         print("响应数据：", response.text)

if __name__ == '__main__':
    query_weather()         