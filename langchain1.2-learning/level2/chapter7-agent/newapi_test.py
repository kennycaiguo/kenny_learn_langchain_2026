from tool_utils import query_news_from_web

new = query_news_from_web("微软")
print(new)
# print(new.get("articles")[0].get("title"))
# print(new.get("articles")[0].get("content"))


