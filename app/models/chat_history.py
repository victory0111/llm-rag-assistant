from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        index=True
    )

    question: Mapped[str] = mapped_column(
        Text
    )

    answer: Mapped[str] = mapped_column(
        Text
    )

    model_name: Mapped[str] = mapped_column(
        String(50)
    )