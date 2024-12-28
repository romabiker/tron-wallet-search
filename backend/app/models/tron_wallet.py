from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import IdBase, TimeStampedBase


class TronWallet(IdBase, TimeStampedBase):
    address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
