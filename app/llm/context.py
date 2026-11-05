from dataclasses import dataclass

from app.config.settings import Settings
from app.llm.client import BaseClientManager
from logging import Logger


@dataclass(slots=True)
class ProviderContext:
    """
    Provider 运行上下文。

    Provider 所需的长期基础设施依赖统一由外部注入。
    Provider 自身不负责创建这些基础设施对象。

    注意：
    ProviderContext 不包含 PromptManager、业务 Service、
    DAO 等上游业务依赖。
    """

    settings: Settings

    logger: Logger

    client_manager: BaseClientManager