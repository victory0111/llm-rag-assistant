from app.llm.prompt.assembler.base import (
    BaseMessageAssembler,
)
from app.llm.prompt.builders.base import (
    BaseTaskBuilder,
)
from app.llm.prompt.enums import PromptTask
from app.llm.prompt.renderer.base import (
    BasePromptRenderer,
)
from app.llm.prompt.schemas import (
    PromptBuildContext,
)
from app.llm.prompt.template import (
    PromptTemplate,
)

from app.llm.schemas.request import LLMRequest


class ChatBuilder(BaseTaskBuilder):
    """
    CHAT Task 的 Prompt 构建策略。

    职责：

    PromptTemplate
          +
    PromptBuildContext
          ↓
    Renderer
          ↓
    MessageAssembler
          ↓
    LLMRequest

    ChatBuilder只负责编排，不实现渲染、
    消息组装或Provider调用。
    """

    def __init__(
        self,
        renderer: BasePromptRenderer,
        assembler: BaseMessageAssembler,
    ) -> None:

        self._renderer = renderer
        self._assembler = assembler

    @property
    def task(self) -> PromptTask:
        return PromptTask.CHAT

    def build(
        self,
        template: PromptTemplate,
        build_context: PromptBuildContext,
    ) -> LLMRequest:

        self._validate_task(
            template,
            build_context,
        )

        rendered_prompt = (
            self._renderer.render(
                template,
                build_context,
            )
        )

        conversation = (
            self._assembler.assemble(
                rendered_prompt,
                build_context.conversation,
            )
        )

        return LLMRequest(
            conversation=conversation,
        )

    def _validate_task(
        self,
        template: PromptTemplate,
        build_context: PromptBuildContext,
    ) -> None:

        if template.task != self.task:
            raise ValueError(
                "ChatBuilder only supports "
                f"{PromptTask.CHAT.value}, "
                f"but template task is "
                f"{template.task.value}"
            )

        if build_context.task != self.task:
            raise ValueError(
                "ChatBuilder only supports "
                f"{PromptTask.CHAT.value}, "
                f"but context task is "
                f"{build_context.task.value}"
            )