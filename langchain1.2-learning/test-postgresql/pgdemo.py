"""
# 安装postgresql python操作库
pip install psycopg2
# 安装python-dotenv
pip install python-dotenv
"""
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

from pymsgbox import password

load_dotenv()

db_user = os.getenv("db_user")
db_pwd = os.getenv("db_pwd")

try:
   conn = psycopg2.connect(
       user=db_user,
       password=db_pwd,
       host="127.0.0.1",
       port="5432",
       database="exampledb"
   )
   print("Database connected successfully")
except Exception as e:
    print(e) 

cursor = conn.cursor()
# # 插入数据
# 
# insert_query = """ INSERT INTO employees (name, age, position)
#                    VALUES (%s,%s,%s) RETURNING id; """

# # data = ('John Doe', 30, 'Software Developer')
# data = ('Mary', 28, 'Secretary')
# cursor.execute(insert_query,data)
# new_id = cursor.fetchone()[0]
# # 需要提交数据
# conn.commit()
# count = cursor.rowcount
# print(count, "Record inserted successfully, ID:", new_id) # ok

# 查询所有数据
# sql = "select * from employees;"
# cursor.execute(sql)
# records = cursor.fetchall()
# print(records) # ok  [(1, 'John Doe', 30, 'Software Developer'), (2, 'Mary', 28, 'Secretary')]

# 更新数据
# sql = "update employees set name=%s where id=%s;"
# data = ("Jack Lee",1)
# cursor.execute(sql,data)
# conn.commit()
# count = cursor.rowcount
# print(count, "Record updated successfully ")

# 删除数据
sql = "delete from employees where id=%s;"
data=(1,)
cursor.execute(sql,data)
conn.commit()
count = cursor.rowcount
print(count, "Record deleted successfully ")
