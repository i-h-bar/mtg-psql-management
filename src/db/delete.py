from asyncpg import Pool

from db.index import delete_indexes
from db.materialized_view import drop_all_mv


async def delete_index_and_mv(pool: Pool) -> None:
    await delete_indexes(pool)
    await drop_all_mv(pool)
