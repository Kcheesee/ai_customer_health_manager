from typing import Dict, Any
from .base import LLMProvider
import anthropic
import openai
import google.generativeai as genai

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = anthropic.Anthropic(api_key=api_key)

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text

    async def analyze_health(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for structured analysis
        prompt = f"Analyze health for: {input_data}"
        response = await self.generate_text(prompt, system_prompt="You are a customer health analyst.")
        return {"analysis": response, "raw": response}

    def count_tokens(self, text: str) -> int:
        return len(text.split()) # Rough approximation for now

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.client = openai.OpenAI(api_key=api_key)

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
            
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

    async def analyze_health(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze health for: {input_data}"
        response = await self.generate_text(prompt, system_prompt="You are a customer health analyst.")
        return {"analysis": response, "raw": response}
    
    def count_tokens(self, text: str) -> int:
        return len(text.split())

class GoogleProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        # Gemini doesn't have 'system' prompt in the same way, usually prepended
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
        response = self.model_instance.generate_content(full_prompt)
        return response.text

    async def analyze_health(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Analyze health for: {input_data}"
        response = await self.generate_text(prompt, system_prompt="You are a customer health analyst.")
        return {"analysis": response, "raw": response}
    
    def count_tokens(self, text: str) -> int:
        return len(text.split())
