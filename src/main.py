import asyncio
import logging
import os
import sys

import asyncpg
from dotenv import load_dotenv

from db.initialiser import create_tables
from db.insert import insert_missing_data
from utils.data import load_scryfall_data
from utils.images import download_missing_images

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    data = await load_scryfall_data()
    if not data:
        logger.error("Scryfall data could not be loaded.")
        sys.exit(1)

    async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
        try:
            card_ids = set(await pool.fetchval("select array_agg(cast(id as varchar)) from card;") or [])
        except asyncpg.exceptions.UndefinedTableError:
            await create_tables(pool)
            card_ids = set()

        data = tuple(
            card
            for card in data
            if card["id"] not in card_ids
            and card.get("set_type") != "memorabilia"
            and card.get("image_uris", {}).get("png") != "https://errors.scryfall.com/soon.jpg"
        )

        if data:
            await insert_missing_data(data, pool)
        else:
            logger.info("DB is up to date.")

        await download_missing_images(pool)


if __name__ == "__main__":
    asyncio.run(main())
