from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any

from app.core.database import get_db
from app.models.account import Account
from app.models.health_score import HealthScore

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. Total Accounts
    total_accounts = db.query(Account).filter(Account.is_active == True).count()
    
    # 2. Latest Health Scores Logic
    # Complex query to get latest score for each account
    # For MVP: Iterate active accounts and get latest score. 
    # Not performant for 10k accounts, but fine for <100.
    
    accounts = db.query(Account).filter(Account.is_active == True).all()
    
    healthy_count = 0
    warning_count = 0
    risk_count = 0
    total_score_sum = 0
    scored_accounts_count = 0
    
    dist = {"healthy": 0, "warning": 0, "at_risk": 0}
    
    for acc in accounts:
        # Get latest score
        latest = db.query(HealthScore).filter(
            HealthScore.account_id == acc.id
        ).order_by(desc(HealthScore.calculated_at)).first()
        
        if latest:
            dist[latest.overall_status] += 1
            total_score_sum += latest.overall_score
            scored_accounts_count += 1
        else:
            # Assume healthy or unknown? Let's generic count as unknown? 
            # Or just ignore for distribution.
            pass
            
    # 3. Upcoming Renewals Logic
    # Contracts ending in next 90 days
    from app.models.contract import Contract
    from datetime import datetime, timedelta
    
    today = datetime.utcnow().date()
    ninety_days = today + timedelta(days=90)
    
    upcoming_renewals = db.query(Contract).join(Account).filter(
        Contract.end_date >= today,
        Contract.end_date <= ninety_days,
        Contract.status == "active"
    ).order_by(Contract.end_date).limit(5).all()
    
    renewals_data = []
    total_arr_at_risk = 0
    
    for contract in upcoming_renewals:
        renewals_data.append({
            "id": contract.id,
            "account_name": contract.account.name,
            "contract_name": contract.contract_name,
            "end_date": contract.end_date,
            "arr": contract.arr
        })
        if contract.arr:
            total_arr_at_risk += contract.arr

    avg_score = int(total_score_sum / scored_accounts_count) if scored_accounts_count > 0 else 0
    
    return {
        "total_accounts": total_accounts,
        "health_distribution": dist,
        "average_score": avg_score,
        "upcoming_renewals": renewals_data,
        "arr_at_risk": total_arr_at_risk
    }

@router.get("/risky", response_model=List[Dict[str, Any]])
def get_risky_accounts(db: Session = Depends(get_db)):
    # Find accounts where latest score is 'at_risk' or 'warning'
    # Again, MVP loop approach
    
    accounts = db.query(Account).filter(Account.is_active == True).all()
    risky_list = []
    
    for acc in accounts:
        latest = db.query(HealthScore).filter(
            HealthScore.account_id == acc.id
        ).order_by(desc(HealthScore.calculated_at)).first()
        
        if latest and latest.overall_score < 70:
            risky_list.append({
                "id": acc.id,
                "name": acc.name,
                "tier": acc.tier,
                "score": latest.overall_score,
                "status": latest.overall_status,
                "last_updated": latest.calculated_at
            })
            
    # Sort by score ascending (lowest first)
    risky_list.sort(key=lambda x: x["score"])
    
    return risky_list[:5]

@router.post("/trigger-daily-job")
async def trigger_daily_job(db: Session = Depends(get_db)):
    from app.core.scheduler import run_daily_health_check
    await run_daily_health_check()
    return {"status": "job_triggered"}
