import asyncio
from app.config.settings import settings
from app.utils.logger import logger
from app.utils.decorators import (
    log_request,
    time_cost
)
from app.config.settings import settings

class ChatService:

    @log_request
    @time_cost
    async def chat(self, question: str):

        logger.info(
            f"用户问题: {question}"
        )

        await asyncio.sleep(1)

        logger.info(
            "开始检索知识库..."
        )

        await asyncio.sleep(1)

        logger.info(
            "检索完成"
        )

        logger.info(
            "开始调用LLM..."
        )

        await asyncio.sleep(1)

        logger.info(
            "LLM生成完成"
        )

        return {
            "question": question,
            "model": settings.model_name,
            "temperature": settings.temperature,
            "answer": "模拟回答"
        }
    

chat_service = ChatService()