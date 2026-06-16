from sqlalchemy.orm import Session

from app.dao.user_dao import user_dao

from app.schemas.user_schema import UserResponse,LoginResponse

from app.exceptions.business_exception import (
    BusinessException
)

from app.exceptions.error_code import (
    USER_ALREADY_EXISTS,USER_NOT_FOUND,PASSWORD_ERROR
)
from app.core.security import (
    hash_password
)
from app.core.jwt import (
    create_access_token
)

from app.core.security import (
    verify_password
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
        
        password_hash = hash_password(password)

        user = user_dao.create_user(
            db,
            username,
            password_hash
        )

        return UserResponse(
            id=user.id,
            username=user.username
        )
    
    def login(
            self,
            db: Session,
            username,
            password
    ):
        user = user_dao.get_by_username(
            db,
            username
        )
        
        if not user:
            raise BusinessException(
            USER_NOT_FOUND,
            "用户不存在"
        )

        if not verify_password(
                password,
                user.password_hash
        ):
            raise BusinessException(
                PASSWORD_ERROR,
                "密码错误"
            )
        
        token = create_access_token(
            {
                "user_id": user.id,
                "username": user.username
            }
        )

        return LoginResponse(
            access_token=token,
            token_type="bearer"
        )


user_service = UserService()