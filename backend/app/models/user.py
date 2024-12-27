from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import IdBase, TimeStampedBase


class User(IdBase, TimeStampedBase):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    full_name: Mapped[str | None] = mapped_column()
