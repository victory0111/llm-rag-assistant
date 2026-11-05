from abc import ABC, abstractmethod
from app.llm.providers.base import BaseProvider
import asyncio

from app.llm.context import ProviderContext
from app.llm.exceptions import ProviderNotFoundException


class BaseProviderFactory(ABC):

    @abstractmethod
    def register(
        self,
        provider_name: str,
        provider_cls: type[BaseProvider]
    ) -> None:
        """
        注册Provider
        """

    @abstractmethod
    async def get_provider(
        self,
        provider_name: str
    ) -> BaseProvider:
        """
        获取Provider
        """

    @abstractmethod
    def list_providers(self) -> list[str]:
        """
        获取已注册Provider
        """

    @abstractmethod
    async def shutdown(self) -> None:
        """
        关闭所有Provider
        """


class ProviderFactory(BaseProviderFactory):

    def __init__(
        self,
        context: ProviderContext
    ):

        self._context = context

        self._registry: dict[
            str,
            type[BaseProvider]
        ] = {}

        self._instances: dict[
            str,
            BaseProvider
        ] = {}

        self._lock = asyncio.Lock()

    def register(

        self,

        provider_name: str,

        provider_cls: type[BaseProvider]

    ):

        if provider_name in self._registry:

            raise ValueError(

                f"{provider_name} already registered."

            )

        self._registry[provider_name] = provider_cls

    async def get_provider(

        self,

        provider_name: str

    ) -> BaseProvider:

        if provider_name in self._instances:

            return self._instances[provider_name]

        async with self._lock:

            if provider_name in self._instances:

                return self._instances[provider_name]

            provider_cls = self._registry.get(provider_name)

            if provider_cls is None:

                raise ProviderNotFoundException(provider_name)

            provider = provider_cls(

                context=self._context

            )

            await provider.initialize()

            self._instances[provider_name] = provider

            return provider
        
    def list_providers(

        self

    ):

        return list(

            self._registry.keys()

        )
    
    async def shutdown(self):

        async with self._lock:

            for provider in self._instances.values():

                await provider.shutdown()

            self._instances.clear()