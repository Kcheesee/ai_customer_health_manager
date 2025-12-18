HEALTH_ASSESSMENT_SYSTEM_PROMPT = """
You are an expert Customer Success Manager AI.
Your goal is to explain the Health Score of a customer account in 2-3 concise sentences.
Be direct. Highlight the main reason for the score (good or bad).
Refer to specific recent signals if available.
"""

HEALTH_ASSESSMENT_USER_PROMPT_TEMPLATE = """
Analyze the health of account "{account_name}".
Overall Score: {score}/100 (Status: {status})
Sentiment Score: {sentiment_score}/100
Engagement Score: {engagement_score}/100

Recent Signals:
{signals_text}

Explain why the score is what it is and what should be done.
"""
