from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.config.settings import settings
from app.core.exception_handler import (
    business_exception_handler
)
from app.exceptions.business_exception import (
    BusinessException
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

app.add_exception_handler(
    BusinessException,
    business_exception_handler
)
app.include_router(chat_router)