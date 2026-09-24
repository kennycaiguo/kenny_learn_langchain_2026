在Python中，如果你想在 `chapter6` 文件夹中的脚本里导入 `chapter5` 文件夹中的文件，最直接且推荐的方法是**将它们上级的共同父目录添加到系统的模块搜索路径（`sys.path`）中**。

假设你的项目目录结构如下：

text

```
project/
│
├── chapter5/
│   └── module5.py  (你想导入的文件，里面有函数 my_func)
│
└── chapter6/
    └── main.py     (你正在编写的文件)
```

 

你可以在 `chapter6/main.py` 中使用以下代码来实现导入：

📁 核心解决方法：动态修改 `sys.path`

python

```
import sys
from pathlib import Path

# 获取当前文件的绝对路径
current_file = Path(__file__).resolve()

# 获取共同的父目录（project 目录）
project_dir = current_file.parent.parent

# 将父目录添加到 Python 的模块搜索路径中
if str(project_dir) not in sys.path:
    sys.path.append(str(project_dir))

# 现在你可以直接通过文件夹名导入了
from chapter5.module5 import my_func

# 测试调用
my_func()
```

 

💡 为什么不直接使用相对导入（如 `from ..chapter5 import ...`）？

在Python中，**直接运行**一个包含 `..`（相对导入）的脚本经常会触发 `ValueError: attempted relative import beyond top-level package` 错误。相对导入只有在整个项目被当作一个完整的包（Package）运行，且你使用 `python -m chapter6.main` 的方式从根目录启动时才会生效。对于平常直接右键运行单文件的习惯，上面修改 `sys.path` 的方法最不容易出错。