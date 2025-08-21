import asyncio
import os

import asyncpg
from dotenv import load_dotenv

from db.queries.materialised_views.drop_all import DROP_MAT_VIEWS
from db.queries.tables.drop_all import DROP_TABLES

load_dotenv()


async def main() -> None:
    async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
        await pool.execute(DROP_MAT_VIEWS)
        await pool.execute(DROP_TABLES)


if __name__ == "__main__":
    asyncio.run(main())
