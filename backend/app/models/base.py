from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_class import AsyncBase


class TimeStampedBase(AsyncBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class IdBase(AsyncBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
