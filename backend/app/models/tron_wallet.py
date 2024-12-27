from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import Field

from app.models.base import IdBase, TimeStampedBase


class TronWallet(IdBase, TimeStampedBase):
    address: str = Field(min_length=1, max_length=255, unique=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
