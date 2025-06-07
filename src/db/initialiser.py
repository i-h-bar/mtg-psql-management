import contextlib

import aiofiles
from asyncpg import Pool
from asyncpg.exceptions import DuplicateObjectError, DuplicateTableError


async def create_tables(pool: Pool) -> None:
    async with aiofiles.open("../sql/create_tables.sql", encoding="utf-8") as file:
        with contextlib.suppress(DuplicateObjectError, DuplicateTableError):
            await pool.execute(await file.read())

    with contextlib.suppress(DuplicateObjectError, DuplicateTableError):
        await pool.execute("create extension pg_trgm;")
