from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderResponse, ReminderCreate, ReminderUpdate

router = APIRouter()

@router.get("/", response_model=List[ReminderResponse])
def get_reminders(account_id: UUID = None, db: Session = Depends(get_db)):
    query = db.query(Reminder)
    if account_id:
        query = query.filter(Reminder.account_id == account_id)
    return query.order_by(Reminder.due_date.asc(), Reminder.created_at.desc()).all()

@router.post("/", response_model=ReminderResponse)
def create_reminder(reminder_in: ReminderCreate, db: Session = Depends(get_db)):
    reminder = Reminder(
        account_id=reminder_in.account_id,
        source_input_id=reminder_in.source_input_id,
        description=reminder_in.description,
        due_date=reminder_in.due_date,
        is_completed=reminder_in.is_completed
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(reminder_id: UUID, reminder_in: ReminderUpdate, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
        
    if reminder_in.description is not None:
        reminder.description = reminder_in.description
    if reminder_in.due_date is not None:
        reminder.due_date = reminder_in.due_date
    if reminder_in.is_completed is not None:
        reminder.is_completed = reminder_in.is_completed
        
    db.commit()
    db.refresh(reminder)
    return reminder

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
        
    db.delete(reminder)
    db.commit()
    return {"status": "success"}
