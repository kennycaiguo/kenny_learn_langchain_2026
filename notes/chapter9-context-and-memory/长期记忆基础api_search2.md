## 基于InMemoryStore

### 按照filter过滤


```python
for item in store.search(("users",),filter={"food":"紫光园奶皮子酸奶"}):
    print(item)
```

    Item(namespace=['users', 'alice', 'memories'], key='preferences', value={'course': '计算机组成原理', 'sports': '跑步', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557515+00:00', updated_at='2026-10-29T02:16:30.557518+00:00', score=None)
    Item(namespace=['users', 'Black', 'memories'], key='preferences', value={'course': '数字电路与模拟电路', 'sports': '羽毛球', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557573+00:00', updated_at='2026-10-29T02:16:30.557574+00:00', score=None)



```python
for item in store.search(("users",),filter={"sports":"羽毛球"}):
    print(item)
```

    Item(namespace=['users', 'Black', 'memories'], key='preferences', value={'course': '数字电路与模拟电路', 'sports': '羽毛球', 'food': '紫光园奶皮子酸奶'}, created_at='2026-10-29T02:16:30.557573+00:00', updated_at='2026-10-29T02:16:30.557574+00:00', score=None)

