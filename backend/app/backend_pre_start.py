import logging
from asyncio import run

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import async_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
@async_connection
async def init(session: AsyncSession) -> None:
    try:
        await session.execute(select(1))
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    run(main())
