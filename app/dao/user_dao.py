from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserDAO:

    async def get_by_username(
            self,
            db: AsyncSession,
            username: str
    ):
        stmt = select(User).where(
        User.username == username
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
            self,
            db: AsyncSession,
            username: str,
            password_hash
    ):

        user = User(
            username=username,
            password_hash=password_hash
        )


        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user


user_dao = UserDAO()