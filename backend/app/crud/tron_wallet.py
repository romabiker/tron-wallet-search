from app.crud.base import CRUDBase
from app.models import TronWallet
from app.dto.tron_wallet import TronWalletCreateDTO, TronWalletUpdateDTO, TronWalletDTO


class TronWalletCRUD(CRUDBase[TronWallet, TronWalletUpdateDTO, TronWalletDTO]):
    pass


tron_wallet_crud = TronWalletCRUD(TronWallet)
