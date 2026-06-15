from pydantic import BaseModel
from pydantic import Field


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="用户问题"
    )

class ChatResponse(BaseModel):

    question: str

    answer: str

    model: str