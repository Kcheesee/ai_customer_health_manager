from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class HealthScoreResponse(BaseModel):
    id: UUID
    account_id: UUID
    overall_score: int
    overall_status: str
    sentiment_score: int
    engagement_score: int
    calculated_at: datetime
