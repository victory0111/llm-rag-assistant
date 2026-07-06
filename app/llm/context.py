# app/llm/context.py

from dataclasses import dataclass

from app.config.settings import Settings
from app.llm.client import BaseClientManager
from app.llm.prompt.manager import PromptManager
from app.utils.logger import Logger


@dataclass(slots=True)
class ProviderContext:
    """
    Provider运行上下文

    Provider所有依赖统一由Factory注入，
    Provider自身禁止创建任何基础设施对象。
    """

    settings: Settings

    logger: Logger

    client_manager: BaseClientManager

    prompt_manager: PromptManager