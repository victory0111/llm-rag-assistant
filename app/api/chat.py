from fastapi import APIRouter
from app.service.chat_service import (
    chat_service
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.chat_service import chat_service
from app.utils.decorators import log_exceptions
from app.config.settings import settings
from app.utils.response import success
from app.schemas.chat_schema import ChatRequest
from app.database.async_deps import get_db
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "欢迎使用 RAG 助手！请访问 /chat 开始对话。"}
@router.post("/chat")
async def chat(request: ChatRequest, 
               db: AsyncSession = Depends(get_db),
               user_id: int = 1
               ):

    result = await chat_service.chat(
        request.question,
        db,
        user_id
    )
    return success(result)

@router.get("/health")
@log_exceptions  
async def health_check():
    """应用健康检查接口"""
    return {
        "status": "ok",
        "app_name": settings.app_name,  # 从配置中心读取应用名
        "version": settings.app_version
    }

