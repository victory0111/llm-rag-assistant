from abc import ABC, abstractmethod

from app.llm.prompt.message import (
    ConversationInput,
    PromptConversation,
)


class BaseMessageAssembler(ABC):
    """
    MessageAssembler抽象接口。

    负责：
        Rendered Prompt
        +
        ConversationInput
        ->
        PromptConversation
    """

    @abstractmethod
    def assemble(
        self,
        rendered_prompt: str,
        conversation: ConversationInput,
    ) -> PromptConversation:
        ...