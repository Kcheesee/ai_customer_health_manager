from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base
from sqlalchemy.orm import relationship

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    source_input_id = Column(UUID(as_uuid=True), ForeignKey("inputs.id"), nullable=True)
    
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    account = relationship("Account", back_populates="reminders")
    source_input = relationship("Input", backref="reminders")
