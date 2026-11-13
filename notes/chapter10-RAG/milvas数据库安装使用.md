# 1.安装wsl，window的linux子系统（可以不用先安装，docker安装后会提示你安装）

​    ![image-20261111104404432](./milvas数据库安装使用.assets/image-20261111104404432.png)

## 在powershell 窗口中wsl --install，就会安装linux子系统

![image-20261111105256322](./milvas数据库安装使用.assets/image-20261111105256322.png)

## 安装完成，不过需要重启系统

![image-20261111105515762](./milvas数据库安装使用.assets/image-20261111105515762.png)



# 2.安装Docker Desktop

下载： https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64

## 点击安装文件，在弹出的窗口在选择第二个选项，点击ok

![image-20261111112115766](./milvas数据库安装使用.assets/image-20261111112115766.png)

## 然后，就开始解压，需要一点时间，稍微等待一下。

![image-20261111112219640](./milvas数据库安装使用.assets/image-20261111112219640.png)



## 安装完成后，提示你重启

![image-20261111112425917](./milvas数据库安装使用.assets/image-20261111112425917.png)

## 重启电脑后，Docker安装程序会启动，出现下面的界面，点击accept

![image-20261111104758535](./milvas数据库安装使用.assets/image-20261111104758535.png)

## 在弹出的窗口中选择跳过

![image-20261111104925977](./milvas数据库安装使用.assets/image-20261111104925977.png)

## 在弹出的窗口在勾选第一个选项，然后点击finish按钮完成设置

![image-20261111105034730](./milvas数据库安装使用.assets/image-20261111105034730.png)

![image-20261111105415662](./milvas数据库安装使用.assets/image-20261111105415662.png)

## 可以在不登录的情况下使用docker

![image-20261111111354069](./milvas数据库安装使用.assets/image-20261111111354069.png)

## 点击这个选项后，在弹出的窗口在点击跳过

![image-20261111111500711](./milvas数据库安装使用.assets/image-20261111111500711.png)

## 验证是否安装成功

### 1.打开一个cmd窗口，输入docker，有下面的显示，说明安装成功

![image-20261111111648741](./milvas数据库安装使用.assets/image-20261111111648741.png)

![image-20261111111758871](./milvas数据库安装使用.assets/image-20261111111758871.png)

## 然后，在工具栏里面可以找到它然后点击，就会弹出图形界面

![image-20261111111903690](./milvas数据库安装使用.assets/image-20261111111903690.png)

# 3.设置proxy，在国外不需要设置，如果在国内有2个选择

## 1》使用这个

## 点击setting->proxies->在第一栏选择manual configuration，填写好代理网址。

![image-20261111115617182](./milvas数据库安装使用.assets/image-20261111115617182.png)

## 2》也可以用这个

![image-20261111115926989](./milvas数据库安装使用.assets/image-20261111115926989.png)



# 4.安装Milvus

## 4.0在安装milvus之前，需要关闭docker的resource saver模式

![image-20261111140608674](./milvas数据库安装使用.assets/image-20261111140608674.png)



## 4.1在D盘创建一个文件夹milvus用来保存milvus数据库的数据，然后以管理员身份打开一个powershell窗口，然后把路径定位到d:\milvus

![image-20261111135559334](./milvas数据库安装使用.assets/image-20261111135559334.png)

### 在继续之前，一定要保证docker的左下角显示：engine running

![image-20261111140644121](./milvas数据库安装使用.assets/image-20261111140644121.png)

## 4.2下载启动脚本

```

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.bat" -OutFile standalone.bat
```

## 4.3 下载完成后，可以在对应的文件夹找到这个bat文件

![image-20261111141145962](./milvas数据库安装使用.assets/image-20261111141145962.png)

![image-20261111141201288](./milvas数据库安装使用.assets/image-20261111141201288.png)

## 4.4在powershell里面运行这个文件 .\standalone.bat start

![image-20261111141413747](./milvas数据库安装使用.assets/image-20261111141413747.png)

## 4.5然后它就会下载数据文件到指定的目录

![image-20261111142950038](./milvas数据库安装使用.assets/image-20261111142950038.png)

## 4.6经过比较长时间的等待，下载完成，并且启动完成

![image-20261111143205953](./milvas数据库安装使用.assets/image-20261111143205953.png)

## 然后在docker里面可以看到我们的容器，此时在actions里面有一个停止按钮，说明它正在运行

![image-20261111143513912](./milvas数据库安装使用.assets/image-20261111143513912.png)

## 4.7停止容器，命令： .\standalone.bat stop，出现成功停止的提示，说明成功停止了。

![image-20261111143756036](./milvas数据库安装使用.assets/image-20261111143756036.png)

## 在docker里面查看，发现actions是一个播放按钮，说明它语句停止了，你可以点击这个按钮来启动

![image-20261111143907717](./milvas数据库安装使用.assets/image-20261111143907717.png)

# 5.测试

## 5.1测试之前的准备工作

### 5.1.1 检查是否安装了milvus相关的python库，发现已经安装了

![image-20261111144859591](./milvas数据库安装使用.assets/image-20261111144859591.png)

### 还有SQLAlchemy

![image-20261111144952177](./milvas数据库安装使用.assets/image-20261111144952177.png)

![image-20261111145225960](./milvas数据库安装使用.assets/image-20261111145225960.png)

### 5.2.2确认milvus数据库容器已经运行

![image-20261111145106289](./milvas数据库安装使用.assets/image-20261111145106289.png)

## 5.2 milvus数据模型

### 5.2.1整体结构4个层级：数据库-》集合-》分区-》实体（一条记录）

![image-20261111145551431](./milvas数据库安装使用.assets/image-20261111145551431.png)

### 5.2.2具体说明

![image-20261111145830496](./milvas数据库安装使用.assets/image-20261111145830496.png)

# 6.milvus数据库的基本使用

## 6.1DDL操作

### 6.1.1数据库操作Database

##### 6.1.1.1 查看数据库

![image-20261111151034318](./milvas数据库安装使用.assets/image-20261111151034318.png)

默认只有一个default数据库



##### 6.1.1.2 创建数据库

![image-20261111151449821](./milvas数据库安装使用.assets/image-20261111151449821.png)

##### 执行完成后重新执行上面查看数据库的代码，就可以看到新增的数据库

![image-20261111160728758](./milvas数据库安装使用.assets/image-20261111160728758.png)

##### 6.1.1.3 删除数据库

![image-20261111151753393](./milvas数据库安装使用.assets/image-20261111151753393.png)

###### 比较严谨的代码如下

```
from rich import print as rprint

client.use_database(db_name)
# 在删除数据库之前，必须删除它里面的所有collection
if len(client.list_collections(db_name=db_name))>0:
    for col in client.list_collections():
        client.drop_collection(col)
client.drop_database(db_name)
```

##### 执行完成后重新执行上面查看数据库的代码，就发现数据库已经被删除了

![image-20261111160952285](./milvas数据库安装使用.assets/image-20261111160952285.png)

### 6.1.2 Collection的相关操作

##### 6.1.2.1切换数据库

```
from pymilvus import MilvusClient
from rich import print as rprint

# 创建客户端对象
client = MilvusClient("http://localhost:19530")

# 新建一个rag_tutorial数据库
client.create_database(db_name="rag_tutorial")

# 查看一下
dbs = client.list_databases()
# rprint(dbs) # ['default', 'rag_tutorial']
# 切换到数据库reg_totorial
client.use_database("rag_tutorial")
```

###### 输出：

```
['default', 'rag_tutorial']
```

##### 6.1.2.2查看数据库里面的collection

```
colls = client.list_collections()
rprint(colls)
```

###### 输出

```
[]
```

##### 6.1.2.3创建collection

```
col_name = "docs"
client.create_collection(
    collection_name=col_name,
    dimension=1024,
    metric_type="COSINE",
)
```

###### 输出

```
['docs']
```

##### 6.1.2.4删除collection

```
client.drop_collection(collection_name=col_name)
rprint(client.list_collections())
```

###### 输出

```
[]
```

## 6.2DML操作

### 6.2.1 初始化嵌入模型

```
from langchain.embeddings import init_embeddings

em_model = init_embeddings(
    ## 我们这里使用bge-m3:latest本地嵌入模型，它支持1024维度
    model="ollama:bge-m3:latest"
)

```

### 6.2.2准备Collection

#### 6.2.2.1创建一个Collection

```
from pymilvus import MilvusClient
from rich import print as rprint
client = MilvusClient(host='localhost', port=19530)
# 切换数据库
client.use_database("rag_tutorial")
# 创建collection
col_name = "docs"
client.create_collection(
    collection_name=col_name,
    dimension=1024, # 给bge-m3:latest模型使用必须是1024维
    metric_type="COSINE",
)

# 查看一下
rprint(client.list_collections())
```

### 输出

```
['docs']
```

#### 6.2.2.2查看这个Collection的元数据

```
meta_data = client.describe_collection(collection_name=col_name, )
rprint(meta_data)
```

### 输出

```
{
    'collection_name': 'docs',
    'auto_id': False,
    'num_shards': 1,
    'description': '',
    'fields': [
        {
            'field_id': 100,
            'name': 'id',
            'description': '',
            'type': <DataType.INT64: 5>,
            'params': {},
            'is_primary': True
        },
        {
            'field_id': 101,
            'name': 'vector',
            'description': '',
            'type': <DataType.FLOAT_VECTOR: 101>,
            'params': {'dim': 1024}
        }
    ],
    'functions': [],
    'aliases': [],
    'collection_id': 470399118321993632,
    'consistency_level': 2,
    'properties': {'timezone': 'UTC', 'namespace.sharding.enabled': 'false', 'max_field_id': '102'},
    'num_partitions': 1,
    'enable_dynamic_field': True,
    'enable_namespace': False,
    'created_timestamp': 470403360512540690,
    'update_timestamp': 470403360512540690
}
```

### 6.2.3准备数据

#### 6.2.3.1 准备原始数据

```
# 准备测试数据
texts = [
    "LangChain 是一个用于构建 LLM 应用的开发框架。",
    "Milvus 是一个适合 AI 应用的向量数据库。",
    "RAG 的核心是先检索相关知识，再让大模型生成答案。",
    "Docker Desktop 可以方便地在本地运行 Milvus Standalone。"
]
```

#### 6.2.3.2生成嵌入向量

```
vectors = em_model.embed_documents(texts)
```

#### 6.2.3.3查看生成的嵌入向量

```
print(len(vectors))
print(len(vectors[0]))
print(vectors[0][:5])
```

##### 输出

4
1024
[-0.0072477185, -0.01241455, 0.006812786, -0.023820743, -0.010981089]

#### 6.2.3.4封装为可以插入的数据格

```
data = [
    {
        "id":i,
        "vector":vectors[i],
        "text":texts[i],
        "source":"demo"
    } for i in range(len(texts))
]
```

### 6.2.4写入数据

#### 6.2.4.1插入数据

```
inserted = client.upsert(
    collection_name=col_name,
    data=data,
)
print("inserted result",inserted)
```

##### 输出

inserted result {'upsert_count': 4, 'ids': [0, 1, 2, 3]}

#### 6.2.4.2手动flush

```
client.flush(collection_name=col_name)
```

#### 6.2.4.5查看collection统计信息

```
stats = client.get_collection_stats(collection_name=col_name)
print("stats : ",stats)
```

##### 输出

stats :  {'row_count': 4}

## 6.3DQL操作

### 6.3.1扫描数据

```
# 扫描返回一个迭代器
iterator= client.query_iterator(
    collection_name=col_name,
    filter="",
    output_fields=["*"]
)
# 遍历这个迭代器
i = 0
while True:
    rows = iterator.next()
    if not rows:
        break # 没有数据就跳出循环
    for row in rows:
        print(f"第{i+1}条数据")
        print(f"id:{row['id']},vector:{row['vector'][:6]},text:{row['text']},source:{row['source']}")
        i+=1
# 关闭迭代器
iterator.close()
```



#### 输出

第1条数据
id:0,vector:[-0.007247718516737223, -0.01241455040872097, 0.006812786217778921, -0.023820742964744568, -0.010981089435517788, 0.003364304779097438],text:LangChain 是一个用于构建 LLM 应用的开发框架。,source:demo
第2条数据
id:1,vector:[-0.02614247426390648, -0.007813695818185806, -0.044614244252443314, 0.027146827429533005, -0.03346766158938408, -0.023296315222978592],text:Milvus 是一个适合 AI 应用的向量数据库。,source:demo
第3条数据
id:2,vector:[-0.016585901379585266, -0.008772866800427437, 0.007794947363436222, -0.0005849088774994016, -0.007447077892720699, -0.021641787141561508],text:RAG 的核心是先检索相关知识，再让大模型生成答案。,source:demo
第4条数据
id:3,vector:[0.01743341237306595, 0.028369862586259842, -0.04740368574857712, -0.008444947190582752, -0.020675532519817352, 0.025601768866181374],text:Docker Desktop 可以方便地在本地运行 Milvus Standalone。,source:demo

### 6.3.2通过主键查询数据，使用get方法，可以传递一个id列表

```
rows = client.get(
    collection_name=col_name,
    ids=[0,1,2]
)

for idx, row in enumerate(rows):
    print(f"第{idx+1}条数据：")
    print(f"id:{row['id']},vector:{row['vector'][:6]},text:{row['text']},source:{row['source']}")
```



#### 输出

第1条数据：
id:0,vector:[-0.007247718516737223, -0.01241455040872097, 0.006812786217778921, -0.023820742964744568, -0.010981089435517788, 0.003364304779097438],text:LangChain 是一个用于构建 LLM 应用的开发框架。,source:demo
第2条数据：
id:1,vector:[-0.02614247426390648, -0.007813695818185806, -0.044614244252443314, 0.027146827429533005, -0.03346766158938408, -0.023296315222978592],text:Milvus 是一个适合 AI 应用的向量数据库。,source:demo
第3条数据：
id:2,vector:[-0.016585901379585266, -0.008772866800427437, 0.007794947363436222, -0.0005849088774994016, -0.007447077892720699, -0.021641787141561508],text:RAG 的核心是先检索相关知识，再让大模型生成答案。,source:demo

### 6.3.3相似度检索

#### 6.3.3.1准备查询嵌入

```
# 相似度检索
query = "什么是向量数据库？"
query_vector = em_model.embed_query(query)
rprint(query_vector[:10])
```

#### 输出

```
[
    -0.05891716,
    -0.043307595,
    -0.031699978,
    0.028268743,
    0.002885767,
    0.006640191,
    0.010140234,
    -0.040027887,
    0.015564025,
    -0.0097677745
]
```

#### 6.3.3.2 检索

```
results = client.search(
    collection_name=col_name,
    data=[query_vector],
    limit=3,
    output_fields=["text","source","id"]
)

for res in results[0]:
    print(res)
```

#### 输出

{'id': 1, 'distance': 0.7204978466033936, 'entity': {'id': 1, 'text': 'Milvus 是一个适合 AI 应用的向量数据库。', 'source': 'demo'}}
{'id': 0, 'distance': 0.46550601720809937, 'entity': {'id': 0, 'text': 'LangChain 是一个用于构建 LLM 应用的开发框架。', 'source': 'demo'}}
{'id': 2, 'distance': 0.4186750054359436, 'entity': {'id': 2, 'text': 'RAG 的核心是先检索相关知识，再让大模型生成答案。', 'source': 'demo'}}



















