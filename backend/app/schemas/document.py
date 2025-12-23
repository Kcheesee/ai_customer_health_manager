from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class DocumentBase(BaseModel):
    name: str

class DocumentCreate(DocumentBase):
    account_id: UUID
    file_path: str
    file_type: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: UUID
    account_id: UUID
    file_path: str
    file_type: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
