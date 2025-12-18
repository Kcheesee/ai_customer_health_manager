from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    
    name = Column(String, nullable=False)
    email = Column(String)
    title = Column(String)
    role_type = Column(String) # champion, economic_buyer, etc
    
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
