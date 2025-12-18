from abc import ABC, abstractmethod
from typing import Any, Dict

class LLMProvider(ABC):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate text completion from the LLM.
        """
        pass

    @abstractmethod
    async def analyze_health(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze customer health based on input data.
        Returns a structured dictionary with scores/reasoning.
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for cost tracking.
        """
        pass
