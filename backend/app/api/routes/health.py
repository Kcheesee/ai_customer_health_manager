from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.services.health.calculator import HealthCalculator
from app.schemas.health import HealthScoreResponse, HealthScoreHistoryItem
from app.models.health_score import HealthScore

router = APIRouter()


@router.post("/accounts/{account_id}/calculate", response_model=HealthScoreResponse)
async def calculate_score(account_id: UUID, db: Session = Depends(get_db)):
    """
    Manually trigger health score recalculation for an account.
    """
    calculator = HealthCalculator(db)
    try:
        return await calculator.calculate_health(account_id, triggered_by="manual")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accounts/{account_id}/latest", response_model=HealthScoreResponse)
def get_latest_score(account_id: UUID, db: Session = Depends(get_db)):
    """
    Get the most recent health score for an account.
    """
    score = db.query(HealthScore).filter(
        HealthScore.account_id == account_id
    ).order_by(HealthScore.calculated_at.desc()).first()
    
    if not score:
        raise HTTPException(status_code=404, detail="No health score found for this account")
    
    return score


@router.get("/accounts/{account_id}/history", response_model=List[HealthScoreHistoryItem])
def get_history(account_id: UUID, limit: int = 30, db: Session = Depends(get_db)):
    """
    Get health score history for an account.
    Useful for trend charts and timeline views.
    """
    scores = db.query(HealthScore).filter(
        HealthScore.account_id == account_id
    ).order_by(HealthScore.calculated_at.desc()).limit(limit).all()
    
    return scores
