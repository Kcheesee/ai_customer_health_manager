import sys
import os
import asyncio
from uuid import uuid4
from datetime import datetime

# Add validation to ensure we're in the right directory or path added
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import AsyncMock, patch
from app.core.database import SessionLocal
from app.services.intelligence import IntelligenceService
from app.schemas.intelligence import InputCreate, AnalysisResult
from app.models.account import Account
from scripts.seed_demo import seed_demo

# Mock result to return when LLM analysis is triggered
MOCK_LLM_RESULT = AnalysisResult(
    sentiment="negative", # triggered by 'terminate'
    summary="User is considering termination due to lack of FedRAMP support.",
    signals=["churn_risk", "compliance_gap"],
    action_items=["Schedule call", "Check FedRAMP status"],
    commitments=[]
)

async def run_demo():
    print("--- 1. Seeding Database ---")
    # Reset/Init DB if needed, but for now we just seed
    # Assuming tables exist or we might need to run migrations/create_db
    # We'll rely on seed_demo to fail if tables are missing, which implies we might need to run create_tables first if this was a fresh env.
    # But seed_demo uses models which usually requires tables.
    # Let's try just running seed_demo.
    try:
        seed_demo()
    except Exception as e:
        print(f"Seeding failed (maybe data exists or tables missing): {e}")
    
    db = SessionLocal()
    try:
        print("\n--- 2. Fetching an Account ---")
        # Get the 'Stark Industries' account or any
        account = db.query(Account).first()
        if not account:
            print("No accounts found! Seeding must have failed.")
            return

        print(f"Using Account: {account.name} ({account.id})")
        
        service = IntelligenceService(db)
        
        print("\n--- 3. Processing Input with NEW Lexicon ---")
        # Test Input: Contains Churn ("terminate"), Compliance ("FedRAMP"), and Action ("schedule a call")
        content = "We are considering to terminate the contract if we don't get FedRAMP support. Let's schedule a call to discuss."
        
        print(f"Input Content: \"{content}\"")
        
        input_data = InputCreate(
            account_id=account.id,
            content=content,
            input_type="email",
            sender="Demo User",
            content_date=datetime.now()
        )
        
        # Helper to mock the LLM if we don't have keys, but the scanner runs BEFORE LLM.
        # IntelligenceService process_input calls scanner first.
        # If LLM is triggered (which it will be due to 'terminate'), it tries to call LLM.
        # We need to make sure we don't crash if LLM fails or is missing keys.
        # The service catches LLM errors usually.
        
        # Patch the LLM analysis to avoid encryption errors and API calls
        with patch.object(service, '_run_llm_analysis', new=AsyncMock(return_value=MOCK_LLM_RESULT)):
            extraction = await service.process_input(input_data)
        
        if extraction:
            print("\n--- 4. Extraction Results ---")
            print(f"Input ID: {extraction.input_id}")
            print(f"Churn Signals: {extraction.churn_signals}")
            print(f"Compliance Signals: {extraction.compliance_signals}")
            print(f"Action Signals: {extraction.action_signals}")
            print(f"Severity: {extraction.keyword_severity}")
            print(f"LLM Status: {extraction.llm_analysis_status}")
            
            # Verify specific signals
            if "terminate" in (extraction.churn_signals or []):
                print("SUCCESS: Detected 'terminate' as churn signal.")
            else:
                print("FAILURE: Did not detect 'terminate'.")
                
            if "fedramp" in (extraction.compliance_signals or []):
                print("SUCCESS: Detected 'fedramp' as compliance signal.")
            else:
                print("FAILURE: Did not detect 'fedramp'.")

        else:
            print("No extraction created (maybe LLM skipped?)")
            
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(run_demo())
