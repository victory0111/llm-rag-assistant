from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMRequest:

    user_id: Optional[int]

    question: str

    system_prompt: Optional[str]

    temperature: float

    top_p: float

    max_tokens: int

    stream: bool = False