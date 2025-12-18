from sqlalchemy import Column, String, Boolean, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base

class Input(Base):
    __tablename__ = "inputs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    input_type = Column(String, nullable=False) # email, meeting_note, etc
    
    subject = Column(String)
    content = Column(Text, nullable=False)
    content_date = Column(DateTime)
    
    # Contact specific
    sender = Column(String)
    recipients = Column(ARRAY(String))
    
    folder = Column(String) # For organization
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="inputs")
