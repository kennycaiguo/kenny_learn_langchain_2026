# [jq命令总结](https://www.cnblogs.com/xwupiaomiao/p/18411630)

![img](https://img2024.cnblogs.com/blog/1278118/202409/1278118-20240913094130315-855198819.png)

 常用示例

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# 获取使用数字为key的value
echo '{"OPT_STATUS": "SUCCESS","DATA": {"16": [{"10": "Alice","11": 25},{"10": "Bob","11": 25},{"10": "Charlie","11": 23}],"expires_in": 3600,"token_type": "password","username": "admin"},"OPT_STATUS_CN": "成功","OPT_STATUS": "SUCCESS"}' | jq -r '.DATA."16"[]."10"'
# 取消双引号
echo '{"OPT_STATUS": "SUCCESS","DATA": {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni","expires_in": 3600,"token_type": "password","username": "admin"},"OPT_STATUS_CN": "成功","OPT_STATUS": "SUCCESS"}' | jq -r .DATA.access_token
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq -r '.DATA | .[].name,.[].city'
# 压缩json
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq -c .DATA
# 使用字符串拼接"\(.field)"来逐个输出字段
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq -r '.DATA[] | "\(.name) \(.age) \(.city)"'
# select条件过滤
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq .DATA | jq '.[] | select(.age >= 25)'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name == "Charlie")'
# 非空判断
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | length > 0)'
# 筛选name包含"li"字符的记录
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | contains("li"))'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | index("li"))'
# 字符串切片，筛选name以"A"开头的记录
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name[0:1] == "A")'
# 过滤name字段的值,以B开头(区分大小写)
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | startswith("B"))'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | startswith("B")) | .name'
# 过滤name字段的值,以e结尾(区分大小写)
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | endswith("e"))'
# 过滤name字段的值使用正则匹配
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name | test("\\w+"))'
# 多条件组合过滤
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select(.name=="Charlie" and .age==23)'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq ".DATA | .[] | select(.name==\"Charlie\" or .age==25)"
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | .[] | select((.name | startswith("B")) and .age==25)'
# 转换为数组
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq ".DATA | map(.name,.city)"
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq ".DATA | [.[].name,.[].city]"
# 转换为对象
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq ".DATA | map({name:.name,city:.city})"
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq ".DATA | [ .[] | {"name":.name,"city":.city}]"
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# 合并对象
RES1='{"name": "Alice",  "age": 30}'
RES2='{"city": "Wonderland",  "country": "Imaginary"}'
RES3='{"hobby": "Reading",  "language": "English"}'
echo $RES1 $RES2 $RES3 | jq -s add
# .[0] 访问第一个对象，.[1] 访问第二个对象，.[2] 访问第三个对象
echo $RES1 $RES2 $RES3 | jq -s '.[0] * .[1] * .[2]'
# 在对象中添加属性
echo '{"name": "Alice", "age": 30}' | jq '.city = "Wonderland"'
echo '{"name": "Alice", "age": 30}' | jq '. + {"city": "Wonderland", "country": "Imaginary"}'
echo '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]' | jq 'map(. + {"city": "Wonderland", "country": "Imaginary"})'
# 合并数组
RES1=$(echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '[.DATA.[]]')
RES2=$(echo '{"DATA": [{"name": "Lucy","age": 18,"city": "Washington"},{"name": "Charlie","age": 23,"city": "Los Angeles"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '[.DATA.[]]')
echo '{"DATA": [{"name": "Jims","age": 42,"city": "Columbia"},{"name": "Trump","age": 77,"city": "Atlanta"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' >data.json
RES3=$(jq '[.DATA.[]]' data.json)
echo $RES1 $RES2 $RES3 | jq -s add
# 在数组中添加元素
echo '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]' | jq '. + [{"name": "Charlie", "age": 22}] | . + [{"name": "Lucy", "age": 18}]'
echo '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]' | jq '. += [{"name": "Charlie", "age": 22}] | . += [{"name": "Lucy", "age": 18}]'
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# 检查对象中是否存在键"city"，如果存在则返回其值，如果不存在则返回"not found"
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq -r '.DATA.[] | if has("city") then .city else "not found" end'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq -r '.DATA[] | if has("city") then .city else "not found" end'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq -r '.DATA.[].city // "not found"'
# 检查对象中是否存在键"city"，如果不存在则返回该对象的name和age
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Jim","age": 20,"job": "IT"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '[.DATA[] | select(has("city") | not) | {name:.name,age:.age}]'
echo '{"DATA": [{"name": "Alice","age": 30,"city": "New York"},{"name": "Bob","age": 25,"city": "San Francisco"},{"name": "Jim","age": 20,"job": "IT"}],"TYPE": "dict","OPT_STATUS": "SUCCESS"}' | jq '.DATA | map(select(has("city") | not) | {name: .name, age: .age})'
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

安装jq命令，或者直接从github下载二进制文件，然后把文件移动到系统的/usr/bin目录下

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# 离线安装
apt-get install autoconf automake libtool oniguruma-dev
yum install autoconf automake libtool oniguruma oniguruma-devel
git clone https://github.com/stedolan/jq.git
cd jq 
autoreconf -i
./configure --prefix=/usr/local/etc/jq --with-oniguruma
make && make install
cd /usr/local/
ln -s ../etc/jq/bin/jq bin/jq

# 在线安装
git clone https://github.com/stedolan/jq.git
cd jq
git submodule update --init
autoreconf -i
./configure --prefix=/usr/local/etc/jq --with-oniguruma=builtin
make && make install
cd /usr/local
ln -s ../etc/jq/bin/jq bin/jq
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0);)

参考链接：
   https://jqlang.github.io/jq/manual/     # jq json格式化命令
   https://github.com/jqlang/jq/releases  # jq二进制文件下载
   https://www.cnblogs.com/websec80/p/17528197.html

