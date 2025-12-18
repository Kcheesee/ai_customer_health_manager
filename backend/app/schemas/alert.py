from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class AlertBase(BaseModel):
    type: str # info, warning, error
    title: str
    message: str
    link: Optional[str] = None
    is_read: bool = False

class AlertCreate(AlertBase):
    user_id: Optional[UUID] = None

class AlertResponse(AlertBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
