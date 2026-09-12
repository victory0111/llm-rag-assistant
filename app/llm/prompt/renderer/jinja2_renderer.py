from typing import Dict, Tuple
from jinja2 import Environment, StrictUndefined, Template, UndefinedError
from app.llm.prompt.schemas import PromptBuildContext
from app.llm.prompt.renderer.base import BasePromptRenderer
from app.llm.prompt.renderer.exceptions import (
    PromptRenderException,
    TemplateVariableMissingException,
)
from app.llm.prompt.template import PromptTemplate


class Jinja2PromptRenderer(BasePromptRenderer):
    """
    基于 Jinja2 的高性能 Prompt 渲染器。
    
    包含企业级模板缓存机制，避免高并发场景下的重复编译。
    """

    def __init__(self):
        super().__init__()
        self._env = Environment(
            undefined=StrictUndefined,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # 核心优化：模板编译缓存
        # Key: (template.name, template.version)
        # Value: 编译后的 jinja2.Template 对象
        self._compiled_templates: Dict[Tuple[str, str], Template] = {}

    async def render(self, template: PromptTemplate, context: PromptBuildContext) -> str:
        """
        渲染 Prompt 模板，优先从缓存获取编译后的模板。
        """
        try:
            # 1. 生成缓存 Key
            cache_key = (template.name, template.version)
            
            # 2. 检查缓存（Cache Hit）
            if cache_key not in self._compiled_templates:
                # 缓存未命中（Cache Miss），执行编译并写入缓存
                compiled_template = self._env.from_string(template.template)
                self._compiled_templates[cache_key] = compiled_template
            
            # 3. 从缓存获取编译好的模板对象
            template_obj = self._compiled_templates[cache_key]
            
            # 4. 解包变量字典进行渲染
            return template_obj.render(**context.variables)
            
        except UndefinedError as e:
            raise TemplateVariableMissingException(
                f"Prompt 渲染失败: 模板中缺少变量。原始错误: {e}"
            ) from e
            
        except Exception as e:
            raise PromptRenderException(
                f"Prompt 渲染过程中发生未知错误: {e}"
            ) from e