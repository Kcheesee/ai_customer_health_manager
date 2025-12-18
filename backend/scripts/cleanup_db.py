import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.account import Account

def cleanup_db():
    db = SessionLocal()
    try:
        accounts = db.query(Account).all()
        for account in accounts:
            if account.tier:
                account.tier = account.tier.lower()
            if account.account_type:
                account.account_type = account.account_type.lower()
        db.commit()
        print("Database types standardized to lowercase.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_db()
