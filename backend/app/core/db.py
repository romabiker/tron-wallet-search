from typing import Any

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

async_engine = create_async_engine(str(settings.SQLALCHEMY_ASYNC_DATABASE_URI))
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


def async_connection(method: callable) -> Any:
    """автоматизация создания и закрытие асинхронной сессии"""

    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper
