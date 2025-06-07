import asyncio
import contextlib
import logging
import sys
from pathlib import Path

import aiofiles
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from asyncpg import Pool, Record
from tqdm import tqdm

logger = logging.getLogger(__name__)


async def fetch_image(record: Record, session: ClientSession, pbar: tqdm, directory: str) -> None:
    proposed_path = f"{directory}{record['id']}.png"

    if not Path(proposed_path).exists():
        try:
            result = await session.get(record["scryfall_url"])
        except TimeoutError:
            pbar.update()
            return

        if result.status != 200:
            logger.warning(f"{result.status}: {result.content}")
            sys.exit(1)

        try:
            png = await result.read()
        except Exception:  # noqa: BLE001
            pbar.update()
            return

        async with aiofiles.open(proposed_path, "wb") as f:
            await f.write(png)

    pbar.update()


async def download_missing_card_images(pool: Pool) -> None:
    with contextlib.suppress(FileExistsError):
        Path("../../mtg_cards/images").mkdir(parents=True)

    all_urls = await pool.fetch("SELECT id, scryfall_url from image")
    all_urls = [record for record in all_urls if not Path(f"../../mtg_cards/images/{record['id']}.png").exists()]

    with tqdm(total=len(all_urls)) as pbar:
        pbar.set_description("Fetching missing card images")
        pbar.refresh()

        connector = TCPConnector(limit=5)
        async with ClientSession(connector=connector, timeout=ClientTimeout(total=300)) as session:
            await asyncio.gather(
                *(fetch_image(record, session, pbar, "../../mtg_cards/images/") for record in all_urls)
            )


async def download_missing_illustrations(pool: Pool) -> None:
    with contextlib.suppress(FileExistsError):
        Path("../../mtg_cards/illustrations").mkdir(parents=True)

    all_urls = await pool.fetch("SELECT id, scryfall_url from illustration")
    all_urls = [record for record in all_urls if not Path(f"../../mtg_cards/illustrations/{record['id']}.png").exists()]

    with tqdm(total=len(all_urls)) as pbar:
        pbar.set_description("Fetching missing illustrations")
        pbar.refresh()

        connector = TCPConnector(limit=5)
        async with ClientSession(connector=connector, timeout=ClientTimeout(total=300)) as session:
            await asyncio.gather(
                *(fetch_image(record, session, pbar, "../../mtg_cards/illustrations/") for record in all_urls)
            )


async def download_missing_images(pool: Pool) -> None:
    await download_missing_card_images(pool)
    await download_missing_illustrations(pool)
    logger.info(f"Card images can be found: {Path('../../mtg_cards/').absolute()!s}")
