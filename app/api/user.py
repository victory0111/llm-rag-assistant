from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.deps import get_db

from app.schemas.user_schema import (
    UserCreateRequest,
    UserLoginRequest
)

from app.service.user_service import (
    user_service
)

from app.utils.response import success


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register")
async def register(
        request: UserCreateRequest,
        db: Session = Depends(get_db)
):

    result = user_service.register(
        db,
        request.username,
        request.password
    )

    return success(result)

@router.post("/login")
async def login(
        request: UserLoginRequest,
        db: Session = Depends(get_db)
):
    result = user_service.login(
        db,
        request.username,
        request.password
    )
    return success(result)
