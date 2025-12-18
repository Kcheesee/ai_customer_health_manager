from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import uuid
from .base import Base

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    account_type = Column(String, nullable=False) # standard, ela_parent, ela_child
    parent_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
    account_email = Column(String, index=True)
    industry = Column(String)
    tier = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    check_in_interval_days = Column(Integer, default=14)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id])
    children = relationship("Account", backref=backref("parent", remote_side=[id]))
    health_scores = relationship("HealthScore", back_populates="account", cascade="all, delete-orphan")
    inputs = relationship("Input", back_populates="account", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="account", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="account", cascade="all, delete-orphan")
