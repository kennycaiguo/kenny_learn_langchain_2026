import re

# 自定义检测函数
def detect_phone_number(content: str):
    return [
        {
            "text":m.group(0),# 提取出具体匹配到的11位数字文本(例如：13800138000)
            "start":m.start(), # 起始索引位置（从0开始）
            "end":m.end()  # 结束索引位置
        } for m in re.finditer(r"[0-9]{11}",content)
    ]

text= "尚硅谷的电话是：13812345678,康师傅的电话是：13987654321"
res = detect_phone_number(text)
print(res)
