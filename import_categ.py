import pandas as pd
import psycopg2
import os

df = pd.read_csv('categ.csv')

conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT", "5432")
)

cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO ref.categories (id, name)
    VALUES (%s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (row["id"], row["name"]))

conn.commit()
cursor.close()
conn.close()
