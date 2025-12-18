from typing import Optional
from app.schemas.llm import LLMProviderType
from .base import LLMProvider
from .providers import AnthropicProvider, OpenAIProvider, GoogleProvider
from .mock_provider import MockProvider

class LLMClientFactory:
    @staticmethod
    def create(provider_type: LLMProviderType, api_key: str, model: str) -> LLMProvider:
        if provider_type == LLMProviderType.ANTHROPIC:
            return AnthropicProvider(api_key, model)
        elif provider_type == LLMProviderType.OPENAI:
            return OpenAIProvider(api_key, model)
        elif provider_type == LLMProviderType.GOOGLE:
            return GoogleProvider(api_key, model)
        elif provider_type == LLMProviderType.MOCK:
            return MockProvider(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider_type}")
