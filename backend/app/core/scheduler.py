from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import SessionLocal
from app.models.account import Account
from app.models.alert import Alert
from app.models.contract import Contract
from app.services.health.calculator import HealthCalculator

scheduler = AsyncIOScheduler()


async def run_daily_health_check():
    """
    Daily job that:
    1. Recalculates health scores for all accounts (with decay)
    2. Creates alerts for at-risk accounts
    3. Creates alerts for expiring contracts
    4. Creates alerts for expiring ATOs (federal compliance!)
    """
    print(f"[{datetime.utcnow()}] Starting Daily Health Check...")
    db: Session = SessionLocal()
    try:
        accounts = db.query(Account).filter(Account.is_active == True).all()
        calculator = HealthCalculator(db)
        
        for acc in accounts:
            try:
                # 1. Update Health Score (with triggered_by for tracking)
                score = await calculator.calculate_health(
                    acc.id, 
                    triggered_by="daily_job"
                )
                print(f"Updated health for {acc.name}: {score.overall_score} ({score.trend_direction})")
                
                # 2. Health Risk Alert
                if score.overall_score < 50:
                    existing = db.query(Alert).filter(
                        Alert.title == f"Health Risk: {acc.name}",
                        Alert.is_read == False
                    ).first()
                    
                    if not existing:
                        # Include trend info in the message
                        trend_msg = ""
                        if score.score_change and score.score_change < 0:
                            trend_msg = f" (down {abs(score.score_change)} points)"
                        
                        alert = Alert(
                            type="error",
                            title=f"Health Risk: {acc.name}",
                            message=f"Health score at {score.overall_score}{trend_msg}. Immediate attention required.",
                            link=f"/accounts/{acc.id}"
                        )
                        db.add(alert)
                        print(f"Created health alert for {acc.name}")

                # 3. Contract Renewal Alerts
                today = datetime.utcnow().date()
                thirty_days = today + timedelta(days=30)
                
                expiring_contracts = db.query(Contract).filter(
                    Contract.account_id == acc.id,
                    Contract.status == "active",
                    Contract.end_date >= today,
                    Contract.end_date <= thirty_days
                ).all()
                
                for contract in expiring_contracts:
                    days_left = (contract.end_date - today).days
                    alert_title = f"Renewal Due: {acc.name}"
                    
                    existing = db.query(Alert).filter(
                        Alert.title == alert_title,
                        Alert.message.contains(contract.contract_name),
                        Alert.is_read == False
                    ).first()
                    
                    if not existing:
                        alert = Alert(
                            type="warning",
                            title=alert_title,
                            message=f"Contract '{contract.contract_name}' expires in {days_left} days.",
                            link=f"/accounts/{acc.id}"
                        )
                        db.add(alert)
                        print(f"Created contract alert for {acc.name}")
                
                # 4. ATO Expiry Alerts (Federal Compliance - YOUR DIFFERENTIATOR!)
                ato_contracts = db.query(Contract).filter(
                    Contract.account_id == acc.id,
                    Contract.status == "active",
                    Contract.ato_status == "active",
                    Contract.ato_expiry_date != None,
                    Contract.ato_expiry_date >= today,
                    Contract.ato_expiry_date <= today + timedelta(days=60)  # 60 day warning for ATOs
                ).all()
                
                for contract in ato_contracts:
                    days_left = (contract.ato_expiry_date - today).days
                    alert_title = f"ATO Expiring: {acc.name}"
                    
                    existing = db.query(Alert).filter(
                        Alert.title == alert_title,
                        Alert.is_read == False
                    ).first()
                    
                    if not existing:
                        alert = Alert(
                            type="error",  # ATOs are critical
                            title=alert_title,
                            message=f"Authorization to Operate expires in {days_left} days. Renewal process typically takes 3-6 months.",
                            link=f"/accounts/{acc.id}"
                        )
                        db.add(alert)
                        print(f"Created ATO alert for {acc.name}")
                         
                db.commit()

            except Exception as e:
                print(f"Failed to process {acc.name}: {e}")
                db.rollback()
                
    except Exception as e:
        print(f"Daily Health Check Failed: {e}")
    finally:
        db.close()
    print(f"[{datetime.utcnow()}] Daily Health Check Complete.")


def start_scheduler():
    """Start the background job scheduler."""
    scheduler.add_job(
        run_daily_health_check, 
        CronTrigger(hour=0, minute=0),  # Midnight UTC
        id="daily_health_check",
        replace_existing=True
    )
    scheduler.start()
    print("Background Scheduler Started.")
