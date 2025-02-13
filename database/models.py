from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

from database.connect import engine

Base = declarative_base()


class UserAction(Base):
    __tablename__ = "user_actions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String)
    action_type = Column(String, nullable=False)
    button_name = Column(String)
    message_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


async def init_models():
    """Створення таблиць при запуску"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
