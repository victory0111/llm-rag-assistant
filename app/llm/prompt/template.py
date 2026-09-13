from dataclasses import dataclass

from app.llm.prompt.enums import PromptTask
from app.llm.prompt.value_objects import PromptVersion


@dataclass(
    frozen=True,
    slots=True,
)
class PromptTemplate:
    name: str
    task: PromptTask
    version: PromptVersion
    description: str
    template: str
    variables: tuple[str, ...] = ()