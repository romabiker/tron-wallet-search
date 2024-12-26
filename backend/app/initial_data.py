import logging

from sqlmodel import Session

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_connection
from asyncio import run
from app.models import User

from app.core.db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    await init_db()


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    run(main())
