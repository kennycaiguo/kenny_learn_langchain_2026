## 1.基于InMemoryStore
### 按照namespace前缀搜索


```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
namespace1 = ("users","alice","memories")
key1="preferences"
value1 = {
    "course": "计算机组成原理",
    "sports": "跑步",
    "food": "紫光园奶皮子酸奶"
}

namespace2 = ("users", "Bob", "memories")
key2 = 'preferences'
value2 = {
    "course": "数字电路与模拟电路",
    "sports": "跑步",
    "food": "奶皮子糖葫芦"
}

namespace3 = ("users", "Black", "memories")
key3 = 'preferences'
value3 = {
    "course": "数字电路与模拟电路",
    "sports": "羽毛球",
    "food": "紫光园奶皮子酸奶"
}

store.put(namespace1, key1,value1)
store.put(namespace2, key2,value2)
store.put(namespace3, key3,value3)

for item in store.search(("users",)):
    print(item)
```

    Item(namespace=['users', 'alice', 'memories'], key='preferences', value={'course': '计算机组成原理', 'sports': '跑步', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557515+00:00', updated_at='2026-10-29T02:16:30.557518+00:00', score=None)
    Item(namespace=['users', 'Bob', 'memories'], key='preferences', value={'course': '数字电路与模拟电路', 'sports': '跑步', 'food': '奶皮子糖葫芦'}, created_at='2026-10-29T02:16:30.557549+00:00', updated_at='2026-10-29T02:16:30.557550+00:00', score=None)
    Item(namespace=['users', 'Black', 'memories'], key='preferences', value={'course': '数字电路与模拟电路', 'sports': '羽毛球', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557573+00:00', updated_at='2026-10-29T02:16:30.557574+00:00', score=None)



```python
for item in store.search(("users", "Black", "memories")):
    print(item)
```

    Item(namespace=['users', 'Black', 'memories'], key='preferences', value={'course': '数字电路与模拟电路', 'sports': '羽毛球', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557573+00:00', updated_at='2026-10-29T02:16:30.557574+00:00', score=None)



```python
for item in store.search(("users", "alice")):
    print(item)
```

    Item(namespace=['users', 'alice', 'memories'], key='preferences', value={'course': '计算机组成原理', 'sports': '跑步', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557515+00:00', updated_at='2026-10-29T02:16:30.557518+00:00', score=None)

