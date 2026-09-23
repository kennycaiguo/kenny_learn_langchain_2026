from io import BytesIO
import requests
from PIL import Image

# 1. 输入图片的网址
url = "https://img.iplaysoft.com/wp-content/uploads/2019/free-images/free_stock_photo_2x.jpg!0x0.webp"

# 2. 发送请求获取图片内容
response = requests.get(url)

# 3. 检查请求是否成功
if response.status_code == 200:
  # 4. 将字节数据转换为字节流并打开图片
  image = Image.open(BytesIO(response.content))
  # 5. 显示图片
  image.show()
else:
  print("图片下载失败")