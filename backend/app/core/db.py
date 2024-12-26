from datetime import datetime
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlmodel import Session, create_engine, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession


from app import crud
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

async_engine = create_async_engine(str(settings.SQLALCHEMY_ASYNC_DATABASE_URI))
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


def async_connection(method):
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

@async_connection
async def init_db(session: AsyncSession) -> None:
    res = await session.execute(select(User).where(User.email == settings.FIRST_SUPERUSER))
    user = res.scalars().one_or_none()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await crud.create_user(session=session, user_create=user_in)
