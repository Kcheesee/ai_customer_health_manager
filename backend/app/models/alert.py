from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base
import enum

class AlertType(str, enum.Enum):
    info = "info"
    warning = "warning"
    error = "error"
    success = "success"

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id")) # Optional: targeted alerts
    
    type = Column(String, default="info") # info, warning, error
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String) # Optional link to resource (e.g. /accounts/123)
    
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
