import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from sqlalchemy import text

def wipe_db():
    db = SessionLocal()
    try:
        # Use TRUNCATE CASCADE to clear all tables safely
        tables = [
            "reminders",
            "alerts",
            "signal_extractions",
            "health_scores",
            "inputs",
            "contracts",
            "accounts"
        ]
        
        tables_str = ", ".join(tables)
        print(f"Truncating tables: {tables_str}")
        db.execute(text(f"TRUNCATE {tables_str} CASCADE"))
        
        db.commit()
        print("Database wiped successfully!")
    except Exception as e:
        print(f"Error wiping database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    wipe_db()
