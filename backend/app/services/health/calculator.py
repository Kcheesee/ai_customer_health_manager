from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import UUID
from datetime import datetime

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
    def __init__(self, db: Session):
        self.db = db
        self.assessment_gen = HealthAssessmentGenerator(db)

    async def calculate_health(self, account_id: UUID) -> HealthScore:
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError("Account not found")

        # 1. Fetch recent inputs & extractions
        recent_inputs = self.db.query(Input).filter(
            Input.account_id == account_id,
            Input.is_processed == True
        ).order_by(desc(Input.content_date)).limit(10).all()
        
        input_ids = [inp.id for inp in recent_inputs]
        extractions = self.db.query(SignalExtraction).filter(
            SignalExtraction.input_id.in_(input_ids)
        ).all()
        
        # 2. Fetch contact count
        contact_count = self.db.query(Contact).filter(Contact.account_id == account_id).count()
        
        # 3. Calculate Pillars
        sentiment_score = SentimentPillar.calculate(extractions)
        
        last_date = recent_inputs[0].content_date if recent_inputs else None
        engagement_score = EngagementPillar.calculate(last_date, account.check_in_interval_days)
        
        request_score = RequestPillar.calculate(extractions)
        relationship_score = RelationshipPillar.calculate(contact_count)
        satisfaction_score = SatisfactionPillar.calculate(extractions)
        expansion_score = ExpansionPillar.calculate(extractions)
        
        # 4. Overall Formula (Weighted)
        # (Sentiment*0.2) + (Engagement*0.2) + (Requests*0.15) + (Relationship*0.15) + (Satisfaction*0.15) + (Expansion*0.15)
        overall_val = (
            (sentiment_score * 0.20) + 
            (engagement_score * 0.20) + 
            (request_score * 0.15) + 
            (relationship_score * 0.15) + 
            (satisfaction_score * 0.15) + 
            (expansion_score * 0.15)
        )
        overall_score = int(overall_val)
        
        # Status
        status = "healthy"
        if overall_score < 40:
            status = "at_risk"
        elif overall_score < 70:
            status = "warning"
            
        # 5. Generate AI Assessment
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

        # 6. Save Score
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
            calculated_at=datetime.utcnow()
        )
        self.db.add(health)
        self.db.commit()
        self.db.refresh(health)
        return health

