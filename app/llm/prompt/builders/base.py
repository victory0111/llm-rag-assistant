from abc import ABC, abstractmethod

from app.llm.prompt.enums import PromptTask
from app.llm.prompt.schemas import PromptBuildContext
from app.llm.prompt.template import PromptTemplate
from app.llm.schemas.request import LLMRequest


class BaseTaskBuilder(ABC):
    """
    Prompt Builder策略接口。
    """

    @property
    @abstractmethod
    def task(self) -> PromptTask:
        """
        Builder支持的Task。
        """

    @abstractmethod
    async def build(
        self,
        template: PromptTemplate,
        build_context: PromptBuildContext,
    ) -> LLMRequest:
        """
        构建统一LLMRequest。
        """