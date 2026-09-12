# test/llm/prompt/renderer/conftest.py

import pytest
from app.llm.prompt.renderer.jinja2_renderer import Jinja2PromptRenderer
from app.llm.prompt.template import PromptTemplate
from app.llm.prompt.value_objects import PromptVersion


@pytest.fixture
def renderer():
    """
    提供 Jinja2PromptRenderer 实例。
    """
    return Jinja2PromptRenderer()


@pytest.fixture
def mock_template():
    """
    提供一个基础的 PromptTemplate 用于测试。
    """
    return PromptTemplate(
        name="test_template",
        version=PromptVersion(1,0,0),
        template="你好 {{question}}"
    )