from enum import Enum
from abc import ABC, abstractmethod
from typing import Any
import asyncio
from typing import Any

class ClientStatus(str, Enum):
    """
    客户端状态枚举
    定义 LLM 客户端管理器可能处于的不同状态。
    继承自 str,使得枚举值可以直接作为字符串比较和使用。
    """
    CREATED = "created"

    INITIALIZED = "initialized"

    CLOSED = "closed"

    ERROR = "error"

class BaseClientManager(ABC):
    """
    基础客户端管理器
    定义了 LLM 客户端管理器的基本接口。
    子类需要实现这些方法来管理 LLM 客户端。
    """

    @abstractmethod
    async def initialize(self) -> None:
        pass

    @abstractmethod
    async def get_client(self, provider: str) -> Any:
        pass

    @abstractmethod
    async def health_check(self) -> dict:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass
    
class LLMClientManager(BaseClientManager):
    """
    LLM客户端管理器
    实现了 LLM 客户端管理器的基本功能。
    包括初始化、获取客户端、健康检查和关闭。
    """

    def __init__(self):
        """
        初始化LLM客户端管理器
        初始化空的客户端字典和状态为创建。
        """

        self._clients: dict[str, Any] = {}

        self._status = ClientStatus.CREATED

        self._lock = asyncio.Lock()

    @property
    def status(self):

        return self._status
    
    async def initialize(self):
        """
        初始化LLM客户端管理器
        创建并初始化LLM客户端。
        """

        async with self._lock:

            if self._status == ClientStatus.INITIALIZED:

                return

            # Sprint1-2先占位
            # 后面真正创建SDK Client

            self._status = ClientStatus.INITIALIZED

    async def get_client(self, provider: str):
        """
        获取LLM客户端
        根据提供程序名称获取对应的LLM客户端。
        """

        if self._status != ClientStatus.INITIALIZED:

            raise RuntimeError(
                "ClientManager not initialized."
            )

        return self._clients.get(provider)

    async def shutdown(self):
        """
        关闭LLM客户端管理器
        清除所有LLM客户端并设置状态为关闭。
        """

        async with self._lock:

            self._clients.clear()

            self._status = ClientStatus.CLOSED

    async def health_check(self):
        """
        健康检查LLM客户端管理器
        返回当前状态和已初始化的提供程序列表。
        """

        return {

            "status": self._status,

            "providers": list(self._clients.keys())
        }