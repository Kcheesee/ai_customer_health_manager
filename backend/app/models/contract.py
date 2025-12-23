from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, Numeric, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.models.base import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    
    contract_name = Column(String, nullable=False)
    contract_type = Column(String, nullable=False) # saas_subscription, consulting, etc.
    status = Column(String, nullable=False) # active, draft, expired
    
    # Dates
    effective_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False, index=True)
    term_length = Column(String) # annual, etc.
    auto_renewal = Column(Boolean, default=True)
    notice_period_days = Column(Integer, default=30)
    
    # Financial
    total_contract_value = Column(Numeric(15, 2))
    arr = Column(Numeric(15, 2))
    
    # Scope
    products_modules = Column(ARRAY(String))
    
    # Contacts
    primary_signer = Column(String)
    economic_buyer = Column(String)
    
    # Federal Compliance - The differentiator
    fedramp_required = Column(Boolean, default=False)
    fisma_level = Column(String, default='none')  # none, low, moderate, high
    hipaa_required = Column(Boolean, default=False)
    section_508_required = Column(Boolean, default=False)
    ato_status = Column(String, default='none')  # none, pending, active, expired
    ato_expiry_date = Column(Date, nullable=True)

    # Content
    full_text = Column(Text, nullable=True)
    document_path = Column(String, nullable=True)
    
    # Metadata
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="contracts")
