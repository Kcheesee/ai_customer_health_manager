from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class Signal(BaseModel):
    topic: str
    severity: str # "high", "medium", "low"

class AnalysisResult(BaseModel):
    sentiment: str
    summary: str
    signals: List[str]
    commitments: List[Dict[str, Any]] = []
    action_items: List[str]

class InputCreate(BaseModel):
    account_id: UUID
    content: str
    input_type: str # "email", "call_notes", "chat"
    folder: Optional[str] = None
    content_date: Optional[datetime] = None
    sender: Optional[str] = None

class InputUpdate(BaseModel):
    folder: Optional[str] = None
    content: Optional[str] = None
    input_type: Optional[str] = None
    sender: Optional[str] = None

class SignalExtractionResponse(BaseModel):
    id: UUID
    input_id: UUID
    sentiment: str
    summary: str
    action_items: List[str]
    created_at: datetime
