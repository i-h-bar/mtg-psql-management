import asyncio
import json
import os

import aiofiles
from dotenv import load_dotenv
from tqdm import tqdm

import asyncpg

from db.index import add_indexes, delete_indexes
from db.insert import insert_card
from db.insert_tokens import insert_token_relations
from db.materialized_view import create_mv_for_set, create_mv_for_artist, drop_all_mv, create_mv_distinct

load_dotenv()


async def main():
    async with aiofiles.open(os.getenv("FILE"), encoding="utf-8") as file:
        data = json.loads(await file.read())

    async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
        try:
            card_ids = set(await pool.fetchval("select array_agg(cast(id as varchar)) from card;") or [])
        except asyncpg.exceptions.UndefinedTableError:
            async with aiofiles.open("sql/create_tables.sql", encoding="utf-8") as file:
                try:
                    await pool.execute(await file.read())
                except (asyncpg.exceptions.DuplicateObjectError, asyncpg.exceptions.DuplicateTableError):
                    pass

            try:
                await pool.execute("create extension pg_trgm;")
            except (asyncpg.exceptions.DuplicateObjectError, asyncpg.exceptions.DuplicateTableError):
                pass

            card_ids = set()

        data = tuple(card for card in data if card["id"] not in card_ids and card.get("set_type") != "memorabilia")

        if data:
            await delete_indexes(pool)
            await drop_all_mv(pool)

            with tqdm(total=len(data)) as pbar:
                pbar.set_description("Inserting Cards")
                pbar.refresh()
                await asyncio.gather(*(insert_card(card, pbar, pool) for card in data))

            await insert_token_relations(pool)

            await create_mv_distinct(pool)

            all_sets = await pool.fetchval("select array_agg(normalised_name) from set;")
            with tqdm(total=len(all_sets)) as pbar:
                pbar.set_description("Creating set MVs")
                pbar.refresh()
                await asyncio.gather(*(create_mv_for_set(set_, pool, pbar) for set_ in all_sets))

            all_artists = await pool.fetchval("select array_agg(normalised_name) from artist;")
            with tqdm(total=len(all_artists)) as pbar:
                pbar.set_description("Creating artist MVs")
                pbar.refresh()
                await asyncio.gather(*(create_mv_for_artist(artist, pool, pbar) for artist in all_artists))

            await add_indexes(pool)


if __name__ == '__main__':
    asyncio.run(main())