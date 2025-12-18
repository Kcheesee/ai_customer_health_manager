
import asyncio
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timedelta
from app.services.health.calculator import HealthCalculator
from app.models.account import Account
from app.models.input import Input
from app.models.signal_extraction import SignalExtraction
from app.models.health_score import HealthScore

async def test_calculation_logic():
    print("Starting Health Intelligence Expansion Test...")
    
    # Mock DB Session
    db = MagicMock()
    
    # Mock Account
    account_id = uuid4()
    mock_account = Account(
        id=account_id,
        name="Test Corp",
        check_in_interval_days=14,
        tier="enterprise",
        account_type="standard"
    )
    
    # Mock Inputs
    mock_input = Input(
        id=uuid4(),
        account_id=account_id,
        content="We loved the new feature but have a bug request.",
        input_type="note",
        content_date=datetime.utcnow() - timedelta(days=2),
        is_processed=True
    )
    
    # Mock Extractions
    # One positive sentiment, but has "bug" and "request" signals
    mock_extraction = SignalExtraction(
        input_id=mock_input.id,
        sentiment="positive",
        signals=["bug in login", "feature request for export", "satisfied with support"]
    )
    
    # Setup DB queries
    db.query().filter().first.return_value = mock_account
    db.query().filter().order_by().limit().all.return_value = [mock_input]
    db.query().filter().all.return_value = [mock_extraction]
    db.query().filter().count.return_value = 2 # 2 contacts
    
    # Mock Assessment Generator
    calculator = HealthCalculator(db)
    calculator.assessment_gen = MagicMock()
    
    # Use AsyncMock for the awaited method
    from unittest.mock import AsyncMock
    calculator.assessment_gen.generate_summary = AsyncMock(return_value="AI Summary: Healthy but has bugs.")
    
    # Execute
    result = await calculator.calculate_health(account_id)
    
    # Verify
    print(f"Overall Score: {result.overall_score}")
    print(f"Pillar Scores:")
    print(f" - Sentiment: {result.sentiment_score}")
    print(f" - Engagement: {result.engagement_score}")
    print(f" - Requests: {result.request_score}")
    print(f" - Relationship: {result.relationship_score}")
    print(f" - Satisfaction: {result.satisfaction_score}")
    print(f" - Expansion: {result.expansion_score}")
    
    assert result.overall_score > 0
    assert result.relationship_score == 100 # 2 contacts
    assert result.request_score < 100 # penalty for bug/request
    assert result.satisfaction_score > 50 # "satisfied" signal
    
    print("Test Passed!")

if __name__ == "__main__":
    asyncio.run(test_calculation_logic())
