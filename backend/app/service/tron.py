import asyncio
import logging

from httpx import HTTPStatusError
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound
from tronpy.providers import AsyncHTTPProvider

from app.core.config import settings
from app.core.db import async_connection
from app.dao.tron_wallet import tron_wallet_dao
from app.dto.tron_wallet import TronWalletCreateDTO, TronWalletDTO, TronWalletUpdateDTO
from app.models.tron_wallet import TronWallet
from app.service.base import ServiceBase

logger = logging.getLogger(__name__)


class UpdateOrCreateTronAccountInfoService(ServiceBase):
    def __init__(self) -> None:
        provider = AsyncHTTPProvider(api_key=settings.TRONGRID_API_KEY)
        self.tron_client = AsyncTron(provider)

    async def __call__(
        self, addr: str
    ) -> tuple[bool, TronWalletDTO] | tuple[bool, str]:
        """
        Service gathers tron account info by tronpy lib and saves or updates it in database
        """
        is_ok = False
        error_msg = ""
        try:
            async with asyncio.TaskGroup() as tg:
                bandwidth_task = tg.create_task(self.tron_client.get_bandwidth(addr))
                account_balance_task = tg.create_task(
                    self.tron_client.get_account_balance(addr)
                )
                # energy_task = tg.create_task(self.tron_client.get_energy(addr)) Не реализован
        except* AddressNotFound:
            logger.error("Address %s is not found", addr)
            error_msg = f"Address {addr} is not found"
        except* HTTPStatusError as http_error:
            logger.error("Http errors: %s", str(http_error.exceptions))
            error_msg = "Http errors. Retry later"
        else:
            is_ok = True
        if not is_ok:
            return is_ok, error_msg

        data = {
            "address": addr,
            "bandwidth": bandwidth_task.result(),
            "balance": float(account_balance_task.result()),
            "energy": 0,  # todo
        }
        tron_wallet_dto = await self._save_data(data, addr)
        return is_ok, tron_wallet_dto

    @async_connection
    async def _save_data(self, data: dict, addr: str, **kwargs) -> TronWalletDTO:  # type:ignore[no-untyped-def]
        session: AsyncSession = kwargs["session"]
        tron_wallet_filter = and_(TronWallet.address == addr)
        tron_wallet = await tron_wallet_dao.get(session, filter_expr=tron_wallet_filter)
        if tron_wallet:
            update_dto = TronWalletUpdateDTO.model_validate(**data)
            tron_wallet_dto = await tron_wallet_dao.update(
                session, tron_wallet_filter, update_dto
            )
        else:
            create_dto = TronWalletCreateDTO.model_validate(**data)
            tron_wallet_dto = await tron_wallet_dao.create(session, create_dto)
        return tron_wallet_dto


update_or_create_tron_account_info_service = UpdateOrCreateTronAccountInfoService()
