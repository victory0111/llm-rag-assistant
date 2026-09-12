
import pytest
import anyio
from unittest.mock import MagicMock

from app.llm.prompt.enums import PromptTask
from app.llm.prompt.builders.base import BaseTaskBuilder
from app.llm.prompt.registry import TaskBuilderRegistry, AlreadyRegistered, BuilderNotFound


# --- 辅助测试夹具 (Fixture) ---
@pytest.fixture
def registry():
    """
    每个测试用例运行前，提供一个全新的、干净的 Registry 实例。
    """
    return TaskBuilderRegistry()

@pytest.fixture
def mock_chat_builder():
    """
    模拟一个处理 CHAT 任务的 Builder。
    """
    builder = MagicMock(spec=BaseTaskBuilder)
    builder.task = PromptTask.CHAT
    return builder

@pytest.fixture
def mock_rag_builder():
    """
    模拟一个处理 RAG 任务的 Builder。
    """
    builder = MagicMock(spec=BaseTaskBuilder)
    builder.task = PromptTask.RAG
    return builder


# --- 测试用例 ---

@pytest.mark.anyio
async def test_register_success(registry, mock_chat_builder):
    """
    Test1: 正常注册一个 Builder 应该成功。
    """
    await registry.register(mock_chat_builder)
    assert PromptTask.CHAT in registry.list()

@pytest.mark.anyio
async def test_register_duplicate_raises_already_registered(registry, mock_chat_builder):
    """
    Test2: 重复注册同一个 Task 的 Builder，应该抛出 AlreadyRegistered 异常。
    """
    await registry.register(mock_chat_builder)
    
    # 再次尝试注册同一个 builder
    with pytest.raises(AlreadyRegistered):
        await registry.register(mock_chat_builder)

def test_get_success(registry, mock_chat_builder):
    """
    Test3: 获取已注册的 Builder 应该成功。
    注意：由于这里不涉及 await，我们使用同步方式直接注入数据来测试 get。
    """
    # 直接写入字典以绕过 async register
    registry._builders[PromptTask.CHAT] = mock_chat_builder
    
    builder = registry.get(PromptTask.CHAT)
    assert builder == mock_chat_builder

def test_get_not_found_raises_builder_not_found(registry):
    """
    Test4: 获取不存在的 Builder，应该抛出 BuilderNotFound 异常。
    """
    with pytest.raises(BuilderNotFound):
        registry.get(PromptTask.CHAT)

def test_list_returns_all_builders(registry, mock_chat_builder, mock_rag_builder):
    """
    Test5: list() 方法应该返回所有已注册的 Builder 的 Task 列表。
    """
    # 直接注入两个 builder
    registry._builders[PromptTask.CHAT] = mock_chat_builder
    registry._builders[PromptTask.RAG] = mock_rag_builder
    
    tasks = registry.list()
    assert len(tasks) == 2
    assert PromptTask.CHAT in tasks
    assert PromptTask.RAG in tasks