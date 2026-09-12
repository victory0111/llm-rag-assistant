from app.llm.prompt.message import (
    MessageRole,
)


def test_message_role_values():
    assert MessageRole.SYSTEM.value == "system"
    assert MessageRole.USER.value == "user"
    assert (
        MessageRole.ASSISTANT.value
        == "assistant"
    )
    assert MessageRole.TOOL.value == "tool"

import pytest
from dataclasses import FrozenInstanceError

from app.llm.prompt.message import (
    MessageRole,
    PromptMessage,
)


def test_prompt_message_is_immutable():

    message = PromptMessage(
        role=MessageRole.USER,
        content="hello",
    )

    with pytest.raises(
        FrozenInstanceError
    ):
        message.content = "changed"
  
def test_prompt_message_rejects_empty_content():

    with pytest.raises(ValueError):
        PromptMessage(
            role=MessageRole.USER,
            content="   ",
        )