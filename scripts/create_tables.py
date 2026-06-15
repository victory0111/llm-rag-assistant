from app.database.base import Base
from app.database.session import engine

from app.models.user import User
from app.models.chat_history import ChatHistory

Base.metadata.create_all(engine)

print("创建成功")