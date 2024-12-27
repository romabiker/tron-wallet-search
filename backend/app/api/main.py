from fastapi import APIRouter

from app.api.routes import tron_wallet, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(tron_wallet.router)
