from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.llm_config import LLMConfiguration
from app.schemas.llm import LLMConfigResponse, LLMConfigUpdate
from app.core.security import encrypt_string, decrypt_string
from app.services.llm.factory import LLMClientFactory
from typing import Dict, Any

router = APIRouter()

@router.get("/", response_model=LLMConfigResponse)
def get_llm_config(db: Session = Depends(get_db)):
    config = db.query(LLMConfiguration).filter(LLMConfiguration.is_active == True).first()
    if not config:
        # Return default or empty
        return {
            "provider": "mock",
            "model_name": "mock-model",
            "is_active": False,
            "api_key_masked": None
        }
    
    # Mask Key
    masked = "********"
    if config.api_key_encrypted:
        try:
            # We don't need to decrypt to mask, just show it exists
            masked = "********" + config.api_key_encrypted[-4:] if len(config.api_key_encrypted) > 4 else "********"
            # Actually, reusing the encrypted string last 4 chars is bad practice visually, 
            # usually we decrypt and show last 4 of actual key, but for security simply returning "********" is safest.
            # Let's decrypt to get last 4 chars if we want to be fancy, or just return specific string.
            # Showing last 4 of actual key is useful.
            real_key = decrypt_string(config.api_key_encrypted)
            if real_key and len(real_key) > 4:
                masked = "..." + real_key[-4:]
            else:
                masked = "********"
        except:
            masked = "Error/Invalid"

    return LLMConfigResponse(
        provider=config.provider,
        model_name=config.model_name,
        is_active=config.is_active,
        api_key_masked=masked
    )

@router.put("/", response_model=LLMConfigResponse)
def update_llm_config(config_in: LLMConfigUpdate, db: Session = Depends(get_db)):
    # Simple logic: we only support one active config for now.
    # Upsert logic.
    config = db.query(LLMConfiguration).first()
    
    if not config:
        config = LLMConfiguration()
        db.add(config)
    
    if config_in.provider:
        config.provider = config_in.provider
    if config_in.model_name:
        config.model_name = config_in.model_name
    if config_in.api_key:
        config.api_key_encrypted = encrypt_string(config_in.api_key)
    if config_in.is_active is not None:
        config.is_active = config_in.is_active
    else:
        config.is_active = True # Default to active on save
        
    db.commit()
    db.refresh(config)
    
    # Mask for response
    real_key = decrypt_string(config.api_key_encrypted)
    masked = "..." + real_key[-4:] if real_key and len(real_key) > 4 else "********"

    return LLMConfigResponse(
        provider=config.provider,
        model_name=config.model_name,
        is_active=config.is_active,
        api_key_masked=masked
    )

@router.post("/test")
async def test_llm_config(config_in: LLMConfigUpdate, db: Session = Depends(get_db)):
    """
    Test a configuration without saving it, or test existing if fields are empty.
    """
    provider = config_in.provider
    model = config_in.model_name
    api_key = config_in.api_key
    
    # If not provided, try to use saved
    if not api_key:
        saved_config = db.query(LLMConfiguration).first()
        if saved_config:
             api_key = decrypt_string(saved_config.api_key_encrypted)
             if not provider: provider = saved_config.provider
             if not model: model = saved_config.model_name
        else:
            raise HTTPException(status_code=400, detail="No API key provided and no configuration saved.")
            
    if not provider or not api_key:
         raise HTTPException(status_code=400, detail="Provider and API Key required.")

    try:
        # Instantiate provider via Factory
        client = LLMClientFactory.create(provider, api_key, model or "default")
        
        # Simple test generation
        # We need a generic test method or just use generate_text
        response = await client.generate_text("Say 'Hello World'", system_prompt="You are a test bot.")
        return {"status": "success", "response": response}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Connection failed: {str(e)}")
