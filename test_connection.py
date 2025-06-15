import os
import ssl
import sqlalchemy

ssl_context = ssl.create_default_context()

try:
    engine = sqlalchemy.create_engine(
        os.environ["DATABASE_URL"],
        connect_args={"ssl_context": ssl_context}
    )
    with engine.connect() as conn:
        print("✅ Connected successfully!")
except Exception as e:
    print("❌ Connection failed:")
    print(e)
    exit(1)
