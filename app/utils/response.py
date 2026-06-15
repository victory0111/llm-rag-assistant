from app.schemas.response_schema import ApiResponse


def success(data=None):

    return ApiResponse(
        code=200,
        message="success",
        data=data
    )


def fail(code: int, message: str):

    return ApiResponse(
        code=code,
        message=message,
        data=None
    )