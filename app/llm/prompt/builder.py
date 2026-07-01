from abc import ABC, abstractmethod

from app.llm.schemas.request import LLMRequest


class BasePromptBuilder(ABC):

    @abstractmethod
    def build_messages(
        self,
        request: LLMRequest
    ) -> list[dict]:
        """
        构造OpenAI Compatible messages
        """
        raise NotImplementedError