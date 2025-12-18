from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, AlertCreate

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
def get_alerts(unread_only: bool = False, db: Session = Depends(get_db)):
    # In a real app, filtering by current_user.id would be here.
    # For MVP, we'll return all alerts or maybe filter if we had a user context.
    # Assuming single tenant / shared alerts for now or just fetching all.
    
    query = db.query(Alert).order_by(Alert.created_at.desc())
    
    if unread_only:
        query = query.filter(Alert.is_read == False)
        
    return query.all()

@router.put("/{alert_id}/read", response_model=AlertResponse)
def mark_alert_read(alert_id: UUID, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    alert.is_read = True
    db.commit()
    db.refresh(alert)
    return alert

@router.put("/read-all")
def mark_all_read(db: Session = Depends(get_db)):
    db.query(Alert).filter(Alert.is_read == False).update({"is_read": True})
    db.commit()
    return {"status": "success"}
