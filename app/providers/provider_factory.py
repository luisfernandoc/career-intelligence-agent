import os
from app.providers.groq_provider import GroqProvider
from app.providers.openai_provider import OpenAIProvider


def get_llm_provider():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        return GroqProvider()

    if provider == "openai":
        return OpenAIProvider()

    raise ValueError(f"Unsupported LLM provider: {provider}")
