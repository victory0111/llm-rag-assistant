from fastapi import APIRouter
from app.service.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat API"])

@router.get("")
async def get_chat():
    """
    GET /chat 接口
    职责：仅负责调用 Service 层并返回响应
    """
    # 直接调用 Service 层的方法，不写任何额外逻辑
    return ChatService.get_hello_rag()
