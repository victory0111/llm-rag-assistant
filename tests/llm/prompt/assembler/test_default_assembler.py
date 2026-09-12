from app.llm.prompt.assembler.default import (
    DefaultMessageAssembler,
)
from app.llm.prompt.message import (
    ConversationInput,
    MessageRole,
)


def test_assemble_system_and_user():

    assembler = DefaultMessageAssembler()

    conversation = assembler.assemble(
        rendered_prompt="你是一名科研助手。",
        conversation=ConversationInput(
            current_user_message="什么是VFI？"
        ),
    )

    assert len(conversation.messages) == 2

    assert (
        conversation.messages[0].role
        == MessageRole.SYSTEM
    )

    assert (
        conversation.messages[1].role
        == MessageRole.USER
    )

    assert (
        conversation.messages[1].content
        == "什么是VFI？"
    )

from app.llm.prompt.message import (
    PromptMessage,
)


def test_history_order_is_preserved():

    assembler = DefaultMessageAssembler()

    history = (
        PromptMessage(
            MessageRole.USER,
            "Q1",
        ),
        PromptMessage(
            MessageRole.ASSISTANT,
            "A1",
        ),
    )

    conversation = assembler.assemble(
        rendered_prompt="SYSTEM",
        conversation=ConversationInput(
            history=history,
            current_user_message="Q2",
        ),
    )

    roles = [
        message.role
        for message
        in conversation.messages
    ]

    assert roles == [
        MessageRole.SYSTEM,
        MessageRole.USER,
        MessageRole.ASSISTANT,
        MessageRole.USER,
    ]

def test_empty_system_prompt_is_allowed():

    assembler = DefaultMessageAssembler()

    conversation = assembler.assemble(
        rendered_prompt="   ",
        conversation=ConversationInput(
            current_user_message="hello"
        ),
    )

    assert len(conversation.messages) == 1

    assert (
        conversation.messages[0].role
        == MessageRole.USER
    )

import pytest

from app.llm.prompt.assembler.exceptions import (
    EmptyConversationException,
)


def test_empty_conversation_raises():

    assembler = DefaultMessageAssembler()

    with pytest.raises(
        EmptyConversationException
    ):
        assembler.assemble(
            rendered_prompt="",
            conversation=ConversationInput(),
        )

def test_assembler_is_stateless():

    assembler = DefaultMessageAssembler()

    input_data = ConversationInput(
        current_user_message="hello"
    )

    result1 = assembler.assemble(
        "system",
        input_data,
    )

    result2 = assembler.assemble(
        "system",
        input_data,
    )

    assert result1 == result2