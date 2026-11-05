from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class TokenUsage:
    """
    一次 LLM 调用的标准化 Token 使用量。

    Provider 负责把不同厂商返回的 usage 字段
    转换为这个统一结构。
    """

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    def __post_init__(self) -> None:

        if self.prompt_tokens < 0:
            raise ValueError(
                "prompt_tokens cannot be negative"
            )

        if self.completion_tokens < 0:
            raise ValueError(
                "completion_tokens cannot be negative"
            )

        if self.total_tokens < 0:
            raise ValueError(
                "total_tokens cannot be negative"
            )

        expected_total = (
            self.prompt_tokens
            + self.completion_tokens
        )

        if self.total_tokens != expected_total:
            raise ValueError(
                "total_tokens must equal "
                "prompt_tokens + completion_tokens"
            )