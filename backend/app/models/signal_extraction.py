from sqlalchemy import Column, String, Boolean, Integer, Text, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class SignalExtraction(Base):
    __tablename__ = "signal_extractions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_id = Column(UUID(as_uuid=True), ForeignKey("inputs.id"), nullable=False)
    
    # Keywords
    # Keeping specific signal buckets for backward compat / keyword scanner specific
    churn_signals = Column(ARRAY(String))
    positive_signals = Column(ARRAY(String))
    keyword_severity = Column(String)
    
    # LLM
    llm_analyzed = Column(Boolean, default=False)
    llm_analysis_status = Column(String) # pending, completed, failed
    
    sentiment = Column(String) # positive, neutral, negative
    sentiment_score = Column(Integer) # -100 to 100
    
    summary = Column(Text)
    signals = Column(ARRAY(String)) # Generic extracted signals from LLM
    action_items = Column(ARRAY(String))
