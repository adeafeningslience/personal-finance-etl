import os
import sqlalchemy

try:
    engine = sqlalchemy.create_engine(os.environ["DATABASE_URL"], connect_args={"sslmode": "require"})
    with engine.connect() as conn:
        print("✅ Connected successfully!")
except Exception as e:
    print("❌ Connection failed:")
    print(e)
    exit(1)

