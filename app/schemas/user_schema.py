from pydantic import BaseModel
from pydantic import Field


class UserCreateRequest(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$', 
        description="用户名，仅允许字母、数字和下划线"
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=50,
        description="密码"
    )

class UserResponse(BaseModel):

    id: int

    username: str