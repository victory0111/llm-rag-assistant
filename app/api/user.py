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
from app.core.dependencies import get_current_user
from app.utils.response import success
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/register")
async def register(
        request: UserCreateRequest,
        db: AsyncSession = Depends(get_db)
):

    result = await user_service.register(
        db,
        request.username,
        request.password
    )

    return success(result)

@router.post("/login")
async def login(
        request: UserLoginRequest,
        db: AsyncSession = Depends(get_db)
):
    result = await user_service.login(
        db,
        request.username,
        request.password
    )
    return success(result)

@router.get("/me")
async def me(
        current_user=Depends(
            get_current_user
        )
):

    return success(
        current_user
    )
