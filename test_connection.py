from sqlalchemy import text
from app.database.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print(result.fetchone())
        print("\n✅ PostgreSQL Connected Successfully!")

except Exception as e:
    print("Connection Failed")
    print(e)