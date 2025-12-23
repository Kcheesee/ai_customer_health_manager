from typing import Optional, Tuple, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import UUID
from datetime import datetime, timedelta

from app.models.account import Account
from app.models.health_score import HealthScore
from app.models.input import Input
from app.models.signal_extraction import SignalExtraction
from app.models.contact import Contact
from app.services.health.pillars import (
    SentimentPillar, 
    EngagementPillar,
    RequestPillar,
    RelationshipPillar,
    SatisfactionPillar,
    ExpansionPillar
)
from app.services.health.assessment import HealthAssessmentGenerator


class HealthCalculator:
    """
    Calculates customer health scores based on 6 pillars.
    Now with decay logic and trend tracking!
    """
    
    # Decay constants
    DECAY_RATE_PER_DAY = 2  # Points lost per day past check-in interval
    DECAY_FLOOR = 30        # Score can't decay below this (prevents false emergencies)
    
    def __init__(self, db: Session):
        self.db = db
        self.assessment_gen = HealthAssessmentGenerator(db)

    def _get_previous_score(self, account_id: UUID) -> Tuple[Optional[int], Optional[HealthScore]]:
        """
        Fetch the most recent health score for comparison.
        Returns (previous_score, previous_health_record)
        """
        previous = self.db.query(HealthScore).filter(
            HealthScore.account_id == account_id
        ).order_by(desc(HealthScore.calculated_at)).first()
        
        if previous:
            return previous.overall_score, previous
        return None, None

    def _apply_decay(self, account: Account, base_score: int, last_interaction: Optional[datetime]) -> Tuple[int, bool]:
        """
        Apply decay if no communication past check-in interval.
        
        Returns (adjusted_score, decay_was_applied)
        
        Logic:
        - If last interaction is within check-in interval: no decay
        - If past interval: lose DECAY_RATE_PER_DAY points per day overdue
        - Score can't drop below DECAY_FLOOR
        """
        if not last_interaction:
            # No interactions ever? Return floor score
            return self.DECAY_FLOOR, True
        
        days_since = (datetime.utcnow() - last_interaction).days
        check_in_interval = account.check_in_interval_days or 14
        
        if days_since <= check_in_interval:
            # Within expected communication window - no decay
            return base_score, False
        
        # Calculate decay
        days_overdue = days_since - check_in_interval
        decay_amount = days_overdue * self.DECAY_RATE_PER_DAY
        
        adjusted_score = max(self.DECAY_FLOOR, base_score - decay_amount)
        
        return adjusted_score, decay_amount > 0

    def _calculate_trend(self, current: int, previous: Optional[int]) -> Tuple[Optional[int], str]:
        """
        Calculate score change and trend direction.
        
        Returns (score_change, trend_direction)
        """
        if previous is None:
            return None, "new"
        
        change = current - previous
        
        if change > 5:
            direction = "up"
        elif change < -5:
            direction = "down"
        else:
            direction = "stable"
        
        return change, direction

    async def calculate_health(
        self, 
        account_id: UUID, 
        triggered_by: str = "manual"
    ) -> HealthScore:
        """
        Calculate health score for an account.
        
        Args:
            account_id: The account to score
            triggered_by: What triggered this calculation
                - "manual": User requested recalculation
                - "input_added": New input was processed
                - "daily_job": Scheduled daily recalculation
                - "decay": Decay check triggered recalc
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError("Account not found")

        # 0. Get previous score for trend tracking
        previous_score, _ = self._get_previous_score(account_id)

        # 1. Fetch recent inputs & extractions
        recent_inputs = self.db.query(Input).filter(
            Input.account_id == account_id,
            Input.is_processed == True
        ).order_by(desc(Input.content_date)).limit(10).all()
        
        input_ids = [inp.id for inp in recent_inputs]
        extractions = []
        if input_ids:
            extractions = self.db.query(SignalExtraction).filter(
                SignalExtraction.input_id.in_(input_ids)
            ).all()
        
        # 2. Fetch contact count
        contact_count = self.db.query(Contact).filter(
            Contact.account_id == account_id
        ).count()
        
        # 3. Calculate Pillars
        sentiment_score = SentimentPillar.calculate(extractions)
        
        last_date = recent_inputs[0].content_date if recent_inputs else None
        engagement_score = EngagementPillar.calculate(
            last_date, 
            account.check_in_interval_days or 14
        )
        
        request_score = RequestPillar.calculate(extractions)
        relationship_score = RelationshipPillar.calculate(contact_count)
        satisfaction_score = SatisfactionPillar.calculate(extractions)
        expansion_score = ExpansionPillar.calculate(extractions)
        
        # 4. Overall Formula (Weighted)
        overall_val = (
            (sentiment_score * 0.20) + 
            (engagement_score * 0.20) + 
            (request_score * 0.15) + 
            (relationship_score * 0.15) + 
            (satisfaction_score * 0.15) + 
            (expansion_score * 0.15)
        )
        overall_score = int(overall_val)
        
        # 5. Apply Decay Logic
        overall_score, decay_applied = self._apply_decay(
            account, 
            overall_score, 
            last_date
        )
        
        # Update triggered_by if decay was the main factor
        if decay_applied and triggered_by == "daily_job":
            triggered_by = "decay"
        
        # 6. Determine Status
        if overall_score < 40:
            status = "at_risk"
        elif overall_score < 70:
            status = "warning"
        else:
            status = "healthy"
        
        # 7. Calculate Trend
        score_change, trend_direction = self._calculate_trend(
            overall_score, 
            previous_score
        )
            
        # 8. Generate AI Assessment
        all_signals = []
        for ext in extractions:
            if ext.signals:
                all_signals.extend(ext.signals)
        unique_signals = list(set(all_signals))[:5] 
        
        ai_summary = await self.assessment_gen.generate_summary(
            account_name=account.name,
            score=overall_score,
            status=status,
            sentiment=sentiment_score,
            engagement=engagement_score,
            signals=unique_signals
        )

        # 9. Save Score with Trend Data
        health = HealthScore(
            account_id=account_id,
            overall_score=overall_score,
            overall_status=status,
            sentiment_score=sentiment_score,
            engagement_score=engagement_score,
            request_score=request_score,
            relationship_score=relationship_score,
            satisfaction_score=satisfaction_score,
            expansion_score=expansion_score,
            ai_summary=ai_summary,
            # New trend fields
            previous_score=previous_score,
            score_change=score_change,
            trend_direction=trend_direction,
            triggered_by=triggered_by,
            calculated_at=datetime.utcnow()
        )
        self.db.add(health)
        self.db.commit()
        self.db.refresh(health)
        return health
