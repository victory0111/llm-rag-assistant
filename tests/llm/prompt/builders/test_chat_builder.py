from unittest.mock import (
    AsyncMock,
    Mock,
)

import pytest

from app.llm.prompt.assembler.base import (
    BaseMessageAssembler,
)
from app.llm.prompt.builders.chat_builder import (
    ChatBuilder,
)
from app.llm.prompt.enums import PromptTask
from app.llm.prompt.message import (
    ConversationInput,
    MessageRole,
    PromptConversation,
    PromptMessage,
)
from app.llm.prompt.renderer.base import (
    BasePromptRenderer,
)
from app.llm.prompt.schemas import (
    PromptBuildContext,
)
from app.llm.prompt.template import (
    PromptTemplate,
)
from app.llm.prompt.value_objects import (
    PromptVersion,
)

def create_chat_template():

    return PromptTemplate(
        name="chat_default",
        task=PromptTask.CHAT,
        version=PromptVersion(
            1,
            0,
            0,
        ),
        description="Default chat prompt",
        template="你是一名科研助手。",
        variables=(),
    )


def create_chat_context():

    return PromptBuildContext(
        task=PromptTask.CHAT,
        variables={},
        conversation=ConversationInput(
            current_user_message=(
                "什么是VFI？"
            )
        ),
        metadata={},
    )

def test_chat_builder_task():

    renderer = Mock(
        spec=BasePromptRenderer
    )

    assembler = Mock(
        spec=BaseMessageAssembler
    )

    builder = ChatBuilder(
        renderer=renderer,
        assembler=assembler,
    )

    assert (
        builder.task
        == PromptTask.CHAT
    )

@pytest.mark.anyio
async def test_build_success():

    renderer = Mock(
        spec=BasePromptRenderer
    )

    renderer.render = Mock(
        return_value=(
            "你是一名科研助手。"
        )
    )

    conversation = PromptConversation(
        messages=(
            PromptMessage(
                role=MessageRole.SYSTEM,
                content="你是一名科研助手。",
            ),
            PromptMessage(
                role=MessageRole.USER,
                content="什么是VFI？",
            ),
        )
    )

    assembler = Mock(
        spec=BaseMessageAssembler
    )

    assembler.assemble.return_value = (
        conversation
    )

    builder = ChatBuilder(
        renderer=renderer,
        assembler=assembler,
    )

    template = create_chat_template()
    context = create_chat_context()

    request = await builder.build(
        template,
        context,
    )

    assert (
        request.conversation
        == conversation
    )

    renderer.render.assert_called_once_with(
        template,
        context,
    )

    assembler.assemble.assert_called_once_with(
        "你是一名科研助手。",
        context.conversation,
    )



@pytest.mark.anyio
async def test_reject_wrong_template_task():

    renderer = Mock(
        spec=BasePromptRenderer
    )

    assembler = Mock(
        spec=BaseMessageAssembler
    )

    builder = ChatBuilder(
        renderer=renderer,
        assembler=assembler,
    )

    template = PromptTemplate(
        name="rag_default",
        task=PromptTask.RAG,
        version=PromptVersion(
            1,
            0,
            0,
        ),
        description="RAG",
        template="...",
        variables=(),
    )

    context = create_chat_context()

    with pytest.raises(ValueError):
        await builder.build(
            template,
            context,
        )

@pytest.mark.anyio
async def test_reject_wrong_context_task():

    renderer = Mock(
        spec=BasePromptRenderer
    )

    assembler = Mock(
        spec=BaseMessageAssembler
    )

    builder = ChatBuilder(
        renderer=renderer,
        assembler=assembler,
    )

    template = create_chat_template()

    context = PromptBuildContext(
        task=PromptTask.RAG,
        variables={},
        conversation=ConversationInput(
            current_user_message="hello"
        ),
        metadata={},
    )

    with pytest.raises(ValueError):
        await builder.build(
            template,
            context,
        )