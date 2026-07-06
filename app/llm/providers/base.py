from abc import ABC, abstractmethod

from app.llm.schemas.request import LLMRequest
from app.llm.schemas.response import LLMResponse


class BaseProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Provider名称
        """

    @abstractmethod
    async def initialize(self) -> None:
        """
        初始化Provider
        """

    @abstractmethod
    async def shutdown(self) -> None:
        """
        释放资源
        """

    @abstractmethod
    async def health_check(self) -> bool:
        """
        健康检查
        """

    @abstractmethod
    async def chat(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        """
        普通聊天
        """

    @abstractmethod
    async def stream_chat(
        self,
        request: LLMRequest
    ):
        """
        流式聊天
        """