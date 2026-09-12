from app.llm.prompt.assembler.base import (
    BaseMessageAssembler,
)
from app.llm.prompt.assembler.exceptions import (
    EmptyConversationException,
    InvalidHistoryException,
)
from app.llm.prompt.message import (
    ConversationInput,
    MessageRole,
    PromptConversation,
    PromptMessage,
)


class DefaultMessageAssembler(
    BaseMessageAssembler
):
    """
    默认消息组装策略。

    顺序：

        SYSTEM
        ↓
        HISTORY
        ↓
        CURRENT USER

    本类无状态，可在Application生命周期中复用。
    """

    def assemble(
        self,
        rendered_prompt: str,
        conversation: ConversationInput,
    ) -> PromptConversation:

        messages: list[PromptMessage] = []

        self._append_system_message(
            messages,
            rendered_prompt,
        )

        self._append_history(
            messages,
            conversation.history,
        )

        self._append_current_user_message(
            messages,
            conversation.current_user_message,
        )

        if not messages:
            raise EmptyConversationException(
                "Cannot assemble an empty conversation"
            )

        return PromptConversation(
            messages=tuple(messages)
        )

    @staticmethod
    def _append_system_message(
        messages: list[PromptMessage],
        rendered_prompt: str,
    ) -> None:

        if not isinstance(rendered_prompt, str):
            raise TypeError(
                "rendered_prompt must be str"
            )

        rendered_prompt = rendered_prompt.strip()

        if not rendered_prompt:
            return

        messages.append(
            PromptMessage(
                role=MessageRole.SYSTEM,
                content=rendered_prompt,
            )
        )

    @staticmethod
    def _append_history(
        messages: list[PromptMessage],
        history: tuple[
            PromptMessage,
            ...
        ],
    ) -> None:

        for message in history:

            if not isinstance(
                message,
                PromptMessage,
            ):
                raise InvalidHistoryException(
                    "history must contain "
                    "PromptMessage instances"
                )

            messages.append(message)

    @staticmethod
    def _append_current_user_message(
        messages: list[PromptMessage],
        current_user_message: str | None,
    ) -> None:

        if current_user_message is None:
            return

        messages.append(
            PromptMessage(
                role=MessageRole.USER,
                content=current_user_message.strip(),
            )
        )