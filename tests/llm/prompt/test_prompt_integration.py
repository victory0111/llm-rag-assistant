from app.llm.prompt.assembler.default import (
    DefaultMessageAssembler,
)
from app.llm.prompt.builders.chat_builder import (
    ChatBuilder,
)
from app.llm.prompt.enums import PromptTask
from app.llm.prompt.manager import PromptManager
from app.llm.prompt.message import (
    ConversationInput,
    MessageRole,
)
from app.llm.prompt.registry import (
    TaskBuilderRegistry,
)
from app.llm.prompt.renderer.jinja2_renderer import (
    Jinja2PromptRenderer,
)
from app.llm.prompt.schemas import (
    PromptBuildContext,
)
from app.llm.prompt.templates.chat import (
    CHAT_TEMPLATE,
)
from app.llm.schemas.request import LLMRequest


def test_chat_prompt_pipeline_builds_llm_request():

    renderer = Jinja2PromptRenderer()

    assembler = DefaultMessageAssembler()

    builder = ChatBuilder(
        renderer=renderer,
        assembler=assembler,
    )

    registry = TaskBuilderRegistry()

    registry.register(builder)

    registry.freeze()

    manager = PromptManager(
        templates={
            PromptTask.CHAT: CHAT_TEMPLATE,
        },
        builder_registry=registry,
    )

    context = PromptBuildContext(
        task=PromptTask.CHAT,
        variables={},
        conversation=ConversationInput(
            current_user_message="What is RAG?"
        ),
        metadata={},
    )

    request = manager.build(context)

    assert isinstance(
        request,
        LLMRequest,
    )

    messages = request.conversation.messages

    assert len(messages) == 2

    assert messages[0].role == MessageRole.SYSTEM

    assert messages[1].role == MessageRole.USER

    assert (
        messages[1].content
        == "What is RAG?"
    )

    assert "What is RAG?" not in messages[0].content

    assert (
    "计算机领域科研助手"
    in messages[0].content
)