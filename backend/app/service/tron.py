from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from core.config import settings
from service.base import ServiceBase

from crud.tron_wallet import tron_wallet_crud


class ObtainTronAccountInfo(ServiceBase):
    
    def __init__(self):
        provider = AsyncHTTPProvider(api_key=settings.TRONGRID_API_KEY)
        self.tron_client = AsyncTron(provider)
    
    async def __call__(self, *args, **kwargs):
        res = await self.tron_client.get_account_balance('TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW')
        res = await self.tron_client.get_bandwidth('TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW')
        # res = await client.get_energy('TTzPiwbBedv7E8p4FkyPyeqq4RVoqRL3TW')
        
        tron_wallet_crud
        
    