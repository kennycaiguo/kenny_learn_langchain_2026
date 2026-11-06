# python jq schema 参考

在 Python 中，提及 “jq schema” 通常是指在使用 jq 库 或在大模型框架（如 LangChain 的 JSONLoader）中，通过 jq 的表达式（语法）作为提取、过滤和重组 JSON 数据的规则（Schema）。
由于 jq 库核心是基于 C 语言版的命令行工具，其所谓的 Schema 实际上就是 jq 过滤表达式。以下为您整理了在 Python 环境下常用的 jq schema 语法、Python 映射关系及代码示例参考。

# 一、 jq 常用过滤语法（Schema 规则）

| 语法 (Expression)  | 作用 (Description)                 | 示例输入               | 示例输出                  |
| ------------------ | ---------------------------------- | ---------------------- | ------------------------- |
| **`.`**            | 身份运算符（输出整个原始数据）     | `{"a": 1}`             | `{"a": 1}`                |
| **`.key`**         | 获取指定键的值                     | `{"name": "Alice"}`    | `"Alice"`                 |
| **`.key1.key2`**   | 链式获取嵌套键的值                 | `{"a": {"b": 2}}`      | `2`                       |
| **`.[]`**          | 展开数组或对象的所有元素           | `[1, 2, 3]`            | `1`, `2`, `3`（多条记录） |
| **`.[index]`**     | 获取数组指定索引的元素             | `["a", "b", "c"]`      | `.[1]` -> `"b"`           |
| **`.[start:end]`** | 数组切片                           | `["a", "b", "c"]`      | `.[0:2]` -> `["a", "b"]`  |
| **`.[] | .key`**   | 管道符：将前者的输出作为后者的输入 | `[{"id":1}, {"id":2}]` | `.[] | .id` -> `1`, `2`   |

## 高级转换与构造

- **构造新数组**：`jq.compile("[ .users[].name ]")` → 将零散的输出打包进一个 Python 列表 `['Alice', 'Bob']`。
- **构造新对象**：`jq.compile("{user_name: .name, user_age: .age}")` → 重新映射键名。
- **条件过滤 (select)**：`jq.compile(".users[] \| select(.age > 28)")` → 只保留年龄大于 28 的用户对象。

# 二、 Python 数据类型映射关系

当 jq 表达式处理完 JSON 后，Python 库会将其自动转换为对应的 Python 内置类型：
• jq 返回数组 → Python list
• jq 返回对象 → Python dict
• jq 返回字符串/数字/布尔 → Python str / int / float / bool



# 三、 核心应用场景与代码示例


场景 1：原生 jq 库的 Schema 数据转化

首先需要安装 Python 绑定库：pip install jq。
import jq

## 原始复杂的嵌套 JSON 数据
data = {
    "store": "Central",
    "books": [
        {"title": "Python Basics", "price": 40, "tags": ["tech", "learn"]},
        {"title": "AI Era", "price": 55, "tags": ["tech", "future"]}
    ]
}

## 1. 提取所有书名列表
### schema 逻辑: 找到 books 数组 -> 迭代每一项 -> 提取 title -> 组合成新数组
schema_1 = "[.books[].title]" 
result_1 = jq.compile(schema_1).input_value(data).first()
print(result_1)  # 输出: ['Python Basics', 'AI Era']

## 2. 过滤并重构全新结构 (Schema 转换)
### schema 逻辑: 遍历 books 数组，把每项转化为自定义的键名，并提取 tags 的第一个元素
schema_2 = ".books | map({book_name: .title, main_tag: .tags[0]})"
result_2 = jq.compile(schema_2).input_value(data).first()
print(result_2)  
### 输出: [{'book_name': 'Python Basics', 'main_tag': 'tech'}, {'book_name': 'AI Era', 'main_tag': 'tech'}]
 

场景 2：LangChain JSONLoader 中的 jq_schema

在搭建 RAG（检索增强生成）应用时，常需从 JSON 中提取文本生成 Document 对象。
python
### 需要安装: pip install langchain-community jq
from langchain_community.document_loaders import JSONLoader

### 假设本地有一个 sample.json，内容为：
#### {"messages": [{"text": "Hello world", "sender": "AI"}, {"text": "Hi", "sender": "User"}]}

### 这里的 jq_schema 作用是：指出哪部分数据应该作为文档的 page_content
loader = JSONLoader(
    file_path="./sample.json",
    jq_schema=".messages[].text",  # Schema 规则：提取 messages 数组下所有 text 字段
    text_content=True              # 期望提取结果为字符串
)

docs = loader.load()
for doc in docs:
    print(doc.page_content)
### 输出:
#### Hello world
#### Hi
 

# 四、 避坑指南

1. text_content 报错：在 LangChain 中，如果你的 jq_schema 提取出来的是一个对象（如 {}）或数组（如 []），而 text_content 默认为 True，程序会抛出 Expected page_content is string, got <class 'dict'> 错误。处理结构化数据时应将其设置为 text_content=False。
2. 特殊字符：如果 JSON 的键名包含空格或横杠（如 "user-name"），在写 jq_schema 时必须加双引号：."user-name"