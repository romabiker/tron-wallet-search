import logging

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import async_connection
from app.dao import user_dao
from app.dto import UserCreateDTO
from app.models import User
from app.service.base import ServiceBase

logger = logging.getLogger(__name__)


class InitDbService(ServiceBase):
    """
    Service adds initial data
    """

    @async_connection
    async def __call__(self, **kwargs) -> None:
        session: AsyncSession = kwargs["session"]

        user = await user_dao.get(
            session, filter_expr=and_(User.email == settings.FIRST_SUPERUSER)
        )
        if not user:
            user_in = UserCreateDTO(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            await user_dao.create_user(session=session, user_create=user_in)
