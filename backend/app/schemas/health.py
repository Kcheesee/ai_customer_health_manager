from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class HealthScoreResponse(BaseModel):
    """Response schema for health scores with full pillar breakdown and trend data."""
    id: UUID
    account_id: UUID
    
    # Overall
    overall_score: int
    overall_status: str  # healthy, warning, at_risk
    
    # Pillar breakdown
    sentiment_score: Optional[int] = None
    engagement_score: Optional[int] = None
    request_score: Optional[int] = None
    relationship_score: Optional[int] = None
    satisfaction_score: Optional[int] = None
    expansion_score: Optional[int] = None
    
    # AI-generated explanation
    ai_summary: Optional[str] = None
    
    # Trend tracking
    previous_score: Optional[int] = None
    score_change: Optional[int] = None  # +5, -12, etc.
    trend_direction: Optional[str] = None  # up, down, stable, new
    triggered_by: Optional[str] = None  # manual, input_added, daily_job, decay
    
    calculated_at: datetime

    class Config:
        from_attributes = True


class HealthScoreHistoryItem(BaseModel):
    """Simplified schema for health score history/timeline."""
    overall_score: int
    overall_status: str
    score_change: Optional[int] = None
    trend_direction: Optional[str] = None
    triggered_by: Optional[str] = None
    calculated_at: datetime

    class Config:
        from_attributes = True
