from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import SessionLocal
from app.models.account import Account
from app.models.alert import Alert
from app.models.contract import Contract
from app.services.health.calculator import HealthCalculator
from datetime import timedelta

scheduler = AsyncIOScheduler()

async def run_daily_health_check():
    print(f"[{datetime.utcnow()}] Starting Daily Health Check...")
    db: Session = SessionLocal()
    try:
        # Get all active accounts
        accounts = db.query(Account).filter(Account.is_active == True).all()
        calculator = HealthCalculator(db)
        
        for acc in accounts:
            try:
                # 1. Update Health
                score = await calculator.calculate_health(acc.id)
                print(f"Updated health for {acc.name}: {score.overall_score}")
                
                # 2. Check for Health Alerts
                if score.overall_score < 50:
                    # Check for existing unread alert to avoid spam
                    existing = db.query(Alert).filter(
                        Alert.title == f"Health Risk: {acc.name}",
                        Alert.is_read == False
                    ).first()
                    
                    if not existing:
                        alert = Alert(
                            type="error",
                            title=f"Health Risk: {acc.name}",
                            message=f"Health score dropped to {score.overall_score}. Immediate attention required.",
                            link=f"/accounts/{acc.id}"
                        )
                        db.add(alert)
                        print(f"Created health alert for {acc.name}")

                # 3. Check for Contract Renewals
                # Normalize today
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
                            link=f"/accounts/{acc.id}" # Ideally deep link to contracts tab
                        )
                         db.add(alert)
                         print(f"Created contract alert for {acc.name}")
                         
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
    # Run every day at midnight (UTC)
    scheduler.add_job(
        run_daily_health_check, 
        CronTrigger(hour=0, minute=0),
        id="daily_health_check",
        replace_existing=True
    )
    scheduler.start()
    print("Background Scheduler Started.")
