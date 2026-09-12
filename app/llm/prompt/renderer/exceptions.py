
class PromptRenderException(Exception):
    """
    Prompt 渲染基础异常。
    当渲染过程中发生任何非预期错误时抛出。
    """

class TemplateVariableMissingException(PromptRenderException):
    """
    模板变量缺失异常。
    当 Jinja2 模板中引用了 context 中不存在的变量时抛出。
    继承自 PromptRenderException，方便上层统一捕获。
    """