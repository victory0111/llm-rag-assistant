from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.business_exception import (
    BusinessException
)


async def business_exception_handler(
        request: Request,
        exc: BusinessException
):

    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None
        }
    )