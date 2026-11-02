# 长期记忆1.基本API，put()/get()

![image-20261101200356756](./长期记忆api_put_get基本使用-PostgresStore.assets/image-20261101200356756.png)


## put()/get()基于PostgresStore


```python
from langgraph.store.postgres import PostgresStore
from dotenv import load_dotenv
import os

load_dotenv() ## 加载.env文件，因为我们的数据库用户和密码都在里面，然后分别加载他们
db_user = os.getenv("PG_USER")
db_pwd = os.getenv("PG_PWD")
# 拼接数据库url
db_url = f"postgresql://{db_user}:{db_pwd}@localhost:5432/langchain_db?sslmode=disable"

with PostgresStore.from_conn_string(db_url) as store:
     # 数据库的store需要setup
     store.setup()
     namespace=("users",)
     user_id = "user_1"
     user_name="Jack"
     store.put(namespace, user_id, {"name":user_name})
     item = store.get(namespace, user_id)
     print(item)

```

    Item(namespace=['users'], key='user_1', value={'name': 'Jack'}, created_at='2026-10-28T19:56:40.635139-06:00', updated_at='2026-10-28T19:56:40.635139-06:00')


### update data


```python
with PostgresStore.from_conn_string(db_url) as store:
     store.setup() # 每一次调用都需要打开连接 和setup
     user_name="Brenda"
     store.put(namespace, user_id, {"name":user_name})
     item = store.get(namespace, user_id)
     print(item)
```

    Item(namespace=['users'], key='user_1', value={'name': 'Brenda'}, created_at='2026-10-28T19:56:40.635139-06:00', updated_at='2026-10-28T19:58:57.550692-06:00')

