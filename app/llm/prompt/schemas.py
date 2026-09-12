from dataclasses import dataclass, field
from typing import Any

from app.llm.prompt.enums import PromptTask
from app.llm.prompt.message import ConversationInput


@dataclass(slots=True)
class PromptBuildContext:
    """
    一次Prompt构建的完整运行上下文。
    """

    task: PromptTask

    variables: dict[str, Any] = field(
        default_factory=dict
    )

    conversation: ConversationInput = field(
        default_factory=ConversationInput
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )