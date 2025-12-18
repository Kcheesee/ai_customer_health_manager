from sqlalchemy import Column, String, Integer, ForeignKey, Text, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base

class HealthScore(Base):
    __tablename__ = "health_scores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    
    overall_score = Column(Integer, nullable=False)
    overall_status = Column(String, nullable=False)
    
    # Pillars
    engagement_score = Column(Integer)
    sentiment_score = Column(Integer)
    request_score = Column(Integer)
    relationship_score = Column(Integer)
    satisfaction_score = Column(Integer)
    expansion_score = Column(Integer)
    
    ai_summary = Column(Text)
    
    calculated_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="health_scores")
