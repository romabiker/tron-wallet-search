from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.core.base_class import Base


class AsyncBase(AsyncAttrs, Base):  # type:ignore[valid-type,misc]
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"  # type:ignore[no-any-return]


class TimeStampedBase(AsyncBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class IdBase(AsyncBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
