
import pytest
from types import SimpleNamespace  # 引入 SimpleNamespace 用于快速构建带属性的对象
from app.llm.prompt.renderer.exceptions import TemplateVariableMissingException
from app.llm.prompt.template import PromptTemplate
from app.llm.prompt.value_objects import PromptVersion
from app.llm.prompt.enums import PromptTask


@pytest.mark.anyio
async def test_render_single_variable(renderer, mock_template):
    """
    Test1: 正常渲染单个变量。
    """
    # 构建包含 variables 属性的 context 对象
    context = SimpleNamespace(variables={"question": "Transformer是什么"})
    result = renderer.render(mock_template, context)
    
    assert result == "你好 Transformer是什么"


@pytest.mark.anyio
async def test_render_multiple_variables(renderer):
    """
    Test2: 正常渲染多个变量。
    """
    template = PromptTemplate(
        task=PromptTask.CHAT,
        description="...",
        name="multi_var_template",
        version=PromptVersion(1, 0, 0),
        template="论文: {{paper}}\n问题: {{question}}"
    )
    context = SimpleNamespace(variables={
        "paper": "Attention Is All You Need", 
        "question": "核心思想是什么?"
    })
    result = renderer.render(template, context)
    
    expected = "论文: Attention Is All You Need\n问题: 核心思想是什么?"
    assert result == expected


@pytest.mark.anyio
async def test_render_missing_variable_raises_exception(renderer):
    """
    Test3: 变量缺失时，应抛出企业级异常 TemplateVariableMissingException。
    """
    template = PromptTemplate(
        task=PromptTask.CHAT,
        description="...",
        name="missing_var_template",
        version=PromptVersion(1, 0, 0),
        template="问题: {{question}}"
    )
    # 故意提供空的 variables
    context = SimpleNamespace(variables={})
    
    with pytest.raises(TemplateVariableMissingException):
        await renderer.render(template, context)


@pytest.mark.anyio 
async def test_render_empty_template(renderer):
    """
    Test4: 空模板应正常渲染，返回空字符串。
    """
    template = PromptTemplate(
        task=PromptTask.CHAT,
        description="...",
        name="empty_template",
        version=PromptVersion(1, 0, 0),
        template=""
    )
    context = SimpleNamespace(variables={"question": "随便什么"})
    result = renderer.render(template, context)
    
    assert result == ""


@pytest.mark.anyio
async def test_metadata_not_participate_in_render(renderer):
    """
    Test5: Metadata 不参与渲染过程，不应影响结果。
    """
    template = PromptTemplate(
        task=PromptTask.CHAT,
        description="...",
        name="metadata_template",
        version=PromptVersion(1, 0, 0),
        template="你好 {{question}}"
    )
    # context 对象中包含 metadata，但 variables 中只有模板需要的变量
    context = SimpleNamespace(
        variables={"question": "RAG"},
        metadata={"user_id": 123, "trace_id": "abc-xyz"}
    )
    result = renderer.render(template, context)
    
    assert result == "你好 RAG"


@pytest.mark.anyio
async def test_renderer_is_stateless(renderer):
    """
    Test6: 验证渲染器是无状态的。
    """
    template = PromptTemplate(
        task=PromptTask.CHAT,
        description="...",
        name="stateless_template",
        version=PromptVersion(1, 0, 0),
        template="Q: {{question}}"
    )
    
    # 第一次渲染
    context_1 = SimpleNamespace(variables={"question": "第一次"})
    result_1 = renderer.render(template, context_1)
    assert result_1 == "Q: 第一次"
    
    # 第二次渲染（使用不同的变量）
    context_2 = SimpleNamespace(variables={"question": "第二次"})
    result_2 = renderer.render(template, context_2)
    assert result_2 == "Q: 第二次"
    
    # 第三次渲染（再次使用第一次的变量）
    result_3 = renderer.render(template, context_1)
    assert result_3 == "Q: 第一次"
    
    # 验证缓存机制没有导致状态污染
    assert result_1 == result_3
    assert result_1 != result_2