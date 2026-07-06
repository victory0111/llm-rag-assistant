from abc import ABC
from typing import Any


class BasePromptTemplate(ABC):
    """
    PromptTemplate 抽象基类。

    PromptTemplate 仅负责描述 Prompt 模板，
    不负责 Prompt 渲染。
    """

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def task(self) -> str:
        raise NotImplementedError

    @property
    def version(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        raise NotImplementedError

    @property
    def template(self) -> str:
        raise NotImplementedError

    @property
    def variables(self) -> list[str]:
        """
        当前模板需要哪些变量
        """
        raise NotImplementedError

    def metadata(self) -> dict[str, Any]:
        """
        返回模板元信息。
        """
        return {}