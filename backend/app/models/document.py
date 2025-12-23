from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base

class AccountDocument(Base):
    __tablename__ = "account_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False) # Path to stored file (or URL)
    file_type = Column(String, nullable=True)  # Mime type or extension
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    account = relationship("Account", back_populates="documents")
