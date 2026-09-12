from enum import Enum
from dataclasses import dataclass

class MessageRole(str, Enum):
    """
    Provider-agnostic LLM message role.

    Prompt层只使用统一Role，
    不依赖OpenAI、DeepSeek等具体SDK定义。
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

@dataclass(
    frozen=True,
    slots=True,
)
class PromptMessage:
    """
    一条发送给LLM的统一消息。

    与任何具体Provider SDK无关。
    """

    role: MessageRole
    content: str

    def __post_init__(self) -> None:
        if not isinstance(self.content, str):
            raise TypeError(
                "PromptMessage.content must be str"
            )

        if not self.content.strip():
            raise ValueError(
                "PromptMessage.content cannot be empty"
            )
        
@dataclass(
    frozen=True,
    slots=True,
)
class PromptConversation:
    """
    当前一次LLM推理使用的完整消息序列。
    """

    messages: tuple[PromptMessage, ...]

    def __post_init__(self) -> None:
        if not self.messages:
            raise ValueError(
                "PromptConversation cannot be empty"
            )

    def __len__(self) -> int:
        return len(self.messages)

    def __iter__(self):
        return iter(self.messages)
    
@dataclass(
    frozen=True,
    slots=True,
)
class ConversationInput:
    """
    MessageAssembler的输入信息。

    history:
        已经选好的模型上下文历史。
        注意：不是完整数据库ChatHistory。

    current_user_message:
        当前用户输入。
    """

    history: tuple[PromptMessage, ...] = ()

    current_user_message: str | None = None

    def __post_init__(self) -> None:
        if self.current_user_message is not None:
            if not isinstance(
                self.current_user_message,
                str,
            ):
                raise TypeError(
                    "current_user_message must be str or None"
                )

            if not self.current_user_message.strip():
                raise ValueError(
                    "current_user_message cannot be empty"
                )