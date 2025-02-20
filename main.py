import asyncio
import json
import os

import aiofiles
from dotenv import load_dotenv
from tqdm import tqdm

import asyncpg
from db.insert import insert_card

load_dotenv()


async def main():
    async with aiofiles.open(os.getenv("FILE"), encoding="utf-8") as file:
        data = json.loads(await file.read())

    async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
        card_ids = set(await pool.fetchval("select array_agg(cast(id as varchar)) from card;"))
        data = tuple(card for card in data if card["id"] not in card_ids and card.get("set_type") != "memorabilia")
        pbar = tqdm(total=len(data))

        await asyncio.gather(*(insert_card(card, pbar, pool) for card in data))



if __name__ == '__main__':
    asyncio.run(main())