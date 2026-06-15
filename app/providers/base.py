from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
    ) -> str:
        pass
