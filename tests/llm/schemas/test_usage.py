import pytest

from app.llm.schemas.usage import TokenUsage


def test_create_token_usage():

    usage = TokenUsage(
        prompt_tokens=120,
        completion_tokens=80,
        total_tokens=200,
    )

    assert usage.prompt_tokens == 120
    assert usage.completion_tokens == 80
    assert usage.total_tokens == 200


def test_reject_inconsistent_total_tokens():

    with pytest.raises(ValueError):

        TokenUsage(
            prompt_tokens=120,
            completion_tokens=80,
            total_tokens=300,
        )