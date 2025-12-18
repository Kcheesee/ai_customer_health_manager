from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.services.health.calculator import HealthCalculator
from app.schemas.health import HealthScoreResponse
from app.models.health_score import HealthScore

router = APIRouter()

@router.post("/accounts/{account_id}/calculate", response_model=HealthScoreResponse)
async def calculate_score(account_id: UUID, db: Session = Depends(get_db)):
    calculator = HealthCalculator(db)
    try:
        return await calculator.calculate_health(account_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/accounts/{account_id}/history", response_model=List[HealthScoreResponse])
def get_history(account_id: UUID, db: Session = Depends(get_db)):
    scores = db.query(HealthScore).filter(
        HealthScore.account_id == account_id
    ).order_by(HealthScore.calculated_at.desc()).all()
    return scores
