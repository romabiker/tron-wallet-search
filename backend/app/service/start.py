import logging

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import async_connection
from app.dao import user_dao
from app.dto import UserCreateDTO
from app.models import User
from app.service.base import ServiceBase

from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


class InitDbService(ServiceBase):
    """
    Service adds initial data
    """

    @async_connection
    async def __call__(self, **kwargs) -> None:  # type: ignore
        session: AsyncSession = kwargs["session"]

        user = await user_dao.get(
            session, filter_expr=and_(User.email == settings.FIRST_SUPERUSER)
        )
        if not user:
            user_in = UserCreateDTO(
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
            )
            await user_dao.create(session, user_in)
