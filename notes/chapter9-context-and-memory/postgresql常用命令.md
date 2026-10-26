# PostgreSQL-常用命令

PostgreSQL数据库是一个系统（应用）最重要的资产之一，所以我们的数据库将从以下几个数据库来进行介绍。

**PostgreSQL常用命令包括数据库连接(`psql`)、查看对象(`\l`, `\dt`, `\d`)、数据操作(CRUD)和权限管理(`\du`, `GRANT`)等，是****数据库管理****和查询的基础工具。**

#### **一、数据库连接与退出**



```javascript
psql -U 用户名 \
     -d 数据库名 \
     -h 主机地址 \
     -p 端口号
     
\q：退出 psql 命令行。
```

#### **二、数据库表操作**

```javascript
\l       显示所有数据库
\c xxx   进入某个数据
\dt      显示所有表
\d xxx   显示表结构 
\dn      查看所有模式

 
#库操作
CREATE DATABASE [数据库名]
DROP DATABASE [数据库名];
#模式操作
CREATE SCHEMA schema_name;
DROP SCHEMA schema_name;
DROP SCHEMA schema_name CASCADE; 强制删除模式下所有对象

#表操作
DROP TABLE 表名;：删除表。
DROP TABLE IF EXISTS 表名;：存在则删除，避免报错。
ALTER TABLE 表名 ADD COLUMN 字段名 数据类型;：添加字段。
ALTER TABLE 表名 DROP COLUMN 字段名;：删除字段。
ALTER TABLE 表名 RENAME COLUMN 旧字段名 TO 新字段名;：修改字段名。
ALTER TABLE 表名 ALTER COLUMN 字段名 TYPE 新数据类型;：修改字段数据类型。
```

**三、用户与权限**



```javascript
#创建超级管理员,需要超级管理员才可以创建。
CREATE ROLE super_admin WITH SUPERUSER LOGIN PASSWORD 'your_password';-- 创建普通角色（无登录权限）

CREATE ROLE 角色名;
-- 创建可登录的用户（角色+LOGIN权限）
CREATE USER 用户名 WITH LOGIN PASSWORD '密码';  
-- USER 是 CREATE ROLE ... WITH LOGIN 的简写
```





```javascript
-- 修改密码
ALTER ROLE 用户名 WITH PASSWORD '新密码';
-- 允许/禁止登录
ALTER ROLE 用户名 WITH LOGIN;   -- 允许登录
ALTER ROLE 用户名 WITH NOLOGIN; -- 禁止登录
-- 授予/撤销超级用户权限
ALTER ROLE 用户名 WITH SUPERUSER;   -- 授予
ALTER ROLE 用户名 WITH NOSUPERUSER; -- 撤销
-- 修改其他属性（如创建数据库权限）
ALTER ROLE 用户名 WITH CREATEDB;    -- 允许创建数据库
ALTER ROLE 用户名 WITH NOCREATEDB;  -- 禁止创建数据库
```



```javascript
-- 列出所有角色（含权限概要）
\du  -- psql 命令
-- 查看角色详细属性（SQL查询）
SELECT * FROM pg_roles WHERE rolname = '角色名';
```



```javascript
-- 删除角色（需先确保无活跃连接，且该角色无依赖对象）
DROP ROLE 角色名;
-- 强制删除（若有依赖，会级联删除关联权限）
DROP ROLE IF EXISTS 角色名 CASCADE;
```



```javascript
-- 授予用户对数据库的所有权限
GRANT ALL PRIVILEGES ON DATABASE 数据库名 TO 用户名;
-- 授予指定权限（如连接、创建表）
GRANT CONNECT, CREATE ON DATABASE 数据库名 TO 用户名;
-- CONNECT：允许连接数据库；CREATE：允许在数据库中创建 schema
```

代码语言：javascript

AI代码解释



```javascript
-- 授予用户对 schema 的所有权限
GRANT ALL PRIVILEGES ON SCHEMA schema名 TO 用户名;
-- 授予指定权限（如创建表、查看对象）
GRANT USAGE, CREATE ON SCHEMA schema名 TO 用户名;
-- USAGE：允许访问 schema 中的对象；CREATE：允许在 schema 中创建对象
```

**三、****数据备份****和还原**

代码语言：javascript

AI代码解释



```javascript
#备份
#备份远程的库，有多少库，就需要输入多少次密码。
pg_dumpall -U postgres -h localhost -p 5432 -f back.sql

#备份本机不需要输入密码
pg_dumpall -U postgres  -f back.sql

#备份单个库,不需要输入密码，默认文本格式，只能用psql还原
pg_dump -U postgres -d dbname  -f dbname.sql

#备份单个库,不需要输入密码，使用二进制备份
pg_dump -U postgres -d dbname -F c -f dbname.sql
#还原单个库，库必须要提前创建
#默认不加参数的pg_dump的备份只能用psql还原
psql -h 192.168.1.1 -p 5432 -U postgres -d public  -f  public.sql 

#二进制备份还原
pg_restore -h 192.168.0.182 -U postgres -d public1  back2.sql 
```

**四、其他运维命令**

代码语言：javascript

AI代码解释



```javascript
#查看每个库的大小
SELECT pg_database.datname AS "Database Name", pg_size_pretty(pg_database_size(pg_database.datname)) AS "Size" FROM pg_database;

#查看当前库有多少表，需要进入库
SELECT count(*) AS table_count FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = 'xxxx';

#查看当前库每个表有多少条记录(需要进入库)，如果表太多，可以添加limit

#查看所有用户
SELECT usename AS "Username", usecreatedb AS "Can Create DB?", usesuper AS "Is Superuser?" FROM pg_user;

#创建表（这里需要注意，在pg里面每个表还有自己的owner，如果权限不对也是无法curd的）
#比如如果某个库绑定了某个账号，如果用psql用户进入库创建了表，则这个绑定的用户对这个表也无curd权限。
CREATE TABLE users1 (id serial PRIMARY KEY, name varchar(100) NOT NULL, email varchar(100) UNIQUE);

#修改表的owner
ALTER TABLE table_name OWNER TO new_owner;

#插入数据
INSERT INTO users1 (name, email) VALUES ('User', 'user@example.com');
```

**五、扩展**

代码语言：javascript

AI代码解释



```javascript
#启用扩展
CREATE EXTENSION citext;  //定义了一种新的数据类型，来代替文本实现忽略大小写的问题

#常用扩展
pgcrypto: 提供了各种密码学函数，用于数据加密、解密和哈希等操作。
uuid-ossp: 支持生成和处理 UUID（通用唯一标识符），用于唯一标识数据行或对象。
hstore: 提供了一个键值对的存储模型，可以在单个列中存储非结构化数据。
pg_trgm: 提供了 trigram 相似度匹配功能，用于进行模糊文本搜索和匹配。
ltree: 支持层次树结构数据的存储和查询，用于处理层次结构数据。
pg_stat_statements: 收集并展示 SQL 查询的统计信息，用于性能调优和查询优化。
postgis: 提供了地理信息系统（GIS）功能，支持地理空间数据的存储和查询。
pg_partman: 提供了表分区管理功能，用于自动管理大型表的数据分区。
pglogical: 实现逻辑复制功能，用于在不同 PostgreSQL 数据库之间进行数据同步和复制。
citext: 提供了大小写不敏感的文本比较和匹配功能，简化文本处理过程。

#查询开启了什么扩展
SELECT * FROM pg_extension;
或者
\dx 
#查询有哪些扩展可用
SELECT * FROM pg_available_extensions;

#部分扩展pg，可能不会自带，需要额外导入包才可以
```

**六、模板**



```javascript
#在pg中，默认会有2个库template0和template1
template0 是一个干净的、只读的空模板数据库，用于创建全新的数据库，不允许用户修改它的内容。
template1 是一个可以修改的模板数据库，用户可以向其中添加自定义数据、设置和表结构，然后将其用作创建新数据库的模板，每加参数默认就是用的这个库
```

