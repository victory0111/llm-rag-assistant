from unittest.mock import Mock

import pytest

from app.llm.prompt.builders.base import BaseTaskBuilder
from app.llm.prompt.enums import PromptTask
from app.llm.prompt.manager import (
    PromptManager,
    PromptTemplateNotFound,
)
from app.llm.prompt.message import (
    ConversationInput,
    PromptConversation,
    PromptMessage,
    MessageRole,
)
from app.llm.prompt.registry import TaskBuilderRegistry
from app.llm.prompt.schemas import PromptBuildContext
from app.llm.prompt.template import PromptTemplate
from app.llm.prompt.value_objects import PromptVersion
from app.llm.schemas.request import LLMRequest


def create_chat_template() -> PromptTemplate:

    return PromptTemplate(
        name="chat_default",
        task=PromptTask.CHAT,
        version=PromptVersion(
            1,
            0,
            0,
        ),
        description="Default chat prompt",
        template="You are a research assistant.",
        variables=(),
    )


def create_conversation() -> PromptConversation:
    """
    构造一个合法的 PromptConversation。

    当前领域模型要求 messages 非空，因此这里提供一条
    与 create_chat_context() 语义一致的用户消息。
    """
    return PromptConversation(
        messages=(
            PromptMessage(
                role=MessageRole.USER,
                content="What is RAG?",
            ),
        )
    )


def create_chat_context() -> PromptBuildContext:

    return PromptBuildContext(
        task=PromptTask.CHAT,
        variables={},
        conversation=ConversationInput(
            current_user_message="What is RAG?"
        ),
        metadata={},
    )


def test_build_success():

    template = create_chat_template()
    context = create_chat_context()

    conversation = create_conversation()

    expected_request = LLMRequest(
        conversation=conversation
    )

    builder = Mock(
        spec=BaseTaskBuilder
    )
    builder.build.return_value = (
        expected_request
    )

    registry = Mock(
        spec=TaskBuilderRegistry
    )
    registry.get.return_value = builder

    manager = PromptManager(
        templates={
            PromptTask.CHAT: template,
        },
        builder_registry=registry,
    )

    request = manager.build(context)

    assert request == expected_request

    registry.get.assert_called_once_with(
        PromptTask.CHAT
    )

    builder.build.assert_called_once_with(
        template,
        context,
    )


def test_missing_template_raises():

    registry = Mock(
        spec=TaskBuilderRegistry
    )

    manager = PromptManager(
        templates={},
        builder_registry=registry,
    )

    context = create_chat_context()

    with pytest.raises(
        PromptTemplateNotFound
    ):
        manager.build(context)

    registry.get.assert_not_called()


def test_reject_template_mapping_task_mismatch():

    rag_template = PromptTemplate(
        name="rag_default",
        task=PromptTask.RAG,
        version=PromptVersion(
            1,
            0,
            0,
        ),
        description="RAG prompt",
        template="...",
        variables=(),
    )

    registry = Mock(
        spec=TaskBuilderRegistry
    )

    with pytest.raises(ValueError):

        PromptManager(
            templates={
                PromptTask.CHAT: rag_template,
            },
            builder_registry=registry,
        )
        