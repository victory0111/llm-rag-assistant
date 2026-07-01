from abc import ABC, abstractmethod

from app.llm.schemas.request import LLMRequest
from app.llm.schemas.response import LLMResponse


class BaseProvider(ABC):

    @abstractmethod
    async def chat(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        """
        普通聊天
        """
        raise NotImplementedError

    @abstractmethod
    async def stream_chat(
        self,
        request: LLMRequest
    ):
        """
        流式聊天
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """
        模型健康检查
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Provider名称
        """
        raise NotImplementedError