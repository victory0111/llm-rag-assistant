from unittest.mock import Mock
from logging import Logger
import pytest

from app.llm.client import BaseClientManager
from app.llm.context import ProviderContext
from app.llm.exceptions import ProviderNotFoundException
from app.llm.providers.base import BaseProvider
from app.llm.providers.factory import ProviderFactory
from app.llm.schemas.request import LLMRequest
from app.llm.schemas.response import LLMResponse


class DummyProvider(BaseProvider):
    """
    ProviderFactory 单元测试使用的最小合法 Provider。

    不连接任何真实 LLM 服务，
    只用于验证 Provider 的创建、依赖注入、
    初始化和实例缓存行为。
    """

    def __init__(
        self,
        context: ProviderContext,
    ) -> None:

        self.context = context

        self.initialized = False

        self.shutdown_called = False

    @property
    def provider_name(self) -> str:

        return "dummy"

    async def initialize(self) -> None:

        self.initialized = True

    async def shutdown(self) -> None:

        self.shutdown_called = True

    async def health_check(self) -> bool:

        return True

    async def chat(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        raise NotImplementedError

    async def stream_chat(
        self,
        request: LLMRequest,
    ):

        raise NotImplementedError


def create_context() -> ProviderContext:
    """
    构造 ProviderFactory 测试使用的 ProviderContext。

    Factory 单元测试不测试 Settings、Logger、
    ClientManager 本身，因此这些依赖使用 Mock。
    """

    return ProviderContext(
        settings=Mock(),
        logger=Mock(spec=Logger),
        client_manager=Mock(
            spec=BaseClientManager
        ),
    )


def test_register_and_list_providers():

    context = create_context()

    factory = ProviderFactory(
        context=context,
    )

    factory.register(
        "dummy",
        DummyProvider,
    )

    assert factory.list_providers() == [
        "dummy"
    ]


def test_register_duplicate_provider_raises():

    context = create_context()

    factory = ProviderFactory(
        context=context,
    )

    factory.register(
        "dummy",
        DummyProvider,
    )

    with pytest.raises(ValueError):

        factory.register(
            "dummy",
            DummyProvider,
        )


@pytest.mark.anyio
async def test_get_provider_creates_initializes_and_caches_instance():

    context = create_context()

    factory = ProviderFactory(
        context=context,
    )

    factory.register(
        "dummy",
        DummyProvider,
    )

    first = await factory.get_provider(
        "dummy"
    )

    second = await factory.get_provider(
        "dummy"
    )

    assert isinstance(
        first,
        DummyProvider,
    )

    assert first.context is context

    assert first.initialized is True

    assert first is second


@pytest.mark.anyio
async def test_get_unknown_provider_raises():

    context = create_context()

    factory = ProviderFactory(
        context=context,
    )

    with pytest.raises(
        ProviderNotFoundException
    ):

        await factory.get_provider(
            "missing"
        )