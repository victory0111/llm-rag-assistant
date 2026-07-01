import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import settings
from app.utils.logger import logger
from app.utils.decorators import log_request, time_cost
from app.schemas.chat_schema import ChatResponse
from app.exceptions.business_exception import BusinessException
from app.dao.chat_history_dao import chat_history_dao



class ChatService:

    @log_request
    @time_cost
    async def chat(self, question: str, db: AsyncSession, user_id: int):  # 2. 增加 db 和 user_id 参数

        logger.info(f"用户问题: {question}")
        await asyncio.sleep(1)  # 模拟耗时操作

        logger.info("开始检索知识库...")
        await asyncio.sleep(1)
        logger.info("检索完成")

        logger.info("开始调用LLM...")
        await asyncio.sleep(1)
        logger.info("LLM生成完成")

        # 3. 生成回答
        answer = f"模拟回答：{question}"

        # 4. 保存聊天记录（注意：这里不需要 await db.commit()，由 get_db 依赖统一管理事务）
        await chat_history_dao.create_chat_history(
            db=db,
            user_id=user_id,
            question=question,
            answer=answer,
            model_name=settings.model_name
        )

        # 5. 返回响应
        return ChatResponse(
            question=question,
            answer=answer,
            model=settings.model_name
        )


chat_service = ChatService()