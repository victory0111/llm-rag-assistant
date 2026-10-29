from collections.abc import Mapping

from app.llm.prompt.enums import PromptTask
from app.llm.prompt.registry import TaskBuilderRegistry
from app.llm.prompt.schemas import PromptBuildContext
from app.llm.prompt.template import PromptTemplate
from app.llm.schemas.request import LLMRequest


class PromptTemplateNotFound(Exception):
    """
    当前 PromptTask 没有对应的 PromptTemplate。
    """


class PromptManager:
    """
    Prompt 子系统统一入口。

    PromptManager 负责：

    PromptBuildContext
            ↓
    PromptTemplate Lookup
            ↓
    TaskBuilder Lookup
            ↓
    LLMRequest

    它不负责模板渲染、消息组装或 Provider 调用。
    """

    def __init__(
        self,
        templates: Mapping[
            PromptTask,
            PromptTemplate,
        ],
        builder_registry: TaskBuilderRegistry,
    ) -> None:

        self._templates = dict(templates)
        self._builder_registry = builder_registry

        self._validate_templates()

    def build(
        self,
        build_context: PromptBuildContext,
    ) -> LLMRequest:

        task = build_context.task

        template = self._get_template(task)

        builder = self._builder_registry.get(task)

        return builder.build(
            template,
            build_context,
        )

    def _get_template(
        self,
        task: PromptTask,
    ) -> PromptTemplate:

        try:
            return self._templates[task]

        except KeyError as exc:
            raise PromptTemplateNotFound(
                f"No prompt template configured for task: {task}"
            ) from exc

    def _validate_templates(self) -> None:

        for task, template in self._templates.items():

            if template.task != task:
                raise ValueError(
                    "Prompt template mapping task mismatch: "
                    f"key={task}, "
                    f"template.task={template.task}"
                )