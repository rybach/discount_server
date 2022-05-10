import asyncio

from api.db.models import db


async def initialize_db(db_settings):
    """
    GINO db initialization for existing db.
    :return:
    """
    loop = asyncio.get_running_loop()

    await db.set_bind(
        db_settings.dsn,
        loop=loop,
        min_size=db_settings.pool_min_size,
        max_size=db_settings.pool_max_size,
    )
