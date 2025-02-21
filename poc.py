import asyncio
import os
import sys
from pathlib import Path

import aiofiles
import asyncpg
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from asyncpg import Record
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


async def fetch_image(record: Record, session: ClientSession, pbar: tqdm) -> None:
    proposed_path = f"images/{record["front_id"]}.png"

    if not Path(proposed_path).exists():
        try:
            result = await session.get(record["front_scryfall_url"])
        except TimeoutError:
            return

        if result.status != 200:
            print(f"{result.status}: {result.content}")
            sys.exit(1)

        try:
            png = await result.read()
        except Exception:
            return

        async with aiofiles.open(proposed_path, "wb") as f:
            await f.write(png)

    pbar.update()


async def main():
    async with asyncpg.create_pool(os.getenv("PSQL_URI")) as pool:
        all_urls = await pool.fetch("SELECT front_id, front_scryfall_url from distinct_cards")

    all_urls = [record for record in all_urls if not Path(f"images/{record["front_id"]}.png").exists()]

    pbar = tqdm(total=len(all_urls))
    pbar.set_description("Fetching images")
    pbar.refresh()

    connector = TCPConnector(limit=10)
    async with ClientSession(connector=connector, timeout=ClientTimeout(total=120)) as session:
        for record in all_urls:
            await fetch_image(record, session, pbar)


if __name__ == '__main__':
    asyncio.run(main())
