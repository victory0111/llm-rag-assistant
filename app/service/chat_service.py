import asyncio
from app.config.settings import settings
from app.utils.logger import logger
from app.utils.decorators import (
    log_request,
    time_cost
)
from app.config.settings import settings
from app.schemas.chat_schema import ChatResponse
from app.exceptions.business_exception import (
    BusinessException
)

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

        return ChatResponse(
            question=question,
            answer=f"模拟回答：{question}",
            model=settings.model_name
        )
    

chat_service = ChatService()