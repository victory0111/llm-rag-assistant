from typing import Optional
from fastapi import Header, HTTPException
# 引入你的业务异常和错误码
from app.exceptions.business_exception import BusinessException
from app.exceptions.error_code import NOT_LOGIN, TOKEN_INVALID
from app.core.jwt import verify_token


def get_current_user(
    # 关键修改：显式指定 alias="Authorization" (大写A)
    # 这样 Swagger 生成的文档里就会显示 Authorization，且发送时也是大写
    authorization: str = Header(None)
):
    if not authorization:
        raise BusinessException(code=NOT_LOGIN, message="未登录，请先进行登录操作")

    # 增加防御性编程：防止前端没传 Bearer 前缀导致报错
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
         # 如果格式不对，也视为未登录或Token格式错误
         raise BusinessException(code=TOKEN_INVALID, message="Token格式错误，需以 Bearer 开头")

    token = parts[1]

    try:
        payload = verify_token(token)
        return payload
    except Exception:
        raise BusinessException(code=TOKEN_INVALID, message="Token无效或已过期")