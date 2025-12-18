from typing import List, Dict, Tuple
from pydantic import BaseModel

class KeywordMatch(BaseModel):
    keyword: str
    category: str
    severity: str # "high", "medium", "low"

# Lexicon from Spec
KEYWORD_LEXICON = {
    "churn_signals": {
        "cancel": "high",
        "terminate": "high",
        "competitor": "medium",
        "too expensive": "medium",
        "budget cut": "high",
        "switching": "high",
        "unhappy": "medium",
        "hate": "high",
        "crash": "high",
        "feature missing": "low"
    },
    "positive_signals": {
        "love": "low",
        "great": "low",
        "expand": "high",
        "upgrade": "high",
        "recommend": "medium"
    },
    "action_required": {
        "schedule a call": "medium",
        "help needed": "medium",
        "urgent": "high",
        "error": "medium",
        "bug": "medium"
    }
}

def scan_text(text: str) -> List[KeywordMatch]:
    matches = []
    text_lower = text.lower()
    
    for category, keywords in KEYWORD_LEXICON.items():
        for keyword, severity in keywords.items():
            if keyword in text_lower:
                matches.append(KeywordMatch(
                    keyword=keyword, 
                    category=category, 
                    severity=severity
                ))
    return matches

def should_analyze_with_llm(matches: List[KeywordMatch]) -> bool:
    """
    Determine if text requires LLM analysis based on keyword severity.
    Rule: Analyze if ANY 'high' severity signal is found, or > 2 'medium' signals.
    """
    high_count = sum(1 for m in matches if m.severity == "high")
    medium_count = sum(1 for m in matches if m.severity == "medium")
    
    if high_count > 0:
        return True
    if medium_count > 2:
        return True
    return False
