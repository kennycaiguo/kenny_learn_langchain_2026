VSCode更新后运行Jupyter Notebook变慢，通常是由于**变量查看器（Variable Viewer）实时计算**、绘图预览配置（Plot Viewer）或内核与缓存冲突导致的。 [[1](https://stackoverflow.com/questions/74700216/vs-code-with-jupyter-notebook-is-extremely-slow-when-re-running-cells), [2](https://www.volcengine.com/article/1519908), [3](https://zhuanlan.zhihu.com/p/104806977)]

快速解决方法

- **关闭变量视图**：
  运行单元格时，关闭界面上的 `Jupyter: Variables`（变量）面板。大对象或复杂数据结构会强制触发 `repr()` 计算，导致极度卡顿。
- **关闭绘图预览选项**：
  在设置中搜索 `python.dataScience.enablePlotViewer`，将其设置为 `false`，并清空 Notebook 的输出后重新运行。
- **清理工作区缓存**：
  删除 VSCode 对应系统的 `workspaceStorage` 目录中和 Jupyter 相关的缓存文件夹。
- **降级 `ipykernel` 版本**：
  部分新版 `ipykernel` 与环境存在兼容问题，可尝试在终端执行 `pip install ipykernel==6.25.0` 降级后重启内核。
- **关闭硬件加速**：
  在设置中搜索 `Window: Enable GPU Acceleration` 并将其设为 `false`，可缓解界面整体掉帧和卡顿

清理 VSCode 的 `workspaceStorage` 中与 Jupyter 相关的缓存，需要先找到对应操作系统的 `workspaceStorage` 目录，然后检查里面各个工作区文件夹，并删除包含 Jupyter 状态或数据的文件夹。

1. 找到 workspaceStorage 目录

不同操作系统的默认路径如下：

- **Windows**: `%APPDATA%\Code\User\workspaceStorage`
- **macOS**: `~/Library/Application Support/Code/User/workspaceStorage`
- **Linux**: `~/.config/Code/User/workspaceStorage` [[1](https://www.reddit.com/r/Python/comments/q54sg3/delete_vs_code_workspacestorage_cache_folders/?tl=zh-hans), [2](https://blog.csdn.net/sidemap/article/details/121530396)]
- 定位与 Jupyter 相关的缓存文件夹

`workspaceStorage` 下面的每一个子文件夹对应一个工作区（用一串随机数字或哈希命名）。进入每个子文件夹后：

- 查看里面的 `workspace.json` 文件（可以用文本编辑器打开），它会记录这个工作区绑定的项目路径或名称。
- 检查子文件夹中是否有 Jupyter 相关的数据库、状态记录或大文件（例如包含 `ms-toolsai.jupyter` 相关状态、缓存输出或 `state.vscdb` 中包含 Jupyter 数据的区块）。
- *提示*：由于 `workspaceStorage` 里的文件夹名称是随机 ID，若想精准清理 Jupyter 缓存，最安全的方法是**关闭 VSCode**，然后根据需要逐个检查各工作区目录下的 `ms-toolsai.jupyter` 缓存文件，或者编写脚本检索包含 Jupyter 标志的文件夹。