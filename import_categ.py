import pandas as pd
import psycopg2
import os

df = pd.read_csv('categ.csv')


# Connect using DATABASE_URL environment variable
conn = psycopg2.connect(os.environ["DATABASE_URL"])
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

