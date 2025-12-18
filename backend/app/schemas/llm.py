from pydantic import BaseModel
from typing import Optional
from enum import Enum

class LLMProviderType(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    XAI = "xai"
    PERPLEXITY = "perplexity"
    MOCK = "mock"

class LLMConfigBase(BaseModel):
    provider: LLMProviderType
    model_name: str
    is_active: bool = False
    
class LLMConfigCreate(LLMConfigBase):
    api_key: str

class LLMConfigUpdate(BaseModel):
    provider: Optional[LLMProviderType] = None
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = None

class LLMConfigResponse(LLMConfigBase):
    api_key_masked: Optional[str] = None
    
    class Config:
        from_attributes = True
