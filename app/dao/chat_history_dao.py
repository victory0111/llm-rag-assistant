from app.models.chat_history import (
    ChatHistory
)
class ChatHistoryDAO:
   async def create_chat_history(
            self,
            db,
            user_id,
            question,
            answer,
            model_name
    ):
      history = ChatHistory(
          user_id=user_id,
          question=question,
          answer=answer,
          model_name=model_name
      )

      db.add(history)

      await db.commit()

      await db.refresh(history)

      return history

chat_history_dao = ChatHistoryDAO()
