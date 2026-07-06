from app.llm.prompt.enums import PromptTask
from app.llm.prompt.template import PromptTemplate
import pytest


def test_create_prompt_template():

    template = PromptTemplate(

        name="chat",

        task=PromptTask.CHAT,

        version="1.0.0",

        description="聊天",

        template="hello {{question}}",

        variables=["question"]

    )

    assert template.name == "chat"

    assert template.task == PromptTask.CHAT

    assert template.version == "1.0.0"

    assert template.variables == ["question"]

def test_prompt_template_is_immutable():

    template = PromptTemplate(

        name="chat",

        task=PromptTask.CHAT,

        version="1.0",

        description="",

        template="abc"

    )

    with pytest.raises(Exception):

        template.name = "new"