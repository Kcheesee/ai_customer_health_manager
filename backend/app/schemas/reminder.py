from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ReminderBase(BaseModel):
    description: str
    due_date: Optional[datetime] = None
    is_completed: bool = False

class ReminderCreate(ReminderBase):
    account_id: UUID
    source_input_id: Optional[UUID] = None

class ReminderUpdate(BaseModel):
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

class ReminderResponse(ReminderBase):
    id: UUID
    account_id: UUID
    source_input_id: Optional[UUID]
    created_at: datetime
    
    class Config:
        from_attributes = True
