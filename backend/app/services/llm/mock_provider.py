from typing import Dict, Any
from .base import LLMProvider
import json

class MockProvider(LLMProvider):
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        # Check if looking for JSON (Signal Extraction)
        if "Return a JSON object" in prompt or "Signal Extraction" in str(system_prompt):
            return json.dumps({
                "sentiment": "negative",
                "summary": "Customer is threatening to cancel due to price.",
                "signals": ["churn_risk", "pricing_complaint"],
                "commitments": [{"description": "Send updated contract", "due_date": "2025-12-25"}],
                "action_items": ["Schedule renewal review", "Discuss discount options"]
            })
        
        # Otherwise, return text (Health Assessment)
        return "This account is at risk due to recent churn signals. Sentiment is negative despite engagement. Immediate intervention required."

    async def analyze_health(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"mock": "data"}

    def count_tokens(self, text: str) -> int:
        return 10
