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
    """
    Processes customer inputs through keyword scanning and LLM analysis.
    Now triggers health recalculation after processing!
    """
    
    def __init__(self, db: Session):
        self.db = db

    async def process_input(self, input_data: InputCreate, auto_recalculate_health: bool = True) -> SignalExtraction:
        """
        Process a new input through the intelligence pipeline.
        
        1. Save input to DB
        2. Run keyword scan
        3. If warranted, run LLM analysis
        4. Extract commitments → create reminders
        5. Optionally trigger health recalculation
        """
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

        # 2. Keyword Scan (free, fast)
        scan_result = scan_text(input_data.content)
        
        extraction = None
        
        # 3. Determine if LLM Analysis is needed
        if should_analyze_with_llm(scan_result):
            print(f"Triggering LLM analysis for input {db_input.id}")
            analysis = await self._run_llm_analysis(input_data)
            
            # 4. Save Extraction with both keyword and LLM results
            extraction = SignalExtraction(
                input_id=db_input.id,
                # Keyword results
                churn_signals=scan_result.churn_signals,
                positive_signals=scan_result.positive_signals,
                action_signals=scan_result.action_signals,
                compliance_signals=scan_result.compliance_signals,
                keyword_severity=scan_result.keyword_severity,
                # LLM results
                sentiment=analysis.sentiment,
                summary=analysis.summary,
                signals=analysis.signals,
                action_items=analysis.action_items,
                llm_analyzed=True,
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
                        pass
                
                if desc:
                    reminder = Reminder(
                        account_id=input_data.account_id,
                        source_input_id=db_input.id,
                        description=desc,
                        due_date=due_date,
                        is_completed=False
                    )
                    self.db.add(reminder)
                    print(f"Created reminder: {desc}")
            
            db_input.is_processed = True
            self.db.commit()
            self.db.refresh(extraction)
            
        else:
            print(f"Skipping LLM analysis for input {db_input.id} (low severity)")
            
            # Still save keyword-only extraction if we found anything
            if scan_result.matches:
                extraction = SignalExtraction(
                    input_id=db_input.id,
                    churn_signals=scan_result.churn_signals,
                    positive_signals=scan_result.positive_signals,
                    action_signals=scan_result.action_signals,
                    compliance_signals=scan_result.compliance_signals,
                    keyword_severity=scan_result.keyword_severity,
                    llm_analyzed=False,
                    llm_analysis_status="skipped"
                )
                self.db.add(extraction)
            
            db_input.is_processed = True
            self.db.commit()

        # 6. Trigger Health Recalculation
        if auto_recalculate_health:
            await self._recalculate_account_health(input_data.account_id)

        return extraction

    async def _recalculate_account_health(self, account_id: UUID):
        """
        Trigger health score recalculation after new input is processed.
        """
        try:
            from app.services.health.calculator import HealthCalculator
            calculator = HealthCalculator(self.db)
            score = await calculator.calculate_health(
                account_id, 
                triggered_by="input_added"
            )
            print(f"Health recalculated: {score.overall_score} ({score.trend_direction})")
        except Exception as e:
            print(f"Failed to recalculate health: {e}")
            # Don't fail the whole input processing if health calc fails

    async def _run_llm_analysis(self, input_data: InputCreate) -> AnalysisResult:
        """Run LLM analysis on the input content."""
        # Fetch active config
        config = self.db.query(LLMConfiguration).filter(
            LLMConfiguration.is_active == True
        ).first()
        
        if not config:
            raise ValueError("No active LLM configuration found")

        # Decrypt key
        api_key = decrypt_string(config.api_key_encrypted)
        
        # Instantiate provider
        llm = LLMClientFactory.create(config.provider, api_key, config.model_name)
        
        # Prepare Prompt
        from app.models.account import Account
        account = self.db.query(Account).filter(
            Account.id == input_data.account_id
        ).first()
        account_name = account.name if account else "Unknown"

        prompt = SIGNAL_EXTRACTION_USER_PROMPT_TEMPLATE.format(
            account_name=account_name,
            content=input_data.content,
            date=input_data.content_date or datetime.now(),
            sender=input_data.sender
        )
        
        # Generate
        response_text = await llm.generate_text(
            prompt, 
            system_prompt=SIGNAL_EXTRACTION_SYSTEM_PROMPT
        )
        
        # Parse JSON
        try:
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
            return AnalysisResult(
                sentiment="neutral",
                summary="Failed to parse analysis results.",
                signals=[],
                action_items=[]
            )
