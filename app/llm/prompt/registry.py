
import asyncio
from enum import Enum, auto
from typing import Dict

from app.llm.prompt.builders.base import BaseTaskBuilder
from app.llm.prompt.enums import PromptTask


# --- 自定义异常 ---
class PromptRegistryError(Exception):
    """Prompt 注册表基础异常"""

class AlreadyRegistered(PromptRegistryError):
    """当尝试重复注册同一个 Task 的 Builder 时抛出"""

class BuilderNotFound(PromptRegistryError):
    """当请求的 Task 未找到对应的 Builder 时抛出"""


# --- 状态枚举 ---
class RegistryState(Enum):
    CREATED = auto()
    REGISTERING = auto()
    FROZEN = auto()


# --- 核心注册表 ---
class TaskBuilderRegistry:
    def __init__(self):
        self._builders: Dict[PromptTask, BaseTaskBuilder] = {}
        self._lock = asyncio.Lock()
        self._state = RegistryState.CREATED

    async def register(self, builder: BaseTaskBuilder) -> None:
        if self._state == RegistryState.FROZEN:
            raise RuntimeError("Cannot register builder: Registry is FROZEN.")
        
        async with self._lock:
            if self._state == RegistryState.FROZEN:
                raise RuntimeError("Cannot register builder: Registry is FROZEN.")
            
            # 核心修改：检查是否已存在，若存在则抛出 AlreadyRegistered
            if builder.task in self._builders:
                raise AlreadyRegistered(f"Builder for task {builder.task} is already registered.")
                
            self._builders[builder.task] = builder
            self._state = RegistryState.REGISTERING

    async def unregister(self, task: PromptTask) -> None:
        if self._state == RegistryState.FROZEN:
            raise RuntimeError("Cannot unregister builder: Registry is FROZEN.")
            
        async with self._lock:
            if self._state == RegistryState.FROZEN:
                raise RuntimeError("Cannot unregister builder: Registry is FROZEN.")
            self._builders.pop(task, None)

    def freeze(self) -> None:
        self._state = RegistryState.FROZEN

    def get(self, task: PromptTask) -> BaseTaskBuilder:
        # 核心修改：找不到时抛出 BuilderNotFound
        if task not in self._builders:
            raise BuilderNotFound(f"No builder registered for task: {task}")
        return self._builders[task]

    def list(self) -> list[PromptTask]:
        return list(self._builders.keys())