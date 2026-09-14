from abc import ABC, abstractmethod

from app.llm.prompt.template import PromptTemplate
from app.llm.prompt.schemas import PromptBuildContext


class BasePromptRenderer(ABC):
    """
    Prompt 渲染器接口。

    Renderer 负责：

    PromptTemplate

            ↓

    Rendered Prompt
    """

    @abstractmethod
    def render(

        self,

        template: PromptTemplate,

        context: PromptBuildContext,

    ) -> str:
        """
        渲染 PromptTemplate。

        Returns:

            最终 Prompt 字符串。
        """