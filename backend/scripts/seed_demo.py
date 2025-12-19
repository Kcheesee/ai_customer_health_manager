"""
Demo data seeder for Customer Pulse.
Now includes federal compliance data - the differentiator!
"""
import sys
import os
from uuid import uuid4
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.account import Account
from app.models.health_score import HealthScore
from app.models.input import Input
from app.models.contract import Contract
from app.models.contact import Contact


def seed_demo():
    db = SessionLocal()
    try:
        # ============================================================
        # 1. CREATE ACCOUNTS
        # ============================================================
        
        # Enterprise - Healthy
        stark = Account(
            id=uuid4(),
            name="Stark Industries",
            account_type="ela_parent",
            tier="enterprise",
            industry="Aerospace & Defense",
            check_in_interval_days=30,
        )
        
        # Mid-market - Warning
        techflow = Account(
            id=uuid4(),
            name="TechFlow Solutions",
            account_type="standard",
            tier="mid_market",
            industry="Software",
            check_in_interval_days=15,
        )
        
        # SMB - At Risk
        churn_risk = Account(
            id=uuid4(),
            name="Churn Risk Corp",
            account_type="standard",
            tier="smb",
            industry="Retail",
            check_in_interval_days=7,
        )
        
        # FEDERAL ACCOUNT - Your differentiator!
        treasury = Account(
            id=uuid4(),
            name="US Treasury - Bureau of Fiscal Service",
            account_type="ela_parent",
            tier="enterprise",
            industry="Federal Government",
            check_in_interval_days=14,
        )
        
        db.add_all([stark, techflow, churn_risk, treasury])
        db.flush()

        # ============================================================
        # 2. ADD HEALTH SCORES (with trend data)
        # ============================================================
        
        health_stark = HealthScore(
            id=uuid4(), 
            account_id=stark.id, 
            overall_score=85, 
            overall_status="healthy",
            sentiment_score=90, 
            engagement_score=100, 
            request_score=70,
            relationship_score=100, 
            satisfaction_score=80, 
            expansion_score=70,
            # Trend data
            previous_score=82,
            score_change=3,
            trend_direction="stable",
            triggered_by="daily_job",
            ai_summary="Stark Industries is a flagship account with high engagement. Expansion possible in Q4.",
            calculated_at=datetime.utcnow()
        )
        
        health_techflow = HealthScore(
            id=uuid4(),
            account_id=techflow.id,
            overall_score=58,
            overall_status="warning",
            sentiment_score=60,
            engagement_score=50,
            request_score=65,
            relationship_score=55,
            satisfaction_score=60,
            expansion_score=40,
            previous_score=65,
            score_change=-7,
            trend_direction="down",
            triggered_by="input_added",
            ai_summary="Engagement declining. Last check-in 12 days ago. Onboarding concerns raised.",
            calculated_at=datetime.utcnow()
        )
        
        health_risk = HealthScore(
            id=uuid4(), 
            account_id=churn_risk.id, 
            overall_score=25, 
            overall_status="at_risk",
            sentiment_score=20, 
            engagement_score=30, 
            request_score=40,
            relationship_score=10, 
            satisfaction_score=20, 
            expansion_score=10,
            previous_score=38,
            score_change=-13,
            trend_direction="down",
            triggered_by="decay",
            ai_summary="CRITICAL: Negative sentiment in recent emails. No response to engagement attempts in 14 days.",
            calculated_at=datetime.utcnow()
        )
        
        health_treasury = HealthScore(
            id=uuid4(),
            account_id=treasury.id,
            overall_score=72,
            overall_status="healthy",
            sentiment_score=75,
            engagement_score=80,
            request_score=65,
            relationship_score=70,
            satisfaction_score=75,
            expansion_score=60,
            previous_score=70,
            score_change=2,
            trend_direction="stable",
            triggered_by="daily_job",
            ai_summary="Federal account performing well. ATO renewal process should begin soon. Section 508 compliance review requested.",
            calculated_at=datetime.utcnow()
        )
        
        db.add_all([health_stark, health_techflow, health_risk, health_treasury])

        # ============================================================
        # 3. ADD INPUTS (Activity)
        # ============================================================
        
        inputs = [
            # Stark - Positive signals
            Input(
                id=uuid4(), 
                account_id=stark.id, 
                input_type="email", 
                sender="Tony Stark", 
                folder="Renewals",
                content="Looking forward to the renewal discussion. We want to expand to the NY office.",
                content_date=datetime.utcnow() - timedelta(days=2),
                is_processed=True
            ),
            Input(
                id=uuid4(), 
                account_id=stark.id, 
                input_type="meeting_note", 
                sender="Pepper Potts", 
                folder="Strategic",
                content="Quarterly sync went well. High interest in the new AI features.",
                content_date=datetime.utcnow() - timedelta(days=5),
                is_processed=True
            ),
            
            # Churn Risk - Negative signals
            Input(
                id=uuid4(), 
                account_id=churn_risk.id, 
                input_type="email", 
                sender="Angry Manager", 
                folder="Support",
                content="The system is too slow. We are considering other options. Leadership is frustrated.",
                content_date=datetime.utcnow() - timedelta(days=1),
                is_processed=True
            ),
            
            # TechFlow - Mixed signals
            Input(
                id=uuid4(), 
                account_id=techflow.id, 
                input_type="call", 
                sender="Sarah Jenkins", 
                folder="Onboarding",
                content="Onboarding is moving slowly but we are making progress. Some concerns about training timeline.",
                content_date=datetime.utcnow() - timedelta(days=10),
                is_processed=True
            ),
            
            # Treasury - Federal compliance signals!
            Input(
                id=uuid4(),
                account_id=treasury.id,
                input_type="email",
                sender="John Martinez (ISSO)",
                folder="Compliance",
                content="We need to discuss the upcoming ATO renewal. The current authorization expires in 45 days. Please provide updated SSP and POA&M documentation.",
                content_date=datetime.utcnow() - timedelta(days=3),
                is_processed=True
            ),
            Input(
                id=uuid4(),
                account_id=treasury.id,
                input_type="meeting_note",
                sender="Lisa Chen (Program Manager)",
                folder="Strategic",
                content="Quarterly review went well. Team requested Section 508 accessibility audit for new dashboard. FedRAMP continuous monitoring report due next month.",
                content_date=datetime.utcnow() - timedelta(days=7),
                is_processed=True
            ),
        ]
        db.add_all(inputs)

        # ============================================================
        # 4. ADD CONTRACTS (with federal compliance fields!)
        # ============================================================
        
        contracts = [
            # Stark - Standard enterprise
            Contract(
                id=uuid4(), 
                account_id=stark.id, 
                contract_name="Enterprise License",
                contract_type="renewal", 
                total_contract_value=500000.0, 
                arr=500000.0, 
                status="active", 
                effective_date=datetime.utcnow() - timedelta(days=300),
                end_date=datetime.utcnow() + timedelta(days=65)
            ),
            
            # TechFlow
            Contract(
                id=uuid4(), 
                account_id=techflow.id, 
                contract_name="Mid-Market SaaS",
                contract_type="new_business", 
                total_contract_value=50000.0, 
                arr=50000.0,
                status="active", 
                effective_date=datetime.utcnow() - timedelta(days=200),
                end_date=datetime.utcnow() + timedelta(days=165)
            ),
            
            # Churn Risk - Expiring soon!
            Contract(
                id=uuid4(), 
                account_id=churn_risk.id, 
                contract_name="SMB Starter",
                contract_type="renewal", 
                total_contract_value=15000.0, 
                arr=15000.0,
                status="active", 
                effective_date=datetime.utcnow() - timedelta(days=350),
                end_date=datetime.utcnow() + timedelta(days=15)
            ),
            
            # Treasury - FEDERAL CONTRACT with compliance fields!
            Contract(
                id=uuid4(),
                account_id=treasury.id,
                contract_name="BPA Task Order - CX Platform",
                contract_type="renewal",
                total_contract_value=1200000.0,
                arr=400000.0,
                status="active",
                effective_date=datetime.utcnow() - timedelta(days=270),
                end_date=datetime.utcnow() + timedelta(days=95),
                primary_signer="Lisa Chen",
                economic_buyer="Deputy Commissioner Office",
                # THE DIFFERENTIATOR - Federal Compliance!
                fedramp_required=True,
                fisma_level="moderate",
                hipaa_required=False,
                section_508_required=True,
                ato_status="active",
                ato_expiry_date=(datetime.utcnow() + timedelta(days=45)).date()  # Expiring soon!
            ),
        ]
        db.add_all(contracts)

        # ============================================================
        # 5. ADD CONTACTS
        # ============================================================
        
        contacts = [
            Contact(id=uuid4(), account_id=stark.id, name="Tony Stark", title="CEO", email="tony@stark.com", is_champion=True),
            Contact(id=uuid4(), account_id=stark.id, name="Pepper Potts", title="COO", email="pepper@stark.com", is_champion=False),
            Contact(id=uuid4(), account_id=treasury.id, name="John Martinez", title="ISSO", email="john.martinez@fiscal.treasury.gov", is_champion=False),
            Contact(id=uuid4(), account_id=treasury.id, name="Lisa Chen", title="Program Manager", email="lisa.chen@fiscal.treasury.gov", is_champion=True),
            Contact(id=uuid4(), account_id=churn_risk.id, name="Angry Manager", title="Director", email="manager@churnrisk.com", is_champion=False),
        ]
        db.add_all(contacts)

        db.commit()
        print("=" * 60)
        print("Demo data seeded successfully!")
        print("=" * 60)
        print(f"  Accounts: 4 (including 1 federal)")
        print(f"  Health Scores: 4 (with trend data)")
        print(f"  Inputs: 6")
        print(f"  Contracts: 4 (1 with federal compliance)")
        print(f"  Contacts: 5")
        print("")
        print("Federal compliance showcase:")
        print("  - Treasury account has FedRAMP Moderate, Section 508")
        print("  - ATO expires in 45 days (will trigger alert!)")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
