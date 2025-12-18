from datetime import datetime, timedelta
from typing import List
from app.models.signal_extraction import SignalExtraction
from app.models.input import Input

class SentimentPillar:
    @staticmethod
    def calculate(extractions: List[SignalExtraction]) -> int:
        if not extractions:
            return 50 # Neutral start
        
        score = 0
        count = 0
        for ext in extractions:
            if ext.sentiment == "positive":
                score += 100
            elif ext.sentiment == "negative":
                score += 0
            else:
                score += 50
            count += 1
            
        return int(score / count)

class EngagementPillar:
    @staticmethod
    def calculate(last_interaction: datetime, expected_interval_days: int) -> int:
        if not last_interaction:
            return 0
        
        days_since = (datetime.utcnow() - last_interaction).days
        
        if days_since <= expected_interval_days:
            return 100
        elif days_since <= expected_interval_days * 2:
            return 70
        elif days_since <= expected_interval_days * 3:
            return 40
        else:
            return 0

class RequestPillar:
    @staticmethod
    def calculate(extractions: List[SignalExtraction]) -> int:
        """
        Calculates score based on feature requests or bugs.
        More requests/bugs slightly decrease health if not handled, 
        but for simple MVP we return 100 if no bugs/requests, 
        and lower for more.
        """
        if not extractions:
            return 100
            
        penalty = 0
        for ext in extractions:
            if not ext.signals:
                continue
            for signal in ext.signals:
                s = signal.lower()
                if "bug" in s or "issue" in s:
                    penalty += 30
                if "request" in s or "feature" in s:
                    penalty += 15
        
        score = 100 - penalty
        return max(0, score)

class RelationshipPillar:
    @staticmethod
    def calculate(contact_count: int) -> int:
        """
        Calculates relationship depth based on number of contacts.
        1 contact = 50, 2+ contacts = 100, 0 = 0.
        """
        if contact_count <= 0:
            return 0
        elif contact_count == 1:
            return 50
        else:
            return 100

class SatisfactionPillar:
    @staticmethod
    def calculate(extractions: List[SignalExtraction]) -> int:
        """
        Similar to sentiment but focused on explicit satisfaction signals.
        """
        if not extractions:
            return 50
            
        score = 0
        count = 0
        for ext in extractions:
            if not ext.signals:
                continue
            for signal in ext.signals:
                s = signal.lower()
                if "happy" in s or "love" in s or "satisfied" in s:
                    score += 100
                elif "unhappy" in s or "frustrated" in s or "dissatisfied" in s:
                    score += 0
                else:
                    score += 50
                count += 1
                
        if count == 0:
            return SentimentPillar.calculate(extractions) # Fallback to general sentiment
            
        return int(score / count)

class ExpansionPillar:
    @staticmethod
    def calculate(extractions: List[SignalExtraction]) -> int:
        """
        Calculates expansion/growth potential.
        """
        if not extractions:
            return 0
            
        score = 0
        for ext in extractions:
            if not ext.signals:
                continue
            for signal in ext.signals:
                s = signal.lower()
                if "upsell" in s or "expansion" in s or "growth" in s or "add-on" in s:
                    score += 50
        
        return min(100, score)

