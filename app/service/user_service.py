from sqlalchemy.orm import Session

from app.dao.user_dao import user_dao

from app.schemas.user_schema import UserResponse

from app.exceptions.business_exception import (
    BusinessException
)

from app.exceptions.error_code import (
    USER_ALREADY_EXISTS
)


class UserService:

    def register(
            self,
            db: Session,
            username: str,
            password: str
    ):

        user = user_dao.get_by_username(
            db,
            username
        )

        if user:

            raise BusinessException(
                USER_ALREADY_EXISTS,
                "用户名已存在"
            )

        user = user_dao.create_user(
            db,
            username,
            password
        )

        return UserResponse(
            id=user.id,
            username=user.username
        )


user_service = UserService()