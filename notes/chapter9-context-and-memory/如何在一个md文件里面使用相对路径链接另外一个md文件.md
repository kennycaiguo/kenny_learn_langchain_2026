在 Markdown 文件中使用相对路径链接另一个 Markdown 文件，标准的语法格式为 `[链接文本](相对路径)`。

## 基本语法

markdown

```
[显示文本](相对路径/文件名.md)
```

- **显示文本**：在页面上看到的超链接文字。
- **相对路径**：以当前文件所在的位置为起点，指向目标文件的路径。 [[1](https://comate.baidu.com/zh/page/o7x6zl3ardh), [2](https://blog.csdn.net/icestorm_rain/article/details/108991703)]
- 常用相对路径写法

### 假设你的项目目录结构如下：

text

```
project/
│
├── README.md                （当前文件）
├── intro.md                 （同级目录下的文件）
├── docs/
│   ├── guide.md             （子目录下的文件）
│   └── images/
└── archive/
    └── old.md               （平行目录下的文件）
```

#### **同级目录**（链接 `intro.md`）：

markdown

```
[项目介绍](intro.md)
```

或者加上 `./`（代表当前目录）：

markdown

```
[项目介绍](./intro.md)
```

#### **进入子目录**（从 `README.md` 链接到 `docs/guide.md`）：

markdown

```
[开发指南](docs/guide.md)
```

#### **返回上一级目录**（假设你在 `docs/guide.md` 中，要链接到同级目录的 `README.md`）：

markdown

```
[返回首页](../README.md)
```

*注：`../` 表示退回到上一级目录。*

- 注意事项

- **路径符号**：在所有操作系统（Windows、macOS、Linux）中，相对路径均使用正斜杠 `/`，请不要使用反斜杠 `\`.
- **空格处理**：如果文件名或目录名中带有空格，建议用 `%20` 代替，或者用尖括号包裹，例如：`[示例文档](<my note.md>)`。
- **软件与平台差异**：
  - 在 **Typora** 等本地编辑器中，点击链接通常能直接在软件内打开对应文件。
  - 在 **GitHub / GitLab** 等网页端，相对路径会被自动解析为该仓库对应分支下的网页链接