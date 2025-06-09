import asyncio

from asyncpg import Pool

from db import queries
from db.materialized_view import drop_all_mv


async def delete_index_and_mv(pool: Pool) -> None:
    await drop_all_mv(pool)


async def truncate_combos(pool: Pool) -> None:
    await pool.execute(queries.combo.TRUNCATE)


async def truncate_tokens(pool: Pool) -> None:
    await pool.execute(queries.related_token.TRUNCATE)


async def truncate_changeable_tables(pool: Pool) -> None:
    await asyncio.gather(truncate_tokens(pool), truncate_combos(pool))
