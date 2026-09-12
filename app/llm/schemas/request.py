from dataclasses import dataclass

from app.llm.prompt.message import (
    PromptConversation,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LLMRequest:

    conversation: PromptConversation

    model: str | None = None

    temperature: float | None = None

    max_tokens: int | None = None

    top_p: float | None = None

    stream: bool = False