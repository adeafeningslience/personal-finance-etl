import pandas as pd
import psycopg2
import os
import socket
from urllib.parse import urlparse


df = pd.read_csv('categ.csv')


# Parse DATABASE_URL
url = urlparse(os.environ["DATABASE_URL"])

# Resolve to IPv4
ipv4_host = socket.gethostbyname(url.hostname)

# Build new DSN with IPv4
dsn = f"dbname={url.path[1:]} user={url.username} password={url.password} host={ipv4_host} port={url.port}"

conn = psycopg2.connect(dsn)

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






