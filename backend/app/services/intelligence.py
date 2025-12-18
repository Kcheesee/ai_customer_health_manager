import json
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models.input import Input
from app.models.signal_extraction import SignalExtraction
from app.models.llm_config import LLMConfiguration
from app.schemas.intelligence import InputCreate, AnalysisResult
from app.services.keyword_scanner import scan_text, should_analyze_with_llm
from app.services.llm.factory import LLMClientFactory
from app.core.security import decrypt_string
from app.core.prompts import SIGNAL_EXTRACTION_SYSTEM_PROMPT, SIGNAL_EXTRACTION_USER_PROMPT_TEMPLATE

class IntelligenceService:
    def __init__(self, db: Session):
        self.db = db

    async def process_input(self, input_data: InputCreate) -> SignalExtraction:
        # 1. Save Input to DB
        db_input = Input(
            account_id=input_data.account_id,
            input_type=input_data.input_type,
            content=input_data.content,
            sender=input_data.sender,
            content_date=input_data.content_date or datetime.now(),
            is_processed=False
        )
        self.db.add(db_input)
        self.db.commit()
        self.db.refresh(db_input)

        # 2. Keyword Scan
        matches = scan_text(input_data.content)
        
        # 3. Determine if LLM Analysis is needed
        if should_analyze_with_llm(matches):
            print(f"Triggering LLM analysis for input {db_input.id}")
            analysis = await self._run_llm_analysis(input_data)
            
            # 4. Save Extraction
            extraction = SignalExtraction(
                input_id=db_input.id,
                sentiment=analysis.sentiment,
                summary=analysis.summary,
                signals=analysis.signals, # SQLAlchemy/Postgres ARRAY
                action_items=analysis.action_items,
                llm_analysis_status="completed"
            )
            self.db.add(extraction)
            
            # 5. Create Reminders from Commitments
            from app.models.reminder import Reminder
            
            for commitment in analysis.commitments:
                desc = commitment.get("description")
                date_str = commitment.get("due_date")
                due_date = None
                if date_str:
                    try:
                        due_date = datetime.strptime(date_str, "%Y-%m-%d")
                    except ValueError:
                        pass # Keep none if invalid format
                
                if desc:
                    reminder = Reminder(
                        account_id=input_data.account_id,
                        source_input_id=db_input.id,
                        description=desc,
                        due_date=due_date,
                        is_completed=False
                    )
                    self.db.add(reminder)
                    print(f"Created reminder for input {db_input.id}: {desc}")
            
            # Update Input status
            db_input.is_processed = True
            self.db.commit()
            self.db.refresh(extraction)
            return extraction
        else:
            print(f"Skipping LLM analysis for input {db_input.id} (not enough signals)")
            # No status update needed if skipped, or maybe add a skipped flag later
            db_input.is_processed = True # Mark processed even if skipped
            self.db.commit()
            return None

    async def _run_llm_analysis(self, input_data: InputCreate) -> AnalysisResult:
        # Fetch active config
        config = self.db.query(LLMConfiguration).filter(LLMConfiguration.is_active == True).first()
        if not config:
            raise ValueError("No active LLM configuration found")

        # Decrypt key
        api_key = decrypt_string(config.api_key_encrypted)
        
        # Instantiate provider
        llm = LLMClientFactory.create(config.provider, api_key, config.model_name)
        
        # Prepare Prompt
        from app.models.account import Account
        account = self.db.query(Account).filter(Account.id == input_data.account_id).first()
        account_name = account.name if account else "Unknown"

        prompt = SIGNAL_EXTRACTION_USER_PROMPT_TEMPLATE.format(
            account_name=account_name,
            content=input_data.content,
            date=input_data.content_date or datetime.now(),
            sender=input_data.sender
        )
        
        # Generate
        response_text = await llm.generate_text(prompt, system_prompt=SIGNAL_EXTRACTION_SYSTEM_PROMPT)
        
        # Parse JSON (Naive implementation for now)
        # TODO: Add robustness / retry logic for JSON parsing
        try:
            # Strip potential markdown code blocks ```json ... ```
            cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned_text)
            
            return AnalysisResult(
                sentiment=data.get("sentiment", "neutral"),
                summary=data.get("summary", ""),
                signals=data.get("signals", []),
                commitments=data.get("commitments", []),
                action_items=data.get("action_items", [])
            )
        except json.JSONDecodeError:
            print(f"Failed to parse LLM response: {response_text}")
            # Fallback
            return AnalysisResult(
                sentiment="neutral",
                summary="Failed to parse analysis results.",
                signals=[],
                action_items=[]
            )
