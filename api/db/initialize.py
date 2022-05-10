import asyncio

from api.config import init_config
from api.db.models import db


async def initialize_db():
    """
    GINO db initialization for existing db.
    :return:
    """
    loop = asyncio.get_running_loop()
    config = init_config()
    postgres = config.postgres

    await db.set_bind(
        postgres.dsn,
        loop=loop,
        min_size=postgres.pool_min_size,
        max_size=postgres.pool_max_size,
    )
