import psycopg2
import os

conn = psycopg2.connect(os.environ["DATABASE_URL"])
print("✅ Connected successfully!")
conn.close()
