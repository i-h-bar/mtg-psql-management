import asyncio
import sys
from pathlib import Path

import aiofiles
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from asyncpg import Pool, Record
from tqdm import tqdm


async def fetch_image(record: Record, session: ClientSession, pbar: tqdm, directory: str) -> None:
    proposed_path = f"{directory}{record["id"]}.png"

    if not Path(proposed_path).exists():
        try:
            result = await session.get(record["scryfall_url"])
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


async def download_missing_card_images(pool: Pool) -> None:
    all_urls = await pool.fetch("SELECT card.id, image.scryfall_url from card join image on card.image_id = image.id")
    all_urls = [record for record in all_urls if not Path(f"images/{record["id"]}.png").exists()]

    with tqdm(total=len(all_urls)) as pbar:
        pbar.set_description("Fetching missing card images")
        pbar.refresh()

        connector = TCPConnector(limit=5)
        async with ClientSession(connector=connector, timeout=ClientTimeout(total=300)) as session:
            await asyncio.gather(*(fetch_image(record, session, pbar, "images/") for record in all_urls))


async def download_missing_illustrations(pool: Pool) -> None:
    all_urls = await pool.fetch("SELECT id, scryfall_url from illustration")
    all_urls = [record for record in all_urls if not Path(f"illustrations/{record["id"]}.png").exists()]

    with tqdm(total=len(all_urls)) as pbar:
        pbar.set_description("Fetching missing illustrations")
        pbar.refresh()

        connector = TCPConnector(limit=5)
        async with ClientSession(connector=connector, timeout=ClientTimeout(total=300)) as session:
            await asyncio.gather(*(fetch_image(record, session, pbar, "illustrations/") for record in all_urls))