from datetime import datetime

from pydantic import BaseModel


class TronWalletBaseDTO(BaseModel):
    address: str
    balance: float = 0
    bandwidth: int = 0
    energy: int = 0


class TronWalletCreateDTO(TronWalletBaseDTO):
    pass


class TronWalletUpdateDTO(TronWalletBaseDTO):
    pass


class TronWalletDTO(TronWalletBaseDTO):
    id: int
    created_at: datetime
    updated_at: datetime
