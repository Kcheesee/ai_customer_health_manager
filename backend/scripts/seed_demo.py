import sys
import os
from uuid import uuid4
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.account import Account
from app.models.health_score import HealthScore

def seed_demo():
    db = SessionLocal()
    try:
        # 1. Create demo accounts
        stark = Account(
            id=uuid4(),
            name="Stark Industries",
            account_type="ela_parent",
            tier="enterprise",
            industry="Aerospace & Defense",
            check_in_interval_days=30,
        )
        techflow = Account(
            id=uuid4(),
            name="TechFlow Solutions",
            account_type="standard",
            tier="mid_market",
            industry="Software",
            check_in_interval_days=15,
        )
        churn_risk = Account(
            id=uuid4(),
            name="Churn Risk Corp",
            account_type="standard",
            tier="smb",
            industry="Retail",
            check_in_interval_days=7,
        )
        
        db.add_all([stark, techflow, churn_risk])
        db.flush()

        # 2. Add Health Scores
        health_stark = HealthScore(
            id=uuid4(), account_id=stark.id, overall_score=85, overall_status="healthy",
            sentiment_score=90, engagement_score=100, request_score=70,
            relationship_score=100, satisfaction_score=80, expansion_score=70,
            ai_summary="Stark Industries is a flagship account with high engagement. Expansion possible in Q4.",
            calculated_at=datetime.utcnow()
        )
        health_risk = HealthScore(
            id=uuid4(), account_id=churn_risk.id, overall_score=25, overall_status="at_risk",
            sentiment_score=20, engagement_score=30, request_score=40,
            relationship_score=10, satisfaction_score=20, expansion_score=10,
            ai_summary="CRITICAL: Negative sentiment in recent emails. No response to engagement attempts in 14 days.",
            calculated_at=datetime.utcnow()
        )
        db.add_all([health_stark, health_risk])

        # 3. Add Inputs (Activity)
        from app.models.input import Input
        inputs = [
            Input(id=uuid4(), account_id=stark.id, input_type="email", sender="Tony Stark", folder="Renewals",
                  content="Looking forward to the renewal discussion. We want to expand to the NY office.",
                  content_date=datetime.utcnow() - timedelta(days=2)),
            Input(id=uuid4(), account_id=stark.id, input_type="meeting_note", sender="Pepper Potts", folder="Strategic",
                  content="Quarterly sync went well. High interest in the new AI features.",
                  content_date=datetime.utcnow() - timedelta(days=5)),
            Input(id=uuid4(), account_id=churn_risk.id, input_type="email", sender="Angry Manager", folder="Support",
                  content="The system is too slow. We are considering other options.",
                  content_date=datetime.utcnow() - timedelta(days=1)),
            Input(id=uuid4(), account_id=techflow.id, input_type="call", sender="Sarah Jenkins", folder="Onboarding",
                  content="Onboarding is moving slowly but we are making progress.",
                  content_date=datetime.utcnow() - timedelta(days=10))
        ]
        db.add_all(inputs)

        # 4. Add Contracts
        from app.models.contract import Contract
        contracts = [
            Contract(id=uuid4(), account_id=stark.id, contract_name="Enterprise License",
                     contract_type="renewal", total_contract_value=500000.0, arr=500000.0, 
                     status="active", effective_date=datetime.utcnow() - timedelta(days=300),
                     end_date=datetime.utcnow() + timedelta(days=65)),
            Contract(id=uuid4(), account_id=techflow.id, contract_name="Mid-Market SaaS",
                     contract_type="new_business", total_contract_value=50000.0, arr=50000.0,
                     status="active", effective_date=datetime.utcnow() - timedelta(days=200),
                     end_date=datetime.utcnow() + timedelta(days=165)),
            Contract(id=uuid4(), account_id=churn_risk.id, contract_name="SMB Starter",
                     contract_type="renewal", total_contract_value=15000.0, arr=15000.0,
                     status="active", effective_date=datetime.utcnow() - timedelta(days=350),
                     end_date=datetime.utcnow() + timedelta(days=15))
        ]
        db.add_all(contracts)

        db.commit()
        print("Demo data seeded successfully with full context (Accounts, Health, Inputs, Contracts)!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo()
