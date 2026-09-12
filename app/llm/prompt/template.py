from dataclasses import dataclass, field
from typing import Any
from app.llm.prompt.value_objects import PromptVersion
from app.llm.prompt.base import BasePromptTemplate
from app.llm.prompt.enums import PromptTask


@dataclass(slots=True, frozen=True)
class PromptTemplate(BasePromptTemplate):
    """
    Prompt 模板对象。

    一个 PromptTemplate 描述一个 Prompt，
    不负责 Prompt 的渲染。
    """

    name: str

    task: PromptTask

    version: PromptVersion

    description: str

    template: str

    variables: list[str] = field(default_factory=list)

    extra: dict[str, Any] = field(default_factory=dict)

    def metadata(self) -> dict[str, Any]:
        return self.extra