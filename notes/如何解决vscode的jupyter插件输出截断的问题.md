解决 VS Code 中 Jupyter 插件输出截断的问题，主要通过修改 VS Code 的**文本行数限制配置**或调整 **Pandas 的显示参数**来实现。 [[1](https://duetorun.com/blog/20191201/7-vscode-jupyter-notebook/), [2](https://ask.csdn.net/questions/8767252)]

方法一：修改 VS Code 的 Notebook 输出行数限制

VS Code 默认对 Notebook 的文本输出行数有限制（通常超过一定行数会折叠或提示超出大小限制）。你可以调高行数限制或开启滚动条。 [[1](https://stackoverflow.com/questions/68331861/vs-code-and-jupyter-notebook-how-to-open-large-output-in-text-editor), [2](https://duetorun.com/blog/20191201/7-vscode-jupyter-notebook/)]

1. 打开 VS Code 设置（快捷键 `Ctrl + ,` 或 `Cmd + ,`）。

2. 在搜索框中输入 `notebook.output.textLineLimit`。

3. 找到 **Notebook > Output: Text Line Limit**，将默认值（如 30 或 50）修改为一个更大的数值（例如 `1000` 或 `5000`）。

4. 或者直接在 `settings.json` 配置文件中添加以下代码：

   json

   ```
   {
     "notebook.output.textLineLimit": 2000,
     "notebook.output.scrolling": true
   }
   ```

   

方法二：解除 Pandas DataFrame 的行列截断

如果截断的内容是 Pandas 的 `DataFrame` 表格（默认只显示前后几行和部分列），需要在代码中通过全局选项取消限制。 [[1](https://ask.csdn.net/questions/8767252)]

在 Jupyter 单元格中加入以下代码： [[1](https://ask.csdn.net/questions/8767252)]

python

```
import pandas as pd

# 允许显示的最大行数和列数（设置为 None 表示不限制）
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 设置单行显示的最大宽度（防止列宽过窄导致自动换行或省略）
pd.set_option('display.width', 1000)
```