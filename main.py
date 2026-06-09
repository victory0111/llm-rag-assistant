from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


app.include_router(chat_router)