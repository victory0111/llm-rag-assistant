from app.llm.prompt.enums import PromptTask
from app.llm.prompt.template import PromptTemplate
from app.llm.prompt.value_objects import PromptVersion

CHAT_TEMPLATE = PromptTemplate(
    name="chat_default",

    task=PromptTask.CHAT,

    version=PromptVersion(
        1,
        0,
        0,
    ),

    description="默认科研聊天",

    template="""
你是一名计算机领域科研助手。

请认真回答用户问题。

问题：

{{question}}
""",

    variables=("question",),
)