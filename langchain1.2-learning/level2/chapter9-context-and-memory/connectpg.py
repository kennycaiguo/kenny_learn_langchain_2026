import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("PG_USER")
db_pwd = os.getenv("PG_PWD")

db_url = f"postgresql://{db_user}:{db_pwd}@localhost:5432/langchain_db?sslmode=disable"
conn = psycopg2.connect(db_url)
cursor = conn.cursor()
print(cursor)
print(db_url)