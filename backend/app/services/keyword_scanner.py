from typing import List, Dict, Any
from pydantic import BaseModel

class KeywordMatch(BaseModel):
    keyword: str
    category: str
    severity: str # "critical", "high", "medium", "low"

class ScanResult(BaseModel):
    churn_signals: List[str] = []
    positive_signals: List[str] = []
    action_signals: List[str] = []
    compliance_signals: List[str] = []
    keyword_severity: str = "low"
    matches: List[KeywordMatch] = []

# Lexicon from Spec
CHURN_SIGNALS = {
    'critical': [
        # Direct churn indicators
        'cancel', 'cancellation', 'cancelling', 'terminate', 'termination',
        'not renewing', "won't renew", 'reconsidering',
        'take our business elsewhere', 'looking at competitors',
        'exploring options', 'evaluating alternatives',
        'end the contract', 'exit', 'off-board', 'wind down',
        'rfp for replacement', 'vendor review',
    ],
    'high': [
        # Frustration
        'frustrated', 'frustrating', 'disappointed', 'disappointing',
        'unacceptable', 'fed up', 'at wit\'s end', 'last straw',
        'deal breaker', 'non-starter',
        # Escalation
        'escalate', 'escalation', 'involve my manager', 'loop in vp',
        'bring in legal', 'c-suite', 'executive sponsor',
        'unresolved', 'still waiting', 'no response', 'ignored',
        'dropped the ball', 'this is the third time', 'yet again',
    ],
    'medium': [
        # Service issues
        'slow response', 'long wait', 'no follow-up', 'ticket still open',
        'support is terrible', "can't get help", 'nobody responds',
        'passed around', 'transferred again', 'sla breach',
        'outage', 'downtime', 'incident', 'service disruption',
        # Product gaps
        'missing feature', "doesn't have", "can't do", 'limitation',
        'workaround', 'competitor has', 'why can\'t you',
        'not intuitive', 'confusing', 'hard to use', 'clunky', 'buggy',
    ]
}

POSITIVE_SIGNALS = {
    'expansion': [
        'expand', 'expansion', 'add more', 'additional licenses',
        'more seats', 'other departments', 'other teams',
        'roll out to', 'enterprise-wide', 'new use case',
        'another project', 'phase 2', 'next phase',
        'budget approved', 'funding secured', 'ready to move forward',
        'who else should i talk to', 'introduce you to',
    ],
    'satisfaction': [
        'love', 'great', 'excellent', 'fantastic', 'amazing', 'impressed',
        'happy with', 'pleased with', 'satisfied', 'delighted',
        'exceeded expectations', 'better than expected', 'blown away',
        'exactly what we needed', 'perfect fit', 'game changer',
    ],
    'relationship': [
        'partner', 'partnership', 'strategic', 'long-term', 'trusted',
        'recommend', 'referral', 'reference', 'case study', 'testimonial',
        'renew', 'renewal', 'multi-year', 'extend', 'committed',
        'advocate', 'champion',
    ],
    'value': [
        'roi', 'return on investment', 'paying off', 'saving us',
        'efficiency', 'productivity', 'streamlined', 'automated',
        'results', 'outcomes', 'impact', 'measurable', 'metrics',
        'success', 'successful', 'working well', 'performing',
    ]
}

ACTION_SIGNALS = {
    'commitments_made': [
        "i'll send", "i'll get back", 'will follow up', 'let me check',
        'by end of week', 'by friday', 'tomorrow', 'next week',
        'circle back', 'reconnect', 'touch base', 'schedule time',
    ],
    'requests_pending': [
        'can you send', 'please provide', 'need from you', 'waiting on',
        'awaiting', 'pending your', 'action required', 'your turn',
        'please confirm', 'need approval', 'sign off needed',
    ],
    'meeting_signals': [
        'let\'s schedule', 'set up a call', 'discuss further',
        'qbr', 'business review', 'check-in', 'sync',
        'demo', 'presentation', 'walk-through', 'deep dive',
    ]
}

COMPLIANCE_SIGNALS = {
    'fedramp': ['fedramp', 'fed ramp', 'federal risk'],
    'fisma': ['fisma', 'federal information security'],
    'ato': ['ato', 'authorization to operate', 'authority to operate'],
    'hipaa': ['hipaa', 'phi', 'protected health information'],
    'section_508': ['508 compliance', 'section 508', 'accessibility', 'wcag'],
    'security': [
        'security review', 'security assessment', 'pen test',
        'penetration test', 'vulnerability', 'il4', 'il5',
        'govcloud', 'government cloud',
    ],
    'federal_process': [
        'contracting officer', 'cor', 'cotr', 'procurement',
        'task order', 'bpa', 'idiq', 'option year',
        'period of performance', 'clin', 'gsa schedule',
    ]
}

def scan_text(text: str) -> ScanResult:
    text_lower = text.lower()
    
    result = ScanResult()
    
    # helper to process category dicts
    def process_dict(signal_dict: Dict[str, List[str]], target_list: List[str], base_severity: str = None):
        for category, keywords in signal_dict.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Determine severity
                    severity = base_severity if base_severity else "low"
                    
                    # For churn signals, the category key IS the severity
                    if signal_dict is CHURN_SIGNALS:
                        severity = category
                    
                    match = KeywordMatch(
                        keyword=keyword,
                        category=category,
                        severity=severity
                    )
                    
                    result.matches.append(match)
                    target_list.append(keyword)
                    
                    # Update global severity
                    current_sev_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
                    if current_sev_rank[severity] > current_sev_rank[result.keyword_severity]:
                        result.keyword_severity = severity

    # Process all signals
    process_dict(CHURN_SIGNALS, result.churn_signals)
    process_dict(POSITIVE_SIGNALS, result.positive_signals, base_severity="low") # Positive signals don't drive severity usually, but we track them
    process_dict(ACTION_SIGNALS, result.action_signals, base_severity="medium")
    process_dict(COMPLIANCE_SIGNALS, result.compliance_signals, base_severity="high") # Compliance is important

    return result

def should_analyze_with_llm(scan_result: ScanResult) -> bool:
    """
    Determine if LLM analysis is warranted based on keyword scan.
    """
    # Always analyze if critical/high severity
    if scan_result.keyword_severity in ['critical', 'high']:
        return True
    
    # Analyze if significant signal count
    total_signals = (
        len(scan_result.churn_signals) +
        len(scan_result.positive_signals) +
        len(scan_result.action_signals)
    )
    if total_signals >= 3:
        return True
    
    # Analyze if compliance signals (important context)
    if scan_result.compliance_signals:
        return True
    
    return False
