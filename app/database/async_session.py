from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from app.config.settings import settings


async_engine = create_async_engine(
    settings.mysql_async_url,

    echo=True,

    pool_pre_ping=True,

    pool_recycle=3600
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,

    class_=AsyncSession,

    autoflush=False,

    expire_on_commit=False
)