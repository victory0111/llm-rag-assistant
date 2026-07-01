from dataclasses import dataclass

from app.llm.schemas.usage import TokenUsage


@dataclass
class LLMResponse:

    content: str

    provider: str

    model: str

    latency_ms: int

    finish_reason: str

    usage: TokenUsage