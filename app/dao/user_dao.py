from sqlalchemy.orm import Session

from app.models.user import User


class UserDAO:

    def get_by_username(
            self,
            db: Session,
            username: str
    ):

        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    def create_user(
            self,
            db: Session,
            username: str,
            password_hash
    ):

        user = User(
            username=username,
            password_hash=password_hash
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user


user_dao = UserDAO()