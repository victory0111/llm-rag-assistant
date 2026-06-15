from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class Base(DeclarativeBase):
        # 统一的创建时间字段
    create_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), comment="创建时间"
    )
    # 统一的更新时间字段
    update_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), onupdate=func.now(), comment="更新时间"
    )