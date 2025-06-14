# this script loads the initial CATEGORIES table from the .csv file

import pandas as pd
import psycopg2

# Load your CSV or Excel
df = pd.read_csv('categ.csv')



# Connect to your database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="K%$h3lle1978",
    host="db.khxszacsifnwklitpkvz.supabase.co",)
cursor = conn.cursor()

# Insert into transactions table
for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO ref.categories (id, name)
    VALUES (%s, %s)
    ON CONFLICT (id) DO UPDATE
    SET name = EXCLUDED.name
    """, (row["id"], row["name"]))

conn.commit()
cursor.close()
conn.close()









