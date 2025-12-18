from typing import List
from sqlalchemy.orm import Session
from app.models.llm_config import LLMConfiguration
from app.core.security import decrypt_string
from app.services.llm.factory import LLMClientFactory
from app.core.prompts_health import HEALTH_ASSESSMENT_SYSTEM_PROMPT, HEALTH_ASSESSMENT_USER_PROMPT_TEMPLATE

class HealthAssessmentGenerator:
    def __init__(self, db: Session):
        self.db = db

    async def generate_summary(self, account_name: str, score: int, status: str, 
                               sentiment: int, engagement: int, signals: List[str]) -> str:
        
        # 1. Get Active Provider
        config = self.db.query(LLMConfiguration).filter(LLMConfiguration.is_active == True).first()
        if not config:
            return "AI Analysis unavailable (No active LLM provider)."

        try:
            # 2. Setup Client
            api_key = decrypt_string(config.api_key_encrypted)
            llm = LLMClientFactory.create(config.provider, api_key, config.model_name)
            
            # 3. Format Signals
            signals_text = "\n".join([f"- {s}" for s in signals]) if signals else "No specific signals found."
            
            # 4. Prompt
            prompt = HEALTH_ASSESSMENT_USER_PROMPT_TEMPLATE.format(
                account_name=account_name,
                score=score,
                status=status,
                sentiment_score=sentiment,
                engagement_score=engagement,
                signals_text=signals_text
            )
            
            # 5. Generate
            summary = await llm.generate_text(prompt, system_prompt=HEALTH_ASSESSMENT_SYSTEM_PROMPT)
            return summary.strip()
            
        except Exception as e:
            print(f"Error generating assessment: {e}")
            return "AI Analysis failed due to technical error."
