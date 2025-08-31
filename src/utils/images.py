import contextlib
import logging
import os
import sys
from pathlib import Path

import aiofiles
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from asyncpg import Pool, Record
from dotenv import load_dotenv
from tqdm import tqdm

logger = logging.getLogger(__name__)

load_dotenv()


async def fetch_image(record: Record, session: ClientSession, pbar: tqdm, directory: Path) -> None:
    proposed_path = directory / f"{record['id']}.png"

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


async def download_missing_card_images(pool: Pool, base_dir: Path) -> None:
    images_dir = base_dir / "images"
    with contextlib.suppress(FileExistsError):
        images_dir.mkdir(parents=True)

    all_urls = await pool.fetch("SELECT id, scryfall_url from image")
    all_urls = [record for record in all_urls if not (images_dir / f"{record['id']}.png").exists()]

    with tqdm(total=len(all_urls)) as pbar:
        pbar.set_description("Fetching missing card images")
        pbar.refresh()

        connector = TCPConnector(limit=5)
        async with ClientSession(connector=connector, timeout=ClientTimeout(total=300)) as session:
            for record in all_urls:
                await fetch_image(record, session, pbar, images_dir)


async def download_missing_illustrations(pool: Pool, base_dir: Path) -> None:
    illustration_dir = base_dir / "illustrations"
    with contextlib.suppress(FileExistsError):
        illustration_dir.mkdir(parents=True)

    all_urls = await pool.fetch("SELECT id, scryfall_url from illustration")
    all_urls = [record for record in all_urls if not (illustration_dir / f"{record['id']}.png").exists()]

    with tqdm(total=len(all_urls)) as pbar:
        pbar.set_description("Fetching missing illustrations")
        pbar.refresh()

        connector = TCPConnector(limit=5)
        async with ClientSession(connector=connector, timeout=ClientTimeout(total=300)) as session:
            for record in all_urls:
                await fetch_image(record, session, pbar, illustration_dir)


async def download_missing_images(pool: Pool) -> None:
    base_dir = Path(os.getenv("IMAGES_DIR"))
    await download_missing_card_images(pool, base_dir)
    await download_missing_illustrations(pool, base_dir)
    logger.info(f"Card images can be found: {base_dir.resolve().absolute()!s}")
