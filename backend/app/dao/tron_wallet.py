from app.dao.base import DAOBase
from app.dto import TronWalletCreateDTO, TronWalletDTO, TronWalletUpdateDTO
from app.models.tron_wallet import TronWallet


class TronWalletDAO(
    DAOBase[TronWallet, TronWalletCreateDTO, TronWalletUpdateDTO, TronWalletDTO]
): ...


tron_wallet_dao = TronWalletDAO(TronWallet, TronWalletDTO)
