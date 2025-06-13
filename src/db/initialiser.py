import contextlib

import aiofiles
from asyncpg import Pool
from asyncpg.exceptions import DuplicateObjectError, DuplicateTableError


async def create_table(pool: Pool, table_query: str) -> None:
    with contextlib.suppress(DuplicateObjectError, DuplicateTableError):
        await pool.execute(table_query)


async def create_tables(pool: Pool) -> None:
    async with aiofiles.open("../sql/create_tables.sql", encoding="utf-8") as file:
        table_queries = await file.read()

    for query in table_queries.replace("\n", "").split(";"):
        if query:
            await create_table(pool, query)

    with contextlib.suppress(DuplicateObjectError, DuplicateTableError):
        await pool.execute("create extension pg_trgm;")
