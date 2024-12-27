from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TronWalletCreateDTO(BaseModel):
    address: str
    balance: float = 0
    bandwidth: int = 0
    energy: int = 0


class TronWalletUpdateDTO(BaseModel):
    balance: float = 0
    bandwidth: int = 0
    energy: int = 0


class TronWalletDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address: str
    balance: float = 0
    bandwidth: int = 0
    energy: int = 0
    created_at: datetime
    updated_at: datetime
