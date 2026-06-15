from fastapi import APIRouter
from app.service.chat_service import (
    chat_service
)
from app.utils.decorators import log_exceptions
from app.config.settings import settings
from pydantic import BaseModel
from app.utils.response import success
from app.schemas.chat_schema import ChatRequest

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "欢迎使用 RAG 助手！请访问 /chat 开始对话。"}
@router.post("/chat")
async def chat(request: ChatRequest):

    result = await chat_service.chat(
        request.question
    )
    return success(result)

@router.get("/health")
@log_exceptions  # 使用刚刚实现的异常日志装饰器
async def health_check():
    """应用健康检查接口"""
    return {
        "status": "ok",
        "app_name": settings.app_name,  # 从配置中心读取应用名
        "version": settings.app_version
    }

