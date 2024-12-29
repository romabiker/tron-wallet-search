from collections.abc import Awaitable, Callable
from typing import Any

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_engine_kwargs(**kwargs):
    engine_kwargs = {
        "url": str(settings.SQLALCHEMY_ASYNC_DATABASE_URI),
        "future": True,
        "pool_recycle": 30 * 60,
        "isolation_level": "REPEATABLE READ",
    }
    engine_kwargs.update(**kwargs)

    if settings.DEBUG:
        engine_kwargs.update({"echo": True})
    return engine_kwargs


async_engine = create_async_engine(**create_engine_kwargs())
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

FuncType = Callable[[Any, Any], Awaitable[Any]]


def async_connection(method: FuncType) -> FuncType:
    """автоматизация создания и закрытие асинхронной сессии"""

    async def wrapper(*args, **kwargs) -> Any:
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
