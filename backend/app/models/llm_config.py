from sqlalchemy import Column, String, Boolean
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.schemas.llm import LLMProviderType

class LLMConfiguration(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider = Column(String, index=True)
    model_name = Column(String)
    api_key_encrypted = Column(String)
    is_active = Column(Boolean, default=False)
